from __future__ import print_function
import ROOT, sys

ngen = 0
for f in sys.argv[1:]:
    tf = ROOT.TFile(f)
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
print(ngen)
