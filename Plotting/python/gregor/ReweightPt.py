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
files["qcd_800_1000"] = "ntop_v8_qcd_800_1000_pythia8_13tev-tagging"
files["zprime_m2000"] = "ntop_v8_zprime_m2000_1p_13tev-tagging"     
                                         

# for the filename: basepath + filename + .root
for k,v in files.iteritems():
    files[k] = basepath + v + ".root"

output_dir = "results/TaggingVars/"


########################################
# Define the plots
########################################


fit_zprime = ROOT.TF1("fit_fun_zprime","pol5",801,999)

combinedPlot ("true_top_pt_cut",
              [plot( "zprime_m2000", 
                     'hadtop_pt', 
                     '(hadtop_pt>800)&&(hadtop_pt<1000)', 
                     "zprime_m2000", 
                     fit=fit_zprime), 
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



fit_qcd = ROOT.TF1("fit_fun_qcd","[0]+[1]*sqrt(x)+[2]/x",801,999)
fit_qcd.SetParameter(0,1)
fit_qcd.SetParameter(1,1)
fit_qcd.SetParameter(2,0)

combinedPlot ("parton_pt_cut",
              [plot( "qcd_800_1000", 
                     'parton_pt', 
                     '(parton_pt>800)&&(parton_pt<1000)', 
                     "qcd_800_1000", fit=fit_qcd)],
              80, 750, 1050, 
              label_x   = "Parton p_{T}",
              label_y   = "Events",
              axis_unit = "GeV",
              log_y     = False,
              normalize = True,
              legend_origin_x = 0.32,
              legend_origin_y = 0.4,
              legend_size_x   = 0.2,
              legend_size_y   = 0.05 * 2)

doWork(files, output_dir )

