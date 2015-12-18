#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import pickle
import socket # to get the hostname

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.PlotEffsHelpers import *
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import *
else:
    from TTH.Plotting.python.Helpers.PlotEffsHelpers import *
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import *


files = {}
files["qcd_pythia6"]      = "ntop_v61_qcd_pythia6_flat_13tev_spring15dr74_asympt25ns-tagging"	
files["qcd_pythia8"]      = "ntop_v61_qcd_pythia8_flat_13tev_spring15dr74_asympt25ns-tagging"


full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + ".root"

########################################
# Define plots
########################################



plotList([plotSettings(sample,
                       "parton_pt",
                       "(ak08softdropz10b00_mass>110) && (ak08softdropz10b00_mass<210) && (ak08_tau3/ak08_tau2 > 0.0) && (ak08_tau3/ak08_tau2 < 0.5) && (fabs(parton_eta) < 1.5)",
                       "(fabs(parton_eta) < 1.5)",
                       sample) for sample in ["qcd_pythia6", "qcd_pythia8"]],
        "test",
         200,
         2000,
         100,
         max_y               = 0.006,
         rebin = 20 * [1] + 10*[2] + 5 * [4] + 4 * [10], 
         do_legend = True,
         legend_size_y       = 0.2,
         legend_origin_y     = 0.7, 
         legend_origin_x     = 0.2)





doPlots(full_file_names)

         

        



