#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.MutualInformationHelpers import *
    from TTH.Plotting.Helpers.VariableHelpers import variable as var
    from TTH.Plotting.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.gregor.HiggsSamples import *
else:
    from TTH.Plotting.python.Helpers.MutualInformationHelpers import *
    from TTH.Plotting.python.Helpers.VariableHelpers import variable as var
    from TTH.Plotting.python.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.python.gregor.HiggsSamples import *


########################################
# Define Input Files and
# output directory
########################################

basepath = '/scratch/gregor/'
                                        
# for the filename: basepath + filename + .root
full_filenames = {}
for k,v in files.iteritems():
    full_filenames[k] = basepath + v + "-weighted.root"

for pair_name, pair in pairs.iteritems():
    mis =[ 
        #mi("masses_v5_"+pair_name, pair[0], pair[1], mass_vars_v5, fiducial_cuts[pair[0]], fiducial_cuts[pair[1]], diagonal_only = True),
        #mi("taus",   "tth", "ttj", tau_vars,  fiducial_cuts["tth"], fiducial_cuts["ttj"], diagonal_only = True)
        #mi("interesting",   "tth", "ttj", interesting_vars,  fiducial_cuts["tth"], fiducial_cuts["ttj"], diagonal_only = False)

        #mi("mass_vars_v7_"+pair_name, pair[0], pair[1], mass_vars_v7,  fiducial_cuts[pair[0]], fiducial_cuts[pair[1]], diagonal_only = True)
        mi("interesting_vars_v7_"+pair_name, pair[0], pair[1], interesting_vars_v7,  fiducial_cuts[pair[0]], fiducial_cuts[pair[1]], diagonal_only = False)
        

    ]

    MakePlots(mis, full_filenames)
