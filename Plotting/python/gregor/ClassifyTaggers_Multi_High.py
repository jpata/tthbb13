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
import multiprocessing as mp

import ROOT

# Our support Code
# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCs
    from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import files, ranges, fiducial_cuts, nosize_fiducial_cuts, pretty_fiducial_cuts, pairs
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCs
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import files, ranges, fiducial_cuts, nosize_fiducial_cuts, pretty_fiducial_cuts, pairs


myStyle.SetTitleXOffset(1.3)
myStyle.SetTitleYOffset(1.7)
myStyle.SetPadLeftMargin(0.19)
myStyle.SetPadBottomMargin(0.13)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()

pool = mp.Pool(processes=10)
  
########################################
# Configuration
########################################

name = "pt-800-to-1000"
sample_sig = "zprime_m2000"
sample_bkg = "qcd_800_1000"


basepath = '/scratch/gregor/'
file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
file_name_bkg  = basepath + files[sample_bkg] + "-weighted.root" 
li_methods      = ["Cuts"]

setups = {}
btag_setups = {}

for label in ["xtruth", 
              #"forWP", 
              "xnosize"
]:
    
    if label == "xtruth":
        signal_fiducial_cuts = fiducial_cuts[sample_sig]
        bkgrnd_fiducial_cuts = fiducial_cuts[sample_bkg]    
        weight = "(weight)"
    if label == "forWP":
        signal_fiducial_cuts = "((pt>800)&&(ak08_pt>500)&&(top_size<0.6))"
        bkgrnd_fiducial_cuts = "((pt>800)&&(ak08_pt>500)&&(top_size<0.6))"
        weight = "(1)"
    if label == "xnosize":
        signal_fiducial_cuts = nosize_fiducial_cuts[sample_sig]
        bkgrnd_fiducial_cuts = nosize_fiducial_cuts[sample_bkg]    
        weight = "(1)"

    setups[label] = []
    btag_setups[label] = []


    # HTT Mass + fRec + DeltaR + tau3/tau2
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_dr_tau", label),
                       "HTT V2 - m, fRec, #Delta R, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=2000000:VarProp[1]=FSmart:VarProp[3]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=130:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=-0.5:CutRangeMax[2]=0.5:CutRangeMin[3]=0:CutRangeMax[3]=1"]], 
                       [variable.di['looseOptRHTT_mass'],
                        variable.di['looseOptRHTT_fRec'],
                        variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc'],
                        variable.di['ak08_tau3/ak08_tau2'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = signal_fiducial_cuts,
                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                       weight_sig = weight,
                       weight_bkg = weight)
    setups[label].append(setup)


#    # HTT Mass + fRec + tau3/tau2
#    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_tau", label),
#                       "HTT V2 - m, fRec, #tau_{3}/#tau_{2}",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=1000000:VarProp[1]=FSmart:VarProp[2]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=130:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=0:CutRangeMax[2]=1"]], 
#                       [variable.di['looseOptRHTT_mass'],
#                        variable.di['looseOptRHTT_fRec'],
#                        variable.di['ak08_tau3/ak08_tau2'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig = signal_fiducial_cuts,
#                       fiducial_cut_bkg = bkgrnd_fiducial_cuts,
#                       weight_sig = weight,
#                       weight_bkg = weight)
#    setups[label].append(setup)

    # CMSTT + tau
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "CMSTT_tau", label),
                       "CMSTT - min. m, top m, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=2000000:VarProp[2]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=150:CutRangeMin[1]=0:CutRangeMax[1]=300:CutRangeMin[2]=0:CutRangeMax[2]=1"]], 
                       [variable.di['ak08cmstt_minMass'],
                        variable.di['ak08cmstt_topMass'],
                        variable.di['ak08_tau3/ak08_tau2'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = signal_fiducial_cuts,
                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts, 
                       weight_sig = weight,
                       weight_bkg = weight)
    setups[label].append(setup)

    # Softdrop Mass + CMSTT Min mass + tau
    mass_var  = "ak08softdropz10b00_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}_{4}".format(sample_sig, sample_bkg, mass_var, "CMSTT_tau", label),
                       variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + ", min. m, #tau_{3}/#tau_{2}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=2000000:VarProp[2]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=150:CutRangeMin[1]=20:CutRangeMax[1]=180:CutRangeMin[2]=0:CutRangeMax[2]=1"]], 
                       [variable.di['ak08cmstt_minMass'],
                        variable.di[mass_var],
                        variable.di['ak08_tau3/ak08_tau2'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = signal_fiducial_cuts,
                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts, 
                       weight_sig = weight,
                       weight_bkg = weight)
    setups[label].append(setup)


    # Softdrop Mass + CMSTT Min mass + tau + btag
    mass_var  = "ak08softdropz10b00_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}_{4}".format(sample_sig, sample_bkg, mass_var, "CMSTT_tau_btag", label),
                       variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + ", min. m, #tau_{3}/#tau_{2}, b",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=2000000:VarProp[2]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=150:CutRangeMin[1]=20:CutRangeMax[1]=180:CutRangeMin[2]=0:CutRangeMax[2]=1:CutRangeMin[3]=0:CutRangeMax[3]=1:VarProp[3]=FSmart"]], 
                       [variable.di['ak08cmstt_minMass'],
                        variable.di[mass_var],
                        variable.di['ak08_tau3/ak08_tau2'],
                        variable.di['ak08softdropz10b00forbtag_btag'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = signal_fiducial_cuts,
                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts, 
                       weight_sig = weight,
                       weight_bkg = weight)
    setups[label].append(setup)



    # Shower Deconstruction
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "SD", label),
                      "log(#chi)",
                      [["Cuts", "V:FitMethod=MC:SampleSize=200000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=8"]], 
                      [variable.di['log(ak08_chi1)']],
                      [],
                      file_name_sig,
                      file_name_bkg,
                       fiducial_cut_sig = signal_fiducial_cuts,
                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                      weight_sig = weight,
                      weight_bkg = weight)
    setups[label].append(setup)

    # Softdrop Mass + Ungroomed Tau3/tau2
    mass_var  = "ak08softdropz10b00_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "{0}_" + mass_var + "Mass_Tau", label),
                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + ", #tau_{3}/#tau_{2}",
                      [["Cuts", "V:FitMethod=MC:SampleSize=400000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:CutRangeMin[1]=0:CutRangeMax[1]=180:VarProp[0]=FSmart"]], 
                      [variable.di['ak08_tau3/ak08_tau2'],
                       variable.di[mass_var],
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig = signal_fiducial_cuts,
                      fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                      weight_sig = weight,
                      weight_bkg = weight)
    setups[label].append(setup)


#    # Softdrop Mass + SD
#    mass_var  = "ak08softdropz10b00_mass"
#    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, mass_var + "Mass_SD", label),
#                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + " + log(#chi)",
#                      [["Cuts", "V:FitMethod=MC:SampleSize=300000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=10:CutRangeMin[1]=0:CutRangeMax[1]=180"]], 
#                      [variable.di['log(ak08_chi1)'],
#                       variable.di[mass_var],
#                   ],
#                      [],
#                      file_name_sig,
#                      file_name_bkg,
#                      fiducial_cut_sig = signal_fiducial_cuts,
#                      fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
#                      weight_sig = weight,
#                      weight_bkg = weight)
#    setups[label].append(setup)


    # Softdrop Mass + Tau3/tau2 + SD
    mass_var  = "ak08softdropz10b00_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, mass_var + "Mass_Tau_SD", label),
                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + ", #tau_{3}/#tau_{2}, log(#chi)",
                      [["Cuts", "V:FitMethod=MC:SampleSize=800000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:CutRangeMin[1]=0:CutRangeMax[1]=180:VarProp[0]=FSmart:CutRangeMin[2]=-10:CutRangeMax[2]=10"]], 
                      [variable.di['ak08_tau3/ak08_tau2'],
                       variable.di[mass_var],
                       variable.di['log(ak08_chi1)']
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig = signal_fiducial_cuts,
                      fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                      weight_sig = weight,
                      weight_bkg = weight)
    setups[label].append(setup)








    # HTT Mass + fRec + DeltaR +  tau3/tau2 + btag
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_dr_tau_btag", label),
                       "HTT V2 - m, fRec, #Delta R, #tau_{3}/#tau_{2}, b",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=2000000:VarProp[1]=FSmart:VarProp[3]=FSmart:VarProp[4]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=130:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=-0.5:CutRangeMax[2]=0.5:CutRangeMin[3]=0:CutRangeMax[3]=1:CutRangeMin[4]=0:CutRangeMax[4]=1"]], 
                       [variable.di['looseOptRHTT_mass'],
                        variable.di['looseOptRHTT_fRec'],
                        variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc'],
                        variable.di['ak08_tau3/ak08_tau2'],
                        variable.di['ak08softdropz10b00forbtag_btag'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = signal_fiducial_cuts,
                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                       weight_sig = weight,
                       weight_bkg = weight)
    setups[label].append(setup)

#    # HTT Mass + fRec + tau3/tau2 + btag
#    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_tau_btag", label),
#                       "HTT V2 - m, fRec, #tau_{3}/#tau_{2}, b",
#                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=1000000:VarProp[1]=FSmart:VarProp[2]=FSmart:VarProp[3]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=130:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=0:CutRangeMax[2]=1:CutRangeMin[3]=0:CutRangeMax[3]=1"]], 
#                       [variable.di['looseOptRHTT_mass'],
#                        variable.di['looseOptRHTT_fRec'],
#                        variable.di['ak08_tau3/ak08_tau2'],
#                        variable.di['ak08softdropz10b00forbtag_btag'],
#                    ],                               
#                       [],
#                       file_name_sig,
#                       file_name_bkg,
#                       fiducial_cut_sig = signal_fiducial_cuts,
#                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
#                       weight_sig = weight,
#                       weight_bkg = weight)
#    btag_setups[label].append(setup)

    # CMSTT + tau + btag
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "CMSTT_tau_btag", label),
                       "CMSTT - min. m, top m, #tau_{3}/#tau_{2}, b",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=2000000:VarProp[2]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=150:CutRangeMin[1]=0:CutRangeMax[1]=300:CutRangeMin[2]=0:CutRangeMax[2]=1:CutRangeMin[3]=0:CutRangeMax[3]=1.:VarProp[3]=FSmart"]], 
                       [variable.di['ak08cmstt_minMass'],
                        variable.di['ak08cmstt_topMass'],
                        variable.di['ak08_tau3/ak08_tau2'],
                        variable.di['ak08softdropz10b00forbtag_btag'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = signal_fiducial_cuts,
                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts, 
                       weight_sig = weight,
                       weight_bkg = weight)
    setups[label].append(setup)

#
#    # Shower Deconstruction + btag
#    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "SD_btag", label),
#                      "log(#chi), b",
#                      [["Cuts", "V:FitMethod=MC:SampleSize=100000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=8:CutRangeMin[1]=0:CutRangeMax[1]=1.:VarProp[1]=FSmart"]], 
#                      [variable.di['log(ak08_chi1)'],
#                       variable.di['ak08softdropz10b00forbtag_btag'],
#                   ],
#                      [],
#                      file_name_sig,
#                      file_name_bkg,
#                       fiducial_cut_sig = signal_fiducial_cuts,
#                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
#                      weight_sig = weight,
#                      weight_bkg = weight)
#    btag_setups[label].append(setup)
#
    # Softdrop Mass + Ungroomed Tau3/tau2 + btag
    mass_var  = "ak08softdropz10b00_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, mass_var + "Mass_Tau_btag", label),
                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + ", #tau_{3}/#tau_{2}, b",
                      [["Cuts", "V:FitMethod=MC:SampleSize=400000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:CutRangeMin[1]=0:CutRangeMax[1]=180:VarProp[0]=FSmart:CutRangeMin[2]=0:CutRangeMax[2]=1.:VarProp[2]=FSmart"]], 
                      [variable.di['ak08_tau3/ak08_tau2'],
                       variable.di[mass_var],
                       variable.di['ak08softdropz10b00forbtag_btag'],
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig = signal_fiducial_cuts,
                      fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                      weight_sig = weight,
                      weight_bkg = weight)
    setups[label].append(setup)

    # Softdrop Mass + Tau3/tau2 + SD + btag
    mass_var  = "ak08softdropz10b00_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, mass_var + "Mass_Tau_SD_btag", label),
                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + ", #tau_{3}/#tau_{2}, log(#chi), b",
                      [["Cuts", "V:FitMethod=MC:SampleSize=800000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:CutRangeMin[1]=0:CutRangeMax[1]=180:VarProp[0]=FSmart:CutRangeMin[2]=-10:CutRangeMax[2]=10:CutRangeMin[3]=0:CutRangeMax[3]=1.:VarProp[3]=FSmart"]], 
                      [variable.di['ak08_tau3/ak08_tau2'],
                       variable.di[mass_var],
                       variable.di['log(ak08_chi1)'],
                       variable.di['ak08softdropz10b00forbtag_btag'],
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig = signal_fiducial_cuts,
                      fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                      weight_sig = weight,
                      weight_bkg = weight)
    setups[label].append(setup)


all_setups = []
for label in ["xtruth", 
              #"forWP", 
              "xnosize"]:
    all_setups.extend( setups[label])

#pool.map(doTMVA, all_setups)


for label in [
        "xtruth", 
        #"forWP", 
        "xnosize"
]:
    
    if label == "xtruth":
        plotROCs(label + "ROC_" + name, 
                 setups[label], 
                 extra_text = [pretty_fiducial_cuts[sample_sig],
                               "flat p_{T} and #eta",
                               "#Delta R(top,parton) < 0.6"],
                 error_band = False
        )


    elif label == "xnosize":
        plotROCs(label + "ROC_" + name, 
                 setups[label], 
                 [pretty_fiducial_cuts[sample_sig]],
                 error_band = False                 
        )

    else:
        plotROCs(label + "ROC_" + name, setups[label])        






