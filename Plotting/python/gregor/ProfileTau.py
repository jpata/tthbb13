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
files["qcd_300_470"]   = "ntop_v61_zprime_m1000_1p_13tev_spring15dr74_asympt25ns-tagging" 
files["zprime_m1000"]  = "ntop_v61_qcd_300_470_13tev_spring15dr74_asympt25ns-tagging"	

full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + "-weighted.root"

########################################
# Define plots and do fits
########################################

samples = [
    "zprime_m1000",      
    "qcd_300_470",]


for sample in samples:


    plotSettings(sample,             
                 "ca15_tau3/ca15_tau2", "(ca15_tau3/ca15_tau2-ca15softdropz20b10_tau3/ca15softdropz20b10_tau2)/(ca15_tau3/ca15_tau2)", 
                 fiducial_cuts[sample]+"&&(ca15_tau2>0)&&(ca15softdropz20b10_tau2>0)&&(ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240)",
                 50, 0, 1, 50, -1, 1,
                 do_legend        = False,
                 x_label = "Ungroomed tau_{3}/tau_{2}",
                 y_label = "#Delta tau_{3}/tau_{2}"
    )

makePlots(full_file_names)




