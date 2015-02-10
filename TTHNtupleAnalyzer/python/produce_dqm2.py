#!/usr/bin/env python
import ROOT, sys

f = ROOT.TFile(sys.argv[1])

tree = f.Get("tthNtupleAnalyzer/events")

if not tree or tree.IsZombie():
    raise Exception("could not open ttree tthNtupleAnalyzer/events")

of = ROOT.TFile(sys.argv[2], "RECREATE")
of.cd()

brs = sorted([b.GetName() for b in tree.GetListOfBranches()])

for br in brs:
	h, l = tree.GetMaximum(br), tree.GetMinimum(br)
	tree.Draw("%s >> h_%s" % (br, br), "%s > -9999" % br)
	hi = of.Get("h_%s" % br)
	print br, h, l, hi.Integral(), hi.GetMean(), hi.GetRMS()
of.Write()
of.Close()
