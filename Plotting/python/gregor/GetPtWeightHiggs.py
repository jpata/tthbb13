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
from TTH.Plotting.gregor.HiggsSamples import *


########################################
# Define Input Files and
# output directory
########################################

to_process = files.keys()

basepath = '/scratch/gregor/'
                                         
fits = {}
fits["rad_hh4b_m800_170_300"] = ROOT.TF1("","pol5",171,299)
fits["rad_hh4b_m800_300_470"] = ROOT.TF1("","pol6",301,469)
fits["rad_hh4b_m1600_470_600"] = ROOT.TF1("","pol5",471,599)
fits["rad_hh4b_m1600_600_800"] = ROOT.TF1("","pol5",601,799)

fits["qcd_170_300"]  = ROOT.TF1("fit_fun_qcd","[0]+[1]*sqrt(x)+[2]/x+[3]/(x*x)+[4]/(x*x*x)",171,299)
fits["qcd_300_470"]  = ROOT.TF1("fit_fun_qcd", "pol5",301,470)
fits["qcd_470_600"]  = ROOT.TF1("fit_fun_qcd","[0]+[1]*sqrt(x)+[2]/x + [3]*x",471,599)
fits["qcd_600_800"]  = ROOT.TF1("fit_fun_qcd","[0]+[1]*sqrt(x)+[2]/x + [3]*x",601,799)
    
for qcd_name in ["qcd_170_300", "qcd_300_470", "qcd_470_600", "qcd_600_800"]:
    fits[qcd_name].SetParameter(0,1)
    fits[qcd_name].SetParameter(1,1)
    fits[qcd_name].SetParameter(2,0.5)



fits["rad_hh4b_m800_300_470"].SetParameter(0,      54.0457)
fits["rad_hh4b_m800_300_470"].SetParameter(1,    -0.714783)
fits["rad_hh4b_m800_300_470"].SetParameter(2,   0.00374876)
fits["rad_hh4b_m800_300_470"].SetParameter(3, -9.74367e-06)
fits["rad_hh4b_m800_300_470"].SetParameter(4,  1.25547e-08)
fits["rad_hh4b_m800_300_470"].SetParameter(5, -6.41858e-12)  









# for the filename: basepath + filename + .root
full_file_names = {}
for name in to_process:
    full_file_names[name] = basepath + files[name] + ".root"

output_dir = "results/GetPtWeightHiggs/"

output_pickle_file_name = "/shome/gregor/TTH-73X/CMSSW/src/TTH/Plotting/python/gregor/flat_pt_weights_higgs.pickle"


########################################
# Define plots and do fits
########################################

if True:    
    for k in to_process:

        if "qcd" in k:
            truth_var = "parton"
        else:
            truth_var = "higgs"

        pt_var = "{0}_pt".format(truth_var)

        fiducial_cut = "(({0}>{1})&&({0}<{2}))".format(pt_var, ranges[k][0], ranges[k][1])


        combinedPlot ( k + "_pt_cut",
                      [plot( k, 
                             pt_var,
                             fiducial_cut,
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
                      legend_origin_x = 0.35,
                      legend_origin_y = 0.3,
                      legend_size_x   = 0.2,
                      legend_size_y   = 0.05 * 2)

print full_file_names

doWork(full_file_names, output_dir )


########################################
# Store the fit result
########################################
# 
# We write two dictionaries to the pickle file and store
#   - a function f (fit of the pT/eta spectrum)
#   - correct variable (hadtop_pt or parton_pt)
# Example:
# { "ntop_v8_zprime_m2000_1p_13tev-tagging" : [ROOT.TF1(..), "hadtop"], ...}

# First get the old functions:
#pickle_file = open(output_pickle_file_name, "r")
functions_and_parameter_pt  = {}#pickle.load(pickle_file)

print "Loaded old pt fit functions from file:"
for k in functions_and_parameter_pt:
    print k
#pickle_file.close()

# Then add the new ones
for k in to_process:
    v = files[k]
    print "Adding: ", v

    if "qcd" in k:
        pt_var = "parton_pt"
    else:
        pt_var = "higgs_pt"

    functions_and_parameter_pt[v]  = [fits[k], pt_var]


# And write everything to the file
pickle_file = open(output_pickle_file_name, "w")
pickle.dump(functions_and_parameter_pt, pickle_file)
pickle_file.close()
 



