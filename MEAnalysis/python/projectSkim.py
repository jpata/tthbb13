import ROOT
import sys
from TTH.MEAnalysis.samples_base import getSitePrefix

ofname = sys.argv[1]
tt = ROOT.TChain("tree")
for fi in sys.argv[2:]:
    print "adding", fi
    tt.AddFile(getSitePrefix(fi))

tt.SetBranchStatus("*", False)
tt.SetBranchStatus("mem_tt*", True)
tt.SetBranchStatus("nMatch*", True)
tt.SetBranchStatus("is_sl", True)
tt.SetBranchStatus("is_dl", True)
tt.SetBranchStatus("numJets", True)
tt.SetBranchStatus("nBCSVM", True)
tt.SetBranchStatus("common_bdt", True)
tt.SetBranchStatus("btag_LR_4b_2b", True)
tt.SetBranchStatus("ttCls", True)
tt.SetBranchStatus("run", True)
tt.SetBranchStatus("lumi", True)
tt.SetBranchStatus("evt", True)
#tt.SetBranchStatus("weight_xs", True)

of = ROOT.TFile(ofname, "RECREATE")
of.cd()
tt.CopyTree("(is_sl && ((numJets>=6 && nBCSVM>=2) || (numJets>=4 && nBCSVM>=3))) || (is_dl && (numJets>=3 && nBCSVM >=3))")
of.Write()
of.Close()
