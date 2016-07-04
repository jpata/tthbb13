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
tt.SetBranchStatus("is_*", True)
tt.SetBranchStatus("numJets*", True)
tt.SetBranchStatus("nB*", True)
tt.SetBranchStatus("n_*", True)
tt.SetBranchStatus("topCand*", True)
tt.SetBranchStatus("btag_LR_4b_2b*", True)
tt.SetBranchStatus("ttCls", True)
tt.SetBranchStatus("run", True)
tt.SetBranchStatus("lumi", True)
tt.SetBranchStatus("evt", True)
tt.SetBranchStatus("cat", True)
tt.SetBranchStatus("ht", True)
tt.SetBranchStatus("isotropy", True)
tt.SetBranchStatus("sphericity", True)
tt.SetBranchStatus("C", True)
tt.SetBranchStatus("D", True)
tt.SetBranchStatus("aplanarity", True)
tt.SetBranchStatus("jets_*", True)
tt.SetBranchStatus("bTagWeight*", True)
tt.SetBranchStatus("puWeight*", True)
tt.SetBranchStatus("HLT*", True)
tt.SetBranchStatus("common*", True)
tt.SetBranchStatus("mean*", True)
tt.SetBranchStatus("std*", True)
tt.SetBranchStatus("momentum*", True)
#tt.SetBranchStatus("weight_xs", True)

of = ROOT.TFile(ofname, "RECREATE")
of.cd()
tt.CopyTree("(is_sl && ((numJets>=6 && nBCSVM>=2) || (numJets>=4 && nBCSVM>=3) || (numJets==5 && nBCSVM>=2))) || (is_dl && (numJets>=3 && nBCSVM >=2)) || (is_fh && (numJets>=4 && nBCSVM>=3))")
of.Write()
of.Close()
