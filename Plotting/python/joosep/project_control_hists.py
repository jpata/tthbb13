
import ROOT
ROOT.gROOT.SetBatch(True)
#ROOT.gErrorIgnoreLevel = ROOT.kError
import sys, os
import random
import numpy as np
import multiprocessing

class Sample:
    def __init__(self, name, filenames):
        self.name = name
        self.fileNamesS2 = filenames

path = "/Users/joosep/Documents/tth/data/ntp/sync722/nome2/"

samples_dict = {
    "tth_13tev_amcatnlo_pu20bx25": Sample(
        "ttH",
        [path + "tth_13tev_amcatnlo_pu20bx25.root"]
    ),
    "tth_13tev_amcatnlo_pu20bx25_hbb": Sample(
        "ttH_hbb",
        [path + "tth_13tev_amcatnlo_pu20bx25_hbb.root"]
    ),
    "tth_13tev_amcatnlo_pu20bx25_hX": Sample(
        "ttH_nohbb",
        [path + "tth_13tev_amcatnlo_pu20bx25_hX.root"]
    ),
    "ttjets_13tev_madgraph_pu20bx25_phys14_tt2b": Sample(
        "ttbarPlus2B",
        [path + "ttjets_13tev_madgraph_pu20bx25_phys14_tt2b.root"]
    ),
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttb": Sample(
        "ttbarPlusB",
        [path + "ttjets_13tev_madgraph_pu20bx25_phys14_ttb.root"]
    ),
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttbb": Sample(
        "ttbarPlusBBbar",
        [path + "ttjets_13tev_madgraph_pu20bx25_phys14_ttbb.root"]
    ),
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttcc": Sample(
        "ttbarPlusCCbar",
        [path + "ttjets_13tev_madgraph_pu20bx25_phys14_ttcc.root"]
    ),
    "ttjets_13tev_madgraph_pu20bx25_phys14_ttll": Sample(
        "ttbarOther",
        [path + "ttjets_13tev_madgraph_pu20bx25_phys14_ttll.root"]
    ),
    "ttw_13tev_madgraph_pu20bx25_phys14": Sample(
        "ttbarW",
        [path + "ttw_13tev_madgraph_pu20bx25_phys14.root"]
    ),
    "ttz_13tev_madgraph_pu20bx25_phys14": Sample(
        "ttbarZ",
        [path + "ttz_13tev_madgraph_pu20bx25_phys14.root"]
    ),
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
    
            #no weights applied
            ("unweighted",          "1.0"),
            
            #only b weight applied
            #("bw",                  "bTagWeight"),
            
            #Use JES-corrected values
            ("",                    "bTagWeight"),
            
            
            #JES up/down
            ("CMS_scale_jUp",       "bTagWeight_JESUp"),
            ("CMS_scale_jDown",     "bTagWeight_JESDown"),
            
            #CSV LF up/down
            ("CMS_ttH_CSVLFUp",     "bTagWeight_LFUp"),
            ("CMS_ttH_CSVLFDown",   "bTagWeight_LFDown"),
            #("bwLFDown",        "bTagWeight_LFDown"),
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
            
        #default, all corrections enabled
        if s.name == "":
            repllist += [("mem_tth_p[0]", "mem_tth_JES_p[0]")]
            repllist += [("mem_tth_p[1]", "mem_tth_JES_p[1]")]
            repllist += [("mem_tth_p[2]", "mem_tth_JES_p[2]")]
            repllist += [("mem_ttbb_p[0]", "mem_ttbb_JES_p[0]")]
            repllist += [("mem_ttbb_p[1]", "mem_ttbb_JES_p[1]")]
            repllist += [("mem_ttbb_p[2]", "mem_ttbb_JES_p[2]")]
        elif "CMS_scale_jUp" in s.name:
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
        
for sample in samples:
    print sample
    tf = ROOT.TChain("tree")
    for fn in samples_dict[sample].fileNamesS2:
        tf.AddFile(fn)
    print tf.GetEntries()

    #weight = "genWeight"
    of.cd()
    
    sampled = of.mkdir(samples_dict[sample].name)
    sampled.cd()

    for lep, lepcut in [("sl", "(is_sl==1 && passPV==1)"), ("dl", "(is_dl==1 && passPV==1)")]:
        for jet_tag, jettagcut in [

                ("j3_t2", "numJets==3 && nBCSVM==2"),
                ("jge3_tge3", "numJets>=3 && nBCSVM==3"),
                ("jge4_t2", "numJets>=4 && nBCSVM==2"),
                ("jge4_tge4", "numJets>=4 && nBCSVM>=4"),

                #("4j", "numJets==4"),
                ("j4_t3", "numJets==4 && nBCSVM==3"),
                ("j4_t4", "numJets==4 && nBCSVM==4"),

                #("5j", "numJets==5"),
                #("5jL", "numJets==5 && nBCSVM<3"),
                ("j5_t3", "numJets==5 && nBCSVM==3"),
                #("5j4t", "numJets==5 && nBCSVM==4"),
                ("j5_tge4", "numJets==5 && nBCSVM>=4"),
                #("5jH", "numJets==5 && nBCSVM>4"),
                
                #("6j", "numJets==6"),
                #("6jL", "numJets==6 && nBCSVM<3"),
                #("6j3t", "numJets==6 && nBCSVM==3"),
                #("6j4t", "numJets==6 && nBCSVM==4"),
                #("6jH", "numJets==6 && nBCSVM>4"),
                
                #("6plusj", "numJets>=6"),
                ("jge6_t2", "numJets>=6 && nBCSVM==2"),
                ("jge6_t3", "numJets>=6 && nBCSVM==3"),
                #("6plusj4t", "numJets>=6 && nBCSVM==4"),
                ("jge6_tge4", "numJets>=6 && nBCSVM>=4"),
                #("6plusjH", "numJets>=6 && nBCSVM>4"),
            ]:
            print jet_tag
            
            lepjetcut = " && ".join([lepcut, jettagcut])
            jetd = sampled.mkdir(lep + "_" + jet_tag)

            Draw(tf, jetd, gensyst, "nBCSVM:numJets >> njets_ntags(15,0,15,15,0,15)", lepjetcut)

            Draw(tf, jetd, gensyst, "jets_pt[0] >> jet0_pt(20,20,500)", lepjetcut)
            #Draw(tf, jetd, gensyst, "jets_pt[1] >> jet1_pt(20,20,500)", lepjetcut)

            #Draw(tf, jetd, gensyst, "jets_eta[0] >> jet0_eta(30,-5,5)", lepjetcut)

            Draw(tf, jetd, gensyst, "jets_btagCSV[0] >> jet0_csvv2(22, -0.1, 1)", lepjetcut)
        
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
            jetd.Write()

        
    sampled.Write()


print "writing"
of.Write()
of.Close()
