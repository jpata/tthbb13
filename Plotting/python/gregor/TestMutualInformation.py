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
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import *
else:
    from TTH.Plotting.python.Helpers.MutualInformationHelpers import *
    from TTH.Plotting.python.Helpers.VariableHelpers import variable as var
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import *


########################################
# Define Input Files and
# output directory
########################################

basepath = '/scratch/gregor/'

for pair_name, pair in pairs.iteritems():

    fiducial_cut_and_weight = "(weight*({0}))".format(fiducial_cuts[pair[0]])

    # for the filename: basepath + filename + weighted.root
    full_filenames = {}
    for k,v in files.iteritems():
        full_filenames[k] = basepath + v + "-weighted.root"

    mis =[ 
        #mi(pair_name + "_taus_08", pair[0], pair[1],   tau_vars_08, fiducial_cut_and_weight, fiducial_cut_and_weight),
        #mi(pair_name + "_taus_15", pair[0], pair[1],   tau_vars_15, fiducial_cut_and_weight, fiducial_cut_and_weight),
        #mi(pair_name + "_masses_08", pair[0], pair[1], mass_vars_08, fiducial_cut_and_weight, fiducial_cut_and_weight),
        #mi(pair_name + "_masses_15", pair[0], pair[1], mass_vars_15, fiducial_cut_and_weight, fiducial_cut_and_weight),
        #mi(pair_name + "_taggers", pair[0], pair[1], tagger_vars, fiducial_cut_and_weight, fiducial_cut_and_weight),

        mi(pair_name + "_taggers", pair[0],  pair[1], good_vars_200_300, fiducial_cut_and_weight, fiducial_cut_and_weight),
    ]

    MakePlots(mis, full_filenames)
