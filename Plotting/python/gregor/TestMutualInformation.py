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


mis =[ #mi("taggers", "zprime_m2000_1p", "qcd_800_1000", tagger_vars, fiducial_cut_and_weight),
       mi("masses", "zprime_m2000_1p", "qcd_800_1000", mass_vars_08+mass_vars_15, fiducial_cut_and_weight),
       mi("taus", "zprime_m2000_1p", "qcd_800_1000",   tau_vars_08+tau_vars_15+[var.di['ca08softdrop_mass']], fiducial_cut_and_weight),
       mi("good", "zprime_m2000_1p", "qcd_800_1000", good_vars, fiducial_cut_and_weight),
]

MakePlots(mis, files)
