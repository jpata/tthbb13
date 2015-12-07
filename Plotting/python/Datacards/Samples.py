import os
hostname = os.environ.get("HOSTNAME", "")
if "t3ui12" in hostname:
    path = "/scratch/gregor/jpata/tth/Oct5_bdt_022sj_V13_47cdf50/"
#Jooseps laptop
elif "pata-slc6" in hostname:
    path = "/home/joosep/joosep-mac/Documents/tth/data/ntp/v14/me/"
elif "pata-macbook" in hostname:
    path = "/Users/joosep/Documents/tth/data/ntp/v16/me/"
#Tallinn
elif "quasar" in hostname:
    path = "/dev/shm/joosep/"
elif "hep.kbfi.ee" in hostname:
    path = "/home/joosep/tth/gc/"
else:
    raise Exception("Sample path not defined for hostname={0}!".format(hostname))

class Sample:
    def __init__(self, name, filenames, prefix):
        self.name = name
        self.filenames = filenames
        self.prefix = prefix 

samples_dict = {
    "SingleMuon": Sample(
        "SingleMuon",
        [path + "cfg_withME_updateBWeight/SingleMuon.root"],
        ""
    ),
    "SingleElectron": Sample(
        "SingleElectron",
        [path + "cfg_withME_updateBWeight/SingleElectron.root"],
        ""
    ),
    "DoubleMuon": Sample(
        "DoubleMuon",
        [path + "cfg_withME_updateBWeight/DoubleMuon.root"],
        ""
    ),
    "DoubleEG": Sample(
        "DoubleEG",
        [path + "cfg_withME_updateBWeight/DoubleEG.root"],
        ""
    ),
    "MuonEG": Sample(
        "MuonEG",
        [path + "cfg_withME_updateBWeight/MuonEG.root"],
        ""
    ),

    "ttH_hbb": Sample(
        "ttH_hbb",
        [path + "cfg_withME_updateBWeight/ttHTobb_M125_13TeV_powheg_pythia8.root"],
        ""
    ),
    "ttbarPlus2B": Sample(
        "ttbarPlus2B", 
        [path + "cfg_withME_updateBWeight/TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root"],
        "",
    ),
    "ttbarPlusB": Sample(
        "ttbarPlusB", 
        [path + "cfg_withME_updateBWeight/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root"],
        "",
    ),
    "ttbarPlusBBbar": Sample(
        "ttbarPlusBBbar", 
        [path + "cfg_withME_updateBWeight/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root"],
        "",
    ),
    "ttbarPlusCCbar": Sample(
        "ttbarPlusCCbar", 
        [path + "cfg_withME_updateBWeight/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root"],
        "",
    ),
    "ttbarOther": Sample(
        "ttbarOther", 
        [path + "cfg_withME_updateBWeight/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root"],
        "",
    ),
    
#    "ttH_hbb_cfg_noME_jetPt20": Sample(
#        "ttH_hbb",
#        [path + "cfg_noME_jetPt20/ttHTobb_M125_13TeV_powheg_pythia8.root"],
#        "_cfg_noME_jetPt20"
#    ),
#    "ttbarPlus2B_cfg_noME_jetPt20": Sample(
#        "ttbarPlus2B", 
#        [path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root"],
#        "_cfg_noME_jetPt20"
#    ),
#    "ttbarPlusB_cfg_noME_jetPt20": Sample(
#        "ttbarPlusB", 
#        [path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root"],
#        "_cfg_noME_jetPt20"
#    ),
#    "ttbarPlusBBbar_cfg_noME_jetPt20": Sample(
#        "ttbarPlusBBbar", 
#        [path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root"],
#        "_cfg_noME_jetPt20"
#    ),
#    "ttbarPlusCCbar_cfg_noME_jetPt20": Sample(
#        "ttbarPlusCCbar", 
#        [path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root"],
#        "_cfg_noME_jetPt20"
#    ),
#    "ttbarOther_cfg_noME_jetPt20": Sample(
#        "ttbarOther", 
#        [path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root"],
#        "_cfg_noME_jetPt20"
#    ),
#    
#    "ttH_hbb_cfg_noME_btagBDT": Sample(
#        "ttH_hbb",
#        [path + "cfg_noME_btagBDT/ttHTobb_M125_13TeV_powheg_pythia8.root"],
#        "_cfg_noME_btagBDT"
#    ),
#    "ttbarPlus2B_cfg_noME_btagBDT": Sample(
#        "ttbarPlus2B", 
#        [path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root"],
#        "_cfg_noME_btagBDT"
#    ),
#    "ttbarPlusB_cfg_noME_btagBDT": Sample(
#        "ttbarPlusB", 
#        [path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root"],
#        "_cfg_noME_btagBDT"
#    ),
#    "ttbarPlusBBbar_cfg_noME_btagBDT": Sample(
#        "ttbarPlusBBbar", 
#        [path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root"],
#        "_cfg_noME_btagBDT"
#    ),
#    "ttbarPlusCCbar_cfg_noME_btagBDT": Sample(
#        "ttbarPlusCCbar", 
#        [path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root"],
#        "_cfg_noME_btagBDT"
#    ),
#    "ttbarOther_cfg_noME_btagBDT": Sample(
#        "ttbarOther", 
#        [path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root"],
#        "_cfg_noME_btagBDT"
#    )
}
