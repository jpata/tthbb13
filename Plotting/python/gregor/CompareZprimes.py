#!/usr/bin/env python
"""
Plots to compare the effect of using either Z'(2 TeV) or Z'(3 TeV) for the 800..1000 GeV top.
For 2 TeV the tops are close to the threshold, for 3 TeV they're from a mostly flat spectrum.
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
# Define Input Files and
# output directory
########################################

if socket.gethostname() == "t3ui12":
    basepath = '/scratch/gregor/'
else:
    basepath = '/Users/gregor/'
                                         
# for the filename: basepath + filename + .root
full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + "-weighted.root"

output_dir = "results/CompareZprimes/"


########################################
# Define plots and do fits
########################################

if True:
    for pair_name, pair in pairs.iteritems():
    
        combinedPlot("true_pt_" + pair_name,
                     [plot(sample,
                           'pt', 
                           '({0})*weight'.format(fiducial_cuts[sample]),
                           sample) for sample in pair],
                     80, ranges[sample][0], ranges[sample][1], 
                     label_x   = "True top p_{T}",
                     label_y   = "True Tops",
                     axis_unit = "GeV",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.35,
                     legend_origin_y = 0.3,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * 2)

        combinedPlot("true_eta_" + pair_name,
                     [plot(sample,
                           'eta', 
                           '((pt>{0})&&(pt<{1})&&(fabs(eta)<2.5))*weight'.format(ranges[sample][0], 
                                                                                 ranges[sample][1]),
                           sample) for sample in pair],
                     80, -3, 3, 0.07,
                     label_x   = "True #eta",
                     label_y   = "True Partons",
                     axis_unit = "GeV",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.35,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * 3)

        combinedPlot("true_eta_cut_" + pair_name,
                     [plot(sample,
                           'eta', 
                           '({0})*weight'.format(fiducial_cuts[sample]),
                           sample) for sample in pair], 
                     80, -2, 2, 0.04,
                     label_x   = "True #eta",
                     label_y   = "True Partons",
                     axis_unit = "GeV",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.35,
                     legend_origin_y = 0.6,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * 3)





for var in all_vars: 
    continue

    combinedPlot(var.name.replace("/","_"),
             [plot(sample,
                   var.name,                                           
                   '({0})*weight'.format(fiducial_cuts[sample]),
                   sample) for sample in interesting_samples],
                 80, var.range_min, var.range_max, 
                 label_x   = var.pretty_name,
                 label_y   = "A.U.",
                 axis_unit = var.unit,
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.6,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.2,
                 legend_size_y   = 0.05*2)


doWork(full_file_names, output_dir )




