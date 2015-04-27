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
    from TTH.Plotting.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.gregor.HiggsSamples import files, ranges, fiducial_cuts, pairs
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCs
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.python.gregor.HiggsSamples import files, ranges, fiducial_cuts, pairs


myStyle.SetTitleXOffset(1.3)
myStyle.SetTitleYOffset(1.7)
myStyle.SetPadLeftMargin(0.19)
myStyle.SetPadBottomMargin(0.13)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()

pool = mp.Pool(processes=16)  

########################################
# Configuration
########################################

DRAW_ROC = False

all_setups = []


for pair_name, pair in pairs.iteritems():
    sample_sig = pair[0]
    sample_bkg = pair[1]

    basepath = '/scratch/gregor/'
    file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
    file_name_bkg  = basepath + files[sample_bkg] + "-weighted.root"

    li_methods      = ["Cuts"]

    fj_size = ranges[pair[0]][2]
        
    combined_setups = []

    for var in [

        "{0}_tau2/{0}_tau1", 

        "{0}trimmedr2f6_tau2/{0}_tau1", 
        "{0}_tau2/{0}trimmedr2f6_tau1", 
        "{0}trimmedr2f6_tau2/{0}trimmedr2f6_tau1", 

        "{0}softdropz10b00_tau2/{0}_tau1", 
        "{0}_tau2/{0}softdropz10b00_tau1", 
        "{0}softdropz10b00_tau2/{0}softdropz10b00_tau1", 

        "{0}softdropz15b10_tau2/{0}_tau1", 
        "{0}_tau2/{0}softdropz15b10_tau1", 
        "{0}softdropz15b10_tau2/{0}softdropz15b10_tau1", 
    ]:
    


        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, var.replace("/","_")),
                                         variable.di[var.format(fj_size)].pretty_name,
                                         ["Cuts"], 
                                         [variable.di[var.format(fj_size)]],
                                         [],
                                         file_name_sig,
                                         file_name_bkg,
                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                                         weight_sig = "weight",
                                         weight_bkg = "weight",
                                         draw_roc = True,
                                         working_points = []))
      
    plotROCs("ROC_higgs_trimmed" + pair_name, [combined_setups[0]] + [x for x in combined_setups if "trimmed" in x.name])
    plotROCs("ROC_higgs_softdropz10b00" + pair_name, [combined_setups[0]] + [x for x in combined_setups if "softdropz10b00" in x.name])
    plotROCs("ROC_higgs_softdropz15b10" + pair_name, [combined_setups[0]] + [x for x in combined_setups if "softdropz15b10" in x.name])
    
    
    #all_setups += combined_setups

                        
#print all_setups
#pool.map(doTMVA, all_setups)





