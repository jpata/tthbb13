class Datacard:
    #draw in these categories
    categories = [
        ("j3_t2", "numJets==3 && nBCSVM==2"),
        ("jge3_tge3", "numJets>=3 && nBCSVM==3"),
        ("jge4_t2", "numJets>=4 && nBCSVM==2"),
        ("jge4_tge4", "numJets>=4 && nBCSVM>=4"),

        #("4j", "numJets==4"),
        ("j4_t3", "numJets==4 && nBCSVM==3"),
        ("j4_t4", "numJets==4 && nBCSVM==4"),

        #("5j", "numJets==5"),
        #("5jL", "numJets==5 && nBCSVM<3"),
        ("j5_t3", "numJets==5 && nBCSVM==3"),
        #("5j4t", "numJets==5 && nBCSVM==4"),
        ("j5_tge4", "numJets==5 && nBCSVM>=4"),
        #("5jH", "numJets==5 && nBCSVM>4"),

        #("6j", "numJets==6"),
        #("6jL", "numJets==6 && nBCSVM<3"),
        #("6j3t", "numJets==6 && nBCSVM==3"),
        #("6j4t", "numJets==6 && nBCSVM==4"),
        #("6jH", "numJets==6 && nBCSVM>4"),

        #("6plusj", "numJets>=6"),
        ("jge6_t2", "numJets>=6 && nBCSVM==2"),
        ("jge6_t3", "numJets>=6 && nBCSVM==3"),
        #("6plusj4t", "numJets>=6 && nBCSVM==4"),
        ("jge6_tge4", "numJets>=6 && nBCSVM>=4"),
        #("6plusjH", "numJets>=6 && nBCSVM>4"),
    ]

    #Draw histograms with these systematic weights
    weights = [

            #no weights applied
            ("unweighted",          "1.0"),
            
            #only b weight applied
            #("bw",                  "bTagWeight"),
            
            #Use JES-corrected values
            ("",                    "bTagWeight"),
            
            
            #JES up/down
            #("CMS_scale_jUp",       "bTagWeight_JESUp"),
            #("CMS_scale_jDown",     "bTagWeight_JESDown"),
            
            #CSV LF up/down
            ("CMS_ttH_CSVLFUp",     "bTagWeight_LFUp"),
            ("CMS_ttH_CSVLFDown",   "bTagWeight_LFDown"),
            #("bwLFDown",        "bTagWeight_LFDown"),
            # ("bwHFUp",          "bTagWeight_HFUp"),
            # ("bwHFDown",        "bTagWeight_HFDown"),
            # ("bwStats1Up",      "bTagWeight_Stats1Up"),
            # ("bwStats1Down",    "bTagWeight_Stats1Down"),
            # ("bwStats2Up",      "bTagWeight_Stats2Up"),
            # ("bwStats2Down",    "bTagWeight_Stats2Down"),
    ]

    #Enable the plotting of these samples
    samples = [
        "ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hbb",
        #"tth_13tev_amcatnlo_pu20bx25_hbb",
        #"tth_13tev_amcatnlo_pu20bx25_hX",
        "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_tt2b",
        "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttb",
        "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttbb",
        "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttcc",
        "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttll",
        #"ttw_13tev_madgraph_pu20bx25_phys14",
        #"ttz_13tev_madgraph_pu20bx25_phys14"
    ]

    output_filename = "ControlPlots_powheg.root"
