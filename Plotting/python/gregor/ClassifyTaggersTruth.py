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
    
    setups = []
    btag_setups = []


    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_OptRHTT_mass_frec_dr_tau"),
                       "HTT V2 - m, fRec, #Delta R, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[1]=FSmart:VarProp[3]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=150:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=-0.5:CutRangeMax[2]=0.5:CutRangeMin[3]=0:CutRangeMax[3]=1"]], 
                       [variable.di['looseOptRHTT_mass'],
                        variable.di['looseOptRHTT_fRec'],
                        variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc'],
                        variable.di['ca15_tau3/ca15_tau2'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = fiducial_cuts[sample_sig],
                       fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                       weight_sig = "(weight)",
                       weight_bkg = "(weight)",
                       draw_roc = DRAW_ROC)
    setups.append(setup)


    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_OptRHTT_mass_frec_tau"),
                       "HTT V2 - m, fRec, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[1]=FSmart:VarProp[2]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=150:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=0:CutRangeMax[2]=1"]], 
                       [variable.di['looseOptRHTT_mass'],
                        variable.di['looseOptRHTT_fRec'],
                        variable.di['ca15_tau3/ca15_tau2'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = fiducial_cuts[sample_sig],
                       fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                       weight_sig = "(weight)",
                       weight_bkg = "(weight)",
                       draw_roc = DRAW_ROC)
    setups.append(setup)

    
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_SD"),
                      "log(#chi)",
                      [["Cuts", "V:FitMethod=MC:SampleSize=100000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=8"]], 
                      [variable.di['log(ca15_chi3)']],
                      [],
                      file_name_sig,
                      file_name_bkg,
                       fiducial_cut_sig = fiducial_cuts[sample_sig],
                       fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                      weight_sig = "(weight)",
                      weight_bkg = "(weight)",
                      draw_roc = DRAW_ROC,
                      working_points = [],
                      manual_working_points = [])
    setups.append(setup)


    mass_var  = "ca15softdropz20b10_mass"
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_" + mass_var + "Mass_Tau"),
                      variable.di[mass_var].pretty_name + "+ #tau_{3}/#tau_{2}",
                      [["Cuts", "V:FitMethod=MC:SampleSize=200000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:CutRangeMin[1]=0:CutRangeMax[1]=250:VarProp[0]=FSmart"]], 
                      [variable.di['ca15_tau3/ca15_tau2'],
                       variable.di[mass_var],
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig = fiducial_cuts[sample_sig],
                      fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                      weight_sig = "(weight)",
                      weight_bkg = "(weight)",
                      draw_roc = DRAW_ROC,
                      working_points = [],
                      manual_working_points = [])
    setups.append(setup)

    mass_var  = "ca15softdropz20b10_mass"
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_" + mass_var + "Mass_Groomed_Tau"),
                      variable.di[mass_var].pretty_name + "+ Groomed #tau_{3}/#tau_{2}",
                      [["Cuts", "V:FitMethod=MC:SampleSize=400000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:CutRangeMin[1]=0:CutRangeMax[1]=250:VarProp[0]=FSmart"]], 
                      [variable.di['ca15softdropz20b10_tau3/ca15softdropz20b10_tau2'],
                       variable.di[mass_var],
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig = fiducial_cuts[sample_sig],
                      fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                      weight_sig = "(weight)",
                      weight_bkg = "(weight)",
                      draw_roc = DRAW_ROC,
                      working_points = [],
                      manual_working_points = [])
    setups.append(setup)






    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_btag_OptRHTT_mass_frec_dr_tau"),
                       "HTT V2 - m, fRec, #Delta R, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[1]=FSmart:VarProp[3]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=150:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=-0.5:CutRangeMax[2]=0.5:CutRangeMin[3]=0:CutRangeMax[3]=1"]], 
                       [variable.di['looseOptRHTT_mass'],
                        variable.di['looseOptRHTT_fRec'],
                        variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc'],
                        variable.di['ca15_tau3/ca15_tau2'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = fiducial_cuts[sample_sig],
                       fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                       extra_cut = "ca15softdropz20b10forbtag_btag>0.814",
                       weight_sig = "(weight)",
                       weight_bkg = "(weight)",
                       draw_roc = DRAW_ROC)
    btag_setups.append(setup)


    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_btag_OptRHTT_mass_frec_tau"),
                       "HTT V2 - m, fRec, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[1]=FSmart:VarProp[2]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=150:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=0:CutRangeMax[2]=1"]], 
                       [variable.di['looseOptRHTT_mass'],
                        variable.di['looseOptRHTT_fRec'],
                        variable.di['ca15_tau3/ca15_tau2'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = fiducial_cuts[sample_sig],
                       fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                       extra_cut = "ca15softdropz20b10forbtag_btag>0.814",
                       weight_sig = "(weight)",
                       weight_bkg = "(weight)",
                       draw_roc = DRAW_ROC)
    btag_setups.append(setup)

    
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_btag_SD"),
                      "log(#chi)",
                      [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=10:VarProp[0]=FSmart"]], 
                      [variable.di['log(ca15_chi3)']],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig = fiducial_cuts[sample_sig],
                      fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                      extra_cut = "ca15softdropz20b10forbtag_btag>0.814",
                      weight_sig = "(weight)",
                      weight_bkg = "(weight)",
                      draw_roc = DRAW_ROC,
                      working_points = [],
                      manual_working_points = [])
    btag_setups.append(setup)


    mass_var  = "ca15softdropz20b10_mass"
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_btag_" +mass_var + "Mass_Tau"),
                      variable.di[mass_var].pretty_name + "+ #tau_{3}/#tau_{2}",
                      [["Cuts", "V:FitMethod=MC:SampleSize=100000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:CutRangeMin[1]=0:CutRangeMax[1]=250:VarProp[0]=FSmart"]], 
                      [variable.di['ca15_tau3/ca15_tau2'],
                       variable.di[mass_var],
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig = fiducial_cuts[sample_sig],
                      fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                      extra_cut = "ca15softdropz20b10forbtag_btag>0.814",
                      weight_sig = "(weight)",
                      weight_bkg = "(weight)",
                      draw_roc = DRAW_ROC,
                      working_points = [],
                      manual_working_points = [])
    btag_setups.append(setup)

    mass_var  = "ca15softdropz20b10_mass"
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_btag_" + mass_var + "Mass_Groomed_Tau"),
                      variable.di[mass_var].pretty_name + "+ Groomed #tau_{3}/#tau_{2}",
                      [["Cuts", "V:FitMethod=MC:SampleSize=100000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:CutRangeMin[1]=0:CutRangeMax[1]=250:VarProp[0]=FSmart"]], 
                      [variable.di['ca15softdropz20b10_tau3/ca15softdropz20b10_tau2'],
                       variable.di[mass_var],
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig = fiducial_cuts[sample_sig],
                      fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                      extra_cut = "ca15softdropz20b10forbtag_btag>0.814",
                      weight_sig = "(weight)",
                      weight_bkg = "(weight)",
                      draw_roc = DRAW_ROC,
                      working_points = [],
                      manual_working_points = [])
    btag_setups.append(setup)



    pool.map(doTMVA, btag_setups)


    #plotROCs("truth_ROC_" + pair_name, setups, extra_text = pretty_fiducial_cuts[sample_sig])        
    plotROCs("truth_btag_ROC_" + pair_name, btag_setups, extra_text = "b-tag + " + pretty_fiducial_cuts[sample_sig])        





