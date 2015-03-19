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
            "pt": 40,
            "eta": 2.5,
            "btagAlgo": "btagCSV",
            "btagWP": "CSVM",
            "btagWPs": {
                "CSVM": ("btagCSV", 0.814),
                "CSVL": ("btagCSV", 0.423),
                "CSVT": ("btagCSV", 0.941)
            }
        }

        self.general = {
            "controlPlotsFileOld": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/ControlPlotsTEST.root",
            "controlPlotsFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/ControlPlotsV6.root",
            "sampleFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/python/samples_vhbb.py",
            #"calcMECategories": []
        }

        self.mem = {

            #Actually run the ME calculation
            "calcME": True,

            #Which categories to analyze the matrix element in
            "MECategories": ["cat1", "cat2", "cat3", "cat6"],

            #If bLR > cut, calculate ME
            "btagLRCut": {
                "cat1": 0.7,
                "cat2": 0.7,
                "cat3": 0.7,
                "cat6": 0.7
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
                #    "wq_btag": 2,
                #    "hb_btag": 2,
                #    "tb_btag": 2,
                #},
                #"cat3": {
                #    "wq_btag": 1,
                #    "hb_btag": 2,
                #    "tb_btag": 2,
                #},
            }
        }
