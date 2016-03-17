#!/usr/bin/env python
"""
Thomas:

This is TFfitting.py. This program only performs the fitting of histograms but does not produce the histograms. It runs fit_single_bins.py, fit_across_bins.py and draw_hists_and_fits.py. For the full chain, see TFmain.py

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

def main(conffile):

    print 'This is TFfitting.py. This program only performs the fitting of histograms but does not produce the histograms. It runs fit_single_bins.py, fit_across_bins.py and draw_hists_and_fits.py. For the full chain, see TFmain.py\n'

    pickle_f = open( conffile, 'rb' )
    config = pickle.load( pickle_f )
    pickle_f.close()


    if os.path.isfile( '{0}/TFMatrix.dat'.format( config['outputdir'] ) ):
        os.remove( '{0}/TFMatrix.dat'.format( config['outputdir'] ) )

    # Fitting the single bins
    Fit_Single_Bins()

    # Fit across the Pt-bins
    Fit_Across_Bins()

    # Drawing the single bin histograms and the ABF results
    Draw_Hists_and_Fits()


########################################
# End of Main
########################################
if __name__ == "__main__":
  main()
