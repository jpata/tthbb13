from TTH.MEAnalysis.vhbb_utils import lvec, autolog

import ROOT
import copy
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM

import numpy as np
import json

from TTH.MEAnalysis.MEMUtils import set_integration_vars, add_obj
from TTH.MEAnalysis.MEMConfig import MEMConfig

#Pre-define shorthands for permutation and integration variable vectors
CvectorPermutations = getattr(ROOT, "std::vector<MEM::Permutations::Permutations>")
CvectorPSVar = getattr(ROOT, "std::vector<MEM::PSVar::PSVar>")
#CmapDistributionTypeTH3D = getattr(ROOT, "std::map<MEM::DistributionType::DistributionType,TH3D>")


def normalize_proba(vec):
    proba_vec = np.array(vec)
    proba_vec[proba_vec <= 1E-50] = 1E-50
    ret = np.array(np.log10(proba_vec), dtype="float64")
    return ret

class MEMPermutation:
    MAXOBJECTS=10

    def __init__(self, idx,
        perm,
        p_mean, p_std,
        p_tf_mean, p_tf_std,
        p_me_mean, p_me_std,
        ):
        self.idx = idx
        self.perm = perm
        for i in range(MEMPermutation.MAXOBJECTS):
            r = perm[i] if i<len(perm) else -99
            setattr(self, "perm_{0}".format(i), r)
        self.p_mean = p_mean
        self.p_std = p_std
        self.p_tf_mean = p_tf_mean
        self.p_tf_std = p_tf_std
        self.p_me_mean = p_me_mean
        self.p_me_std = p_me_std

from TTH.MEAnalysis.Analyzer import FilterAnalyzer
class MECategoryAnalyzer(FilterAnalyzer):
    """
    Performs ME categorization
    FIXME: doc
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(MECategoryAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.cat_map = {"NOCAT":-1, "cat1": 1, "cat2": 2, "cat3": 3, "cat6":6, "cat7":7, "cat8":8, "cat9":9, "cat10":10, "cat11":11, "cat12":12 }
        self.btag_cat_map = {"NOCAT":-1, "L": 0, "H": 1}

    def process(self, event):
        for (syst, event_syst) in event.systResults.items():
            if event_syst.passes_wtag:
                #print syst, event_syst, event_syst.__dict__
                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_mecat = False
        return self.conf.general["passall"] or np.any([v.passes_mecat for v in event.systResults.values()])

    def _process(self, event):

        if "debug" in self.conf.general["verbosity"]:
            autolog("MECategoryAnalyzer started")

        cat = "NOCAT"
        
        pass_btag_csv = (self.conf.jets["untaggedSelection"] == "btagCSV" and
            len(event.selected_btagged_jets_high) >= 4
        )

        #Here we define if an event was of high-btag multiplicity
        cat_btag = "NOCAT"
        if event.pass_category_blr or pass_btag_csv:
            cat_btag = "H"
        else:
            cat_btag = "L"

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
        elif event.is_fh:
            #exactly 8 jets, Wtag in [60,100]
            if (len(event.good_jets) == 8 and event.Wmass >= 60 and event.Wmass < 100):
                #event.wquark_candidate_jets = event.buntagged_jets + event.selected_btagged_jets_low #DS adds 5th,6th,... btags
                if(len(event.selected_btagged_jets_high) == 4):
                    cat = "cat8"
                elif(len(event.selected_btagged_jets_high) == 3):
                    cat = "cat10"
            #exactly 7 jets, Wtag in [60,100]
            if (len(event.good_jets) == 7 and event.Wmass >= 60 and event.Wmass < 100):
                #event.wquark_candidate_jets = event.buntagged_jets + event.selected_btagged_jets_low
                if(len(event.selected_btagged_jets_high) == 4):
                    cat = "cat7"
                elif(len(event.selected_btagged_jets_high) == 3):
                    cat = "cat11"
            #exactly 9 jets, Wtag in [72,94]
            if (len(event.good_jets) == 9 and event.Wmass >= 72 and event.Wmass < 94):
                #event.wquark_candidate_jets = event.buntagged_jets + event.selected_btagged_jets_low
                if(len(event.selected_btagged_jets_high) == 4):
                    cat = "cat9"
                elif(len(event.selected_btagged_jets_high) == 3):
                    cat = "cat12"

        event.cat = cat
        event.cat_btag = cat_btag
        event.catn = self.cat_map.get(cat, -1)
        event.cat_btag_n = self.btag_cat_map.get(cat_btag, -1)
       
        #always pass ME category analyzer
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
            #v.configure_btag_pdf(self.conf)
            v.configure_transfer_function(self.conf)

        self.memkeysToRun = self.conf.mem["methodsToRun"]
        
        #Create an empty vector for the integration variables
        self.vars_to_integrate   = CvectorPSVar()
        self.vars_to_marginalize = CvectorPSVar()
        
        cfg = MEMConfig(self.conf)
        #cfg.configure_btag_pdf(self.conf)
        cfg.configure_transfer_function(self.conf)
        self.integrator = MEM.Integrand(
            MEM.output, #verbosity level
            cfg.cfg
        )

    def beginLoop(self, setup):
        super(MEAnalyzer, self).beginLoop(setup)
        # self.inputCounter = ROOT.TH1F("MEAnalyzer_Count","Count",1,0,2)
        # self.inputCounterPosWeight = ROOT.TH1F("MEAnalyzer_CountPosWeight","Count genWeight>0",1,0,2)
        # self.inputCounterNegWeight = ROOT.TH1F("MEAnalyzer_CountNegWeight","Count genWeight<0",1,0,2)

    def configure_mem(self, event, mem_cfg):
        self.integrator.set_cfg(mem_cfg.cfg)
        self.vars_to_integrate.clear()
        self.vars_to_marginalize.clear()
        self.integrator.next_event()

        set_integration_vars(self.vars_to_integrate, self.vars_to_marginalize, mem_cfg.mem_assumptions)
        
        bquarks = sorted(list(mem_cfg.b_quark_candidates(event)), key=lambda x: x.pt, reverse=True)

        if len(bquarks) > mem_cfg.maxBJets:
            autolog("More than {0} b-quarks supplied, dropping last {1} from MEM".format(
                mem_cfg.maxBJets, len(bquarks) - mem_cfg.maxBJets)
            )
            for q in bquarks[mem_cfg.maxBJets:]:
                print "Dropping jet", q.pt, q.eta
            bquarks = bquarks[:mem_cfg.maxBJets]
        
        lquarks = sorted(list(mem_cfg.l_quark_candidates(event)), key=lambda x: x.pt, reverse=True)

        if len(lquarks) > mem_cfg.maxLJets:
            autolog("More than {0} l-quarks supplied, dropping last {1} from MEM".format(
                mem_cfg.maxLJets, len(lquarks) - mem_cfg.maxLJets)
            )
            for q in lquarks[mem_cfg.maxLJets:]:
                print "Dropping jet", q.pt, q.eta
            lquarks = lquarks[:mem_cfg.maxLJets]
        
        ##Only take up to 4 candidates, otherwise runtimes become too great
        for jet in bquarks + lquarks:
            add_obj(
                self.integrator,
                MEM.ObjectType.Jet,
                p4s=(jet.pt, jet.eta, jet.phi, jet.mass),
                obs_dict={
                    MEM.Observable.BTAG: jet.btagFlag,
                    #MEM.Observable.CSV: getattr(jet, mem_cfg.btagMethod, -1),
                    #MEM.Observable.PDGID: getattr(jet, "PDGID", 0)
                    },
                tf_dict={
                    MEM.TFType.bReco: jet.tf_b, MEM.TFType.qReco: jet.tf_l,
                }
            )
            if "meminput" in self.conf.general["verbosity"]:
                print "memBQuark" if jet in bquarks else "memLQuark",\
                    jet.pt, jet.eta, jet.phi, jet.mass,\
                    ", Flag: ", jet.btagFlag,\
                    ", CSV: ",  getattr(jet, mem_cfg.btagMethod, -1),\
                    ", PDGID: ",  getattr(jet, "PDGID", -1),\
                    ", Match: ", jet.tth_match_label, jet.tth_match_index
                
                
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

        return self.conf.general["passall"] or np.any([v.passes_mem for v in event.systResults.values()])

    def printInputs(self, event, confname):
        inputs = {
            "selectedJetsP4": [
                (j.pt, j.eta, j.phi, j.mass) for j in event.good_jets
            ],
            "selectedJetsCSV": [
                (j.btagCSV) for j in event.good_jets
            ],
            "selectedJetsBTag": [
                (j.btagFlag) for j in event.good_jets
            ],
            "selectedLeptonsP4": [
                (l.pt, l.eta, l.phi, l.mass) for l in event.good_leptons
            ],
            "selectedLeptonsCharge": [
                (l.charge) for l in event.good_leptons
            ],
            "metP4": (event.MET.pt, event.MET.phi)
        }
        outobjects = {"input": inputs}
        outobjects["event"] = {
            "run": event.input.run,
            "lumi":event.input.lumi,
            "event": event.input.evt,
            "cat": event.category_string,
            "blr": event.btag_LR_4b_2b,
            "match_btag": "{0}w_{1}h_{2}h".format(
                event.nMatch_wq_btag,
                event.nMatch_hb_btag,
                event.nMatch_tb_btag,
            ),
            "match": "{0}w_{1}h_{2}h".format(
                event.nMatch_wq,
                event.nMatch_hb,
                event.nMatch_tb,
            )
        }
        #FIXME: make independent of methodOrder
        try:
            memidx = self.conf.mem["methodOrder"].index(confname)
            outobjects["output"] = {
                "mem_cfg": confname,
                "p_tth": event.mem_results_tth[memidx].p,
                "p_ttbb": event.mem_results_ttbb[memidx].p,
                "p": event.mem_results_tth[memidx].p / (
                    event.mem_results_tth[memidx].p + self.conf.mem["weight"]*event.mem_results_ttbb[memidx].p
                ) if event.mem_results_tth[memidx].p > 0 else 0.0
            }
        except:
            print "Potential error!! self.conf.mem['methodOrder'] is missing"
        #end FIXME
        self.jsonout = open("events.json", "a")
        self.jsonout.write(
            json.dumps(outobjects) + "\n"
        )
        self.jsonout.close()

    def _process(self, event):
        
        if "debug" in self.conf.general["verbosity"]:
            autolog("MEMAnalyzer started")
        
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
                event.is_sl, event.is_dl,
                event.cat, event.cat_btag, event.numJets, event.nBCSVM,
                event.n_el_SL, event.n_mu_SL, getattr(event, "systematic", None),
                getattr(event, "systematic", None),
            )

        for hypo in [MEM.Hypothesis.TTH, MEM.Hypothesis.TTBB]:
            skipped = []
            for confname in self.memkeysToRun:
                mem_cfg = self.conf.mem_configs[confname]
                fstate = MEM.FinalState.Undefined
                if "dl" in mem_cfg.mem_assumptions:
                    fstate = MEM.FinalState.LL
                elif "sl" in mem_cfg.mem_assumptions:
                    fstate = MEM.FinalState.LH 
                elif "fh" in mem_cfg.mem_assumptions:
                    fstate = MEM.FinalState.HH
                else:
                    if confname in self.memkeysToRun:
                        raise ValueError("Need to specify sl, dl of fh in assumptions but got {0}".format(str(mem_cfg.mem_assumptions)))
                    else:
                        res[(hypo, confname)] = MEM.MEMOutput()
                        continue

                #if "meminput" in self.conf.general["verbosity"]:
                if ("meminput" in self.conf.general["verbosity"] or
                    "debug" in self.conf.general["verbosity"]):
                    autolog("MEMconf={0} fstate={1} MEMCand[l={2} b={3} q={4}] Reco[j={5} b={6} bLR={7}] MEMconf.doCalc={8} event.selection={9} toBeRun={10} isMC={11}".format(
                        confname,
                        fstate,
                        len(mem_cfg.lepton_candidates(event)),
                        len(mem_cfg.b_quark_candidates(event)),
                        len(mem_cfg.l_quark_candidates(event)),
                        event.numJets, event.nBCSVM, event.btag_LR_4b_2b,
                        mem_cfg.do_calculate(event, mem_cfg),
                        self.conf.mem["selection"](event),
                        confname in self.memkeysToRun,
                        self.cfg_comp.isMC
                    ))
                    
                #Run MEM if we did not explicitly disable it
                if (self.conf.mem["calcME"] and
                        mem_cfg.do_calculate(event, mem_cfg) and
                        self.conf.mem["selection"](event) and
                        confname in self.memkeysToRun
                    ):
                    
                    print "Integrator::run started hypo={0} conf={1} run:lumi:evt={2}:{3}:{4} {5} blr={6}".format(
                        hypo, confname,
                        event.input.run, event.input.lumi, event.input.evt,
                        event.category_string, event.btag_LR_4b_2b
                    )
                    print "Integrator conf: b={0} l={1}".format(
                        len(mem_cfg.b_quark_candidates(event)),
                        len(mem_cfg.l_quark_candidates(event))
                    )
                    self.configure_mem(event, mem_cfg)
                    r = self.integrator.run(
                        fstate,
                        hypo,
                        self.vars_to_integrate,
                        self.vars_to_marginalize
                    )
                    print "Integrator::run done hypo={0} conf={1} cat={2}".format(hypo, confname, event.cat) #DS

                    res[(hypo, confname)] = r
                else:
                    skipped += [confname]
                    r = MEM.MEMOutput()
                    res[(hypo, confname)] = r
            if "meminput" in self.conf.general["verbosity"]:
                print "skipped confs", skipped
        
        #Add MEM results to event
        for key in self.memkeysToRun:
            for (hypo_name, hypo) in [
                ("tth", MEM.Hypothesis.TTH),
                ("ttbb", MEM.Hypothesis.TTBB)
            ]:
                mem_res = res[(hypo, key)]
                setattr(event, "mem_{0}_{1}".format(hypo_name, key), mem_res)

                #Create MEM permutations
                perms = []
                for iperm in range(mem_res.num_perm):
                    perm = mem_res.permutation_indexes[iperm]
                    v_p = normalize_proba([v for v in mem_res.permutation_probas[iperm]])
                    v_p_tf = normalize_proba([v for v in mem_res.permutation_probas_transfer[iperm]])
                    v_p_me = normalize_proba([v for v in mem_res.permutation_probas_me[iperm]])
                    mem_perm = MEMPermutation(
                        iperm,
                        [_p for _p in perm],
                        np.mean(v_p), np.std(v_p), 
                        np.mean(v_p_tf), np.std(v_p_tf), 
                        np.mean(v_p_me), np.std(v_p_me),
                    )
                    perms += [mem_perm]
                setattr(event, "mem_{0}_{1}_perm".format(hypo_name, key), perms)

        #print out the JSON format for the standalone integrator
        for confname in self.memkeysToRun:
            mem_cfg = self.mem_configs[confname]
            if "commoninput" in self.conf.general["verbosity"] and mem_cfg.do_calculate(event, mem_cfg):
                self.printInputs(event, confname)
        

        event.passes_mem = True
        return event
