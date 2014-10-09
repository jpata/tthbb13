import ROOT, sys


f = ROOT.TFile(sys.argv[1])
t = f.Get("tthNtupleAnalyzer/events")

i = 0
for ev in t:
    print ev.event__id, ev.event__run, ev.event__lumi
    i += 1
    if i>100:
        break
