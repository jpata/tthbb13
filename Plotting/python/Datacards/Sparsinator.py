#!/usr/bin/env python
"""
Sparsinator: Loop over trees containing MEM result and project them
into N-dimensional (sparse) histograms.

Careful - broken with some ROOT versions (like 6.02/5). This one works fine:
. /afs/cern.ch/sw/lcg/external/gcc/4.9/x86_64-slc6-gcc49-opt/setup.sh
. /afs/cern.ch/sw/lcg/app/releases/ROOT/6.05.02/x86_64-slc6-gcc49-opt/root/bin/thisroot.sh
"""

########################################
# Imports
########################################

import os      
import array   
import sys     
import imp     
import random
import datetime
import pickle

import ROOT

from MiniSamples import samples_dict


########################################
# Configuration
########################################

max_entries = -1

lumi = 10000 # 10 fb-1 in pb

samples = [
#    "ttH_hbb",
#    "ttH_nohbb",
    "ttbarPlus2B",
    "ttbarPlusB",
    "ttbarPlusBBbar",
    "ttbarPlusCCbar",
    "ttbarOther",
    "ttw_wlnu",       
    "ttw_wqq",        
    "ttz_zllnunu",    
    "ttz_zqq",
]        



# Helper function to calculate the MEM        
                 
def calc_mem(t):
    mem_tth_p  = getattr(t, "mem_tth_p")
    mem_ttbb_p = getattr(t, "mem_ttbb_p")
                    
    denom = mem_tth_p[5] + 0.15 * mem_ttbb_p[5]
    if denom == 0:
        mem = 0
    else:
        mem = mem_tth_p[5] / (mem_tth_p[5] + 0.15 * mem_ttbb_p[5])
    return mem
# end of calc_mem


########################################
# Axes
########################################

class axis:
    def __init__(self,
                 nbins,
                 xmin,
                 xmax,
                 fun,
                 addUnderflow,
                 addOverflow):
        """" Defines an axis for a multi-dimensional histogram
        nbins        : number of bins
        xmin         : lower boundary of axis
        xmax         : upper boundary of axis
        fun          : function to evaluate, will receive a TTree as argument
        addUnderflow : if True - put values into lowest bin instead of underflow
        addOverflow  : if True - put values into highest bin instead of overflow
        """

        self.nbins        = nbins
        self.xmin         = xmin
        self.xmax         = xmax
        self.fun          = fun
        self.addUnderflow = addUnderflow
        self.addOverflow  = addOverflow
# end of class axis        


########################################
# Sparsinate
########################################

def sparsinate(samples):

    # Define the axes
    axes = [ 
        axis(20, 0, 1, calc_mem, 1, 1),
        axis(3,  3.5, 6.5, lambda t : getattr(t, "numJets"), 0, 1),
        axis(3, 1.5, 4.5,  lambda t : getattr(t, "nBCSVM"), 0, 1)
    ]

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    outdir = "/scratch/gregor/SparseMEM_{0}".format(timestamp)
    os.makedirs(outdir)

    for sample_shortname in samples:

        fn = samples_dict[sample_shortname]

        # Open input
        f = ROOT.TFile.Open(fn)
        t = f.Get("tree")

        # Open Output and construct histogram
        of = ROOT.TFile("{0}/{1}.root".format(outdir, sample_shortname), "recreate")
        bins = array.array('i',[a.nbins for a in axes])
        xmin = array.array('d',[a.xmin  for a in axes])
        xmax = array.array('d',[a.xmax  for a in axes])
        h = ROOT.THnSparseF("foo", "foo", len(axes), bins, xmin, xmax)


        form_basic_cut = ROOT.TTreeFormula("basic_cut", 
                                      "is_sl && passPV && (HLT_BIT_HLT_Ele27_eta2p1_WP85_Gsf_HT200_v || HLT_BIT_HLT_IsoMu24_eta2p1_v) && btag_LR_4b_2b > 0.95", 
                                      t)
        form_weight = ROOT.TTreeFormula("weight", "weight_xs * bTagWeight * {0}".format(lumi), t)

        print "Entries in file:", t.GetEntries()
        if max_entries == -1:
            process_entries = t.GetEntries()
        else:
            process_entries = max_entries

        # Begin Event Loop
        for i_ev in xrange(process_entries):

            t.GetEntry( i_ev )

            # Update every 1%
            if not i_ev % int(process_entries / 100.):
                print "{0:.1f}% ({1} out of {2})".format(
                    100.*i_ev/process_entries, i_ev, process_entries)

            if form_basic_cut.EvalInstance():

                to_fill = []

                for a in axes:

                    v = a.fun(t)

                    if v < a.xmin and a.addUnderflow:
                        v = a.xmin + (a.xmax-a.xmin)/(4 * a.nbins)
                    if v > a.xmax and a.addOverflow:
                        v = a.xmax - (a.xmax-a.xmin)/(4 * a.nbins)

                    to_fill.append(v)
                # End axes loop

                h.Fill(array.array("d",to_fill),
                       form_weight.EvalInstance())

            # End passed basic selection                
        # End event loop

        f.Close()
        h.Write()

    # End loop over samples                
# End of sparsinate

if __name__ == "__main__":
    
    ROOT.gROOT.SetBatch(True)
    sparsinate(samples)

