import ROOT
import sys
from TTH.MEAnalysis.samples_base import getSitePrefix

filenames = sys.argv[2:]
filenames = map(getSitePrefix, filenames)

ofname = sys.argv[1]
of = ROOT.TFile(ofname, "RECREATE")

def get_tree_entries(treename, filenames):
    tt = ROOT.TChain(treename)
    for fi in filenames:
        print "adding", fi
        tt.AddFile(fi)
    i = tt.GetEntries()
    return i

good_filenames = []
for infn in filenames:
    tf = ROOT.TFile.Open(infn)
    if not tf or tf.IsZombie():
        print "Could not open {0}, skipping".format(infn)
        continue
    print "good file", infn, tf
    good_filenames += [infn]
    vhbb_dir = tf.Get("vhbb")
    for k in vhbb_dir.GetListOfKeys():
        kn = k.GetName() 
        if "Count" in kn:
            o = k.ReadObj()
            print "Entries", kn, o.GetBinContent(1)
            if not of.Get(kn):
                print "first file, creating histogram", kn
                o2 = o.Clone()
                of.Add(o2)
            else:
                of.Get(kn).Add(o)
    of.Write()
    tf.Close()

#hEntries = ROOT.TH1D("numEntries", "numEntries", 3, 0, 3)
#hEntries.SetDirectory(of)
#hEntries.SetBinContent(1, get_tree_entries("vhbb/tree", good_filenames))
#hEntries.SetBinContent(2, get_tree_entries("tree", good_filenames))
#hEntries.Write()

of.Close()
