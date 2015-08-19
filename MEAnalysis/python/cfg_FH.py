from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

#Conf.mem["calcME"] = True
Conf.leptons["selection"] = lambda event: event.is_fh
Conf.jets["NJetsForBTagLR"] = 8
