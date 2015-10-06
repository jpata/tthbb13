import os
from TTH.MEAnalysis.MEAnalysis_cfg_FH import Conf

Conf.general["sampleFile"]= os.environ["CMSSW_BASE"]+"/python/TTH/MEAnalysis/samples_data.py"

Conf.general["passall"] = True
Conf.trigger["filter"] =  False


Conf.mem["calcME"] = False


Conf.general["verbosity"] = (
            #"trigger",
            #"gen", #print out gen-level info
            #"debug", #very high-level debug info
            #"reco", #info about reconstructed final state
            #"meminput" #info about particles used for MEM input
       )
