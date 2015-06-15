import os
class Conf:
    def __init__(self):
        self.leptons = {
            "mu": {
                "tight": {
                    "pt": 30,
                    "eta":2.1,
                    "iso": 0.12
                },
                "tight_veto": {
                    "pt": 0.0,
                    "eta": 0.0,
                    "iso": 0.0,
                },
                "loose": {
                    "pt": 20,
                    "eta": 2.4,
                    "iso": 0.2,
                },
                "loose_veto": {
                    "pt": 0.0,
                    "eta": 0.0,
                    "iso": 0.0,
                },
                "isotype": "relIso03",
                "dxy": 0.2,

            },
            "el": {
                "tight": {
                    "pt": 30,
                    "eta": 2.5,
                    "iso": 0.1
                },
                "tight_veto": {
                    "pt": 20,
                    "eta": 2.5,
                    "iso": 0.15,
                },
                "loose": {
                    "pt": 20,
                    "eta": 2.2,
                    "iso": 0.15,
                },
                "loose_veto": {
                    "pt": 10,
                    "eta": 2.2,
                    "iso": 0.04,
                },
                "isotype": "relIso03",
                "dxy": 0.04,
            }
        }
        self.leptons["mu"]["tight_veto"] = self.leptons["mu"]["loose"]

        self.jets = {
            "pt": 30,
            "eta": 2.5,

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
            "sampleFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/python/samples_vhbb.py",
            "transferFunctionsPickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/transfer_functions.pickle",
            "transferFunctions_sj_Pickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/transfer_functions_sj.pickle",

            #If the list contains:
            # "gen" - print out the ttH gen-level particles (b from top, b form higgs, q from W, leptons
            # "reco" - print out the reco-level selected particles
            # "matching" - print out the association between gen and reco objects
            #"verbosity": ["eventboundary", "input", "matching", "gen", "reco", "meminput"],
            #"verbosity": ["meminput"],
            "verbosity": [],

            #Process only these events (will scan through file to find)
            #"eventWhitelist": [

            ##(1, 536, 537 ),

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
            "calcME": True,

            #Generic event-dependent selection function applied
            #just before the MEM. If False, MEM is skipped
            "selection": lambda event: True,

            "methodsToRun": [

                "SL_2qW",
                "SL_1qW",

                "SL_2qW_sj",
                "SL_1qW_sj",

                #"SL_2qW_NewTF",
                #"SL_1qW_NewTF",

                #"SL_2qW_sj_NewTF",
                #"SL_1qW_sj_NewTF",

                "SL_2qW_sj_perm",
                "SL_1qW_sj_perm",

                #"DL",

                #"SL_2qW_gen",
                #"SL_1qW_gen",
                #"DL_gen",

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
