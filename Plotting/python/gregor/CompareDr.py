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

output_dir = "/shome/gregor/new_results/CompareDistributions/"
        
weight_vars = {"zprime_m750"     : "weight_nosize",
               "zprime_m1000"    : "weight_nosize",
               "zprime_m1250"    : "weight_nosize",
               "zprime_m2000_low": "weight_nosize",
               "zprime_m2000"    : "weight_nosize",
               "zprime_m3000"    : "weight_nosize",
               "qcd_170_300"     : "weight",
               "qcd_300_470"     : "weight",
               "qcd_470_600"     : "weight",
               "qcd_600_800"     : "weight",
               "qcd_800_1000"    : "weight",
               "qcd_1000_1400"   : "weight",
}



# Everything that does not need a previous mass cut is a mass (-;
masses = [
          "ca15softdropz20b10_mass",
          "ca15prunedn3z10rfac50_mass",
]



sample = "zprime_m1000"

for var in masses:

    xpos = 0.5
    ypos = 0.67
    ymax = None
    nbins = 80
    extra_text = ["CA15, flat p_{T}, #eta", "<#mu>=20, 25ns"]

    if "softdrop" in var and ("b10" in var or "b20" in var):
        ymax = 0.13

    actual_var = variable.di[var]
    if actual_var.pretty_name_short:
        x_label = actual_var.pretty_name_short
    else:
        x_label = actual_var.pretty_name

    combinedPlot("fixedMatch_sizes_" + var.replace("/","_"),
                 [plot("#Delta R (t,q) < " + str(size),
                       actual_var.name,                                           
                       '({0}&&{1}&&(top_size<{2}))*{3}'.format(fiducial_cuts[sample],
                                                               actual_var.extra_cut, 
                                                               size,weight_vars[sample]),
                       sample,
                       extra_fiducial = "(" + fiducial_cuts[sample] + "&&(top_size<{0}))*".format(size) + weight_vars[sample] ,
                   ) for size in [0.8, 1.0, 1.2]],
                 nbins, actual_var.range_min, actual_var.range_max, ymax,
                 label_x   = x_label,
                 label_y   = "A.U.",
                 axis_unit = actual_var.unit,
                 log_y     = False,
                 normalize = True,
                 draw_legend = True,
                 legend_origin_x = xpos,
                 legend_origin_y = ypos,
                 legend_size_x   = 0.2,
                 legend_text_size= 0.03,
                 add_eff = False,
                 extra_text = extra_text)


            

doWork(full_file_names, output_dir )




