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

filename_tth   = "output"

dic_files = {}
dic_files["tth"]      = [filename_tth, 'tthNtupleAnalyzer/events'  ]


# for the filename: basepath + filename + .root
for k,v in dic_files.iteritems():
    # only a filename
    if isinstance( v, str ):
        dic_files[k] = basepath+v+".root"
    # filename and treename
    else:
        dic_files[k] = ( basepath+v[0]+".root", v[1] )
# end of adding paths to the filenames

output_dir = "TopVars/"


########################################
# Define the plots
########################################

jet_collections_15 = ['ca15', 
                      'ca15filtered', 
                      'ca15pruned', 
                      'ca15trimmed']

combinedPlot ("pt",
              [plot( jc, 'jet_{0}__pt'.format(jc), '(1)', "tth") for jc in jet_collections_15],
              80, 0, 2000, 4e5,
              label_x   = "Fatjet p_{T}",
              label_y   = "Jets",
              axis_unit = "GeV",
              log_y     = True,
              normalize = False,
              legend_origin_x = 0.6,
              legend_origin_y = 0.7,
              legend_size_x   = 0.2,
              legend_size_y   = 0.05 * len(jet_collections_15))

combinedPlot ("mass",
              [plot( jc, 'jet_{0}__mass'.format(jc), '(1)', "tth") for jc in jet_collections_15],
              60, 0, 1200, 3e5,
              label_x   = "Fatjet mass",
              label_y   = "Jets",
              axis_unit = "GeV",
              log_y     = True,
              normalize = False,
              legend_origin_x = 0.6,
              legend_origin_y = 0.7,
              legend_size_x   = 0.2,
              legend_size_y   = 0.05 * len(jet_collections_15))

for nsub in [1,2,3]:
    combinedPlot ("tau_{0}".format(nsub),
                  [plot( jc, 'jet_{0}__tau{1}'.format(jc, nsub), '(1)', "tth") for jc in jet_collections_15],
                  50, 0, 1, 1e5,
                  label_x   = "#tau_{{0}}".format(nsub),
                  label_y   = "Jets",
                  axis_unit = "GeV",
                  log_y     = False,
                  normalize = False,
                  legend_origin_x = 0.6,
                  legend_origin_y = 0.7,
                  legend_size_x   = 0.2,
                  legend_size_y   = 0.05 * len(jet_collections_15))


doWork( dic_files, output_dir )
