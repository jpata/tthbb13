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
    variable('ca15_mass', "m", 0, 800, unit = "GeV"),
    variable('ca15filtered_mass', "filtered m", 0, 400, unit = "GeV"),
    variable('ca15pruned_mass', "pruned m", 0, 800, unit = "GeV"),
    variable('ca15trimmed_mass', "trimmed m", 0, 800, unit = "GeV"),
    variable('ca15softdrop_mass', "softdrop m", 0, 400, unit = "GeV"),   
]

all_vars = mass_vars
