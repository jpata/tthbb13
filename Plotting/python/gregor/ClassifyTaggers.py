#!/usr/bin/env python
"""
Schedule the testing of different variable/method-sets with TMVA
"""

########################################
# Imports 
########################################

import pickle

from TTH.Plotting.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCs
from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
from TTH.Plotting.gregor.TopTaggingVariables import *

import ROOT

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


########################################
# Configuration
########################################

run_TMVA = False

basepath = '/scratch/gregor/'
file_name_sig  = basepath + "ntop_v8_zprime_m2000_1p_13tev-tagging-weighted.root"
file_name_bg   = basepath + "ntop_v8_qcd_800_1000_pythia8_13tev-tagging-weighted.root"

li_methods      = ["Likelihood"]


# We want to make single-variable ROC curves
# so first create a list of variables and then send them individually to TMVA
    
def create_setups(li_vars):
    li_TMVAs = []
    for v in li_vars:
        name = v.name.replace("/","_")
        li_TMVAs.append( TMVASetup( name,
                                    v.pretty_name,
                                    li_methods, 
                                    [v],
                                    file_name_sig,
                                    file_name_bg,
                                    fiducial_cut_sig = "((pt>801)&&(pt<999))",
                                    fiducial_cut_bg = "((pt>801)&&(pt<999))",
                                    weight_sig = "weight",
                                    weight_bg = "weight",
                                ))
    return li_TMVAs
# end of create_setups
    
mass_setups_15 = create_setups(mass_vars_15)
tau_setups_15  = create_setups(tau_vars_15)
tagger_setups_15 = create_setups(tagger_vars_15)
all_setups_15 = create_setups(all_vars_15)

mass_setups_08 = create_setups(mass_vars_08)
tau_setups_08  = create_setups(tau_vars_08)
tagger_setups_08 = create_setups(tagger_vars_08)
all_setups_08 = create_setups(all_vars_08)

all_setups = all_setups_08 + all_setups_15

mass_setups = mass_setups_08 + mass_setups_15
tau_setups = tau_setups_08 + tau_setups_15
tagger_setups = tagger_setups_08 + tagger_setups_15



if run_TMVA:
    for setup in all_setups:
        doTMVA(setup)

#plotROCs("ROC_mass", mass_setups)
#plotROCs("ROC_tau", tau_setups)
#plotROCs("ROC_tagger", tagger_setups)
#plotROCs("ROC_all_08", all_setups_08)
#plotROCs("ROC_all_08_zoom", all_setups_08, True)

plotROCs("ROC_all_15", all_setups_15)
plotROCs("ROC_all_15_zoom", all_setups_15, True)

#plotROCs("ROC_all", all_setups_08 + tagger_setups_15)
#plotROCs("ROC_all_zoom", all_setups_08 + tagger_setups_15, True)
