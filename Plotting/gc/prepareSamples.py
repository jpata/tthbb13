import os, glob
import ROOT

import fnmatch
import os


base = "/hdfs/local/joosep/tth/Feb11_jec_74x_moriond/"
for sample, files in [
    ("ttH_hbb", [base + "ttHTobb_M125_13TeV_powheg_pythia8.root"]),
    #("ttH_nonhbb", [base + "ttHToNonbb_M125_13TeV_powheg_pythia8.root"]),
    ("ttbarPlusBBbar", [base + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000_ttbb.root"]),
    ("ttbarPlusCCbar", [base + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000_ttcc.root"]),
    ("ttbarPlusB", [base + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000_ttb.root"]),
    ("ttbarPlus2B", [base + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000_tt2b.root"]),
    ("ttbarOther", [base + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000_ttll.root"]),
    #("ttW_Wlnu", [base + "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.root"]),
    #("ttW_Wqq", [base + "TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.root"]),
    #("ttZ_Zqq", [base + "TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8.root"]),
    #("wjets", [base + "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root"]),
    #("ww", [base + "WW_TuneCUETP8M1_13TeV-pythia8.root"]),
    #("wz", [base + "WZ_TuneCUETP8M1_13TeV-pythia8.root"]),
    #("zz", [base + "ZZ_TuneCUETP8M1_13TeV-pythia8.root"]),
    #("stop_t", [base + "ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.root"]),
    #("stop_tbar", [base + "ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.root"]),
    #("stop_tW", [base + "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.root"]),
    #("stop_tbarW", [base + "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.root"]),
    #("stop_s", [base + "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.root"]),
    #("SingleMuon", [base + "SingleMuon.root"]),
    #("SingleElectron", [base + "SingleElectron.root"]),
    #("DoubleMuon", [base + "DoubleMuon.root"]),
    #("DoubleEG", [base + "DoubleEG.root"]),
    #("MuonEG", [base + "MuonEG.root"]),
    ]:

    #files = []
    #for root, dirnames, filenames in os.walk(basepath):
    #    for filename in fnmatch.filter(filenames, '*.root'):
    #        files.append(os.path.join(root, filename))
    
    print "[{0}]".format(sample)
    for fi in files:
        tf = ROOT.TFile(fi)
        n = tf.Get("tree").GetEntries()
        print "{0} = {1}".format(fi, n)
        tf.Close()
