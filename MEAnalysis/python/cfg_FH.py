from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

#Conf.mem["calcME"] = True
Conf.leptons["selection"] = lambda event: event.is_fh
Conf.jets["NJetsForBTagLR"] = 8
        
Conf.trigger["HLTpaths"] = [
    "HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p5_2PFBTagCSV_v",
    "HLT_BIT_HLT_PFHT450_SixJet40_PFBTagCSV_v",
    "HLT_ttHhardonicLowLumi",
]
