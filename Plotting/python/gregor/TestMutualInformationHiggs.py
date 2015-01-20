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
    full_filenames[k] = basepath + v + ".root"

mis =[ 
    #mi("masses", "tth", "ttj", mass_vars, fiducial_cuts["tth"], fiducial_cuts["ttj"]),
    mi("taus",   "tth", "ttj", tau_vars + [variable.di["ca15trimmed_mass"]] ,  fiducial_cuts["tth"], fiducial_cuts["ttj"])
]

MakePlots(mis, full_filenames)
