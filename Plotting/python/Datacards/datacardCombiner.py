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
def makeStatVariations(tf, of, categories): 
    for cat in categories:
        for proc in cat.processes:
            hn = "{0}/{1}/{2}".format(proc, cat.name, cat.discriminator)
            h = tf.Get(hn)
            h = h.Clone()
            outdir = "{0}/{1}".format(proc, cat.name)
            if of.Get(outdir) == None:
                of.mkdir(outdir)
            outdir = of.Get(outdir)
            for ibin in range(1, h.GetNbinsX() + 1):
                for sigma, sdir in [(+1, "Up"), (-1, "Down")]:
                    outdir.cd()
                    hvar = h.Clone(h.GetName() + "_{0}_{1}_Bin{2}{3}".format(proc, cat.name, ibin, sdir))
                    delta = hvar.GetBinError(ibin)
                    c = hvar.GetBinContent(ibin) + sigma*delta
                    if c <= 10**-5 and h.Integral() > 0:
                        c = 10**-5
                    hvar.SetBinContent(ibin, c)
                    outdir.Add(hvar)
                    hvar.Write("", ROOT.TObject.kOverwrite)

########################################
# Create fake data
########################################
def fakeData(infile, outfile, categories):
    dircache = {}
    for cat in categories:
        h = infile.Get("{0}/{1}/{2}".format(cat.processes[0], cat.name, cat.discriminator)).Clone()
        for proc in cat.processes[1:]:
            h2 = infile.Get("{0}/{1}/{2}".format(proc, cat.name, cat.discriminator))
            h.Add(h2)

        outdir = "data_obs/{0}".format(cat.name)
        dircache[outdir] = h 

    # End of loop over categories
    for (k, v) in dircache.items():
        if outfile.Get(k) == None:
            outfile.mkdir(k)
        k = outfile.Get(k)
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
