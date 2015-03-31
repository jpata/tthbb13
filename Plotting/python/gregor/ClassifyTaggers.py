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

import ROOT

# Our support Code
# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCMultiple
    from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import files, ranges, fiducial_cuts, pairs
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCMultiple
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import files, ranges, fiducial_cuts, pairs


myStyle.SetTitleXOffset(1.3)
myStyle.SetTitleYOffset(1.7)
myStyle.SetPadLeftMargin(0.19)
myStyle.SetPadBottomMargin(0.13)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


########################################
# Configuration
########################################

for pair_name, pair in pairs.iteritems():
    sample_sig = pair[0]
    sample_bkg = pair[1]

    basepath = '/scratch/gregor/'
    file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
    file_name_bg   = basepath + files[sample_bkg] + "-weighted.root"

    li_methods      = ["Cuts"]

    fj_size = ranges[pair[0]][4]
    
    combined_setups = []
    combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "trimmed_combined"),
                                     "Trimmed (r=0.2, f=0.06) m + #tau_{3}/#tau_{2}",
                                     ["Cuts"], 
                                     [variable.di['{0}trimmedr2f6_mass'.format(fj_size)],
                                      variable.di['{0}_tau3/{0}_tau2'.format(fj_size)],
                                  ],                               
                                     file_name_sig,
                                     file_name_bg,
                                     fiducial_cut_sig = fiducial_cuts[sample_sig],
                                     fiducial_cut_bg  = fiducial_cuts[sample_bkg],
                                     weight_sig = "weight",
                                     weight_bg = "weight"))

    combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_combined"),
                                     "Softdrop (z=0.1, beta=0) m + #tau_{3}/#tau_{2}",
                                     ["Cuts"], 
                                     [variable.di['{0}softdropz10b00_mass'.format(fj_size)],
                                      variable.di['{0}_tau3/{0}_tau2'.format(fj_size)],
                                  ],                               
                                     file_name_sig,
                                     file_name_bg,
                                     fiducial_cut_sig = fiducial_cuts[sample_sig],
                                     fiducial_cut_bg  = fiducial_cuts[sample_bkg],
                                     weight_sig = "weight",
                                     weight_bg = "weight"))


    combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "showerdeconstruction"),
                                     "Shower Deconstruction",
                                     ["Cuts"], 
                                     [variable.di['log({0}_chi)'.format(fj_size)],
                                  ],                               
                                     file_name_sig,
                                     file_name_bg,
                                     fiducial_cut_sig = fiducial_cuts[sample_sig],
                                     fiducial_cut_bg  = fiducial_cuts[sample_bkg],
                                     weight_sig = "weight",
                                     weight_bg = "weight"))

    combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "HTT_combined"),
                                     "HTT (m, f_{Rec}, #Delta R)",
                                     ["Cuts"], 
                                     [variable.di['looseOptRHTT_mass'],
                                      variable.di['looseOptRHTT_fRec'],
                                      variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc']],                               
                                     file_name_sig,
                                     file_name_bg,
                                     fiducial_cut_sig = fiducial_cuts[sample_sig],
                                     fiducial_cut_bg  = fiducial_cuts[sample_bkg],
                                     weight_sig = "weight",
                                     weight_bg = "weight"))

    #if not pair_name in ["pt-200-to-300", "pt-300-to-470"]:
    combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "CMSTT_combined"),
                                     "CMSTT (topMass, minMass)",
                                     ["Cuts"], 
                                     [variable.di['{0}cmstt_topMass'.format(fj_size)],
                                      variable.di['{0}cmstt_minMass'.format(fj_size)]], 
                                     file_name_sig,
                                     file_name_bg,
                                     fiducial_cut_sig = fiducial_cuts[sample_sig],
                                     fiducial_cut_bg  = fiducial_cuts[sample_bkg],
                                     weight_sig = "weight",
                                     weight_bg = "weight"))



    #for setup in combined_setups:
    #    doTMVA(setup)

    plotROCMultiple("ROC_combined_" + pair_name, combined_setups)

