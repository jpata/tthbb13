#!/usr/bin/env python
"""
Thomas:

This is TFmain.py. This program runs the full chain of creating a matrix of transfer functions from a customized .root file. To create the customized .root file, see 'outputtree.py'

"""

########################################
# Imports
########################################

import pickle
import time
import datetime
import shutil
import os

from config import Make_config
from make_histograms import Make_Histograms
from fit_single_bins import Fit_Single_Bins
from fit_across_bins import Fit_Across_Bins
from draw_hists_and_fits import Draw_Hists_and_Fits

########################################
# Main
########################################

def main():

    print 'This is TFfitting.py. This program only performs the fitting of histograms but does not produce the histograms. It runs fit_single_bins.py, fit_across_bins.py and draw_hists_and_fits.py. For the full chain, see TFmain.py\n'

    Make_config()

    pickle_f = open( 'config.dat', 'rb' )
    config = pickle.load( pickle_f )
    pickle_f.close()


    if os.path.isfile( '{0}/TFMatrix.dat'.format( config['outputdir'] ) ):
        os.remove( '{0}/TFMatrix.dat'.format( config['outputdir'] ) )

    # Fitting the single bins
    Fit_Single_Bins()

    # Fit across the Pt-bins
    Fit_Across_Bins()

    # Fitting the single bins again, taking TFMatrix.dat as initialization
    #Fit_Single_Bins()

    # Fit across the Pt-bins again
    #Fit_Across_Bins()

    # Drawing the single bin histograms and the ABF results
    Draw_Hists_and_Fits()


########################################
# End of Main
########################################
if __name__ == "__main__":
  main()
