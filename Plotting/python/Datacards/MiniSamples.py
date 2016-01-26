import os

hostname = os.environ.get("HOSTNAME", "")
#PSI
if "t3ui12" in hostname:
    path = "/scratch/gregor/jpata/tth/Oct5_bdt_022sj_V13_47cdf50/"
#Jooseps laptop
elif "pata-slc6" in hostname:
    path = "/home/joosep/joosep-mac/Documents/tth/data/ntp/v14/me/"
elif "pata-macbook" in hostname:
    path = "/Users/joosep/Documents/tth/data/ntp/v14/me/"
#Tallinn
elif "quasar" in hostname:
    path = "/scratch/joosep/"
elif "hep.kbfi.ee" in hostname:
    path = "/home/joosep/tth/gc/"
else:
    print "Sample path not defined for hostname={0}!".format(hostname)
    path = ""

samples_dict = {
    #"SingleMuon"     : path + "SingleMuon.root",
    #"SingleElectron" : path + "SingleElectron.root",
    #"DoubleMuon"     : path + "DoubleMuon.root",
    #"DoubleEG"       : path + "DoubleEG.root",
    #"MuonEG"         : path + "MuonEG.root",
    "ttH_hbb"        : path + "ttHTobb_M125_13TeV_powheg_pythia8.root",
    #"ttH_nohbb"      : path + "ttHToNonbb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2.root",        
    "ttbarPlus2B"    : path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root",
    "ttbarPlusB"     : path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root",
    "ttbarPlusBBbar" : path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root",
    "ttbarPlusCCbar" : path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root",
    "ttbarOther"     : path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root",
    
#    "ttH_hbb"        : path + "cfg_noME_jetPt20/ttHTobb_M125_13TeV_powheg_pythia8.root",
#    #"ttH_nohbb"      : path + "ttHToNonbb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2.root",        
#    "ttbarPlus2B"    : path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root",
#    "ttbarPlusB"     : path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root",
#    "ttbarPlusBBbar" : path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root",
#    "ttbarPlusCCbar" : path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root",
#    "ttbarOther"     : path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root",
#    
#    "ttH_hbb"        : path + "cfg_noME_btagBDT/ttHTobb_M125_13TeV_powheg_pythia8.root",
#    #"ttH_nohbb"      : path + "ttHToNonbb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2.root",        
#    "ttbarPlus2B"    : path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root",
#    "ttbarPlusB"     : path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root",
#    "ttbarPlusBBbar" : path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root",
#    "ttbarPlusCCbar" : path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root",
#    "ttbarOther"     : path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root",
    #"SingleMuon"     : path + "SingleMuon.root",
    #"SingleElectron" : path + "SingleElectron.root",
    #"ttw_wlnu"       : path + "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
    #"ttw_wqq"        : path + "TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
    #"ttz_zllnunu"    : path + "TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
    #"ttz_zqq"        : path + "TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root",
}
