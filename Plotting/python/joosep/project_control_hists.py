#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError
#ROOT.gROOT.cd()
#ROOT.TH1.AddDirectory(False)
ROOT.TH1.SetDefaultSumw2(True)
import sys, os
import random
import numpy as np
import multiprocessing
import imp
import datetime

#Number of parallel processes to run for the histogram projection
#ncores = multiprocessing.cpu_count()
ncores = 4

samplepath = "/Users/joosep/Documents/tth/data/ntp/v14/"
samples = {
    "ttHTobb_M125_13TeV_powheg_pythia8": samplepath + "/me/ttHTobb_M125_13TeV_powheg_pythia8.root",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b": samplepath + "/me/TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb": samplepath + "/me/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb": samplepath + "/me/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc": samplepath + "/me/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll": samplepath + "/me/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root",
    "SingleMuon": samplepath + "/nome/SingleMuon.root",
    "SingleElectron": samplepath + "/nome/SingleElectron.root",
}

lumi = 1280.23
#lumi = 10000.0

def is_data(sample):
    if "Single" in sample:
        return True
    return False

def weight_str(cut, sample, weight=1.0, lumi=lumi):
    w = 1.0
    if not is_data(sample):
        return "weight_xs * sign(genWeight) * bTagWeight * {1} * {2} * {3} * ({0})".format(cut, weight, lumi, w)
    else:
        return "json==1 && ({0})".format(cut)

def drawHelper(args):
    """
    Simple draw command that projects out a histogram on a single core.
    Argument is a tuple because that allows it to be used transparently in
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
    h = ROOT.TH1D(hname, hname, int(hbins[0]), float(hbins[1]), float(hbins[2]))
    h.SetDirectory(ROOT.gROOT)
    #tf.SetDirectory(ROOT.gROOT)
    #ROOT.gROOT.Add(h)
    #n = 0
    n = tf.Draw(hfunc + ">>{0}".format(hname), cut, "goff", nev, nfirst)
    #h = ROOT.gROOT.Get(hname)
    h = ROOT.gROOT.Get(hname)
    if not (type(h) in [ROOT.TH1D, ROOT.TH2D, ROOT.TH1F, ROOT.TH2F]):
        raise Exception("Wrong histo type: {0}".format(type(h)))
    if (h.GetEntries() != n):
        raise Exception("Wrong number of entries: {0} != {1}".format(
            h.GetEntries(), n
        ))
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
    
    cuts = cut
    if isinstance(cut, ROOT.TEventList):
        cuts = "1.0"
        tf.SetEventList(cut)
    if hasattr(tf, "elist"):
        cuts = "1.0"
        tf.SetEventList(tf.elist)

    ntot = tf.GetEntriesFast()

    #how many events to process per core
    chunksize = max(ntot/ncores, 100000)
    chunks = range(0, ntot, chunksize)
    #print args, len(chunks)
    
    npool = min(ncores, len(chunks))
    if npool > 1:
        pool = multiprocessing.Pool(npool)

    h = hfunc + ">>" + hname + "(" + hbins
    
    ROOT.gROOT.cd()            
    if npool == 1:
        h = drawHelper((tf, h, cuts, 0, ntot))
        #n = tf.Draw(h, cuts, "goff")    
        #h = ROOT.gROOT.Get(hname)
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
    
    for samplename, samplepath in samples.items():
        print samplename

        event_counts[samplename] = {}

        tf = ROOT.TChain("tree")
        for fn in [samplepath]:
            if not os.path.isfile(fn):
                raise Exception("could not open ROOT file: {0}".format(fn))
            tf.AddFile(fn)
        print "Read ", tf.GetEntries(), "entries"
        tf.SetCacheSize(128 * 1024 * 1024)

        of.cd()
        
        sampled = of.mkdir(samplename)
        sampled.cd()

        for cutname, cut in [
            ("sl", "is_sl"),

            ("sl_mu", "is_sl && abs(leps_pdgId[0])==13"),
            ("sl_jge4_mu", "is_sl && numJets>=4 && abs(leps_pdgId[0])==13"),
            
            ("sl_j4_t3_mu", "is_sl && numJets==4 && nBCSVM==3 && abs(leps_pdgId[0])==13"),
            ("sl_j4_t4_mu", "is_sl && numJets==4 && nBCSVM==4 && abs(leps_pdgId[0])==13"),

            ("sl_j5_t3_mu", "is_sl && numJets==5 && nBCSVM==3 && abs(leps_pdgId[0])==13"),
            ("sl_j5_tge4_mu", "is_sl && numJets==5 && nBCSVM>=4 && abs(leps_pdgId[0])==13"),

            ("sl_jge6_mu", "is_sl && numJets>=6 && abs(leps_pdgId[0])==13"),
            ("sl_jge6_t2_mu", "is_sl && numJets>=6 && nBCSVM==2 && abs(leps_pdgId[0])==13"),
            ("sl_jge6_t3_mu", "is_sl && numJets>=6 && nBCSVM==3 && abs(leps_pdgId[0])==13"),
            ("sl_jge6_tge4_mu", "is_sl && numJets>=6 && nBCSVM>=4 && abs(leps_pdgId[0])==13"),
            

            ("sl_el", "is_sl && abs(leps_pdgId[0])==11"),
            ("sl_jge4_el", "is_sl && numJets>=4 && abs(leps_pdgId[0])==11"),
            
            ("sl_j4_t3_el", "is_sl && numJets==4 && nBCSVM==3 && abs(leps_pdgId[0])==11"),
            ("sl_j4_t4_el", "is_sl && numJets==4 && nBCSVM==4 && abs(leps_pdgId[0])==11"),

            ("sl_j5_t3_el", "is_sl && numJets==5 && nBCSVM==3 && abs(leps_pdgId[0])==11"),
            ("sl_j5_tge4_el", "is_sl && numJets==5 && nBCSVM>=4 && abs(leps_pdgId[0])==11"),

            ("sl_jge6_el", "is_sl && numJets>=6 && abs(leps_pdgId[0])==11"),
            ("sl_jge6_t2_el", "is_sl && numJets>=6 && nBCSVM==2 && abs(leps_pdgId[0])==11"),
            ("sl_jge6_t3_el", "is_sl && numJets>=6 && nBCSVM==3 && abs(leps_pdgId[0])==11"),
            ("sl_jge6_tge4_el", "is_sl && numJets>=6 && nBCSVM>=4 && abs(leps_pdgId[0])==11"),
            ]:

        
            #add the trigger flags
            # trig = "(1)"
            # if "sl" in cutname:
            #     trig = "(HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v || HLT_BIT_HLT_IsoMu24_eta2p1_v)"
            # cut = "{0} && {1}".format(cut, trig)

            print "cut:", cutname, tf.GetEntries(cut)
            #ROOT.gROOT.cd()
            #tf.Draw(">>elist", cut)
            #elist = ROOT.gROOT.Get("elist")
            #tf.elist = elist
            #tf.SetEventList(elist)

            jetd = sampled.mkdir(cutname)
            Draw(tf, jetd, samplename, "nBCSVM:numJets >> njets_ntags(15,0,15,15,0,15)", cut)
            Draw(tf, jetd, samplename, "nBCSVM >> ntags(5,2,7)", cut)
            if "sl" in cutname:
                Draw(tf, jetd, samplename, "numJets >> njets(7,4,11)", cut)
            elif "dl" in cutname:
                Draw(tf, jetd, samplename, "numJets >> njets(7,2,9)", cut)
            #Draw(tf, jetd, samplename, "nfatjets >> nfatjets(5,0,5)", cut)
            
            Draw(tf, jetd, samplename, "leps_pt[0] >> lep0_pt(20,0,500)", cut)
            if "dl" in cutname:
                Draw(tf, jetd, samplename, "leps_pt[1] >> lep1_pt(20,0,500)", cut)
            # 
            # Draw(tf, jetd, samplename, "leps_pdgId[0] >> lep0_pdgId(100,-50,50)", cut)
            # if "dl" in cutname:
            #     Draw(tf, jetd, samplename, "leps_pdgId[1] >> lep1_pdgId(100,-50,50)", cut)
            # 
            # Draw(tf, jetd, samplename, "leps_relIso03[0] >> lep0_relIso03(100,0,0.5)", cut)
            # if "dl" in cutname:
            #     Draw(tf, jetd, samplename, "leps_relIso03[1] >> lep1_relIso03(100,0,0.5)", cut)
            # 
            # Draw(tf, jetd, samplename, "leps_relIso04[0] >> lep0_relIso04(100,0,0.5)", cut)
            # if "dl" in cutname:
            #     Draw(tf, jetd, samplename, "leps_relIso04[1] >> lep1_relIso04(100,0,0.5)", cut)

            #Draw(tf, jetd, gensyst, "nBCSVM:numJets >> njets_ntags(15,0,15,15,0,15)", cut)
            Draw(tf, jetd, samplename, "jets_pt[0] >> jet0_pt(20,0,500)", cut)
            Draw(tf, jetd, samplename, "jets_pt[1] >> jet1_pt(20,0,500)", cut)
            
            Draw(tf, jetd, samplename, "jets_eta[0] >> jet0_eta(20,-5,5)", cut)
            Draw(tf, jetd, samplename, "jets_eta[1] >> jet1_eta(20,-5,5)", cut)

            Draw(tf, jetd, samplename, "jets_btagCSV[0] >> jet0_btagCSV(20,0,1)", cut)
            Draw(tf, jetd, samplename, "jets_btagCSV[1] >> jet1_btagCSV(20,0,1)", cut)
            
            Draw(tf, jetd, samplename, "jets_btagBDT[0] >> jet0_btagBDT(20,-1,1)", cut)
            Draw(tf, jetd, samplename, "jets_btagBDT[1] >> jet1_btagBDT(20,-1,1)", cut)
                        
            Draw(tf, jetd, samplename, "abs(jets_eta[0]) >> jet0_aeta(20, 0, 5)", cut)
            Draw(tf, jetd, samplename, "abs(jets_eta[1]) >> jet1_aeta(20, 0, 5)", cut)
            
            Draw(tf, jetd, samplename, "btag_LR_4b_2b >> btag_LR_4b_2b(20,0,1)", cut)
            Draw(tf, jetd, samplename, "log(btag_LR_4b_2b/(1.0-btag_LR_4b_2b)) >> btag_LR_4b_2b_logit(20,-10,10)", cut)
            
            Draw(tf, jetd, samplename, "fatjets_pt[0] >> fatjet0_pt(20,0,500)", cut)
            Draw(tf, jetd, samplename, "fatjets_pt[1] >> fatjet1_pt(20,0,500)", cut)
            Draw(tf, jetd, samplename, "fatjets_eta[0] >> fatjet0_eta(20,-5,5)", cut)
            Draw(tf, jetd, samplename, "fatjets_eta[1] >> fatjet1_eta(20,-5,5)", cut)
            #fixme fatjet mass
            # Draw(tf, jetd, samplename, "topCandidate_pt[0] >> topCandidate_pt(20, 200, 800)", cut)
            # Draw(tf, jetd, samplename, "topCandidate_mass[0] >> topCandidate_mass(20, 80, 250)", cut)

            # #fixme low frec -> top cand mass and vice versa
            # Draw(tf, jetd, samplename, "topCandidate_fRec[0] >> topCandidate_fRec(20, 0, 0.5)", cut)
            # #fix binning 0.1
            # Draw(tf, jetd, samplename, "topCandidate_Ropt[0] >> topCandidate_Ropt(20, 0.4, 2)", cut)
            # Draw(tf, jetd, samplename, "topCandidate_RoptCalc[0] >> topCandidate_RoptCalc(20, 0.4, 2)", cut)
            # Draw(tf, jetd, samplename, "topCandidate_bbtag[0] >> topCandidate_bbtag(20, -1, 1)", cut)
            # Draw(tf, jetd, samplename, "topCandidate_tau1[0] >> topCandidate_tau1(20, 0, 1)", cut)
            # Draw(tf, jetd, samplename, "topCandidate_tau2[0] >> topCandidate_tau2(20, 0, 1)", cut)
            # Draw(tf, jetd, samplename, "topCandidate_tau3[0] >> topCandidate_tau3(20, 0, 1)", cut)
            # #top can mass peak
            # #groomed nsubjettiness only for tops
            # Draw(tf, jetd, samplename, "topCandidate_n_subjettiness[0] >> topCandidate_n_subjettiness(20, 0, 1)", cut)
            # 
            # #pt>400 as well
            # Draw(tf, jetd, samplename, "higgsCandidate_pt >> higgsCandidate_pt(20, 200, 800)", cut)
            # Draw(tf, jetd, samplename, "higgsCandidate_mass >> higgsCandidate_mass(20, 0, 500)", cut)
            # Draw(tf, jetd, samplename, "higgsCandidate_mass_pruned >> higgsCandidate_mass_pruned(20, 0, 500)", cut)
            # Draw(tf, jetd, samplename, "higgsCandidate_mass_softdrop >> higgsCandidate_mass_softdrop(20, 0, 500)", cut)
            # Draw(tf, jetd, samplename, "higgsCandidate_tau1 >> higgsCandidate_tau1(20, 0, 1)", cut)
            # Draw(tf, jetd, samplename, "higgsCandidate_tau2 >> higgsCandidate_tau2(20, 0, 1)", cut)
            # Draw(tf, jetd, samplename, "higgsCandidate_tau3 >> higgsCandidate_tau3(20, 0, 1)", cut)
            # Draw(tf, jetd, samplename, "higgsCandidate_bbtag >> higgsCandidate_bbtag(20, -1, 1)", cut)
            # Draw(tf, jetd, samplename, "higgsCandidate_n_subjettiness >> higgsCandidate_n_subjettiness(20, -1, 1)", cut)
            # Draw(tf, jetd, samplename, "higgsCandidate_dr_top >> higgsCandidate_dr_top(20, 0, 5)", cut)
            # Draw(tf, jetd, samplename, "higgsCandidate_dr_genHiggs >> higgsCandidate_dr_genHiggs(20, 0, 5)", cut)

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
                    ("SL_2w2h2t", 5),
                    ("DL_0w2h2t", 1),
                    ]:

                    #skip unnecessary MEM distributions
                    if not (
                        ("dl" in cutname and "DL" in memname) or
                        ("sl" in cutname and "SL" in memname)
                        ):
                        continue

                    #1D mem distribution
                    Draw(tf, jetd, samplename,
                        "mem_tth_p[{0}] / (mem_tth_p[{0}] + 0.15*mem_ttbb_p[{0}]) >> mem_{1}{2}(12,0,1)".format(
                            memidx, memname, matchname
                        ),
                        cut
                    )
            
            jetd.Write()

            
        sampled.Write()
        del tf
    # End of loop over samples

    channels = ["sl_jge6_tge4", "sl_jge6_tge4_blrH", "sl_jge6_tge4_blrL"]
    print "writing"
    of.Write()
    of.Close()

    #PrintDatacard(event_counts, dcard.Datacard, dcof)
