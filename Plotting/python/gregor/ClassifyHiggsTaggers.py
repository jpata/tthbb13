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
    from TTH.Plotting.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.gregor.HiggsSamples import files, fiducial_cuts
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCMultiple
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.python.gregor.HiggsSamples import files, fiducial_cuts

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


########################################
# Configuration
########################################

run_TMVA = False

sample_sig = "tth"
sample_bkg  = "ttj"

basepath = '/scratch/gregor/'
file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
file_name_bg   = basepath + files[sample_bkg] + "-weighted.root"

li_methods      = ["Cuts"]


# We want to make single-variable ROC curves
# so first create a list of variables and then send them individually to TMVA
    
def create_setups(li_vars):
    li_TMVAs = []
    for v in li_vars:
        name = "{0}_{1}_{2}".format(sample_sig, sample_bkg, v.name)
        name = name.replace("/","_")
        li_TMVAs.append( TMVASetup( name,
                                    prettier_names[v.pretty_name],
                                    li_methods, 
                                    [v],
                                    file_name_sig,
                                    file_name_bg,
                                    fiducial_cut_sig = "(pt>150)",
                                    fiducial_cut_bg  = "(pt>150)",
                                    weight_sig = "(1)",
                                    weight_bg  = "(1)",
                                ))
    return li_TMVAs
# end of create_setups


combined_setups = []

#combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "trimmed_combined"),
#                                 "trimmed m + unfiltered tau_{2}/tau_{1}",
#                                 ["Cuts"], 
#                                 [variable.di['ca15trimmed_mass'],
#                                  variable.di['ca15_tau2/ca15_tau1'],
#                              ],                               
#                                 file_name_sig,
#                                 file_name_bg,
#                                 fiducial_cut_sig = "(pt>150)", 
#                                 fiducial_cut_bg  = "(pt>150)",
#                                 weight_sig = "(1)",
#                                 weight_bg =  "(1)"))
#
#

#btag_setups = create_setups(btag_vars)
mass_setups = create_setups(mass_vars)
good_setups = create_setups(good_vars)
#tau_setups  = create_setups(tau_vars)

#all_setups =  tau_setups + btag_setups



if run_TMVA:
    for setup in mass_setups:
        doTMVA(setup)

plotROCMultiple("ROC_higgs_mass", mass_setups, "higgs")
plotROCMultiple("ROC_higgs_good", good_setups, "higgs")
#plotROCMultiple("ROC_higgs_tau", tau_setups, "higgs")
