#!/usr/bin/env python
"""
Schedule the testing of different variable/method-sets with TMVA
"""

########################################
# Imports 
########################################

import pickle
import os
from copy import deepcopy
import multiprocessing as mp

import ROOT

# Our support Code
# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCs
    from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import fiducial_cuts
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCs
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import fiducial_cuts

files = {}
files["zprime_m1000"]    = "ntop_v58a_zprime_m1000_1p_13tev_spring15dr74_asympt25ns-tagging"	
files["qcd_300_470"]     = "ntop_v58a_qcd_300_470_13tev_spring15dr74_asympt25ns-tagging" 
files["zprime_m1000_61"] = "ntop_v61_zprime_m1000_1p_13tev_spring15dr74_asympt25ns-tagging"	
files["qcd_300_470_61"]  = "ntop_v61_qcd_300_470_13tev_spring15dr74_asympt25ns-tagging" 

pairs = { 
    "pt-300-to-470-v58"  : ["zprime_m1000", "qcd_300_470"],
    "pt-300-to-470-v61"  : ["zprime_m1000_61", "qcd_300_470_61"],
}

myStyle.SetTitleXOffset(1.3)
myStyle.SetTitleYOffset(1.7)
myStyle.SetPadLeftMargin(0.19)
myStyle.SetPadBottomMargin(0.13)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()

pool = mp.Pool(processes=12)  

########################################
# Configuration
########################################

fiducial_cuts_signal = fiducial_cuts["zprime_m1000"]
fiducial_cuts_background = fiducial_cuts["qcd_300_470"]

setups = []

for pair_name, pair in pairs.iteritems():
    sample_sig = pair[0]
    sample_bkg = pair[1]

    basepath = '/scratch/gregor/'
    file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
    file_name_bkg  = basepath + files[sample_bkg] + "-weighted.root"

    for var in ["log(ca15_chi1)", "log(ca15_chi2)", "log(ca15_chi3)"]:
        setup = TMVASetup("{0}_{1}_{2}_SDtruth".format(sample_sig, sample_bkg, var),
                          pair_name + " " + var,
                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=10"]], 
                          [variable.di[var]],
                          [],
                          file_name_sig,
                          file_name_bkg,
                          fiducial_cut_sig = fiducial_cuts_signal,
                          fiducial_cut_bkg = fiducial_cuts_background,
                          weight_sig = "weight",
                          weight_bkg = "weight",
                          draw_roc = True,
                          working_points = [],
                          manual_working_points = [])
        setups.append(setup)
    
pool.map(doTMVA, setups)
plotROCs("SDtruth_ROC_300_470" , setups)        




