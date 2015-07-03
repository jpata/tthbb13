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
    from TTH.Plotting.gregor.TopSamples import files, ranges, fiducial_cuts, pretty_fiducial_cuts
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCs
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import files, ranges, fiducial_cuts, pretty_fiducial_cuts


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

DRAW_ROC = True


pairs = { 
    "pt-300-to-470" : ["zprime_m1000", "qcd_300_470"]
}

for pair_name, pair in pairs.iteritems():
    sample_sig = pair[0]
    sample_bkg = pair[1]

    basepath = '/scratch/gregor/'
    file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
    file_name_bkg  = basepath + files[sample_bkg] + "-weighted.root"

    li_methods      = ["Cuts"]

    fj_size = ranges[pair[0]][4]
    
    setups = []                

    btag_vars = ["ca15trimmedr2f3forbtag_btag",
                 "ca15softdropz10b00forbtag_btag",
                 "ca15softdropz20b10forbtag_btag",
                 "ca15filteredn3r2forbtag_btag",
                 "ca15prunedn3z10rfac50forbtag_btag"]
    
    for btag_var in btag_vars:

        mass_var =  "ca15softdropz20b10_mass"
        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_150_240_tau_btag_" + btag_var),
                          "#tau_{3}/#tau_{2} + b-tag " + variable.di[btag_var].pretty_name,
                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
                          [variable.di['ca15_tau3/ca15_tau2'], 
                           variable.di[btag_var]],
                          [],
                          file_name_sig,
                          file_name_bkg,
                          fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
                          fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
                          extra_cut = "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240))",
                          weight_sig = "(1)",
                          weight_bkg = "(1)",
                          draw_roc = DRAW_ROC,
                          working_points = [],
                          manual_working_points = [])
        setups.append(setup)

    #pool.map(doTMVA, setups)
    plotROCs("real_btag_tau_ROC_" + pair_name, setups)             

