#!/usr/bin/env python
import sys
import ROOT
from collections import OrderedDict
import sparse
import plotlib

cuts = OrderedDict()
#cuts["sl_jge6_t2"] = "is_sl && numJets>=6 && nBCSVM==2"
cuts["sl_jge6_t3"] = "is_sl && numJets>=6 && nBCSVM==3"
cuts["sl_jge6_tge4"] = "is_sl && numJets>=6 && nBCSVM>=4"

files = OrderedDict()
files["ttH_hbb"] = "/hdfs/local/joosep/tth/Feb11_jec_74x_moriond/ttHTobb_M125_13TeV_powheg_pythia8.root"
files["ttbar"] = "/hdfs/local/joosep/tth/Feb11_jec_74x_moriond/TT_TuneCUETP8M1_13TeV-powheg-pythia8.root"

if __name__ == "__main__":
    outd = {}
    for nick, fi in files.items():
        print nick
        for cutname, cut in cuts.items():
            h = plotlib.process_sample_hist(
                [fi],
                "{0}_{1}_mem_SL_0w2h2t".format(nick, cutname),
                "mem_tth_p[0]/(mem_tth_p[0] + 0.15 * mem_ttbb_p[0])",
                [100, 0, 1],
                cut
            )
            outd["{0}/{1}/mem_SL_0w2h2t".format(nick, cutname)] = h
            
            h2 = plotlib.process_sample_hist(
                [fi],
                "{0}_{1}_mem_SL_2w2h2t".format(nick, cutname),
                "mem_tth_p[5]/(mem_tth_p[5] + 0.15 * mem_ttbb_p[5])",
                [100, 0, 1],
                cut
            )
            outd["{0}/{1}/mem_SL_2w2h2t".format(nick, cutname)] = h2
            
            #h3 = plotlib.process_sample_hist(
            #    [fi],
            #    "{0}_{1}_mem_SL_0w2h2t_match".format(nick, cutname),
            #    "mem_tth_p[0]/(mem_tth_p[0] + 0.15 * mem_ttbb_p[0])",
            #    [100, 0, 1],
            #    cut + " && nMatch_wq_btag==2 && nMatch_hb_btag==2 && nMatch_tb_btag==2"
            #)
            #outd["{0}/{1}/mem_SL_0w2h2t".format(nick, cutname)] = h2
    sparse.save_hdict("mem_control.root", outd)
