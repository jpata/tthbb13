import ROOT, sys

tf = ROOT.TFile(sys.argv[1])

for k in tf.GetListOfKeys():
	print k.GetName()
