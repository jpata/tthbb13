#!/usr/bin/env python
"""
Schedule the testing of different variable/method-sets with TMVA
"""

########################################
# Imports 
########################################

import pickle
import os
from copy import deepcopy

import ROOT

# Our support Code
# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCMultiple
    from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.gregor.TopTaggingVariables import *
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCMultiple
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.TopTaggingVariables import *

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


########################################
# Configuration
########################################

run_TMVA = False

pairs = { 
    "pt-800-to-1000-v18" : ["zprime_m2000_v18", "qcd_800_1000_v18", "fixed R_{microjet}"],
    "pt-800-to-1000-v19" : ["zprime_m2000_v19", "qcd_800_1000_v19", "dynamic R_{microjet}"],
}



files = {
    "zprime_m2000_v18" : "ntop_v18_zprime_m2000_1p_13tev-tagging",     
    "qcd_800_1000_v18" : "ntop_v18_qcd_800_1000_pythia8_13tev-tagging",
    "zprime_m2000_v19" : "ntop_v19_zprime_m2000_1p_13tev-tagging",     
    "qcd_800_1000_v19" : "ntop_v19_qcd_800_1000_pythia8_13tev-tagging",
}

fiducial_cut = "((pt>801)&&(pt<999)&&(fabs(eta)<1.5))"
basepath = '/scratch/gregor/'
li_methods      = ["Cuts"]

li_TMVAs = []    
for pair_name, pair in pairs.iteritems():    
    
    sample_sig = pair[0]
    sample_bkg = pair[1]

    file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
    file_name_bg   = basepath + files[sample_bkg] + "-weighted.root"


    for v in sd_vars:
        name = "{0}_{1}_{2}".format(sample_sig, sample_bkg, v.name)
        name = name.replace("/","_")
        li_TMVAs.append( TMVASetup( name,
                                    v.pretty_name +" " +pair[2],
                                    li_methods, 
                                    [v],
                                    file_name_sig,
                                    file_name_bg,
                                    fiducial_cut_sig = fiducial_cut,
                                    fiducial_cut_bg  = fiducial_cut,
                                    weight_sig = "weight",
                                    weight_bg  = "weight",
                                ))
    # end of loop over variables
# end of loop over paurs


print li_TMVAs

if run_TMVA:
    for setup in li_TMVAs:
        doTMVA(setup)

plotROCMultiple("ROC_SDs", li_TMVAs)
