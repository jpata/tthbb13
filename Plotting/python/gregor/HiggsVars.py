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

basepath = ' ../../../TTHNtupleAnalyzer/test/'

filename_tth    = "output-tth"
filename_ttbar  = "output-ttbar"

dic_files = {}
dic_files["tth"]      = [filename_tth,  'tthNtupleAnalyzer/events'  ]
dic_files["ttbar"]    = [filename_ttbar,'tthNtupleAnalyzer/events'  ]

# for the filename: basepath + filename + .root
for k,v in dic_files.iteritems():
    # only a filename
    if isinstance( v, str ):
        dic_files[k] = basepath+v+".root"
    # filename and treename
    else:
        dic_files[k] = ( basepath+v[0]+".root", v[1] )
# end of adding paths to the filenames

output_dir = "results/HiggsVars/"


########################################
# Define the plots
########################################

jet_collections_15 = ['fat', 
                      'fatMDT', 
                      'fatMDTFiltered']

combinedPlot ("mass",
              [plot( jc + "(ttH)", 
                     'jet_{0}__mass'.format(jc), 
                     '(jet_{0}__close_higgs_dr < 1.2)&&(jet_{0}__close_higgs_pt > 120)'.format(jc),
                     "tth") for jc in jet_collections_15] + 
              [plot( jc + "(ttbar)", 
                     'jet_{0}__mass'.format(jc), 
                     '(1)',
                     "ttbar") for jc in jet_collections_15],
              20, 0, 600, 0.7,
              label_x   = "Fatjet mass",
              label_y   = "Jets",
              axis_unit = "GeV",
              log_y     = False,
              normalize = True,
              legend_origin_x = 0.6,
              legend_origin_y = 0.7,
              legend_size_x   = 0.2,
              legend_size_y   = 2 * 0.05 * len(jet_collections_15))

doWork( dic_files, output_dir )
