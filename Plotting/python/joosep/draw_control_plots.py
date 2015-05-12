import ROOT
ROOT.gROOT.SetBatch(True)
import sys, os
#sys.path += ["./heplot/"]
#import heplot.heplot as he
#from rootpy.plotting import Hist, Hist2D
#import matplotlib.pyplot as plt
import random
#import matplotlib
#from rootpy import asrootpy
#from matplotlib.ticker import NullLocator, LinearLocator, MultipleLocator, FormatStrFormatter, AutoMinorLocator
import numpy as np

from TTH.Plotting.joosep.samples import samples_dict

samples = ["tth_13TeV_phys14", "ttjets_13TeV_phys14"]

of = ROOT.TFile("ControlPlots.root", "RECREATE")
for sample in samples:
    print sample
    tf = ROOT.TChain("tree")
    for fn in samples_dict[sample].fileNamesS2:
        tf.AddFile(fn)

    of.cd()
    d = of.mkdir(sample)
    d.cd()
    tf.Draw("is_sl >> sl(2,0,2)")
    tf.Draw("is_dl >> dl(2,0,2)")

    for lep, lepcut in [("sl", "is_sl==1"), ("dl", "is_dl==1")]:
        d.cd()
        lepd = d.mkdir(lep)
        lepd.cd()
        tf.Draw("leps_pt[0] >> lep0_pt(30,0,300)", lepcut)
        tf.Draw("leps_eta[0] >> lep0_eta(30,-5,5)", lepcut)

        tf.Draw("leps_pt[1] >> lep1_pt(30,0,300)", lepcut)
        tf.Draw("leps_eta[1] >> lep1_eta(30,-5,5)", lepcut)

        tf.Draw("njets >> njets(15,0,15)", lepcut)
        tf.Draw("nBCSVM >> ntags(15,0,15)", lepcut)

        tf.Draw("jets_pt[0] >> jet0_pt(30,0,600)", lepcut)
        tf.Draw("jets_eta[0] >> jet0_eta(30,-5,5)", lepcut)

        tf.Draw("jets_pt[1] >> jet1_pt(30,0,600)", lepcut)
        tf.Draw("jets_eta[1] >> jet1_eta(30,-5,5)", lepcut)
        for jet_tag, jettagcut in [
                ("6j", "njets==6"),
                ("6j3t", "njets==6 && nBCSVM==3"),
                ("6j4t", "njets==6 && nBCSVM==4"),
                ("5j", "njets==5"),
                ("5j3t", "njets==5 && nBCSVM==3"),
                ("5j4t", "njets==5 && nBCSVM==4"),
            ]:
            lepd.cd()
            jetd = lepd.mkdir(jet_tag)
            jetd.cd()
            tf.Draw("btag_LR_4b_2b >> btag_lr(30,0,1)", " && ".join([lepcut, jettagcut]))

            tf.Draw("nMatch_wq_btag >> nMatch_wq_btag(4,0,4)", " && ".join([lepcut, jettagcut]))
            tf.Draw("nMatch_hb_btag >> nMatch_hb_btag(4,0,4)", " && ".join([lepcut, jettagcut]))
            tf.Draw("nMatch_tb_btag >> nMatch_tb_btag(4,0,4)", " && ".join([lepcut, jettagcut]))

            for match, matchcut in [
                    ("nomatch", "1"),
                    ("tb2_wq2", "nMatch_wq_btag==2 && nMatch_tb_btag==2"),
                    ("hb2_tb2_wq2", "nMatch_hb_btag==2 && nMatch_wq_btag==2 && nMatch_tb_btag==2")
                ]:
                for nmem in [0, 1, 2, 3, 4, 5]:
                    tf.Draw("mem_tth_p[{0}] / (mem_tth_p[{0}] + 0.02*mem_ttbb_p[{0}]) >> mem_d_{1}_{0}(20,0,1)".format(nmem, match),
                        " && ".join([lepcut, jettagcut, matchcut])
                    )


    of.Write()
of.Close()

