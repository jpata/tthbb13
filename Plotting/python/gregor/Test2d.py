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
files["qcd_800_1000"] = "ntop_v8_qcd_800_1000_pythia8_13tev-tagging"
files["zprime_m2000_1p"] = "ntop_v8_zprime_m2000_1p_13tev-tagging"
                                        
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

for sample in files.keys(): 


    plots.append( plot( 
        "ca15_tau32_vs_ca15_trimmed_tau32_{0}".format(sample), 
        'ca15_tau3/ca15_tau2', 
        'ca15trimmed_tau3/ca15trimmed_tau2', 
        '(1)', 
        sample, 
        60, 0, 1.2,
        60, 0, 1.2,
        label_x = "CA (R=1.5) #tau_{3}/#tau_{2}",
        label_y = "CA (R=1.5) trimmed #tau_{3}/#tau_{2}",
    ))



    if False:
        plots.append( plot( 
            "ca15_mass_vs_ca08_mass_{0}".format(sample), 
            'ca15_mass', 
            'ca08_mass', 
            '(1)', 
            sample, 
            50, 0, 800,
            50, 0, 800,
            label_x = "CA (R=1.5) mass [GeV]",
            label_y = "CA (R=0.8) mass [GeV]",
        ))


        plots.append( plot( 
            "ca15_mass_vs_ca15_trimmed_mass_{0}".format(sample), 
            'ca15_mass', 
            'ca15trimmed_mass', 
            '(1)', 
            sample, 
            50, 0, 800,
            50, 0, 800,
            label_x = "CA (R=1.5) mass [GeV]",
            label_y = "CA (R=1.5) trimmed mass [GeV]",
        ))
   

MakePlots(files, plots )
