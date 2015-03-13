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
            "btagWPs": {"CSVM": ("btagCSV", 0.9)}
        }

        self.general = {
            "controlPlotsFile": "./root/ControlPlotsTEST.root"
        }
