from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf
from ROOT import MEM

# integrator options
#for k in ["FH_4w2h2t", "FH_3w2h2t", "FH_4w2h1t", "FH_0w2h2t", "FH_0w2h1t", "FH_0w1h2t"]:

for k, v in Conf.mem_configs.items():
    Conf.mem_configs[k].cfg.do_prefit = 0 #selects perms based on highest MEprob (Minimisation)
    Conf.mem_configs[k].cfg.do_perm_filtering = 1 #does runtime pruning of permutations

#    Conf.mem_configs[k].cfg.n_max_calls = 20000 #number of function calls per iteration (5 iterations)
#    Conf.mem_configs[k].cfg.is_default = False #must be false to set n_max_calls

#other options
Conf.general["passall"] = False
Conf.leptons["selection"] = lambda event: event.is_fh 
Conf.mem["selection"] = lambda event: (event.is_fh 
                                       and event.cat in ["cat7","cat8","cat9","cat10","cat11"]
                                       #and event.btag_LR_4b_2b > 0.95
                                       )
Conf.jets["untaggedSelection"] = "btagCSV" #or "btagLR"
Conf.jets["NJetsForBTagLR"] = 9

Conf.mem["calcME"] = True
Conf.mem["methodsToRun"] = [
            #"SL_0w2h2t",                 #[0]
            #"DL_0w2h2t",                 #[1]
            #"SL_1w2h2t",                 #[2]
            #"SL_2w2h1t_l",               #[3]
            #"SL_2w2h1t_h",               #[4]
            #"SL_2w2h2t",                 #[5]
            #"SL_2w2h2t_memLR",           #[6]
            #"SL_0w2h2t_memLR",           #[7]
            #"DL_0w2h2t_Rndge4t",         #[8]
            #"SL_2w2h2t_sj",              #[9]
            #"SL_0w2h2t_sj",              #[10]
            "FH_4w2h2t", #8j,4b & 9j,4b  #[11]
            "FH_3w2h2t", #7j,4b          #[12]
            "FH_4w2h1t", #7j,3b & 8j,3b  #[13]
            "FH_0w0w2h2t", #all 4b cats  #[14]
            "FH_0w0w2h1t", #all cats     #[15]
            #"FH_0w0w1h2t"  #all cats     #[16]   *********DO NOT RUN!!!********* 
        ]

Conf.general["verbosity"] = [
            #"eventboundary",
            #"input",
            #"matching",
            #"trigger",
            #"jets",
            #"gen", #print out gen-level info
            #"debug", #very high-level debug info
            #"reco", #info about reconstructed final state
            #"meminput", #info about particles used for MEM input
            #"commoninput" #print out inputs for CommonClassifier
       ]
