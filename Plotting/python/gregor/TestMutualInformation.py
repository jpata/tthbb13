#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

from TTH.Plotting.python.Helpers.MutualInformationHelpers import *

from TTH.Plotting.python.Helpers.VariableHelpers import variable as var

from TTH.Plotting.python.gregor.TopTaggingVariables import *


########################################
# Define Input Files and
# output directory
########################################

basepath = '/Users/gregor/'

files = {}
files["qcd_800_1000"] = "ntop_v11_qcd_800_1000_pythia8_13tev-tagging-weighted"
files["zprime_m2000_1p"] = "ntop_v11_zprime_m2000_1p_13tev-tagging-weighted"

fiducial_cut_and_weight = "(weight*((pt>801)&&(pt<999)))"
                                        
# for the filename: basepath + filename + .root
for k,v in files.iteritems():
    files[k] = basepath + v + ".root"


mis = [mi("test", "zprime_m2000_1p", "qcd_800_1000",
          [var.di['ca08_mass'],
           var.di['ca15_mass'],
           var.di['ca08_tau3/ca08_tau2'],
           var.di['log(ca08_chi)'],
           var.di['log(ca15_chi)'],
       ], fiducial_cut_and_weight)]

MakePlots(mis, files)
