import os

class Sample:
    def __init__(self, name, filenames):
        self.name = name
        self.fileNamesS2 = filenames


hostname = os.environ.get("HOSTNAME", "")
#PSI
if "t3ui12" in hostname:
    path = "/scratch/gregor/jpata/tth/Oct5_bdt_022sj_V13_47cdf50/"
#Jooseps laptop
elif "pata-slc6" in hostname:
    path = "/home/joosep/joosep-mac/Documents/tth/data/ntp/v12/Sep9_jec_jer/"
#Tallinn
elif "hep.kbfi.ee" in hostname:
    path = "/home/joosep/tth/gc/"
#elif "hep.kbfi.ee" in hostname:
#    path = "/hdfs/cms/store/user/jpata/tth/Sep28_spring15_prev13_f6c61f/"
else:
    raise Exception("Sample path not defined for hostname={0}!".format(hostname))

samples_dict = {
    "ttH_hbb"        : path + "ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
    "ttH_nohbb"      : path + "ttHToNonbb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2.root",        
    "ttbarPlus2B"    : path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_tt2b.root",
    "ttbarPlusB"     : path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttb.root",        
    "ttbarPlusBBbar" : path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttbb.root",
    "ttbarPlusCCbar" : path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttcc.root",
    "ttbarOther"     : path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ttll.root",    
    #"ttw_wlnu"       : path + "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
    #"ttw_wqq"        : path + "TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
    #"ttz_zllnunu"    : path + "TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
    #"ttz_zqq"        : path + "TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
}
