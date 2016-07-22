import ROOT
import sys
from TTH.MEAnalysis.samples_base import getSitePrefix

ofname = sys.argv[1]
tt = ROOT.TChain("vhbb/tree")
for fi in sys.argv[2:]:
    print "adding", fi
    tt.AddFile(getSitePrefix(fi))

tt.SetBranchStatus("*", False)
tt.SetBranchStatus("GenBQuarkFromH*", True)
tt.SetBranchStatus("GenBQuarkFromTop*", True)
tt.SetBranchStatus("GenGluon*", True)
tt.SetBranchStatus("GenHiggsBoson*", True)
tt.SetBranchStatus("GenJet*", True)
tt.SetBranchStatus("Jet*", True)
tt.SetBranchStatus("aLeptons*", True)
tt.SetBranchStatus("GenLep*", True)
tt.SetBranchStatus("GenLepFromTop*", True)
tt.SetBranchStatus("GenNuFromTop*", True)
tt.SetBranchStatus("GenTop*", True)
tt.SetBranchStatus("GenWZQuark*", True)
tt.SetBranchStatus("GenStatus2bHad*", True)
tt.SetBranchStatus("ttCls*", True)

of = ROOT.TFile(ofname, "RECREATE")
of.cd()
tt.CopyTree("1")
of.Write()
of.Close()
