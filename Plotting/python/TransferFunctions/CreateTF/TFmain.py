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

from config import Make_config
from make_histograms import Make_Histograms
from fit_single_bins import Fit_Single_Bins
from fit_across_bins import Fit_Across_Bins
from draw_hists_and_fits import Draw_Hists_and_Fits

import TTH.MEAnalysis.samples as samples

########################################
# Main
########################################

def main(conffile):

    print 'This is TFmain.py. This program runs the full chain of creating a matrix of transfer functions from a customized .root file. To create the customized .root file, see \'outputtree.py\'\n'

    Make_Histograms(conffile)
    Fit_Single_Bins(conffile)
    Fit_Across_Bins(conffile)
    Draw_Hists_and_Fits(conffile)
    
    pickle_f = open( conffile, 'rb' )
    config = pickle.load( pickle_f )
    pickle_f.close()

    print config['info']

    ts = time.time()
    config['enddate'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    print ' Analysis end time:              {0}\n'.format( config['enddate'] )


########################################
# End of Main
########################################
if __name__ == "__main__":
    for s in ["resolved"]:
        main("configs/{1}/config.dat".format(samples.version, s))
