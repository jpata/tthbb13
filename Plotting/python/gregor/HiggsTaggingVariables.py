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


mass_vars = [
#    variable('ca15_mass', "m", 0, 800, unit = "GeV"),
#    variable('ca15filtered_mass', "filtered m", 0, 800, unit = "GeV"),
#    variable('ca15massdrop_mass', "massdrop m", 0, 800, unit = "GeV"),
#    variable('ca15massdropfiltered_mass', "massdrop+filtered m", 0, 800, unit = "GeV"),
#    variable('ca15pruned_mass', "pruned m", 0, 800, unit = "GeV"),
    variable('ca15trimmed_mass', "trimmed m", 0, 800, unit = "GeV"),
#    variable('ca15softdrop_mass', "softdrop m", 0, 800, unit = "GeV"),   
]

tau_vars = [
    variable('ca15_tau2/ca15_tau1', "tau_{2}/tau_{1}", 0, 1, unit = ""),
    variable('ca15filtered_tau2/ca15filtered_tau1', "filtered tau_{2}/tau_{1}", 0, 1, unit = ""),
    variable('ca15massdrop_tau2/ca15massdrop_tau1', "massdrop tau_{2}/tau_{1}", 0, 1, unit = ""),
    variable('ca15massdropfiltered_tau2/ca15massdropfiltered_tau1', "massdrop+filtered tau_{2}/tau_{1}", 0, 1, unit = ""),
    variable('ca15pruned_tau2/ca15pruned_tau1', "pruned tau_{2}/tau_{1}", 0, 1, unit = ""),
    variable('ca15trimmed_tau2/ca15trimmed_tau1', "trimmed tau_{2}/tau_{1}", 0, 1, unit = ""),
    variable('ca15softdrop_tau2/ca15softdrop_tau1', "softdrop tau_{2}/tau_{1}", 0, 1, unit = ""),   
]

btag_vars = [
    variable('ca15_btag', "btag", 0, 1, unit = "")
]


good_vars = [
    variable.di["ca15trimmed_mass"],
    variable.di["ca15_tau2/ca15_tau1"],
    variable.di["ca15_btag"],
]

all_vars = mass_vars + tau_vars + btag_vars
