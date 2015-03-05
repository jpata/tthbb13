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

output_dir = "results/CheckPtWeight/"


########################################
# Define plots and do fits
########################################




for var in mass_vars_v36: #cmstt_vars_v36 + nsub_vars_v36 + qvol_vars_v36 + 
    continue

    samples = ['zprime_m1000', 'zprime_m2000_low', 'zprime_m2000', "qcd_300_470", "qcd_470_600", "qcd_600_800"]        
    samples = [s for s in samples if ranges[s][4] in var.name]
        
    combinedPlot(var.pretty_name.replace("/","_").replace(" ", "_").replace("{","").replace("}",""),
             [plot(sample_names[sample],
                   var.name,                                           
                   '({0}&&{1})*weight'.format(fiducial_cuts[sample], var.extra_cut),
                   sample) for sample in samples] +
             [plot(sample_names[sample]  + ", Phys14", 
                   var.name,                                           
                   '({0}&&{1})*weight'.format(fiducial_cuts[sample], var.extra_cut),
                   sample + "_phys14") for sample in samples],
                 80, var.range_min, var.range_max, 
                 label_x   = var.pretty_name,
                 label_y   = "A.U.",
                 axis_unit = var.unit,
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.57,
                 legend_origin_y = 0.65,
                 legend_size_x   = 0.2,
                 legend_size_y   = 0.03*len(samples)*2,
                 legend_text_size= 0.03)


if True:
    samples = ['zprime_m1000', "qcd_300_470"]        

    if True:
        combinedPlot("npv",
                 [plot(sample_names[sample],
                       "npv",                                           
                       '({0})*weight'.format(fiducial_cuts[sample]),
                       sample) for sample in samples] +
                 [plot(sample_names[sample]  + ", Phys14", 
                       "npv",                                           
                       '({0}&&{1})*weight'.format(fiducial_cuts[sample], var.extra_cut),
                       sample + "_phys14") for sample in samples],
                     80, 0, 40, 
                     label_x   = "NPV",
                     label_y   = "A.U.",
                     axis_unit = "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.57,
                     legend_origin_y = 0.65,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.03*len(samples)*2,
                     legend_text_size= 0.03)



    if False:
        combinedPlot("true_pt",
                     [plot(sample_names[sample],
                           "pt",                                           
                           '({0})*weight'.format(fiducial_cuts[sample]),
                           sample) for sample in samples] +
                     [plot(sample_names[sample]  + ", Phys14", 
                           "pt",
                           '({0}&&{1})*weight'.format(fiducial_cuts[sample], var.extra_cut),
                           sample + "_phys14") for sample in samples],
                     80, ranges[sample][0], ranges[sample][1], 
                     label_x   = "True p_{T}",
                     label_y   = "Partons",
                     axis_unit = "GeV",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.35,
                     legend_origin_y = 0.3,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * 4)

    if False:
        combinedPlot("true_eta",
                     [plot(sample_names[sample],
                           "eta",                                           
                           '({0})*weight'.format(fiducial_cuts[sample]),
                           sample) for sample in samples] +
                     [plot(sample_names[sample]  + ", Phys14", 
                           "eta",
                           '({0}&&{1})*weight'.format(fiducial_cuts[sample], var.extra_cut),
                           sample + "_phys14") for sample in samples],
                     80, -2.6, 2.6,
                     label_x   = "True #eta",
                     label_y   = "Partons",
                     axis_unit = "GeV",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.35,
                     legend_origin_y = 0.3,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * 4)

doWork(full_file_names, output_dir )




