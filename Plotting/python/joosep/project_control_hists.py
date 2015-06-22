
import ROOT
ROOT.gROOT.SetBatch(True)
#ROOT.gErrorIgnoreLevel = ROOT.kError
import sys, os
import random
import numpy as np
import multiprocessing

class Sample:
    def __init__(self, filenames):
        self.fileNamesS2 = filenames

path = "/Users/joosep/Documents/tth/data/ntp/sync722/nome2/"

samples_dict = {
    "tth_13tev_amcatnlo_pu20bx25": Sample([path + "tth_13tev_amcatnlo_pu20bx25.root"]),
    "tth_13tev_amcatnlo_pu20bx25_hbb": Sample([path + "tth_13tev_amcatnlo_pu20bx25_hbb.root"]),
    "tth_13tev_amcatnlo_pu20bx25_hX": Sample([path + "tth_13tev_amcatnlo_pu20bx25_hX.root"]),
    "ttjets_13tev_madgraph_pu20bx25_phys14_tt2b": Sample([path + "ttjets_13tev_madgraph_pu20bx25_phys14_tt2b.root"]),
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttb": Sample([path + "ttjets_13tev_madgraph_pu20bx25_phys14_ttb.root"]),
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttbb": Sample([path + "ttjets_13tev_madgraph_pu20bx25_phys14_ttbb.root"]),
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttcc": Sample([path + "ttjets_13tev_madgraph_pu20bx25_phys14_ttcc.root"]),
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttll": Sample([path + "ttjets_13tev_madgraph_pu20bx25_phys14_ttll.root"]),
    "ttw_13tev_madgraph_pu20bx25_phys14": Sample([path + "ttw_13tev_madgraph_pu20bx25_phys14.root"]),
    "ttz_13tev_madgraph_pu20bx25_phys14": Sample([path + "ttz_13tev_madgraph_pu20bx25_phys14.root"]),
}

samples = [
    "tth_13tev_amcatnlo_pu20bx25",
    "tth_13tev_amcatnlo_pu20bx25_hbb",
    "tth_13tev_amcatnlo_pu20bx25_hX",
    "ttjets_13tev_madgraph_pu20bx25_phys14_tt2b",
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttb",
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttbb",
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttcc",
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttll",
    "ttw_13tev_madgraph_pu20bx25_phys14",
    "ttz_13tev_madgraph_pu20bx25_phys14"
]

of = ROOT.TFile("ControlPlots.root", "RECREATE")

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
    for sname, weight in [
            ("unw",             "1.0"),
            ("bw",              "bTagWeight"),
            ("corr",            "bTagWeight"),
            ("JESUp",           "bTagWeight_JESUp"),
            ("JESDown",         "bTagWeight_JESDown"),
            ("bwLFUp",          "bTagWeight_LFUp"),
            ("bwLFDown",        "bTagWeight_LFDown"),
            # ("bwHFUp",          "bTagWeight_HFUp"),
            # ("bwHFDown",        "bTagWeight_HFDown"),
            # ("bwStats1Up",      "bTagWeight_Stats1Up"),
            # ("bwStats1Down",    "bTagWeight_Stats1Down"),
            # ("bwStats2Up",      "bTagWeight_Stats2Up"),
            # ("bwStats2Down",    "bTagWeight_Stats2Down"),
    ]:
        s = Systematic(sname, weight=weight, hfunc=hfunc)
        
        repllist = [
        ]
        
        def replacer(s, repllist):
            for r1, r2 in repllist:
                s = s.replace(r1, r2)
            return s
        if s.name == "corr":
            repllist += [("mem_tth_p[0]", "mem_tth_JES_p[0]")]
            repllist += [("mem_tth_p[1]", "mem_tth_JES_p[1]")]
            repllist += [("mem_tth_p[2]", "mem_tth_JES_p[2]")]
            repllist += [("mem_ttbb_p[0]", "mem_ttbb_JES_p[0]")]
            repllist += [("mem_ttbb_p[1]", "mem_ttbb_JES_p[1]")]
            repllist += [("mem_ttbb_p[2]", "mem_ttbb_JES_p[2]")]
        elif "JESUp" in s.name:
            repllist += [("numJets",    "numJets_JESUp")]
            repllist += [("nBCSVM",     "nBCSVM_JESUp")]
            repllist += [("jets_pt[0]", "jets_corr_JESUp[0] * jets_pt[0]")]
        elif "JESDown" in s.name:
            repllist += [("numJets",    "numJets_JESDown")]
            repllist += [("nBCSVM",     "nBCSVM_JESDown")]
            repllist += [("jets_pt[0]", "jets_corr_JESDown[0] * jets_pt[0]")]
        else:
            repllist += [("jets_pt[0]", "jets_corr[0] * jets_pt[0]")]
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
        hname_new = hname + "_" + syst.name
        hfunc_new = replacer(hfunc)
        cuts_new = replacer(cuts)
        if syst.name == "unw":
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
        
for sample in samples:
    print sample
    tf = ROOT.TChain("tree")
    for fn in samples_dict[sample].fileNamesS2:
        tf.AddFile(fn)
    print tf.GetEntries()

    #weight = "genWeight"
    of.cd()
    d = of.mkdir(sample)
    d.cd()
    Draw(tf, d, gensyst, "is_sl >> nsl(2,0,2)", "1")
    Draw(tf, d, gensyst, "is_dl >> ndl(2,0,2)", "1")

    for lep, lepcut in [("sl", "(is_sl==1 && passPV==1)"), ("dl", "(is_dl==1 && passPV==1)")]:
        print lep
        d.cd()
        lepd = d.mkdir(lep)
        lepd.cd()
        # Draw(tf, lepd, gensyst, "leps_pt[0] >> lep0_pt(30,0,300)", lepcut)
        # Draw(tf, lepd, gensyst, "leps_eta[0] >> lep0_eta(30,-5,5)", lepcut)
        # 
        # Draw(tf, lepd, gensyst, "leps_pt[1] >> lep1_pt(30,0,300)", lepcut)
        # Draw(tf, lepd, gensyst, "leps_eta[1] >> lep1_eta(30,-5,5)", lepcut)
        # 
        # Draw(tf, lepd, gensyst, "leps_pdgId[0] >> lep0_pdgId(32,-16,16)", lepcut)
        # if lep == "dl":
        #     Draw(tf, lepd, gensyst, "leps_pdgId[1] >> lep1_pdgId(32,-16,16)", lepcut)
        # 
        # Draw(tf, lepd, gensyst, "numJets >> njets(15,0,15)", lepcut)
        # Draw(tf, lepd, gensyst, "nBCSVM >> ntags(15,0,15)", lepcut)
        # 
        Draw(tf, lepd, gensyst, "nBCSVM:numJets >> njets_nBCSVM(15,0,15,15,0,15)", lepcut)
        # 
        # Draw(tf, lepd, gensyst, "jets_pt[0] >> jet0_pt(30,0,600)", lepcut)
        # Draw(tf, lepd, gensyst, "jets_eta[0] >> jet0_eta(30,-5,5)", lepcut)
        # 
        # Draw(tf, lepd, gensyst, "jets_pt[1] >> jet1_pt(30,0,600)", lepcut)
        # Draw(tf, lepd, gensyst, "jets_eta[1] >> jet1_eta(30,-5,5)", lepcut)
        # Draw(tf, lepd, gensyst, "(100*nMatch_wq + 10*nMatch_hb + nMatch_tb) >> nMatch(300,0,300)", lepcut)
        # Draw(tf, lepd, gensyst, "(100*nMatch_wq_btag + 10*nMatch_hb_btag + nMatch_tb_btag) >> nMatch_btag(300,0,300)", lepcut)
        for jet_tag, jettagcut in [
                # ("cat1H", "cat==1 && cat_btag==1"),
                # ("cat2H", "cat==2 && cat_btag==1"),
                # ("cat3H", "cat==3 && cat_btag==1"),
                # 
                # ("cat6Hee", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==22 && cat==6 && cat_btag==1"),
                # ("cat6Hem", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==24 && cat==6 && cat_btag==1"),
                # ("cat6Hmm", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==26 && cat==6 && cat_btag==1"),
        
                #("cat1L", "cat==1 && cat_btag==0"),
                #("cat2L", "cat==2 && cat_btag==0"),
                #("cat3L", "cat==3 && cat_btag==0"),
        
                #("cat6Lee", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==22 && cat==6 && cat_btag==0"),
                #("cat6Lem", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==24 && cat==6 && cat_btag==0"),
                #("cat6Lmm", "nleps==2 && (abs(leps_pdgId[0]) + abs(leps_pdgId[1]))==26 && cat==6 && cat_btag==0"),
                
                ("3j2t", "numJets==3 && nBCSVM==2"),
                ("3plusj3t", "numJets>=3 && nBCSVM==3"),
                ("4plusj2t", "numJets>=4 && nBCSVM==2"),
                ("4plusj4plust", "numJets>=4 && nBCSVM>=4"),

                #("4j", "numJets==4"),
                ("4j3t", "numJets==4 && nBCSVM==3"),
                ("4j4t", "numJets==4 && nBCSVM==4"),

                #("5j", "numJets==5"),
                #("5jL", "numJets==5 && nBCSVM<3"),
                ("5j3t", "numJets==5 && nBCSVM==3"),
                #("5j4t", "numJets==5 && nBCSVM==4"),
                ("5j4plust", "numJets==5 && nBCSVM>=4"),
                #("5jH", "numJets==5 && nBCSVM>4"),
                
                #("6j", "numJets==6"),
                #("6jL", "numJets==6 && nBCSVM<3"),
                #("6j3t", "numJets==6 && nBCSVM==3"),
                #("6j4t", "numJets==6 && nBCSVM==4"),
                #("6jH", "numJets==6 && nBCSVM>4"),
                
                #("6plusj", "numJets>=6"),
                ("6plusj2t", "numJets>=6 && nBCSVM==2"),
                ("6plusj3t", "numJets>=6 && nBCSVM==3"),
                #("6plusj4t", "numJets>=6 && nBCSVM==4"),
                ("6plusj4plust", "numJets>=6 && nBCSVM>=4"),
                #("6plusjH", "numJets>=6 && nBCSVM>4"),
                
                #("7j", "numJets==7"),
                #("7jL", "numJets==7 && nBCSVM<3"),
                #("7j3t", "numJets==7 && nBCSVM==3"),
                #("7j4t", "numJets==7 && nBCSVM==4"),
                #("7jH", "numJets==7 && nBCSVM>4"),
        
        #         ("8plusj", "njets>=8"),
        #         ("8plusjL", "njets>=8 && nBCSVM<3"),
        #         ("8plusj3t", "njets>=8 && nBCSVM==3"),
        #         ("8plusj4t", "njets>=8 && nBCSVM==4"),
        #         ("8plusjH", "njets>=8 && nBCSVM>4"),
            ]:
            print jet_tag
            
            lepjetcut = " && ".join([lepcut, jettagcut])
            lepd.cd()
            jetd = lepd.mkdir(jet_tag)

            #Draw(tf, jetd, gensyst, "nBCSVM:numJets >> njets_nBCSVM(15,0,15,15,0,15)", lepjetcut)

            Draw(tf, jetd, gensyst, "jets_pt[0] >> jet0_pt(20,20,500)", lepjetcut)
            #Draw(tf, jetd, gensyst, "jets_pt[1] >> jet1_pt(20,20,500)", lepjetcut)

            #Draw(tf, jetd, gensyst, "jets_eta[0] >> jet0_eta(30,-5,5)", lepjetcut)

            Draw(tf, jetd, gensyst, "jets_btagCSV[0] >> jet0_btagCSV(22, -0.1, 1)", lepjetcut)
        
            #Draw(tf, jetd, gensyst, "leps_pt[0] >> lep0_pt(30,0,300)", lepjetcut)
            #Draw(tf, jetd, gensyst, "leps_eta[0] >> lep0_eta(30,-5,5)", lepjetcut)
        
            #Draw(tf, jetd, gensyst, "btag_LR_4b_2b >> btag_lr(30,0,1)", lepjetcut)
            # 
            # Draw(tf, jetd, gensyst, "(100*nMatch_wq + 10*nMatch_hb + nMatch_tb) >> nMatch(300,0,300)", lepjetcut)
            # Draw(tf, jetd, gensyst, "(100*nMatch_wq_btag + 10*nMatch_hb_btag + nMatch_tb_btag) >> nMatch_btag(300,0,300)", lepjetcut)
            # 
            # for match, matchcut in [
            #         ("nomatch", "1"),
            #         ("tb2_wq2", "nMatch_wq_btag==2 && nMatch_tb_btag==2"),
            #         ("hb2_tb2_wq2", "nMatch_hb_btag==2 && nMatch_wq_btag==2 && nMatch_tb_btag==2"),
            #         ("tb2_wq1", "nMatch_wq_btag==1 && nMatch_tb_btag==2"),
            #         ("hb2_tb2_wq1", "nMatch_hb_btag==2 && nMatch_wq_btag==1 && nMatch_tb_btag==2")
            #     ]:
            #     if "hb2" in match and "ttjets" in sample:
            #         continue
            #     cut = " && ".join([lepcut, jettagcut, matchcut])
            #     if tf.GetEntries(cut) == 0:
            #         continue
            #     for nmem in range(3):
            #         Draw(tf, jetd, gensyst,
            #             "mem_tth_p[{0}] / (mem_tth_p[{0}] + 0.15*mem_ttbb_p[{0}]) >> mem_d_{1}_{0}(20,0,1)".format(nmem, match),
            #             cut
            #         )
            # 
            # jetd.Write()

        
        lepd.Write()
    d.Write()


print "writing"
of.Write()
of.Close()
