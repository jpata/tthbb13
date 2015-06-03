from TTH.MEAnalysis.VHbbTree import lvec
import ROOT
import copy
#Load the MEM integrator libraries
# ROOT.gSystem.Load("libFWCoreFWLite")
# ROOT.gROOT.ProcessLine('AutoLibraryLoader::enable();')
# ROOT.gSystem.Load("libFWCoreFWLite")
ROOT.gSystem.Load("libCintex")
ROOT.gROOT.ProcessLine('ROOT::Cintex::Cintex::Enable();')
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")

from ROOT import MEM

#Pre-define shorthands for permutation and integration variable vectors
CvectorPermutations = getattr(ROOT, "std::vector<MEM::Permutations::Permutations>")
CvectorPSVar = getattr(ROOT, "std::vector<MEM::PSVar::PSVar>")
#CmapDistributionTypeTH3D = getattr(ROOT, "std::map<MEM::DistributionType::DistributionType,TH3D>")

from TTH.MEAnalysis.Analyzer import FilterAnalyzer
class MECategoryAnalyzer(FilterAnalyzer):
    """
    Performs ME categorization
    FIXME: doc
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(MECategoryAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.cat_map = {"NOCAT":-1, "cat1": 1, "cat2": 2, "cat3": 3, "cat6":6}
        self.btag_cat_map = {"NOCAT":-1, "L": 0, "H": 1}

    def beginLoop(self, setup):
        super(MECategoryAnalyzer, self).beginLoop(setup)

        for c in ["NOCAT", "cat1", "cat2", "cat3", "cat6"]:
            self.counters["processing"].register(c)

    def process(self, event):
        self.counters["processing"].inc("processed")

        cat = "NOCAT"
        pass_btag_lr = (self.conf.jets["untaggedSelection"] == "btagLR" and
            event.btag_LR_4b_2b > self.conf.mem["btagLRCut"][event.cat]
        )
        pass_btag_csv = (self.conf.jets["untaggedSelection"] == "btagCSV" and
            len(event.selected_btagged_jets) >= 4
        )
        cat_btag = "NOCAT"

        if pass_btag_lr or pass_btag_csv:
            cat_btag = "H"

        if event.is_sl:

            #at least 6 jets, if 6, Wtag in [60,100], if more Wtag in [72,94]
            if ((len(event.good_jets) == 6 and event.Wmass >= 60 and event.Wmass < 100) or
               (len(event.good_jets) > 6 and event.Wmass >= 72 and event.Wmass < 94)):
               cat = "cat1"
               #W-tagger fills wquark_candidate_jets
            #at least 6 jets, no W-tag
            elif len(event.good_jets) >= 6:
                cat = "cat2"
            #one W daughter missing
            elif len(event.good_jets) == 5:
                event.wquark_candidate_jets = event.buntagged_jets
                cat = "cat3"
        elif event.is_dl and len(event.good_jets)>=4:
            event.wquark_candidate_jets = []
            cat = "cat6"

        self.counters["processing"].inc(cat)
        event.cat = cat
        event.cat_btag = cat_btag
        event.catn = self.cat_map.get(cat, -1)
        event.cat_btag_n = self.btag_cat_map.get(cat_btag, -1)

        passes = True
        if passes:
            self.counters["processing"].inc("passes")
        return passes

class MEMConfig:
    def __init__(self):
        self.cfg = MEM.MEMConfig()
        self.cfg.defaultCfg()
        self.b_quark_candidates = lambda event: event.selected_btagged_jets
        self.l_quark_candidates = lambda event: event.wquark_candidate_jets
        self.lepton_candidates = lambda event: event.good_leptons
        self.met_candidates = lambda event: event.met
        self.transfer_function_method = MEM.TFMethod.External

        self.do_calculate = lambda event, config: False
        self.mem_assumptions = set([])
        self.enabled = True

    def configure_btag_pdf(self, conf):
        """
        Add the jet b-tag discriminator distributions to the MEM::MEMConfig object.
        The distributions are 3D in (pt, |eta|, CSV).
        """
        #btag_map = CmapDistributionTypeTH1F()
        
        for x,y in [
            ("b", MEM.DistributionType.csv_b),
            ("c", MEM.DistributionType.csv_c),
            ("l", MEM.DistributionType.csv_l),
        ]:
            self.cfg.add_distribution_global(
                y,
                conf.BTagLRAnalyzer.csv_pdfs[(x, "pt_eta")]
            )

    def configure_transfer_function(self, conf):
        for nb in [0, 1]:
            for fl1, fl2 in [('b', MEM.TFType.bLost), ('l', MEM.TFType.qLost)]:
                tf = conf.tf_matrix[fl1][nb].Make_CDF()
                #set pt cut for efficiency function
                tf.SetParameter(0, conf.jets["pt"])
                tf.SetNpx(10000)
                tf.SetRange(0, 500)
                self.cfg.set_tf_global(fl2, nb, tf)

    def configure_minimize(self, orig_mem):
        self.cfg.do_minimize = 1

    def configure_sudakov(self, orig_mem):
        self.cfg.int_code |= MEM.IntegrandType.Sudakov
        njets = 6
        if "dl" in orig_mem.mem_assumptions:
            njets = 4
        if "1qW" in orig_mem.mem_assumptions:
            njets -= 1
        self.do_calculate = lambda event, conf, njets=njets: (
            orig_mem.do_calculate(event, conf) and
            len(event.good_jets) == njets
        )

    def configure_newtf(self, orig_mem):
        self.cfg.transfer_function_method = MEM.TFMethod.External

    def configure_recoil(self, orig_mem):
        self.cfg.int_code |= MEM.IntegrandType.Recoil

class MEAnalyzer(FilterAnalyzer):
    """
    Performs ME calculation using the external integrator.
    It supports multiple MEM algorithms at the same time, configured via the
    self.configs dictionary. The outputs are stored in a vector in the event.

    The ME algorithms are run only in case the njet/nlep/Wtag category (event.cat)
    is in the accepted categories specified in the config.
    Additionally, we require the b-tagging category (event.cat_btag) to be "H" (high).

    For each ME configuration on each event, the jets which are counted to be b-tagged
    in event.selected_btagged_jets are added as the candidates for t->b (W) or h->bb.
    These jets must be exactly 4, otherwise no permutation is accepted (in case
    using BTagged/QUntagged assumptions).

    Any additional jets are assumed to come from the hadronic W decay. These are
    specified in event.wquark_candidate_jets.

    Based on the event njet/nlep/Wtag category, if a jet fmor the W is counted as missing,
    it is integrated over using additional variables set by self.vars_to_integrate.

    The MEM top pair hypothesis (di-leptonic or single leptonic top pair) is chosen based
    on the reconstructed lepton multiplicity (event.good_leptons).

    The algorithm is shortly as follows:
    1. check if event passes event.cat and event.cat_btag
    2. loop over all MEM configurations i=[0...Nmem)
        2a. add all 4 b-tagged jets to integrator
        2b. add all 0-3 untagged jets to integrator
        2c. add all leptons to integrator
        2d. decide SL/DL top pair hypo based on leptons
        2e. based on event.cat, add additional integration vars
        2f. run ME integrator for both tth and ttbb hypos
        2g. save output in event.mem_output_tth[i] (or ttbb)
        2i. clean up event in integrator

    Relies on:
    event.good_jets, event.good_leptons, event.cat, event.input.met_pt

    Produces:
    mem_results_tth (MEMOutput): probability for the tt+H(bb) hypothesis
    mem_results_ttbb (MEMOutput): probability for the tt+bb hypothesis

    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(MEAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

        self.configs = {

            #"SL_2qW": MEM.MEMConfig(),
            #"SL_2qW_gen": MEM.MEMConfig(),
            #"SL_1qW": MEM.MEMConfig(),
            #"SL_1qW_gen": MEM.MEMConfig(),
            #"DL": MEM.MEMConfig(),
            #"DL_gen": MEM.MEMConfig(),

            "SL_2w2h2t"   :  MEMConfig(),
            "SL_1w2h2t"   :  MEMConfig(),
            "SL_2w2h1t_h" :  MEMConfig(),
            "SL_2w2h1t_l" :  MEMConfig(),
            "SL_0w2h2t"   :  MEMConfig(),
            "SL_1w2h1t_h" :  MEMConfig(),
            "SL_1w2h1t_l" :  MEMConfig(),

            "SL_2qW": MEMConfig(),
            "SL_2qW_notag": MEMConfig(),
            "SL_2qW_gen": MEMConfig(),
            "SL_2qW_gen_nosmear": MEMConfig(),
            "SL_1qW": MEMConfig(),
            "SL_1qW_gen": MEMConfig(),
            "SL_1qW_gen_nosmear": MEMConfig(),
            "SL_0qW": MEMConfig(),
            "SL_1bT": MEMConfig(),
            "SL_1bTbar": MEMConfig(),
            "SL_1bH": MEMConfig(),
            "DL": MEMConfig(),
            "DL_gen": MEMConfig(),
            "DL_gen_nosmear": MEMConfig(),
        }

        #These MEM configurations will actually be considered for calculation
        self.memkeys = self.conf.mem["methodsToRun"]
        print "Running over MEM configurations"
        for nmem, memk in enumerate(self.memkeys):
            print "MEM", nmem, memk

        #Set the MEM
        for (k, v) in self.configs.items():
            v.configure_btag_pdf(self.conf)
            v.configure_transfer_function(self.conf)

        for k in ["DL_gen", "SL_2qW_gen", "SL_1qW_gen"]:
            self.configs[k].b_quark_candidates = lambda event: (
                event.b_quarks_gen if len(event.b_quarks_gen)>=4 else
                event.b_quarks_gen + event.unmatched_b_jets_gen
            )
            self.configs[k].l_quark_candidates = lambda event: event.l_quarks_gen
            self.configs[k].lepton_candidates = lambda event: event.good_leptons
            self.configs[k].met_candidates = lambda event: event.gen_met
            self.configs[k].cfg.int_code |= MEM.IntegrandType.SmearJets
            self.configs[k].cfg.int_code |= MEM.IntegrandType.SmearMET
        for k in ["DL_gen_nosmear", "SL_2qW_gen_nosmear", "SL_1qW_gen_nosmear"]:
            self.configs[k].b_quark_candidates = lambda event: (
                event.b_quarks_gen if len(event.b_quarks_gen)>=4 else
                event.b_quarks_gen + event.unmatched_b_jets_gen
            )
            self.configs[k].l_quark_candidates = lambda event: event.l_quarks_gen
            self.configs[k].lepton_candidates = lambda event: event.good_leptons
            self.configs[k].met_candidates = lambda event: event.gen_met
            #self.configs[k].cfg.int_code |= MEM.IntegrandType.Smear
        for x in ["SL_2qW", "SL_2qW_notag", "SL_2qW_gen", "SL_2qW_gen_nosmear"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(c.lepton_candidates(y)) == 1 and
                len(c.b_quark_candidates(y)) >= 4 and
                len(c.l_quark_candidates(y)) >= 2
            )
        for x in ["SL_1qW", "SL_1qW_gen", "SL_1qW_gen_nosmear"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(c.lepton_candidates(y)) == 1 and
                len(c.b_quark_candidates(y)) >= 4 and
                len(c.l_quark_candidates(y)) >= 1
            )
            self.configs[x].mem_assumptions.add("1qW")
        for x in ["SL_0qW"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(c.lepton_candidates(y)) == 1 and
                len(c.b_quark_candidates(y)) >= 4 and
                len(c.l_quark_candidates(y)) >= 1
            )
            self.configs[x].mem_assumptions.add("0qW")
        for x in ["SL_1bT", "SL_1bTbar", "SL_1bH"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(c.lepton_candidates(y)) == 1 and
                len(c.b_quark_candidates(y)) >= 3 and
                len(c.l_quark_candidates(y)) >= 2
            )
            k = x.split("_")[1]
            self.configs[x].mem_assumptions.add(k)
        for x in ["DL", "DL_gen", "DL_gen_nosmear"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(c.lepton_candidates(y)) == 2 and
                len(c.b_quark_candidates(y)) >= 4
            )
            self.configs[x].mem_assumptions.add("dl")

        for k in [
                "SL_2qW", "SL_2qW_notag", "SL_1qW", "SL_2qW_gen",
                "SL_1qW_gen", "SL_2qW_gen_nosmear", "SL_1qW_gen_nosmear",
                "SL_0qW", "SL_1bT", "SL_1bTbar", "SL_1bH"
            ]:
            self.configs[k].mem_assumptions.add("sl")

        for x in ["SL_2w2h2t", 
                  "SL_2w2h1t_h", "SL_2w2h1t_l", 
                  "SL_1w2h1t_h", "SL_1w2h1t_l"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(y.good_leptons) == 1 and
                len(c.b_quark_candidates(y)) >= 4 and
                len(c.l_quark_candidates(y)) >= 2 and
                y.cat_btag == "H"
            )
            self.configs[x].mem_assumptions.add("sl")

        for x in ["SL_1w2h2t", "SL_0w2h2t"]:
            self.configs[x].do_calculate = lambda y, c: (
                len(y.good_leptons) == 1 and
                len(c.b_quark_candidates(y)) >= 4 and
                len(c.l_quark_candidates(y)) >= 1 and
                y.cat_btag == "H"
            )
            self.configs[x].mem_assumptions.add("sl")


        for k in ["SL_2w2h1t_h", "SL_2w2h1t_l",
                  "SL_1w2h1t_h", "SL_1w2h1t_l"]:
            self.configs[k].cfg.defaultCfg(1.5)

        for k in ["SL_2w2h2t", 
                  "SL_1w2h2t", "SL_2w2h1t_h", "SL_2w2h1t_l", 
                  "SL_0w2h2t", "SL_1w2h1t_h", "SL_1w2h1t_l"]:
            self.configs[k].cfg.do_prefit = 1

        self.configs["SL_2w2h2t"].mem_assumptions.add("2w2h2t")
        self.configs["SL_1w2h2t"].mem_assumptions.add("1w2h2t")
        self.configs["SL_2w2h1t_l"].mem_assumptions.add("2w2h1t_l")
        self.configs["SL_0w2h2t"].mem_assumptions.add("0w2h2t")
        self.configs["SL_1w2h1t_h"].mem_assumptions.add("1w2h1t_h")
        self.configs["SL_1w2h1t_l"].mem_assumptions.add("1w2h1t_l")


        permutations = CvectorPermutations()
        #self.permutations.push_back(MEM.Permutations.BTagged)
        #self.permutations.push_back(MEM.Permutations.QUntagged)
        #self.permutations.push_back(MEM.Permutations.QQbarBBbarSymmetry)
        self.configs["SL_2qW_notag"].cfg.perm_pruning = permutations

        #Create additional configurations
        for strat, configure in [

                #Run with recoil instead of met
                ("Recoil", MEMConfig.configure_recoil),

                #apply sudakov factors
                ("Sudakov", MEMConfig.configure_sudakov),

                #apply sudakov factors
                ("NewTF", MEMConfig.configure_newtf),

                #run minimization
                ("Minimize", MEMConfig.configure_minimize)
            ]:
            for k in ["SL_2qW", "SL_1qW", "DL"]:
                kn = k + "_" + strat
                self.configs[kn] = copy.deepcopy(self.configs[k])
                self.configs[kn].cfg.defaultCfg()
                configure(self.configs[kn], self.configs[k])

        #only in 6J SL
        #self.configs["Sudakov"].do_calculate = (
        #    lambda x: len(x.good_jets) == 6 and
        #    len(x.good_leptons) == 1
        #)

        #Create the ME integrator.
        #Arguments specify the verbosity
        #the first argument:
        #../MEIntegratorStandalone/interface/Parameters.h:  enum DebugVerbosity { output=1, input=2, init=4, init_more=8, event=16, integration=32};
        self.integrator = MEM.Integrand(
            MEM.output,
            self.configs["SL_2qW"].cfg
        )

        #Create an emtpy std::vector<MEM::Permutations::Permutations>
        #self.permutations = CvectorPermutations()

        ##Assume that only jets passing CSV>0.5 are b quarks
        #self.permutations.push_back(MEM.Permutations.BTagged)

        ##Assume that only jets passing CSV<0.5 are l quarks
        #self.permutations.push_back(MEM.Permutations.QUntagged)

        #self.integrator.set_permutation_strategy(self.permutations)

        #Create an empty vector for the integration variables
        self.vars_to_integrate = CvectorPSVar()

    def add_obj(self, objtype, **kwargs):
        """
        Add an event object (jet, lepton, MET) to the ME integrator.

        objtype: specifies the object type
        kwargs: p4s: spherical 4-momentum (pt, eta, phi, M) as a tuple
                obsdict: dict of additional observables to pass to MEM
                tf_dict: Dictionary of MEM.TFType->TF1 of transfer functions
        """
        if kwargs.has_key("p4s"):
            pt, eta, phi, mass = kwargs.pop("p4s")
            v = ROOT.TLorentzVector()
            v.SetPtEtaPhiM(pt, eta, phi, mass);
        elif kwargs.has_key("p4c"):
            v = ROOT.TLorentzVector(*kwargs.pop("p4c"))
        obs_dict = kwargs.pop("obs_dict", {})
        tf_dict = kwargs.pop("tf_dict", {})

        o = MEM.Object(v, objtype)

        #Add observables from observable dictionary
        for k, v in obs_dict.items():
            o.addObs(k, v)
        for k, v in tf_dict.items():
            o.addTransferFunction(k, v)
        self.integrator.push_back_object(o)

    def beginLoop(self, setup):
        super(MEAnalyzer, self).beginLoop(setup)

    def configure_mem(self, event, mem_cfg):
        self.integrator.set_cfg(mem_cfg.cfg)
        self.vars_to_integrate.clear()
        self.integrator.next_event()
        mem_cfg.enabled = True

        #One quark from W missed, integrate over its direction if possible
        if "1qW" in mem_cfg.mem_assumptions:
            self.vars_to_integrate.push_back(MEM.PSVar.cos_qbar1)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_qbar1)
        if "0qW" in mem_cfg.mem_assumptions:
            self.vars_to_integrate.push_back(MEM.PSVar.cos_q1)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_q1)
            self.vars_to_integrate.push_back(MEM.PSVar.cos_qbar1)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_qbar1)
        if "1bT" in mem_cfg.mem_assumptions:
            self.vars_to_integrate.push_back(MEM.PSVar.cos_b1)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_b1)
        if "1bTbar" in mem_cfg.mem_assumptions:
            self.vars_to_integrate.push_back(MEM.PSVar.cos_b2)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_b2)
        if "1bH" in mem_cfg.mem_assumptions:
            self.vars_to_integrate.push_back(MEM.PSVar.cos_bbar)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_bbar)

        if "1w2h2t" in mem_cfg.mem_assumptions:
            self.vars_to_integrate.push_back(MEM.PSVar.cos_qbar1)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_qbar1)

        if "2w2h1t_h" in mem_cfg.mem_assumptions:
            self.vars_to_integrate.push_back(MEM.PSVar.cos_b1)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_b1)

        if "2w2h1t_l" in mem_cfg.mem_assumptions:
            self.vars_to_integrate.push_back(MEM.PSVar.cos_b2)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_b2)

        if "0w2h2t" in mem_cfg.mem_assumptions:
            self.vars_to_integrate.push_back(MEM.PSVar.cos_q1)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_q1)
            self.vars_to_integrate.push_back(MEM.PSVar.cos_qbar1)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_qbar1)

        if "1w2h1t_h" in mem_cfg.mem_assumptions:
            self.vars_to_integrate.push_back(MEM.PSVar.cos_qbar1)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_qbar1)
            self.vars_to_integrate.push_back(MEM.PSVar.cos_b1)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_b1)

        if "1w2h1t_l" in mem_cfg.mem_assumptions:
            self.vars_to_integrate.push_back(MEM.PSVar.cos_qbar1)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_qbar1)
            self.vars_to_integrate.push_back(MEM.PSVar.cos_b2)
            self.vars_to_integrate.push_back(MEM.PSVar.phi_b2)



        #Add heavy flavour jets that are assumed to come from top/higgs decay
        #Only take up to 4 candidates, otherwise runtimes become too great
        for jet in list(mem_cfg.b_quark_candidates(event))[:4]:
            self.add_obj(
                MEM.ObjectType.Jet,
                p4s=(jet.pt, jet.eta, jet.phi, jet.mass),
                obs_dict={MEM.Observable.BTAG: jet.btagFlag},
                tf_dict={
                    MEM.TFType.bReco: jet.tf_b, MEM.TFType.qReco: jet.tf_l,
                }
            )
            if "meminput" in self.conf.general["verbosity"]:
                print "memBQuark", jet.pt, jet.eta, jet.phi, jet.mass, jet.btagFlag, jet.tth_match_label, jet.tth_match_index

        #Add light jets that are assumed to come from hadronic W decay
        #Only take up to 4 candidates, otherwise runtimes become too great
        for jet in list(mem_cfg.l_quark_candidates(event))[:4]:
            self.add_obj(
                MEM.ObjectType.Jet,
                p4s=(jet.pt, jet.eta, jet.phi, jet.mass),
                obs_dict={MEM.Observable.BTAG: jet.btagFlag},
                tf_dict={
                    MEM.TFType.bReco: jet.tf_b, MEM.TFType.qReco: jet.tf_l,
                }
            )
            if "meminput" in self.conf.general["verbosity"]:
                print "memLQuark", jet.pt, jet.eta, jet.phi, jet.mass, jet.btagFlag, jet.tth_match_label, jet.tth_match_index
        for lep in mem_cfg.lepton_candidates(event):
            self.add_obj(
                MEM.ObjectType.Lepton,
                p4s=(lep.pt, lep.eta, lep.phi, lep.mass),
                obs_dict={MEM.Observable.CHARGE: lep.charge},
            )
            if "meminput" in self.conf.general["verbosity"]:
                print "memLepton", lep.pt, lep.eta, lep.phi, lep.mass, lep.charge

        met_cand = mem_cfg.met_candidates(event)[0]
        if "meminput" in self.conf.general["verbosity"]:
            print "memMET", met_cand.pt, met_cand.phi
        self.add_obj(
            MEM.ObjectType.MET,
            #MET is caused by massless object
            p4s=(met_cand.pt, 0, met_cand.phi, 0),
        )

    def process(self, event):
        self.counters["processing"].inc("processed")

        #Clean up any old MEM state
        self.vars_to_integrate.clear()
        self.integrator.next_event()

        #Initialize members for tree filler
        event.mem_results_tth = []
        event.mem_results_ttbb = []

        #jets = sorted(event.good_jets, key=lambda x: x.pt, reverse=True)
        leptons = event.good_leptons
        met_pt = event.input.met_pt
        met_phi = event.input.met_phi

        res = {}
        print (event.input.run, event.input.lumi, event.input.evt,
            event.cat, event.cat_btag, len(event.good_jets), event.nBCSVM,
            event.n_mu_tight, event.n_el_tight
        )

        for hypo in [MEM.Hypothesis.TTH, MEM.Hypothesis.TTBB]:
            skipped = []
            for confname in self.memkeys:
                mem_cfg = self.configs[confname]

                fstate = MEM.FinalState.TTH
                if "dl" in mem_cfg.mem_assumptions:
                    fstate = MEM.FinalState.LL
                elif "sl" in mem_cfg.mem_assumptions:
                    fstate = MEM.FinalState.LH
                print "MEM", ("hypo", hypo), ("conf", confname), fstate, len(mem_cfg.b_quark_candidates(event)), len(mem_cfg.l_quark_candidates(event))
                #Run MEM if we did not explicitly disable it
                if (self.conf.mem["calcME"] and
                        mem_cfg.do_calculate(event, mem_cfg) and
                        mem_cfg.enabled and
                        self.conf.mem["selection"](event)
                    ):
                    print "MEM", confname, "started"

                    self.configure_mem(event, mem_cfg)
                    r = self.integrator.run(
                        fstate,
                        hypo,
                        CvectorPSVar(),
                        self.vars_to_integrate
                    )
                    print "MEM done", ("hypo", hypo), ("conf", confname)

                    res[(hypo, confname)] = r
                else:
                    skipped += [confname]
                    r = MEM.MEMOutput()
                    res[(hypo, confname)] = r
            print "skipped confs", skipped
        if "default" in self.memkeys:
            p1 = res[(MEM.Hypothesis.TTH, "default")].p
            p2 = res[(MEM.Hypothesis.TTBB, "default")].p

            #In case of an erroneous calculation, print a message
            if self.conf.mem["calcME"] and (p1<=0 or p2<=0 or (p1 / (p1+0.02*p2))<0.0001):
                print "MEM BADPROB", p1, p2

        #print out full MEM result dictionary
        #print "RES", [(k, res[k].p) for k in sorted(res.keys())]

        event.mem_results_tth = [res[(MEM.Hypothesis.TTH, k)] for k in self.memkeys]
        event.mem_results_ttbb = [res[(MEM.Hypothesis.TTBB, k)] for k in self.memkeys]
        print "---MEM done EVENT r:l:e", event.input.run, event.input.lumi, event.input.evt
