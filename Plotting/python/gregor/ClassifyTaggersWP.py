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

    fj_size = ranges[pair[0]][4]
    
    setups = []
    setups_size = []
    setups_notruth = []        

    # PLOT!
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_dr_tau_size"),
                       "HTT V2 - m, fRec, dR, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=2000000:VarProp[1]=FSmart:VarProp[3]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=250:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=-1:CutRangeMax[2]=1:CutRangeMin[3]=0:CutRangeMax[3]=1"]], 
                       [variable.di['looseOptRHTT_mass'],
                        variable.di['looseOptRHTT_fRec'],
                        variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc'],
                        variable.di['ca15_tau3/ca15_tau2'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
                       weight_sig = "(1)",
                       weight_bkg = "(1)",
                       draw_roc = DRAW_ROC)
    setups.append(setup)

    # PLOT!
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_tau_size"),
                       "HTT V2 - m, fRec, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=2000000:VarProp[1]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=250:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=0:CutRangeMax[2]=1:VarProp[2]=FSmart"]], 
                       [variable.di['looseOptRHTT_mass'],
                        variable.di['looseOptRHTT_fRec'],
                        variable.di['ca15_tau3/ca15_tau2'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
                       weight_sig = "(1)",
                       weight_bkg = "(1)",
                       draw_roc = DRAW_ROC)
    setups.append(setup)

    
    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "SD_size"),
                      "log(#chi)",
                      [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=10:VarProp[0]=FSmart"]], 
                      [variable.di['log(ca15_chi3)']],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
                      fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
                      weight_sig = "(1)",
                      weight_bkg = "(1)",
                      draw_roc = DRAW_ROC,
                      working_points = [],
                      manual_working_points = [])
    setups.append(setup)


    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "SD_tau_size"),
                      "log(#chi) + #tau_{3}/#tau_{2}",
                      [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=10:VarProp[0]=FSmart:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
                      [variable.di['log(ca15_chi3)'], 
                       variable.di['ca15_tau3/ca15_tau2']
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
                      fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
                      weight_sig = "(1)",
                      weight_bkg = "(1)",
                      draw_roc = DRAW_ROC,
                      working_points = [],
                      manual_working_points = [])
    setups.append(setup)

    



    # PLOT!
    for mass_var in  ["ca15softdropz20b10_mass"]:
        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_150_240_tau_WP_size"),
                          variable.di[mass_var].pretty_name + "(150..240) #tau_{3}/#tau_{2}",
                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
                          [variable.di['ca15_tau3/ca15_tau2']],
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

    plotROCs("SDtest" + pair_name, setups, extra_text = pretty_fiducial_cuts[sample_sig])        



#    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_140_190_frec_tau_size"),
#                       "HTT V2 - m (140..190), fRec, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                       [variable.di['looseOptRHTT_fRec'],
#                        variable.di['ca15_tau3/ca15_tau2'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       extra_cut = "((looseOptRHTT_mass>140)&&(looseOptRHTT_mass<190))",
#                       weight_sig = "(1)",
#                       weight_bkg = "(1)",
#                       draw_roc = DRAW_ROC)
#    setups.append(setup)
#
#    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_130_190_frec_tau_size"),
#                       "HTT V2 - m (130..190), fRec, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                       [variable.di['looseOptRHTT_fRec'],
#                        variable.di['ca15_tau3/ca15_tau2'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       extra_cut = "((looseOptRHTT_mass>130)&&(looseOptRHTT_mass<190))",
#                       weight_sig = "(1)",
#                       weight_bkg = "(1)",
#                       draw_roc = DRAW_ROC)
#    setups.append(setup)
#
#    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_120_190_frec_tau_size"),
#                       "HTT V2 - m (120..190), fRec, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                       [variable.di['looseOptRHTT_fRec'],
#                        variable.di['ca15_tau3/ca15_tau2'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       extra_cut = "((looseOptRHTT_mass>120)&&(looseOptRHTT_mass<190))",
#                       weight_sig = "(1)",
#                       weight_bkg = "(1)",
#                       draw_roc = DRAW_ROC)
#    setups.append(setup)
#
#
#    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_140_180_frec_tau_size"),
#                       "HTT V2 - m (140..180), fRec, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                       [variable.di['looseOptRHTT_fRec'],
#                        variable.di['ca15_tau3/ca15_tau2'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       extra_cut = "((looseOptRHTT_mass>140)&&(looseOptRHTT_mass<180))",
#                       weight_sig = "(1)",
#                       weight_bkg = "(1)",
#                       draw_roc = DRAW_ROC)
#    setups.append(setup)
#
#    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_130_180_frec_tau_size"),
#                       "HTT V2 - m (130..180), fRec, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                       [variable.di['looseOptRHTT_fRec'],
#                        variable.di['ca15_tau3/ca15_tau2'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       extra_cut = "((looseOptRHTT_mass>130)&&(looseOptRHTT_mass<180))",
#                       weight_sig = "(1)",
#                       weight_bkg = "(1)",
#                       draw_roc = DRAW_ROC)
#    setups.append(setup)
#
#    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_120_180_frec_deltaROpt_tau_size"),
#                       "HTT V2 - m (120..180), fRec, dR, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=1000000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:CutRangeMin[2]=-1:CutRangeMax[2]=1:VarProp[1]=FSmart"]], 
#                       [variable.di['looseOptRHTT_fRec'],
#                        variable.di['ca15_tau3/ca15_tau2'],
#                        variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       extra_cut = "((looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180))",
#                       weight_sig = "(1)",
#                       weight_bkg = "(1)",
#                       draw_roc = DRAW_ROC)
#    setups.append(setup)
#
#    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_120_180_frec_tau_size"),
#                       "HTT V2 - m (120..180), fRec, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                       [variable.di['looseOptRHTT_fRec'],
#                        variable.di['ca15_tau3/ca15_tau2'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       extra_cut = "((looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180))",
#                       weight_sig = "(1)",
#                       weight_bkg = "(1)",
#                       draw_roc = DRAW_ROC)
#    setups.append(setup)


#    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_140_170_frec_tau_size"),
#                       "HTT V2 - m (140..170), fRec, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                       [variable.di['looseOptRHTT_fRec'],
#                        variable.di['ca15_tau3/ca15_tau2'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       extra_cut = "((looseOptRHTT_mass>140)&&(looseOptRHTT_mass<170))",
#                       weight_sig = "(1)",
#                       weight_bkg = "(1)",
#                       draw_roc = DRAW_ROC)
#    setups.append(setup)
#
#    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_130_170_frec_tau_size"),
#                       "HTT V2 - m (130..170), fRec, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                       [variable.di['looseOptRHTT_fRec'],
#                        variable.di['ca15_tau3/ca15_tau2'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       extra_cut = "((looseOptRHTT_mass>130)&&(looseOptRHTT_mass<170))",
#                       weight_sig = "(1)",
#                       weight_bkg = "(1)",
#                       draw_roc = DRAW_ROC)
#    setups.append(setup)
#
#    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "OptRHTT_mass_120_170_frec_tau_size"),
#                       "HTT V2 - m (120..170), fRec, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=500000:VarProp[0]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=0.5:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                       [variable.di['looseOptRHTT_fRec'],
#                        variable.di['ca15_tau3/ca15_tau2'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       extra_cut = "((looseOptRHTT_mass>120)&&(looseOptRHTT_mass<170))",
#                       weight_sig = "(1)",
#                       weight_bkg = "(1)",
#                       draw_roc = DRAW_ROC)
#    setups.append(setup)
#





#    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "HTT_mass_frec_tau_size"),
#                       "HTT V2 (singleR)- m, fRec, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=2000000:VarProp[1]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=250:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=0:CutRangeMax[2]=1:VarProp[2]=FSmart"]], 
#                       [variable.di['looseHTT_mass'],
#                        variable.di['looseHTT_fRec'],
#                        variable.di['ca15_tau3/ca15_tau2'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                       weight_sig = "(1)",
#                       weight_bkg = "(1)",
#                       draw_roc = DRAW_ROC)
#
#    setups.append(setup)

    
    #pool.map(doTMVA, setups)
    #plotROCs("withDr_testsizeHTT_ROC_" + pair_name, setups)             










   #for mass_var in  ["ca15trimmedr2f9_mass",
   #                  "ca15softdropz10b00_mass",
   #                  "ca15softdropz20b10_mass",]:
   #
   #    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_combined_WP_size"),
   #                      variable.di[mass_var].pretty_name + " #tau_{3}/#tau_{2}",
   #                      [["Cuts", "V:FitMethod=MC:SampleSize=800000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
   #                      [variable.di[mass_var],
   #                       variable.di['ca15_tau3/ca15_tau2']],
   #                      [],
   #                      file_name_sig,
   #                      file_name_bkg,
   #                      fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
   #                      fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
   #                      weight_sig = "(1)",
   #                      weight_bkg = "(1)",
   #                      draw_roc = DRAW_ROC,
   #                      working_points = [],
   #                      manual_working_points = [])
   #    setups.append(setup)
   #
   #    setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_combined_WP"),
   #                      variable.di[mass_var].pretty_name + " #tau_{3}/#tau_{2}",
   #                      [["Cuts", "V:FitMethod=MC:SampleSize=800000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
   #                      [variable.di[mass_var],
   #                       variable.di['ca15_tau3/ca15_tau2']],
   #                      [],
   #                      file_name_sig,
   #                      file_name_bkg,
   #                      fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200))",
   #                      fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200))",
   #                      weight_sig = "(1)",
   #                      weight_bkg = "(1)",
   #                      draw_roc = DRAW_ROC,
   #                      working_points = [],
   #                      manual_working_points = [])
   #    setups.append(setup)

#
#
#
#    for mass_var in  ["ca15softdropz20b10_mass"]:
#
#        #setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_140_240_tau_WP_size"),
#        #                  variable.di[mass_var].pretty_name + "(140..240) #tau_{3}/#tau_{2}",
#        #                  [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
#        #                  [variable.di['ca15_tau3/ca15_tau2']],
#        #                  [],
#        #                  file_name_sig,
#        #                  file_name_bkg,
#        #                  fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#        #                  fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#        #                  extra_cut = "((ca15softdropz20b10_mass>140)&&(ca15softdropz20b10_mass<240))",
#        #                  weight_sig = "(1)",
#        #                  weight_bkg = "(1)",
#        #                  draw_roc = DRAW_ROC,
#        #                  working_points = [],
#        #                  manual_working_points = [])
#        #setups.append(setup)
#        #setups_size.append(setup)
# 
#        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_150_240_tau_WP_size"),
#                          variable.di[mass_var].pretty_name + "(150..240) #tau_{3}/#tau_{2}",
#                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
#                          [variable.di['ca15_tau3/ca15_tau2']],
#                          [],
#                          file_name_sig,
#                          file_name_bkg,
#                          fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                          fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                          extra_cut = "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240))",
#                          weight_sig = "(1)",
#                          weight_bkg = "(1)",
#                          draw_roc = DRAW_ROC,
#                          working_points = [],
#                          manual_working_points = [])
#        setups.append(setup)
#        setups_size.append(setup)
#
#        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_150_240_tau_WP_size_medium_sd_btag"),
#                          variable.di[mass_var].pretty_name + "(150..240) #tau_{3}/#tau_{2}, b-tag (SD, z=0.1, #beta=0)",
#                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
#                          [variable.di['ca15_tau3/ca15_tau2']],
#                          [],
#                          file_name_sig,
#                          file_name_bkg,
#                          fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                          fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                          extra_cut = "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240)&&(ca15softdropz10b00forbtag_btag>0.814))",
#                          weight_sig = "(1)",
#                          weight_bkg = "(1)",
#                          draw_roc = DRAW_ROC,
#                          working_points = [],
#                          manual_working_points = [])
#        setups.append(setup)
#        setups_size.append(setup)
#
#        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_150_240_tau_WP_size_medium_sd20z10_btag"),
#                          variable.di[mass_var].pretty_name + "(150..240) #tau_{3}/#tau_{2}, b-tag (SD, z=0.2, #beta=1)",
#                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
#                          [variable.di['ca15_tau3/ca15_tau2']],
#                          [],
#                          file_name_sig,
#                          file_name_bkg,
#                          fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                          fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                          extra_cut = "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240)&&(ca15softdropz20b10forbtag_btag>0.814))",
#                          weight_sig = "(1)",
#                          weight_bkg = "(1)",
#                          draw_roc = DRAW_ROC,
#                          working_points = [],
#                          manual_working_points = [])
#        setups.append(setup)
#        setups_size.append(setup)
#
#        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_150_240_tau_WP_size_medium_trim_btag"),
#                          variable.di[mass_var].pretty_name + "(150..240) #tau_{3}/#tau_{2}, b-tag (trim)",
#                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
#                          [variable.di['ca15_tau3/ca15_tau2']],
#                          [],
#                          file_name_sig,
#                          file_name_bkg,
#                          fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                          fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                          extra_cut = "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240)&&(ca15trimmedr2f6forbtag_btag>0.814))",
#                          weight_sig = "(1)",
#                          weight_bkg = "(1)",
#                          draw_roc = DRAW_ROC,
#                          working_points = [],
#                          manual_working_points = [])
#        setups.append(setup)
#        setups_size.append(setup)
#
#        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_150_240_tau_WP_size_medium_filt_btag"),
#                          variable.di[mass_var].pretty_name + "(150..240) #tau_{3}/#tau_{2}, b-tag (filt)",
#                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
#                          [variable.di['ca15_tau3/ca15_tau2']],
#                          [],
#                          file_name_sig,
#                          file_name_bkg,
#                          fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                          fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
#                          extra_cut = "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240)&&(ca15filteredn3r2forbtag_btag>0.814))",
#                          weight_sig = "(1)",
#                          weight_bkg = "(1)",
#                          draw_roc = DRAW_ROC,
#                          working_points = [],
#                          manual_working_points = [])
#        setups.append(setup)
#        setups_size.append(setup)
#
#        #pool.map(doTMVA, setups)
#        plotROCs("withBtags_testsize_ROC_" + pair_name, setups)             
#


##        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_160_240_tau_WP_size"),
##                          variable.di[mass_var].pretty_name + "(160..240) #tau_{3}/#tau_{2}",
##                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
##                          [variable.di['ca15_tau3/ca15_tau2']],
##                          [],
##                          file_name_sig,
##                          file_name_bkg,
##                          fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
##                          fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
##                          extra_cut = "((ca15softdropz20b10_mass>160)&&(ca15softdropz20b10_mass<240))",
##                          weight_sig = "(1)",
##                          weight_bkg = "(1)",
##                          draw_roc = DRAW_ROC,
##                          working_points = [],
##                          manual_working_points = [])
##        setups.append(setup)
##        setups_size.append(setup)
##
##
##        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_140_220_tau_WP_size"),
##                          variable.di[mass_var].pretty_name + "(140..220) #tau_{3}/#tau_{2}",
##                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
##                          [variable.di['ca15_tau3/ca15_tau2']],
##                          [],
##                          file_name_sig,
##                          file_name_bkg,
##                          fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
##                          fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
##                          extra_cut = "((ca15softdropz20b10_mass>140)&&(ca15softdropz20b10_mass<220))",
##                          weight_sig = "(1)",
##                          weight_bkg = "(1)",
##                          draw_roc = DRAW_ROC,
##                          working_points = [],
##                          manual_working_points = [])
##        setups.append(setup)
##        setups_size.append(setup)
##
##        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_150_220_tau_WP_size"),
##                          variable.di[mass_var].pretty_name + "(150..220) #tau_{3}/#tau_{2}",
##                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
##                          [variable.di['ca15_tau3/ca15_tau2']],
##                          [],
##                          file_name_sig,
##                          file_name_bkg,
##                          fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
##                          fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
##                          extra_cut = "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<220))",
##                          weight_sig = "(1)",
##                          weight_bkg = "(1)",
##                          draw_roc = DRAW_ROC,
##                          working_points = [],
##                          manual_working_points = [])
##        setups.append(setup)
##        setups_size.append(setup)
##
##        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_160_220_tau_WP_size"),
##                          variable.di[mass_var].pretty_name + "(160..220) #tau_{3}/#tau_{2}",
##                          [["Cuts", "V:FitMethod=MC:SampleSize=50000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:VarProp[0]=FSmart"]], 
##                          [variable.di['ca15_tau3/ca15_tau2']],
##                          [],
##                          file_name_sig,
##                          file_name_bkg,
##                          fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
##                          fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
##                          extra_cut = "((ca15softdropz20b10_mass>160)&&(ca15softdropz20b10_mass<220))",
##                          weight_sig = "(1)",
##                          weight_bkg = "(1)",
##                          draw_roc = DRAW_ROC,
##                          working_points = [],
##                          manual_working_points = [])
##        setups.append(setup)
##        setups_size.append(setup)
##
##
##
##        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_combined_WP_size"),
##                          variable.di[mass_var].pretty_name + " #tau_{3}/#tau_{2}",
##                          [["Cuts", "V:FitMethod=MC:SampleSize=800000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
##                          [variable.di[mass_var],
##                           variable.di['ca15_tau3/ca15_tau2']],
##                          [],
##                          file_name_sig,
##                          file_name_bkg,
##                          fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
##                          fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200)&&(top_size<0.8))",
##                          weight_sig = "(1)",
##                          weight_bkg = "(1)",
##                          draw_roc = DRAW_ROC,
##                          working_points = [],
##                          manual_working_points = [
##                              {"name" : "0.001", "cuts" : "(ca15softdropz20b10_mass>160)&&(ca15softdropz20b10_mass<220)&&(ca15_tau3_D_ca15_tau2>-1.0000000000000000e+30)&&(ca15_tau3_D_ca15_tau2<5.4e-01)"},
##                              {"name" : "0.003", "cuts" : "(ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<210)&&(ca15_tau3_D_ca15_tau2>-1.0000000000000000e+30)&&(ca15_tau3_D_ca15_tau2<6.0e-01)"},
##                              {"name" : "0.01" , "cuts" : "(ca15softdropz20b10_mass>140)&&(ca15softdropz20b10_mass<240)&&(ca15_tau3_D_ca15_tau2>-1.0000000000000000e+30)&&(ca15_tau3_D_ca15_tau2<6.6e-01)"},
##                              {"name" : "0.03" , "cuts" : "(ca15softdropz20b10_mass>140)&&(ca15softdropz20b10_mass<250)&&(ca15_tau3_D_ca15_tau2>-1.0000000000000000e+30)&&(ca15_tau3_D_ca15_tau2<7.2e-01)"},
##                              {"name" : "0.1"  , "cuts" : "(ca15softdropz20b10_mass>130)&&(ca15softdropz20b10_mass<430)&&(ca15_tau3_D_ca15_tau2>-1.0000000000000000e+30)&&(ca15_tau3_D_ca15_tau2<7.9e-01)"},
##                          ])
##        setups.append(setup)
##        setups_size.append(setup)
##
    #
    #setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, mass_var + "_combined_WP"),
    #                  variable.di[mass_var].pretty_name + " #tau_{3}/#tau_{2}",
    #                  [["Cuts", "V:FitMethod=MC:SampleSize=800000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
    #                  [variable.di[mass_var],
    #                   variable.di['ca15_tau3/ca15_tau2']],
    #                  [],
    #                  file_name_sig,
    #                  file_name_bkg,
    #                  fiducial_cut_sig  = "((pt>200)&&(ca15_pt>200))",
    #                  fiducial_cut_bkg  = "((pt>200)&&(ca15_pt>200))",
    #                  weight_sig = "(1)",
    #                  weight_bkg = "(1)",
    #                  draw_roc = DRAW_ROC,
    #                  working_points = [],
    #                  manual_working_points = [
    #                      {"name" : "0.001", "cuts" : "(ca15softdropz20b10_mass>160)&&(ca15softdropz20b10_mass<220)&&(ca15_tau3_D_ca15_tau2>-1.0000000000000000e+30)&&(ca15_tau3_D_ca15_tau2<5.4e-01)"},
    #                      {"name" : "0.003", "cuts" : "(ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<210)&&(ca15_tau3_D_ca15_tau2>-1.0000000000000000e+30)&&(ca15_tau3_D_ca15_tau2<6.0e-01)"},
    #                      {"name" : "0.01" , "cuts" : "(ca15softdropz20b10_mass>140)&&(ca15softdropz20b10_mass<240)&&(ca15_tau3_D_ca15_tau2>-1.0000000000000000e+30)&&(ca15_tau3_D_ca15_tau2<6.6e-01)"},
    #                      {"name" : "0.03" , "cuts" : "(ca15softdropz20b10_mass>140)&&(ca15softdropz20b10_mass<250)&&(ca15_tau3_D_ca15_tau2>-1.0000000000000000e+30)&&(ca15_tau3_D_ca15_tau2<7.2e-01)"},
    #                      {"name" : "0.1"  , "cuts" : "(ca15softdropz20b10_mass>130)&&(ca15softdropz20b10_mass<430)&&(ca15_tau3_D_ca15_tau2>-1.0000000000000000e+30)&&(ca15_tau3_D_ca15_tau2<7.9e-01)"},
    #                  ])
    #setups.append(setup)
    #setups_notruth.append(setup)

    #plotROCs("sizeWP_ROC_" + pair_name, setups_size, extra_text = pretty_fiducial_cuts[sample_sig])        
    #plotROCs("notruthWP_ROC_" + pair_name, setups_notruth, extra_text = pretty_fiducial_cuts[sample_sig])        
     
    #pool.map(doTMVA, setups)





