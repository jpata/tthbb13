from TTH.Plotting.Datacards.MiniSamples import path

class Sample:
    def __init__(self, name, filenames, prefix):
        self.name = name
        self.filenames = filenames
        self.prefix = prefix 

samples_dict = {
    "SingleMuon": Sample(
        "SingleMuon",
        [path + "cfg_withME/SingleMuon.root"],
        ""
    ),
    "SingleElectron": Sample(
        "SingleElectron",
        [path + "cfg_withME/SingleElectron.root"],
        ""
    ),
    "DoubleMuon": Sample(
        "DoubleMuon",
        [path + "cfg_withME/DoubleMuon.root"],
        ""
    ),
    "DoubleEG": Sample(
        "DoubleEG",
        [path + "cfg_withME/DoubleEG.root"],
        ""
    ),
    "MuonEG": Sample(
        "MuonEG",
        [path + "cfg_withME/MuonEG.root"],
        ""
    ),

    "ttH_hbb": Sample(
        "ttH_hbb",
        [path + "cfg_withME/ttHTobb_M125_13TeV_powheg_pythia8.root"],
        ""
    ),
    "ttbarPlus2B": Sample(
        "ttbarPlus2B", 
        [path + "cfg_withME/TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root"],
        "",
    ),
    "ttbarPlusB": Sample(
        "ttbarPlusB", 
        [path + "cfg_withME/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root"],
        "",
    ),
    "ttbarPlusBBbar": Sample(
        "ttbarPlusBBbar", 
        [path + "cfg_withME/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root"],
        "",
    ),
    "ttbarPlusCCbar": Sample(
        "ttbarPlusCCbar", 
        [path + "cfg_withME/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root"],
        "",
    ),
    "ttbarOther": Sample(
        "ttbarOther", 
        [path + "cfg_withME/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root"],
        "",
    ),
}
