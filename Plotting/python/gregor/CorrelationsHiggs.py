#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.CorrelationHelpers import *
    from TTH.Plotting.Helpers.VariableHelpers import variable as var
    from TTH.Plotting.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.gregor.HiggsSamples import files, fiducial_cuts
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.CorrelationHelpers import *
    from TTH.Plotting.python.Helpers.VariableHelpers import variable as var
    from TTH.Plotting.python.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.python.gregor.HiggsSamples import files, fiducial_cuts


########################################
# Define Input Files and
# output directory
########################################

basepath = '/scratch/gregor/'

# for the filename: basepath + filename + .root
full_filenames = {}
for k,v in files.iteritems():
    full_filenames[k] = basepath + v + "-weighted.root"

corrs = []
for sample in full_filenames.keys():
    corrs.append(corr("good", sample, good_vars, fiducial_cuts[sample]))


MakePlots(corrs, full_filenames)
