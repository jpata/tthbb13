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
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import *
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import *


########################################
# Define plots
########################################

output_dir = "results/PlotTopVars/"

pair_name = "pt-200-to-300"
pair = pairs[pair_name]


low_pt_mass_vars = [
    variable.di['ca15_mass'],
    variable.di['ca15trimmed_mass'],
    variable.di['ca15softdrop_mass'],
    variable.di['ca15newsoftdrop_mass'],
]



combinedPlot(pair_name + "_masses",
             [plot(sample +" " + var.pretty_name,
                   var.name,                                           
                   '((pt>{0})&&(pt<{1})&&({2}))*weight'.format(ranges[sample][0], 
                                                               ranges[sample][1],
                                                               var.extra_cut),
                   sample) for sample in pair for var in low_pt_mass_vars],
             60, 0, 600, 
             label_x   = "Mass",
             label_y   = "A.U.",
             axis_unit = "GeV",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.5,
             legend_origin_y = 0.5,
             legend_text_size= 0.02)

doWork(weighted_files, output_dir)




