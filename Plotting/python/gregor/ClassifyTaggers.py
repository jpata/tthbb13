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

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


########################################
# Configuration
########################################

run_TMVA = True

pair_name = "pt-200-to-300"

pair = pairs[pair_name]
sample_sig = pair[0]
sample_bkg = pair[1]

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
                                    v.pretty_name,
                                    li_methods, 
                                    [v],
                                    file_name_sig,
                                    file_name_bg,
                                    fiducial_cut_sig = fiducial_cuts[sample_sig],
                                    fiducial_cut_bg  = fiducial_cuts[sample_bkg],
                                    weight_sig = "weight",
                                    weight_bg  = "weight",
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

good_setups_200_300 = create_setups(good_vars_200_300)

combined_setups = []

combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "CMSTT_combined"),
                                 "CMSTT (topMass, minMass)",
                                 ["Cuts"], 
                                 [variable.di['ca08cmstt_topMass'],
                                  variable.di['ca08cmstt_minMass']], 
                                 file_name_sig,
                                 file_name_bg,
                                 fiducial_cut_sig = fiducial_cuts[sample_sig],
                                 fiducial_cut_bg  = fiducial_cuts[sample_bkg],
                                 weight_sig = "weight",
                                 weight_bg = "weight"))

combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "HTT_combined"),
                                 "HTT (m, f_{W}, #Delta R)",
                                 ["Cuts"], 
                                 [variable.di['looseMultiRHTT_mass'],
                                  variable.di['looseMultiRHTT_fW'],
                                  variable.di['looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected']],                               
                                 file_name_sig,
                                 file_name_bg,
                                 fiducial_cut_sig = fiducial_cuts[sample_sig],
                                 fiducial_cut_bg  = fiducial_cuts[sample_bkg],
                                 weight_sig = "weight",
                                 weight_bg = "weight"))

combined_setups.append(TMVASetup("{0}_{1}_200_to_300_mass_tau".format(sample_sig, sample_bkg),
                                  "trimmed m + #tau_{3}/#tau_{2} (R=1.5)",
                                  ["Cuts"], 
                                 [variable.di['ca15trimmed_mass'],
                                  variable.di['ca15_tau3/ca15_tau2']],
                                  file_name_sig,
                                  file_name_bg,
                                  fiducial_cut_sig = fiducial_cuts[sample_sig],
                                  fiducial_cut_bg  = fiducial_cuts[sample_bkg],
                                  weight_sig = "weight",
                                  weight_bg = "weight"))

combined_setups.append(TMVASetup("{0}_{1}_200_to_300_mass_tau_qvol".format(sample_sig, sample_bkg),
                                  "trimmed m + #tau_{3}/#tau_{2} + Q-vol (R=1.5)",
                                  ["Cuts"], 
                                 [variable.di['ca15trimmed_mass'],
                                  variable.di['ca15_tau3/ca15_tau2'],
                                  variable.di['ca15_qvol'],
                              ],
                                 file_name_sig,
                                 file_name_bg,
                                 fiducial_cut_sig = fiducial_cuts[sample_sig],
                                 fiducial_cut_bg  = fiducial_cuts[sample_bkg],
                                 weight_sig = "weight",
                                 weight_bg = "weight"))




#combined_setups.append(TMVASetup("08_combined",
#                                 "softdrop m + #tau_{3}/#tau_{2} (R=0.8)",
#                                 ["Cuts"], 
#                                 [variable.di['ca08_tau3/ca08_tau2'],
#                                  variable.di['ca08softdrop_mass']],
#                                 file_name_sig,
#                                 file_name_bg,
#                                 fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                 fiducial_cut_bg  = fiducial_cuts[sample_bkg],
#                                 weight_sig = "weight",
#                                 weight_bg = "weight"))
#


with_btag_setups = []
for setup in combined_setups:
    new_setup = deepcopy(setup)

    new_setup.name = setup.name + "_btag"
    new_setup.li_methods = ["Cuts"]
    new_setup.li_vars.append(variable.di['ca08_btag'])

    with_btag_setups.append(new_setup)


if run_TMVA:
    for setup in good_setups_200_300 + combined_setups:
        doTMVA(setup)

#plotROCMultiple("ROC_good", [setup_08_combined, setup_cmstt_combined, setup_htt_combined] + good_setups + btag_setups)

#plotROCMultiple("ROC_mass", mass_setups)
#plotROCMultiple("ROC_tau", tau_setups)
#plotROCMultiple("ROC_tagger", tagger_setups + [setup_htt_combined, setup_cmstt_combined])
#
#plotROCMultiple("ROC_good", [setup_08_combined, setup_htt_combined, setup_cmstt_combined]+good_setups + btag_setups)
#plotROCMultiple("ROC_withb", combined_setups + with_btag_setups)
plotROCMultiple("ROC_" + pair_name, good_setups_200_300 + combined_setups)
