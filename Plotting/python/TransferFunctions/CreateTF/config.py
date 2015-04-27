#!/usr/bin/env python
"""
Thomas:

This program creates config.dat, which contains a dictionary of all relevant input
and parameters.

The programs readtree.py and fit_across_bins.py will also write parameters to
config.dat.

"""

########################################
# Imports
########################################

import pickle
import os
import shutil
import copy
from TFClasses import function

import time
import datetime

########################################
# Main
########################################

def Make_config():

    config = {}

    ########################################
    # Information concerning this config file
    ########################################

    ts = time.time()
    config['date'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    config['info'] = '*** Information on this config.dat ***\n'\
    'This config file contains the input parameters (and some output parameters) used in the creation of TFMat.dat, the matrix of transfer functions. \n\n'\
    'Some html-overviews are produced in the output directory.\n'\
    '\n This config.dat was created on: {0}'.format(config['date'])

    ########################################
    # I/O information
    ########################################

    #config['input_root_file_name'] = '/scratch/tklijnsm/V11_full_subjets_0.3delR.root'
    #config['input_root_file_name'] = '/scratch/tklijnsm/V10_full_jets_TTBarH.root'
    #V11_full_jets_0.3delR.root

    config['input_root_file_name'] = '/scratch/tklijnsm/V11_full_jets_0.3delR.root'

    config['input_tree_name'] = 'tree'

    config['outputdir'] = 'V11_full_TTbar_0.3delR'

        
    config['SBF_fitted_hists_pickle_filename'] = \
        '{0}/SBF_fitted_hists_pickle.dat'.format( config['outputdir'] )

    config['SBF_hists_pickle_filename'] = \
        '{0}/SBF_hists_pickle.dat'.format( config['outputdir'] )

    ########################################
    # Program parameters
    ########################################

    # Use only a part of the root file
    config['Use_limited_entries'] = False

    # Specify the number of entries if only a limited number of entries is used
    #   This number is not used if Use_limited_entries is set to False
    config['n_entries_limited'] = 100000

    # Specify whether to make a TF from E_mc to E_reco, or Pt_mc to Pt_reco
    config['Use_Pt'] = True

    # Uses the Monte Carlo branches to retrieve data instead of the quark branches
    config['Use_mc_values'] = False

    # Specify whether the results of the ABF should be drawn in the single bin
    # histograms
    config['Draw_ABF_in_single_bins'] = True

    # Used for plotting purposes
    if config['Use_Pt']:
        config['E_or_Pt_str'] = 'Pt'
    else:
        config['E_or_Pt_str'] = 'E'


    ########################################
    # root file branch info
    ########################################
    
    # Branches for the reconstructed jet
    config['reco_E_str'] = 'Jet_E'
    config['reco_Pt_str'] = 'Jet_pt'
    config['reco_Eta_str'] = 'Jet_eta'
    config['reco_Phi_str'] = 'Jet_phi'

    # Branches to use if Use_mc_values == True
    config['mc_E_str'] = 'Jet_mcE'
    config['mc_Eta_str'] = 'Jet_mcEta'
    config['mc_Pt_str'] = 'Jet_mcPt'
    config['mc_Phi_str'] = 'Jet_mcPhi'
    config['mc_Flavour_str'] = 'Jet_mcFlavour'

    # Branches to use if Use_mc_values == False (i.e. use quark values)
    config['quark_E_str'] = 'Quark_E'
    config['quark_Eta_str'] = 'Quark_eta'
    config['quark_Pt_str'] = 'Quark_pt'
    config['quark_Phi_str'] = 'Quark_phi'
    config['quark_Flavour_str'] = 'Quark_pdgId'

    # Change branches if using Pt instead of E
    if config['Use_Pt']:
        config['reco_E_str'] = config['reco_Pt_str']
        config['mc_E_str'] = config['mc_Pt_str']
        config['quark_E_str'] = config['quark_Pt_str']    


    ########################################
    # Particles and binning
    ########################################

    # Set which particles will be used in the analysis.
    #   'b' = bottom, 'l' = light
    config['particles'] = [ 'b', 'l' ]
   
    # Set the eta axis
    #   Requires a minimum input of 2 (double) values.
    #   The first value is the left side of the first bin, the last value is the
    #   right side of the last bin.
    config['eta_axis'] = [ 0.0 , 1.0 , 2.5 ]

    # Set the number of energy bins
    #   The boundaries of the energy bins are determined by dividing all entries 
    #   inside the bounds into the set number of energy bins.
    config['n_E_bins'] = 58

    # Set the energy bounds. Quark/MC energies outside these bounds will not be
    # analyzed.
    config['E_bounds'] = [ 30.0, 300.0 ]


    ########################################
    # Standard functions
    #  - Define a standard single Gaussian
    #  - Define a standard double Gaussian
    #  - User has the option to use these standard functions, or create his own
    #    function object
    #  - Only the standard functions will have an analytic CDF
    ########################################

    #--------------------------------------#
    # Define a 'standard' single Gaussian

    # Define the mean and rms
    SG_mean = '[1]'
    SG_rms = '[2]'

    # Create the function object
    SG_func = function( "[0]*exp(-0.5*((x-({0}))/({1}))**2)".format(
        SG_mean, SG_rms ), [ "0", "mean", "rms" ] )

    # Tag it as a standard single Gaussian function, pass mean and rms
    setattr( SG_func, 'Is_SG', True )
    setattr( SG_func, 'SG_mean', SG_mean )
    setattr( SG_func, 'SG_rms', SG_rms )

    config['Standard_SG_func'] = SG_func

    #--------------------------------------#
    # Define a 'standard' double Gaussian

    # Define the means and rms'
    DG_mean = [ '[1]', '[3]' ]
    DG_rms = [ '[2]', '[2]+[4]' ]

    # Set relative weight of the two Gaussians
    config['DG_rel_weight'] = 0.90
    
    # Create the formula
    DG_formula = "[0]*({0}*exp(-0.5*((x-({1}))/({2}))**2)+(1-{0})*exp(-0.5*((x-({3}))/({4}))**2))".format(
        config['DG_rel_weight'],
        DG_mean[0],
        DG_rms[0],
        DG_mean[1],
        DG_rms[1] )

    # Optional: Specify limits for the parameters, if any are present.
    #   format: ( parameter number, lower bound, upper bound )
    DG_parlimits = [
        ( 1, 0.0, 2000.0 ),
        ( 2, 0.0 , 2000.0 ),
        ( 3, 0.0, 2000.0 ),
        ( 4, 0.0 , 2000.0 ) ]

    # Set proper initialization values
    #   ( high weight, high mean, low rms + low weight, low mean, high rms seems
    #   to work well )
    DG_init = [ "0", "1.1*mean", "0.5*rms", "0.8*mean", "0*rms" ]

    # Create the function object
    DG_func = function( DG_formula, DG_init, DG_parlimits )

    # Tag it as a standard double Gaussian function, pass rel_weight, mean and rms
    setattr( DG_func, 'Is_DG', True )
    setattr( DG_func, 'DG_rel_weight', config['DG_rel_weight'] )
    setattr( DG_func, 'DG_mean', DG_mean )
    setattr( DG_func, 'DG_rms', DG_rms )

    # Optional: set a fit range
    setattr( DG_func, 'fitrange', (30.1, 500.0) )

    config['Standard_DG_func'] = DG_func

    ########################################
    # Fit functions
    ########################################

    # Specify a function for every eta bin, for every particle
    config['bin_functions'] = {}
    config['ABFunctions'] = {}


    # Define actual fit functions per eta bin
    #   Currently: fill in double Gaussians for every eta bin for b, single for l
    config['bin_functions']['b']= [
        copy.deepcopy(DG_func) for i in range(len(config['eta_axis'])-1)]
    config['bin_functions']['l']= [
        copy.deepcopy(DG_func) for i in range(len(config['eta_axis'])-1)]

    # Specify the across bin functions; use 1 function per parameter in the SBF
    config['ABFunctions']['b'] = [
        function(),
        function( "[0]+[1]*x", [ "0" , "1" ] ),
        function( "sqrt([0]*[0] + x*[1]*[1] + x*x*[2]*[2])", [ "0", "0", "0" ] ),
        function( "[0]+[1]*x", [ "0" , "1" ] ),
        function( "sqrt([0]*[0] + x*[1]*[1] + x*x*[2]*[2])", [ "0", "0", "0" ] ) ]

    config['ABFunctions']['l'] = [
        function(),
        function( "[0]+[1]*x", [ "0" , "1" ] ),
        function( "sqrt([0]*[0] + x*[1]*[1] + x*x*[2]*[2])", [ "0", "0", "0" ] ),
        function( "[0]+[1]*x", [ "0" , "1" ] ),
        function( "sqrt([0]*[0] + x*[1]*[1] + x*x*[2]*[2])", [ "0", "0", "0" ] ) ]

    """
    # Standard for Single Gaussian:
    config['ABFunctions']['l'] = [
        function(),
        function( "[0]+[1]*x", [ "0" , "1" ] ),
        function( "sqrt([0]*[0] + x*[1]*[1] + x*x*[2]*[2])", [ "0", "0", "0" ] ) ]
    """


    ########################################
    # Entries added by readtree.py
    ########################################

    # config['selection_string']: The string used in the E-binning to select the
    #   right events

    # config['n_E_hist_bins']: The number of bins used when creating a histogram of
    #   quark/mc energy to determine the E-binning

    # config['E_value_mean_or_center']: Method of determining the single energy value
    #   of an energy bin. With option 'm', the mean of the entries of the bin was
    #   chosen as the single E-value. With the option 'c', simply the center is used.

    # config['SBF_plot_ranges']: A dictionary with particles as keys (usually 'b' and
    #   'l'). In config['SBF_plot_ranges'][particle][i_eta][i_E], a 2-element list is
    #   stored, [x_min, x_max], which are the ranges of the plot for this particle/
    #   eta/energy.

    # config['SBF_n_bins']: A dictionary with particles as keys (usually 'b' and
    #   'l'). config['SBF_n_bins'][particle][i_eta][i_E] contains the number of bins
    #   used for a single eta-E bin histogram.

    # config['n_total_events']: Total number of events in .root file.

    # config['events_used']: Total number of events actually used in the histograms.

    # config['SBF_pickle_filename']: path/filename of the pickle file that contains
    #   the single bin fit data.


    ########################################
    # Write configuration to file:
    ########################################

    f = open( 'config.dat', 'wb' )
    pickle.dump( config , f )

    print "config.dat created"


    if not os.path.isdir( 'configs/{0}'.format(config['outputdir']) ):
        os.makedirs( 'configs/{0}'.format(config['outputdir']) )

    shutil.copyfile( 'config.py', 'configs/{0}/config.py'.format(
        config['outputdir'] ) )

########################################
# End of Main
########################################
def main():
    Make_config()

if __name__ == "__main__":
  main()
