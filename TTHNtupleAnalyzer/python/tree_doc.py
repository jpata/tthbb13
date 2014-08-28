import ROOT, sys, re
tf = ROOT.TFile(sys.argv[1])
tt = tf.Get("tthNtupleAnalyzer/events")
brs = sorted([b for b in tt.GetListOfBranches()])

#for br in brs:
#    bn = br.GetName()
#    ls = br.GetListOfLeaves()
#    print "| %s | %s | | |" % (bn, ls[0].GetTypeName())

print tt.GetEntries()
