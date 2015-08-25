import os
from collections import OrderedDict
from TTH.MEAnalysis.MEMConfig import MEMConfig
import ROOT
from ROOT import MEM

def jet_baseline(jet, oldpt=None):
    #in case pt has been rescaled, then need to rescale energy fractions
    if oldpt is None:
        oldpt = jet.pt
    ptfrac = jet.pt / oldpt
    
    #X = x / oldpt
    #Xnew = x / (ptfrac * oldpt) = X / ptfrac
    return (jet.neHEF/ptfrac < 0.99
        and jet.chEmEF/ptfrac < 0.99
        and jet.neEmEF/ptfrac < 0.99
        and jet.numberOfDaughters > 1
        and jet.chHEF/ptfrac > 0.0
        and jet.chMult/ptfrac > 0.0
    )

# LB: in fact,  mu.tightId should contain all the other cuts
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Tight_Muon
# https://github.com/vhbb/cmssw/blob/vhbbHeppy722patch2/PhysicsTools/Heppy/python/physicsobjects/Muon.py
def mu_baseline(mu):
    return (
        mu.tightId and
        mu.isPFMuon and
        mu.isGlobalMuon and
        mu.dxy < 0.2 and
        mu.dz < 0.5 and
        mu.globalTrackChi2 < 10 and
        (getattr(mu, "nMuonHits", 0) > 0 or getattr(mu, "nChamberHits", 0) > 0) and #the name of the branch changed between v11 and v12 
        mu.pixelHits > 0 and
        mu.nStations > 1 #FIXME: is this the same as nMuonHits
    )

def print_mu(mu):
    print "Muon: (pt=%s, eta=%s, tight=%s, pf=%s, glo=%s, dxy=%s, dz=%s, chi2=%s, nhits=%s, pix=%s, stat=%s, pfRelIso04=%s)" % (mu.pt, mu.eta, mu.tightId, mu.isPFMuon,  mu.isGlobalMuon, mu.dxy , mu.dz, mu.globalTrackChi2, (getattr(mu, "nMuonHits", 0) > 0 or getattr(mu, "nChamberHits", 0) > 0) , mu.pixelHits , mu.nStations, mu.pfRelIso04)


#def el_baseline_tight(el):
#    sca = abs(el.etaSc)
#    ret = (
#        not(sca > 1.4442 and sca < 1.5660) and
#        el.convVeto
#    )
#    if not ret:
#        return False
#
#    if sca <= 1.479:
#        ret = ret and (
#            (abs(el.eleDEta)    < 0.006046) and
#            (abs(el.eleDPhi)    < 0.028092) and
#            (el.eleSieie        < 0.009947) and
#            (el.eleHoE          < 0.045772) and
#            (abs(el.dxy)        < 0.008790) and
#            (abs(el.dz)         < 0.021226) and
#            (el.pfRelIso03        < 0.069537)
#            #FIXME: expectedMissingInnerHits and hOverE 
#        )
#    elif sca < 2.5:
#        ret = ret and (
#            (abs(el.eleDEta)    < 0.007057) and
#            (abs(el.eleDPhi)    < 0.030159) and
#            (el.eleSieie        < 0.028237) and
#            (el.eleHoE          < 0.067778) and
#            (abs(el.dxy)        < 0.027984) and
#            (abs(el.dz)         < 0.133431) and
#            (el.pfRelIso03        < 0.078265)
#            #FIXME: expectedMissingInnerHits and hOverE 
#        )
#    return ret

def el_baseline_medium(el):
    sca = abs(el.etaSc)
    ret = (
        not(sca > 1.4442 and sca < 1.5660) and
        el.convVeto
    )
    if not ret:
        return False

    if (sca <= 1.479):
        ret = ret and (
            (el.eleSieie < 0.0101) and
            (abs(el.eleDEta) < 0.0103) and
            (abs(el.eleDPhi) < 0.0336) and
            (el.eleHoE < 0.0876) and
            (el.relIso03 < 0.0766) and
            (el.eleooEmooP < 0.0174) and
            (abs(el.dxy) < 0.0118) and
            (abs(el.dz) < 0.373) and
            (el.eleExpMissingInnerHits <= 2.0) and
            (el.convVeto)
        )
    elif (sca < 2.5):
        ret = ret and (
            (el.eleSieie < 0.0283) and
            (abs(el.eleDEta) < 0.00733) and
            (abs(el.eleDPhi) < 0.114) and
            (el.eleHoE < 0.0678) and
            (el.relIso03 < 0.0678) and
            (el.eleooEmooP < 0.0898) and
            (abs(el.dxy) < 0.0739) and
            (abs(el.dz) < 0.602) and
            (el.eleExpMissingInnerHits <= 1.0) and
            (el.convVeto)
        )
        
    return ret

def el_baseline_loose(el):
    sca = abs(el.etaSc)
    ret = (
        not(sca > 1.4442 and sca < 1.5660) and
        el.convVeto
    )
    if not ret:
        return False

    if (sca <= 1.479):
        ret = ret and (
            (el.eleSieie < 0.0103) and
            (abs(el.eleDEta) < 0.0105) and
            (abs(el.eleDPhi) < 0.115) and
            (el.eleHoE < 0.104) and
            (el.relIso03 < 0.0893) and
            (el.eleooEmooP < 0.102) and
            (abs(el.dxy) < 0.0261) and
            (abs(el.dz) < 0.41) and
            (el.eleExpMissingInnerHits <= 2.0) and
            (el.convVeto)
        )
    elif (sca < 2.5):
        ret = ret and (
            (el.eleSieie < 0.0301) and
            (abs(el.eleDEta) < 0.00814) and
            (abs(el.eleDPhi) < 0.182) and
            (el.eleHoE < 0.0897) and
            (el.relIso03 < 0.121) and
            (el.eleooEmooP < 0.126) and
            (abs(el.dxy) < 0.118) and
            (abs(el.dz) < 0.822) and
            (el.eleExpMissingInnerHits <= 1.0) and
            (el.convVeto)
        )
    return ret


def print_el(el):
    print "Electron: (pt=%s, eta=%s, convVeto=%s, etaSc=%s, dEta=%s, dPhi=%s, sieie=%s, HoE=%s, dxy=%s, dz=%s, iso03=%s, nhits=%s, eOp=%s, pfRelIso03=%s)" % (el.pt, el.eta, el.convVeto, abs(el.etaSc), abs(el.eleDEta) , abs(el.eleDPhi) , el.eleSieie, el.eleHoE , abs(el.dxy) , abs(el.dz) , el.relIso03 , getattr(el, "eleExpMissingInnerHits", 0) , getattr(el, "eleooEmooP", 0), el.pfRelIso03)



#https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#PHYS14_selection_all_conditions
#PHYS14 selection, conditions: PU20 bx25, barrel cuts ( |eta supercluster| <= 1.479)
#                    Veto        Loose           Medium          Tight
#abs(dEtaIn) <   0.013625        0.009277        0.008925        0.006046
#abs(dPhiIn) <   0.230374        0.094739        0.035973        0.028092
#sieie <         0.011586        0.010331        0.009996        0.009947
#hOverE <        0.181130        0.093068        0.050537        0.045772
#abs(d0) <       0.094095        0.035904        0.012235        0.008790
#abs(dz) <       0.713070        0.075496        0.042020        0.021226
#ooEmooP <       0.295751        0.189968        0.091942        0.020118
#iso             0.158721        0.130136        0.107587        0.069537
#expectedMissingInnerHits <=     2       1       1       1
#
#PHYS14 selection, conditions: PU20 bx25, endcap cuts (1.479 < |eta supercluster| < 2.5)
#    Veto        Loose   Medium  Tight
#abs(dEtaIn) <   0.011932        0.009833        0.007429        0.007057
#abs(dPhiIn) <   0.255450        0.149934        0.067879        0.030159
#sie <           0.031849        0.031838        0.030135        0.028237
#hOverE <        0.223870        0.115754        0.086782        0.067778
#abs(d0) <       0.342293        0.099266        0.036719        0.027984
#abs(dz) <       0.953461        0.197897        0.138142        0.133431
#ooEmooP <       0.155501        0.140662        0.100683        0.098919
#iso             0.177032        0.163368        0.113254        0.078265
#h <=             3       1       1       1


class Conf:
    leptons = {
        "mu": {

            #SL
            "tight": {
                "pt": 30,
                "eta":2.1,
                "iso": 0.12,
                "idcut": mu_baseline,
            },
            "tight_veto": {
                "pt": 10.0,
                "eta": 2.4,
                "iso": 0.2,
                "idcut": mu_baseline,
            },

            #DL
            "loose": {
                "pt": 20,
                "eta": 2.4,
                "iso": 0.12,
                "idcut": mu_baseline,
            },
            "loose_veto": {
                "pt": 10.0,
                "eta": 2.4,
                "iso": 0.2,
                "idcut": mu_baseline,
            },
            "isotype": "pfRelIso04", #pfRelIso - delta-beta, relIso - rho
            "debug" : print_mu
        },


        "el": {
            "tight": {
                "pt": 30,
                "eta": 2.1,
                "idcut": lambda el: el_baseline_medium(el),
            },
            "tight_veto": {
                "pt": 20,
                "eta": 2.4,
                "idcut": lambda el: el_baseline_loose(el),
            },

            "loose": {
                "pt": 20,
                "eta": 2.4,
                "idcut": lambda el: el_baseline_medium(el),
            },
            "loose_veto": {
                "pt": 10,
                "eta": 2.4,
                "idcut": lambda el: el_baseline_loose(el),
            },
            #"isotype": "pfRelIso03", #pfRelIso - delta-beta, relIso - rho
            "isotype": "relIso03", #pfRelIso - delta-beta, relIso - rho
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
            #"CSVM": ("btagCSV", 0.814),
            "CSVM": ("btagCSV", 0.89),
            "CSVL": ("btagCSV", 0.423),
            "CSVT": ("btagCSV", 0.941)
        },

        #if btagCSV, untagged/tagged selection for W mass and MEM is done by CSVM cut
        #if btagLR, selection is done by the btag likelihood ratio permutation
        "untaggedSelection": "btagLR",
        
        #how many jets to consider for the btag LR permutations
        "NJetsForBTagLR": 6,
        "selection": jet_baseline
    }

    trigger = {

        "filter": False,
        "HLTpaths": [
            "HLT_BIT_HLT_Ele27_eta2p1_WP85_Gsf_HT200_v",
            "HLT_BIT_HLT_IsoMu24_eta2p1_v"
            #"HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p5_2PFBTagCSV_v",
            #"HLT_BIT_HLT_PFHT450_SixJet40_PFBTagCSV_v",
            #"HLT_ttHhardonicLowLumi",
            ],
      
    }

    general = {
        "controlPlotsFileOld": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/ControlPlotsTEST.root",
        "controlPlotsFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/ControlPlotsV6_finerPt.root",
        "QGLPlotsFile_flavour": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/Histos_QGL_flavour.root",
        #"sampleFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/python/samples_722sync.py",
        #"sampleFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/python/samples_722minisync.py",
        "sampleFile": os.environ["CMSSW_BASE"]+"/python/TTH/MEAnalysis/samples_v12.py",
        "transferFunctionsPickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/transfer_functions.pickle",
        "transferFunctions_sj_Pickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/transfer_functions_sj.pickle",
        "systematics": ["nominal"],
        #"systematics": ["nominal", "JESUp", "JESDown", "raw"],
        
        
        #If the list contains:
        # "gen" - print out the ttH gen-level particles (b from top, b form higgs, q from W, leptons
        # "reco" - print out the reco-level selected particles
        # "matching" - print out the association between gen and reco objects
        #"verbosity": ["eventboundary", "input", "matching", "gen", "reco", "meminput"],
        "verbosity": [
            #"trigger",
            #"gen", #print out gen-level info
            #"debug", #very high-level debug info
            #"reco", #info about reconstructed final state
            #"meminput" #info about particles used for MEM input
        ],

        #"eventWhitelist": [
        #    (1, 1094, 109371),
        #]
    }

    bran = {
      
        "pdfFile" :  general["controlPlotsFile"], #os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/ControlPlotsV6_finerPt_722sync.root",

        "jetCategories" : {
            #"2t"   : (2, 2, 0),
            "3t"   : (3, 3, 1),
            "ge4t" : (4, 6, 2), # needed for timing 
            }
        }


    mem = {

        #Actually run the ME calculation
        #If False, all ME values will be 0
        "calcME": False,

        #Generic event-dependent selection function applied
        #just before the MEM. If False, MEM is skipped
        "selection": lambda event: event.btag_LR_4b_2b > 0.98 ,
        
        #This configures what the array elements mean
        #Better not change this
        "methodOrder": [
            "SL_0w2h2t",
            "DL_0w2h2t",
            "SL_2w2h2t",

            #with bLR calc by mem code
            "SL_2w2h2t_memLR",
            "SL_0w2h2t_memLR",

            # with rnd CSV values
            "DL_0w2h2t_Rndge4t",
            "SL_2w2h2t_sj",

            #fully-hadronic
            "FH" #Fixme - add other AH categories
        ],

        #This configures the MEMs to actually run, the rest will be set to 0
        "methodsToRun": [
            "SL_0w2h2t",
            "DL_0w2h2t",
            "SL_2w2h2t",
            "SL_2w2h2t_sj",
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
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t"] = c

###
### SL_0w2h2t
###
c = MEMConfig()
c.l_quark_candidates = lambda ev: []
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    ev.nBCSVM >= 3
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
    len(mcfg.b_quark_candidates(ev)) >= 3 and
    ev.nBCSVM >= 3
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
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    ev.nBCSVM >= 3
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
    ev.nBCSVMRndge4t >= 4
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
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t_sj"] = c

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
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 4
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
        if callable(v):
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
            s += print_dict(v)
        else:
            s += str(v)
    s += "\n"
    return s
