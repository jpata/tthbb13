
#https://twiki.cern.ch/twiki/bin/view/CMS/TTbarHbbRun2ReferenceAnalysis
# Proposed selection steps for dilepton analyses
# Step1a: Apply dilepton triggers
# Step1: Check if the first primary vertex is of good quality
# Step2: >=2 OS leptons (pT>20, |eta|<2.4)
# Step3: mll>20
# Step4: Exclude Z window for ee and mumu
# Step5: >=2 jets (pT>30, |eta|<2.4) and the rest pT>20 GeV
# Step6: MET>=40 for ee and mumu
# Step7: >=1 medium WP b-tagged jet

#dl_cuts = "is_dl==1 && ll_mass>20 && passPV==1 && abs(ll_mass-91.2)>8 && (abs(leps_pdgId[0])==abs(leps_pdgId[1]) ? met_pt>40 : 1) && sign(leps_pdgId[0])!=sign(leps_pdgId[1])"
dl_cuts = "is_dl==1 && passPV==1 && (abs(leps_pdgId[0])==abs(leps_pdgId[1]) ? met_pt>40 : 1) && sign(leps_pdgId[0])!=sign(leps_pdgId[1])"
sl_cuts = "is_sl==1 && passPV==1"

class Datacard:
    #draw in these categories
    # (name, cut-string, decision variable to use)
    categories = [
        #("dl_j3_t2", dl_cuts + " && numJets==3 && nBCSVM==2"),
        #("dl_jge3_tge3", dl_cuts + "&& numJets>=3 && nBCSVM==3"),
        #("dl_jge4_t2", dl_cuts + "&& numJets>=4 && nBCSVM==2"),
        #("dl_jge4_tge4", dl_cuts + "&& numJets>=4 && nBCSVM>=4"),

        #("4j", "numJets==4"),
        #("sl_j4_t3", sl_cuts + " && numJets==4 && nBCSVM==3"),
        #("sl_j4_t4", "numJets==4 && nBCSVM==4"),

        #("5j", "numJets==5"),
        #("5jL", "numJets==5 && nBCSVM<3"),
        #("sl_j5_t3", sl_cuts + " && numJets==5 && nBCSVM==3"),
        #("5j4t", "numJets==5 && nBCSVM==4"),
        #("sl_j5_tge4", sl_cuts + " && numJets==5 && nBCSVM>=4"),
        #("5jH", "numJets==5 && nBCSVM>4"),

        #("6j", "numJets==6"),
        #("6jL", "numJets==6 && nBCSVM<3"),
        #("6j3t", "numJets==6 && nBCSVM==3"),
        #("6j4t", "numJets==6 && nBCSVM==4"),
        #("6jH", "numJets==6 && nBCSVM>4"),

        #("6plusj", "numJets>=6"),
        #("sl_jge6_t2", sl_cuts + " && numJets>=6 && nBCSVM==2"),
        #("sl_jge6_t3", sl_cuts + " && numJets>=6 && nBCSVM==3"),
        #("6plusj4t", "numJets>=6 && nBCSVM==4"),
        ("sl_jge6_tge4", sl_cuts + " && numJets>=6 && nBCSVM>=4", "mem_d_nomatch_0"),
        #("6plusjH", "numJets>=6 && nBCSVM>4"),
    ]

    # Subset of categories we want to use for limit setting
    analysis_categories = [
        "sl_jge6_tge4"
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
            ("CMS_ttH_CSVLFUp",         "bTagWeight_LFUp"),
            ("CMS_ttH_CSVLFDown",       "bTagWeight_LFDown"),
            ("CMS_ttH_CSVHFUp",         "bTagWeight_HFUp"),
            ("CMS_ttH_CSVHFDown",       "bTagWeight_HFDown"),
            ("CMS_ttH_CSVStats1Up",     "bTagWeight_Stats1Up"),
            ("CMS_ttH_CSVStats1Down",   "bTagWeight_Stats1Down"),
            ("CMS_ttH_CSVStats2Up",     "bTagWeight_Stats2Up"),
            ("CMS_ttH_CSVStats2Down",   "bTagWeight_Stats2Down"),
    ]

    # Subset of the reweighted distributions we want to use as syst. shape uncertainties
    shape_uncertainties = [
    ]
    
    # nested dictionaries:

    # value: normalization uncertainty
    scale_uncertainties = {
        "sl_jge6_tge4" : {
            "ttH_hbb" : {
                "lumi" : 1.05
            },
            "ttbarPlus2B" : {
                "bgnorm_ttbarPlus2B" : 1.5
            },
            "ttbarPlusB" : {
                "bgnorm_ttbarPlusB" : 1.3
            },
            "ttbarPlusBBbar" : {
                "bgnorm_ttbarPlusBBbar" : 1.3
            },
            "ttbarPlusCCbar" : {
                "bgnorm_ttbarPlusCCbar" : 1.3
            },
            "ttbarOther" : {
                "bgnorm_ttbarOther" : 1.3
            },
    }}


    #Enable the plotting of these samples
    # !!!Important: Signal has to be the first one!!!!
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

    output_filename = "ControlPlots.root"
    output_datacardname = "shapes.txt"

    output_basepath = "/shome/gregor/VHBB-745/CMSSW_7_4_5/src/tthbb13/Plotting/python/joosep/"

    # luminosity we're interested in (measure in pb-1)
    lumi = 10000. # 10fb-1
