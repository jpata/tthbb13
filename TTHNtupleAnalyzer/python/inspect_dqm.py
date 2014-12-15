#!/usr/bin/env python
import ROOT, sys

tf = ROOT.TFile(sys.argv[1])

kl = tf.GetListOfKeys()

for k in kl:
	o = k.ReadObj()

	print k.GetName(), o.GetMean(), o.GetRMS(), o.Integral(), o.GetBinContent(0), o.GetBinContent(o.GetNbinsX()+1)
