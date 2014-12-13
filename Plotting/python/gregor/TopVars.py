#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

from TTH.Plotting.Helpers.CompareDistributionsHelpers import *


########################################
# Define Input Files and
# output directory
########################################

basepath = '/scratch/gregor/'

files = {}
files["ntop_v3_qcd_120_170_pythia6_13tev"   ]      = ["ntop_v3_qcd_120_170_pythia6_13tev"   , 'tthNtupleAnalyzer/events'  ] 
files["ntop_v3_qcd_170_300_pythia6_13tev"   ]      = ["ntop_v3_qcd_170_300_pythia6_13tev"   , 'tthNtupleAnalyzer/events'  ]
files["ntop_v3_qcd_300_470_pythia6_13tev"   ]      = ["ntop_v3_qcd_300_470_pythia6_13tev"   , 'tthNtupleAnalyzer/events'  ]
files["ntop_v3_qcd_470_600_pythia6_13tev"   ]      = ["ntop_v3_qcd_470_600_pythia6_13tev"   , 'tthNtupleAnalyzer/events'  ]
files["ntop_v3_qcd_800_1000_pythia6_13tev"  ]      = ["ntop_v3_qcd_800_1000_pythia6_13tev"  , 'tthNtupleAnalyzer/events'  ]
files["ntop_v3_qcd_1000_1400_pythia6_13tev" ]      = ["ntop_v3_qcd_1000_1400_pythia6_13tev" , 'tthNtupleAnalyzer/events'  ]
files["ntop_v3_qcd_1400_1800_pythia6_13tev" ]      = ["ntop_v3_qcd_1400_1800_pythia6_13tev" , 'tthNtupleAnalyzer/events'  ]
files["ntop_v3_qcd_1800_inf_pythia6_13tev"  ]      = ["ntop_v3_qcd_1800_inf_pythia6_13tev"  , 'tthNtupleAnalyzer/events'  ]
files["ntop_v3_zprime_m1250_1p_13tev"       ]      = ["ntop_v3_zprime_m1250_1p_13tev"       , 'tthNtupleAnalyzer/events'  ]
files["ntop_v3_zprime_m1500_1p_13tev"       ]      = ["ntop_v3_zprime_m1500_1p_13tev"       , 'tthNtupleAnalyzer/events'  ]
files["ntop_v3_zprime_m2000_1p_13tev"       ]      = ["ntop_v3_zprime_m2000_1p_13tev"       , 'tthNtupleAnalyzer/events'  ]
files["ntop_v3_zprime_m4000_1p_13tev"       ]      = ["ntop_v3_zprime_m4000_1p_13tev"       , 'tthNtupleAnalyzer/events'  ]
                                         

# for the filename: basepath + filename + .root
for k,v in files.iteritems():
    # only a filename
    if isinstance( v, str ):
        files[k] = basepath+v+".root"
    # filename and treename
    else:
        files[k] = ( basepath+v[0]+".root", v[1] )
# end of adding paths to the filenames

output_dir = "results/TopVars/"


########################################
# Define the plots
########################################

zprimes = {"Z'(1.25 TeV)" : "ntop_v3_zprime_m1250_1p_13tev",
           "Z'(1.5 TeV)"  : "ntop_v3_zprime_m1500_1p_13tev",
           "Z'(2.0 TeV)"  : "ntop_v3_zprime_m2000_1p_13tev",
           "Z'(4.0 TeV)"  : "ntop_v3_zprime_m4000_1p_13tev",
           }

qcd = {"QCD(120-170 GeV)" :   "ntop_v3_qcd_120_170_pythia6_13tev",
       "QCD(170-300 GeV)" :   "ntop_v3_qcd_170_300_pythia6_13tev",   
       "QCD(300-470 GeV)" :   "ntop_v3_qcd_300_470_pythia6_13tev",   
       "QCD(470-600 GeV)" :   "ntop_v3_qcd_470_600_pythia6_13tev",   
       "QCD(800-1000 GeV)" :   "ntop_v3_qcd_800_1000_pythia6_13tev",  
       "QCD(1000-1400 GeV)" :   "ntop_v3_qcd_1000_1400_pythia6_13tev", 
       "QCD(1400-1800 GeV)" :   "ntop_v3_qcd_1400_1800_pythia6_13tev", 
       "QCD(1800-.. GeV)" :   "ntop_v3_qcd_1800_inf_pythia6_13tev",  }

qcd_sorted = sorted(qcd, key = lambda x: int(x.split("-")[0].replace("QCD(","")))

jet_names = {'jet_ca08':"", 
             'jet_ca08filtered':"Filtered", 
             'jet_ca08pruned':"Pruned",  
             'jet_ca08trimmed':"Trimmed", 
             'jet_ca08cmstt':"CMSTT",
             'jet_ca15':"", 
             'jet_ca15filtered':"Filtered", 
             'jet_ca15pruned':"Pruned",  
             'jet_ca15trimmed':"Trimmed", 
             'jet_ca15cmstt':"CMSTT",             
             "jet_looseMultiRHTT" : "HTT",}

jet_collections_ca15 = ['jet_ca15', 
                      'jet_ca15filtered', 
                      'jet_ca15pruned', 
                      'jet_ca15trimmed']



if False:

    # Distance parton/top to fatjet
    combinedPlot ("dr_truth",
                  [plot( "Z', CA R=0.8", 'jet_ca08__close_hadtop_dr', '(1)',  "ntop_v3_zprime_m2000_1p_13tev"),
                   plot( "Z', CA R=1.5", 'jet_ca15__close_hadtop_dr', '(1)',  "ntop_v3_zprime_m2000_1p_13tev"),
                   plot( "QCD, CA R=0.8", 'jet_ca08__close_parton_dr', '(1)', "ntop_v3_qcd_800_1000_pythia6_13tev"),
                   plot( "QCD, CA R=1.5", 'jet_ca15__close_parton_dr', '(1)', "ntop_v3_qcd_800_1000_pythia6_13tev")],
                  80, 0, 6., 
                  label_x   = "#Delta R(fj, truth)",
                  label_y   = "Jets",
                  axis_unit = "GeV",
                  log_y     = True,
                  normalize = True,
                  legend_origin_x = 0.6,
                  legend_origin_y = 0.6,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * 4)


    # True top pT
    combinedPlot ("true_top_pt",
                  [plot( name, 'max(gen_t__pt,gen_tbar__pt)', '(1)', zprimes[name]) for name in sorted(zprimes)],
                  80, 0, 2500, 4e5,
                  label_x   = "Leading True top p_{T}",
                  label_y   = "Events",
                  axis_unit = "GeV",
                  log_y     = True,
                  normalize = False,
                  legend_origin_x = 0.2,
                  legend_origin_y = 0.3,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * len(zprimes))


    # Fatjet pT (CA, R=1.5), Z'
    combinedPlot ("signal_ca15_pt",
                  [plot( name, 'jet_ca15__pt', '(1)', zprimes[name]) for name in sorted(zprimes)],
                  80, 0, 2500, 
                  label_x   = "CA (R=1.5) Fat jet p_{T}",
                  label_y   = "Jets",
                  axis_unit = "GeV",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.6,
                  legend_origin_y = 0.6,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * len(zprimes))


    # Fatjet pT (CA, R=0.8), Z'
    combinedPlot ("signal_ca08_pt",
                  [plot( name, 'jet_ca08__pt', '(1)', zprimes[name]) for name in sorted(zprimes)],
                  80, 0, 2500, 
                  label_x   = "CA (R=0.8) Fat jet p_{T}",
                  label_y   = "Jets",
                  axis_unit = "GeV",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.6,
                  legend_origin_y = 0.6,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * len(zprimes))


    # Fatjet pT (CA, R=1.5), QCD
    combinedPlot ("bg_ca15_pt",
                  [plot( name, 'jet_ca15__pt', '(1)', qcd[name]) for name in qcd_sorted],
                  80, 0, 2500, 
                  label_x   = "CA (R=1.5) Fat jet p_{T}",
                  label_y   = "Jets",
                  axis_unit = "GeV",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.45,
                  legend_origin_y = 0.4,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * len(qcd))


    # Fatjet pT (CA, R=0.8), QCD
    combinedPlot ("bg_ca08_pt",
                  [plot( name, 'jet_ca08__pt', '(1)', qcd[name]) for name in qcd_sorted],
                  80, 0, 2500, 
                  label_x   = "CA (R=1.5) Fat jet p_{T}",
                  label_y   = "Jets",
                  axis_unit = "GeV",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.45,
                  legend_origin_y = 0.4,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * len(qcd))


    # Comparison of Groomed Masses
    combinedPlot ("ca15_groomed_masses",
                  [plot( "Z' " +jet_names[jc], 
                         "{0}__mass".format(jc), 
                         '({0}__close_hadtop_dr<1.2)'.format(jc), 
                         "ntop_v3_zprime_m2000_1p_13tev") for jc in jet_collections_ca15] + 
                  [plot( "QCD " + jet_names[jc], 
                         "{0}__mass".format(jc), 
                         '({0}__close_parton_dr<1.2)'.format(jc), 
                         "ntop_v3_qcd_800_1000_pythia6_13tev") for jc in jet_collections_ca15],
                  80, 0, 1000, 
                  label_x   = "CA (R=1.5) Fat jet mass",
                  label_y   = "Jets",
                  axis_unit = "GeV",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.5,
                  legend_origin_y = 0.4,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * len(qcd))


    # N-Subjettiness for CA R=1.5
    combinedPlot ("ca15_tau32",
                  [plot( "Z' " +jet_names[jc], 
                         "{0}__tau3/{0}__tau2".format(jc), 
                         '({0}__close_hadtop_dr<1.2)'.format(jc), 
                         "ntop_v3_zprime_m2000_1p_13tev") for jc in ['jet_ca15','jet_ca15trimmed']] + 
                  [plot( "QCD " + jet_names[jc], 
                         "{0}__tau3/{0}__tau2".format(jc), 
                         '({0}__close_parton_dr<1.2)'.format(jc), 
                         "ntop_v3_qcd_800_1000_pythia6_13tev") for jc in ['jet_ca15','jet_ca15trimmed']],
                  50, 0, 1, 
                  label_x   = "CA (R=1.5) #tau_{3}/#tau_{2}",
                  label_y   = "Jets",
                  axis_unit = "",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.2,
                  legend_origin_y = 0.4,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * 4)


    # N-Subjettiness for CA R=0.8
    combinedPlot ("ca08_tau32",
                  [plot( "Z' " +jet_names[jc], 
                         "{0}__tau3/{0}__tau2".format(jc), 
                         '({0}__close_hadtop_dr<0.6)'.format(jc), 
                         "ntop_v3_zprime_m2000_1p_13tev") for jc in ['jet_ca08','jet_ca08trimmed']] + 
                  [plot( "QCD " + jet_names[jc], 
                         "{0}__tau3/{0}__tau2".format(jc), 
                         '({0}__close_parton_dr<0.6)'.format(jc), 
                         "ntop_v3_qcd_800_1000_pythia6_13tev") for jc in ['jet_ca08','jet_ca08trimmed']],
                  50, 0, 1, 
                  label_x   = "CA (R=0.8) #tau_{3}/#tau_{2}",
                  label_y   = "Jets",
                  axis_unit = "",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.2,
                  legend_origin_y = 0.4,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * 4)


    # CMS TopTagger Top Mass
    jc = 'jet_ca15cmstt'
    combinedPlot ("ca15_cmstt_topMass",
                  [plot( "Z' " +jet_names[jc], 
                         "{0}__topMass".format(jc), 
                         '({0}__close_hadtop_dr<1.2)'.format(jc), 
                         "ntop_v3_zprime_m2000_1p_13tev"),
                  plot( "QCD " + jet_names[jc], 
                         "{0}__topMass".format(jc), 
                         '({0}__close_parton_dr<1.2)'.format(jc), 
                         "ntop_v3_qcd_800_1000_pythia6_13tev")],
                  80, 0, 1000, 
                  label_x   = "CMSTopTagger top Mass",
                  label_y   = "Jets",
                  axis_unit = "GeV",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.6,
                  legend_origin_y = 0.6,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * 4)


    # HEPTopTagger TopMass
    jc = 'jet_looseMultiRHTT'
    combinedPlot ("ca15_htt_mass",
                  [plot( "Z' " +jet_names[jc], 
                         "{0}__mass".format(jc), 
                         '({0}__close_hadtop_dr<1.2)'.format(jc), 
                         "ntop_v3_zprime_m2000_1p_13tev"),
                  plot( "QCD " + jet_names[jc], 
                         "{0}__mass".format(jc), 
                         '({0}__close_parton_dr<1.2)'.format(jc), 
                         "ntop_v3_qcd_800_1000_pythia6_13tev")],
                  80, 0, 300, 
                  label_x   = "HEPTopTagger top mass",
                  label_y   = "Jets",
                  axis_unit = "GeV",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.65,
                  legend_origin_y = 0.6,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * 2)

    
    # HEPTopTagger fW
    jc = 'jet_looseMultiRHTT'
    combinedPlot ("ca15_htt_fW",
                  [plot( "Z' " +jet_names[jc], 
                         "{0}__fW".format(jc), 
                         '({0}__close_hadtop_dr<1.2)'.format(jc), 
                         "ntop_v3_zprime_m2000_1p_13tev"),
                  plot( "QCD " + jet_names[jc], 
                         "{0}__fW".format(jc), 
                         '({0}__close_parton_dr<1.2)'.format(jc), 
                         "ntop_v3_qcd_800_1000_pythia6_13tev")],
                  80, 0, 0.8, 
                  label_x   = "HEPTopTagger f_{W}",
                  label_y   = "Jets",
                  axis_unit = "",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.6,
                  legend_origin_y = 0.6,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * 2)


    # HEPTopTagger Delta Rmin
    jc = 'jet_looseMultiRHTT'
    combinedPlot ("ca15_htt_DRmin",
                  [plot( "Z' " +jet_names[jc], 
                         "{0}__Rmin-{0}__RminExpected".format(jc), 
                         '({0}__close_hadtop_dr<1.2)'.format(jc), 
                         "ntop_v3_zprime_m2000_1p_13tev"),
                  plot( "QCD " + jet_names[jc], 
                         "{0}__Rmin-{0}__RminExpected".format(jc), 
                         '({0}__close_parton_dr<1.2)'.format(jc), 
                         "ntop_v3_qcd_800_1000_pythia6_13tev")],
                  21, -1, 1, 
                  label_x   = "HEPTopTagger #Delta R_{min}",
                  label_y   = "Jets",
                  axis_unit = "",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.6,
                  legend_origin_y = 0.6,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * 2)



                    
doWork(files, output_dir )
