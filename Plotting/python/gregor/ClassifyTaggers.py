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
    from TTH.Plotting.gregor.TopSamples import files, ranges, fiducial_cuts, pretty_fiducial_cuts, pairs
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.TMVAHelpers import variable, TMVASetup, doTMVA, plotROCs
    from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import files, ranges, fiducial_cuts, pretty_fiducial_cuts, pairs


myStyle.SetTitleXOffset(1.3)
myStyle.SetTitleYOffset(1.7)
myStyle.SetPadLeftMargin(0.19)
myStyle.SetPadBottomMargin(0.13)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()

#pool = mp.Pool(processes=18)  

########################################
# Configuration
########################################

DRAW_ROC = True

all_setups = []

for pair_name, pair in pairs.iteritems():
    sample_sig = pair[0]
    sample_bkg = pair[1]

    basepath = '/scratch/gregor/'
    file_name_sig  = basepath + files[sample_sig] + "-weighted.root"
    file_name_bkg  = basepath + files[sample_bkg] + "-weighted.root"

    li_methods      = ["Cuts"]

    fj_size = ranges[pair[0]][4]
    if fj_size=="ca15":
        other_fj_size="ca08"
    else:
        other_fj_size="ca15"
    
    
    combined_setups = []

        
#    combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_combined"),
#                                     "SD(z=0.1, #beta=0), #tau_{3}/#tau_{2}",
#                                    [["Cuts", "V:FitMethod=MC:SampleSize=500000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                                    [variable.di['{0}softdropz10b00_mass'.format(fj_size)],
#                                     variable.di['{0}_tau3/{0}_tau2'.format(fj_size)]],
#                                    [],
#                                    file_name_sig,
#                                    file_name_bkg,
#                                    fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                    fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                    weight_sig = "weight",
#                                    weight_bkg = "weight",
#                                    draw_roc = DRAW_ROC,
#                                    working_points = [{"file_name" : "zprime_m2000_qcd_800_1000_softdropz10b00_combined_Cuts",
#                                                       "eff" : 0.2,
#                                                       "name" : "20%"},
#                                                      {"file_name" : "zprime_m2000_qcd_800_1000_softdropz10b00_combined_Cuts",
#                                                       "eff" : 0.4,
#                                                       "name" : "40%"},
#                                                      {"file_name" : "zprime_m2000_qcd_800_1000_softdropz10b00_combined_Cuts",
#                                                       "eff" : 0.6,
#                                                       "name" : "60%"}]))
#
#
#
#    combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_combined_btag"),
#                                     "SD(z=0.1, #beta=0), #tau_{3}/#tau_{2}, btag",
#                                     [["Cuts", "V:FitMethod=MC:SampleSize=1000000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart:CutRangeMin[2]=0:CutRangeMax[2]=1:VarProp[2]=FSmart"]], 
#                                    [variable.di['{0}softdropz10b00_mass'.format(fj_size)],
#                                     variable.di['{0}_tau3/{0}_tau2'.format(fj_size)],
#                                     variable.di['{0}trimmedr2f6forbtag_btag'.format(fj_size)],                                     
#                                 ],
#                                    [],
#                                    file_name_sig,
#                                    file_name_bkg,
#                                    fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                    fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                    weight_sig = "weight",
#                                    weight_bkg = "weight",
#                                    draw_roc = DRAW_ROC,
#                                    working_points = []))
#
#
    if pair_name in ["pt-300-to-470", "pt-200-to-300"]:
#
#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "HTT_mass_frec_DeltaRopt"),
#                                 "HTT V2 - m, fRec, #DeltaR",
#                                 [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=2000000:VarProp[1]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=250"]], 
#                                 [variable.di['looseOptRHTT_mass'],
#                                  variable.di['looseOptRHTT_fRec'],
#                                  variable.di['looseOptRHTT_Ropt-looseOptRHTT_RoptCalc']],                               
#                                 [],
#                                 file_name_sig,
#                                 file_name_bkg,
#                                 fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                 fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                 weight_sig = "weight",
#                                 weight_bkg = "weight",
#                                 draw_roc = DRAW_ROC,
#                             ))
#
#        
        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "HTT_mass_frec_tau"),
                                "HTT V2 - m, fRec, #tau_{3}/#tau_{2}",
                                         [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=2000000:VarProp[1]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=250:CutRangeMin[2]=0:CutRangeMax[2]=1:VarProp[2]=FSmart"]], 
                                [variable.di['looseOptRHTT_mass'],
                                 variable.di['looseOptRHTT_fRec'],
                                 variable.di['{0}_tau3/{0}_tau2'.format(fj_size)],
                             ],                               
                                [],
                                file_name_sig,
                                file_name_bkg,
                                fiducial_cut_sig = fiducial_cuts[sample_sig],
                                fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                                weight_sig = "weight",
                                weight_bkg = "weight",
                                draw_roc = DRAW_ROC,
                                working_points = [{"file_name" : "zprime_m1000_qcd_300_470_HTT_mass_frec_tau_Cuts",
                                                                    "eff" : 0.2,
                                                                    "name" : "20% - with HTT"},
                                                                   {"file_name" : "zprime_m1000_qcd_300_470_HTT_mass_frec_tau_Cuts",
                                                                    "eff" : 0.4,
                                                                    "name" : "40% - with HTT"},
                                                                   {"file_name" : "zprime_m1000_qcd_300_470_HTT_mass_frec_tau_Cuts",
                                                                    "eff" : 0.6,
                                                                    "name" : "60% - with HTT"}]))
        
        
#
#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "HTT_mass_frec_tau_btag"),
#                                "HTT V2 - m, fRec, #tau_{3}/#tau_{2}, btag",
#                                         [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=3000000:VarProp[1]=FSmart:CutRangeMin[0]=0:CutRangeMax[0]=250:CutRangeMin[2]=0:CutRangeMax[2]=1:VarProp[2]=FSmart:CutRangeMin[3]=0:CutRangeMax[3]=1:VarProp[3]=FSmart"]], 
#                                [variable.di['looseOptRHTT_mass'],
#                                 variable.di['looseOptRHTT_fRec'],
#                                 variable.di['{0}_tau3/{0}_tau2'.format(fj_size)],
#                                 variable.di['{0}trimmedr2f6forbtag_btag'.format(fj_size)],
#                             ],                               
#                                [],
#                                file_name_sig,
#                                file_name_bkg,
#                                fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                weight_sig = "weight",
#                                weight_bkg = "weight",
#                                draw_roc = DRAW_ROC,
#                            ))
#
        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz15b10_combined"),
                                         "SD(z=0.15, #beta=1), #tau_{3}/#tau_{2}",
                                         [["Cuts", "V:FitMethod=MC:SampleSize=500000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
                                         [variable.di['{0}softdropz15b10_mass'.format(fj_size)],
                                          variable.di['{0}_tau3/{0}_tau2'.format(fj_size)]],
                                         [],
                                         file_name_sig,
                                         file_name_bkg,
                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
                                         weight_sig = "weight",
                                         weight_bkg = "weight",
                                         draw_roc = DRAW_ROC,
                                         working_points = [{"file_name" : "zprime_m1000_qcd_300_470_softdropz15b10_combined_Cuts",
                                                                             "eff" : 0.2,
                                                                             "name" : "20%"},
                                                                            {"file_name" : "zprime_m1000_qcd_300_470_softdropz15b10_combined_Cuts",
                                                                             "eff" : 0.4,
                                                                             "name" : "40%"},
                                                                            {"file_name" : "zprime_m1000_qcd_300_470_softdropz15b10_combined_Cuts",
                                                                             "eff" : 0.6,
                                                                             "name" : "60%"}]))


#
#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz15b10_combined_btag"),
#                                         "SD(z=0.15, #beta=1), #tau_{3}/#tau_{2}, btag",
#                                         [["Cuts", "V:FitMethod=MC:SampleSize=800000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart:CutRangeMin[2]=0:CutRangeMax[2]=1:VarProp[2]=FSmart"]], 
#                                         [variable.di['{0}softdropz15b10_mass'.format(fj_size)],
#                                          variable.di['{0}_tau3/{0}_tau2'.format(fj_size)],
#                                          variable.di['{0}trimmedr2f6forbtag_btag'.format(fj_size)],
#                                      ],
#                                         [],
#                                         file_name_sig,
#                                         file_name_bkg,
#                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                         weight_sig = "weight",
#                                         weight_bkg = "weight",
#                                         draw_roc = DRAW_ROC,
#                                         working_points = []))
#


#    if pair_name in ["pt-800-to-1000", "pt-600-to-800"]:

#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "showerdeconstruction"),
#                             "Shower Deconstruction",
#                             [["Cuts", "FitMethod=MC:SampleSize=90000"]], 
#                             [variable.di['log({0}_chi)'.format(fj_size)]],
#                             [variable.di['log({0}_chi)'.format(other_fj_size)]],
#                             file_name_sig,
#                             file_name_bkg,
#                             fiducial_cut_sig = fiducial_cuts[sample_sig],
#                             fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                             weight_sig = "weight",
#                             weight_bkg = "weight",
#                             draw_roc = DRAW_ROC))
#
#
#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "CMSTT_mtop_mmin"),
#                                         "m(min), m(top)",
#                                         [["Cuts", "FitMethod=MC:Sigma=0.3:SampleSize=1200000:CutRangeMin[0]=0:CutRangeMax[0]=401:CutRangeMin[1]=0:CutRangeMax[1]=150"]], 
#                                         [variable.di['{0}cmstt_topMass'.format(fj_size)],
#                                          variable.di['{0}cmstt_minMass'.format(fj_size)]], 
#                                         [], 
#                                         file_name_sig,
#                                         file_name_bkg,
#                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                         weight_sig = "weight",
#                                         weight_bkg = "weight",
#                                         draw_roc = DRAW_ROC))
#
#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_tau3tau2_CMSTT_mmin"),
#                                         "SD(z=0.1, #beta=0), #tau_{3}/#tau_{2}, m(min)",
#                                         [["Cuts", "V:FitMethod=MC:SampleSize=1200000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1::CutRangeMin[2]=0:CutRangeMax[2]=150:VarProp[1]=FSmart"]], 
#                                         [
#                                          variable.di['{0}softdropz10b00_mass'.format(fj_size)],
#                                          variable.di['{0}_tau3/{0}_tau2'.format(fj_size)],
#                                          variable.di['{0}cmstt_minMass'.format(fj_size)],],
#                                         [], 
#                                         file_name_sig,
#                                         file_name_bkg,
#                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                         weight_sig = "weight",
#                                         weight_bkg = "weight",
#                                         draw_roc = DRAW_ROC
#                                     ))
#
#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_tau3tau2_CMSTT_mmin_mtop"),
#                                         "SD(z=0.1, #beta=0), #tau_{3}/#tau_{2}, m(min), m(top)",
#                                         [["Cuts", "V:FitMethod=MC:SampleSize=4000000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:CutRangeMin[2]=0:CutRangeMax[2]=150:VarProp[1]=FSmart"]], 
#                                         [
#                                          variable.di['{0}softdropz10b00_mass'.format(fj_size)],
#                                          variable.di['{0}_tau3/{0}_tau2'.format(fj_size)],
#                                          variable.di['{0}cmstt_minMass'.format(fj_size)],
#                                          variable.di['{0}cmstt_topMass'.format(fj_size)]],
#                                         [], 
#                                         file_name_sig,
#                                         file_name_bkg,
#                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                         weight_sig = "weight",
#                                         weight_bkg = "weight",
#                                         draw_roc = DRAW_ROC))
#
#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_combined_CMSTTWP_both"),
#                                         "SD(z=0.1, #beta=0), #tau_{3}/#tau_{2}, fix m(min) and m(top)",
#                                         [["Cuts", "V:FitMethod=MC:SampleSize=2000000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                                         [variable.di['{0}softdropz10b00_mass'.format(fj_size)],
#                                          variable.di['{0}_tau3/{0}_tau2'.format(fj_size)]],
#                                         [],
#                                         file_name_sig,
#                                         file_name_bkg,
#                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                         extra_cut = "(({0}cmstt_nSubJets>=3)&&({0}cmstt_topMass>140)&&({0}cmstt_topMass<250)&&({0}cmstt_minMass>50))".format(fj_size),
#                                         weight_sig = "weight",
#                                         weight_bkg = "weight",
#                                         draw_roc = DRAW_ROC,
#                                         ))
#
#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_combined_CMSTTWP_one"),
#                                         "SD(z=0.1, #beta=0), #tau_{3}/#tau_{2}, fix m(min)",
#                                         [["Cuts", "V:FitMethod=MC:SampleSize=2000000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart"]], 
#                                         [variable.di['{0}softdropz10b00_mass'.format(fj_size)],
#                                          variable.di['{0}_tau3/{0}_tau2'.format(fj_size)]],
#                                         [],
#                                         file_name_sig,
#                                         file_name_bkg,
#                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                         extra_cut = "(({0}cmstt_nSubJets>=3)&&({0}cmstt_minMass>50))".format(fj_size),
#                                         weight_sig = "weight",
#                                         weight_bkg = "weight",
#                                         draw_roc = DRAW_ROC,                            
#                                        working_points = [{"file_name" : "zprime_m2000_qcd_800_1000_softdropz10b00_combined_CMSTTWP_one_Cuts",
#                                                           "eff" : 0.2,
#                                                           "name" : "20% - with CMSTT"},
#                                                          {"file_name" : "zprime_m2000_qcd_800_1000_softdropz10b00_combined_CMSTTWP_one_Cuts",
#                                                           "eff" : 0.4,
#                                                           "name" : "40% - with CMSTT"},
#                                                          {"file_name" : "zprime_m2000_qcd_800_1000_softdropz10b00_combined_CMSTTWP_one_Cuts",
#                                                           "eff" : 0.6,
#                                                          "name" : "60% - with CMSTT"}]))
#          
#
#        combined_setups.append(TMVASetup("{0}_{1}_{2}".format(sample_sig, sample_bkg, "softdropz10b00_combined_CMSTTWP_one_btag"),
#                                         "SD(z=0.1, #beta=0), #tau_{3}/#tau_{2}, fix m(min), btag",
#                                         [["Cuts", "V:FitMethod=MC:SampleSize=3000000:Sigma=0.3:CutRangeMin[0]=0:CutRangeMax[0]=301:CutRangeMin[1]=0:CutRangeMax[1]=1:VarProp[1]=FSmart:CutRangeMin[2]=0:CutRangeMax[2]=1:VarProp[2]=FSmart"]], 
#                                         [variable.di['{0}softdropz10b00_mass'.format(fj_size)],
#                                          variable.di['{0}_tau3/{0}_tau2'.format(fj_size)],
#                                          variable.di['{0}trimmedr2f6forbtag_btag'.format(fj_size)],
#                                      ],
#                                         [],
#                                         file_name_sig,
#                                         file_name_bkg,
#                                         fiducial_cut_sig = fiducial_cuts[sample_sig],
#                                         fiducial_cut_bkg  = fiducial_cuts[sample_bkg],
#                                         extra_cut = "(({0}cmstt_nSubJets>=3)&&({0}cmstt_minMass>50))".format(fj_size),
#                                         weight_sig = "weight",
#                                         weight_bkg = "weight",
#                                         draw_roc = DRAW_ROC))                                     
#

    


  

    plotROCs("WP_ROC_" + pair_name, combined_setups, extra_text = pretty_fiducial_cuts[sample_sig])        
    all_setups += combined_setups

#pool.map(doTMVA, all_setups)





