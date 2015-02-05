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
                                         
# for the filename: basepath + filename + .root
full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + "-weighted.root"

output_dir = "results/HiggsPlots/"


########################################
# Plots
########################################


if False:
    combinedPlot("ca15softdropz20b10_mass",
                 [plot( pair[0], 'ca15softdropz20b10_mass',  fiducial_cuts[pair[0]], pair[0]) for pair in sorted(pairs.values())] + 
                 [plot( pair[1], 'ca15softdropz20b10_mass',  fiducial_cuts[pair[1]], pair[1]) for pair in sorted(pairs.values())],
                 50, 0, 600, 
                 label_x   = "Mass",
                 label_y   = "A.U.",
                 axis_unit = "GeV",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.4,
                 legend_size_x   = 0.2,
                 legend_size_y   = 0.05 * 6)

if False:
    combinedPlot("ca15trimmedr2f6_mass",
                 [plot( pair[0], 'ca15trimmedr2f6_mass',  fiducial_cuts[pair[0]], pair[0]) for pair in sorted(pairs.values())] + 
                 [plot( pair[1], 'ca15trimmedr2f6_mass',  fiducial_cuts[pair[1]], pair[1]) for pair in sorted(pairs.values())],
                 50, 0, 600, 
                 label_x   = "Mass",
                 label_y   = "A.U.",
                 axis_unit = "GeV",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.4,
                 legend_size_x   = 0.2,
                 legend_size_y   = 0.05 * 6)

if False:
    combinedPlot("ca15_qvol",
                 [plot( pair[0], 'ca15_qvol',  fiducial_cuts[pair[0]], pair[0]) for pair in sorted(pairs.values())] + 
                 [plot( pair[1], 'ca15_qvol',  fiducial_cuts[pair[1]], pair[1]) for pair in sorted(pairs.values())],
                 50, 0, 1, 
                 label_x   = "Q-Jet Volatility",
                 label_y   = "A.U.",
                 axis_unit = "GeV",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.4,
                 legend_size_x   = 0.2,
                 legend_size_y   = 0.05 * 6)
if False:
    combinedPlot("ca15_nsub",
                 [plot( pair[0], 'ca15_tau2/ca15_tau1',  fiducial_cuts[pair[0]], pair[0]) for pair in sorted(pairs.values())] + 
                 [plot( pair[1], 'ca15_tau2/ca15_tau1',  fiducial_cuts[pair[1]], pair[1]) for pair in sorted(pairs.values())],
                 50, 0, 1, 
                 label_x   = "#tau_{2}/#tau_{1}",
                 label_y   = "A.U.",
                 axis_unit = "GeV",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.22,
                 legend_origin_y = 0.4,
                 legend_size_x   = 0.2,
                 legend_size_y   = 0.05 * 6)

combinedPlot("ca15_nsub_valid",
             [plot( pair[0], 'ca15_tau1>0',  fiducial_cuts[pair[0]], pair[0]) for pair in sorted(pairs.values())] + 
             [plot( pair[1], 'ca15_tau1>0',  fiducial_cuts[pair[1]], pair[1]) for pair in sorted(pairs.values())],
             15, -.05, 1.05, 
             label_x   = "#tau_{1} > 0",
             label_y   = "A.U.",
             axis_unit = "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.22,
             legend_origin_y = 0.4,
             legend_size_x   = 0.2,
             legend_size_y   = 0.05 * 6)




if False:
    combinedPlot("true_pt",
                 [plot( "ttH",     'higgs_pt',  fiducial_cuts["tth"], "tth"), 
                  plot( "tt+Jets", 'parton_pt', fiducial_cuts["ttj"], "ttj")],
                 50, 150, 600, 
                 label_x   = "True p_{T}",
                 label_y   = "Events",
                 axis_unit = "GeV",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.35,
                 legend_origin_y = 0.3,
                 legend_size_x   = 0.2,
                 legend_size_y   = 0.05 * 2)


if False:
    for var in other_vars:
        combinedPlot(var.pretty_name.replace("/","_").replace(" ","_"),
                     [plot( "ttH",     var.name, fiducial_cuts["tth"], "tth"), 
                      plot( "tt+Jets", var.name, fiducial_cuts["ttj"], "ttj")],
                     80, var.range_min, var.range_max, 
                     label_x   = var.pretty_name,
                     label_y   = "",
                     axis_unit = "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.35,
                     legend_origin_y = 0.3,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * 2)


if False:
    for var in mass_vars:
        combinedPlot(var.pretty_name.replace("/","_").replace(" ","_"),
                     [plot( "ttH",     var.name, fiducial_cuts["tth"], "tth"), 
                      plot( "tt+Jets", var.name, fiducial_cuts["ttj"], "ttj")],
                     80, var.range_min, var.range_max, 
                     label_x   = var.pretty_name,
                     label_y   = "",
                     axis_unit = "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.35,
                     legend_origin_y = 0.3,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * 2)

if False:
    for var in tau_vars:
        combinedPlot(var.pretty_name.replace("/","_").replace(" ","_"),
                     [plot( "ttH",     var.name, fiducial_cuts["tth"], "tth"), 
                      plot( "tt+Jets", var.name, fiducial_cuts["ttj"], "ttj")],
                     80, var.range_min, var.range_max, 
                     label_x   = var.pretty_name,
                     label_y   = "",
                     axis_unit = "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.35,
                     legend_origin_y = 0.3,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * 2)



for sample in files.keys():
    
    if False:
        name = "mass_vars"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           fiducial_cuts[sample],
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
        name = "tau_vars"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           fiducial_cuts[sample],
                           sample) for var in collection],
                     80, collection[0].range_min, collection[0].range_max, 0.14, 
                     label_x   = "#tau_{2}/#tau_{1}",
                     label_y   = "A.U.",
                     axis_unit = "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.2,
                     legend_origin_y = 0.45,
                     legend_size_x   = 0.2,
                     legend_size_y   = 0.05 * len(collection))

    if False:
        name = "btag_vars"
        collection = globals()[name]
        combinedPlot(name + "_" + sample,                     
                     [plot(var.pretty_name, 
                           var.name,                    
                           fiducial_cuts[sample],
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




