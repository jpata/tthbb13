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
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsHelpers import *


########################################
# Define Input Files and
# output directory
########################################

if socket.gethostname() == "t3ui12":
    basepath = '/scratch/gregor/'
else:
    basepath = '/Users/gregor/'

files = {}
files["tth"] = "nhiggs_v3_tth_hbb_13tev"     
files["ttj"] = "nhiggs_v3_ttj_13tev"     
                                         
# for the filename: basepath + filename + .root
full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = (basepath + v + ".root", 'tthNtupleAnalyzer/events')

output_dir = "results/HiggsDeltaR/"


########################################
# Plots
########################################

combinedPlot("deltaR",
             [plot( "ttH",     'jet_ca15__close_higgs_dr', "gen_higgs__pt>150", "tth"), 
              plot( "tt+Jets", 'jet_ca15__close_parton_dr',"gen_parton__pt>150", "ttj"), 
          ],
             80, 0, 4.5, 
             label_x   = "#Delta R(parton, jet)",
             label_y   = "Events",
             axis_unit = "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.35,
             legend_origin_y = 0.5,
             legend_size_x   = 0.2,
             legend_size_y   = 0.05 * 2)

combinedPlot("trimmed_deltaR",
             [plot( "ttH",     'jet_ca15trimmed__close_higgs_dr', "gen_higgs__pt>150", "tth"), 
              plot( "tt+Jets", 'jet_ca15trimmed__close_parton_dr',"gen_parton__pt>150", "ttj"), 
          ],
             80, 0, 4.5, 
             label_x   = "#Delta R(parton, jet)",
             label_y   = "Events",
             axis_unit = "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.35,
             legend_origin_y = 0.5,
             legend_size_x   = 0.2,
             legend_size_y   = 0.05 * 2)



doWork(full_file_names, output_dir )




