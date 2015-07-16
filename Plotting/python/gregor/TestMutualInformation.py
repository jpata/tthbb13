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

    fatjet_size = ranges[pair[0]][4]    

    mis = []



    interesting_vars_ca15 = [

        #"ca15_mass",        

        "ca15prunedn3z10rfac50_mass",
        "ca15filteredn3r2_mass",
        "ca15trimmedr2f3_mass",
        "ca15softdropz10b00_mass",
        "ca15softdropz20b10_mass",

        "ca15_tau3/ca15_tau2",    
        "ca15softdropz20b10_tau3/ca15softdropz20b10_tau2",    
        "ca15_qvol",

        "looseOptRHTT_mass",
        "looseOptRHTT_fRec",
        "looseOptRHTT_Ropt-looseOptRHTT_RoptCalc",

        "log(ca15_chi2)",

        #"ca15softdropz20b10forbtag_btag",
    ]



    interesting_vars_ak08 = [
            #"ak08_mass",        

            "ak08prunedn3z10rfac50_mass",
            "ak08filteredn3r2_mass",
            "ak08trimmedr2f3_mass",
            "ak08softdropz10b00_mass",

            "ak08_tau3/ak08_tau2",    
            "ak08_qvol",

            "looseOptRHTT_mass",
            "looseOptRHTT_fRec",
            "looseOptRHTT_Ropt-looseOptRHTT_RoptCalc",

            "ak08cmstt_minMass",
            "ak08cmstt_topMass",

            "log(ak08_chi1)",
    ]



    #mis.append(mi(pair_name + "_interesting_vars_ca15_fixedR", 
    #              pair[0], pair[1], 
    #              [ var.di[v] for v in interesting_vars_ca15], 
    #              fiducial_cut_and_weight, fiducial_cut_and_weight,
    #              read_from_pickle = True,
    #          ))


    mis.append(mi(pair_name + "_interesting_vars_ak08", 
                  pair[0], pair[1], 
                  [ var.di[v] for v in interesting_vars_ak08], 
                  fiducial_cut_and_weight, fiducial_cut_and_weight,
                  read_from_pickle = False,
              ))

    MakePlots(mis, full_filenames)
