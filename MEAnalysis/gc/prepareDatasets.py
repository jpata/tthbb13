from __future__ import print_function
from TTH.MEAnalysis.samples_v1 import lfn_to_pfn
import sys, imp
import ROOT

samplefile = sys.argv[1]
samplefile = imp.load_source("samplefile", samplefile)
from samplefile import samples_dict

for sample_name, sample in samples_dict.items():
    ngen = 0
    files = sample.subFiles
    print("[{0}]".format(sample_name))
    for f in files:
        tf = ROOT.TFile(lfn_to_pfn(f))
        if (tf != None):
            tt = tf.Get("tree")
            if (tt != None):
                print("{0} = {1}".format(f, int(tt.GetEntries())))
            else:
                print("could not read tree", file=sys.stderr)
                continue
            hc = tf.Get("Count")
            ngen += hc.GetBinContent(1)
        else:
            print("could not read file {0}".format(f), file=sys.stderr)
    print(sample_name, ngen)
