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
        return ROOT.TH1D("mem", "mem", 12, 0, 1)
    elif hname.startswith("jet0_pt"):
        return ROOT.TH1D("pt", "pt", 20, 0, 500)
    return None



########################################
# Copy existing, needed histograms
#  into new file 
########################################
def copyHistograms(tf, of, hists, channels, processes): 
    #print "Copying existing histograms..."
    
    for hist in hists:
        for ch in channels:
            for proc in processes:
    
                h = tf.Get("{0}/{1}/{2}".format(proc, ch, hist)).Clone()
                outdir = "{0}/{1}".format(proc, ch)
                if of.Get(outdir) == None:
                    of.mkdir(outdir)
                outdir = of.Get(outdir)
                h.SetDirectory(outdir)
                outdir.Write()
    
            # End of loop over processes
        # End of loop over channels
    # End of loop over histograms
    
    print "Done."


########################################
# Create fake data
########################################
def fakeData(tf, of, hists, channels, processes):
    print "Creating fake data..."
    
    for hist in hists:
        #print " hist=", hist
        for ch in channels:
            #print "  channel=", ch
            h = None
            for proc in processes:
                #print "   proc=", proc

                h2 = tf.Get("{0}/{1}/{2}".format(proc, ch, hist))
                if h2:
                    if not h:
                        h = h2.Clone()
                    else:
                        h.Add(h2)
            if h == None:
                h = defaultHistogram(hist)

            outdir = "data_obs/{0}".format(ch)
            if of.Get(outdir) == None:
                of.mkdir(outdir)
            outdir = of.Get(outdir)
            h.SetDirectory(outdir)
            outdir.Write()
        # End of loop over channels
    # End of loop over histograms
    
    print "Done."


########################################
# Combine categories
########################################

def combineCategories(tf, of, hists, mergers, processes):
    #print "Combining categories..."
    
    for hist in hists:
        for proc in processes:
            #print " combining", hist, proc
            for name, channels in mergers.iteritems():
                #print "  {0} <= {1}".format(name, channels)
                h = None
    
                for ch in channels:
                    hn = "{0}/{1}/{2}".format(proc, ch, hist)
                    h2 = tf.Get(hn)
                    if h2:
                        if not h:
                            h = h2.Clone()
                        else:
                            h.Add(h2)
                if h == None:
                    h = defaultHistogram(hist)

                #it can happen that no category had this histogram defined
                
                if h == None:
                    h = defaultHistogram(hist)
                outdir = "{0}/{1}".format(proc,name)
                if of.Get(outdir) == None:
                    of.mkdir(outdir)
                outdir = of.Get(outdir)
                h.SetDirectory(outdir)
                outdir.Write()
            # End of loop over things to merge
         # End of loop over processes
    # End of loop over histograms
    
    print "Done."

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
