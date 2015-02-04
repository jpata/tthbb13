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


########################################
# Define plots and do fits
########################################

samples = ["zprime_m750",
           "zprime_m1000",
           "zprime_m1250",
           "zprime_m2000_low",
           "zprime_m2000",
           "zprime_m3000",
           "zprime_m4000"]

multi_cuts = [fiducial_cuts[sample] + "&&(weight>0)&&(looseMultiRHTT_ptFiltForRminExp>0)" for sample in samples]

plotSettings(samples,             
             "looseMultiRHTT_ptFiltForRminExp", "looseMultiRHTT_Rmin",             
             multi_cuts,
             200, 220, 2000, 100, 0.5, 1.3,
             sample_type = "multiple",
             do_legend        = False,
)

makePlots(weighted_files)




