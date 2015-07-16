#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.PlotProfilesHelpers import *
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import *
else:
    from TTH.Plotting.python.Helpers.PlotProfilesHelpers import *
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import *

# Overwrite imported files
files = {}
files["qcd_300_470_puppi"]   = "ntop_v59b_qcd_300_470_13tev_spring15dr74_asympt25ns-tagging" 
files["zprime_m1000_puppi"]  = "ntop_v59c_zprime_m1000_1p_13tev_spring15dr74_asympt25ns-tagging"	
files["qcd_300_470"]   = "ntop_v58a_qcd_300_470_13tev_spring15dr74_asympt25ns-tagging" 
files["zprime_m1000"]     = "ntop_v58a_zprime_m1000_1p_13tev_spring15dr74_asympt25ns-tagging"	

full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + "-weighted.root"

########################################
# Define plots and do fits
########################################

samples = [
    "zprime_m1000",      
    "qcd_300_470",
    "zprime_m1000_puppi",      
    "qcd_300_470_puppi"]


for sample in samples:

    for mass in ["ca15softdropz20b10_mass", "ca15softdropz10b00_mass", "ca15_mass"]:
        plotSettings(sample,             
                     "npv", mass,
                     fiducial_cuts[sample],
                     40, -0.5, 39.5, 50, 0, 300,
                     do_legend        = False,
                     x_label = "Number of Primary Vertices",
                     y_label =variable.di[mass].pretty_name + " [GeV]"
        )

    plotSettings(sample,             
                 "npv", "ca15_tau3/ca15_tau2",
                 fiducial_cuts[sample]+"&&(ca15_tau2>0)",
                 40, -0.5, 39.5, 50, 0, 1,
                 do_legend        = False,
                 x_label = "Number of Primary Vertices",
                 y_label = "tau_{3}/tau_{2}"
    )

makePlots(full_file_names)




