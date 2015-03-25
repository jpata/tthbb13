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
    from TTH.Plotting.gregor.HiggsSamples import *
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCMultiple
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.python.gregor.HiggsSamples import *

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


########################################
# Configuration
########################################

run_TMVA = True

for pair_name in ["pt-170-to-300"]:

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
                                        fiducial_cut_sig = fiducial_cuts[pair[0]],
                                        fiducial_cut_bg  = fiducial_cuts[pair[1]],
                                        weight_sig = "(1)",
                                        weight_bg  = "(1)",
                                    ))
        return li_TMVAs
    # end of create_setups

    #variable.di["ca15_tau2/ca15_tau1"].pretty_name = "Ungroomed #tau_{3}/#tau_{2}"

    setups = []
    #create_setups([
        #variable.di["ca15_mass"],
    #    variable.di["ca15trimmedr2f6_mass"],
        #variable.di["ca15softdropz20b10_mass"],
        #variable.di["ca15_tau2/ca15_tau1"],
    #])

    #setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "sd_tau"),
    #                        "Softdrop m + Q-jet Volatility",
    #                        ["Cuts"], 
    #                        [variable.di['ca15softdropz20b10_mass'],
    #                         variable.di['ca15_qvol'],
    #                     ],                               
    #                        file_name_sig,
    #                        file_name_bg,
    #                        fiducial_cut_sig = fiducial_cuts[pair[0]],
    #                        fiducial_cut_bg  = fiducial_cuts[pair[1]],
    #                        weight_sig = "(1)",
    #                        weight_bg =  "(1)"))

    setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "sd_tau"),
                            "trimmed m + tau_{2}/tau_{1}",
                            ["Cuts"], 
                            [variable.di['ca15trimmedr2f6_mass'],
                             variable.di['ca15_tau2/ca15_tau1'],
                         ],                               
                            file_name_sig,
                            file_name_bg,
                            fiducial_cut_sig = fiducial_cuts[pair[0]],
                            fiducial_cut_bg  = fiducial_cuts[pair[1]],
                            weight_sig = "(1)",
                            weight_bg =  "(1)"))
    #
    #setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "sd_tau_qvol"),
    #                        "softdrop m + unfiltered tau_{2}/tau_{1} + Q-vol",
    #                        ["Cuts"], 
    #                        [variable.di['ca15softdropz20b10_mass'],
    #                         variable.di['ca15_tau2/ca15_tau1'],
    #                         variable.di['ca15_qvol'],
    #                     ],                               
    #                        file_name_sig,
    #                        file_name_bg,
    #                        fiducial_cut_sig = fiducial_cuts[pair[0]],
    #                        fiducial_cut_bg  = fiducial_cuts[pair[1]],
    #                        weight_sig = "(1)",
    #                        weight_bg =  "(1)"))
    #

    if run_TMVA:
        for setup in setups:
            doTMVA(setup)

    plotROCMultiple("ROC_higgs_" + pair_name, setups, "higgs")
    #plotROCMultiple("ROC_higgs_good", good_setups, "higgs")
    #plotROCMultiple("ROC_higgs_tau", tau_setups, "higgs")
