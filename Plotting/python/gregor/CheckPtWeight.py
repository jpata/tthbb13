#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import sys
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

output_dir = "/shome/gregor/new_results/CheckPtWeight/"


########################################
# Define plots and do fits
########################################

if True:


    combinedPlot("true_pt",
                 [plot( other_sample_names[sample] + " (Flat)", 
                        'pt', 
                        "(weight*({0}))".format(fiducial_cuts[sample]),
                        sample) for sample in files.keys()] + 
                 [plot( other_sample_names[sample], 
                        'pt', 
                        "(({0}))".format(fiducial_cuts[sample]),
                        sample) for sample in files.keys()],
                 30, 300, 470, 0.24,
                 label_x   = "True p_{T}",
                 label_y   = "Fraction of Partons",
                 axis_unit = "GeV",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.45,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.2,
                 legend_text_size= 0.03,
                 add_eff         = False,
    )

    combinedPlot("true_eta",
                 [plot( other_sample_names[sample] + " (Flat)", 
                        'eta', 
                        "(weight*({0}))".format(fiducial_cuts[sample]),
                        sample) for sample in files.keys()] + 
                 [plot( other_sample_names[sample],
                        'eta', 
                        "(({0}))".format(fiducial_cuts[sample]),
                        sample) for sample in files.keys()],
                 80, -2.6, 2.6, 0.04,
                 label_x   = "True #eta",
                 label_y   = "Fraction of Partons",
                 axis_unit = "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.45,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.2,
                 legend_text_size= 0.03,
                 add_eff         = False,
)
#
#
#        combinedPlot("true_pt_noweight",
#                     [plot( other_sample_names[sample], 
#                            'pt', 
#                            "(({0}))".format(fiducial_cuts[sample]),
#                            sample) for sample in files.keys()],
#                     80, ranges[sample][0], ranges[sample][1], 
#                     label_x   = "True p_{T}",
#                     label_y   = "Fraction of Partons",
#                     axis_unit = "GeV",
#                     log_y     = False,
#                     normalize = True,
#                     legend_origin_x = 0.35,
#                     legend_origin_y = 0.55,
#                     legend_size_x   = 0.2,
#                     legend_size_y   = 0.05 * 2)
#
#        combinedPlot("true_eta_noweight",
#                     [plot( other_sample_names[sample], 
#                            'eta', 
#                            "(({0}))".format(fiducial_cuts[sample]),
#                            sample) for sample in files.keys()],
#                     80, -2.6, 2.6, 
#                     label_x   = "True #eta",
#                     label_y   = "Fraction of Partons",
#                     axis_unit = "",
#                     log_y     = False,
#                     normalize = True,
#                     legend_origin_x = 0.35,
#                     legend_origin_y = 0.3,
#                     legend_size_x   = 0.2,
#                     legend_size_y   = 0.05 * 2)
#
#    samples = [x for x in files.keys() if "zprime" in x]
#    var = variable.di["top_size"]
#    combinedPlot(("top_size"),
#                 [plot(sample,
#                       var.name,                                           
#                       '((pt>{0})&&(pt<{1})&&(abs(eta)<{2})&&({3}))*weight'.format(ranges[sample][0], 
#                                                                                   ranges[sample][1],
#                                                                                   ranges[sample][2],
#                                                                                   var.extra_cut),
#                       sample) for sample in samples],
#                 80, var.range_min, var.range_max, 
#                 label_x   = var.pretty_name,
#                 label_y   = "A.U.",
#                 axis_unit = var.unit,
#                 log_y     = False,
#                 normalize = True,
#                 legend_origin_x = 0.6,
#                 legend_origin_y = 0.7,
#                 legend_size_x   = 0.2,
#                 legend_size_y   = 0.05*len(samples))
#
doWork(full_file_names, output_dir )




