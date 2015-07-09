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
                     40, -0.5, 39.5, 50, 0, 200,
                     do_legend        = False,
        )

    plotSettings(sample,             
                 "npv", "ca15_tau3/ca15_tau2",
                 fiducial_cuts[sample]+"&&(ca15_tau2>0)",
                 40, -0.5, 39.5, 50, 0, 1,
                 do_legend        = False,
    )

makePlots(full_file_names)




