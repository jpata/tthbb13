import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError
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

samples = [
    "tth_13TeV_phys14",
    "ttjets_13TeV_phys14",
    "ttjets_13TeV_phys14_bb", "ttjets_13TeV_phys14_b",
    "ttjets_13TeV_phys14_cc", "ttjets_13TeV_phys14_ll"
]

of = ROOT.TFile("ControlPlots.root", "RECREATE")

#Number of parallel processes to run for the histogram projection
ncores = 20

def weight_str(cut):
    return "genWeight * ({0})".format(cut)

def drawHelper(args):
    tf, hist, cut, nfirst, nev = args
    #print hist, cut, nfirst, nev
    hname = hist.split(">>")[1].split("(")[0].strip()
    ROOT.gROOT.cd()
    ROOT.TH1.SetDefaultSumw2(True)
    if isinstance(cut, str):
        n = tf.Draw(hist, weight_str(cut), "goff", nev, nfirst)
    elif isinstance(cut, ROOT.TEntryList):
        tf.SetEntryList(cut)
        n = tf.Draw(hist, weight_str("1"), "goff", nev, nfirst)
        tf.SetEntryList(0)
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
        #how many events to process per core
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
        print of.GetPath(), h.GetName(), h.GetEntries(), h.Integral()
        return h


for sample in samples:
    print sample
    tf = ROOT.TChain("tree")
    for fn in samples_dict[sample].fileNamesS2:
        tf.AddFile(fn)
    print tf.GetEntries()

    weight = "genWeight"
    of.cd()
    d = of.mkdir(sample)
    d.cd()
    Draw(tf, d, "is_sl >> nsl(2,0,2)", "1")
    Draw(tf, d, "is_dl >> ndl(2,0,2)", "1")

    for lep, lepcut in [("sl", "(is_sl==1)"), ("dl", "(is_dl==1)")]:
        d.cd()
        lepd = d.mkdir(lep)
        lepd.cd()
        #Draw(tf, lepd, "leps_pt[0] >> lep0_pt(30,0,300)", lepcut)
        #Draw(tf, lepd, "leps_eta[0] >> lep0_eta(30,-5,5)", lepcut)

        #Draw(tf, lepd, "leps_pt[1] >> lep1_pt(30,0,300)", lepcut)
        #Draw(tf, lepd, "leps_eta[1] >> lep1_eta(30,-5,5)", lepcut)

        #Draw(tf, lepd, "njets >> njets(15,0,15)", lepcut)
        #Draw(tf, lepd, "nBCSVM >> ntags(15,0,15)", lepcut)

        #Draw(tf, lepd, "nBCSVM:njets >> njets_nBCSVM(15,0,15,15,0,15)", lepcut)

        Draw(tf, lepd, "jets_pt[0] >> jet0_pt(30,0,600)", lepcut)
        #Draw(tf, lepd, "jets_eta[0] >> jet0_eta(30,-5,5)", lepcut)

        #Draw(tf, lepd, "jets_pt[1] >> jet1_pt(30,0,600)", lepcut)
        #Draw(tf, lepd, "jets_eta[1] >> jet1_eta(30,-5,5)", lepcut)
        Draw(tf, lepd, "(100*nMatch_wq + 10*nMatch_hb + nMatch_tb) >> nMatch(300,0,300)", lepcut)
        Draw(tf, lepd, "(100*nMatch_wq_btag + 10*nMatch_hb_btag + nMatch_tb_btag) >> nMatch_btag(300,0,300)", lepcut)
        for jet_tag, jettagcut in [
                ("cat1H", "cat==1 && cat_btag==1"),
                ("cat2H", "cat==2 && cat_btag==1"),
                ("cat3H", "cat==3 && cat_btag==1"),

                ("cat6Hee", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==22 && cat==6 && cat_btag==1"),
                ("cat6Hem", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==24 && cat==6 && cat_btag==1"),
                ("cat6Hmm", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==26 && cat==6 && cat_btag==1"),

                #("cat1L", "cat==1 && cat_btag==0"),
                #("cat2L", "cat==2 && cat_btag==0"),
                #("cat3L", "cat==3 && cat_btag==0"),

                #("cat6Lee", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==22 && cat==6 && cat_btag==0"),
                #("cat6Lem", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==24 && cat==6 && cat_btag==0"),
                #("cat6Lmm", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==26 && cat==6 && cat_btag==0"),

                ("4j", "njets==4"),
                ("4j3t", "njets==4 && nBCSVM==3"),
                ("4j4t", "njets==4 && nBCSVM==4"),

                ("5j", "njets==5"),
                ("5jL", "njets==5 && nBCSVM<3"),
                ("5j3t", "njets==5 && nBCSVM==3"),
                ("5j4t", "njets==5 && nBCSVM==4"),
                ("5j4plust", "njets==5 && nBCSVM>=4"),
                ("5jH", "njets==5 && nBCSVM>4"),

                ("6j", "njets==6"),
                ("6jL", "njets==6 && nBCSVM<3"),
                ("6j3t", "njets==6 && nBCSVM==3"),
                ("6j4t", "njets==6 && nBCSVM==4"),
                ("6jH", "njets==6 && nBCSVM>4"),

                ("6plusj", "njets>=6"),
                ("6plusj2t", "njets>=6 && nBCSVM==2"),
                ("6plusj3t", "njets>=6 && nBCSVM==3"),
                ("6plusj4t", "njets>=6 && nBCSVM==4"),
                ("6plusj4plust", "njets>=6 && nBCSVM>=4"),
                ("6plusjH", "njets>=6 && nBCSVM>4"),

                ("7j", "njets==7"),
                ("7jL", "njets==7 && nBCSVM<3"),
                ("7j3t", "njets==7 && nBCSVM==3"),
                ("7j4t", "njets==7 && nBCSVM==4"),
                ("7jH", "njets==7 && nBCSVM>4"),

                ("8plusj", "njets>=8"),
                ("8plusjL", "njets>=8 && nBCSVM<3"),
                ("8plusj3t", "njets>=8 && nBCSVM==3"),
                ("8plusj4t", "njets>=8 && nBCSVM==4"),
                ("8plusjH", "njets>=8 && nBCSVM>4"),
            ]:

            if lep == "sl" and "cat6" in jet_tag:
                continue
            if lep == "dl" and (
                "cat1" in jet_tag or
                "cat2" in jet_tag or
                "cat3" in jet_tag
            ):
                continue
            lepjetcut = " && ".join([lepcut, jettagcut])
            if tf.GetEntries(lepjetcut)==0:
                continue
            ROOT.gROOT.cd()
            tf.Draw(">>elist", lepjetcut, "entrylist")
            elist = ROOT.gROOT.Get("elist")

            lepd.cd()
            jetd = lepd.mkdir(jet_tag)
            jetd.cd()

            #Draw(tf, jetd, "nBCSVM:njets >> njets_nBCSVM(15,0,15,15,0,15)", lepjetcut)
            #Draw(tf, jetd, "nMatchSimB:nMatchSimC >> nMatchSimB_nMatchSimC(6,0,6,6,0,6)", lepjetcut)

            Draw(tf, jetd, "jets_pt[0] >> jet0_pt(30,0,600)", elist)
            #Draw(tf, jetd, "jets_eta[0] >> jet0_eta(30,-5,5)", lepjetcut)

            #Draw(tf, jetd, "leps_pt[0] >> lep0_pt(30,0,300)", lepjetcut)
            #Draw(tf, jetd, "leps_eta[0] >> lep0_eta(30,-5,5)", lepjetcut)

            #Draw(tf, jetd, "btag_LR_4b_2b >> btag_lr(30,0,1)", lepjetcut)

            Draw(tf, jetd, "(100*nMatch_wq + 10*nMatch_hb + nMatch_tb) >> nMatch(300,0,300)", elist)
            Draw(tf, jetd, "(100*nMatch_wq_btag + 10*nMatch_hb_btag + nMatch_tb_btag) >> nMatch_btag(300,0,300)", elist)

            for match, matchcut in [
                    ("nomatch", "1"),
                    ("tb2_wq2", "nMatch_wq_btag==2 && nMatch_tb_btag==2"),
                    ("hb2_tb2_wq2", "nMatch_hb_btag==2 && nMatch_wq_btag==2 && nMatch_tb_btag==2"),
                    ("tb2_wq1", "nMatch_wq_btag==1 && nMatch_tb_btag==2"),
                    ("hb2_tb2_wq1", "nMatch_hb_btag==2 && nMatch_wq_btag==1 && nMatch_tb_btag==2")
                ]:
                if "hb2" in match and "ttjets" in sample:
                    continue
                cut = " && ".join([lepcut, jettagcut, matchcut])
                if tf.GetEntries(cut) == 0:
                    continue
                for nmem in range(3):
                    Draw(tf, jetd,
                        "mem_tth_p[{0}] / (mem_tth_p[{0}] + 0.15*mem_ttbb_p[{0}]) >> mem_d_{1}_{0}(20,0,1)".format(nmem, match),
                        cut
                    )


of.Write()
of.Close()

