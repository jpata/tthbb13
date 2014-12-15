#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

from TTH.Plotting.Helpers.Plot2DHelpers import *


########################################
# Define Input Files and
# output directory
########################################

basepath = '/scratch/gregor/'

files = {}
files["ntop_v8_zprime_m2000_1p_13tev-tagging"       ] = "ntop_v8_zprime_m2000_1p_13tev-tagging"
                                         
# for the filename: basepath + filename + .root
for k,v in files.iteritems():
    # only a filename
    if isinstance( v, str ):
        files[k] = basepath+v+".root"
    # filename and treename
    else:
        files[k] = ( basepath+v[0]+".root", v[1] )
# end of adding paths to the filenames


plots = []
plots.append( plot( 
    "name", 
    'ca15_mass', 
    'ca15trimmed_mass', 
    '(1)', 
    "ntop_v8_zprime_m2000_1p_13tev-tagging",
    50, 0, 800,
    50, 0, 800))
    

MakePlots(files, plots )
