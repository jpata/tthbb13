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

            #If the list contains:
            # "gen" - print out the ttH gen-level particles (b from top, b form higgs, q from W, leptons
            # "reco" - print out the reco-level selected particles
            # "matching" - print out the association between gen and reco objects
            #"verbosity": ["eventboundary", "input", "matching", "gen", "reco"],
            "verbosity": [],

            #Process only these events (will scan through file to find)
            #"eventWhitelist": [
            #    (1, 1201, 120035),
            #    #(1, 626, 62574),
            #    #(1, 180, 17914)
            #]
        }

        self.mem = {

            #Actually run the ME calculation
            #If False, all ME values will be 0
            #"calcME": True,
            "calcME": True,

            #Which categories to analyze the matrix element in
            "MECategories": ["cat1", "cat2", "cat3", "cat6"],
            #"MECategories": ["cat1"],

            #If bLR > cut, calculate ME
            #only used if untaggedSelection=btagLR
            "btagLRCut": {
                "cat1": -100.0,
                "cat2": -100.0,
                "cat3": -100.0,
                "cat6": -100.0
            },

            #if a number is N specified for wq, tb, hb (+ _btag), require
            #that reco jets dR matched to quarks from W, top, higgs >= N
            #in order to calculate the ME.
            #If disabled, calculate ME regardless of gen-level matching
            "requireMatched": {
                #"cat2": {
                #    "wq_btag": 1,
                #    "hb_btag": 2,
                #    "tb_btag": 2,
                #},
                #"cat1": {
                #   "wq_btag": 2,
                #   "hb_btag": 2,
                #   "tb_btag": 2,
                #},
                #"cat3": {
                #    "wq_btag": 1,
                #    "hb_btag": 2,
                #    "tb_btag": 2,
                #},
            },

            "methodsToRun": [

                #full ME
                "default",

                #These are additional MEM checks, where only part of the MEM is ran.
                #Switched off by default

                #"NumPointsDouble",
                #"NumPointsHalf",
                #"NoJacobian",
                #"NoDecayAmpl",
                #"NoPDF",
                #"NoScattAmpl",
                #"QuarkEnergy98",
                #"NuPhiRestriction",
                #"JetsPtOrder",
                #"JetsPtOrderIntegrationRange",
            ],

        }
