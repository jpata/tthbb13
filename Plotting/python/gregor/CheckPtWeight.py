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
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.python.gregor.TopTaggingVariables import *


########################################
# Define Input Files and
# output directory
########################################

if socket.gethostname() == "t3ui12":
    basepath = '/scratch/gregor/'
else:
    basepath = '/Users/gregor/'

files = {}
files["qcd_800_1000"] = "ntop_v14_qcd_800_1000_pythia8_13tev-tagging-weighted"
files["zprime_m2000"] = "ntop_v14_zprime_m2000_1p_13tev-tagging-weighted"     
                                         
# for the filename: basepath + filename + .root
full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + ".root"

output_dir = "results/CheckPtWeight/"


########################################
# Define plots and do fits
########################################

if False:
    combinedPlot("true_top_pt_cut",
                 [plot( "zprime_m2000", 
                        'hadtop_pt', 
                        '((hadtop_pt>800)&&(hadtop_pt<1000))*weight', 
                        "zprime_m2000"), 
              ],
                 80, 750, 1050, 
                 label_x   = "True top p_{T}",
                 label_y   = "Events",
                 axis_unit = "GeV",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.35,
                 legend_origin_y = 0.3,
                 legend_size_x   = 0.2,
                 legend_size_y   = 0.05 * 2)

if False:
    combinedPlot("parton_pt_cut",
                 [plot( "qcd_800_1000", 
                        'parton_pt', 
                        '((parton_pt>800)&&(parton_pt<1000))*weight', 
                        "qcd_800_1000")],
                 80, 750, 1050, 
                 label_x   = "Parton p_{T}",
                 label_y   = "Events",
                 axis_unit = "GeV",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.32,
                 legend_origin_y = 0.25,
                 legend_size_x   = 0.2,
                 legend_size_y   = 0.05 * 2)



for var in htt_vars: 
    continue
    
    if ("chi" in var.name or 
        "tau" in var.name
    ):
        leg_x = 0.2
    else:
        leg_x = 0.55

    combinedPlot(var.name.replace("/","_"),
             [plot(sample,
                   var.name,                                           
                   '((pt>800)&&(pt<1000)&&({0}))*weight'.format(var.extra_cut),
                   sample) for sample in files.keys()],
                 80, var.range_min, var.range_max, 
                 label_x   = var.pretty_name,
                 label_y   = "A.U.",
                 axis_unit = var.unit,
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = leg_x,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.2,
                 legend_size_y   = 0.05*2)


for sample in files.keys():
    
    if False:
        name = "mass_vars_15"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           '((pt>800)&&(pt<1000))*weight',
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

    if False:
        name = "mass_vars_08"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           '((pt>800)&&(pt<1000))*weight',
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

    if False:
        name = "tau_vars_08"
        collection = globals()[name]
        if "qcd" in sample:
            do_legend = True
        else:
            do_legend = False
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           '((pt>800)&&(pt<1000))*weight',
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

    if False:
        name = "tau_vars_15"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           '((pt>800)&&(pt<1000))*weight',
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

    if False:
        name = "cmstt_vars"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           '((pt>800)&&(pt<1000))*weight',
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
                           '((pt>800)&&(pt<1000)&&({0}))*weight'.format(var.extra_cut),
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
                           '((pt>800)&&(pt<1000))*weight',
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




