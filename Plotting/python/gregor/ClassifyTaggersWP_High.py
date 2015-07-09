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

pairs = { 
    "pt-800-to-1000" : ["zprime_m2000", "qcd_800_1000"],
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
    setups_size = []
    setups_notruth = []        



    for mass_var in  ["ak08softdropz10b00_mass"]:

        # Mass Window + SD
        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "mass_110_210_SD_WP_size"),
                          variable.di[mass_var].pretty_name + "(110..210) log(#chi)",
                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=10:VarProp[0]=FSmart"]], 
                          [variable.di['log(ak08_chi2)']],
                          [],
                          file_name_sig,
                          file_name_bkg,
                          fiducial_cut_sig  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                          fiducial_cut_bkg  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                          extra_cut = "((ak08softdropz10b00_mass>110)&&(ak08softdropz10b00_mass<210))",
                          weight_sig = "(1)",
                          weight_bkg = "(1)",
                          draw_roc = DRAW_ROC,
                          working_points = [],
                          manual_working_points = [])
        setups.append(setup)

        # Mass Window + SD + btag
        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "mass_110_210_SD_btag_WP_size"),
                          variable.di[mass_var].pretty_name + "(110..210) log(#chi) + b-tag",
                          [["Cuts", "V:FitMethod=MC:SampleSize=100000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=10:VarProp[0]=FSmart:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
                          [variable.di['log(ak08_chi2)'],
                           variable.di['ak08softdropz10b00forbtag_btag']],
                          [],
                          file_name_sig,
                          file_name_bkg,
                          fiducial_cut_sig  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                          fiducial_cut_bkg  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                          extra_cut = "((ak08softdropz10b00_mass>110)&&(ak08softdropz10b00_mass<210))",
                          weight_sig = "(1)",
                          weight_bkg = "(1)",
                          draw_roc = DRAW_ROC,
                          working_points = [],
                          manual_working_points = [])
        setups.append(setup)
                        
    # HTT: mass window + fRec + tau
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_120_180_frec_tau_WP_size"),
                       "HTT V2 - m (120..180), fRec, dR, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
                       [variable.di['looseOptRHTT_fRec'],
                        variable.di['ak08_tau3/ak08_tau2'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                       fiducial_cut_bkg  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                       extra_cut = "((looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180))",
                       weight_sig = "(1)",
                       weight_bkg = "(1)",
                       draw_roc = DRAW_ROC)
    setups.append(setup)

    # HTT: mass window + fRec + tau + DeltaR
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_120_180_frec_deltaROpt_tau_WP_size"),
                       "HTT V2 - m (120..180), fRec, dR, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=1000000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:CutRangeMin[2]=-1:CutRangeMax[2]=1:VarProp[1]=FSmart"]], 
                       [variable.di['looseOptRHTT_fRec'],
                        variable.di['ak08_tau3/ak08_tau2'],
                        variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                       fiducial_cut_bkg  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                       extra_cut = "((looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180))",
                       weight_sig = "(1)",
                       weight_bkg = "(1)",
                       draw_roc = DRAW_ROC)
    setups.append(setup)

    # HTT: mass window + fRec + tau + DeltaR + btag
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_120_180_frec_deltaROpt_tau_btag_WP_size"),
                       "HTT V2 - m (120..180), fRec, dR, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=1000000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:CutRangeMin[2]=-1:CutRangeMax[2]=1:VarProp[1]=FSmart:VarProp[3]=FSmart:CutRangeMin[3]=0:CutRangeMax[3]=1."]], 
                       [variable.di['looseOptRHTT_fRec'],
                        variable.di['ak08_tau3/ak08_tau2'],
                        variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc'],
                        variable.di['ak08softdropz10b00forbtag_btag']
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                       fiducial_cut_bkg  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                       extra_cut = "((looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180))",
                       weight_sig = "(1)",
                       weight_bkg = "(1)",
                       draw_roc = DRAW_ROC)
    setups.append(setup)

    # SD
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "SD_WP_size"),
                      "log(#chi)",
                      [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=10:VarProp[0]=FSmart"]], 
                      [variable.di['log(ak08_chi2)']],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                      fiducial_cut_bkg  = "((pt>200)&&(ak08_pt>200)&&(top_size<0.6))",
                      weight_sig = "(1)",
                      weight_bkg = "(1)",
                      draw_roc = DRAW_ROC,
                      working_points = [],
                      manual_working_points = [])
    setups.append(setup)

    
    pool.map(doTMVA, setups)
    plotROCs("WPS_" + pair_name, setups, extra_text = pretty_fiducial_cuts[sample_sig])        
