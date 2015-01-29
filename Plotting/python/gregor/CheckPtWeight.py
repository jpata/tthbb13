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

if False:
    for sample in files.keys():
        combinedPlot(sample + "_true_pt",
                     [plot( sample,
                            'pt', 
                            '((pt>{0})&&(pt<{1}))*weight'.format(ranges[sample][0], 
                                                                 ranges[sample][1]),
                            sample), 
                  ],
                     80, ranges[sample][0], ranges[sample][1], 
                     label_x   = "True p_{T}",
                     label_y   = "Partons",
                     axis_unit = "GeV",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.35,
                     legend_origin_y = 0.3,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * 2)



for var in htt_vars: 

    combinedPlot(var.pretty_name.replace("/","_").replace(" ", "_").replace("{","").replace("}",""),
             [plot(sample,
                   var.name,                                           
                   '((pt>{0})&&(pt<{1})&&({2}))*weight'.format(ranges[sample][0], 
                                                               ranges[sample][1],
                                                               var.extra_cut),
                   sample) for sample in files.keys()],
                 80, var.range_min, var.range_max, 
                 label_x   = var.pretty_name,
                 label_y   = "A.U.",
                 axis_unit = var.unit,
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.6,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.2,
                 legend_size_y   = 0.05*6)


for sample in files.keys():
    continue

    fiducial_cut = '((pt>{0})&&(pt<{1}))*weight'.format(ranges[sample][0], 
                                                        ranges[sample][1])
    
    if True:
        name = "mass_vars_15"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           fiducial_cut,
                           sample) for var in collection],
                     80, collection[0].range_min, collection[0].range_max, 
                     label_x   = "Mass",
                     label_y   = "A.U.",
                     axis_unit = "GeV",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.45,
                     legend_origin_y = 0.45,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * len(collection))

    if True:
        name = "mass_vars_08"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           fiducial_cut,
                           sample) for var in collection],
                     80, collection[0].range_min, collection[0].range_max, 
                     label_x   = "Mass",
                     label_y   = "A.U.",
                     axis_unit = "GeV",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.5,
                     legend_origin_y = 0.5,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * len(collection))

    if True:
        name = "tau_vars_08"
        collection = globals()[name]
        if "qcd" in sample:
            do_legend = True
        else:
            do_legend = False
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           fiducial_cut,
                           sample) for var in collection],
                     80, collection[0].range_min, collection[0].range_max, 
                     label_x   = "#tau_{3}/#tau_{2}",
                     label_y   = "A.U.",
                     axis_unit = "",
                     log_y     = False,
                     normalize = True,
                     draw_legend = do_legend,
                     legend_origin_x = 0.2,
                     legend_origin_y = 0.5,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * len(collection))

    if True:
        name = "tau_vars_15"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,    
                           fiducial_cut,                
                           sample) for var in collection],
                     80, collection[0].range_min, collection[0].range_max, 
                     label_x   = "#tau_{3}/#tau_{2}",
                     label_y   = "A.U.",
                     axis_unit = "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.2,
                     legend_origin_y = 0.5,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * len(collection))

    if True:
        name = "cmstt_vars"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           fiducial_cut,                
                           sample) for var in collection],
                     80, collection[0].range_min, 600, 
                     label_x   = "Mass",
                     label_y   = "A.U.",
                     axis_unit = "GeV",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.4,
                     legend_origin_y = 0.5,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * len(collection))

    if False:
        name = "sd_vars"
        collection = globals()[name]
        if "qcd" in sample:
            leg_x = 0.6
        else:
            leg_x = 0.2
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           '((pt>{0})&&(pt<{1})&&{2})*weight'.format(ranges[sample][0], 
                                                                     ranges[sample][1],
                                                                     var.extra_cut),
                           sample) for var in collection],
                     80, collection[0].range_min, collection[0].range_max, 
                     label_x   = "Shower Deconstruction log(#chi)",
                     label_y   = "A.U.",
                     axis_unit = "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = leg_x, 
                     legend_origin_y = 0.5,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * len(collection))

    if True:
        name = "btag_vars"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,          
                           fiducial_cut,                          
                           sample) for var in collection],
                     80, collection[0].range_min, collection[0].range_max, 
                     label_x   = "b-tag Discriminator",
                     label_y   = "A.U.",
                     axis_unit = "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.55,
                     legend_origin_y = 0.45,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * len(collection))

doWork(full_file_names, output_dir )




