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
 
    #EGamma POG MVA ID for triggering electrons (0=none, 1=WP90, 2=WP80, Spring15 training); 1 for muons
    # We want 80%
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/TTbarHbbRun2ReferenceAnalysis_76XTransition#Electrons
    ret = ret and el.eleMVAIdSpring15Trig == 2

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
    print "Electron: (pt=%s, eta=%s, convVeto=%s, etaSc=%s, dEta=%s, dPhi=%s, sieie=%s, HoE=%s, dxy=%s, dz=%s, iso03=%s, nhits=%s, eOp=%s, pfRelIso03=%s, mvaIdFlag=%s, mvaId=%s, ecalIso=%s, hcalIso=%s)" % (
        el.pt, el.eta, el.convVeto, abs(el.etaSc), abs(el.eleDEta),
        abs(el.eleDPhi), el.eleSieie, el.eleHoE, abs(el.dxy),
        abs(el.dz), el.relIso03 , getattr(el, "eleExpMissingInnerHits", 0),
        getattr(el, "eleooEmooP", 0), el.pfRelIso03, el.eleMVAIdSpring15Trig, el.eleMVArawSpring15Trig,
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
            "DL": {
                "iso": 0.15,
                "eta": 2.4,
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
                "eta": 2.4,
                "idcut": el_baseline_medium,
            },
            "veto": {
                "pt": 15.0,
                "eta": 2.4,
                "idcut": lambda el: el_baseline_medium(el),
            },
            #"isotype": "pfRelIso03", #pfRelIso - delta-beta, relIso - rho
            "isotype": "none", #pfRelIso - delta-beta, relIso - rho (Heppy.LeptonAnalyzer.ele/mu_isoCorr), none
            "debug" : print_el
        },
        "DL": {
            "pt_leading": 20,
            "pt_subleading": 15,
        },
        "selection": lambda event: event.is_sl or event.is_dl or event.is_fh
        #"selection": lambda event: event.is_fh #DS
    }

    jets = {
        # pt, |eta| thresholds for **leading two jets** (common between sl and dl channel)
        "pt":   30,
        "eta":  2.4,

        # pt, |eta| thresholds for **leading jets** specific to sl channel
        "pt_sl":  30,
        "eta_sl": 2.4,

        # pt, |eta| thresholds for **trailing jets** specific to dl channel
        "pt_dl":  20,
        "eta_dl": 2.4,

        # pt threshold for leading jets in fh channel
        "pt_fh": 40,

        # nhard'th jet is used for pt threshold
        "nhard_fh": 6,

        # minimum number of jets to save event in tree
        "minjets_fh": 6,

        #The default b-tagging algorithm (branch name)
        "btagAlgo": "btagCSV",

        #The default b-tagging WP
        "btagWP": "CSVM",

        #These working points are evaluated and stored in the trees as nB* - number of jets passing the WP
        #https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80X
        "btagWPs": {
            "CSVM": ("btagCSV", 0.800),
            "CSVL": ("btagCSV", 0.460),
            "CSVT": ("btagCSV", 0.935),
            
            "CMVAM": ("btagCMVA", 0.185),
            "CMVAL": ("btagCMVA", -0.715),
            "CMVAT": ("btagCMVA", 0.875)
        },

        #if btagCSV, untagged/tagged selection for W mass and MEM is done by CSVM cut
        #if btagLR, selection is done by the btag likelihood ratio permutation
        #"untaggedSelection": "btagCSV",
        "untaggedSelection": "btagLR",
        
        #how many jets to consider for the btag LR permutations
        "NJetsForBTagLR": 9, #DS

        #base jet selection
        "selection": jet_baseline
    }

    trigger = {

        "filter": False,
        "trigTable": trig.triggerTable, 
        "trigTableData": trigData.triggerTable, 
    }

    general = {
        "passall": False,
        "doQGL": False,
        "controlPlotsFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/ControlPlotsV20.root",
        "QGLPlotsFile_flavour": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/Histos_QGL_flavour.root",
        "sampleFile": os.environ["CMSSW_BASE"]+"/python/TTH/MEAnalysis/samples.py",
        "transferFunctionsPickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions.pickle",
        "transferFunctions_sj_Pickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions_sj.pickle",
        #"systematics": ["nominal"],
        "systematics": [
            "nominal",
            #"JESUp", "JESDown",
            #"JERUp", "JERDown"
        ],
        
        
        #If the list contains:
        # "gen" - print out the ttH gen-level particles (b from top, b form higgs, q from W, leptons
        # "reco" - print out the reco-level selected particles
        # "matching" - print out the association between gen and reco objects
        "verbosity": [
            #"eventboundary", #print run:lumi:event
            #"trigger", #print trigger bits
            #"input", #print input particles
            #"gen", #print out gen-level info
            #"debug", #very high-level debug info
            #"reco", #info about reconstructed final state
            #"meminput", #info about particles used for MEM input
            #"commoninput", #print out inputs for CommonClassifier
            #"commonclassifier",
        ],

        #"eventWhitelist": [
        #    (1, 144279, 14372670)
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
        "calcMECommon": False,
        "n_integration_points_mult": 1.0,

        "weight": 0.15, #k in Psb = Ps/(Ps+k*Pb)

        "blr_cuts": {
            "sl_j4_t2": 20,
            "sl_j4_t3": 1.1,
            "sl_j4_tge4": -20,
            
            "sl_j5_t2": 20,
            "sl_j5_t3": 2.3,
            "sl_j5_tge4": -20,
            
            "sl_jge6_t2": -0.4,
            "sl_jge6_t3": 2.9,
            "sl_jge6_tge4": -20,

            "dl_j3_t2": 20,
            "dl_j3_t3": -20,
            "dl_jge4_t2": 20,
            "dl_jge4_t3": 2.3,
            "dl_jge4_tge4": -20,
        },

        #Generic event-dependent selection function applied
        #just before the MEM. If False, MEM is skipped for all hypos
        #note that we set hypothesis-specific cuts below
        "selection": lambda event: (
            event.pass_category_blr and (
                (event.is_sl and event.nBCSVM >= 2)
                or (event.is_dl and event.nBCSVM >= 2)
            ) or
            (event.is_fh and event.cat in ["cat7","cat8","cat10","cat11"]
            and event.btag_LR_4b_2b > 0.95)
        ),
        
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
            "FH_4w2h2t", #8j,4b & 9j,4b
            "FH_3w2h2t", #7j,4b
            "FH_4w2h1t", #7j,3b & 8j,3b
            "FH_0w0w2h2t", #all 4b cats
            "FH_0w0w2h1t", #all cats
            "FH_0w0w1h2t",  #all cats
            "SL_2w2h2t_1j",
        ],

        #This configures the MEMs to actually run, the rest will be set to 0
        "methodsToRun": [
            "SL_0w2h2t",
            "DL_0w2h2t",
            "SL_1w2h2t",
            #"SL_2w2h1t_l",
            #"SL_2w2h1t_h",
            "SL_2w2h2t",
            "SL_2w2h2t_1j",
            #"SL_2w2h2t_sj",
            #"SL_0w2h2t_sj",
            #"SL_2w2h2t_memLR",
            #"SL_0w2h2t_memLR",
            #"DL_0w2h2t_Rndge4t",
            #"FH_4w2h2t", #8j,4b
            #"FH_3w2h2t", #7j,4b
            #"FH_4w2h1t", #7j,3b & 8j,3b
            #"FH_0w0w2h2t", #all 4b cats
            #"FH_0w0w2h1t", #all cats
            #"FH_0w0w1h2t"  #all cats
        ],

    }
    
    mem_configs = OrderedDict()

CvectorPermutations = getattr(ROOT, "std::vector<MEM::Permutations::Permutations>")
CvectorPSVar = getattr(ROOT, "std::vector<MEM::PSVar::PSVar>")

###
### SL_2w2h2t
###
c = MEMConfig(Conf)
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
### SL_2w2h2t_1j
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 3
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
c.cfg.int_code += ROOT.MEM.IntegrandType.AdditionalRadiation
Conf.mem_configs["SL_2w2h2t_1j"] = c

###
### SL_1w2h2t
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 1 and
    ev.numJets == 5
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
c = MEMConfig(Conf)
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
c = MEMConfig(Conf)
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
c = MEMConfig(Conf)
c.l_quark_candidates = lambda ev: []
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    ev.numJets == 4
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
### DL_0w2h2t
###
c = MEMConfig(Conf)
c.b_quark_candidates = lambda ev: ev.good_jets
c.l_quark_candidates = lambda ev: []
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 2 and
    len(mcfg.b_quark_candidates(ev)) >= 4
    #(len(mcfg.l_quark_candidates(ev)) + len(mcfg.b_quark_candidates(ev))) >= 4
)
c.maxLJets = 4
c.mem_assumptions.add("dl")
strat = CvectorPermutations()
#FIXME: are we sure about these assumptions?
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.FirstRankedByBTAG)
c.cfg.perm_pruning = strat
Conf.mem_configs["DL_0w2h2t"] = c


#Subjet configurations#
#######################

#SL_2w2h2t_sj
c = MEMConfig(Conf)
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
c = MEMConfig(Conf)
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
#c = MEMConfig(Conf)
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
### FH_4w2h2t #8j,4b, 9j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low #DS adds 5th,6th,... btags
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and #DS #although from BTagLRAnalyzer there are max 4 candidates
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 ) #DS do not consider 10 jet events
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("4w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry, but then add _l,_h for all missing-q methods
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_4w2h2t"] = c

###
### FH_3w2h2t #7j,4b (& 8j,4b)
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and #DS
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 ) #DS run two methods for 8j,4b category
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("3w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_3w2h2t"] = c

###
### FH_4w2h1t #7j,3b, 8j,3b #do not need _l,_h if not imposing t-tbar symmetry
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) == 3 and #DS
    ( len(mcfg.l_quark_candidates(ev)) == 4 or len(mcfg.l_quark_candidates(ev)) == 5 ) #DS
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("4w2h1t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_4w2h1t"] = c

###
### FH_0w0w2h2t #all 4b categories: 7j,4b, 8j,4b, 9j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and #DS
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 ) 
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("0w0w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_0w0w2h2t"] = c

###
### FH_0w0w2h1t #all FH categories: 7j,4b, 8j,4b, 9j,4b, 7j,3b, 8j,3b, 9j,3b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and #DS
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 ) 
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("0w0w2h1t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_0w0w2h1t"] = c

###
### FH_0w0w1h2t #all FH categories: 7j,4b, 8j,4b, 9j,4b, 7j,3b, 8j,3b, 9j,3b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and #DS
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 ) 
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("0w0w1h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_0w0w1h2t"] = c

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
