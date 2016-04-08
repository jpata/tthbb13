import ROOT, sys

d = {}
for fn in sys.argv[1:]:
    f = ROOT.TFile(fn)
    
    h = f.Get("Count")
    d[fn.split("/")[-1].split(".")[0]] = h.GetBinContent(1)
print d
