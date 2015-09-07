
import ROOT
ROOT.gROOT.SetBatch(True)
#ROOT.gErrorIgnoreLevel = ROOT.kError
import sys, os
import random
import numpy as np
import multiprocessing
import imp
from samples import samples_dict

datacard_path = sys.argv[1]

dcard = imp.load_source("dcard", datacard_path)
of = ROOT.TFile(dcard.Datacard.output_filename, "RECREATE")

#Number of parallel processes to run for the histogram projection
ncores = 4

def weight_str(cut, weight=1.0):
    return "weight_xs * sign(genWeight) * {1} * ({0})".format(cut, weight)
    #return "1.0 * ({0})".format(cut)

def drawHelper(args):
    tf, hist, cut, nfirst, nev = args
    #print hist, cut, nfirst, nev
    hname = hist.split(">>")[1].split("(")[0].strip()
    ROOT.gROOT.cd()
    ROOT.TH1.SetDefaultSumw2(True)
    n = tf.Draw(hist, cut, "goff", nev, nfirst)
    h = ROOT.gROOT.Get(hname)
    assert(h.GetEntries() == n)
    return h
        
class Systematic(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.__dict__.update(kwargs)
        
    def __str__(self):
        return "s {0} {1} {2}".format(
            self.name,
            getattr(self, "weight", None),
            getattr(self, "hfunc", None)
        )
        
def gensyst(hfunc, hname, cut):
    systs = []
    for sname, weight in dcard.Datacard.weights:
        s = Systematic(sname, weight=weight, hfunc=hfunc)
        
        repllist = [
        ]
        
        def replacer(s, repllist):
            for r1, r2 in repllist:
                s = s.replace(r1, r2)
            return s
            
        #default, all corrections enabled
        # if s.name == "":
        #     repllist += [("mem_tth_p[0]", "mem_tth_JES_p[0]")]
        #     repllist += [("mem_tth_p[1]", "mem_tth_JES_p[1]")]
        #     repllist += [("mem_tth_p[2]", "mem_tth_JES_p[2]")]
        #     repllist += [("mem_ttbb_p[0]", "mem_ttbb_JES_p[0]")]
        #     repllist += [("mem_ttbb_p[1]", "mem_ttbb_JES_p[1]")]
        #     repllist += [("mem_ttbb_p[2]", "mem_ttbb_JES_p[2]")]
        if "CMS_scale_jUp" in s.name:
            repllist += [("numJets",    "numJets_JESUp")]
            repllist += [("nBCSVM",     "nBCSVM_JESUp")]
            repllist += [("jets_pt[0]", "jets_corr_JESUp[0]/jets_corr[0] * jets_pt[0]")]
        elif "CMS_scale_jDown" in s.name:
            repllist += [("numJets",    "numJets_JESDown")]
            repllist += [("nBCSVM",     "nBCSVM_JESDown")]
            repllist += [("jets_pt[0]", "jets_corr_JESDown[0]/jets_corr[0] * jets_pt[0]")]
        s.repllist = repllist
        s.varreplacement = lambda cut, r=repllist: replacer(cut, r)
        
        systs += [s]
    return systs
    
def Draw(tf, of, gensyst, *args):
    hist = args[0]
    cut = args[1]
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
    chunksize = max(ntot/ncores, 100000)
    chunks = range(0, ntot, chunksize)
    #print args, len(chunks)
    
    npool = min(ncores, len(chunks))
    if npool > 1:
        pool = multiprocessing.Pool(npool)

    for syst in gensyst(hfunc, hname, cuts):
        
        replacer = getattr(syst, "varreplacement", lambda c: c)
        if len(syst.name)>0:
            hname_new = hname + "_" + syst.name
        else:
            hname_new = hname
        hfunc_new = replacer(hfunc)
        cuts_new = replacer(cuts)
        if syst.name == "unweighted":
            cut_new = cuts_new
        else:
            cut_new = weight_str(cuts_new, getattr(syst, "weight", "1.0"))
        h = hfunc_new + ">>" + hname_new + "(" + hbins
        
        ROOT.gROOT.cd()            
        if npool == 1:
            n = tf.Draw(h, cut_new, "goff")
            h = ROOT.gROOT.Get(hname_new)
        else:
            parargs = []
            for ch in chunks:
                parargs += [tuple([tf, h, cut_new, ch, min(chunksize, ntot-ch)])]
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
        
for sample in dcard.Datacard.samples:
    print sample
    tf = ROOT.TChain("tree")
    for fn in samples_dict[sample].fileNamesS2:
        if not os.path.isfile(fn):
            raise FileError("could not open file: {0}".format(fn))
        tf.AddFile(fn)
    print tf.GetEntries()

    #weight = "genWeight"
    of.cd()
    
    sampled = of.mkdir(samples_dict[sample].name)
    sampled.cd()

    for cutname, cut in dcard.Datacard.categories:
        
        jetd = sampled.mkdir(cutname)

        Draw(tf, jetd, gensyst, "nBCSVM:numJets >> njets_ntags(15,0,15,15,0,15)", cut)

        Draw(tf, jetd, gensyst, "jets_pt[0] >> jet0_pt(20,20,500)", cut)
        #Draw(tf, jetd, gensyst, "jets_pt[1] >> jet1_pt(20,20,500)", cut)

        #Draw(tf, jetd, gensyst, "jets_eta[0] >> jet0_eta(30,-5,5)", cut)

        Draw(tf, jetd, gensyst, "jets_btagCSV[0] >> jet0_csvv2(22, -0.1, 1)", cut)
    
        #Draw(tf, jetd, gensyst, "leps_pt[0] >> lep0_pt(30,0,300)", cut)
        #Draw(tf, jetd, gensyst, "leps_eta[0] >> lep0_eta(30,-5,5)", cut)
    
        #Draw(tf, jetd, gensyst, "btag_LR_4b_2b >> btag_lr(30,0,1)", cut)
        # 
        # Draw(tf, jetd, gensyst, "(100*nMatch_wq + 10*nMatch_hb + nMatch_tb) >> nMatch(300,0,300)", cut)
        # Draw(tf, jetd, gensyst, "(100*nMatch_wq_btag + 10*nMatch_hb_btag + nMatch_tb_btag) >> nMatch_btag(300,0,300)", cut)
        # 
        for match, matchcut in [
                ("nomatch", "1"),
                #("tb2_wq2", "nMatch_wq_btag==2 && nMatch_tb_btag==2"),
                #("hb2_tb2_wq2", "nMatch_hb_btag==2 && nMatch_wq_btag==2 && nMatch_tb_btag==2"),
                #("tb2_wq1", "nMatch_wq_btag==1 && nMatch_tb_btag==2"),
                #("hb2_tb2_wq1", "nMatch_hb_btag==2 && nMatch_wq_btag==1 && nMatch_tb_btag==2")
            ]:
            if "hb2" in match and "ttjets" in sample:
                continue
            cut = " && ".join([cut, matchcut])
            if tf.GetEntries(cut) == 0:
                continue
            for nmem in range(3):
                Draw(tf, jetd, gensyst,
                    "mem_tth_p[{0}] / (mem_tth_p[{0}] + 0.15*mem_ttbb_p[{0}]) >> mem_d_{1}_{0}(12,0,1)".format(nmem, match),
                    cut
                )
        
        jetd.Write()

        
    sampled.Write()


print "writing"
of.Write()
of.Close()
