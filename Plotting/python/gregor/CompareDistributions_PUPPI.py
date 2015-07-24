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

output_dir = "/shome/gregor/new_results/CompareDistributions_PUPPI/"

samples = [
    "zprime_m1000",      
    "qcd_300_470",
    "zprime_m1000_puppi",      
    "qcd_300_470_puppi"]

this_sample_names = {

    "zprime_m1000"     : "CHS, Top",                      
    "qcd_300_470"      : "CHS, QCD",
    "zprime_m1000_puppi": "PUPPI, Top",                      
    "qcd_300_470_puppi": "PUPPI, QCD",
}


for sample in samples:

    # Everything that does not need a previous mass cut is a mass (-;
    masses = ["ca15_mass",
              "ca15softdropz10b00_mass",
              "ca15softdropz20b10_mass",

              #"log(ca15_chi1)",
              #"log(ca15_chi2)",
              #"log(ca15_chi3)",

              #"looseOptRHTT_mass",

              #"ca15cmstt_minMass",
              #"ca15cmstt_topMass",
              #"ca15cmstt_nSubJets"
    ]

    

    # These need a cut on the HTT mass
    htt_vars = [
        "looseOptRHTT_fRec",
        "looseOptRHTT_Ropt-looseOptRHTT_RoptCalc",
        ]

    # These need a mass-cut
    others = [
        "ca15_tau3/ca15_tau2",
    ]

    if True:
        for var in masses:

            ymax = None            
            xpos = 0.65
            ypos = 0.76
            nbins = 80
            extra_text = ["CA15, flat p_{T}, #eta", "300-470 GeV"]

            if var == "ca15_mass":
                ymax = 0.15
            if var == "ca15softdropz10b00_mass":
                ymax = 0.3
            if var == "ca15softdropz20b10_mass":
                ymax = 0.15


            combinedPlot("nosize_" + var.replace("/","_"),
                         [plot(this_sample_names[sample],
                               variable.di[var].name,                                           
                               '({0}&&{1})*weight'.format(nosize_fiducial_cuts[sample], variable.di[var].extra_cut),
                               sample,
                               extra_fiducial = "(" + nosize_fiducial_cuts[sample] + ")*" + "weight"
                           ) for sample in samples],
                         80, variable.di[var].range_min, variable.di[var].range_max, ymax,
                         label_x   = variable.di[var].pretty_name,
                         label_y   = "A.U.",
                         axis_unit = variable.di[var].unit,
                         log_y     = False,
                         normalize = True,
                         legend_origin_x = xpos,
                         legend_origin_y = ypos,
                         legend_size_x   = 0.2,
                         legend_text_size= 0.03,
                         extra_text = extra_text)
            
    if True:
        for var in others:

            
            ymax = 0.15            
            xpos = 0.55
            ypos = 0.6
            nbins = 80
            extra_text = ["CA15, flat p_{T}, #eta", "300-470 GeV", "m_{SD} > 120 GeV"]
        
            cut = "(ca15softdropz10b00_mass>120)"

            combinedPlot("nosize_masscut_" + var.replace("/","_"),
                         [plot(this_sample_names[sample],
                               variable.di[var].name,                                           
                               '({0}&&{1}&&{2})*weight'.format(nosize_fiducial_cuts[sample], 
                                                               variable.di[var].extra_cut,
                                                               cut),
                               sample,
                               extra_fiducial = "(" + nosize_fiducial_cuts[sample] + ")*" + "weight",
                           ) for sample in samples],
                         80, variable.di[var].range_min, variable.di[var].range_max, ymax,
                         label_x   = variable.di[var].pretty_name,
                         label_y   = "A.U.",
                         axis_unit = variable.di[var].unit,
                         log_y     = False,
                         normalize = True,
                         legend_origin_x = xpos,
                         legend_origin_y = ypos,
                         legend_size_x   = 0.2,
                         legend_text_size= 0.03,
                         extra_text = extra_text)
            

    if False:
        for var in htt_vars:

            if name == "high":

                xpos = 0.6
                ypos = 0.6
                ymax = None
                nbins = 80
                extra_text = "AK08, flat pT"

                if "HTT" in var:                    
                    extra_text = "CA15, flat pT"


                cut = "((looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180))"

            else:
                xpos = 0.6
                ypos = 0.76
                ymax = None
                nbins = 80
                extra_text = "CA15, flat pT"
                                
                cut = "((looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180))"


            combinedPlot("nosize_httmasscut_" + var.replace("/","_")+"_"+name,
                         [plot(other2_sample_names[sample],
                               variable.di[var.replace("X",ranges[sample][4])].name,                                           
                               '({0}&&{1}&&{2})*weight'.format(nosize_fiducial_cuts[sample], 
                                                               variable.di[var.replace("X",ranges[sample][4])].extra_cut,
                                                               cut),
                               sample) for sample in samples],
                         80, variable.di[var.replace("X",ranges[sample][4])].range_min, variable.di[var.replace("X",ranges[sample][4])].range_max, ymax,
                         label_x   = variable.di[var.replace("X",ranges[sample][4])].pretty_name,
                         label_y   = "A.U.",
                         axis_unit = variable.di[var.replace("X",ranges[sample][4])].unit,
                         log_y     = False,
                         normalize = True,
                         legend_origin_x = xpos,
                         legend_origin_y = ypos,
                         legend_size_x   = 0.2,
                         legend_text_size= 0.03,
                         extra_text = extra_text)

doWork(full_file_names, output_dir )




