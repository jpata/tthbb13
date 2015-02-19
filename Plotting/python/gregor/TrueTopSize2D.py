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

for sample in files.keys():
    if not "zprime" in sample:
        continue
  


    plots.append( plot( 
        "ca15_mass_{0}".format(sample), 
        'top_size', 
        'ca15_mass', 
        '(weight)', 
        sample, 
        60, 0, 3,
        60, 0, 600,
        log_z   = True,
        normalize   = True,
        label_x = "Top Size",
        label_y = "Mass",
    ))

    plots.append( plot( 
        "ca15_softdropz15b00_{0}".format(sample), 
        'top_size', 
        'ca15softdropz15b00_mass', 
        '(weight)', 
        sample, 
        60, 0, 3,
        60, 0, 600,
        log_z   = True,
        normalize   = True,
        label_x = "Top Size",
        label_y = "Mass",
    ))


    plots.append( plot( 
        "ca08_mass_{0}".format(sample), 
        'top_size', 
        'ca08_mass', 
        '(weight)', 
        sample, 
        60, 0, 3,
        60, 0, 600,
        log_z   = True,
        normalize   = True,
        label_x = "Top Size",
        label_y = "Mass",
    ))

    plots.append( plot( 
        "ca08_softdropz15b00_{0}".format(sample), 
        'top_size', 
        'ca08softdropz15b00_mass', 
        '(weight)', 
        sample, 
        60, 0, 3,
        60, 0, 600,
        log_z   = True,
        normalize   = True,
        label_x = "Top Size",
        label_y = "Mass",
    ))


   

MakePlots(full_file_names, plots )
