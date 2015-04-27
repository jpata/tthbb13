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

if socket.gethostname() == "t3ui12":
    basepath = '/scratch/gregor/'
else:
    basepath = '/Users/gregor/'
                                         
# for the filename: basepath + filename + .root
full_file_names = {"tth" : basepath + "tree.root"}

output_dir = "results/CompareDistributionsDelR/"


        
        

combinedPlot("del_r",
             [plot("#Delta R(jet, light)",
                   "GenQFromW_jet_delR",                                           
                   "(1)",
                   "tth"),
              plot("#Delta R(subjet, light)",
                   "GenQFromW_subjet_delR",                                           
                   "(1)",
                   "tth"),
              plot("#Delta R(jet, b)",
                   "GenBFromTop_jet_delR",                                           
                   "(1)",
                   "tth"),
              plot("#Delta R(subjet, b)",
                   "GenBFromTop_subjet_delR",                                           
                   "(1)",
                   "tth"),
          ],
             50, 0, .3, 
             label_x   = "#Delta R",
             label_y   = "A.U.",
             axis_unit = "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.55,
             legend_origin_y = 0.5,
             legend_size_x   = 0.2,
             legend_text_size= 0.04)

doWork(full_file_names, output_dir )




