#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import pickle
import socket # to get the hostname

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.gregor.HiggsSamples import files, pairs, fiducial_cuts
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.python.gregor.HiggsTaggingVariables import *
    from TTH.Plotting.python.gregor.HiggsSamples import files, pairs, fiducial_cuts


########################################
# Define Input Files and
# output directory
########################################

if socket.gethostname() == "t3ui12":
    basepath = '/scratch/gregor/'
else:
    basepath = '/Users/gregor/'
                                         
full_file_names = {"tth":  [basepath + "ntop_v41_tth_hbb_13tev-tagging.root","tthNtupleAnalyzer/events"],
                   "wjets_400_600" : [basepath + "ntop_v45c_wjets_lnu_ht_400_600_13tev_phys14_20bx25-tagging.root", "tree"],
                   "wjets_600_inf" : [basepath + "ntop_v45c_wjets_lnu_ht_600_inf_13tev_phys14_20bx25-tagging.root", "tree"],                
}

output_dir = "/shome/gregor/new_results/PtPlot/"


########################################
# Plots
########################################

#combinedPlot("pt",
#             [plot( "Top", 
#                    "gen_hadtop__pt",
#                    "(1)", 
#                    "tth"),
#              plot( "Higgs", 
#                    "gen_higgs__pt",
#                    "(1)", 
#                    "tth")],
#             100, 0, 500, 
#             label_x   = "True p_{T} ",
#             label_y   = "A.U.",
#             axis_unit = "GeV",
#             log_y     = False,
#             normalize = True,
#             legend_origin_x = 0.6,
#             legend_origin_y = 0.6,
#             legend_size_x   = 0.2,
#             legend_text_size= 0.05,
#         )

combinedPlot("pt",
             [plot( "400..600", 
                    "parton_pt",
                    "(1)", 
                    "wjets_400_600"),
              plot( "600..inf", 
                    "parton_pt",
                    "(1)", 
                    "wjets_600_inf")],
             100, 200, 800, 
             label_x   = "Parton p_{T}",
             label_y   = "Number of Partons",
             axis_unit = "GeV",
             log_y     = False,
             normalize = False,
             legend_origin_x = 0.6,
             legend_origin_y = 0.6,
             legend_size_x   = 0.2,
             legend_text_size= 0.05,
         )

combinedPlot("eta",
             [plot( "200..300 (from 400..600)", 
                    "parton_eta",
                    "(parton_pt>200)&&(parton_pt<300)", 
                    "wjets_400_600"),
              plot( "200..300 (from 600..inf)", 
                    "parton_eta",
                    "(parton_pt>200)&&(parton_pt<300)", 
                    "wjets_600_inf"),
              plot( "300..470 (from 600..inf)", 
                    "parton_eta",
                    "(parton_pt>300)&&(parton_pt<470)", 
                    "wjets_600_inf"),
              plot( "600..800 (from 600..inf)", 
                    "parton_eta",
                    "(parton_pt>600)&&(parton_pt<800)", 
                    "wjets_600_inf")],
             40, -3, 3, 
             label_x   = "Parton #eta",
             label_y   = "A.U.",
             axis_unit = "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.63,
             legend_origin_y = 0.65,
             legend_size_x   = 0.2,
             legend_text_size= 0.03,
         )




    





doWork(full_file_names, output_dir )




