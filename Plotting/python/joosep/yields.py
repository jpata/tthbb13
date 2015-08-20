import ROOT
ROOT.gROOT.SetBatch(True)
import sys, os
import numpy as np

basecut = "passPV && "
categories = [
    ("sl", basecut + "is_sl"),
    ("sl_4j_3t", basecut + "is_sl && numJets==4 && nBCSVM==3")
]

if __name__ == "__main__":
    for fi in sys.argv[1:]:
        tf = ROOT.TFile(fi)
        tt = tf.Get("tree")
        l = [
            int(tt.GetEntries()),
        ]
        for cn, cat in categories:
            l += [int(tt.GetEntries(cat))]
        print fi, l
