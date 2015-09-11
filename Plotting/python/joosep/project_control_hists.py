#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
#ROOT.gErrorIgnoreLevel = ROOT.kError
import sys, os
import random
import numpy as np
import multiprocessing
import imp
import datetime
from samples import samples_dict

#Number of parallel processes to run for the histogram projection
#ncores = multiprocessing.cpu_count()
ncores = 1

def weight_str(cut, weight=1.0, lumi=1.0):
    return "weight_xs * sign(genWeight) * {1} * {2} * ({0})".format(cut, weight, lumi)
    #return "1.0 * ({0})".format(cut)

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

    NB: the histogram is created in the !!globa!! ROOT "memory directory"
    Returns: resulting histogram
    """
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
    """
    hfunc (string): 
    hname (string):  
    cut (string): 
    """
    systs = []
    for sname, weight in dcard.Datacard.weights:
        s = Systematic(sname, weight=weight, hfunc=hfunc)
        
        repllist = [
        ]
        
        def replacer(s, repllist):
            """
            Mini-function that performs in-place replacements for systematics
            """
            for r1, r2 in repllist:
                s = s.replace(r1, r2)
            return s
            
        #Here we list all replacement rules for the TTree variables that
        #need to be done for a particular systematic
        
        #JES variations need replacements of the numJets, nBCSVM and pretty much every
        #jet-containing variable down the line (e.g. Fox-Wolfram momenta)
        #FIXME: Type1 propagation to MET
        if "CMS_scale_jUp" in s.name:
            repllist += [("numJets",    "numJets_JESUp")]
            repllist += [("nBCSVM",     "nBCSVM_JESUp")]
            for ij in range(5):
                repllist += [("jets_pt[{0}]".format(ij), "jets_corr_JESUp[{0}]/jets_corr[{0}] * jets_pt[{0}]".format(ij))]
            repllist += [("mem_tth_p", "mem_tth_JESUp_p")]
            repllist += [("mem_ttbb_p", "mem_ttbb_JESUp_p")]
        elif "CMS_scale_jDown" in s.name:
            repllist += [("numJets",    "numJets_JESDown")]
            repllist += [("nBCSVM",     "nBCSVM_JESDown")]
            for ij in range(5):
                repllist += [("jets_pt[{0}]".format(ij), "jets_corr_JESUp[{0}]/jets_corr[{0}] * jets_pt[{0}]".format(ij))]
            repllist += [("mem_tth_p", "mem_tth_JESDown_p")]
            repllist += [("mem_ttbb_p", "mem_ttbb_JESDown_p")]
        s.repllist = repllist
        s.varreplacement = lambda cut, r=repllist: replacer(cut, r)
        
        systs += [s]
    return systs
    
def Draw(tf, of, gensyst, *args):
    """
    tf (TFile): Input file
    of (TFile): output file
    gensyst (method): function to generate systematics 
    args (list): (hist, cut)
        hist (string): TTree::Draw type command of the form "jet_pt >> h(10,0,100)"
        cut (string): cutstring for TTree::Draw
        OR
        cut (TEntryList): pre-determined entry list with the events passing the cut
    """
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
    chunksize = max(ntot/ncores, 10000)
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
            cut_new = weight_str(cuts_new, getattr(syst, "weight", "1.0"), dcard.Datacard.lumi)
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

        
def PrintDatacard(event_counts, datacard, dcof):

    number_of_bins = len(datacard.analysis_categories)    
    number_of_backgrounds = len(datacard.samples) - 1 

    dcof.write("imax {0}\n".format(number_of_bins))
    dcof.write("jmax {0}\n".format(number_of_backgrounds))
    dcof.write("kmax *\n".format(number_of_backgrounds))
    dcof.write("---------------\n")

    for cat in datacard.analysis_categories:                
        # Loop over the full table of categories and extract the one we're interested in. Pick up the corresponding MEM var
        analysis_var = [c[2] for c in datacard.categories if c[0]==cat][0]
        dcof.write("shapes * {0} {1} $PROCESS/$CHANNEL/{2} $PROCESS/$CHANNEL/{2}_$SYSTEMATIC\n".format(cat, of_name, analysis_var))

    # TODO: Automatic handling of 'fake' data
    dcof.write("shapes data_obs sl_jge6_tge4 /shome/jpata/tth/datacards/Sep7_ref2_spring15/fakeData.root $PROCESS/$CHANNEL/mem_d_nomatch_0 $PROCESS/$CHANNEL/mem_d_nomatch_0_$SYSTEMATIC\n")
        
    dcof.write("---------------\n")

    dcof.write("bin\t" +  "\t".join(datacard.analysis_categories) + "\n")
    dcof.write("observation\t" + "\t".join("-1" for _ in datacard.analysis_categories) + "\n")
    dcof.write("---------------\n")

    bins        = []
    processes_0 = []
    processes_1 = []
    rates       = []

    # Conversion: 
    # Example: ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hbb -> ttH_hbb
    samples = [samples_dict[s].name for s in datacard.samples]

    for cat in datacard.analysis_categories:
        for i_sample, sample in enumerate(samples):
            bins.append(cat)
            processes_0.append(sample)
            processes_1.append(str(i_sample))
            rates.append(str(event_counts[sample][cat]))

    dcof.write("bin\t"+"\t".join(bins)+"\n")
    dcof.write("process\t"+"\t".join(processes_0)+"\n")
    dcof.write("process\t"+"\t".join(processes_1)+"\n")
    dcof.write("rate\t"+"\t".join(rates)+"\n")
    dcof.write("---------------\n")

    # Gather all scale uncerainties
    all_scale_uncerts = []
    for k,v in datacard.scale_uncertainties.iteritems():
        for kk, vv in v.iteritems():
            all_scale_uncerts.extend(vv.keys())
    # Uniquify
    all_scale_uncerts = list(set(all_scale_uncerts))
            
    for scale in all_scale_uncerts:
        dcof.write(scale + "\t lnN \t")
        for cat in datacard.analysis_categories:
            for sample in samples:
                if (cat in datacard.scale_uncertainties.keys() and 
                    sample in datacard.scale_uncertainties[cat].keys() and 
                    scale in datacard.scale_uncertainties[cat][sample].keys()):
                    dcof.write(str(datacard.scale_uncertainties[cat][sample][scale]))
                else:
                    dcof.write("-")
                dcof.write("\t")
        dcof.write("\n")

    # Gather all shape uncerainties
    all_shape_uncerts = []
    for k,v in datacard.shape_uncertainties.iteritems():
        for kk, vv in v.iteritems():
            all_shape_uncerts.extend(vv.keys())
    # Uniquify
    all_shape_uncerts = list(set(all_shape_uncerts))


    for shape in all_shape_uncerts:
        dcof.write(shape + "\t shape \t")
        for cat in datacard.analysis_categories:
            for sample in samples:
                if (cat in datacard.shape_uncertainties.keys() and 
                    sample in datacard.shape_uncertainties[cat].keys() and 
                    shape in datacard.shape_uncertainties[cat][sample].keys()):
                    dcof.write(str(datacard.shape_uncertainties[cat][sample][shape]))
                else:
                    dcof.write("-")
                dcof.write("\t")
        dcof.write("\n")
            
    dcof.write("# Execute with:\n")
    dcof.write("# combine -M Asymptotic -t -1 {0} \n".format(dcof_name))
    
# end of PrintDataCard


if __name__ == "__main__":


    # Get the input proto-datacard
    datacard_path = sys.argv[1]
    dcard = imp.load_source("dcard", datacard_path)

    # Create the output directory
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    full_path = os.path.join(dcard.Datacard.output_basepath, "Datacard-" + timestamp)
    os.makedirs(full_path)

    # output root file
    of_name = os.path.join(full_path, dcard.Datacard.output_filename)
    of = ROOT.TFile(of_name, "RECREATE")
    # output datacard text file
    dcof_name = os.path.join(full_path, dcard.Datacard.output_datacardname)
    dcof = open(dcof_name, "w")

    # dict of dicts. First key: sample Second key: cut
    # Content: events at given lumi
    event_counts = {}

    for sample in dcard.Datacard.samples:
        print sample

        sample_shortname = samples_dict[sample].name

        event_counts[sample_shortname] = {}

        tf = ROOT.TChain("tree")
        for fn in samples_dict[sample].fileNamesS2:
            
            if not os.path.isfile(fn):
                raise Exception("could not open ROOT file: {0}".format(fn))
            tf.AddFile(fn)        
        print "Read ", tf.GetEntries(), "entries"

        of.cd()
        
        sampled = of.mkdir(sample_shortname)
        sampled.cd()

        for cutname, cut, analysis_var in dcard.Datacard.categories:
            
            print "cut:", cutname

            jetd = sampled.mkdir(cutname)
            
            #Draw(tf, jetd, gensyst, "nBCSVM:numJets >> njets_ntags(15,0,15,15,0,15)", cut)

            Draw(tf, jetd, gensyst, "jets_pt[0] >> jet0_pt(20,20,500)", cut)
            Draw(tf, jetd, gensyst, "jets_pt[1] >> jet1_pt(20,20,500)", cut)

            #Draw(tf, jetd, gensyst, "jets_eta[0] >> jet0_eta(30,-5,5)", cut)

            Draw(tf, jetd, gensyst, "jets_btagCSV[0] >> jet0_csvv2(22, -0.1, 1)", cut)
        
            #Draw(tf, jetd, gensyst, "leps_pt[0] >> lep0_pt(30,0,300)", cut)
            #Draw(tf, jetd, gensyst, "leps_eta[0] >> lep0_eta(30,-5,5)", cut)
        
            #Draw(tf, jetd, gensyst, "btag_LR_4b_2b >> btag_lr(30,0,1)", cut)
            # 
            # Draw(tf, jetd, gensyst, "(100*nMatch_wq + 10*nMatch_hb + nMatch_tb) >> nMatch(300,0,300)", cut)
            # Draw(tf, jetd, gensyst, "(100*nMatch_wq_btag + 10*nMatch_hb_btag + nMatch_tb_btag) >> nMatch_btag(300,0,300)", cut)
            #

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

                    Draw(tf, jetd, gensyst,
                        "mem_tth_p[{0}] / (mem_tth_p[{0}] + 0.15*mem_ttbb_p[{0}]) >> mem_{1}{2}(12,0,1)".format(
                            memidx, memname, matchname
                        ),
                        cut
                    )
                    
            event_counts[sample_shortname][cutname] = jetd.Get(analysis_var).Integral()
            
            jetd.Write()

            
        sampled.Write()
    # End of loop over samples

    print "writing"
    of.Write()
    of.Close()

    PrintDatacard(event_counts, dcard.Datacard, dcof)
