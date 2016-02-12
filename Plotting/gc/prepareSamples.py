import os, glob
import ROOT

import fnmatch
import os


base = "/hdfs/local/joosep/tth/Feb11_jec_74x_moriond/"
for sample, files in [
    ("ttH_hbb", [
        base + "ttHTobb_M125_13TeV_powheg_pythia8.root"
    ]),
    ("ttH_nonhbb", [
        base + "ttHToNonbb_M125_13TeV_powheg_pythia8.root"
    ]),
    ("ttbarPlusBBbar", [
        base + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000_ttbb.root"
    ]),
    ("ttbarPlusCCbar", [
        base + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000_ttcc.root"
    ]),
    ("ttbarPlusB", [
        base + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000_ttb.root"
    ]),
    ("ttbarPlus2B", [
        base + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000_tt2b.root"
    ]),
    ("ttbarOther", [
        base + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000_ttll.root"
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
