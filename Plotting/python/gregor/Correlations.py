#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.CorrelationHelpers import *
    from TTH.Plotting.Helpers.VariableHelpers import variable as var
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import files, ranges
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.CorrelationHelpers import *
    from TTH.Plotting.python.Helpers.VariableHelpers import variable as var
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import files, ranges


########################################
# Define Input Files and
# output directory
########################################

basepath = '/scratch/gregor/'

# for the filename: basepath + filename + .root
full_filenames = {}
for k,v in files.iteritems():
    full_filenames[k] = basepath + v + "-weighted.root"

fiducial_cut_and_weight = "(weight*((pt>801)&&(pt<999)))"

corrs = [#corr("masses_15", "zprime_m2000_1p", mass_vars_15, fiducial_cut_and_weight),
         #corr("masses_15", "qcd_800_1000",    mass_vars_15, fiducial_cut_and_weight),

         #corr("taus_15", "zprime_m2000_1p", tau_vars_15, fiducial_cut_and_weight),
         #corr("taus_15", "qcd_800_1000",    tau_vars_15, fiducial_cut_and_weight),

         #corr("taggers_taus08", "zprime_m2000_1p", tagger_vars + tau_vars_08, fiducial_cut_and_weight),
         #corr("taggers_taus08", "qcd_800_1000",    tagger_vars + tau_vars_08, fiducial_cut_and_weight),
         
         #corr("taggers", "zprime_m2000_1p", tagger_vars, fiducial_cut_and_weight),
         #corr("taggers", "qcd_800_1000",    tagger_vars, fiducial_cut_and_weight),

         corr("good", "zprime_m2000_1p", good_vars, fiducial_cut_and_weight),
         #corr("good", "qcd_800_1000",    good_vars, fiducial_cut_and_weight),

         #corr("all_15", "zprime_m2000_1p", mass_vars_15 + tau_vars_15 + tagger_vars_15, fiducial_cut_and_weight),
         #corr("all_15", "qcd_800_1000",    mass_vars_15 + tau_vars_15 + tagger_vars_15, fiducial_cut_and_weight),

         #corr("all_08", "zprime_m2000_1p", mass_vars_08 + tau_vars_08 + tagger_vars_08, fiducial_cut_and_weight),
         #corr("all_08", "qcd_800_1000",    mass_vars_08 + tau_vars_08 + tagger_vars_08, fiducial_cut_and_weight),


]

MakePlots(corrs, files)
