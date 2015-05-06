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

all_setups = []

for pair_name, pair in pairs.iteritems():
    sample_sig = pair[0]
    sample_bkg = pair[1]

    basepath = '/scratch/gregor/'
    file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
    file_name_bkg  = basepath + files[sample_bkg] + "-weighted.root"

    li_methods      = ["Cuts"]

    fj_size = ranges[pair[0]][4]
    if fj_size=="ca15":
        other_fj_size="ca08"
    else:
        other_fj_size="ca15"
    
    
    combined_setups = []

    combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "showerdeconstruction"),
                                 "Shower Deconstruction",
                                 [["Cuts", "FitMethod=MC:SampleSize=50000"]], 
                                 [variable.di['log({0}_chi)'.format(fj_size)]],
                                 [variable.di['log({0}_chi)'.format(other_fj_size)]],
                                 file_name_sig,
                                 file_name_bkg,
                                 fiducial_cut_sig = fiducial_cuts[sample_sig],
                                 fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                                 weight_sig = "weight",
                                 weight_bkg = "weight",
                                 draw_roc = DRAW_ROC))
        


    combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_combined"),
                                     "SD(z=0.1, #beta=0) m, #tau_{3}/#tau_{2}",
                                     [["Cuts", "FitMethod=MC:SampleSize=1600000"]], 
                                     [variable.di['{0}softdropz10b00_mass'.format(fj_size)],
                                      variable.di['{0}_tau3/{0}_tau2'.format(fj_size)]],
                                     [],
                                     file_name_sig,
                                     file_name_bkg,
                                     fiducial_cut_sig = fiducial_cuts[sample_sig],
                                     fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                                     weight_sig = "weight",
                                     weight_bkg = "weight",
                                     draw_roc = DRAW_ROC,
                                     working_points = []))

    combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "HTT_mass_frec_DeltaRopt"),
                                     "HEPTopTagger V2",
                                     [["Cuts", "FitMethod=MC:SampleSize=24000000"]], 
                                     [variable.di['looseOptRHTT_mass'],
                                      variable.di['looseOptRHTT_fRec'],
                                      variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc']],                               
                                     [],
                                     file_name_sig,
                                     file_name_bkg,
                                     fiducial_cut_sig = fiducial_cuts[sample_sig],
                                     fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                                     weight_sig = "weight",
                                     weight_bkg = "weight",
                                     draw_roc = DRAW_ROC,
                                 ))

#    combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "HTT_mass_frec_NoOptR"),
#                                     "HEPTopTagger V2 - noOptR",
#                                     [["Cuts", "FitMethod=MC:SampleSize=3000000"]], 
#                                     [variable.di['looseHTT_mass'],
#                                      variable.di['looseHTT_fRec']],
#                                     [],
#                                     file_name_sig,
#                                     file_name_bkg,
#                                     fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                     fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                     weight_sig = "weight",
#                                     weight_bkg = "weight",
#                                     draw_roc = DRAW_ROC,
#                                 ))
#
 

    

    if pair_name in ["pt-300-to-470"]:
        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz15b10_combined"),
                                         "SD(z=0.15, #beta=1) m, #tau_{3}/#tau_{2}",
                                         [["Cuts", "FitMethod=MC:SampleSize=1600000"]], 
                                         [variable.di['{0}softdropz15b10_mass'.format(fj_size)],
                                          variable.di['{0}_tau3/{0}_tau2'.format(fj_size)]],
                                         [],
                                         file_name_sig,
                                         file_name_bkg,
                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                                         weight_sig = "weight",
                                         weight_bkg = "weight",
                                         draw_roc = DRAW_ROC,
                                         working_points = []))

#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "trimmed_combined"),
#                                         "Trimmed (r=0.2, f=0.06) m, #tau_{3}/#tau_{2}",
#                                         [["Cuts", "FitMethod=MC:SampleSize=200000"]], 
#                                         [variable.di['{0}trimmedr2f6_mass'.format(fj_size)],
#                                          variable.di['{0}_tau3/{0}_tau2'.format(fj_size)],
#                                      ],                               
#                                         [],
#                                         file_name_sig,
#                                         file_name_bkg,
#                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                         weight_sig = "weight",
#                                         weight_bkg = "weight",
#                                         draw_roc = DRAW_ROC,
#                                         working_points = []))
#


    if pair_name in ["pt-800-to-1000"]:
        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "CMSTT_mtop_mmin"),
                                         "CMSTT(minMass, topMass)",
                                         [["Cuts", "FitMethod=MC:SampleSize=2000000"]], 
                                         [variable.di['{0}cmstt_topMass'.format(fj_size)],
                                          variable.di['{0}cmstt_minMass'.format(fj_size)]], 
                                         [], 
                                         file_name_sig,
                                         file_name_bkg,
                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                                         weight_sig = "weight",
                                         weight_bkg = "weight",
                                         draw_roc = DRAW_ROC))

#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_CMSTT_mmin"),
#                                         "SD(z=0.1, #beta=0), CMSTT(minMass)",
#                                         [["Cuts", "FitMethod=MC:SampleSize=600000"]], 
#                                         [variable.di['{0}cmstt_minMass'.format(fj_size)],
#                                          variable.di['{0}softdropz10b00_mass'.format(fj_size)]],
#                                         [], 
#                                         file_name_sig,
#                                         file_name_bkg,
#                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                         weight_sig = "weight",
#                                         weight_bkg = "weight",
#                                         draw_roc = DRAW_ROC))
#
        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_tau3tau2_CMSTT_mmin"),
                                         "SD(z=0.1, #beta=0), #tau_{3}/#tau_{2}, CMSTT(minMass)",
                                         [["Cuts", "FitMethod=MC:SampleSize=20000000"]], 
                                         [variable.di['{0}cmstt_minMass'.format(fj_size)],
                                          variable.di['{0}softdropz10b00_mass'.format(fj_size)],
                                          variable.di['{0}_tau3/{0}_tau2'.format(fj_size)]],
                                         [], 
                                         file_name_sig,
                                         file_name_bkg,
                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                                         weight_sig = "weight",
                                         weight_bkg = "weight",
                                         draw_roc = DRAW_ROC))

        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_combined_CMSTTWP"),
                                         "SD(z=0.1, #beta=0) m, #tau_{3}/#tau_{2}, CMSTT WP",
                                         [["Cuts", "FitMethod=MC:SampleSize=1600000"]], 
                                         [variable.di['{0}softdropz10b00_mass'.format(fj_size)],
                                          variable.di['{0}_tau3/{0}_tau2'.format(fj_size)]],
                                         [],
                                         file_name_sig,
                                         file_name_bkg,
                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                                         extra_cut = "(({0}cmstt_nSubJets>=3)&&({0}cmstt_topMass>140)&&({0}cmstt_topMass<250)&&({0}cmstt_minMass>50))".format(fj_size),
                                         weight_sig = "weight",
                                         weight_bkg = "weight",
                                         draw_roc = DRAW_ROC,
                                         working_points = []))


    


  

    #plotROCs("ROC_" + pair_name, combined_setups, extra_text = pretty_fiducial_cuts[sample_sig])        
    all_setups += combined_setups

pool.map(doTMVA, all_setups)





