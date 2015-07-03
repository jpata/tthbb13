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
    from TTH.Plotting.Helpers.Plot2DHelpers import *
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import *
else:
    from TTH.Plotting.python.Helpers.Plot2DHelpers import *
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
full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + "-weighted.root"

########################################
# Define Input Files and
# output directory
########################################

plots = []

for sample in ["zprime_m1000", "qcd_300_470"]:
  
    plots.append( plot( 
        "mass_vs_tau_ungroomed_{0}".format(sample), 
        'ca15softdropz20b10_mass', 
        'ca15_tau3/ca15_tau2', 
        fiducial_cuts[sample]+'*(weight)', 
        sample, 
        40, 0, 300,
        40, 0, 1,
        log_z      = True,
        normalize  = True,
        label_x = "Softdrop(z=0.2, #beta=1) Mass [GeV]",
        label_y = "#tau_{3} /  #tau_{2} (Ungroomed)",
    ))

    plots.append( plot( 
        "prunedmass_vs_tau_ungroomed_{0}".format(sample), 
        'ca15prunedn3z10rfac50_mass', 
        'ca15_tau3/ca15_tau2', 
        fiducial_cuts[sample]+'*(weight)', 
        sample, 
        40, 0, 300,
        40, 0, 1,
        log_z      = True,
        normalize  = True,
        label_x = "Pruned Mass [GeV]",
        label_y = "#tau_{3} /  #tau_{2} (Ungroomed)",
    ))


    plots.append( plot( 
        "mass_vs_tau_groomed_{0}".format(sample), 
        'ca15softdropz20b10_mass', 
        'ca15softdropz20b10_tau3/ca15softdropz20b10_tau2', 
        fiducial_cuts[sample]+'*(weight)', 
        sample, 
        40, 0, 300,
        40, 0, 1,
        log_z      = True,
        normalize  = True,
        label_x = "Softdrop(z=0.2, #beta=1) Mass [GeV]",
        label_y = "#tau_{3} /  #tau_{2} (Groomed)",
    ))


   

MakePlots(full_file_names, plots )
