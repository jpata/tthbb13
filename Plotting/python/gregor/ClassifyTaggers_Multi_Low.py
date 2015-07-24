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
    from TTH.Plotting.gregor.TopSamples import files, ranges, nosize_fiducial_cuts, fiducial_cuts, pretty_fiducial_cuts, pairs
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCs
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import files, ranges, nosize_fiducial_cuts, fiducial_cuts, pretty_fiducial_cuts, pairs


myStyle.SetTitleXOffset(1.3)
myStyle.SetTitleYOffset(1.7)
myStyle.SetPadLeftMargin(0.19)
myStyle.SetPadBottomMargin(0.13)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()

pool = mp.Pool(processes=16)
  
########################################
# Configuration
########################################

name = "pt-300-to-470"
sample_sig = "zprime_m1000"
sample_bkg = "qcd_300_470"


basepath = '/scratch/gregor/'
file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
file_name_bkg  = basepath + files[sample_bkg] + "-weighted.root" 
li_methods      = ["Cuts"]

setups = {}
btag_setups = {}

for label in ["xxtruth",
              "xxnosize", 
              #"forWP"
]:
    
    if label == "xxtruth":
        signal_fiducial_cuts = fiducial_cuts[sample_sig]
        bkgrnd_fiducial_cuts = fiducial_cuts[sample_bkg]    
        weight = "(weight)"
    if label == "forWP":
        signal_fiducial_cuts = "((pt>300)&&(ca15_pt>300)&&(top_size<0.8))"
        bkgrnd_fiducial_cuts = "((pt>300)&&(ca15_pt>300)&&(top_size<0.8))"
        weight = "(1)"
    if label == "xxnosize":
        signal_fiducial_cuts = nosize_fiducial_cuts[sample_sig]
        bkgrnd_fiducial_cuts = nosize_fiducial_cuts[sample_bkg]    
        weight = "(1)"

        
    setups[label] = []
    btag_setups[label] = []



##    # Old HTT Mass + fRec + tau3/tau2
##    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "OldHTT_mass_tau3tau2", label),
##                       "HTT - m, fRec, tau_{3}/tau_{2}",
##                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=1000000:VarProp[1]=FSmart:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[0]=140:CutRangeMax[0]=250.:CutRangeMin[2]=0:CutRangeMax[2]=1."]], 
##                       [variable.di['msortHTT_mass'],
##                        variable.di['msortHTT_fRec'],
##                        variable.di['ca15_tau3/ca15_tau2'],
##                    ],                               
##                       [],
##                       file_name_sig,
##                       file_name_bkg,
##                       fiducial_cut_sig = signal_fiducial_cuts,
##                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
##                       weight_sig = weight,
##                       weight_bkg = weight)
##    setups[label].append(setup)



##    # HTT Mass + fRec + DeltaR + tau3/tau2
##    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_dr_tau", label),
##                       "HTT V2 - m, fRec, #Delta R, #tau_{3}/#tau_{2}",
##                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=1000000:VarProp[1]=FSmart:VarProp[3]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=130:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=-0.5:CutRangeMax[2]=0.5:CutRangeMin[3]=0:CutRangeMax[3]=1"]], 
##                       [variable.di['looseOptRHTT_mass'],
##                        variable.di['looseOptRHTT_fRec'],
##                        variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc'],
##                        variable.di['ca15_tau3/ca15_tau2'],
##                    ],                               
##                       [],
##                       file_name_sig,
##                       file_name_bkg,
##                       fiducial_cut_sig = signal_fiducial_cuts,
##                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
##                       weight_sig = weight,
##                       weight_bkg = weight)
##    setups[label].append(setup)

    # HTT Mass + fRec + DeltaR + groomed tau3/tau2
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_dr_groomed_tau", label),
                       "HTT V2 - m, fRec, #Delta R, #tau_{3, SD}/#tau_{2, SD}",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=8000000:VarProp[1]=FSmart:VarProp[3]=FSmart:CutRangeMin[0]=50:CutRangeMax[0]=130:CutRangeMin[1]=0:CutRangeMax[1]=0.3:CutRangeMin[2]=-0.5:CutRangeMax[2]=0.5:CutRangeMin[3]=0.2:CutRangeMax[3]=1"]], 
                       [variable.di['looseOptRHTT_mass'],
                        variable.di['looseOptRHTT_fRec'],
                        variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc'],
                        variable.di['ca15softdropz20b10_tau3/ca15softdropz20b10_tau2'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = signal_fiducial_cuts,
                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                       weight_sig = weight,
                       weight_bkg = weight)
    setups[label].append(setup)

##    # HTT Mass + fRec + tau3/tau2
##    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_tau", label),
##                       "HTT V2 - m, fRec, #tau_{3}/#tau_{2}",
##                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=1000000:VarProp[1]=FSmart:VarProp[2]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=130:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=0:CutRangeMax[2]=1"]], 
##                       [variable.di['looseOptRHTT_mass'],
##                        variable.di['looseOptRHTT_fRec'],
##                        variable.di['ca15_tau3/ca15_tau2'],
##                    ],                               
##                       [],
##                       file_name_sig,
##                       file_name_bkg,
##                       fiducial_cut_sig = signal_fiducial_cuts,
##                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
##                       weight_sig = weight,
##                       weight_bkg = weight)
##    setups[label].append(setup)


##    # HTT Mass + fRec + groomed tau3/tau2
##    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_groomed_tau", label),
##                       "HTT V2 - m, fRec, #tau_{3, SD}/#tau_{2, SD}",
##                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=8000000:VarProp[1]=FSmart:VarProp[2]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=130:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=0:CutRangeMax[2]=1"]], 
##                       [variable.di['looseOptRHTT_mass'],
##                        variable.di['looseOptRHTT_fRec'],
##                        variable.di['ca15softdropz20b10_tau3/ca15softdropz20b10_tau2'],
##                    ],                               
##                       [],
##                       file_name_sig,
##                       file_name_bkg,
##                       fiducial_cut_sig = signal_fiducial_cuts,
##                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
##                       weight_sig = weight,
##                       weight_bkg = weight)
##    setups[label].append(setup)

    # Shower Deconstruction
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "SD", label),
                      "log(#chi)",
                      [["Cuts", "V:FitMethod=MC:SampleSize=800000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=8:VarProp[0]=FSmart"]], 
                      [variable.di['log(ca15_chi2)']],
                      [],
                      file_name_sig,
                      file_name_bkg,
                       fiducial_cut_sig = signal_fiducial_cuts,
                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                      weight_sig = weight,
                      weight_bkg = weight)
    setups[label].append(setup)

    # Softdrop Mass + Ungroomed Tau3/tau2
    mass_var  = "ca15softdropz20b10_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "{0}_" + mass_var + "Mass_Tau", label.replace("x","")),
                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + " + #tau_{3}/#tau_{2}",
                      [["Cuts", "V:FitMethod=MC:SampleSize=600000:Sigma=0.3:CutRangeMin[0]=0.2:CutRangeMax[0]=1:CutRangeMin[1]=50:CutRangeMax[1]=180:VarProp[0]=FSmart"]], 
                      [variable.di['ca15_tau3/ca15_tau2'],
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

    # Softdrop Mass + groomed Tau3/tau2
    mass_var  = "ca15softdropz20b10_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, mass_var + "Mass_Groomed_Tau", label),
                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + " + #tau_{3, SD}/#tau_{2, SD}",
                      [["Cuts", "V:FitMethod=MC:SampleSize=800000:Sigma=0.3:CutRangeMin[0]=0.2:CutRangeMax[0]=1:CutRangeMin[1]=50:CutRangeMax[1]=180:VarProp[0]=FSmart"]], 
                      [variable.di['ca15softdropz20b10_tau3/ca15softdropz20b10_tau2'],
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

    # Softdrop Mass + SD
    mass_var  = "ca15softdropz20b10_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, mass_var + "Mass_SD", label),
                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + " + log(#chi)",
                      [["Cuts", "V:FitMethod=MC:SampleSize=900000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=10:CutRangeMin[1]=50:CutRangeMax[1]=180:VarProp[0]=FSmart"]], 
                      [variable.di['log(ca15_chi2)'],
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


    # Softdrop Mass + groomed Tau3/tau2 + SD
    mass_var  = "ca15softdropz20b10_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, mass_var + "Mass_Groomed_Tau_SD", label),
                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + ", #tau_{3, SD}/#tau_{2, SD}, log(#chi)",
                      [["Cuts", "V:FitMethod=MC:SampleSize=1600000:Sigma=0.3:CutRangeMin[0]=0.2:CutRangeMax[0]=1:CutRangeMin[1]=50:CutRangeMax[1]=180:VarProp[0]=FSmart:CutRangeMin[2]=-10:CutRangeMax[2]=10:VarProp[2]=FSmart"]], 
                      [variable.di['ca15softdropz20b10_tau3/ca15softdropz20b10_tau2'],
                       variable.di[mass_var],
                       variable.di['log(ca15_chi2)']
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig = signal_fiducial_cuts,
                      fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                      weight_sig = weight,
                      weight_bkg = weight)
    setups[label].append(setup)

    # HTT Mass + fRec + DeltaR + groomed tau3/tau2 + btag
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_dr_groomed_tau_btag", label),
                       "HTT V2 - m, fRec, #Delta R, #tau_{3, SD}/#tau_{2, SD}, b",
                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=4000000:VarProp[1]=FSmart:VarProp[3]=FSmart:VarProp[4]=FSmart:CutRangeMin[0]=50:CutRangeMax[0]=130:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=-0.5:CutRangeMax[2]=0.5:CutRangeMin[3]=0.2:CutRangeMax[3]=1:CutRangeMin[4]=0.1:CutRangeMax[4]=1:"]], 
                       [variable.di['looseOptRHTT_mass'],
                        variable.di['looseOptRHTT_fRec'],
                        variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc'],
                        variable.di['ca15softdropz20b10_tau3/ca15softdropz20b10_tau2'],
                        variable.di['ca15softdropz20b10forbtag_btag'],
                    ],                               
                       [],
                       file_name_sig,
                       file_name_bkg,
                       fiducial_cut_sig = signal_fiducial_cuts,
                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                       weight_sig = weight,
                       weight_bkg = weight)
    setups[label].append(setup)

##    # HTT Mass + fRec + groomed tau3/tau2 + btag
##    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "OptRHTT_mass_frec_groomed_tau_btag", label),
##                       "HTT V2 - m, fRec, Groomed #tau_{3}/#tau_{2}, b",
##                       [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=1000000:VarProp[1]=FSmart:VarProp[2]=FSmart:VarProp[3]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=130:CutRangeMin[1]=0:CutRangeMax[1]=0.5:CutRangeMin[2]=0:CutRangeMax[2]=1:CutRangeMin[3]=0:CutRangeMax[3]=1"]], 
##                       [variable.di['looseOptRHTT_mass'],
##                        variable.di['looseOptRHTT_fRec'],
##                        variable.di['ca15softdropz20b10_tau3/ca15softdropz20b10_tau2'],
##                        variable.di['ca15softdropz20b10forbtag_btag'],
##                    ],                               
##                       [],
##                       file_name_sig,
##                       file_name_bkg,
##                       fiducial_cut_sig = signal_fiducial_cuts,
##                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
##                       weight_sig = weight,
##                       weight_bkg = weight)
##    btag_setups[label].append(setup)

    # Shower Deconstruction + btag
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, "SD_btag", label),
                      "log(#chi), b",
                      [["Cuts", "V:FitMethod=MC:SampleSize=800000:Sigma=0.3:CutRangeMin[0]=-10:CutRangeMax[0]=8:CutRangeMin[1]=0:CutRangeMax[1]=1.:VarProp[1]=FSmart:VarProp[0]=FSmart"]], 
                      [variable.di['log(ca15_chi2)'],
                       variable.di['ca15softdropz20b10forbtag_btag'],
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                       fiducial_cut_sig = signal_fiducial_cuts,
                       fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                      weight_sig = weight,
                      weight_bkg = weight)
    setups[label].append(setup)

##    # Softdrop Mass + Ungroomed Tau3/tau2 + btag
##    mass_var  = "ca15softdropz20b10_mass"
##    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, mass_var + "Mass_Tau_btag", label),
##                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + " + #tau_{3}/#tau_{2}, b",
##                      [["Cuts", "V:FitMethod=MC:SampleSize=200000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=1:CutRangeMin[1]=0:CutRangeMax[1]=180:VarProp[0]=FSmart:CutRangeMin[2]=0:CutRangeMax[2]=1.:VarProp[2]=FSmart"]], 
##                      [variable.di['ca15_tau3/ca15_tau2'],
##                       variable.di[mass_var],
##                       variable.di['ca15softdropz20b10forbtag_btag'],
##                   ],
##                      [],
##                      file_name_sig,
##                      file_name_bkg,
##                      fiducial_cut_sig = signal_fiducial_cuts,
##                      fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
##                      weight_sig = weight,
##                      weight_bkg = weight)
##    btag_setups[label].append(setup)

    # Softdrop Mass + groomed Tau3/tau2 + b-tag
    mass_var  = "ca15softdropz20b10_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, mass_var + "Mass_Groomed_Tau_btag", label),
                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + ", #tau_{3, SD}/#tau_{2, SD} + b",
                      [["Cuts", "V:FitMethod=MC:SampleSize=800000:Sigma=0.3:CutRangeMin[0]=0/2:CutRangeMax[0]=1:CutRangeMin[1]=50:CutRangeMax[1]=180:VarProp[0]=FSmart:CutRangeMin[2]=0.1:CutRangeMax[2]=1.:VarProp[2]=FSmart"]], 
                      [variable.di['ca15softdropz20b10_tau3/ca15softdropz20b10_tau2'],
                       variable.di[mass_var],
                       variable.di['ca15softdropz20b10forbtag_btag'],
                   ],
                      [],
                      file_name_sig,
                      file_name_bkg,
                      fiducial_cut_sig = signal_fiducial_cuts,
                      fiducial_cut_bkg  = bkgrnd_fiducial_cuts,
                      weight_sig = weight,
                      weight_bkg = weight)
    setups[label].append(setup)

    # Softdrop Mass + groomed Tau3/tau2 + SD + btag
    mass_var  = "ca15softdropz20b10_mass"
    setup = TMVASetup("{0}_{1}_{2}_{3}".format(sample_sig, sample_bkg, mass_var + "Mass_Groomed_Tau_SD_btag", label),
                      variable.di[mass_var].pretty_name.replace("Mass","").replace("Softdrop","m_{SD}") + ", #tau_{3, SD}/#tau_{2, SD}, log(#chi), b",
                      [["Cuts", "V:FitMethod=MC:SampleSize=3200000:Sigma=0.3:CutRangeMin[0]=0.:CutRangeMax[0]=1:CutRangeMin[1]=50:CutRangeMax[1]=180:CutRangeMin[2]=-10:CutRangeMax[2]=10:CutRangeMin[3]=0:CutRangeMax[3]=1.:VarProp[0]=FSmart:VarProp[2]=FSmart:VarProp[3]=FSmart"]], 
                      [variable.di['ca15softdropz20b10_tau3/ca15softdropz20b10_tau2'],
                       variable.di[mass_var],
                       variable.di['log(ca15_chi2)'],
                       variable.di['ca15softdropz20b10forbtag_btag'],
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
for label in ["xxtruth", 
              "xxnosize"
          ]:
    all_setups.extend( setups[label])

#pool.map(doTMVA, all_setups)

for label in [
        "xxtruth", 
        #"forWP", 
        "xxnosize"
]:
    
    if label == "xxtruth":
        plotROCs(label + "ROC_" + name, 
                 setups[label], 
                 extra_text = [pretty_fiducial_cuts[sample_sig],
                               "flat p_{T} and #eta",
                               "#Delta R(top,parton) < 0.8"],
                 error_band = False)
                                 
    elif label == "xxnosize":
        plotROCs(label + "ROC_" + name, setups[label], 
                 extra_text = [pretty_fiducial_cuts[sample_sig]],
                 error_band = False)

    else:
        plotROCs(label + "ROC_" + name, setups[label])        
        #plotROCs(label + "btag_ROC_" + name, btag_setups[label])        












