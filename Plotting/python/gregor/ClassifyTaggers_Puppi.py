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
    from TTH.Plotting.gregor.TopSamples import ranges, fiducial_cuts, pretty_fiducial_cuts
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCs
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import ranges, fiducial_cuts, pretty_fiducial_cuts


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

# Overwrite imported files
files = {}
files["qcd_300_470_puppi"]   = "ntop_v59b_qcd_300_470_13tev_spring15dr74_asympt25ns-tagging" 
files["zprime_m1000_puppi"]  = "ntop_v59c_zprime_m1000_1p_13tev_spring15dr74_asympt25ns-tagging"	
files["qcd_300_470"]   = "ntop_v58a_qcd_300_470_13tev_spring15dr74_asympt25ns-tagging" 
files["zprime_m1000"]     = "ntop_v58a_zprime_m1000_1p_13tev_spring15dr74_asympt25ns-tagging"	


pairs = { 
    "pt-300-to-470" : ["zprime_m1000", "qcd_300_470"],
    "pt-300-to-470-puppi" : ["zprime_m1000_puppi", "qcd_300_470_puppi"],
}


setups = []

for pair_name, pair in pairs.iteritems():
    sample_sig = pair[0]
    sample_bkg = pair[1]

    basepath = '/scratch/gregor/'
    file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
    file_name_bkg  = basepath + files[sample_bkg] + "-weighted.root"

    li_methods      = ["Cuts"]

    for mass_var in ["ca15softdropz20b10_mass"]:

        if "puppi" in pair_name:
            objects = "PUPPI"
        else:
            objects = "CHS"

        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_" + mass_var + "Mass_Tau_ComparePuppi"),
                          variable.di[mass_var].pretty_name + " + #tau_{3}/#tau_{2} " + objects,
                          [["Cuts", "V:FitMethod=MC:SampleSize=100000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:CutRangeMin[1]=0:CutRangeMax[1]=200:VarProp[0]=FSmart"]], 
                          [variable.di['ca15_tau3/ca15_tau2'],
                           variable.di[mass_var],
                       ],
                          [],
                          file_name_sig,
                          file_name_bkg,
                          fiducial_cut_sig = fiducial_cuts[sample_sig],
                          fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                          weight_sig = "(weight)",
                          weight_bkg = "(weight)",
                          draw_roc = DRAW_ROC,
                          working_points = [],
                          manual_working_points = [])
        setups.append(setup)
        
        groomed_taus = {"ca15softdropz20b10_mass" : 'ca15softdropz20b10_tau3/ca15softdropz20b10_tau2',
                        "ca15softdropz10b00_mass" : 'ca15softdropz10b00_tau3/ca15softdropz10b00_tau2'}

        
        setup = TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "Truth_" + mass_var + "Mass_Groomed_Tau_ComparePuppi"),
                          variable.di[mass_var].pretty_name + " + Groomed #tau_{3}/#tau_{2} " + objects,
                          [["Cuts", "V:FitMethod=MC:SampleSize=100000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:CutRangeMin[1]=0:CutRangeMax[1]=200:VarProp[0]=FSmart"]], 
                          [variable.di[groomed_taus[mass_var]],
                           variable.di[mass_var],
                       ],
                          [],
                          file_name_sig,
                          file_name_bkg,
                          fiducial_cut_sig = fiducial_cuts[sample_sig],
                          fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                          weight_sig = "(weight)",
                          weight_bkg = "(weight)",
                          draw_roc = DRAW_ROC,
                          working_points = [],
                          manual_working_points = [])
        setups.append(setup)

#pool.map(doTMVA, setups)
plotROCs("truth_PUPPI_ROC_" + pair_name, setups, 
         extra_text = [pretty_fiducial_cuts[sample_sig],
                       "flat p_{T} and #eta",
                       "#Delta R(top,parton) < 0.8"],
         error_band = False)





