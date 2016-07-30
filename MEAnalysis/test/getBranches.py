import ROOT, sys
from TTH.MEAnalysis.samples_base import getSitePrefix

tf = ROOT.TFile.Open(getSitePrefix(sys.argv[1]))
if not tf:
    raise Exception("Could not open file")
tt = tf.Get(sys.argv[2])

branches = sorted([br.GetName() for br in tt.GetListOfBranches()])
for br in branches:
    print br

