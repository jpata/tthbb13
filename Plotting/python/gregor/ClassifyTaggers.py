#!/usr/bin/env python
"""
Schedule the testing of different variable/method-sets with TMVA
"""

########################################
# Imports 
########################################

import pickle
import os

import ROOT

# Our support Code
# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCMultiple
    from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.gregor.TopTaggingVariables import *
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCMultiple
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.TopTaggingVariables import *

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


########################################
# Configuration
########################################

run_TMVA = True

basepath = '/scratch/gregor/'
file_name_sig  = basepath + "ntop_v14_zprime_m2000_1p_13tev-tagging-weighted.root"
file_name_bg   = basepath + "ntop_v14_qcd_800_1000_pythia8_13tev-tagging-weighted.root"

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
tau31_setups_15  = create_setups(tau31_vars_15)
tagger_setups_15 = create_setups(tagger_vars_15)
all_setups_15 = create_setups(all_vars_15)

mass_setups_08 = create_setups(mass_vars_08)
tau_setups_08  = create_setups(tau_vars_08)
tau31_setups_08  = create_setups(tau31_vars_08)
tagger_setups_08 = create_setups(tagger_vars_08)
all_setups_08 = create_setups(all_vars_08)

btag_setups = create_setups(btag_vars)

good_setups = create_setups(good_vars)
cmstt_setups = create_setups(cmstt_vars)

all_setups = all_setups_08 + all_setups_15 + btag_setups

mass_setups = mass_setups_08 + mass_setups_15
tau_setups = tau_setups_08 + tau_setups_15
tagger_setups = tagger_setups_08 + tagger_setups_15


setup_htt_combined = TMVASetup("HTT_combined",
                               "HTT (m, f_{W})",
                               ["Cuts"], 
                               [variable.di['looseMultiRHTT_mass'],
                                variable.di['looseMultiRHTT_fW'],
                                #variable.di['looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected']
                            ],                               
                               file_name_sig,
                               file_name_bg,
                               fiducial_cut_sig = "((pt>801)&&(pt<999))",
                               fiducial_cut_bg  = "((pt>801)&&(pt<999))",
                               weight_sig = "weight",
                               weight_bg = "weight")
#doTMVA(setup_htt_combined)

setup_cmstt_combined = TMVASetup("CMSTT_combined",
                               "CMSTT (topMass, minMass)",
                               ["Cuts"], 
                               [variable.di['ca08cmstt_topMass'],
                                variable.di['ca08cmstt_minMass']], 
                               file_name_sig,
                               file_name_bg,
                               fiducial_cut_sig = "((pt>801)&&(pt<999))",
                               fiducial_cut_bg  = "((pt>801)&&(pt<999))",
                               weight_sig = "weight",
                               weight_bg = "weight")
#doTMVA()

setup_08_combined = TMVASetup("08_combined",
                              "softdrop m + #tau_{3}/#tau_{2} (R=0.8)",
                              ["Cuts"], 
                              [variable.di['ca08_tau3/ca08_tau2'],
                               variable.di['ca08softdrop_mass']],
                              file_name_sig,
                              file_name_bg,
                              fiducial_cut_sig = "((pt>801)&&(pt<999))",
                              fiducial_cut_bg  = "((pt>801)&&(pt<999))",
                              weight_sig = "weight",
                              weight_bg = "weight")
#doTMVA(setup_08_combined)

setup_08_combined2 = TMVASetup("08_combined2",
                              "softdrop m + #tau_{3}/#tau_{2} + .. (R=0.8)",
                              ["Cuts"], 
                              [variable.di['ca08_tau3/ca08_tau2'],
                               variable.di['ca08softdrop_tau3/ca08_tau2'],
                               variable.di['ca08softdrop_mass']],
                              file_name_sig,
                              file_name_bg,
                              fiducial_cut_sig = "((pt>801)&&(pt<999))",
                              fiducial_cut_bg  = "((pt>801)&&(pt<999))",
                              weight_sig = "weight",
                              weight_bg = "weight")
#doTMVA(setup_08_combined2)

setup_softdrop_b = TMVASetup("softdrop_b",
                              "softdrop m + b-tag (R=0.8)",
                              ["Cuts"], 
                              [variable.di['ca08_btag'],
                               variable.di['ca08softdrop_mass']],
                              file_name_sig,
                              file_name_bg,
                              fiducial_cut_sig = "((pt>801)&&(pt<999))",
                              fiducial_cut_bg  = "((pt>801)&&(pt<999))",
                              weight_sig = "weight",
                              weight_bg = "weight")
#doTMVA(setup_softdrop_b)



if run_TMVA:
    for setup in btag_setups:
        doTMVA(setup)

plotROCMultiple("ROC_good", [setup_08_combined, setup_cmstt_combined, setup_htt_combined] + good_setups + btag_setups)

plotROCMultiple("ROC_mass", mass_setups)
plotROCMultiple("ROC_tau", tau_setups)
plotROCMultiple("ROC_tau31", tau31_setups_08 + tau31_setups_15)
plotROCMultiple("ROC_tagger", tagger_setups)
