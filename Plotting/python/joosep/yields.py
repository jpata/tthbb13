import ROOT
ROOT.gROOT.SetBatch(True)
#ROOT.TH1.AddDirectory(False)

from collections import OrderedDict
import sys, os
import numpy as np

lumi = 10000

#select gen-level SL+DL events
basecut = "passPV && cat_gen<=1"
basecut_sl = basecut + " && (HLT_BIT_HLT_Ele27_eta2p1_WP85_Gsf_HT200_v || HLT_BIT_HLT_IsoMu24_eta2p1_v)&& is_sl"

categories = [
    ("sl", basecut_sl + "&& 1"),
    ("sl_j4_t2", basecut_sl + " && numJets==4 && nBCSVM==2"),
    ("sl_j4_t3", basecut_sl + " && numJets==4 && nBCSVM==3"),

    ("sl_j5_t2", basecut_sl + " && numJets==5 && nBCSVM==2"),
    ("sl_j5_t3", basecut_sl + " && numJets==5 && nBCSVM==3"),
    ("sl_j5_tge4", basecut_sl + " && numJets==5 && nBCSVM>=4"),

    ("sl_jge6_t2", basecut_sl + " && numJets>=6 && nBCSVM==2"),
    ("sl_jge6_t3", basecut_sl + " && numJets>=6 && nBCSVM==3"),
    ("sl_jge6_tge4", basecut_sl + " && numJets>=6 && nBCSVM>=4"),

    ("sl_jge7_t2", basecut_sl + " && numJets>=7 && nBCSVM==2"),
    ("sl_jge7_t3", basecut_sl + " && numJets>=7 && nBCSVM==3"),
    ("sl_jge7_tge4", basecut_sl + " && numJets>=7 && nBCSVM>=4"),
]

def getYield(tree, cut, lumi):
    ROOT.gROOT.cd()
    tree.Draw("jets_pt[0]>>h(100,0,10000)", "{0} * weight_xs * ({1})".format(lumi, cut), "goff")
    h = ROOT.gROOT.Get("h")
    w = h.Integral()
    return w

matchstrings = OrderedDict()

matchstrings["tb"] = "nMatch_tb>=2"
matchstrings["tb_btag"] = "nMatch_tb_btag>=2"

matchstrings["hb"] = "nMatch_hb>=2"
matchstrings["hb_btag"] = "nMatch_hb_btag>=2"

matchstrings["wq"] = "nMatch_wq>=2"
matchstrings["wq_btag"] = "nMatch_wq_btag>=2"

matchstrings["tb_wq"] = "nMatch_tb>=2 && nMatch_wq>=2"
matchstrings["tb_wq_btag"] = "nMatch_tb_btag>=2 && nMatch_wq_btag>=2"

matchstrings["tb_hb"] = "nMatch_tb>=2 && nMatch_hb>=2"
matchstrings["tb_hb_btag"] = "nMatch_tb_btag>=2 && nMatch_hb_btag>=2"

matchstrings["tb_wq_hb"] = "nMatch_tb>=2 && nMatch_wq>=2 && nMatch_hb>=2"
matchstrings["tb_wq_hb_btag"] = "nMatch_tb_btag>=2 && nMatch_wq_btag>=2 && nMatch_hb_btag>=2"

if __name__ == "__main__":
    for fi in sys.argv[1:]:
        tf = ROOT.TFile(fi)
        tt = tf.Get("tree")
        entries = [
            int(tt.GetEntries()),
        ]
        yields = [
            getYield(tt, "1", lumi)
        ]
        matches = matchstrings.keys()
        yields_matched = {
            k: [getYield(tt, matchstrings[k], lumi)] for k in matches
        }
    
        print "cat | N | total | " + " | ".join(matches)

        for cn, cat in categories:
            entries += [int(tt.GetEntries(cat))]
            yields += [getYield(tt, cat, lumi)]
            for k in matches:
                yields_matched[k] += [getYield(tt, cat + "&&" + matchstrings[k], lumi)]
            matchstr = " | ".join(["{0:.2f}".format(yields_matched[k][-1]) for k in matches])
            print "{0} | {1} | {2:.2f} | {3}".format(cn, entries[-1], yields[-1], matchstr)
