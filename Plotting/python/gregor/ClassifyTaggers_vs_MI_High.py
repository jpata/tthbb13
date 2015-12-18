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

    single_setups = []
    double_setups = []

    
    interesting_vars = [
        ["log(ak08_chi2)", "CutRangeMin[0]=-10:CutRangeMax[0]=10:VarProp[0]=FSmart"],
        #["ak08softdropz10b00forbtag_btag", "CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"],
        ["ak08trimmedr2f3_mass",       "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        ["looseOptRHTT_mass", "CutRangeMin[0]=0:CutRangeMax[0]=150"                      ],
        ["ak08softdropz20b10_mass",    "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        #["looseOptRHTT_Ropt-looseOptRHTT_RoptCalc", "CutRangeMin[0]=-0.8:CutRangeMax[0]=0.5"],
        ["ak08filteredn3r2_mass",      "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        ["looseOptRHTT_fRec", "CutRangeMin[0]=0:CutRangeMax[0]=0.5"                      ],
        ["ak08_qvol", "CutRangeMin[0]=0:CutRangeMax[0]=1"],
        ["ak08softdropz10b00_mass",    "CutRangeMin[0]=0:CutRangeMax[0]=250"], 
        ["ak08prunedn3z10rfac50_mass", "CutRangeMin[0]=0:CutRangeMax[0]=250"],
        ["ak08_tau3/ak08_tau2", "CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"],
        ["ak08cmstt_minMass", "CutRangeMin[0]=0:CutRangeMax[0]=150"],
        ["ak08cmstt_topMass", "CutRangeMin[0]=0:CutRangeMax[0]=300"],            
    ]
    
    for var, extra in interesting_vars:
    
        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, var.replace("/","_")),
                                         variable.di[var].pretty_name.replace("Mass", "m"),
                                        # [["Likelihood","V"]], 
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


    for i_var_1 in range(len(interesting_vars)):
        for i_var_2 in range(len(interesting_vars)):
            
            if i_var_1 >= i_var_2:
                continue

            var_1, extra_1 = interesting_vars[i_var_1]
            var_2, extra_2 = interesting_vars[i_var_2]

            setup = TMVASetup("{0}_{1}_{2}_{3}_vsMI".format(sample_sig, sample_bkg, var_1.replace("/","_"), var_2.replace("/","_")),
                              variable.di[var_1].pretty_name.replace("Mass", "m").replace("Mass", "m") + " " + variable.di[var_2].pretty_name.replace("Mass", "m").replace("Mass", "m"),
                              #[["Likelihood", "V"]], 
                              [["BDT", "NTrees=1000:MaxDepth=3:BoostType=Grad:Shrinkage=0.3"]], 
                              [variable.di[var_1],
                               variable.di[var_2],
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

            
            double_setups.append(setup)



#    plotROCs("fixedR_MI_ROC_" + pair_name, single_setups, 
#                 extra_text = [pretty_fiducial_cuts[sample_sig],
#                               "flat p_{T} and #eta",
#                               "#Delta R(top,parton) < 0.6"],
#                 error_band = False)
#


    # fixedR_MI_ROC_high_LikBDT_ Diagonal: Likelihood, Off-Diagonal: BDT NTrees=100:MaxDepth=3
    # fixedR_MI_ROC_high_testLikBDT2_ Diagonal: Likelihood, Off-Diagonal: BDT NTrees=1000:MaxDepth=3:BoostType=Grad:Shrinkage=0.3

    #pool.map(doTMVA, single_setups + double_setups)
    #plotROCs("fixedR_MI_ROC_high_TestLikBDT4_" + pair_name, single_setups + double_setups, error_band = False)        



    plotROCs("MI_ROCcut_high_single_" + pair_name, 
             single_setups, 
             extra_text = [pretty_fiducial_cuts[sample_sig],
                           "#DeltaR(top,parton) < 0.6",
                           "flat p_{T} and #eta"],
             error_band = False
         )        




