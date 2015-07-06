from TTH.MEAnalysis.vhbb_utils import lvec

import ROOT
import copy
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM

import numpy as np

from TTH.MEAnalysis.MEMUtils import set_integration_vars, add_obj
from TTH.MEAnalysis.MEMConfig import MEMConfig

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

    def process(self, event):
        for (syst, event_syst) in event.systResults.items():
            if event_syst.passes_wtag:
                #print syst, event_syst, event_syst.__dict__
                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_mecat = False
        return np.any([v.passes_mecat for v in event.systResults.values()])

    def _process(self, event):

        cat = "NOCAT"
        #pass_btag_lr = (self.conf.jets["untaggedSelection"] == "btagLR" and
        #    event.btag_LR_4b_2b > self.conf.mem["btagLRCut"][event.cat]
        #)
        pass_btag_lr = False
        pass_btag_csv = (self.conf.jets["untaggedSelection"] == "btagCSV" and
            len(event.selected_btagged_jets_high) >= 4
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
            #event.wquark_candidate_jets = []
            event.wquark_candidate_jets = event.buntagged_jets
            cat = "cat6"

        event.cat = cat
        event.cat_btag = cat_btag
        event.catn = self.cat_map.get(cat, -1)
        event.cat_btag_n = self.btag_cat_map.get(cat_btag, -1)

        event.passes_mecat = True
        return event

class MEAnalyzer(FilterAnalyzer):
    """
    Performs ME calculation using the external integrator.
    It supports multiple MEM algorithms at the same time, configured via the
    self.configs dictionary. The outputs are stored in a vector in the event.

    The ME algorithms are run only in case the njet/nlep/Wtag category (event.cat)
    is in the accepted categories specified in the config.
    Additionally, we require the b-tagging category (event.cat_btag) to be "H" (high).

    For each ME configuration on each event, the jets which are counted to be b-tagged
    in event.selected_btagged_jets_high are added as the candidates for t->b (W) or h->bb.
    These jets must be exactly 4, otherwise no permutation is accepted (in case
    using BTagged/QUntagged assumptions).

    Any additional jets are assumed to come from the hadronic W decay. These are
    specified in event.wquark_candidate_jets.

    Based on the event njet/nlep/Wtag category, if a jet fmor the W is counted as missing,
    it is integrated over using additional variables set by self.vars_to_integrate.

    self.vars_to_integrate_any contains the list of particles which are integrated over assuming
    perfect reconstruction efficiency.

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

        self.mem_configs = self.conf.mem_configs
        for k, v in self.mem_configs.items():
            v.configure_btag_pdf(self.conf)
            v.configure_transfer_function(self.conf)

        self.memkeys = self.conf.mem["methodOrder"]
        self.memkeysToRun = self.conf.mem["methodsToRun"]
        
        #Create an empty vector for the integration variables
        self.vars_to_integrate   = CvectorPSVar()
        self.vars_to_marginalize = CvectorPSVar()
        
        cfg = MEMConfig()
        cfg.configure_btag_pdf(self.conf)
        cfg.configure_transfer_function(self.conf)
        self.integrator = MEM.Integrand(
            MEM.output,
            #MEM.output + MEM.init + MEM.init_more,
            cfg.cfg
        )

    def beginLoop(self, setup):
        super(MEAnalyzer, self).beginLoop(setup)

    def configure_mem(self, event, mem_cfg):
        self.integrator.set_cfg(mem_cfg.cfg)
        self.vars_to_integrate.clear()
        self.vars_to_marginalize.clear()
        self.integrator.next_event()
        
        mem_cfg.enabled = True

        set_integration_vars(self.vars_to_integrate, self.vars_to_marginalize, mem_cfg.mem_assumptions)
        
        bquarks = list(mem_cfg.b_quark_candidates(event))
        if len(bquarks)>mem_cfg.maxJets:
            print "More than {0} b-quarks supplied, dropping last {1} from MEM".format(mem_cfg.maxJets, len(bquarks) - mem_cfg.maxJets)
        
        lquarks = list(mem_cfg.l_quark_candidates(event))
        if len(lquarks)>mem_cfg.maxJets:
            print "More than {0} l-quarks supplied, dropping last {1} from MEM".format(mem_cfg.maxJets, len(lquarks) - mem_cfg.maxJets)
        
        ##Only take up to 4 candidates, otherwise runtimes become too great
        for jet in bquarks[:mem_cfg.maxJets] + lquarks[:mem_cfg.maxJets]:
            add_obj(
                self.integrator,
                MEM.ObjectType.Jet,
                p4s=(jet.pt, jet.eta, jet.phi, jet.mass),
                obs_dict={MEM.Observable.BTAG: jet.btagFlag, MEM.Observable.CSV: jet.btagCSV},
                tf_dict={
                    MEM.TFType.bReco: jet.tf_b, MEM.TFType.qReco: jet.tf_l,
                }
            )
            if "meminput" in self.conf.general["verbosity"]:
                print "memBQuark" if jet in bquarks else "memLQuark",\
                    jet.pt, jet.eta, jet.phi, jet.mass,\
                    ", Flag: ", jet.btagFlag,\
                    ", CSV: ", jet.btagCSV,\
                    ", Match: ", jet.tth_match_label, jet.tth_match_index\
                
                
        for lep in mem_cfg.lepton_candidates(event):
            add_obj(
                self.integrator,
                MEM.ObjectType.Lepton,
                p4s=(lep.pt, lep.eta, lep.phi, lep.mass),
                obs_dict={MEM.Observable.CHARGE: lep.charge},
            )
            if "meminput" in self.conf.general["verbosity"]:
                print "memLepton", lep.pt, lep.eta, lep.phi, lep.mass, lep.charge

        met_cand = mem_cfg.met_candidates(event)
        if "meminput" in self.conf.general["verbosity"]:
            print "memMET", met_cand.pt, met_cand.phi
        add_obj(
            self.integrator,
            MEM.ObjectType.MET,
            #MET is caused by massless object
            p4s=(met_cand.pt, 0, met_cand.phi, 0),
        )

    def process(self, event):
        for (syst, event_syst) in event.systResults.items():
            if event_syst.passes_btag:
                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_mem = False

        return np.any([v.passes_mem for v in event.systResults.values()])

    def _process(self, event):
        #Clean up any old MEM state
        self.vars_to_integrate.clear()
        self.vars_to_marginalize.clear()
        self.integrator.next_event()

        #Initialize members for tree filler
        event.mem_results_tth = []
        event.mem_results_ttbb = []

        res = {}
        if "meminput" in self.conf.general["verbosity"]:
            print "-----"
            print "MEM id={0},{1},{2} cat={3} cat_b={4} nj={5} nt={6} nel={7} nmu={8} syst={9}".format(
                event.input.run, event.input.lumi, event.input.evt,
                event.cat, event.cat_btag, event.numJets, event.nBCSVM,
                event.n_mu_tight, event.n_el_tight, getattr(event, "systematic", None),
            )

        for hypo in [MEM.Hypothesis.TTH, MEM.Hypothesis.TTBB]:
            skipped = []
            for confname in self.memkeys:
                if self.mem_configs.has_key(confname):
                    mem_cfg = self.mem_configs[confname]
                else:
                    if "meminput" in self.conf.general["verbosity"]:
                        print "skipping", confname
                    res[(hypo, confname)] = MEM.MEMOutput()
                    continue

                fstate = MEM.FinalState.Undefined
                if "dl" in mem_cfg.mem_assumptions:
                    fstate = MEM.FinalState.LL
                elif "sl" in mem_cfg.mem_assumptions:
                    fstate = MEM.FinalState.LH
                else:
                    if confname in self.memkeysToRun:
                        raise ValueError("Need to specify sl or dl in assumptions but got {0}".format(str(mem_cfg.mem_assumptions)))
                    else:
                        res[(hypo, confname)] = MEM.MEMOutput()
                        continue

                #if "meminput" in self.conf.general["verbosity"]:
                if "meminput" in self.conf.general["verbosity"]:
                    print "MEM conf={0} fs={1} nb={2} nq={3} doCalc={4} sel={5} inRun={6}".format(
                        confname,
                        fstate,
                        len(mem_cfg.b_quark_candidates(event)),
                        len(mem_cfg.l_quark_candidates(event)),
                        mem_cfg.do_calculate(event, mem_cfg),
                        self.conf.mem["selection"](event),
                        confname in self.memkeysToRun
                    )
                    
                #Run MEM if we did not explicitly disable it
                if (self.conf.mem["calcME"] and
                        mem_cfg.do_calculate(event, mem_cfg) and
                        mem_cfg.enabled and
                        self.conf.mem["selection"](event) and
                        confname in self.memkeysToRun
                    ):
                    
                    if "meminput" in self.conf.general["verbosity"]:
                        print "Integrator::run started hypo={0} conf={1}".format(hypo, confname)
                    self.configure_mem(event, mem_cfg)
                    r = self.integrator.run(
                        fstate,
                        hypo,
                        self.vars_to_integrate,
                        self.vars_to_marginalize
                    )
                    if "meminput" in self.conf.general["verbosity"]:
                        print "Integrator::run done hypo={0} conf={1}".format(hypo, confname)

                    res[(hypo, confname)] = r
                else:
                    skipped += [confname]
                    r = MEM.MEMOutput()
                    res[(hypo, confname)] = r
            if "meminput" in self.conf.general["verbosity"]:
                print "skipped confs", skipped
                
        if "default" in self.memkeys:
            p1 = res[(MEM.Hypothesis.TTH, "default")].p
            p2 = res[(MEM.Hypothesis.TTBB, "default")].p

        event.mem_results_tth = [res[(MEM.Hypothesis.TTH, k)] for k in self.memkeys]
        event.mem_results_ttbb = [res[(MEM.Hypothesis.TTBB, k)] for k in self.memkeys]
        if "memoutput" in self.conf.general["verbosity"]:
            print [r.p for r in event.mem_results_tth]
            print [r.p for r in event.mem_results_ttbb]
            print "---MEM done EVENT r:l:e", event.input.run, event.input.lumi, event.input.evt
        event.passes_mem = True
        return event
