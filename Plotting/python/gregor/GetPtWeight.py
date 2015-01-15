#!/usr/bin/env python
"""
We want to use flat true-pT distributions
- plot the true pT spectra
- fit with a function
- store the functions and the correct parameter in a pickle file
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
files["qcd_800_1000"] = "ntop_v13_qcd_800_1000_pythia8_13tev-tagging"
files["zprime_m2000"] = "ntop_v13_zprime_m2000_1p_13tev-tagging"     
                                         

# for the filename: basepath + filename + .root
full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + ".root"

output_dir = "results/GetPtWeight/"

output_pickle_file_name = "/shome/gregor/TTH-73X/CMSSW/src/TTH/Plotting/python/gregor/flat_pt_weights.pickle"


########################################
# Define plots and do fits
########################################

fit_zprime = ROOT.TF1("fit_fun_zprime","pol5",801,999)

if True:
    combinedPlot ("true_top_pt_cut",
                  [plot( "zprime_m2000", 
                         'hadtop_pt', 
                         '(hadtop_pt>801)&&(hadtop_pt<999)', 
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


if True:
    fit_qcd = ROOT.TF1("fit_fun_qcd","[0]+[1]*sqrt(x)+[2]/x",801,999)
    fit_qcd.SetParameter(0,1)
    fit_qcd.SetParameter(1,1)
    fit_qcd.SetParameter(2,0)

    combinedPlot ("parton_pt_cut",
                  [plot( "qcd_800_1000", 
                         'parton_pt', 
                         '(parton_pt>801)&&(parton_pt<999)', 
                         "qcd_800_1000", fit=fit_qcd)],
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


########################################
# Store the fit result
########################################

# We write a dictionary to the pickle file and store
#   - a function f (fit of the pT spectrum)
#   - correct variable (hadtop_pt or parton_pt)
# Example:
# { "ntop_v8_zprime_m2000_1p_13tev-tagging" : [ROOT.TF1(..), "hadtop"], ...}

# First get the old functions:
pickle_file = open(output_pickle_file_name, "r")
functions_and_parameter = pickle.load(pickle_file)
print "Loaded old fit functions from file:"
for k in functions_and_parameter:
    print k
pickle_file.close()

# Then add the new ones
functions_and_parameter[files["qcd_800_1000"]] = [fit_qcd, "parton_pt"]
functions_and_parameter[files["zprime_m2000"]] = [fit_zprime, "hadtop_pt"]

# And write everything to the file
pickle_file = open(output_pickle_file_name, "w")
pickle.dump(functions_and_parameter, pickle_file)
pickle_file.close()




