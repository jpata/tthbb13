#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.PlotProfilesHelpers import *
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import *
else:
    from TTH.Plotting.python.Helpers.PlotProfilesHelpers import *
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import *


full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + "-weighted.root"


########################################
# Define plots and do fits
########################################

samples = [
    "zprime_m1000_low",
    "zprime_m1000",
    "zprime_m2000_low",
    "zprime_m2000",
]

multi_cuts = ["((pt>{0})&&(pt<{1})&&(fabs(eta)<{2})&&(weight>0)&&(looseOptRHTT_ptForRoptCalc>0)&&(looseOptRHTT_mass>120)&&(looseOptRHTT_mass<220)&&(looseOptRHTT_fRec<0.175))*weight".format(ranges[sample][0],
                                                                                                                ranges[sample][1],
                                                                                                                ranges[sample][2]) for sample in samples]


plotSettings(samples,             
             "looseOptRHTT_ptForRoptCalc", "looseOptRHTT_Ropt",             
             multi_cuts,
             50, 200, 1000, 12, 0.45, 1.65,
             sample_type = "multiple",
             do_legend        = False,
)

makePlots(full_file_names)




