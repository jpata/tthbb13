from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

Conf.mem["calcME"] = False
Conf.general["verbosity"] = [
    "eventboundary",
    "trigger",
    "input",
    "gen",
    "debug",
    "reco",
    "meminput",
    "commoninput"
]
