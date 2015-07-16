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
files["zprime_m2000"]     = "ntop_v58_zprime_m2000_1p_13tev_spring15dr74_asympt25ns-tagging"	
files["qcd_800_1000"]     = "ntop_v58_qcd_800_1000_13tev_spring15dr74_asympt25ns-tagging" 
files["zprime_m2000_60"]  = "ntop_v60_zprime_m2000_1p_13tev_spring15dr74_asympt25ns-tagging"	
files["qcd_800_1000_60"]  = "ntop_v60_qcd_800_1000_13tev_spring15dr74_asympt25ns-tagging" 
files["zprime_m2000_60a"] = "ntop_v60a_zprime_m2000_1p_13tev_spring15dr74_asympt25ns-tagging"	
files["qcd_800_1000_60a"] = "ntop_v60a_qcd_800_1000_13tev_spring15dr74_asympt25ns-tagging"
files["zprime_m2000_60b"] = "ntop_v60b_zprime_m2000_1p_13tev_spring15dr74_asympt25ns-tagging"	
files["qcd_800_1000_60b"] = "ntop_v60b_qcd_800_1000_13tev_spring15dr74_asympt25ns-tagging" 
files["zprime_m2000_60c"] = "ntop_v60c_zprime_m2000_1p_13tev_spring15dr74_asympt25ns-tagging"	
files["qcd_800_1000_60c"] = "ntop_v60c_qcd_800_1000_13tev_spring15dr74_asympt25ns-tagging" 
files["zprime_m2000_60d"] = "ntop_v60d_zprime_m2000_1p_13tev_spring15dr74_asympt25ns-tagging"	
files["qcd_800_1000_60d"] = "ntop_v60d_qcd_800_1000_13tev_spring15dr74_asympt25ns-tagging" 


pairs = { 
    "pt-800-to-1000-v58"  : ["zprime_m2000", "qcd_800_1000"],
#    "pt-800-to-1000-v60"  : ["zprime_m2000_60",  "qcd_800_1000_60"],
    "pt-800-to-1000-v60a" : ["zprime_m2000_60a", "qcd_800_1000_60a"],
#    "pt-800-to-1000-v60b" : ["zprime_m2000_60b", "qcd_800_1000_60b"],
    "pt-800-to-1000-v60c" : ["zprime_m2000_60c", "qcd_800_1000_60c"],
    "pt-800-to-1000-v60d" : ["zprime_m2000_60c", "qcd_800_1000_60d"],
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

fiducial_cuts_signal = fiducial_cuts["zprime_m2000"]
fiducial_cuts_background = fiducial_cuts["qcd_800_1000"]

setups = []

for pair_name, pair in pairs.iteritems():
    sample_sig = pair[0]
    sample_bkg = pair[1]

    basepath = '/scratch/gregor/'
    file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
    file_name_bkg  = basepath + files[sample_bkg] + "-weighted.root"

    for var in ["log(ak08_chi1)", "log(ak08_chi2)"]:
        setup = TMVASetup("{0}_{1}_{2}_SDtruth".format(sample_sig, sample_bkg, var),
                          pair_name + " " + var,
                          [["Cuts", "V:FitMethod=MC:SampleSize=100000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=10"]], 
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
plotROCs("SDtruth_ROC_800_1000" , setups)        




