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

    htt_truth_setups = []
    truth_setups = []
    trimmed_truth_setups = []
    only_size_setups = []
            
    gg_truth_setups = []
    ug_truth_setups = []
    gu_truth_setups = []

    best_setup = None
    
    groomers = [
        "ca15",
        "ca15filteredn3r2",
        "ca15prunedn3z10rfac50",
        "ca15trimmedr2f3",
        "ca15softdropz10b00",
        "ca15softdropz20b10",
    ]

    for groomer in groomers:
        
        if groomer == "ca15":
            vars = ["{0}_tau3/{0}_tau2".format(groomer)]
        else:
            vars = ["{0}_tau3/{0}_tau2".format(groomer), "ca15_tau3/{0}_tau2".format(groomer), "{0}_tau3/ca15_tau2".format(groomer)]

        for var, setups  in zip(vars, [gg_truth_setups, ug_truth_setups, gu_truth_setups]):                                
            setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, var.replace("/","_")+"_massWindow"),
                              variable.di[var].pretty_name,
                              # !!!! 8 only set for UG-truth
                              [["Cuts", "V:FitMethod=MC:SampleSize=400000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=4:VarProp[0]=FSmart"]], 
                              [variable.di[var]],
                              [],
                              file_name_sig,
                              file_name_bkg,
                              fiducial_cut_sig = fiducial_cuts[sample_sig],
                              fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                              extra_cut = "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240))",
                              weight_sig = "weight",
                              weight_bkg = "weight",
                              draw_roc = DRAW_ROC,
                              working_points = [],
                              manual_working_points = [])
            setups.append(setup)
            
            if var == "ca15softdropz20b10_tau3/ca15softdropz20b10_tau2":
                best_setup = setup


        var = "{0}_tau3/{0}_tau2".format(groomer)
        
        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, var.replace("/","_")+"_Trimmedr2f3massWindow"),
                          variable.di[var].pretty_name,
                          [["Cuts", "V:FitMethod=MC:SampleSize=400000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
                          [variable.di[var]],
                          [],
                          file_name_sig,
                          file_name_bkg,
                          fiducial_cut_sig = fiducial_cuts[sample_sig],
                          fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                          extra_cut = "((ca15trimmedr2f3_mass>120)&&(ca15trimmedr2f3_mass<190))",
                          weight_sig = "weight",
                          weight_bkg = "weight",
                          draw_roc = DRAW_ROC,
                          working_points = [],
                          manual_working_points = [])
        trimmed_truth_setups.append(setup)

        #
        #setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, var.replace("/","_")+"_massWindow_onlySize"),
        #                  variable.di[var].pretty_name,
        #                  [["Cuts", "V:FitMethod=MC:SampleSize=400000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
        #                  [variable.di[var]],
        #                  [],
        #                  file_name_sig,
        #                  file_name_bkg,
        #                  fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
        #                  fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
        #                  extra_cut = "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240))",
        #                  weight_sig = "(1)",
        #                  weight_bkg = "(1)",
        #                  draw_roc = DRAW_ROC,
        #                  working_points = [],
        #                  manual_working_points = [])
        #only_size_setups.append(setup)
         
        #setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, var.replace("/","_")+"_HTTmassWindow"),
        #                  variable.di[var].pretty_name,
        #                  [["Cuts", "V:FitMethod=MC:SampleSize=500000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart:VarProp[1]=FSmart:CutRangeMin[1]=0:CutRangeMax[1]=0.5"]], 
        #                  [variable.di[var],
        #                   variable.di['looseOptRHTT_fRec'],
        #               ],
        #                  [],
        #                  file_name_sig,
        #                  file_name_bkg,
        #                  fiducial_cut_sig = fiducial_cuts[sample_sig],
        #                  fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
        #                  extra_cut = "((looseOptRHTT_mass>140)&&(looseOptRHTT_mass<190))",
        #                  weight_sig = "weight",
        #                  weight_bkg = "weight",
        #                  draw_roc = DRAW_ROC,
        #                  working_points = [],
        #                  manual_working_points = [])
        #htt_truth_setups.append(setup)
        


    

    pool.map(doTMVA, ug_truth_setups)
    #plotROCs("differentTaus_HTT_ROC_" + pair_name, htt_truth_setups, extra_text = pretty_fiducial_cuts[sample_sig])        

       
    
    #plotROCs("differentTaus_gg_ROC_" + pair_name, gg_truth_setups, extra_text = pretty_fiducial_cuts[sample_sig])        
    plotROCs("differentTaus_ug_ROC_" + pair_name, ug_truth_setups + [best_setup], extra_text = pretty_fiducial_cuts[sample_sig])        
    #plotROCs("differentTaus_gu_ROC_" + pair_name, gu_truth_setups + [best_setup], extra_text = pretty_fiducial_cuts[sample_sig])        

    #plotROCs("differentTaus_trimmed_ROC_" + pair_name, trimmed_truth_setups + [best_setup], extra_text = pretty_fiducial_cuts[sample_sig])        

    #pool.map(doTMVA, only_size_setups)
    #plotROCs("differentTaus_onlySize_ROC_" + pair_name, only_size_setups, extra_text = "p_{T}>200 GeV, merged Tops")       

