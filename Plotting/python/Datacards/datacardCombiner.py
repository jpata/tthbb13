#!/usr/bin/env python
"""
Combine datacards across categories.
Also Create the FakeData file
"""

########################################
# Imports
########################################

import ROOT
import sys

def defaultHistogram(hname):
    """
    In case a histogram was not found for a specific cut, we need to provide a default 0-histogram.
    """
    if hname.startswith("mem_"):
        return ROOT.TH1D(hname, "mem", 6, 0, 1)
    elif hname.startswith("jet0_pt"):
        return ROOT.TH1D(hname, "pt", 20, 0, 500)
    raise Exception("Undefined default histogram {0}".format(hname))



########################################
# Copy existing, needed histograms
#  into new file 
########################################
def copyHistograms(tf, of, hists, channels, processes): 
    #print "Copying existing histograms..."
    
    #print "copying", processes, channels, hists
    for hist in hists:
        for ch in channels:
            for proc in processes:
    
                h = tf.Get("{0}/{1}/{2}".format(proc, ch, hist))
                if h == None:
                    h = defaultHistogram(hist)
                h = h.Clone()
                outdir = "{0}/{1}".format(proc, ch)
                if of.Get(outdir) == None:
                    of.mkdir(outdir)
                outdir = of.Get(outdir)
                #outdir.Add(h)
                #h.Write("", ROOT.TObject.kOverwrite)
                h.SetDirectory(outdir)
                #h.Write()
                outdir.Write("", ROOT.TObject.kOverwrite)
    
            # End of loop over processes
        # End of loop over channels
    # End of loop over histograms

########################################
# Copy existing, needed histograms
#  into new file 
########################################
def makeStatVariations(tf, of, hists, channels, processes): 
    #print "Copying existing histograms..."
    
    for proc in processes:
        for hist in hists:
            for ch in channels:
                hn = "{0}/{1}/{2}".format(proc, ch, hist)
                h = tf.Get(hn)
                if not h:
                    h = defaultHistogram(hist)
                h = h.Clone()
                outdir = "{0}/{1}".format(proc, ch)
                if of.Get(outdir) == None:
                    of.mkdir(outdir)
                outdir = of.Get(outdir)
                for ibin in range(1, h.GetNbinsX() + 1):
                    for sigma, sdir in [(+1, "Up"), (-1, "Down")]:
                        outdir.cd()
                        hvar = h.Clone(h.GetName() + "_{0}_{1}_Bin{2}{3}".format(proc, ch, ibin, sdir))
                        delta = hvar.GetBinError(ibin)
                        c = hvar.GetBinContent(ibin) + sigma*delta
                        if c <= 10**-5 and h.Integral()>0:
                            c = 10**-5
                        hvar.SetBinContent(ibin, c)
                        outdir.Add(hvar)
                        hvar.Write("", ROOT.TObject.kOverwrite)
                        #outdir.Write("", ROOT.TObject.kOverwrite)
    
            # End of loop over processes
        # End of loop over channels
    # End of loop over histograms

########################################
# Create fake data
########################################
def fakeData(tf, of, hists, channels, processes):
    dircache = {}
    for hist in hists:
        for ch in channels:
            h = tf.Get("{0}/{1}/{2}".format(processes[0], ch, hist)).Clone()
            for proc in processes[1:]:
                h2 = tf.Get("{0}/{1}/{2}".format(proc, ch, hist))
                h.Add(h2)
    
            outdir = "data_obs/{0}".format(ch)
            dircache[outdir] = h 

        # End of loop over channels
    # End of loop over histograms
    for (k, v) in dircache.items():
        if of.Get(k) == None:
            of.mkdir(k)
        k = of.Get(k)
        #outdir.Add(h)
        #h.Write("", ROOT.TObject.kOverwrite)
        v.SetDirectory(k)
        k.Write("", ROOT.TObject.kOverwrite)

########################################
# Combine categories
########################################

def combineCategories(tf, of, hists, mergers, processes):
    #print "Combining categories...", tf, of
    
    for hist in hists:
        for proc in processes:
            #print " combining", hist, proc
            for name, channels in mergers.iteritems():
                h = None
    
                for ch in channels:
                    hn = "{0}/{1}/{2}".format(proc, ch, hist)
                    h2 = tf.Get(hn)
                    if h2:
                        if not h:
                            h = h2.Clone()
                        else:
                            h.Add(h2)
                    else:
                        #print "could not find", hn, tf
                        pass
                #it can happen that no category had this histogram defined
                if h == None:
                    h = defaultHistogram(hist)
                outdir = "{0}/{1}".format(proc,name)
                if of.Get(outdir) == None:
                    of.mkdir(outdir)
                outdir = of.Get(outdir)
                #outdir.Add(h)
                #h.Write("", ROOT.TObject.kOverwrite)
                h.SetDirectory(outdir)
                outdir.Write("", ROOT.TObject.kOverwrite)
            # End of loop over things to merge
         # End of loop over processes
    # End of loop over histograms

if __name__ == "__main__":
    inf = sys.argv[1]
    tf = ROOT.TFile(inf)
    
    ########################################
    # Configuration
    ########################################
    
    processes = [
        "ttbarPlus2B",
        "ttbarPlusB",
        "ttbarPlusBBbar",
        "ttbarPlusCCbar",
        "ttbarOther",
    ]
    
    channels = [
        "sl_jge6_tge4"
    ]
    
    hists = [
        "mem_SL_0w2h2t"
    ]
    
    mergers = {
        "sl_jge6_tge3" : ["sl_jge6_t3", "sl_jge6_tge4"]
    }
    
    of = ROOT.TFile("combinedDatacards.root", "RECREATE")
    copyHistograms(tf, of, hists, channels, processes)
    fakeData(tf, of, hists, channels, processes)
    combineCategories(tf, of, hists, mergers, processes)
