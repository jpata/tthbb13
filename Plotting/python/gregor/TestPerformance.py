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
    "pt-800-to-1000" : ["zprime_m2000", "qcd_800_1000"],
}

for pair_name, pair in pairs.iteritems():


    fiducial_cut_and_weight = "(weight*({0}))".format(fiducial_cuts[pair[0]])

    # for the filename: basepath + filename + weighted.root
    full_filenames = {}
    for k,v in files.iteritems():
        full_filenames[k] = basepath + v + "-weighted.root"

    fatjet_size = ranges[pair[0]][4]    

    mis = []


    if pair_name == "pt-300-to-470":
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

            "ca15softdropz20b10forbtag_btag",
            "log(ca15_chi2)", 
        ]
        dr_text = "#Delta R(top,parton) < 0.8"
        fn = "fixedR_MI_ROC_LikBDT4_pt-300-to-470_out_gr.dat"
        
    else:
        interesting_vars = [
            "ak08prunedn3z10rfac50_mass",
            "ak08filteredn3r2_mass", 
            "ak08softdropz10b00_mass",
            "ak08trimmedr2f3_mass", 

            "ak08_tau3/ak08_tau2",
            "ak08_qvol", 

            "looseOptRHTT_mass",
            "looseOptRHTT_fRec",
            "looseOptRHTT_Ropt-looseOptRHTT_RoptCalc", 



            "ak08cmstt_minMass",
            "ak08cmstt_topMass",
            
            "ak08softdropz10b00forbtag_btag",
            "log(ak08_chi1)", 
        ]
        dr_text = "#Delta R(top,parton) < 0.6"        
  #      fn = "fixedR_MI_ROC_high_LikBDT3_pt-800-to-1000_out_gr.dat"
        #fn = "fixedR_MI_ROC_high_TestLikBDT3_pt-800-to-1000_out_gr.dat"
        fn = "fixedR_MI_ROC_high_TestLikBDT4_pt-800-to-1000_out_gr.dat"
        
    mis.append(mi(pair_name + "_interesting_vars", 
                  [var.di[v] for v in interesting_vars],     
                  fn,
                  [pretty_fiducial_cuts[pair[0]],"flat p_{T} and #eta", dr_text],
                  error = False
              ))

    MakePlots(mis)
