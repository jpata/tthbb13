import ROOT, sys

for fn in sys.argv[1:]:
    f = ROOT.TFile(fn)
    
    h = f.Get("Count")
    print fn, h.GetBinContent(1)
