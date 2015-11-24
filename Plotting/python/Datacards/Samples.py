from TTH.Plotting.Datacards.MiniSamples import path

class Sample:
    def __init__(self, name, filenames, prefix):
        self.name = name
        self.filenames = filenames
        self.prefix = prefix 

samples_dict = {
    "ttH_hbb_cfg_noME": Sample(
        "ttH_hbb",
        [path + "cfg_noME/ttHTobb_M125_13TeV_powheg_pythia8.root"],
        ""
    ),
    "ttbarPlus2B_cfg_noME": Sample(
        "ttbarPlus2B", 
        [path + "cfg_noME/TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root"],
        "",
    ),
    "ttbarPlusB_cfg_noME": Sample(
        "ttbarPlusB", 
        [path + "cfg_noME/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root"],
        "",
    ),
    "ttbarPlusBBbar_cfg_noME": Sample(
        "ttbarPlusBBbar", 
        [path + "cfg_noME/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root"],
        "",
    ),
    "ttbarPlusCCbar_cfg_noME": Sample(
        "ttbarPlusCCbar", 
        [path + "cfg_noME/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root"],
        "",
    ),
    "ttbarOther_cfg_noME": Sample(
        "ttbarOther", 
        [path + "cfg_noME/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root"],
        "",
    ),
    
    "ttH_hbb_cfg_noME_jetPt20": Sample(
        "ttH_hbb",
        [path + "cfg_noME_jetPt20/ttHTobb_M125_13TeV_powheg_pythia8.root"],
        "_cfg_noME_jetPt20"
    ),
    "ttbarPlus2B_cfg_noME_jetPt20": Sample(
        "ttbarPlus2B", 
        [path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root"],
        "_cfg_noME_jetPt20"
    ),
    "ttbarPlusB_cfg_noME_jetPt20": Sample(
        "ttbarPlusB", 
        [path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root"],
        "_cfg_noME_jetPt20"
    ),
    "ttbarPlusBBbar_cfg_noME_jetPt20": Sample(
        "ttbarPlusBBbar", 
        [path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root"],
        "_cfg_noME_jetPt20"
    ),
    "ttbarPlusCCbar_cfg_noME_jetPt20": Sample(
        "ttbarPlusCCbar", 
        [path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root"],
        "_cfg_noME_jetPt20"
    ),
    "ttbarOther_cfg_noME_jetPt20": Sample(
        "ttbarOther", 
        [path + "cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root"],
        "_cfg_noME_jetPt20"
    ),
    
    "ttH_hbb_cfg_noME_btagBDT": Sample(
        "ttH_hbb",
        [path + "cfg_noME_btagBDT/ttHTobb_M125_13TeV_powheg_pythia8.root"],
        "_cfg_noME_btagBDT"
    ),
    "ttbarPlus2B_cfg_noME_btagBDT": Sample(
        "ttbarPlus2B", 
        [path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root"],
        "_cfg_noME_btagBDT"
    ),
    "ttbarPlusB_cfg_noME_btagBDT": Sample(
        "ttbarPlusB", 
        [path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root"],
        "_cfg_noME_btagBDT"
    ),
    "ttbarPlusBBbar_cfg_noME_btagBDT": Sample(
        "ttbarPlusBBbar", 
        [path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root"],
        "_cfg_noME_btagBDT"
    ),
    "ttbarPlusCCbar_cfg_noME_btagBDT": Sample(
        "ttbarPlusCCbar", 
        [path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root"],
        "_cfg_noME_btagBDT"
    ),
    "ttbarOther_cfg_noME_btagBDT": Sample(
        "ttbarOther", 
        [path + "cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root"],
        "_cfg_noME_btagBDT"
    )
}
