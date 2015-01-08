#!/usr/bin/env python
"""
Collection of Top Tagging Variables (so we can use them across Plotting/Correlation/TMVA)
"""

from TTH.Plotting.Helpers.VariableHelpers import variable


mass_vars_15 = [
    variable('ca15_mass', "m (R=1.5)", 0, 1000),
    variable('ca15filtered_mass', "filtered m (R=1.5)", 0, 1000),
    variable('ca15pruned_mass', "pruned m (R=1.5)", 0, 1000),
    variable('ca15trimmed_mass', "trimmed m (R=1.5)", 0, 1000),
    variable('ca15softdrop_mass', "softdrop m (R=1.5)", 0, 1000),    
]

mass_vars_08 = [
    variable('ca08_mass', "m (R=0.8)", 0, 1000),
    variable('ca08filtered_mass', "filtered m (R=0.8)", 0, 1000),
    variable('ca08pruned_mass', "pruned m (R=0.8)", 0, 1000),
    variable('ca08trimmed_mass', "trimmed m (R=0.8)", 0, 1000),
    variable('ca08softdrop_mass', "softdrop m (R=0.8)", 0, 1000),    
]

tau_vars_15 = [
    variable('ca15_tau3/ca15_tau2', "#tau_{3}/#tau_{2}  (R=1.5)", 0, 2.),
    variable('ca15filtered_tau3/ca15filtered_tau2', "filtered #tau_{3}/#tau_{2}  (R=1.5)", 0, 2.),
    variable('ca15pruned_tau3/ca15pruned_tau2', "pruned #tau_{3}/#tau_{2}  (R=1.5)", 0, 2.),
    variable('ca15trimmed_tau3/ca15trimmed_tau2', "trimmed #tau_{3}/#tau_{2}  (R=1.5)", 0, 2.),
    variable('ca15softdrop_tau3/ca15softdrop_tau2', "softdrop #tau_{3}/#tau_{2}  (R=1.5)", 0, 2.),    
]

tau_vars_08 = [
    variable('ca08_tau3/ca08_tau2', "#tau_{3}/#tau_{2}  (R=0.8)", 0, 2.),
    variable('ca08filtered_tau3/ca08filtered_tau2', "filtered #tau_{3}/#tau_{2}  (R=0.8)", 0, 2.),
    variable('ca08pruned_tau3/ca08pruned_tau2', "pruned #tau_{3}/#tau_{2}  (R=0.8)", 0, 2.),
    variable('ca08trimmed_tau3/ca08trimmed_tau2', "trimmed #tau_{3}/#tau_{2}  (R=0.8)", 0, 2.),
    variable('ca08softdrop_tau3/ca08softdrop_tau2', "softdrop #tau_{3}/#tau_{2}  (R=0.8)", 0, 2.),    
]

tagger_vars_15 = [
    variable('looseMultiRHTT_mass', "HTT m", 0, 1000),
    variable('looseMultiRHTT_fW', "HTT f_{W}", 0, 2),
    variable('looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected', "HTT #Delta R_{min,exp}", -3., 3.),
    variable('ca15cmstt_minMass', "CMSTT minMass (R=1.5)", 0., 1000),
]

tagger_vars_08 = [
    variable('ca08cmstt_minMass', "CMSTT minMass (R=0.8)", 0., 1000),
]

all_vars_15 = mass_vars_15 + tau_vars_15 + tagger_vars_15
all_vars_08 = mass_vars_08 + tau_vars_08 + tagger_vars_08
