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

import ROOT

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


########################################
# Configuration
########################################

run_TMVA = True

basepath = '/scratch/gregor/'
file_name_sig  = basepath + "ntop_v8_zprime_m2000_1p_13tev-tagging-weighted.root"
file_name_bg   = basepath + "ntop_v8_qcd_800_1000_pythia8_13tev-tagging-weighted.root"

li_methods      = ["Fisher"]

# We want to make single-variable ROC curves
# so first create a list of variables and then send them individually to TMVA

# Masses
v = variable("ca15_mass", "m (R=1.5)", allowed_range=[0,2000])


li_TMVAs = [TMVASetup( "methods",
                       v.pretty_name,
                       li_methods, 
                       [v],
                       file_name_sig,
                       file_name_bg,
                       fiducial_cut_sig = "((pt>801)&&(pt<999))",
                       fiducial_cut_bg = "((pt>801)&&(pt<999))",
                       weight_sig = "weight",
                       weight_bg = "weight")]
    
if run_TMVA:
    doTMVA(li_TMVAs[0])

plotROCs("ROC", li_TMVAs)
