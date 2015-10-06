from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

#Conf.mem["calcME"] = True
Conf.general["passall"] = False
Conf.leptons["selection"] = lambda event: event.is_fh
Conf.jets["NJetsForBTagLR"] = 8
        

Conf.trigger["paths"] =  (
            #FH triggers: in separate config file
            "HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p5_2PFBTagCSV_v",
            "HLT_BIT_HLT_PFHT450_SixJet40_PFBTagCSV_v",
            "HLT_ttHhardonicLowLumi",
            )

Conf.mem["calcME"] = False
Conf.mem["methodsToRun"] = (
            #"SL_0w2h2t",
            #"DL_0w2h2t",
            #"SL_1w2h2t",
            #"SL_2w2h1t_l",
            #"SL_2w2h1t_h",
            #"SL_2w2h2t",
            #"SL_2w2h2t",
            #"SL_2w2h2t_sj",
            #"SL_2w2h2t_memLR",
            #"SL_0w2h2t_memLR",
            #"DL_0w2h2t_Rndge4t",
            "FH"
        )

Conf.general["verbosity"] = (
            #"trigger",
            #"gen", #print out gen-level info
            #"debug", #very high-level debug info
            #"reco", #info about reconstructed final state
            #"meminput" #info about particles used for MEM input
       )
