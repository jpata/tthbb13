#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.PlotPerformanceHelper import *
    from TTH.Plotting.Helpers.VariableHelpers import variable as var
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import *
else:
    from TTH.Plotting.python.Helpers.PlotPerformanceHelper import *
    from TTH.Plotting.python.Helpers.VariableHelpers import variable as var
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import *


########################################
# Define Input Files and
# output directory
########################################

basepath = '/scratch/gregor/'

pairs = { 
    "pt-300-to-470" : ["zprime_m1000", "qcd_300_470"],
}

for pair_name, pair in pairs.iteritems():


    fiducial_cut_and_weight = "(weight*({0}))".format(fiducial_cuts[pair[0]])

    # for the filename: basepath + filename + weighted.root
    full_filenames = {}
    for k,v in files.iteritems():
        full_filenames[k] = basepath + v + "-weighted.root"

    fatjet_size = ranges[pair[0]][4]    

    mis = []



    interesting_vars = [

        "ca15prunedn3z10rfac50_mass",
        "ca15filteredn3r2_mass", 
        "ca15softdropz10b00_mass",
        "ca15trimmedr2f3_mass", 
        "ca15softdropz20b10_mass",

        "looseOptRHTT_mass",
        "looseOptRHTT_fRec",
        "looseOptRHTT_Ropt-looseOptRHTT_RoptCalc", 

        "ca15_qvol", 

        "ca15_tau3/ca15_tau2",
        "ca15softdropz20b10_tau3/ca15softdropz20b10_tau2", 

        "log(ca15_chi2)", 
    ]

    mis.append(mi(pair_name + "_interesting_vars", 
                  pair[0], pair[1], 
                  [ var.di[v] for v in interesting_vars], 
                  fiducial_cut_and_weight, fiducial_cut_and_weight,
                  read_from_pickle = False,
                  extra_text = [pretty_fiducial_cuts[pair[0]],
                                "flat p_{T} and #eta",
                                "#Delta R(top,parton) < 0.6"],

              ))

    MakePlots(mis, full_filenames)
