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

samples = [#"zprime_m1000_low", 
           "zprime_m1000",
           #"zprime_m2000_low",
           #"zprime_m2000",
           #"qcd_170_300",
           "qcd_300_470",
           #"qcd_600_800",
           #"qcd_800_1000",
           #"wjets_lnu_ht_600_inf_200_300",
           #"wjets_lnu_ht_600_inf_300_470",
           #"wjets_lnu_ht_600_inf_600_800",
]

for var in [
        #"X_mass",
        #"Xfilteredn3r2_mass",
        #"Xfilteredn5r2_mass",
        #"Xprunedn3z10rfac50_mass",
        #"Xtrimmedr2f3_mass",
        #"Xtrimmedr2f6_mass",
        #"Xtrimmedr2f9_mass",
        "Xsoftdropz10b00_mass",
        #"Xsoftdropz10b10_mass",
        #"Xsoftdropz10b20_mass",
        #"Xsoftdropz15b00_mass",
        #"Xsoftdropz15b10_mass",
        #"Xsoftdropz15b20_mass",
        #"Xsoftdropz20b00_mass",
        #"Xsoftdropz20b10_mass",
        #"Xsoftdropz20b20_mass",
        #"log(X_chi)",
        "X_tau3/X_tau2", 
        #"X_qvol",
        #"Xtrimmedr2f6forbtag_btag",
        #"Xcmstt_nSubJets",
        #"Xcmstt_minMass",
        #"Xcmstt_topMass",
        "looseOptRHTT_mass",
        "looseOptRHTT_fRec",
        "looseOptRHTT_Ropt-looseOptRHTT_RoptCalc",
        #"looseOptRRejRminHTT_Ropt-looseOptRRejRminHTT_RoptCalc",

]:
    
    if var=="X_tau3/X_tau2":
        xpos = 0.25
    elif var=="X_mass":
        xpos = 0.60
    elif  var == "log(X_chi)":
        xpos = 0.23
    else:
        xpos = 0.57
        
        
    if False:
        combinedPlot(var.replace("/","_"),
                     [plot(other_sample_names[sample],
                           variable.di[var.replace("X",ranges[sample][4])].name,                                           
                           '({0}&&{1})*weight'.format(fiducial_cuts[sample], variable.di[var.replace("X",ranges[sample][4])].extra_cut),
                           sample) for sample in samples],
                     80, variable.di[var.replace("X",ranges[sample][4])].range_min, variable.di[var.replace("X",ranges[sample][4])].range_max, 
                     label_x   = variable.di[var.replace("X",ranges[sample][4])].pretty_name,
                     label_y   = "A.U.",
                     axis_unit = variable.di[var.replace("X",ranges[sample][4])].unit,
                     log_y     = True,
                     normalize = True,
                     legend_origin_x = xpos,
                     legend_origin_y = 0.65,
                     legend_size_x   = 0.2,
                     legend_text_size= 0.03)
    if True:
        combinedPlot(var.replace("/","_")+"_pass",
                     [plot(other_sample_names[sample],
                           "(({0}>{1})&&({0}<{2})&&({3}))".format(variable.di[var.replace("X",ranges[sample][4])].name,
                                                                 variable.di[var.replace("X",ranges[sample][4])].range_min,                                           
                                                                 variable.di[var.replace("X",ranges[sample][4])].range_max,
                                                                 variable.di[var.replace("X",ranges[sample][4])].extra_cut),                                           
                           '({0})*weight'.format(fiducial_cuts[sample], ),
                           sample) for sample in samples],
                     80, -0.1, 1.1,
                     label_x   = variable.di[var.replace("X",ranges[sample][4])].pretty_name,
                     label_y   = "A.U.",
                     axis_unit = variable.di[var.replace("X",ranges[sample][4])].unit,
                     log_y     = True,
                     normalize = True,
                     legend_origin_x = xpos,
                     legend_origin_y = 0.65,
                     legend_size_x   = 0.2,
                     legend_text_size= 0.03)



doWork(full_file_names, output_dir )




