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
    from TTH.Plotting.gregor.TopSamples import files, ranges, fiducial_cuts, pretty_fiducial_cuts, pairs
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCs
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import files, ranges, fiducial_cuts, pretty_fiducial_cuts, pairs


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

for pair_name, pair in pairs.iteritems():
    sample_sig = pair[0]
    sample_bkg = pair[1]

    basepath = '/scratch/gregor/'
    file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
    file_name_bkg  = basepath + files[sample_bkg] + "-weighted.root"

    li_methods      = ["Cuts"]

    single_setups = []
    tau_setups = []
            

    # Low pT, multiple variables
    
    interesting_vars = [
        ["log(ca15_chi3)", "CutRangeMin[0]=-10:CutRangeMax[0]=10:VarProp[0]=FSmart"],
        ["ca15trimmedr2f3_mass",       "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        ["looseOptRHTT_mass", "CutRangeMin[0]=0:CutRangeMax[0]=150"                      ],
        ["ca15softdropz20b10_mass",    "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        ["looseOptRHTT_Ropt-looseOptRHTT_RoptCalc", "CutRangeMin[0]=-0.8:CutRangeMax[0]=0.5"],
        ["ca15filteredn3r2_mass",      "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        ["looseOptRHTT_fRec", "CutRangeMin[0]=0:CutRangeMax[0]=0.5"                      ],
        ["ca15_qvol", "CutRangeMin[0]=0:CutRangeMax[0]=1"],
        ["ca15softdropz10b00_mass",    "CutRangeMin[0]=0:CutRangeMax[0]=250"], 
        ["ca15prunedn3z10rfac50_mass", "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        ["ca15_tau3/ca15_tau2", "CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"],
        
        #["ca15_mass", "CutRangeMin[0]=0:CutRangeMax[0]=300"],        
    
    ]
    
    for var, extra in interesting_vars:
    
        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, var.replace("/","_")),
                                         variable.di[var].pretty_name,
                                         [["Cuts", "V:FitMethod=MC:SampleSize=400000:Sigma=0.3:"+extra]], 
                                         [variable.di[var]],
                                         [],
                                         file_name_sig,
                                         file_name_bkg,
                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                                         weight_sig = "weight",
                                         weight_bkg = "weight",
                                         draw_roc = DRAW_ROC,
                                         working_points = [],
                                         manual_working_points = [])
        single_setups.append(setup)

    
    # Low pT, multiple variables
     
    interesting_vars = [
        ["ca15trimmedr2f3_mass",       "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        ["ca15softdropz10b00_mass",    "CutRangeMin[0]=0:CutRangeMax[0]=250"], 
        ["ca15softdropz20b10_mass",    "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        ["ca15filteredn3r2_mass",      "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        ["ca15prunedn3z10rfac50_mass", "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        ["ca15_mass", "CutRangeMin[0]=0:CutRangeMax[0]=300"],             
    ]
     
    for var, extra in interesting_vars:
        
        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, var.replace("/","_"))+"_tau",
                          variable.di[var].pretty_name,
                          [["Cuts", "V:FitMethod=MC:SampleSize=400000:Sigma=0.3:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart:"+extra]], 
                          [variable.di[var],
                           variable.di["ca15_tau3/ca15_tau2"],                           
                       ],
                          [],
                          file_name_sig,
                          file_name_bkg,
                          fiducial_cut_sig = fiducial_cuts[sample_sig],
                          fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                          weight_sig = "weight",
                          weight_bkg = "weight",
                          draw_roc = DRAW_ROC,
                          working_points = [],
                          manual_working_points = [])
        tau_setups.append(setup)
        

       
    #pool.map(doTMVA, single_setups)
    plotROCs("MI_ROC_" + pair_name, single_setups, extra_text = pretty_fiducial_cuts[sample_sig])        

    #pool.map(doTMVA, tau_setups)
    plotROCs("MI_ROCtau_" + pair_name, tau_setups, extra_text = pretty_fiducial_cuts[sample_sig])        




