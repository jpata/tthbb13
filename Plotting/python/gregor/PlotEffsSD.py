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


if False:
    wps = {
        "sd1 Tight" : "((ca15_chi1>0)&&log(ca15_chi1)>5)",
        "sd2 Tight" : "((ca15_chi2>0)&&log(ca15_chi2)>5)",
        "sd3 Tight" : "((ca15_chi3>0)&&log(ca15_chi3)>5)",

        "sd1 Medium" : "((ca15_chi1>0)&&log(ca15_chi1)>3)",
        "sd2 Medium" : "((ca15_chi2>0)&&log(ca15_chi2)>3)",
        "sd3 Medium" : "((ca15_chi3>0)&&log(ca15_chi3)>3)",
    }

    plotList([plotSettings(sample,
                           "pt",
                           "(top_size < 0.8)&&"+cut,
                           "(top_size < 0.8)",
                           name +" " + sample) for name,cut in sorted(wps.iteritems()) for sample in ["zprime_m1000"]],
            "sd_truept_signal_lowpt",
             200,
             500,
             30,
             max_y               = 1.,
             do_legend = True,
             legend_size_y       = 0.2,
             legend_origin_y     = 0.7, 
             legend_origin_x     = 0.2)

    plotList([plotSettings(sample,
                           "pt",
                           cut,
                           "(1)",
                           name +" " + sample) for name,cut in sorted(wps.iteritems()) for sample in ["qcd_300_470"]],
            "sd_truept_bg_lowpt",
             200,
             500,
             30,
             max_y               = .01,
             do_legend = True,
             legend_size_y       = 0.2,
             legend_origin_y     = 0.7, 
             legend_origin_x     = 0.2)

if True:
    wps = {
        "sd1" : "((ak08_chi1>0)&&log(ak08_chi1)>5)",
        "sd2" : "((ak08_chi2>0)&&log(ak08_chi2)>5)",
        "sd3" : "((ak08_chi3>0)&&log(ak08_chi3)>5)",
    }

    plotList([plotSettings(sample,
                           "pt",
                           "(top_size < 0.6)&&"+cut,
                           "(top_size < 0.6)",
                           name +" " + sample) for name,cut in sorted(wps.iteritems()) for sample in ["zprime_m2000"]],
            "sd_truept_signal_highpt",
             400,
             1200,
             30,
             max_y               = 1.,
             do_legend = True,
             legend_size_y       = 0.2,
             legend_origin_y     = 0.7, 
             legend_origin_x     = 0.2)


    plotList([plotSettings(sample,
                           "ak08_pt",
                           "(top_size < 0.6)&&"+cut,
                           "(top_size < 0.6)",
                           name +" " + sample) for name,cut in sorted(wps.iteritems()) for sample in ["zprime_m2000"]],
            "sd_recopt_signal_highpt",
             400,
             1200,
             30,
             max_y               = 1.,
             do_legend = True,
             legend_size_y       = 0.2,
             legend_origin_y     = 0.7, 
             legend_origin_x     = 0.2)


    for sample in ["qcd_470_600", "qcd_600_800", "qcd_800_1000", "qcd_1000_1400"]:
        plotList([plotSettings(sample,
                               "pt",
                               cut,
                               "(1)",
                               name +" " + sample) for name,cut in sorted(wps.iteritems())],
                "sd_truept_{0}_highpt".format(sample),
                 400,
                 1200,
                 30,
                 max_y               = .01,
                 do_legend = True,
                 legend_size_y       = 0.2,
                 legend_origin_y     = 0.7, 
                 legend_origin_x     = 0.2)


        plotList([plotSettings(sample,
                               "ak08_pt",
                               cut,
                               "(1)",
                               name +" " + sample) for name,cut in sorted(wps.iteritems())],
                "sd_recopt_{0}_highpt".format(sample),
                 400,
                 1200,
                 30,
                 max_y               = .01,
                 do_legend = True,
                 legend_size_y       = 0.2,
                 legend_origin_y     = 0.7, 
                 legend_origin_x     = 0.2)






doPlots(full_file_names)

         

        



