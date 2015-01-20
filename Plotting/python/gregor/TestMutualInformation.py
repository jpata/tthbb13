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

fiducial_cut_and_weight = "(weight*((pt>801)&&(pt<999)))"
                                        
# for the filename: basepath + filename + weighted.root
full_filenames = {}
for k,v in files.iteritems():
    full_filenames[k] = basepath + v + "-weighted.root"

mis =[ 
    #mi("taus_08", "zprime_m2000_1p", "qcd_800_1000",   tau_vars_08 + tau_cross_vars, fiducial_cut_and_weight, fiducial_cut_and_weight),
    #mi("taus_15", "zprime_m2000_1p", "qcd_800_1000",   tau_vars_15, fiducial_cut_and_weight, fiducial_cut_and_weight),
    #mi("masses_08", "zprime_m2000_1p", "qcd_800_1000",   mass_vars_08, fiducial_cut_and_weight, fiducial_cut_and_weight),
    #mi("masses_15", "zprime_m2000_1p", "qcd_800_1000",   mass_vars_15, fiducial_cut_and_weight, fiducial_cut_and_weight),
    #mi("taggers", "zprime_m2000_1p", "qcd_800_1000", tagger_vars, fiducial_cut_and_weight, fiducial_cut_and_weight),
    mi("good_top", "zprime_m2000", "qcd_800_1000", good_vars + [variable.di['ca08_btag'],], fiducial_cut_and_weight, fiducial_cut_and_weight),
]

MakePlots(mis, full_filenames)
