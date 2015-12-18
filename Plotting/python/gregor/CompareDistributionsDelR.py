#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import sys
import pickle
import socket # to get the hostname

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import *
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import *


########################################
# Define Input Files and
# output directory
########################################


basepath = '/scratch/gregor/'
full_file_names = {}
full_file_names["zprime_m1000"] = [basepath + "ntop_v64_zprime_m1000_1p_13tev_spring15dr74_asympt25ns.root",
                                   "tthNtupleAnalyzer/events"]

output_dir = "results/CompareDistributionsDelR/"
               
combinedPlot("del_r",
             [plot("CA15",
                   "jet_ca15__close_hadtop_dr",                                           
                   "(1)",
                   "zprime_m1000"),
              plot("AK8",
                   "jet_ak08__close_hadtop_dr",                                           
                   "(1)",
                   "zprime_m1000"),

          ],
             39, 0, 1.3, 1.,
             label_x   = "#DeltaR (Jet, Top Quark)",
             label_y   = "A.U.",
             axis_unit = "",
             log_y     = True,
             normalize = True,
             legend_origin_x = 0.7,
             legend_origin_y = 0.7,
             legend_size_x   = 0.2,
             legend_text_size= 0.04,
             add_eff = False,
             
)

doWork(full_file_names, output_dir )




