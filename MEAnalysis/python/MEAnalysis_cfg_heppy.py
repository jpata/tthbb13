import os

def mu_baseline(mu):
    return (
        mu.tightId and
        mu.isPFMuon and
        mu.isGlobalMuon and
        mu.dxy < 0.2 and
        mu.dz < 0.5 and
        mu.globalTrackChi2 < 10 and
        mu.nMuonHits > 0 and
        mu.pixelHits > 0 and
        mu.nStations > 1 #FIXME: is this the same as nMuonHits
    )

def el_baseline_tight(el):
    sca = abs(el.etaSc)
    ret = (
        not(sca > 1.442 and sca < 1.5660) and
        el.convVeto
    )
    if not ret:
        return False

    if sca <= 1.479:
        ret = ret and (
            (abs(el.eleDEta)    < 0.006046) and
            (abs(el.eleDPhi)    < 0.028092) and
            (el.eleSieie        < 0.009947) and
            (el.eleHoE          < 0.045772) and
            (abs(el.dxy)        < 0.008790) and
            (abs(el.dz)         < 0.021226) and
            (el.relIso03        < 0.069537)
            #FIXME: expectedMissingInnerHits and hOverE 
        )
    elif sca < 2.5:
        ret = ret and (
            (abs(el.eleDEta)    < 0.007057) and
            (abs(el.eleDPhi)    < 0.030159) and
            (el.eleSieie        < 0.028237) and
            (el.eleHoE          < 0.067778) and
            (abs(el.dxy)        < 0.027984) and
            (abs(el.dz)         < 0.133431) and
            (el.relIso03        < 0.078265)
            #FIXME: expectedMissingInnerHits and hOverE 
        )
    return ret

def el_baseline_medium(el):
    sca = abs(el.etaSc)
    ret = (
        not(sca > 1.442 and sca < 1.5660) and
        el.convVeto
    )
    if not ret:
        return False

    if sca <= 1.479:
        ret = ret and (
            (abs(el.eleDEta)    < 0.008925) and
            (abs(el.eleDPhi)    < 0.035973) and
            (el.eleSieie        < 0.009996) and
            (el.eleHoE          < 0.050537) and
            (abs(el.dxy)        < 0.012235) and
            (abs(el.dz)         < 0.042020) and
            (el.relIso03        < 0.069537) #and
            #(el.eleExpMIHits    < 0.069537) #
            #(el.ooEmooP         < 0.069537) #
        )
    elif sca < 2.5:
        ret = ret and (
            (abs(el.eleDEta)    < 0.007429) and
            (abs(el.eleDPhi)    < 0.067879) and
            (el.eleSieie        < 0.030135) and
            (el.eleHoE          < 0.086782) and
            (abs(el.dxy)        < 0.036719) and
            (abs(el.dz)         < 0.138142) and
            (el.relIso03        < 0.113254) #and
            #(el.eleExpMIHits    < 0.069537) #
            #(el.ooEmooP         < 0.069537) #
        )
    return ret

def el_baseline_loose(el):
    sca = abs(el.etaSc)
    ret = (
        not(sca > 1.442 and sca < 1.5660) and
        el.convVeto
    )
    if not ret:
        return False

    if sca <= 1.479:
        ret = ret and (
            (abs(el.eleDEta)    < 0.009277) and
            (abs(el.eleDPhi)    < 0.094739) and
            (el.eleSieie        < 0.010331) and
            (el.eleHoE          < 0.093068) and
            (abs(el.dxy)        < 0.035904) and
            (abs(el.dz)         < 0.075496) and
            (el.relIso03        < 0.130136) #and
            #(el.eleExpMIHits    < 0.069537) #
            #(el.ooEmooP         < 0.069537) #
        )
    elif sca < 2.5:
        ret = ret and (
            (abs(el.eleDEta)    < 0.009833) and
            (abs(el.eleDPhi)    < 0.149934) and
            (el.eleSieie        < 0.031838) and
            (el.eleHoE          < 0.115754) and
            (abs(el.dxy)        < 0.099266) and
            (abs(el.dz)         < 0.197897) and
            (el.relIso03        < 0.163368) #and
            #(el.eleExpMIHits    < 0.069537) #
            #(el.ooEmooP         < 0.069537) #
        )
    return ret


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
    def __init__(self):
        self.leptons = {
            "mu": {

                #SL
                "tight": {
                    "pt": 30,
                    "eta":2.1,
                    "iso": 0.12,
                    "idcut": mu_baseline
                },
                "tight_veto": {
                    "pt": 10.0,
                    "eta": 2.4,
                    "iso": 0.2,
                    "idcut": mu_baseline
                },

                #DL
                "loose": {
                    "pt": 20,
                    "eta": 2.4,
                    "iso": 0.12,
                    "idcut": mu_baseline
                },
                "loose_veto": {
                    "pt": 10.0,
                    "eta": 2.4,
                    "iso": 0.2,
                    "idcut": mu_baseline
                },
                "isotype": "relIso04",
            },


            "el": {
                "tight": {
                    "pt": 30,
                    "eta": 2.1,
                    "iso": 0.1,
                    "idcut": lambda el: el_baseline_medium(el)
                },
                "tight_veto": {
                    "pt": 20,
                    "eta": 2.4,
                    "iso": 0.15,
                    "idcut": lambda el: el_baseline_loose(el)
                },

                "loose": {
                    "pt": 20,
                    "eta": 2.4,
                    "iso": 0.15,
                    "idcut": lambda el: el_baseline_medium(el)
                },
                "loose_veto": {
                    "pt": 10,
                    "eta": 2.4,
                    "iso": 0.04,
                    "idcut": lambda el: el_baseline_loose(el)
                },
                "isotype": "relIso03",
            }
        }

        self.jets = {
            "pt": 30,
            "eta": 2.4,

            #The default b-tagging algorithm (branch name)
            "btagAlgo": "btagCSV",

            #The default b-tagging WP
            "btagWP": "CSVM",

            #These working points are evaluated and stored in the trees as nB* - number of jets passing the WP
            #https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagging#Preliminary_working_or_operating
            "btagWPs": {
                "CSVM": ("btagCSV", 0.814),
                "CSVL": ("btagCSV", 0.423),
                "CSVT": ("btagCSV", 0.941)
            },

            #if btagCSV, untagged/tagged selection for W mass and MEM is done by CSVM cut
            #if btagLR, selection is done by the btag likelihood ratio permutation
            "untaggedSelection": "btagCSV"
        }

        self.general = {
            "controlPlotsFileOld": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/ControlPlotsTEST.root",
            "controlPlotsFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/ControlPlotsV6.root",
            "sampleFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/python/samples_722sync.py",
            "transferFunctionsPickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/transfer_functions.pickle",

            #If the list contains:
            # "gen" - print out the ttH gen-level particles (b from top, b form higgs, q from W, leptons
            # "reco" - print out the reco-level selected particles
            # "matching" - print out the association between gen and reco objects
            #"verbosity": ["eventboundary", "input", "matching", "gen", "reco", "meminput"],
            "verbosity": [],

            #Process only these events (will scan through file to find)
            #"eventWhitelist": [
                #('MEM', 1, 214, 21320, 'cat2', 'H', 7, 5, 1, 0, 'JES')
            #    (1, 214, 21320),
            ##    #cat6
            ##    (1, 1326, 132576),
            ##    (1, 1001, 100098),
            ##    (1, 1075, 107401),
            ##    (1, 1910, 190937),
            ##    (1, 739, 73869),

            ##    #root [2] tree->Scan("run:lumi:evt:mem_tth_p[0]", "njets==6 && nBCSVM==4 && is_sl==1 && mem_tth_p[0]==0")
            ##    (1,  558,  55798),
            ##    (1,  566,  56576),
            ##    (1,   12,   1121),
            ##    (1,  714,  71316),
            ##    (1, 1222, 122152),
            ##    (1,  856,  85542),
            ##    (1,  300,  29931),
            ##    (1, 1675, 167428),
            #]
        }

        self.mem = {

            #Actually run the ME calculation
            #If False, all ME values will be 0
            "calcME": False,

            #Generic event-dependent selection function applied
            #just before the MEM. If False, MEM is skipped
            "selection": lambda event: True,

            "methodsToRun": [

                # ALL
                "SL_2w2h2t"   ,
                "SL_1w2h2t"   ,
                #"SL_2w2h1t_h" ,
                #"SL_2w2h1t_l" ,
                "SL_0w2h2t"   ,
                #"SL_1w2h1t_h" ,
                #"SL_1w2h1t_l" ,
                "SL_2w2h2t_wtag",

                #"SL_2qW",
                #"SL_1qW",
                "DL",

#                "SL_2qW_gen",
#                "SL_1qW_gen",
#                "DL_gen",

                #"SL_0qW",
                #"SL_1bT",
                #"SL_1bTbar",
                #"SL_1bH",
                #"SL_2qW_notag",

                #"SL_2qW_Sudakov",
                #"SL_1qW_Sudakov",
                #"SL_2qW_Recoil",
                #"SL_1qW_Recoil",
                #"DL_Recoil",

                #"SL_2qW_NewTF",
                #"SL_1qW_NewTF",
                #"DL_NewTF",
                #"SL_2qW_Minimize",
                #"SL_1qW_Minimize",
                #"DL_Minimize",

                #"SL_2qW_gen_nosmear",
                #"SL_1qW_gen_nosmear",
                #"DL_gen_nosmear",
            ],

        }
