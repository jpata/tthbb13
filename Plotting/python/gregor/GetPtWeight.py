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
from TTH.Plotting.gregor.TopSamples import files, ranges


########################################
# Define Input Files and
# output directory
########################################

to_process = files.keys()
#[
    #"zprime_m1000",
    #"zprime_m2000_low",
    #"zprime_m3000",    
    #"zprime_m4000",    
#]

basepath = '/scratch/gregor/'
                                         
fits = {}
fits["zprime_m750"]      = ROOT.TF1("fit_fun_zprime","pol5",201,299)
fits["zprime_m1000"]     = ROOT.TF1("fit_fun_zprime","pol5",301,469)
fits["zprime_m1250"]     = ROOT.TF1("fit_fun_zprime","pol5",471,599)
fits["zprime_m1500"]     = ROOT.TF1("fit_fun_zprime","pol5",601,799)
fits["zprime_m2000_low"] = ROOT.TF1("fit_fun_zprime","pol5",601,799)
fits["zprime_m2000"]     = ROOT.TF1("fit_fun_zprime","pol5",801,999)
fits["zprime_m3000"]     = ROOT.TF1("fit_fun_zprime","pol5",1001,1499)
fits["zprime_m4000"]     = ROOT.TF1("fit_fun_zprime","pol5",1401,1799)

fits["qcd_170_300"]  = ROOT.TF1("fit_fun_qcd","[0]+[1]*sqrt(x)+[2]/x + [3]*x",201,299)
fits["qcd_470_600"]  = ROOT.TF1("fit_fun_qcd","[0]+[1]*sqrt(x)+[2]/x + [3]*x",471,599)
fits["qcd_300_470"]  = ROOT.TF1("fit_fun_qcd","[0]+[1]*sqrt(x)+[2]/x+[3]/(x*x)+[4]/(x*x*x)",301,470)
fits["qcd_800_1000"] = ROOT.TF1("fit_fun_qcd","[0]+[1]*sqrt(x)+[2]/x",801,999)

for qcd_name in ["qcd_170_300", "qcd_300_470", "qcd_470_600", "qcd_800_1000"]:
    fits[qcd_name].SetParameter(0,1)
    fits[qcd_name].SetParameter(1,1)
    fits[qcd_name].SetParameter(2,0.5)


eta_fits = {}

for k in fits.keys():
    eta_fits[k] = ROOT.TF1("eta_k","pol6", -1.5, 1.5)


# for the filename: basepath + filename + .root
full_file_names = {}
for name in to_process:
    full_file_names[name] = basepath + files[name] + ".root"

output_dir = "results/GetPtWeight/"

output_pickle_file_name = "/shome/gregor/TTH-73X/CMSSW/src/TTH/Plotting/python/gregor/flat_pt_weights.pickle"


########################################
# Define plots and do fits
########################################

if True:    
    for k in to_process:

        if "zprime" in k:
            truth_var = "hadtop"
        else:
            truth_var = "parton"

        combinedPlot ( k + "_pt_cut",
                      [plot( k, 
                             "{0}_pt".format(truth_var),
                             '(({0}_pt>{1})&&({0}_pt<{2}))'.format(truth_var, ranges[k][0], ranges[k][1]), 
                             k,
                             fit=fits[k]
                         ), 
                       ],
                      80, ranges[k][0], ranges[k][1], 
                      label_x   = "True p_{T}",
                      label_y   = "Partons",
                      axis_unit = "GeV",
                      log_y     = False,
                      normalize = True,
                      legend_origin_x = 0.55,
                      legend_origin_y = 0.6,
                      legend_size_x   = 0.2,
                      legend_size_y   = 0.05 * 2)

        combinedPlot ( k + "_eta",
                      [plot( k, 
                             "{0}_eta".format(truth_var),
                             '(({0}_pt>{1})&&({0}_pt<{2}))'.format(truth_var, ranges[k][0], ranges[k][1]), 
                             k,
                             fit=eta_fits[k]
                         ), 
                       ],
                      80, -3, 3, 
                      label_x   = "True #eta",
                      label_y   = "Partons",
                      axis_unit = "GeV",
                      log_y     = False,
                      normalize = True,
                      legend_origin_x = 0.55,
                      legend_origin_y = 0.6,
                      legend_size_x   = 0.2,
                      legend_size_y   = 0.05 * 2)

print full_file_names

doWork(full_file_names, output_dir )


########################################
# Store the fit result
########################################

# We write two dictionaries to the pickle file and store
#   - a function f (fit of the pT/eta spectrum)
#   - correct variable (hadtop_pt or parton_pt)
# Example:
# { "ntop_v8_zprime_m2000_1p_13tev-tagging" : [ROOT.TF1(..), "hadtop"], ...}

# First get the old functions:
pickle_file = open(output_pickle_file_name, "r")
functions_and_parameter_pt  = pickle.load(pickle_file)
functions_and_parameter_eta = pickle.load(pickle_file)


print "Loaded old pt fit functions from file:"
for k in functions_and_parameter_pt:
    print k
print "Loaded old eta fit functions from file:"
for k in functions_and_parameter_eta:
    print k
pickle_file.close()

# Then add the new ones
for k in to_process:
    v = files[k]
    print "Adding: ", v

    if "zprime" in k:
        pt_var  = "hadtop_pt"
        eta_var = "hadtop_eta"
    else:
        pt_var  = "parton_pt"
        eta_var = "parton_eta"

    functions_and_parameter_pt[v]  = [fits[k], pt_var]
    functions_and_parameter_eta[v] = [eta_fits[k], eta_var]

# And write everything to the file
pickle_file = open(output_pickle_file_name, "w")
pickle.dump(functions_and_parameter_pt, pickle_file)
pickle.dump(functions_and_parameter_eta, pickle_file)
pickle_file.close()




