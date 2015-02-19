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

    #if not pair_name == "pt-200-to-300":
    #    continue

    #if not pair_name == "pt-470-to-600":
    #    continue

    if not pair_name == "pt-800-to-1000":
        continue

    fiducial_cut_and_weight = "(weight*({0}))".format(fiducial_cuts[pair[0]])

    # for the filename: basepath + filename + weighted.root
    full_filenames = {}
    for k,v in files.iteritems():
        full_filenames[k] = basepath + v + "-weighted.root"

    fatjet_size = ranges[pair[0]][4]

    

    mis = []
    # mis.append(mi(pair_name + "_mass_vars", 
    #               pair[0], pair[1], 
    #               [v for v in mass_vars_v27 if fatjet_size in v.name], 
    #               fiducial_cut_and_weight, fiducial_cut_and_weight, True))
    # mis.append(mi(pair_name + "_support_vars", 
    #               pair[0], pair[1], 
    #               [v for v in qvol_vars_v27+nsub_vars_v27 if fatjet_size in v.name], 
    #               fiducial_cut_and_weight, fiducial_cut_and_weight, True))
    # mis.append(mi(pair_name + "_cmstt_vars", 
    #               pair[0], pair[1], 
    #               [v for v in cmstt_vars_v27 if fatjet_size in v.name], 
    #               fiducial_cut_and_weight, fiducial_cut_and_weight, True))
    mis.append(mi(pair_name + "_interesting", 
                  pair[0], pair[1], 
                  ineresting_highpt_vars_v27,
                  fiducial_cut_and_weight, fiducial_cut_and_weight))

    


#
#mis =[ 
#    #mi(pair_name + "_taus_08", pair[0], pair[1],   tau_vars_08, fiducial_cut_and_weight, fiducial_cut_and_weight),
#    #mi(pair_name + "_taus_15", pair[0], pair[1],   tau_vars_15, fiducial_cut_and_weight, fiducial_cut_and_weight),
#    #mi(pair_name + "_masses_08", pair[0], pair[1], mass_vars_08, fiducial_cut_and_weight, fiducial_cut_and_weight),
#    #mi(pair_name + "_masses_15", pair[0], pair[1], mass_vars_15, fiducial_cut_and_weight, fiducial_cut_and_weight),
#    #mi(pair_name + "_taggers", pair[0], pair[1], tagger_vars, fiducial_cut_and_weight, fiducial_cut_and_weight),
#
#    #mi(pair_name + "_interesting", pair[0], pair[1], interesting_vars_470_600,fiducial_cut_and_weight,fiducial_cut_and_weight),
#    #mi(pair_name + "_htt", pair[0], pair[1], htt_vars,fiducial_cut_and_weight, fiducial_cut_and_weight),
#
#    #mi(pair_name + "_new_masses_08", pair[0], pair[1], new_mass_vars_08, fiducial_cut_and_weight, fiducial_cut_and_weight, True),
#    #mi(pair_name + "_new_masses_15", pair[0], pair[1], new_mass_vars_15, fiducial_cut_and_weight, fiducial_cut_and_weight, True),
#
#    #mi(pair_name + "_mass_vars_08_v21", pair[0], pair[1], mass_vars_08_v21, fiducial_cut_and_weight, fiducial_cut_and_weight, True),
#    #mi(pair_name + "_mass_vars_15_v21", pair[0], pair[1], mass_vars_15_v21, fiducial_cut_and_weight, fiducial_cut_and_weight, True),
#
#    #mi(pair_name + "_mass_vars_v27", pair[0], pair[1], mass_vars_v27, fiducial_cut_and_weight, fiducial_cut_and_weight, True),
#
#    #mi(pair_name + "_mass_vars_v27_ca08", pair[0], pair[1], mass_vars_v27_ca08, fiducial_cut_and_weight, fiducial_cut_and_weight, True),
#    #mi(pair_name + "_mass_vars_v27_ca15", pair[0], pair[1], mass_vars_v27_ca15, fiducial_cut_and_weight, fiducial_cut_and_weight, True),
#
#    #mi(pair_name + "_mass_vars_v27_ca08puppi", pair[0], pair[1], mass_vars_v27_ca08puppi, fiducial_cut_and_weight, fiducial_cut_and_weight, True),
#    #mi(pair_name + "_mass_vars_v27_ca15puppi", pair[0], pair[1], mass_vars_v27_ca15puppi, fiducial_cut_and_weight, fiducial_cut_and_weight, True),
#
#
#    #mi(pair_name + "_taggers", pair[0],  pair[1], good_vars_200_300, fiducial_cut_and_weight, fiducial_cut_and_weight),
#    #mi(pair_name + "_taggers", pair[0],  pair[1], good_vars_470_600, fiducial_cut_and_weight, fiducial_cut_and_weight),
#    #mi(pair_name + "_good", pair[0],  pair[1], good_vars_800_1000, fiducial_cut_and_weight, fiducial_cut_and_weight),
#]

    MakePlots(mis, full_filenames)
