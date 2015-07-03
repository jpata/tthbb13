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
    from TTH.Plotting.gregor.TopSamples import *
else:
    from TTH.Plotting.python.Helpers.PlotEffsHelpers import *
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import *

# for the filename: basepath + filename + .root
full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + "-weighted.root"

########################################
# Define plots
########################################

pair_name = "pt-300-to-470"
pair = pairs[pair_name]

#plotList([plotSettings(sample,
#                       "pt",
#                       "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240)&&(ca15_tau3/ca15_tau2 < {0})&&(ca15_tau2>0) && (top_size < 0.8))".format(tau_cut),
#                       "(top_size < 0.8)",
#                       str(tau_cut)+" " + sample) for tau_cut in [0.52, 0.58, 0.66, 0.74, 0.87] for sample in ["zprime_m750", "zprime_m1000"]],
#        "pt",
#         200,
#         600,
#         30,
#         max_y               = 1.7,
#         do_legend = True,
#         legend_size_y       = 0.3,
#         legend_origin_y     = 0.61, 
#         legend_origin_x     = 0.2)
#


#plotList([plotSettings(sample,
#                       "eta",
#                       "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240)&&(ca15_tau3/ca15_tau2 < {0})&&(ca15_tau2>0) && (top_size < 0.8) && (pt > 300 ) && (pt < 370))".format(tau_cut),
#                       "(top_size < 0.8) && (pt > 300 ) && (pt < 370)",
#                       "tau_{3}/tau_{2} < " + str(tau_cut)+" " + sample) for tau_cut in [0.52, 0.58, 0.66, 0.74, 0.87] for sample in ["zprime_m750", "zprime_m1000"]],
#        "eta",
#         -2.4,
#         2.4,
#         30,
#         max_y               = 1.7,
#         xtitle              = "#eta_{Gen.} [GeV]",
#         do_legend = True,
#         legend_size_y       = 0.3,
#         legend_origin_y     = 0.61, 
#         legend_origin_x     = 0.2)
#

wps = {
    "htt_01" : "(looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180)&&(looseOptRHTT_fRec<0.13)&&(ca15_tau3/ca15_tau2<0.54)&&(ca15_tau2>0)",
    "htt_03" : "(looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180)&&(looseOptRHTT_fRec<0.14)&&(ca15_tau3/ca15_tau2<0.62)&&(ca15_tau2>0)",
    "htt_10" : "(looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180)&&(looseOptRHTT_fRec<0.18)&&(ca15_tau3/ca15_tau2<0.73)&&(ca15_tau2>0)",
    "htt_30" : "(looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180)&&(looseOptRHTT_fRec<0.39)&&(ca15_tau3/ca15_tau2<0.87)&&(ca15_tau2>0)",

    "httDR_01" : "(looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180)&&(looseOptRHTT_fRec<0.13)&&(ca15_tau3/ca15_tau2<0.58)&&(looseOptRHTT_Ropt-looseOptRHTT_RoptCalc > -0.74) && (looseOptRHTT_Ropt-looseOptRHTT_RoptCalc < 0.15) && (ca15_tau2>0)",
    "httDR_03" : "(looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180)&&(looseOptRHTT_fRec<0.14)&&(ca15_tau3/ca15_tau2<0.67)&&(looseOptRHTT_Ropt-looseOptRHTT_RoptCalc > -0.49) && (looseOptRHTT_Ropt-looseOptRHTT_RoptCalc < 0.16) && (ca15_tau2>0)",
    "httDR_10" : "(looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180)&&(looseOptRHTT_fRec<0.19)&&(ca15_tau3/ca15_tau2<0.78)&&(looseOptRHTT_Ropt-looseOptRHTT_RoptCalc > -0.67) && (looseOptRHTT_Ropt-looseOptRHTT_RoptCalc < 0.25) && (ca15_tau2>0)",
    "httDR_30" : "(looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180)&&(looseOptRHTT_fRec<0.45)&&(ca15_tau3/ca15_tau2<0.97)&&(looseOptRHTT_Ropt-looseOptRHTT_RoptCalc > -0.53) && (looseOptRHTT_Ropt-looseOptRHTT_RoptCalc < 0.38) && (ca15_tau2>0)",

    "SD_01"  : "(ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240)&&(ca15_tau3/ca15_tau2<0.52)&&(ca15_tau2>0)",
    "SD_03"  : "(ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240)&&(ca15_tau3/ca15_tau2<0.58)&&(ca15_tau2>0)",
    "SD_10"  : "(ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240)&&(ca15_tau3/ca15_tau2<0.66)&&(ca15_tau2>0)",
    "SD_30"  : "(ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240)&&(ca15_tau3/ca15_tau2<0.74)&&(ca15_tau2>0)",
}



htt_wps = []

for wp in [["01",.5], ["03",0.7], ["10",1.0], ["30",1.3] ]:
    plotList([plotSettings(sample,
                           "pt",
                           "(top_size < 0.8)&&"+cut,
                           "(top_size < 0.8)",
                           name +" " + sample) for name,cut in sorted(wps.iteritems()) if wp[0] in name for sample in ["zprime_m1000"]],
            "misc_pt" + wp[0],
             200,
             500,
             30,
             max_y               = wp[1],
             do_legend = True,
             legend_size_y       = 0.2,
             legend_origin_y     = 0.7, 
             legend_origin_x     = 0.2)

for wp in [["01",.005], ["03",0.015], ["10",0.05], ["30",0.15] ]:
    plotList([plotSettings(sample,
                           "pt",
                           cut,
                           "(1)",
                           name +" " + sample) for name,cut in sorted(wps.iteritems()) if wp[0] in name for sample in ["qcd_170_300", "qcd_300_470"]],
            "bg_pt" + wp[0],
             200,
             500,
             30,
             max_y               = wp[1],
             do_legend = True,
             legend_size_y       = 0.2,
             legend_origin_y     = 0.7, 
             legend_origin_x     = 0.2)





doPlots(full_file_names)

         

        



