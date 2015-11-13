import os
from collections import OrderedDict
from TTH.MEAnalysis.MEMConfig import MEMConfig
import ROOT
from ROOT import MEM
import VHbbAnalysis.Heppy.TriggerTableData as trigData
import VHbbAnalysis.Heppy.TriggerTable as trig

def jet_baseline(jet):
    #Require that jet must have at least loose POG_PFID
    #Look in Heppy autophobj.py and Jet.py 
    return (jet.id >= 1)

# LB: in fact,  mu.tightId should contain all the other cuts
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Tight_Muon
# https://github.com/vhbb/cmssw/blob/vhbbHeppy722patch2/PhysicsTools/Heppy/python/physicsobjects/Muon.py
def mu_baseline_tight(mu):
    return (
        mu.tightId == 1
    )

def print_mu(mu):
    print "Muon: (pt=%s, eta=%s, tight=%s, pf=%s, glo=%s, dxy=%s, dz=%s, chi2=%s, nhits=%s, pix=%s, stat=%s, pfRelIso04=%s)" % (mu.pt, mu.eta, mu.tightId, mu.isPFMuon,  mu.isGlobalMuon, mu.dxy , mu.dz, mu.globalTrackChi2, (getattr(mu, "nMuonHits", 0) > 0 or getattr(mu, "nChamberHits", 0) > 0) , mu.pixelHits , mu.nStations, mu.pfRelIso04)

def el_baseline_medium(el):

    sca = abs(el.etaSc)
    ret = ((sca < 1.4442 and
        el.eleSieie < 0.012 and
        el.eleHoE < 0.09 and
        el.eleEcalClusterIso/ el.pt < 0.37 and
        el.eleHcalClusterIso / el.pt < 0.25 and
        abs(el.eleDEta) < 0.0095 and
        abs(el.eleDPhi) < 0.065 and
        el.dr03TkSumPt/el.pt < 0.18) or
        (sca > 1.5660 and
        el.eleSieie < 0.033 and
        el.eleHoE < 0.09 and
        el.eleEcalClusterIso / el.pt < 0.45 and
        el.eleHcalClusterIso / el.pt < 0.28 and
        el.dr03TkSumPt/el.pt < 0.18)
    )
    
    #medium ID (cut-based)
    #ret = ret and el.eleCutIdSpring15_25ns_v1 >= 3
    
    ret = ret and el.mvaIdTrigMediumResult == 1
    return ret

#def el_baseline_loose(el):
#
#    sca = abs(el.etaSc)
#    ret = not (sca > 1.4442 and sca < 1.5660)
#
#    #Loose ID
#    ret = ret and el.eleCutIdSpring15_25ns_v1 >= 2
#    return ret

def print_el(el):
    print "Electron: (pt=%s, eta=%s, convVeto=%s, etaSc=%s, dEta=%s, dPhi=%s, sieie=%s, HoE=%s, dxy=%s, dz=%s, iso03=%s, nhits=%s, eOp=%s, pfRelIso03=%s mvaId=%s ecalIso=%s hcalIso=%s)" % (
        el.pt, el.eta, el.convVeto, abs(el.etaSc), abs(el.eleDEta),
        abs(el.eleDPhi), el.eleSieie, el.eleHoE, abs(el.dxy),
        abs(el.dz), el.relIso03 , getattr(el, "eleExpMissingInnerHits", 0),
        getattr(el, "eleooEmooP", 0), el.pfRelIso03, el.mvaIdTrigMediumResult,
        el.eleEcalClusterIso/el.pt, el.eleHcalClusterIso/el.pt
    )

class Conf:
    leptons = {
        "mu": {

            #SL
            "SL": {
                "pt": 25,
                "eta":2.1,
                "iso": 0.15,
                "idcut": mu_baseline_tight,
            },
            #DL
            "DL": {
                "pt_leading": 20,
                "pt_subleading": 15,
                "eta": 2.4,
                "iso": 0.15,
                "idcut": mu_baseline_tight,
            },
            "veto": {
                "pt": 15.0,
                "eta": 2.4,
                "iso": 0.15,
                "idcut": mu_baseline_tight,
            },
            "isotype": "pfRelIso04", #pfRelIso - delta-beta, relIso - rho
            "debug" : print_mu
        },


        "el": {
            "SL": {
                "pt": 30,
                "eta": 2.1,
                "idcut": lambda el: el_baseline_medium(el),
            },
            "DL": {
                "pt_leading": 20,
                "pt_subleading": 15,
                "eta": 2.4,
                "idcut": lambda el: el_baseline_medium(el),
            },
            "veto": {
                "pt": 15,
                "eta": 2.4,
                "idcut": lambda el: el_baseline_medium(el),
            },
            #"isotype": "pfRelIso03", #pfRelIso - delta-beta, relIso - rho
            "isotype": "none", #pfRelIso - delta-beta, relIso - rho (Heppy.LeptonAnalyzer.ele/mu_isoCorr), none
            "debug" : print_el
        },
        "selection": lambda event: event.is_sl or event.is_dl
        #"selection": lambda event: event.is_fh
    }

    jets = {
        # pt, |eta| thresholds for **leading two jets** (common between sl and dl channel)
        "pt":   30,
        "eta":  2.4,

        # pt, |eta| thresholds for **trailing jets** specific to sl channel
        "pt_sl":  30,
        "eta_sl": 2.4,

        # pt, |eta| thresholds for **trailing jets** specific to dl channel
        "pt_dl":  20,
        "eta_dl": 2.4,

        # pt threshold for leading jets in fh channel
        "pt_fh": 40,

        #The default b-tagging algorithm (branch name)
        "btagAlgo": "btagCSV",

        #The default b-tagging WP
        "btagWP": "CSVM",

        #These working points are evaluated and stored in the trees as nB* - number of jets passing the WP
        #https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagging#Preliminary_working_or_operating
        "btagWPs": {
            "CSVM": ("btagCSV", 0.89),
            "CSVL": ("btagCSV", 0.423),
            "CSVT": ("btagCSV", 0.941)
        },

        #if btagCSV, untagged/tagged selection for W mass and MEM is done by CSVM cut
        #if btagLR, selection is done by the btag likelihood ratio permutation
        #"untaggedSelection": "btagCSV",
        "untaggedSelection": "btagLR",
        
        #how many jets to consider for the btag LR permutations
        "NJetsForBTagLR": 6,

        #base jet selection
        "selection": jet_baseline
    }

    trigger = {

        "filter": False,
        "trigTable": trig.triggerTable, 
        "trigTableData": trigData.triggerTable, 
    }

    general = {
        "passall": True,
        "doQGL": False,
        "controlPlotsFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/ControlPlotsV14.root",
        #"controlPlotsFileNew": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/ControlPlotsV14.root",
        "QGLPlotsFile_flavour": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/Histos_QGL_flavour.root",
        "sampleFile": os.environ["CMSSW_BASE"]+"/python/TTH/MEAnalysis/samples_v14.py",
        "transferFunctionsPickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/transfer_functions.pickle",
        "transferFunctions_sj_Pickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/transfer_functions_sj.pickle",
        #"systematics": ["nominal"],
        "systematics": ["nominal", "JESUp", "JESDown"],
        
        
        #If the list contains:
        # "gen" - print out the ttH gen-level particles (b from top, b form higgs, q from W, leptons
        # "reco" - print out the reco-level selected particles
        # "matching" - print out the association between gen and reco objects
        #"verbosity": ["eventboundary", "input", "matching", "gen", "reco", "meminput"],
        "verbosity": [
            #"eventboundary", #print run:lumi:event
            #"trigger", #print trigger bits
            #"input", #print input particles
            #"gen", #print out gen-level info
            "debug", #very high-level debug info
            #"reco", #info about reconstructed final state
            #"meminput" #info about particles used for MEM input
        ],

        #"eventWhitelist": [
        #    #KIT
        #    (1, 1386, 276274),
        #    (1, 15709, 3131733),

        #    #DESY
        #    (1, 11333, 2259327),
        #    (1, 15646, 3119109),
        #]
    }

    bran = {
      
        "enabled": False,
        "pdfFile" :  general["controlPlotsFile"], #os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/ControlPlotsV6_finerPt_722sync.root",

        "jetCategories" : {
            #"2t"   : (2, 2, 0),
            "3t"   : (3, 3, 1),
            "ge4t" : (4, 6, 2), # needed for timing 
        }
    }

    tth_mva = {
        "filename": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/tth_bdt.pkl",
        "varlist": [
            "is_sl",
            "is_dl",
            "lep0_pt",
            "lep0_aeta",
            "lep1_pt",
            "lep1_aeta",
            "jet0_pt",
            "jet0_btag",
            "jet0_aeta",
            "jet1_pt",
            "jet1_btag",
            "jet1_aeta",
            "jet2_pt",
            "jet2_btag",
            "jet2_aeta",
            "mean_bdisc",
            "mean_bdisc_btag",
            "min_dr_btag",
            "mean_dr_btag",
            "std_dr_btag",
            "momentum_eig0",
            "momentum_eig1",
            "momentum_eig2",
            "fw_h0",
            "fw_h1",
            "fw_h2",
            "aplanarity",
            "isotropy",
            "numJets",
            "nBCSVM",
            "Wmass"
        ]
    }
    
    mem = {

        #Actually run the ME calculation
        #If False, all ME values will be 0
        "calcME": True,

        #Generic event-dependent selection function applied
        #just before the MEM. If False, MEM is skipped for all hypos
        #note that we set hypothesis-specific cuts below
        "selection": lambda event: (
            event.btag_LR_4b_2b > 0.95
            or (event.is_sl and event.nBCSVM >= 3) #always calculate for tagged events
            or (event.is_dl and event.nBCSVM >= 2) #always calculate for tagged events
        ),
        #"selection": lambda event: (event.btag_LR_4b_2b > 0.95 #optimized for 40% tth(bb) acceptance
        #    and (event.is_sl and event.numJets >= 6 and event.nBCSVM >= 4) #always calculate for tagged events
        #),
        
        #This configures what the array elements mean
        #Better not change this
        "methodOrder": [
            "SL_0w2h2t",
            "DL_0w2h2t",
            
            "SL_1w2h2t",
            "SL_2w2h1t_l",
            "SL_2w2h1t_h",
            "SL_2w2h2t",

            #with bLR calc by mem code
            "SL_2w2h2t_memLR",
            "SL_0w2h2t_memLR",

            # with rnd CSV values
            "DL_0w2h2t_Rndge4t",
            "SL_2w2h2t_sj",
            "SL_0w2h2t_sj",

            #fully-hadronic
            "FH" #Fixme - add other AH categories
        ],

        #This configures the MEMs to actually run, the rest will be set to 0
        "methodsToRun": [
            "SL_0w2h2t",
            "DL_0w2h2t",
            #"SL_1w2h2t",
            #"SL_2w2h1t_l",
            #"SL_2w2h1t_h",
            "SL_2w2h2t",
            "SL_2w2h2t_sj",
            #"SL_0w2h2t_sj",
            #"SL_2w2h2t_memLR",
            #"SL_0w2h2t_memLR",
            #"DL_0w2h2t_Rndge4t",
            #"FH"
        ],

    }
    
    mem_configs = OrderedDict()

CvectorPermutations = getattr(ROOT, "std::vector<MEM::Permutations::Permutations>")
CvectorPSVar = getattr(ROOT, "std::vector<MEM::PSVar::PSVar>")

###
### SL_2w2h2t
###
#FIXME: why == here and not >= ?
c = MEMConfig()
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t"] = c

###
### SL_1w2h2t
###
c = MEMConfig()
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 1
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("1w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_1w2h2t"] = c

###
### SL_2w2h1t_l
###
c = MEMConfig()
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and
    len(mcfg.l_quark_candidates(ev)) >= 1
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("2w2h1t_l")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h1t_l"] = c

###
### SL_2w2h1t_h
###
c = MEMConfig()
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and
    len(mcfg.l_quark_candidates(ev)) >= 1
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("2w2h1t_h")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h1t_h"] = c

###
### SL_0w2h2t
###
c = MEMConfig()
c.l_quark_candidates = lambda ev: []
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4
    #(len(mcfg.l_quark_candidates(ev)) + len(mcfg.b_quark_candidates(ev))) >= 4
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("0w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
#c.cfg.int_code = 0
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_0w2h2t"] = c

###
### SL_0w2h2t _memLR
###
c = MEMConfig()
c.b_quark_candidates = lambda ev: ev.good_jets
c.l_quark_candidates = lambda ev: []
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 3
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("0w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.FirstRankedByBTAG)
c.cfg.perm_pruning = strat
#c.cfg.int_code = 1+2+4
#c.cfg.int_code = 0
c.maxJets = 8
Conf.mem_configs["SL_0w2h2t_memLR"] = c

###
### DL_0w2h2t
###
c = MEMConfig()
c.b_quark_candidates = lambda ev: ev.good_jets
c.l_quark_candidates = lambda ev: []
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 2 and
    len(mcfg.b_quark_candidates(ev)) >= 4
    #(len(mcfg.l_quark_candidates(ev)) + len(mcfg.b_quark_candidates(ev))) >= 4
)
#c.cfg.int_code = 0
c.maxJets = 8
c.mem_assumptions.add("dl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.FirstRankedByBTAG)
c.cfg.perm_pruning = strat
Conf.mem_configs["DL_0w2h2t"] = c

###
### DL_0w2h2t_Rnd4t
###
c = MEMConfig()
c.b_quark_candidates = lambda ev: ev.good_jets
c.l_quark_candidates = lambda ev: []
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 2 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    getattr(ev, "nBCSVMRndge4t", 0) >= 4
)
c.btagMethod = "btagCSVRndge4t"
c.maxJets = 8
c.mem_assumptions.add("dl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.FirstRankedByBTAG)
c.cfg.perm_pruning = strat
Conf.mem_configs["DL_0w2h2t_Rndge4t"] = c

#Subjet configurations#
#######################

#SL_2w2h2t_sj
c = MEMConfig()
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2 and
    ev.PassedSubjetAnalyzer == True
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t_sj"] = c

#SL_0w2h2t_sj
c = MEMConfig()
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 0
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("0w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_0w2h2t_sj"] = c

##SL_2w2h2t_sj_perm
#c = MEMConfig()
#c.do_calculate = lambda ev, mcfg: (
#    len(mcfg.lepton_candidates(ev)) == 1 and
#    len(mcfg.b_quark_candidates(ev)) >= 4 and
#    len(mcfg.l_quark_candidates(ev)) == 2
#)
#c.mem_assumptions.add("sl")
##FIXME: Thomas, why this is not required?
##strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
#strat = CvectorPermutations()
#strat.push_back(MEM.Permutations.HEPTopTagged)
#strat.push_back(MEM.Permutations.QUntagged)
#strat.push_back(MEM.Permutations.BTagged)
#c.cfg.perm_pruning = strat
#Conf.mem_configs["SL_2w2h2t_sj_perm"] = c

###
### FH
###
c = MEMConfig()
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) == 4 and #DS
    len(mcfg.l_quark_candidates(ev)) == 4 #DS
)
c.mem_assumptions.add("fh")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH"] = c

import inspect
def print_dict(d):
    s = "(\n"
    for k, v in sorted(d.items(), key=lambda x: x[0]):
        if callable(v) and not isinstance(v, ROOT.TF1):
            v = inspect.getsource(v).strip()
        elif isinstance(v, dict):
            s += print_dict(v)
        s += "  {0}: {1},\n".format(k, v)
    s += ")"
    return s
    
def conf_to_str(Conf):
    s = "Conf (\n"
    for k, v in sorted(Conf.__dict__.items(), key=lambda x: x[0]):
        s += "{0}: ".format(k)
        if isinstance(v, dict):
            s += print_dict(v) + ",\n"
        elif isinstance(v, ROOT.TF1):
            s += "ROOT.TF1({0}, {1})".format(v.GetName(), v.GetTitle()) + ",\n"
        else:
            s += str(v) + ",\n"
    s += "\n"
    return s
