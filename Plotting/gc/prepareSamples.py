import os, glob
import ROOT

import fnmatch
import os


base = "/hdfs/local/joosep/tth/Feb11_jec_74x_moriond/"
base2 = "/hdfs/local/joosep/tth/Feb16_nome/"
for sample, files in [
    ("ttH_hbb", [
        base2 + "ttHTobb_M125_13TeV_powheg_pythia8.root"
    ]),
    ("ttH_nonhbb", [
        base2 + "ttHToNonbb_M125_13TeV_powheg_pythia8.root"
    ]),
    ("ttbarPlusBBbar", [
        base2 + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root"
    ]),
    ("ttbarPlusCCbar", [
        base2 + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root"
    ]),
    ("ttbarPlusB", [
        base2 + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root"
    ]),
    ("ttbarPlus2B", [
        base2 + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root"
    ]),
    ("ttbarOther", [
        base2 + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root"
    ]),
    ("SingleMuon", [
        base + "SingleMuon.root"
    ]),
    ("SingleElectron", [
        base + "SingleElectron.root"
    ]),
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
