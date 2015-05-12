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

ncores = 1

def drawHelper(args):
    tf, hist, cut, nfirst, nev = args
    #print hist, cut, nfirst, nev
    hname = hist.split(">>")[1].split("(")[0].strip()
    ROOT.gROOT.cd()
    n = tf.Draw(hist, cut, "goff", nev, nfirst)
    h = ROOT.gROOT.Get(hname)
    assert(h.GetEntries() == n)
    return h

if ncores == 1:
    def Draw(tf, of, *args):
        return tf.Draw(*args)
else:
    import multiprocessing
    pool = multiprocessing.Pool(ncores)

    def Draw(tf, of, *args):
        ntot = tf.GetEntriesFast()
        #print tf, ntot
        chunksize = max(ntot/ncores, 100000)
        chunks = range(0, ntot, chunksize)
        parargs = []
        for ch in chunks:
            parargs += [tuple([tf] + list(args)+[ch, min(chunksize, ntot-ch)])]
        hlist = pool.map(drawHelper, parargs)
        h = hlist[0].Clone()
        for h_ in hlist[1:]:
            h.Add(h_)
        h.SetDirectory(of)
        of.Add(h, True)
        return h

for sample in samples:
    print sample
    tf = ROOT.TChain("tree")
    for fn in samples_dict[sample].fileNamesS2:
        tf.AddFile(fn)
    print tf.GetEntries()
    of.cd()
    d = of.mkdir(sample)
    d.cd()
    Draw(tf, d, "is_sl >> sl(2,0,2)", "1")
    Draw(tf, d, "is_dl >> dl(2,0,2)", "1")

    for lep, lepcut in [("sl", "is_sl==1"), ("dl", "is_dl==1")]:
        d.cd()
        lepd = d.mkdir(lep)
        lepd.cd()
        Draw(tf, lepd, "leps_pt[0] >> lep0_pt(30,0,300)", lepcut)
        Draw(tf, lepd, "leps_eta[0] >> lep0_eta(30,-5,5)", lepcut)

        Draw(tf, lepd, "leps_pt[1] >> lep1_pt(30,0,300)", lepcut)
        Draw(tf, lepd, "leps_eta[1] >> lep1_eta(30,-5,5)", lepcut)

        Draw(tf, lepd, "njets >> njets(15,0,15)", lepcut)
        Draw(tf, lepd, "nBCSVM >> ntags(15,0,15)", lepcut)

        Draw(tf, lepd, "jets_pt[0] >> jet0_pt(30,0,600)", lepcut)
        Draw(tf, lepd, "jets_eta[0] >> jet0_eta(30,-5,5)", lepcut)

        Draw(tf, lepd, "jets_pt[1] >> jet1_pt(30,0,600)", lepcut)
        Draw(tf, lepd, "jets_eta[1] >> jet1_eta(30,-5,5)", lepcut)
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
            Draw(tf, jetd, "btag_LR_4b_2b >> btag_lr(30,0,1)", " && ".join([lepcut, jettagcut]))

            Draw(tf, jetd, "nMatch_wq_btag >> nMatch_wq_btag(4,0,4)", " && ".join([lepcut, jettagcut]))
            Draw(tf, jetd, "nMatch_hb_btag >> nMatch_hb_btag(4,0,4)", " && ".join([lepcut, jettagcut]))
            Draw(tf, jetd, "nMatch_tb_btag >> nMatch_tb_btag(4,0,4)", " && ".join([lepcut, jettagcut]))

            for match, matchcut in [
                    ("nomatch", "1"),
                    ("tb2_wq2", "nMatch_wq_btag==2 && nMatch_tb_btag==2"),
                    ("hb2_tb2_wq2", "nMatch_hb_btag==2 && nMatch_wq_btag==2 && nMatch_tb_btag==2")
                ]:
                for nmem in [0, 1, 2, 3, 4, 5]:
                    Draw(tf, jetd, "mem_tth_p[{0}] / (mem_tth_p[{0}] + 0.02*mem_ttbb_p[{0}]) >> mem_d_{1}_{0}(20,0,1)".format(nmem, match),
                        " && ".join([lepcut, jettagcut, matchcut])
                    )


of.Write()
of.Close()

