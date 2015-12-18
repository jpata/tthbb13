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
    from TTH.Plotting.Helpers.PlotEffsHelpers import *
    from TTH.Plotting.gregor.TopTaggingVariables import *
else:
    from TTH.Plotting.python.Helpers.PlotEffsHelpers import *
    from TTH.Plotting.python.gregor.TopTaggingVariables import *

basepath = '/scratch/gregor/'
full_file_names = {}
full_file_names["zprime_m1000"] = basepath + "ntop_v64_zprime_m1000_1p_13tev_spring15dr74_asympt25ns.root"
full_file_names["zprime_m1000_truth"] = basepath + "ntop_v64_zprime_m1000_1p_13tev_spring15dr74_asympt25ns-tagging.root"
full_file_names["zprime_m2000_truth"] = basepath + "ntop_v64_zprime_m2000_1p_13tev_spring15dr74_asympt25ns-tagging.root"

########################################
# Define plots
########################################


#plotList([plotSettings("zprime_m1000",
#                       "gen_hadtop__pt[0]",
#                       [ "0",
#                         "(jet_ca15__close_hadtop_i[0]==0 && jet_ca15__close_hadtop_dr[0] < 0.8) && (n__jet_ca15 == 1)",
#                         "((jet_ca15__close_hadtop_i[0]==0 && jet_ca15__close_hadtop_dr[0] < 0.8) || (jet_ca15__close_hadtop_i[1]==0 && jet_ca15__close_hadtop_dr[1] < 0.8)) && (n__jet_ca15 == 2)"
#                    ],
#                       ["(n__jet_ca15 == 0)",
#                        "(n__jet_ca15 == 1)",
#                        "(n__jet_ca15 == 2)",
#                    ],
#                       ev_weight = ["(1)","(1)","(1)"],
#                       legend = "CA (R=1.5)",
#                       input_treename     = "tthNtupleAnalyzer/events"
#                   ),
#          plotSettings("zprime_m1000",
#                       "gen_hadtop__pt[0]",
#                       [ "0",
#                         "(jet_ak08__close_hadtop_i[0]==0 && jet_ak08__close_hadtop_dr[0] < 0.8) && (n__jet_ak08 == 1)",
#                         "((jet_ak08__close_hadtop_i[0]==0 && jet_ak08__close_hadtop_dr[0] < 0.8) || (jet_ak08__close_hadtop_i[1]==0 && jet_ak08__close_hadtop_dr[1] < 0.8)) && (n__jet_ak08 == 2)"
#                    ],
#                       ["(n__jet_ak08 == 0)",
#                        "(n__jet_ak08 == 1)",
#                        "(n__jet_ak08 == 2)",
#                    ],
#                       ev_weight = ["(1)","(1)","(1)"],
#                       legend = "AK (R=0.8)",
#                       input_treename     = "tthNtupleAnalyzer/events"
#                   ),
#      ],
#         "dr_pt",
#         200,
#         500,
#         30,
#         max_y               = 1.25,
#         do_legend = True,
#         legend_size_y       = 0.15,
#         legend_origin_y     = 0.6, 
#         legend_origin_x     = 0.7,
#         xtitle              = "Hadronic Top p_{T}  [GeV]",
#         ytitle              = "Jet Reconstruction Efficiency",
#        
#)
#

plotList([
    plotSettings("zprime_m2000_truth",
                 "hadtop_pt",
                [ "(dr_ca15 < 1.2)",],
                 ["(1)",],
                 ev_weight = ["(1)"],
                 legend = "#DeltaR(top, CA15) < 1.2"),
    plotSettings("zprime_m2000_truth",
                 "hadtop_pt",
                 [ "(dr_ak08 < 0.6)",],
                 ["(1)",],
                 ev_weight = ["(1)"],
                legend = "#DeltaR(top, AK8) < 0.6",),
##          plotSettings("zprime_m2000_truth",
##                       "hadtop_pt",
##                       [ "(dr_ak08 < 0.8)",],
##                       ["(1)",],
##                       ev_weight = ["(1)"],
##                       legend = "AK, R=0.8, All, 2 TeV",),

    plotSettings("zprime_m2000_truth",
                 "hadtop_pt",
                 [ "(top_size < 0.6)",],
                 ["(1)",],
                 ev_weight = ["(1)"],
                 legend = "max #DeltaR(top, q) < 0.6",),
    plotSettings("zprime_m2000_truth",
                 "hadtop_pt",
                 [ "(top_size < 0.8)",],
                 ["(1)",],
                 ev_weight = ["(1)"],
                 legend = "max #DeltaR(top, q) < 0.8",),
#    plotSettings("zprime_m2000_truth",
#                 "hadtop_pt",
#                 [ "(top_size < 1.0)",],
#                 ["(1)",],
#                 ev_weight = ["(1)"],
#                 legend = "max #Delta R(top, q) < 1.0",),
#    plotSettings("zprime_m2000_truth",
#                 "hadtop_pt",
#                 [ "(top_size < 1.2)",],
#                 ["(1)",],
#                 ev_weight = ["(1)"],
#                 legend = "max #Delta R(top, q) < 1.2",),
    #          plotSettings("zprime_m2000_truth",
    #                       "hadtop_pt",
    #                       [ "(dr_ak08 < 0.8 && top_size < 0.6)",],
    #                       ["(top_size < 0.6)",],
    #                       ev_weight = ["(1)"],
    #                       legend = "AK, R=0.8, Merged 2 TeV",),    
      ],
         "dr_pt",
         200,
         1000,
         40,
         max_y               = 1.35,
         do_legend = True,
         legend_size_y       = 0.15,
         legend_origin_y     = 0.19, 
         legend_origin_x     = 0.49,
         xtitle              = "Top Quark p_{T}  [GeV]",
         ytitle              = "Efficiency",
        
)



#
#plotList([plotSettings("zprime_m2000_truth",
#                       "hadtop_pt",
#                       [ "(dr_ca15 < 1.2)",],
#                       ["(1)",],
#                       ev_weight = ["(1)"],
#                       legend = "CA R=1.5, all top"),
#          plotSettings("zprime_m2000_truth",
#                       "hadtop_pt",
#                       [ "(dr_ak08 < 0.6)",],
#                       ["(1)",],
#                       ev_weight = ["(1)"],
#                       legend = "AK, R=0.8, all top",),
#          plotSettings("zprime_m2000_truth",
#                       "hadtop_pt",
#                       [ "(top_size < 0.8 && dr_ca15 < 1.2)",],
#                       ["(top_size < 0.8)",],
#                       ev_weight = ["(1)"],
#                       legend = "CA R=1.5, merged top",),
#          plotSettings("zprime_m2000_truth",
#                       "hadtop_pt",
#                       [ "(top_size < 0.6 && dr_ak08 < 0.6)",],
#                       ["(top_size < 0.6)",],
#                       ev_weight = ["(1)"],
#                       legend = "AK R=0.8, merged top",),
#
#
#      ],
#         "dr_pt",
#         200,
#         500,
#         30,
#         max_y               = 1.25,
#         do_legend = True,
#         legend_size_y       = 0.15,
#         legend_origin_y     = 0.3, 
#         legend_origin_x     = 0.5,
#         xtitle              = "Hadronic Top p_{T}  [GeV]",
#         ytitle              = "Jet Reconstruction Efficiency",
#        
#)
#




doPlots(full_file_names)

         

        



