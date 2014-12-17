#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

from TTH.Plotting.Helpers.CorrelationHelpers import *


########################################
# Define Input Files and
# output directory
########################################

basepath = '/scratch/gregor/'

files = {}
files["qcd_800_1000"] = "ntop_v8_qcd_800_1000_pythia8_13tev-tagging"
files["zprime_m2000_1p"] = "ntop_v8_zprime_m2000_1p_13tev-tagging"
                                        
# for the filename: basepath + filename + .root
for k,v in files.iteritems():
    files[k] = basepath + v + ".root"


mass_vars = [
    var('ca15_mass', "m", 0, 1000),
    var('ca15filtered_mass', "filtered m", 0, 1000),
    var('ca15pruned_mass', "pruned m", 0, 1000),
    var('ca15trimmed_mass', "trimmed m", 0, 1000),
    var('ca15softdrop_mass', "softdrop m", 0, 1000),    
]

tau_vars = [
    var('ca15_tau3/ca15_tau2', "#tau_{3}/#tau_{2}", 0, 2.),
    var('ca15filtered_tau3/ca15filtered_tau2', "filtered #tau_{3}/#tau_{2}", 0, 2.),
    var('ca15pruned_tau3/ca15pruned_tau2', "pruned #tau_{3}/#tau_{2}", 0, 2.),
    var('ca15trimmed_tau3/ca15trimmed_tau2', "trimmed #tau_{3}/#tau_{2}", 0, 2.),
    var('ca15softdrop_tau3/ca15softdrop_tau2', "softdrop #tau_{3}/#tau_{2}", 0, 2.),    
]

tagger_vars = [
    var('looseMultiRHTT_mass', "HTT m", 0, 1000),
    var('looseMultiRHTT_fW', "HTT f_{W}", 0, 2),
    var('looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected', "HTT #Delta R_{min,exp}", -3., 3.),
    var('ca15cmstt_minMass', "CMSTT minMass", 0., 1000),
]


corrs = [corr("masses", "zprime_m2000_1p", mass_vars),
         corr("taus", "zprime_m2000_1p", tau_vars),
         corr("taggers", "zprime_m2000_1p", tagger_vars),
         corr("all", "zprime_m2000_1p", mass_vars+tau_vars+tagger_vars),

         corr("masses", "qcd_800_1000", mass_vars),
         corr("taus", "qcd_800_1000", tau_vars),
         corr("taggers", "qcd_800_1000", tagger_vars),
         corr("all", "qcd_800_1000", mass_vars+tau_vars+tagger_vars)
]

MakePlots(corrs, files)
