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
    from TTH.Plotting.Helpers.VariableHelpers import variable
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.python.Helpers.VariableHelpers import variable

########################################
# Define Input Files and
# output directory
########################################

if socket.gethostname() == "t3ui12":
    basepath = '/shome/mameinha/TTHBB/CMSSW/src/Analysis/Feb2015/'
else:
    basepath = '/Users/gregor/'
                                         

files = {
    "tth" : ["C1_tth.root","tree"],     
    "ttj" : ["C1_ttjets.root", "tree"],
}


# for the filename: basepath + filename + .root
full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = [basepath + v[0], v[1]]

output_dir = "results/Test/"


fiducial_cut = "(((type==0 || (type==3 && flag_type3>0)) && syst==0)&&(jet_ca15softdropz20b10__pt[0]>200)&&(jet_ca15softdropz20b10__pt[1]>200)&&(jet_ca15softdropz20b10__close_hadtop_dr>1.5))*(weight)"



combinedPlot("foo",
             [plot(sample,
                   'weight',
                   fiducial_cut,
                   sample) for sample in sorted(files.keys())],
             30, 0, 10,
             label_x   = "",
             label_y   = "A.U.",
             axis_unit = "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.7, 
             legend_origin_y = 0.6,
             legend_size_x   = 0.2,
             legend_size_y   = 0.05 * 4)


doWork(full_file_names, output_dir )




