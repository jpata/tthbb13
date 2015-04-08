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






samples = [
    "rad_hh4b_m800_170_300",
    "rad_hh4b_m800_300_470",
    "rad_hh4b_m1600_470_600",
    "rad_hh4b_m1600_600_800",

    "qcd_170_300",
    "qcd_300_470",
    "qcd_470_600",
    "qcd_600_800",

    ]

sample_names = {
    "rad_hh4b_m800_170_300" : "H: 170 < pT < 300",
    "rad_hh4b_m800_300_470" : "H: 300 < pT < 470",
    "rad_hh4b_m1600_470_600" : "H: 470 < pT < 600",
    "rad_hh4b_m1600_600_800" : "H: 600 < pT < 800",
    "qcd_170_300": "QCD: 170 < pT < 300",
    "qcd_300_470": "QCD: 300 < pT < 470",
    "qcd_470_600": "QCD: 470 < pT < 600",
    "qcd_600_800": "QCD: 600 < pT < 800",
}

print sample_names["qcd_470_600"]


nice_names = {    
    "ca15": "CA (R=1.5)",
    "ak08": "AK (R=0.8)",
    
    ''             : "Ungroomed", 
    'filteredn3r3' : "Filtered (n=3, r=0.3)",
    'filteredn3r2' : "Filtered (n=3, r=0.2)",
    'filteredn2r3' : "Filtered (n=2, r=0.3)",
    'filteredn2r2' : "Filtered (n=2, r=0.2)",
    'prunedn2z10rfac50' : "Pruned (n=2, z=0.1, rfrac=0.5)",
    'trimmedr2f3' : "Trimmed (r=0.2, f=0.03)",
    'trimmedr2f6' : "Trimmed (r=0.2, f=0.06)",
    'trimmedr2f10' : "Trimmed (r=0.2, f=0.1)",
    'softdropz10b00' : "Softdrop (z=0.1, b=0)",
    'softdropz15b00' : "Softdrop (z=0.15, b=0)",
    'softdropz15b10' : "Softdrop (z=0.15, b=1)",
    'softdropz20b10' : "Softdrop (z=0.2, b=1)",
    'softdropz30b10' : "Softdrop (z=0.3, b=1)",
    'softdropz30b15' : "Softdrop (z=0.3, b=1.5)",
}



mass_vars = []
mass_var_names = []
for fj in ["ca15","ak08"]:
    for groomer in ["",
                    'filteredn3r3',
                    'filteredn3r2',
                    'filteredn2r3',
                    'filteredn2r2',
                    'prunedn2z10rfac50',
                    'trimmedr2f3',
                    'trimmedr2f6',
                    'trimmedr2f10',
                    'softdropz10b00',
                    'softdropz15b00',
                    'softdropz15b10',
                    'softdropz20b10',
                    'softdropz30b10',
                    'softdropz30b15',
    ]:        
        mass_vars.append("{0}{1}_mass".format(fj, groomer))
        mass_var_names.append("{0} {1}".format(nice_names[fj], nice_names[groomer]))
        


        



if False:
    for mass_var,name in zip(mass_vars, mass_var_names):
        combinedPlot(mass_var,
                     [plot( sample_names[sample], 
                            mass_var,
                            fiducial_cuts[sample], 
                            sample) for sample in samples],
                     50, 0, 250, 
                     label_x   = name,
                     label_y   = "A.U.",
                     axis_unit = "GeV",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.6,
                     legend_origin_y = 0.6,
                     legend_size_x   = 0.2,
                     legend_text_size= 0.03,
                 )



if False:
    combinedPlot("pt",
                 [plot( sample_names[sample], 
                        "pt",
                        fiducial_cuts[sample], 
                        sample) for sample in samples],
                 50, 0, 1000, 
                 label_x   = "p_{T}",
                 label_y   = "",
                 axis_unit = "GeV",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.6,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.2,
                 legend_text_size= 0.03,
             )

if False:
    combinedPlot("eta",
                 [plot( sample_names[sample], 
                        "eta",
                        fiducial_cuts[sample], 
                        sample) for sample in samples],
                 50, -3.5, 3.5, 
                 label_x   = "#eta",
                 label_y   = "A.U.",
                 axis_unit = "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.6,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.2,
                 legend_text_size= 0.03,
             )

if False:
    combinedPlot("npv",
                 [plot( sample_names[sample], 
                        "npv",
                        fiducial_cuts[sample], 
                        sample) for sample in samples],
                 41, 0, 40, 
                 label_x   = "NPV",
                 label_y   = "A.U.",
                 axis_unit = "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.6,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.2,
                 legend_text_size= 0.03,
             )
if False:
    combinedPlot("qvol",
                 [plot( sample_names[sample], 
                        "ca15_qvol",
                        fiducial_cuts[sample], 
                        sample) for sample in samples],
                 41, 0, 1, 
                 label_x   = "Q-Jet Volatility",
                 label_y   = "A.U.",
                 axis_unit = "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.2,
                 legend_text_size= 0.03,
             )

if False:
    combinedPlot("nsub",
                 [plot( sample_names[sample], 
                        "ca15_tau2/ca15_tau1",
                        fiducial_cuts[sample], 
                        sample) for sample in samples],
                 41, 0, 1, 
                 label_x   = "N-Subjettiness #tau_{2}/#tau_{1}",
                 label_y   = "A.U.",
                 axis_unit = "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.3,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.2,
                 legend_text_size= 0.03,
             )




if True:

    for var in qvol_vars:

        combinedPlot(var.name,
                     [plot( sample_names[pair[0]], var.name,  fiducial_cuts[pair[0]], pair[0]) for pair in sorted(pairs.values())] + 
                     [plot( sample_names[pair[1]], var.name,  fiducial_cuts[pair[1]], pair[1]) for pair in sorted(pairs.values())],
                     50, 0, 1, 
                     label_x   = "Q-Jet Volatility({0})".format(var.pretty_name),
                     label_y   = "A.U.",
                     axis_unit = "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.6,
                     legend_origin_y = 0.6,
                     legend_size_x   = 0.2,
                     legend_text_size= 0.03)
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
if False:
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




