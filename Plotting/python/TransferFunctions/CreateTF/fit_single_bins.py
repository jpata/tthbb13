#!/usr/bin/env python


########################################
# Imports
########################################

import pickle
import ROOT
import copy
import os

from TFClasses import function
from TFClasses import TF

from draw_hists_and_fits import Draw_Hists_and_Fits


########################################
# Functions
########################################

def Fit_DG( hist, f_DG_in_main, config ):


    func_SG = copy.deepcopy( config['Standard_SG_func'] )
    f_SG = func_SG.Initialize_as_TF1( hist )

    
    hist.Fit( f_SG, 'Q' )

    SG_mean = f_SG.GetParameter(1)
    SG_rms = f_SG.GetParameter(2)

    func_DG = copy.deepcopy( config['Standard_DG_func'] )

    func_DG.par_initials[1] = str(0.8*SG_mean)
    func_DG.par_initials[3] = str(0.4*SG_mean)





    f_DG = func_DG.Initialize_as_TF1( hist )

    f_DG_in_main = copy.deepcopy(f_DG)

    return f_DG


########################################
# Main
########################################

def Fit_Single_Bins(conffile):

    ROOT.gROOT.SetBatch(True)
    #ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")

    # Don't display standard statistics
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptStat(0)


    # Load config.dat
    pickle_f = open( conffile, 'rb' )
    config = pickle.load( pickle_f )
    pickle_f.close()

    outputdir = config['outputdir']

    # Load the single bin histograms
    pickle_f = open( config['SBF_hists_pickle_filename'] , 'rb' )
    dicts = pickle.load( pickle_f )
    pickle_f.close()

    """
    # Load TF matrix, if it is already produced
    if os.path.isfile( '{0}/TFMatrix.dat'.format( config['outputdir'] ) ):
        pickle_f = open( '{0}/TFMatrix.dat'.format( config['outputdir'] ) , 'rb' )
        TFmat = pickle.load( pickle_f )
        pickle_f.close()
    """


    ########################################
    # Fitting & Drawing
    ########################################

    if config['Draw_ABF_in_single_bins']:
        print 'Performing fits'
        print '    Figures will be printed later (ABF results will be drawn in)'
    else:
        print 'Performing fits'
        print '    Figures will printed now'
        print '    (To draw the ABF results in the single bins, set'
        print "    config['Draw_ABF_in_single_bins'] to True)"

    c1 = ROOT.TCanvas("c1","c1",500,400)

    # Open up list to output the fit_dicts
    #   fit_dicts will be a dictionary of a matrix of fit-dictionaries. This is not 
    #   so cumbersome as it sounds; accessing a fit-dictionary is done with for
    #   example: fit_dicts['b'][0][1], which accesses the fit_dict for a bottom,
    #   at eta-index 0 and energy-index 1.

    fit_dicts = {}


    for particle in config['particles']:

        fit_dicts[particle] = []

        dic = dicts[particle]

        for i_eta in range( dic['n_eta_bins'] ):

            fit_dicts_this_eta = []

            for i_E in range( dic['n_E_bins'] ):

                # Get fitfunc, a function object
                fitfunc = copy.deepcopy( config['bin_functions'][particle][i_eta] )

                n_fit_params = len( fitfunc.par_initials )

                # Get a TF1 object. Requires hist as argument to calculate
                # mean/rms for initialization of the parameters
                f1 = fitfunc.Initialize_as_TF1( dic['hist_mat'][i_eta][i_E] )

                #f1.FixParameter(4, 0.0)

                # Doing the fit

                """
                # TODO: buggy behaviour
                if hasattr( fitfunc, 'Is_DG' ) and \
                    os.path.isfile('{0}/TFMatrix.dat'.format( config['outputdir'] )):

                    #print '--------------\n i_E = {0}'.format(i_E)

                    for i in range(5):
                        func_i = TFmat[particle][i_eta].AcrossBinFuncs[i]

                        f_i = func_i.Initialize_as_TF1()

                        for (i_par, par_val) in enumerate(func_i.par_values):
                            f_i.SetParameter( i_par, par_val )

                        f1.SetParameter(i, f_i.Eval( dic['E_values'][i_eta][i_E] ) )

                        #print 'par {0} = {1}'.format(
                        #    i, f_i.Eval( dic['E_values'][i_eta][i_E] ) )
                """

                if hasattr( fitfunc, 'Is_DG' ):

                    #left = max( 30.1, 0.7*dic['hist_mat'][i_eta][i_E].GetMean() )
                    left = 30.01
                    right = 1.7*dic['hist_mat'][i_eta][i_E].GetMean()

                    f1.SetRange( left, right )

                    print 'Range set: {0} to {1}'.format( left, right )


                dic['hist_mat'][i_eta][i_E].Fit(f1,'RQ')
                dic['hist_mat'][i_eta][i_E].Fit(f1,'RQ')
                dic['hist_mat'][i_eta][i_E].Fit(f1,'RQ')


                # Save the fit results in separate dicts; these dicts will be used to
                # fit across bins.
                fit_dict = {}

                fit_dict['type'] = dic['type']

                fit_dict['n_eta_bins'] = dic['n_eta_bins']
                fit_dict['n_E_bins'] = dic['n_E_bins']

                fit_dict['i_eta'] = i_eta
                fit_dict['i_E'] = i_E

                fit_dict['eta_bounds'] = [
                    config['eta_axis'][i_eta],
                    config['eta_axis'][i_eta+1] ]

                fit_dict['E_value'] = dic['E_values'][i_eta][i_E]
                fit_dict['E_bounds'] = [ dic['E_axis'][i_eta][i_E], dic['E_axis'][i_eta][i_E+1] ]

                for i in range( n_fit_params ):
                    fitfunc.par_values.append( f1.GetParameter(i) )
                    fitfunc.par_errors.append( f1.GetParError(i) )

                fit_dict['single_bin_func'] = copy.deepcopy(fitfunc)

                fit_dict['hist'] = copy.deepcopy(dic['hist_mat'][i_eta][i_E])

                fit_dicts_this_eta.append( fit_dict )

            fit_dicts[particle].append( fit_dicts_this_eta )


    # Export the dictionary of fit data to pickle file
    print 'Writing single bin fit data to {0}'.format(
        config['SBF_fitted_hists_pickle_filename'] )
    picklef = open( config['SBF_fitted_hists_pickle_filename'], 'wb' )
    pickle.dump( fit_dicts , picklef )
    picklef.close()




########################################
# End of Fit_Single_Bins
########################################   

def main():
    Fit_Single_Bins()

if __name__ == "__main__":
    main()
