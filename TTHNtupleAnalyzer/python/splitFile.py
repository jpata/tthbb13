import ROOT, sys, re
import os
tf = ROOT.TFile.Open(sys.argv[1])
ofdir = sys.argv[2]

if not os.path.exists(ofdir):
    print "creating output dir", ofdir
    os.makedirs(ofdir)

Nblock = 10000
tt = tf.Get("tthNtupleAnalyzer/events")
n = tt.GetEntries()


nblock = 0
for first in range(0, n, Nblock):
    print "copying ", first, first+Nblock
    of = ROOT.TFile(ofdir + "/block_{0}.root".format(nblock), "RECREATE")
    if of==None or not of or of.IsZombie():
        break
    of.cd()
    copy = tt.CopyTree("", "", Nblock, first)
    copy.SetDirectory(of)
    copy.Write()
    of.Close()
    nblock += 1
