#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import pickle

from TTH.Plotting.Helpers.CompareDistributionsHelpers import *


########################################
# Define Input Files and
# output directory
########################################

basepath = '/scratch/gregor/'

files = {}
files["qcd_800_1000"] = "ntop_v8_qcd_800_1000_pythia8_13tev-tagging-weighted"
files["zprime_m2000"] = "ntop_v8_zprime_m2000_1p_13tev-tagging-weighted"     
                                         

# for the filename: basepath + filename + .root
full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + ".root"

output_dir = "results/CheckPtWeight/"


########################################
# Define plots and do fits
########################################

fit_zprime = ROOT.TF1("fit_fun_zprime","pol5",801,999)

combinedPlot ("true_top_pt_cut",
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

combinedPlot ("parton_pt_cut",
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


doWork(full_file_names, output_dir )




