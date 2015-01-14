#!/usr/bin/env python
"""
Collection of Top Tagging Variables (so we can use them across Plotting/Correlation/TMVA)
"""

import os

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.VariableHelpers import variable
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.VariableHelpers import variable


mass_vars_15 = [
    variable('ca15_mass', "m (R=1.5)", 0, 1000, unit = "GeV"),
    variable('ca15filtered_mass', "filtered m (R=1.5)", 0, 1000, unit = "GeV"),
    variable('ca15pruned_mass', "pruned m (R=1.5)", 0, 1000, unit = "GeV"),
    variable('ca15trimmed_mass', "trimmed m (R=1.5)", 0, 1000, unit = "GeV"),
    variable('ca15softdrop_mass', "softdrop m (R=1.5)", 0, 1000, unit = "GeV"),   
]

mass_vars_08 = [
    variable('ca08_mass', "m (R=0.8)", 0, 500, unit = "GeV"),
    variable('ca08filtered_mass', "filtered m (R=0.8)", 0, 500, unit = "GeV"),
    variable('ca08pruned_mass', "pruned m (R=0.8)", 0, 500, unit = "GeV"),
    variable('ca08trimmed_mass', "trimmed m (R=0.8)", 0, 500, unit = "GeV"),
    variable('ca08softdrop_mass', "softdrop m (R=0.8)", 0, 500, unit = "GeV"),
]

tau_vars_15 = [
    variable('ca15_tau3/ca15_tau2', "#tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),
    variable('ca15filtered_tau3/ca15filtered_tau2', "filtered #tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),
    variable('ca15pruned_tau3/ca15pruned_tau2', "pruned #tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),
    variable('ca15trimmed_tau3/ca15trimmed_tau2', "trimmed #tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),
    variable('ca15softdrop_tau3/ca15softdrop_tau2', "softdrop #tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),    
]

tau_vars_08 = [
    variable('ca08_tau3/ca08_tau2', "#tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),
    variable('ca08filtered_tau3/ca08filtered_tau2', "filtered #tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),
    variable('ca08pruned_tau3/ca08pruned_tau2', "pruned #tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),
    variable('ca08trimmed_tau3/ca08trimmed_tau2', "trimmed #tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),
    variable('ca08softdrop_tau3/ca08softdrop_tau2', "softdrop #tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),    
]

tau31_vars_15 = [
    variable('ca15_tau3/ca15_tau1', "#tau_{3}/#tau_{1}  (R=1.5)", 0, 1.),
    variable('ca15filtered_tau3/ca15filtered_tau1', "filtered #tau_{3}/#tau_{1}  (R=1.5)", 0, 1.),
    variable('ca15pruned_tau3/ca15pruned_tau1', "pruned #tau_{3}/#tau_{1}  (R=1.5)", 0, 1.),
    variable('ca15trimmed_tau3/ca15trimmed_tau1', "trimmed #tau_{3}/#tau_{1}  (R=1.5)", 0, 1.),
    variable('ca15softdrop_tau3/ca15softdrop_tau1', "softdrop #tau_{3}/#tau_{1}  (R=1.5)", 0, 1.),    
]

tau31_vars_08 = [
    variable('ca08_tau3/ca08_tau1', "#tau_{3}/#tau_{1}  (R=0.8)", 0.01, 1.),
    variable('ca08filtered_tau3/ca08filtered_tau1', "filtered #tau_{3}/#tau_{1}  (R=0.8)", 0.01, 1.),
    variable('ca08pruned_tau3/ca08pruned_tau1', "pruned #tau_{3}/#tau_{1}  (R=0.8)", 0.01, 1.),
    variable('ca08trimmed_tau3/ca08trimmed_tau1', "trimmed #tau_{3}/#tau_{1}  (R=0.8)", 0.01, 1.),
    variable('ca08softdrop_tau3/ca08softdrop_tau1', "softdrop #tau_{3}/#tau_{1}  (R=0.8)", 0.01, 1.),    
]


btag_vars = [
    variable('ca15_btag', "btag (R=1.5)", 0, 10),
    variable('ca08_btag', "btag (R=0.8)", 0, 10),
]



htt_vars = [
    variable('looseMultiRHTT_mass', "HTT m", 0, 400, unit = "GeV"),
    variable('looseMultiRHTT_fW', "HTT f_{W}", 0, 0.8),
    variable('looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected', "HTT #Delta R_{min,exp}", -0.5, 1.5),
]

tagger_vars_15 = htt_vars + [variable('log(ca15_chi)', "log(#chi) (R=1.5)", -10., 10, extra_cut = 'ca15_chi>0'),
                             variable('ca15cmstt_minMass', "CMSTT minMass (R=1.5)", 0., 400, unit = "GeV")
                             ]
                             

tagger_vars_08 = [
    variable('ca08cmstt_minMass', "CMSTT minMass (R=0.8)", 0., 250, unit = "GeV"),
    variable('ca08cmstt_topMass', "CMSTT topMass (R=0.8)", 0., 600., unit = "GeV"),
    variable('log(ca08_chi)', "log(#chi) (R=0.8)", -10., 10, extra_cut = 'ca08_chi>0'),
]

tagger_vars = tagger_vars_15 + tagger_vars_08

good_vars = [ variable.di['ca08trimmed_mass'],
              variable.di['ca08softdrop_mass'],
              variable.di['ca08_tau3/ca08_tau2'],
              variable.di['log(ca15_chi)'],
              variable.di['looseMultiRHTT_mass'],
              variable.di['looseMultiRHTT_fW'],
              variable.di['ca08cmstt_topMass'],              
              variable.di['ca08cmstt_minMass'],
]
              

all_vars_15 = mass_vars_15 + tau_vars_15 + tagger_vars_15
all_vars_08 = mass_vars_08 + tau_vars_08 + tagger_vars_08

all_vars = all_vars_08 + all_vars_15
