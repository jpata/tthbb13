import sys
import ROOT
ROOT.gROOT.SetBatch(True)
from collections import OrderedDict

def get_yield(file, cut):
    fi = ROOT.TFile(file)
    tt = fi.Get("tree")
    N1 = float(tt.GetEntries(cut)) / tt.GetEntries() 
    tt.Draw("is_sl[0] >> h", "(1) * ({0})".format(cut))
    N2 = fi.Get("h").Integral()
    fi.Close()
    return N1, N2

cuts = OrderedDict()
cuts["sl_jge6_t2"] = "is_sl && numJets>=6 && nBCSVM==2"
cuts["sl_jge6_t3"] = "is_sl && numJets>=6 && nBCSVM==3"
cuts["sl_jge6_tge4"] = "is_sl && numJets>=6 && nBCSVM>=4"

files = OrderedDict()
files["ttH_hbb"] = "/Users/joosep/Documents/tth/data/ntp/VHBBHeppyV20_tthbbV3/ttHTobb_M125_13TeV_powheg_pythia8.root"

files_old = OrderedDict()
files_old["ttH_hbb"] = "/Users/joosep/Documents/tth/data/ntp/Jan18/tth.root"


print "files"
for nick, fi in files.items():
    print nick
    for cutname, cut in cuts.items():
        print cutname, get_yield(fi, cut)

print "files_old"
for nick, fi in files_old.items():
    print nick
    for cutname, cut in cuts.items():
        print cutname, get_yield(fi, cut)
