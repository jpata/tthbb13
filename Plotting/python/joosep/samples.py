sample_shortname = {
    "ttbarPlusBBbar": "tt+bb",
    "ttbarPlusB": "tt+b",
    "ttbarPlus2B": "tt+2b",
    "ttbarPlusCCbar": "tt+cc",
    "ttbarOther": "tt+ll",
    #"ttw_13tev_madgraph_pu20bx25_phys14": "tt+W",
    #"ttz_13tev_madgraph_pu20bx25_phys14": "tt+Z",
    "ttH": "tt+H",
    "ttH_hbb": "tt+H(bb)",
    "ttH_hX": "tt+H(X)",
    #"tth_13tev_amcatnlo_pu20bx25_hX": "tt+HX",
    #"tth_13tev_amcatnlo_pu20bx25_hbb": "tt+Hbb",
}
samples_latex = [
    #("tth_13tev_amcatnlo_pu20bx25", "$\\mathrm{t}\\bar{\\mathrm{t}} + \mathrm{H}$"),
    ("ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8", "$\\mathrm{t}\\bar{\\mathrm{t}} + \mathrm{H}$"),
    ("ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hbb", "$\\mathrm{t}\\bar{\\mathrm{t}} + \mathrm{Hbb}$"),
    ("ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hX", "$\\mathrm{t}\\bar{\\mathrm{t}} + \mathrm{HX}$"),
    #("tth_13tev_amcatnlo_pu20bx25_hX", "$\\mathrm{t}\\bar{\\mathrm{t}} + \mathrm{HX}$"),
    ("TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttll", "$\\mathrm{t}\\bar{\\mathrm{t}} + \mathrm{ll}$"),
    ("TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttb", "$\\mathrm{t}\\bar{\\mathrm{t}} + \mathrm{b}$"),
    ("TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttbb", "$\\mathrm{t}\\bar{\\mathrm{t}} + \mathrm{bb}$"),
    ("TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_tt2b", "$\\mathrm{t}\\bar{\\mathrm{t}} + 2\mathrm{b}$"),
    ("TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttcc", "$\\mathrm{t}\\bar{\\mathrm{t}} + \mathrm{cc}$"),
    #("ttw_13tev_madgraph_pu20bx25_phys14", "$\\mathrm{t}\\bar{\\mathrm{t}} + \mathrm{W}$"),
    #("ttz_13tev_madgraph_pu20bx25_phys14", "$\\mathrm{t}\\bar{\\mathrm{t}} + \mathrm{Z}$"),
]

path = "/Users/joosep/Documents/tth/data/ntp/v12/Sep4_fullrun/"

class Sample:
    def __init__(self, name, filenames):
        self.name = name
        self.fileNamesS2 = filenames

samples_dict = {
    "ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hbb": Sample(
        "ttH_hbb",
        [path + "ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hbb.root"]
    ),
    "ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hX": Sample(
        "ttH_nohbb",
        [path + "ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hX.root"]
    ),
    
    "ttHTobb_M125_13TeV_powheg_pythia8_hbb": Sample(
        "ttH_hbb",
        [path + "ttHTobb_M125_13TeV_powheg_pythia8_hbb.root"]
    ),
    "ttHTobb_M125_13TeV_powheg_pythia8_hX": Sample(
        "ttH_nohbb",
        [path + "ttHTobb_M125_13TeV_powheg_pythia8_hX.root"]
    ),
    
    "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_tt2b": Sample(
        "ttbarPlus2B",
        [path + "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_tt2b.root"]
    ),
    "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttb": Sample(
        "ttbarPlusB",
        [path + "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttb.root"]
    ),
    "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttbb": Sample(
        "ttbarPlusBBbar",
        [path + "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttbb.root"]
    ),
    "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttcc": Sample(
        "ttbarPlusCCbar",
        [path + "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttcc.root"]
    ),
    "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttll": Sample(
        "ttbarOther",
        [path + "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttll.root"]
    ),
    
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b": Sample(
        "ttbarPlus2B",
        [path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root"]
    ),
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb": Sample(
        "ttbarPlusB",
        [path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root"]
    ),
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb": Sample(
        "ttbarPlusBBbar",
        [path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root"]
    ),
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc": Sample(
        "ttbarPlusCCbar",
        [path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root"]
    ),
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll": Sample(
        "ttbarOther",
        [path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root"]
    ),
    

    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll": Sample(
        "ttbarOther",
        [path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root"]
    ),
    # "ttw_13tev_madgraph_pu20bx25_phys14": Sample(
    #     "ttbarW",
    #     [path + "ttw_13tev_madgraph_pu20bx25_phys14.root"]
    # ),
    # "ttz_13tev_madgraph_pu20bx25_phys14": Sample(
    #     "ttbarZ",
    #     [path + "ttz_13tev_madgraph_pu20bx25_phys14.root"]
    # ),
}

#Extracted using apple color picker from CMS combination paper
colors = {
    "ttbarOther": (251, 102, 102),
    "ttbarPlusCCbar": (204, 2, -0),
    "ttbarPlusB": (153, 51, 51),
    "ttbarPlusBBbar": (102, 0, 0),
    "ttbarPlus2B": (80, 0, 0),
    "ttH": (44, 62, 167),
    "ttH_hbb": (44, 62, 167),
    "ttH_hX": (39, 57, 162),
    "other": (251, 73, 255),
}

for n in colors.keys():
    colors[n] = tuple(map(lambda x: float(x)/255.0, list(colors[n])))
    
cut_map = {
    "sl_j4_t3": r"SL, $N_j=4\ N_t=3$",
    "sl_j4_t4": r"SL, $N_j=4\ N_t=4$",
    "sl_j5_t3": r"SL, $N_j=5\ N_t=3$",
    "sl_j5_tge4": r"SL, $N_j=5\ N_t \geq 4$",
    "sl_jge6_t2": r"SL, $N_j\geq 6\ N_t=2$",
    "sl_jge6_t3": r"SL, $N_j\geq 6\ N_t=3$",
    "sl_jge6_tge4": r"SL, $N_j\geq 6\ N_t\geq4$",
    "dl_j3_t2": r"DL, $N_j=3\ N_t=2$",
    "dl_jge3_tge3": r"DL, $N_j\geq3\ N_t\geq3$",
    "dl_jge4_t2": r"DL, $N_j\geq4\ N_t=2$",
    "dl_jge4_tge4": r"DL, $N_j\geq4\ N_t\geq4$",
}
