#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError
import sys, os
import random
import numpy as np
import multiprocessing
import imp
import datetime

#Number of parallel processes to run for the histogram projection
#ncores = multiprocessing.cpu_count()
ncores = 4

samplepath = "/Users/joosep/Documents/tth/data/ntp/v14/small/"
samples = [
    "ttHTobb_M125_13TeV_powheg_pythia8.root",
    "ttHToNonbb_M125_13TeV_powheg_pythia8.root",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8.root", 
    "SingleMuon.root",
    #"SingleElectron.root"
    ]

def is_data(sample):
    if "Single" in sample:
        return True
    return False

def weight_str(cut, sample, weight=1.0, lumi=1000.0):
    w = 1.0
    if not is_data(sample):
        return "weight_xs * sign(genWeight) * {1} * {2} * {3} * ({0})".format(cut, weight, lumi, w)
    else:
        return cut

def drawHelper(args):
    """
    Simple draw command that projects out a histogram on a single core.
    Arguments are a tuple because that allows it to be used transparently in
    multiprocessing.

    args - tuple of (
        input ttree (TTree) - TTree with events to project
        hist command (string) - command for TTree::Draw in the for [func >> name(bins)]
        cut string (string) - cut string for the TTree::Draw method
        nfirst (int) - first event to process (index)
        nev (int) - how many indices to process
    )

    NB: the histogram is created in the !!global!! ROOT "memory directory"
    Returns: resulting histogram
    """
    tf, hist, cut, nfirst, nev = args
    #print hist, cut, nfirst, nev
    hname = hist.split(">>")[1].split("(")[0].strip()
    hfunc = hist.split(">>")[0]
    x = hist.split(">>")[1]
    hbins = x[x.find("(")+1:-1].split(",")
    ROOT.gROOT.cd()
    ROOT.TH1.SetDefaultSumw2(True)
    h = ROOT.TH1D(hname, hname, int(hbins[0]), float(hbins[1]), float(hbins[2]))
    n = tf.Draw(hfunc + ">>" + hname, cut, "goff", nev, nfirst)
    #h = ROOT.gROOT.Get(hname)
    assert(h.GetEntries() == n)
    return h

def Draw(tf, of, sample, *args):
    """
    tf (TFile): Input file
    of (TFile): output file
    args (list): (hist, cut)
        hist (string): TTree::Draw type command of the form "jet_pt >> h(10,0,100)"
        cut (string): cutstring for TTree::Draw
        OR
        cut (TEntryList): pre-determined entry list with the events passing the cut
    """
    hist = args[0]
    cut = args[1]
    cut = weight_str(cut, sample)
    hname = hist.split(">>")[1].split("(")[0].strip()
    hbins = hist.split(">>")[1].split("(")[1].strip()
    hfunc = hist.split(">>")[0]
    
    ROOT.gROOT.cd()
    
    if isinstance(cut, ROOT.TEntryList):
        tf.SetEntryList(cut)
    
    cuts = cut
    if isinstance(cut, ROOT.TEntryList):
        cuts = "1.0"
            
    ntot = tf.GetEntriesFast()

    #how many events to process per core
    chunksize = max(ntot/ncores, 50000)
    chunks = range(0, ntot, chunksize)
    #print args, len(chunks)
    
    npool = min(ncores, len(chunks))
    if npool > 1:
        pool = multiprocessing.Pool(npool)

    h = hfunc + ">>" + hname + "(" + hbins
    
    ROOT.gROOT.cd()            
    if npool == 1:
        n = tf.Draw(h, cuts, "goff")
        h = ROOT.gROOT.Get(hname)
    else:
        parargs = []
        for ch in chunks:
            parargs += [tuple([tf, h, cuts, ch, min(chunksize, ntot-ch)])]
        hlist = pool.map(drawHelper, parargs)
        
        #h = sum(h)
        h = hlist[0].Clone()
        for h_ in hlist[1:]:
            h.Add(h_)
    hold = h
    of.cd()
    h = h.Clone()    

    #print of.GetName(), h.GetName()
    #h.SetDirectory(of)
    h.Write()
    #of.Append(h, True)
    
    hold.Delete()
        
    if isinstance(cut, ROOT.TEntryList):
        tf.SetEntryList(0)
    
    if npool > 1:
        pool.close()

    return 0

if __name__ == "__main__":

    # output root file
    of = ROOT.TFile("ControlPlotsMEM.root", "RECREATE")


    # dict of dicts. First key: sample Second key: cut
    # Content: events at given lumi
    event_counts = {}
    
    for sample in samples:
        print sample
        sample_shortname = sample.replace(".root", "")

        event_counts[sample_shortname] = {}

        tf = ROOT.TChain("tree")
        for fn in [samplepath+sample]:
            
            if not os.path.isfile(fn):
                raise Exception("could not open ROOT file: {0}".format(fn))
            tf.AddFile(fn)        
        print "Read ", tf.GetEntries(), "entries"

        of.cd()
        
        sampled = of.mkdir(sample_shortname)
        sampled.cd()

        for cutname, cut in [
            ("sl", "is_sl"),
            ("sl_jge6_t2", "is_sl && numJets>=6 && nBCSVM==2"),
            ("sl_jge6_t3", "is_sl && numJets>=6 && nBCSVM==3"),
            ("sl_jge6_tge4", "is_sl && numJets>=6 && nBCSVM>=4"),
            ]:
            
            print "cut:", cutname
            
            trig = "(1)"
            if "sl" in cutname:
                trig = "(HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v || HLT_BIT_HLT_IsoMu24_eta2p1_v)"
            cut = "{0} && {1}".format(cut, trig)
            jetd = sampled.mkdir(cutname)
            Draw(tf, jetd, sample_shortname, "nBCSVM:numJets >> njets_ntags(15,0,15,15,0,15)", cut)
            
            Draw(tf, jetd, sample_shortname, "leps_pt[0] >> lep0_pt(20,0,500)", cut)
            if "dl" in cutname:
                Draw(tf, jetd, sample_shortname, "leps_pt[1] >> lep1_pt(20,0,500)", cut)

            Draw(tf, jetd, sample_shortname, "leps_pdgId[0] >> lep0_pdgId(100,-50,50)", cut)
            if "dl" in cutname:
                Draw(tf, jetd, sample_shortname, "leps_pdgId[1] >> lep1_pdgId(100,-50,50)", cut)

            Draw(tf, jetd, sample_shortname, "leps_relIso03[0] >> lep0_relIso03(100,0,0.5)", cut)
            if "dl" in cutname:
                Draw(tf, jetd, sample_shortname, "leps_relIso03[1] >> lep1_relIso03(100,0,0.5)", cut)

            Draw(tf, jetd, sample_shortname, "leps_relIso04[0] >> lep0_relIso04(100,0,0.5)", cut)
            if "dl" in cutname:
                Draw(tf, jetd, sample_shortname, "leps_relIso04[1] >> lep1_relIso04(100,0,0.5)", cut)

            #Draw(tf, jetd, gensyst, "nBCSVM:numJets >> njets_ntags(15,0,15,15,0,15)", cut)
            Draw(tf, jetd, sample_shortname, "jets_pt[0] >> jet0_pt(20,0,500)", cut)
            Draw(tf, jetd, sample_shortname, "jets_pt[1] >> jet1_pt(20,0,500)", cut)

            Draw(tf, jetd, sample_shortname, "jets_btagCSV[0] >> jet0_btagCSV(20,0,1)", cut)
            Draw(tf, jetd, sample_shortname, "jets_btagCSV[1] >> jet1_btagCSV(20,0,1)", cut)

            Draw(tf, jetd, sample_shortname, "jets_btagBDT[0] >> jet0_btagBDT(20,-1,1)", cut)
            Draw(tf, jetd, sample_shortname, "jets_btagBDT[1] >> jet1_btagBDT(20,-1,1)", cut)
                        
            Draw(tf, jetd, sample_shortname, "abs(jets_eta[0]) >> jet0_aeta(20, 0, 5)", cut)
            Draw(tf, jetd, sample_shortname, "abs(jets_eta[1]) >> jet1_aeta(20, 0, 5)", cut)
            
            Draw(tf, jetd, sample_shortname, "btag_LR_4b_2b >> btag_LR_4b_2b(200,0,1)", cut)
            Draw(tf, jetd, sample_shortname, "log(btag_LR_4b_2b/(1.0-btag_LR_4b_2b)) >> btag_LR_4b_2b_logit(60,-20,20)", cut)

            Draw(tf, jetd, sample_shortname, "higgsCandidate_mass >> higgsCandidate_mass(60, 0, 500)", cut)

            Draw(tf, jetd, sample_shortname, "higgsCandidate_tau1 >> higgsCandidate_tau1(60, 0, 1)", cut)
            Draw(tf, jetd, sample_shortname, "higgsCandidate_tau2 >> higgsCandidate_tau2(60, 0, 1)", cut)
            Draw(tf, jetd, sample_shortname, "higgsCandidate_tau3 >> higgsCandidate_tau3(60, 0, 1)", cut)
            Draw(tf, jetd, sample_shortname, "higgsCandidate_bbtag >> higgsCandidate_bbtag(60, -1, 1)", cut)
            Draw(tf, jetd, sample_shortname, "higgsCandidate_n_subjettiness >> higgsCandidate_n_subjettiness(60, -1, 1)", cut)

            #MEM distributions
            for matchname, matchcut in [
                    ("", "1"), #no matching criteria applied
                    #("_tb2_wq2", "nMatch_wq_btag==2 && nMatch_tb_btag==2"),
                    #("_hb2_tb2_wq2", "nMatch_hb_btag==2 && nMatch_wq_btag==2 && nMatch_tb_btag==2"),
                    #("_tb2_wq1", "nMatch_wq_btag==1 && nMatch_tb_btag==2"),
                    #("_hb2_tb2_wq1", "nMatch_hb_btag==2 && nMatch_wq_btag==1 && nMatch_tb_btag==2")
                ]:
                if "hb2" in matchname and "ttjets" in sample:
                    continue
                cut = " && ".join([cut, matchcut])
                if tf.GetEntries(cut) == 0:
                    continue

                #Various mem hypotheses
                #memname - suffix of the created histogram
                #memidx - index into the MEM results array (see MEAnalysis_cfg_heppy -> Conf.mem["methodOrder"])
                for memname, memidx in [
                    ("SL_0w2h2t", 0),
                    ("DL_0w2h2t", 1),
                    ]:

                    #skip unnecessary MEM distributions
                    if not (
                        ("dl" in cutname and "DL" in memname) or
                        ("sl" in cutname and "SL" in memname)
                        ):
                        continue

                    #1D mem distribution
                    Draw(tf, jetd, sample_shortname,
                        "mem_tth_p[{0}] / (mem_tth_p[{0}] + 0.15*mem_ttbb_p[{0}]) >> mem_{1}{2}(12,0,1)".format(
                            memidx, memname, matchname
                        ),
                        cut
                    )
            
            jetd.Write()

            
        sampled.Write()
    # End of loop over samples

    channels = ["sl_jge6_tge4", "sl_jge6_tge4_blrH", "sl_jge6_tge4_blrL"]
    print "writing"
    of.Write()
    of.Close()

    #PrintDatacard(event_counts, dcard.Datacard, dcof)
