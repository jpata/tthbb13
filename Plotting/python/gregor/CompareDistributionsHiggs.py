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
    from TTH.Plotting.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.gregor.HiggsSamples import *
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.python.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.python.gregor.HiggsSamples import *

########################################
# Define Input Files and
# output directory
########################################

if socket.gethostname() == "t3ui12":
    basepath = '/scratch/gregor/'
else:
    basepath = '/Users/gregor/'
                                         
# for the filename: basepath + filename + .root
full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + "-weighted.root"

output_dir = "results/CompareDistributions/"

samples = ["rad_hh4b_m800_170_300",              
           "rad_hh4b_m800_300_470",   
           "rad_hh4b_m1600_470_600",  
           "rad_hh4b_m1600_600_800", 
           "qcd_170_300",             
           "qcd_300_470",             
           "qcd_470_600",             
           "qcd_600_800",             
       ]

for var in [
       # "pt",
        
       #"X_tau2/X_tau1", 
       #
       #"Xtrimmedr2f6_tau2/X_tau1", 
       #"X_tau2/Xtrimmedr2f6_tau1", 
       #"Xtrimmedr2f6_tau2/Xtrimmedr2f6_tau1", 
       #
       #"Xsoftdropz10b00_tau2/X_tau1", 
       #"X_tau2/Xsoftdropz10b00_tau1", 
       #"Xsoftdropz10b00_tau2/Xsoftdropz10b00_tau1", 
       #
       #"Xsoftdropz15b10_tau2/X_tau1", 
       #"X_tau2/Xsoftdropz15b10_tau1", 
       #"Xsoftdropz15b10_tau2/Xsoftdropz15b10_tau1", 

        #"X_qvol",
        # "X_mass",
        "Xtrimmedr2f6_mass",
        #"Xsoftdropz10b00_mass",
        #"Xsoftdropz15b10_mass",
]:
    

    if var=="X_mass":
        xpos = 0.60
    elif  var == "log(X_chi)":
        xpos = 0.23
    else:
        xpos = 0.62
        
        
    if True:
        combinedPlot(var.replace("/","_"),
                     [plot(sample_names[sample],
                           variable.di[var.replace("X",ranges[sample][2])].name,                                           
                           '({0}&&{1})*weight'.format(fiducial_cuts[sample], variable.di[var.replace("X",ranges[sample][2])].extra_cut),
                           sample) for sample in samples],
                     80, variable.di[var.replace("X",ranges[sample][2])].range_min, variable.di[var.replace("X",ranges[sample][2])].range_max, 
                     label_x   = variable.di[var.replace("X",ranges[sample][2])].pretty_name,
                     label_y   = "A.U.",
                     axis_unit = variable.di[var.replace("X",ranges[sample][2])].unit,
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = xpos,
                     legend_origin_y = 0.6,
                     legend_size_x   = 0.2,
                     legend_text_size= 0.025)



doWork(full_file_names, output_dir )




