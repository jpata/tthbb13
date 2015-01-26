
#!/usr/bin/env python
"""
Collection of Higgs Tagging Variables (so we can use them across Plotting/Correlation/TMVA)
"""

import os

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.VariableHelpers import variable
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.VariableHelpers import variable


prettier_names = {'ca15': "Ungroomed",
                  'ca15filteredn2r2': "Filter(n=2, R=0.2)",
                  'ca15filteredn2r3': "Filter(n=2, R=0.3)",
                  'ca15filteredn3r3': "Filter(n=3, R=0.3)",
                  'ca15filteredn4r2': "Filter(n=4, R=0.2)",
                  'ca15massdrop': "MD",
                  'ca15massdropfilteredn2r2': "MD + Filter(n=2, R=0.2)",
                  'ca15massdropfilteredn2r3': "MD + Filter(n=2, R=0.3)",
                  'ca15massdropfilteredn3r3': "MD + Filter(n=3, R=0.3)",
                  'ca15massdropfilteredn4r2': "MD + Filter(n=4, R=0.2)",
                  'ca15prunedz1r5': "Pruner(z=0.1, r=0.5)",
                  'ca15prunedz2r5': "Pruner(z=0.2, r=0.5)",
                  'ca15prunedz1r3': "Pruner(z=0.1, r=0.3)",
                  'ca15trimmedr2f6': "Trimmer(r=0.2, f=0.06)",
                  'ca15trimmedr2f3': "Trimmer(r=0.2, f=0.03)",
                  'ca15trimmedr2f1': "Trimmer(r=0.2, f=0.01)",
                  'ca15softdropz15b2': "Softdrop(z=0.15, #beta=2)",
                  'ca15softdropz10b0': "Softdrop(z=0.1, #beta=0)",
                  'ca15softdropz5b0':  "Softdrop(z=0.05, #beta=0)",
}



li_fjs = ['ca15',
          'ca15filteredn2r2',
          'ca15filteredn2r3',
          'ca15filteredn3r3',
          'ca15filteredn4r2',
          'ca15massdrop',
          'ca15massdropfilteredn2r2',
          'ca15massdropfilteredn2r3',
          'ca15massdropfilteredn3r3',
          'ca15massdropfilteredn4r2',
          'ca15prunedz1r5',
          'ca15prunedz2r5',
          'ca15prunedz1r3',
          'ca15trimmedr2f3',
          'ca15trimmedr2f1',
          'ca15trimmedr2f6',
          'ca15softdropz10b0',
          'ca15softdropz5b0',
          'ca15softdropz15b2']


mass_vars = [ variable(fj+"_mass", fj, 0, 800, unit = "GeV") for fj in li_fjs   ]

    

#    variable('ca15_mass', "m", 0, 800, unit = "GeV"),
#    variable('ca15filtered_mass', "filtered m", 0, 800, unit = "GeV"),
#    variable('ca15massdrop_mass', "massdrop m", 0, 800, unit = "GeV"),
#    variable('ca15massdropfiltered_mass', "massdrop+filtered m", 0, 800, unit = "GeV"),
#    variable('ca15pruned_mass', "pruned m", 0, 800, unit = "GeV"),
#    variable('ca15trimmed_mass', "trimmed m", 0, 800, unit = "GeV"),
#    variable('ca15softdrop_mass', "softdrop m", 0, 800, unit = "GeV"),   


tau_vars = [
#    variable('ca15_tau2/ca15_tau1', "tau_{2}/tau_{1}", 0, 1, unit = ""),
#    variable('ca15filtered_tau2/ca15filtered_tau1', "filtered tau_{2}/tau_{1}", 0, 1, unit = ""),
#    variable('ca15massdrop_tau2/ca15massdrop_tau1', "massdrop tau_{2}/tau_{1}", 0, 1, unit = ""),
#    variable('ca15massdropfiltered_tau2/ca15massdropfiltered_tau1', "massdrop+filtered tau_{2}/tau_{1}", 0, 1, unit = ""),
#    variable('ca15pruned_tau2/ca15pruned_tau1', "pruned tau_{2}/tau_{1}", 0, 1, unit = ""),
#    variable('ca15trimmed_tau2/ca15trimmed_tau1', "trimmed tau_{2}/tau_{1}", 0, 1, unit = ""),
#    variable('ca15softdrop_tau2/ca15softdrop_tau1', "softdrop tau_{2}/tau_{1}", 0, 1, unit = ""),   
]

btag_vars = [
    variable('ca15_btag', "btag", 0, 1, unit = "")

]


good_vars = [
    variable.di['ca15_mass'],
    variable.di['ca15trimmedr2f6_mass'],
    variable.di['ca15trimmedr2f3_mass'],
    variable.di['ca15filteredn4r2_mass'],
    variable.di['ca15massdropfilteredn4r2_mass'],
    variable.di['ca15massdropfilteredn2r3_mass'],
    variable.di['ca15prunedz2r5_mass'],
    variable.di['ca15softdropz15b2_mass'],

#    variable.di["ca15trimmed_mass"],
#    variable.di["ca15_tau2/ca15_tau1"],
#    variable.di["ca15_btag"],
]

all_vars = mass_vars + tau_vars + btag_vars
