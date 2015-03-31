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
    from TTH.Plotting.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.gregor.HiggsSamples import files, pairs, fiducial_cuts
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.python.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.python.gregor.HiggsSamples import files, pairs, fiducial_cuts


########################################
# Define Input Files and
# output directory
########################################

if socket.gethostname() == "t3ui12":
    basepath = '/scratch/gregor/'
else:
    basepath = '/Users/gregor/'
                                         
full_file_names = {"tth":  [basepath + "ntop_v41_tth_hbb_13tev-tagging.root","tthNtupleAnalyzer/events"]}

output_dir = "results/PtPlot/"


########################################
# Plots
########################################

combinedPlot("pt",
             [plot( "Top", 
                    "gen_hadtop__pt",
                    "(1)", 
                    "tth"),
              plot( "Higgs", 
                    "gen_higgs__pt",
                    "(1)", 
                    "tth")],
             100, 0, 500, 
             label_x   = "True p_{T} ",
             label_y   = "A.U.",
             axis_unit = "GeV",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.6,
             legend_origin_y = 0.6,
             legend_size_x   = 0.2,
             legend_text_size= 0.05,
         )




    





doWork(full_file_names, output_dir )




