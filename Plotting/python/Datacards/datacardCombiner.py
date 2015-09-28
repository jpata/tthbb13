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

########################################
# Copy existing, needed histograms
#  into new file 
########################################
def copyHistograms(of, hists, channels, processes): 
    print "Copying existing histograms..."
    
    for hist in hists:
        for ch in channels:
            for proc in processes:
    
                h = tf.Get("{0}/{1}/{2}".format(proc, ch, hist)).Clone()
                outdir = "{0}/{1}".format(proc, ch)
                of.mkdir(outdir)
                outdir = of.Get(outdir)
                h.SetDirectory(outdir)
                of.Write()
    
            # End of loop over processes
        # End of loop over channels
    # End of loop over histograms
    
    print "Done."


########################################
# Create fake data
########################################
def fakeData(of, hists, channels, processes):
    print "Creating fake data..."
    
    for hist in hists:
        for ch in channels:
            h = None
            for proc in processes:
    
                h2 = tf.Get("{0}/{1}/{2}".format(proc, ch, hist))
                if not h:
                    h = h2.Clone()
                else:
                    h.Add(h2)
            outdir = "data_obs/{0}".format(ch)
            of.mkdir(outdir)
            outdir = of.Get(outdir)
            h.SetDirectory(outdir)
            of.Write()
        # End of loop over channels
    # End of loop over histograms
    
    print "Done."


########################################
# Combine categories
########################################

def combineCategories(of, hists, channels, processes):
    print "Combining categories..."
    
    for hist in hists:
        for proc in processes:
            for name, channels in mergers.iteritems():
            
                h = None
    
                for ch in channels:
    
                    h2 = tf.Get("{0}/{1}/{2}".format(proc, ch, hist))
                    if not h:
                        h = h2.Clone()
                    else:
                        h.Add(h2)
    
                outdir = "{0}/{1}".format(proc,name)
                of.mkdir(outdir)
                outdir = of.Get(outdir)
                h.SetDirectory(outdir)
                of.Write()
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
    copyHistograms(of, hists, channels, processes)
    fakeData(of, hists, channels, processes)
    combineCategories(of, hists, channels, processes)
