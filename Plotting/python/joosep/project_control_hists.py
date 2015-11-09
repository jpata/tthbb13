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
ncores = 30

samplepath = "/dev/shm/joosep/"
samples = {
    "ttHTobb_M125_13TeV_powheg_pythia8": samplepath + "/ttHTobb_M125_13TeV_powheg_pythia8.root",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b": samplepath + "/TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb": samplepath + "/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb": samplepath + "/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc": samplepath + "/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll": samplepath + "/TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root",
    "SingleMuon": samplepath + "/SingleMuon.root",
    "SingleElectron": samplepath + "/SingleElectron.root",
    "DoubleEG": samplepath + "/DoubleEG.root",
    "DoubleMuon": samplepath + "/DoubleMuon.root",
    "MuonEG": samplepath + "/MuonEG.root",
}

lumi = 1280.23
#lumi = 10000.0

def is_data(sample):
    if "Single" in sample or "Double" in sample or "Muon" in sample:
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
    chunksize = max(ntot/ncores, 10000)
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
            if h.GetNbinsX() != h_.GetNbinsX():
                raise Exception("bin error: " + h.GetName())
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
            #("dl", "is_dl"),
            ('dl_j3_t2', "(is_dl==1) & (numJets==3) & (nBCSVM==2)"),
            ('dl_jge3_t3', "(is_dl==1) & (numJets>=3) & (nBCSVM==3)"),
            ('dl_jge4_t2', "(is_dl==1) & (numJets>=4) & (nBCSVM==2)"),
            ('dl_jge4_tge4', "(is_dl==1) & (numJets>=4) & (nBCSVM>=4)"),
     
            #("sl", "is_sl"),

            #("sl_mu", "is_sl && abs(leps_pdgId[0])==13"),
            #("sl_jge4_mu", "is_sl && numJets>=4 && abs(leps_pdgId[0])==13"),
            
            ("sl_j4_t3_mu", "is_sl && numJets==4 && nBCSVM==3 && abs(leps_pdgId[0])==13"),
            #("sl_j4_t4_mu", "is_sl && numJets==4 && nBCSVM==4 && abs(leps_pdgId[0])==13"),

            ("sl_j5_t3_mu", "is_sl && numJets==5 && nBCSVM==3 && abs(leps_pdgId[0])==13"),
            ("sl_j5_tge4_mu", "is_sl && numJets==5 && nBCSVM>=4 && abs(leps_pdgId[0])==13"),

            #("sl_jge6_mu", "is_sl && numJets>=6 && abs(leps_pdgId[0])==13"),
            ("sl_jge6_t2_mu", "is_sl && numJets>=6 && nBCSVM==2 && abs(leps_pdgId[0])==13"),
            ("sl_jge6_t3_mu", "is_sl && numJets>=6 && nBCSVM==3 && abs(leps_pdgId[0])==13"),
            ("sl_jge6_tge4_mu", "is_sl && numJets>=6 && nBCSVM>=4 && abs(leps_pdgId[0])==13"),
            

            #("sl_el", "is_sl && abs(leps_pdgId[0])==11"),
            #("sl_jge4_el", "is_sl && numJets>=4 && abs(leps_pdgId[0])==11"),
            
            ("sl_j4_t3_el", "is_sl && numJets==4 && nBCSVM==3 && abs(leps_pdgId[0])==11"),
            #("sl_j4_t4_el", "is_sl && numJets==4 && nBCSVM==4 && abs(leps_pdgId[0])==11"),

            ("sl_j5_t3_el", "is_sl && numJets==5 && nBCSVM==3 && abs(leps_pdgId[0])==11"),
            #("sl_j5_tge4_el", "is_sl && numJets==5 && nBCSVM>=4 && abs(leps_pdgId[0])==11"),

            #("sl_jge6_el", "is_sl && numJets>=6 && abs(leps_pdgId[0])==11"),
            ("sl_jge6_t2_el", "is_sl && numJets>=6 && nBCSVM==2 && abs(leps_pdgId[0])==11"),
            ("sl_jge6_t3_el", "is_sl && numJets>=6 && nBCSVM==3 && abs(leps_pdgId[0])==11"),
            ("sl_jge6_tge4_el", "is_sl && numJets>=6 && nBCSVM>=4 && abs(leps_pdgId[0])==11"),
            ]:

        
            #add the trigger flags
            trig = "(1)"
            if "sl" in cutname:
                trig = "(HLT_WmnHbbAll) | (HLT_WenHbbAll)"
            elif "dl" in cutname:
                trig = "(HLT_ZmmHbbAll) | (HLT_ZeeHbbAll) | (HLT_ttHleptonic)"
            cut = "{0} && {1}".format(cut, trig)

            print "cut:", cutname, tf.GetEntries(cut)
            #ROOT.gROOT.cd()
            #tf.Draw(">>elist", cut)
            #elist = ROOT.gROOT.Get("elist")
            #tf.elist = elist
            #tf.SetEventList(elist)

            jetd = sampled.mkdir(cutname)
            #Draw(tf, jetd, samplename, "nBCSVM:numJets >> njets_ntags(15,0,15,15,0,15)", cut)
            Draw(tf, jetd, samplename, "nBCSVM >> ntags(5,2,7)", cut)
            if "sl" in cutname:
                Draw(tf, jetd, samplename, "numJets >> njets(7,4,11)", cut)
            elif "dl" in cutname:
                Draw(tf, jetd, samplename, "numJets >> njets(7,2,9)", cut)
            Draw(tf, jetd, samplename, "nfatjets >> nfatjets(5,0,5)", cut)
            
            Draw(tf, jetd, samplename, "leps_pt[0] >> lep0_pt(20,0,500)", cut)
            if "dl" in cutname:
                Draw(tf, jetd, samplename, "leps_pt[1] >> lep1_pt(20,0,500)", cut)
            
            Draw(tf, jetd, samplename, "leps_pdgId[0] >> lep0_pdgId(100,-50,50)", cut)
            if "dl" in cutname:
                Draw(tf, jetd, samplename, "leps_pdgId[1] >> lep1_pdgId(100,-50,50)", cut)
            
            Draw(tf, jetd, samplename, "leps_relIso03[0] >> lep0_relIso03(100,0,0.5)", cut)
            if "dl" in cutname:
                Draw(tf, jetd, samplename, "leps_relIso03[1] >> lep1_relIso03(100,0,0.5)", cut)
            
            Draw(tf, jetd, samplename, "leps_relIso04[0] >> lep0_relIso04(100,0,0.5)", cut)
            if "dl" in cutname:
                Draw(tf, jetd, samplename, "leps_relIso04[1] >> lep1_relIso04(100,0,0.5)", cut)

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
            if "sl" in cutname: 
                Draw(tf, jetd, samplename, "fatjets_pt[0] >> fatjet0_pt(20,0,500)", cut)
                Draw(tf, jetd, samplename, "fatjets_pt[1] >> fatjet1_pt(20,0,500)", cut)
                Draw(tf, jetd, samplename, "fatjets_eta[0] >> fatjet0_eta(20,-5,5)", cut)
                Draw(tf, jetd, samplename, "fatjets_eta[1] >> fatjet1_eta(20,-5,5)", cut)
                Draw(tf, jetd, samplename, "fatjets_mass[0] >> fatjet0_mass(20,0,300)", cut)
                Draw(tf, jetd, samplename, "fatjets_mass[1] >> fatjet1_mass(20,0,300)", cut)
                Draw(tf, jetd, samplename, "topCandidate_pt[0] >> topCandidate_pt(20, 200, 800)", cut)
                Draw(tf, jetd, samplename, "topCandidate_mass[0] >> topCandidate_mass(20, 80, 250)", cut)

                #fixme low frec -> top cand mass and vice versa
                for (addcutname, addcut) in [
                    ("inclusive", "1"),
                    ("_fRecless02", "topCandidate_fRec[0]<0.2"),
                    ("_fRecgeq02", "topCandidate_fRec[0]>=0.2"),
                    ("_massOn", "topCandidate_mass[0]>120 && topCandidate_mass[0]<200"),
                    ("_massOff", "topCandidate_mass[0]>120 && topCandidate_mass[0]<200"),
                ]:
                    _cut = cut + "&&" + addcut
                    Draw(tf, jetd, samplename, "topCandidate_fRec[0] >> topCandidate_fRec_{0}(50, 0, 0.5)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "topCandidate_Ropt[0] >> topCandidate_Ropt_{0}(20, 0.4, 2)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "topCandidate_RoptCalc[0] >> topCandidate_RoptCalc_{0}(20, 0.4, 2)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "topCandidate_bbtag[0] >> topCandidate_bbtag_{0}(20, -1, 1)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "topCandidate_tau1[0] >> topCandidate_tau1_{0}(20, 0, 1)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "topCandidate_tau2[0] >> topCandidate_tau2_{0}(20, 0, 1)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "topCandidate_tau3[0] >> topCandidate_tau3_{0}(20, 0, 1)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "topCandidate_n_subjettiness[0] >> topCandidate_n_subjettiness_{0}(20, 0, 1)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "topCandidate_n_subjettiness_groomed[0] >> topCandidate_n_subjettiness_groomed_{0}(20, 0, 1)".format(addcutname), _cut)
                
                for (addcutname, addcut) in [
                    ("inclusive", "1"),
                    ("_ptless400", "higgsCandidate_pt<400"),
                    ("_ptgeq400", "higgsCandidate_pt>=400"),
                ]:
                    _cut = cut + "&&" + addcut
                    Draw(tf, jetd, samplename, "higgsCandidate_pt >> higgsCandidate_pt_{0}(20, 200, 800)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "higgsCandidate_mass >> higgsCandidate_mass_{0}(20, 0, 500)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "higgsCandidate_mass_pruned >> higgsCandidate_mass_pruned_{0}(20, 0, 500)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "higgsCandidate_mass_softdrop >> higgsCandidate_mass_softdrop_{0}(20, 0, 500)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "higgsCandidate_bbtag >> higgsCandidate_bbtag_{0}(20, -1, 1)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "higgsCandidate_n_subjettiness >> higgsCandidate_n_subjettiness_{0}(20, -1, 1)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "higgsCandidate_dr_top >> higgsCandidate_dr_top_{0}(20, 0, 5)".format(addcutname), _cut)
                    Draw(tf, jetd, samplename, "higgsCandidate_dr_genHiggs >> higgsCandidate_dr_genHiggs_{0}(20, 0, 5)".format(addcutname), _cut)

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

    print "writing"
    of.Write()
    of.Close()
