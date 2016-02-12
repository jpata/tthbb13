from TTH.MEAnalysis.vhbb_utils import lvec

import pdb

import itertools

import ROOT
import copy
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM

import numpy as np
import json
import pickle

from TTH.MEAnalysis.MEMUtils import set_integration_vars, add_obj
from TTH.MEAnalysis.MEMConfig import MEMConfig

from TTH.MEAnalysis.MakeTaggingNtuple import calc_vars_hadtop_3j
import TTH.TTHNtupleAnalyzer.AccessHelpers as AH

#Pre-define shorthands for permutation and integration variable vectors
CvectorPermutations = getattr(ROOT, "std::vector<MEM::Permutations::Permutations>")
CvectorPSVar = getattr(ROOT, "std::vector<MEM::PSVar::PSVar>")
#CmapDistributionTypeTH3D = getattr(ROOT, "std::map<MEM::DistributionType::DistributionType,TH3D>")

pickle_f = open("/shome/gregor/VHBB-7415/CMSSW_7_4_15/src/TTH/MEAnalysis/python/cls_top_resolved.pickle","rb")
cls = pickle.load(pickle_f)
pickle_f.close()

    
from TTH.MEAnalysis.Analyzer import FilterAnalyzer
class MECategoryAnalyzer(FilterAnalyzer):
    """
    Performs ME categorization
    FIXME: doc
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(MECategoryAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.cat_map = {"NOCAT":-1, "cat1": 1, "cat2": 2, "cat3": 3, "cat6":6, "cat8":8}
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
        elif event.is_fh:   #AH
            #exactly 8 jets, Wtag in [60,100]
            if (len(event.good_jets) == 8 and event.Wmass >= 60 and event.Wmass < 100):
                event.wquark_candidate_jets = event.buntagged_jets
                cat = "cat8"
            #FIXME: add other AH categories

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
            #0,
            MEM.output,
            #MEM.output + MEM.input + MEM.init + MEM.init_more,
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

        mem_cfg.enabled = True

        set_integration_vars(self.vars_to_integrate, self.vars_to_marginalize, mem_cfg.mem_assumptions)
        
        bquarks = sorted(list(mem_cfg.b_quark_candidates(event)), key=lambda x: x.pt, reverse=True)

        maxjets = mem_cfg.maxJets

        if len(bquarks)>maxjets:
            print "More than {0} b-quarks supplied, dropping last {1} from MEM".format(maxjets, len(bquarks) - maxjets)
        
        lquarks = sorted(list(mem_cfg.l_quark_candidates(event)), key=lambda x: x.pt, reverse=True)

        if len(lquarks)>maxjets:
            print "More than {0} l-quarks supplied, dropping last {1} from MEM".format(maxjets, len(lquarks) - maxjets)
        print "lquarks", lquarks 
        ##Only take up to 4 candidates, otherwise runtimes become too great
        for jet in bquarks[:maxjets] + lquarks[:maxjets]:
            add_obj(
                self.integrator,
                MEM.ObjectType.Jet,
                p4s=(jet.pt, jet.eta, jet.phi, jet.mass),
                obs_dict={
                    MEM.Observable.BTAG: jet.btagFlag,
                    MEM.Observable.CSV: getattr(jet, mem_cfg.btagMethod, -1),
                    MEM.Observable.PDGID: getattr(jet, "PDGID", 0)
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
                    ", PDGID: ",  getattr(jet, "PDGID", 0)
                    #", Match: ", jet.tth_match_label, jet.tth_match_index\
                
                
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
        # #self.inputCounter.Fill(1)
        # if self.cfg_comp.isMC:
        #     genWeight = getattr(event.input, "genWeight")
        #     if genWeight > 0:
        #         self.inputCounterPosWeight.Fill(1)
        #     elif genWeight < 0:
        #         self.inputCounterNegWeight.Fill(1)

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
            "blr": event.btag_LR_4b_2b
        }
        memidx = self.conf.mem["methodOrder"].index(confname)
        outobjects["output"] = {
            "p_tth": event.mem_results_tth[memidx].p,
            "p_ttbb": event.mem_results_ttbb[memidx].p,
            "p": event.mem_results_tth[memidx].p / (
                event.mem_results_tth[memidx].p + self.conf.mem["weight"]*event.mem_results_ttbb[memidx].p
            ) if event.mem_results_tth[memidx].p > 0 else 0.0
        }
        print json.dumps(outobjects, indent=2)
        self.jsonout = open("events.json", "a")
        self.jsonout.write(
            json.dumps(outobjects, indent=2) + "\n\n\n"
        )
        self.jsonout.close()

    def _process(self, event):
        #Clean up any old MEM state
        self.vars_to_integrate.clear()
        self.vars_to_marginalize.clear()
        self.integrator.next_event()


        #Permuation magic
        #pdb.set_trace()
        
        jets = []
        for ij,jet in enumerate(event.good_jets):
            tlv = AH.buildTlv(jet.pt, jet.eta, jet.phi, jet.mass)
            tlv.btagCSV        = jet.btagCSV
            tlv.index          = ij
            jets.append(tlv)
        # Make sure jets are sorted
        jets.sort(key = lambda x:-x.Pt())

        

        
        best_comb = None
        best_response = -1

        for comb in itertools.combinations(jets, 3):
            v = calc_vars_hadtop_3j(comb, False)

            vararray = np.array([v[vname] for vname in cls.varlist])
            vararray = vararray.reshape(1,-1)

            response = cls.predict_proba(vararray)[0,1]

            if response > best_response:
                best_response = response
                best_comb = comb
        
        #if best_response > 0:
        #    print "Found: ", best_response, best_comb[0].index, best_comb[1].index, best_comb[2].index
            
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
                getattr(event, "systematic", None),
            )

        for hypo in [MEM.Hypothesis.TTH, MEM.Hypothesis.TTBB]:
            skipped = []
            for confname in self.memkeys:
                if self.mem_configs.has_key(confname):
                    mem_cfg = self.mem_configs[confname]
                else:
                    if confname in self.memkeysToRun:
                        raise KeyError(
                            "Asked for configuration={0} but this was never specified in mem_configs.keys={1}".format(
                                confname, list(self.mem_configs.keys())
                            )
                        )
                    else:
                        if "meminput" in self.conf.general["verbosity"]:
                            print "skipping conf", confname

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
                    
                if confname == "SL_2w2h2t_3jt":                    
                    top_indices = [best_comb[0].index, best_comb[1].index, best_comb[2].index]
                    for j in event.good_jets:
                        j.PDGID = 0
                        
                        tmp_jets = [event.good_jets[i] for i in top_indices]
                        tmp_jets.sort(key = lambda x:x.btagCSV)
                        if len(tmp_jets)==3:
                            tmp_jets[0].PDGID = 1
                            tmp_jets[1].PDGID = 1
                            tmp_jets[2].PDGID = 5
                    # TODO: RESTORE AFERWARDS!!!


                #if "meminput" in self.conf.general["verbosity"]:
                if "meminput" in self.conf.general["verbosity"]:
                    print "MEM conf={0} fs={1} nl={2} nb={3} nq={4} numJets={5} nBCSVM={6} bLR={7} doCalc={8} enabled={9} selection={10} inRun={11} isMC={12}".format(
                        confname,
                        fstate,
                        len(mem_cfg.lepton_candidates(event)),
                        len(mem_cfg.b_quark_candidates(event)),
                        len(mem_cfg.l_quark_candidates(event)),
                        event.numJets, event.nBCSVM, event.btag_LR_4b_2b,
                        mem_cfg.do_calculate(event, mem_cfg),
                        mem_cfg.enabled,
                        self.conf.mem["selection"](event),
                        confname in self.memkeysToRun,
                        self.cfg_comp.isMC
                    )
                    
                #Run MEM if we did not explicitly disable it
                if (self.conf.mem["calcME"] and
                        mem_cfg.do_calculate(event, mem_cfg) and
                        mem_cfg.enabled and
                        self.conf.mem["selection"](event) and
                        confname in self.memkeysToRun
                        #self.cfg_comp.isMC #only run MEM on MC
                    ):
                    
                    print "Integrator::run started hypo={0} conf={1} run:lumi:evt={2}:{3}:{4} {5} blr={6}".format(
                        hypo, confname,
                        event.input.run, event.input.lumi, event.input.evt,
                        event.category_string, event.btag_LR_4b_2b
                    )
                    self.configure_mem(event, mem_cfg)
                    r = self.integrator.run(
                        fstate,
                        hypo,
                        self.vars_to_integrate,
                        self.vars_to_marginalize
                    )
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

        for confname in self.memkeysToRun:
            if confname not in skipped and "commoninput" in self.conf.general["verbosity"]:
                self.printInputs(event, confname)
        
        if "memoutput" in self.conf.general["verbosity"]:
            print [r.p for r in event.mem_results_tth]
            print [r.p for r in event.mem_results_ttbb]
            print "---MEM done EVENT r:l:e", event.input.run, event.input.lumi, event.input.evt
        

        event.passes_mem = True
        return event
