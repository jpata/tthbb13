#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

from TTH.Plotting.Helpers.CorrelationHelpers import *

from TTH.Plotting.Helpers.VariableHelpers import variable as var

from TTH.Plotting.gregor.TopTaggingVariables import *


########################################
# Define Input Files and
# output directory
########################################

basepath = '/scratch/gregor/'

files = {}
files["qcd_800_1000"] = "ntop_v11_qcd_800_1000_pythia8_13tev-tagging-weighted"
files["zprime_m2000_1p"] = "ntop_v11_zprime_m2000_1p_13tev-tagging-weighted"

fiducial_cut_and_weight = "(weight*((pt>801)&&(pt<999)))"
                                        
# for the filename: basepath + filename + .root
for k,v in files.iteritems():
    files[k] = basepath + v + ".root"


corrs = [#corr("masses_15", "zprime_m2000_1p", mass_vars_15, fiducial_cut_and_weight),
         #corr("masses_15", "qcd_800_1000",    mass_vars_15, fiducial_cut_and_weight),

         #corr("taus_15", "zprime_m2000_1p", tau_vars_15, fiducial_cut_and_weight),
         #corr("taus_15", "qcd_800_1000",    tau_vars_15, fiducial_cut_and_weight),

         #corr("taggers_taus08", "zprime_m2000_1p", tagger_vars + tau_vars_08, fiducial_cut_and_weight),
         #corr("taggers_taus08", "qcd_800_1000",    tagger_vars + tau_vars_08, fiducial_cut_and_weight),
         
         corr("taggers", "zprime_m2000_1p", tagger_vars, fiducial_cut_and_weight),
         #corr("taggers", "qcd_800_1000",    tagger_vars, fiducial_cut_and_weight),

         #corr("all_15", "zprime_m2000_1p", mass_vars_15 + tau_vars_15 + tagger_vars_15, fiducial_cut_and_weight),
         #corr("all_15", "qcd_800_1000",    mass_vars_15 + tau_vars_15 + tagger_vars_15, fiducial_cut_and_weight),

         #corr("all_08", "zprime_m2000_1p", mass_vars_08 + tau_vars_08 + tagger_vars_08, fiducial_cut_and_weight),
         #corr("all_08", "qcd_800_1000",    mass_vars_08 + tau_vars_08 + tagger_vars_08, fiducial_cut_and_weight),


]

MakePlots(corrs, files)
