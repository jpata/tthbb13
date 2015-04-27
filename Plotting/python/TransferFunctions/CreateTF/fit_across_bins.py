#!/usr/bin/env python
"""
Thomas:
Calculating the Transfer Function

"""


########################################
# Imports
########################################

import pickle
import ROOT
import os

from TFClasses import function
from TFClasses import TF


########################################
# About the TF Matrix
########################################

    ### Structure of the TF matrix ###

    # TFmat is in this case a 2x2 matrix: 2 particles ('b' and 'l'), and 2 eta bins.
    # Retrieving a TF object is done by first specifying the particle, and then the
    # eta bin (0: 0.0<eta<1.0, 1: 1.0<eta<2.5). For example:
    # TFMat['b'][0] is the TF object for bottom quarks with 0.0<eta<1.0.

    ### The TF Object ###

    # The TF class can be found in TFClasses.py. The most important features of the
    # class are described here.

    # The attribute 'SingleBinFunc' contains the (ROOT formatted) string which
    # specifies the function used to fit the reconstr. energy in a single energy-eta
    # bin. The fit parameters of this SingleBinFunc are fitted *across* the
    # energy-eta bins, which results in one fit function dependent on MC energy per
    # eta-bin per fit parameter in the SingleBinFunc.

    # The fit functions across the bins are stored in separate function objects. The
    # function object can also be found in TFClasses.py. It contains the following
    # attributes:
    #  - str: the (ROOT) string that is the fit function
    #  - init: initialization of the parameters
    #  - par_values: fitted values of the parameters
    #  - par_errors: found errors of the fitted parameters.

    # The TH class contains the function 'Make_Formula()'. The across bin functions
    # are then filled in in the SingleBinFunc to create one (ROOT) output string.
    # The function automatically sets the parameters (the values are stored in
    # par_values).

    # In this version, Make_Formula returns a string which contains 7 parameters:
    #  - 1 parameter that is constant (1)
    #  - 2 parameters for the linear fit over the mean of the Gaussian
    #  - 3 parameters for the quadratic fit over the RMS of the Gaussian
    #  - 1 parameter that should be set by the user: the MC energy. This will be
    #    always parameter [0].

    # Later versions will contain more parameters, but [0] will always be MC energy
    # (or quark energy).

    # See also the example regarding Make_Formula at the end of this program.


########################################
# Functions
########################################

def Make_AcrossBinFit( TFobj, fit_dicts, config ):

    i_eta = TFobj.i_eta
    particle = TFobj.particle

    eta_bounds = fit_dicts[0]['eta_bounds']


    # Setup the canvas
    c1 = ROOT.TCanvas("c1","c1",500,400)
    c1.SetGrid()    

    # Fill in the ABFs into the TFobj (deep copies)
    for (i_abfunc, abfunc) in enumerate( config['ABFunctions'][particle] ):
        TFobj.SetAcrossBinFunc( i_abfunc, abfunc )

    # Perform the fits on the across bin functions in the class
    for (i_abfunc, abfunc) in enumerate( TFobj.AcrossBinFuncs ):

        # Don't perform any fitting for empty functions
        if abfunc.str == "1":
            continue


        ########################################
        # Creating and filling TGraph object
        ########################################

        # Usually begin and end fits are bad - specify number of skipped bins at
        # beginning and at end
        skip_begin = 3
        skip_end = 0

        # Open temporary lists to store across-bin fit data
        point_x = []
        point_y = []
        er_point_y = []


        for (i_E, dic) in enumerate(fit_dicts):

            if i_E >= skip_begin and i_E < (len(fit_dicts) - skip_end):

                if dic['single_bin_func'].par_values[3] > 30.0 and \
                   dic['single_bin_func'].par_values[3] < \
                   0.9*dic['single_bin_func'].par_values[1] :

                    point_y.append(
                        abs( dic['single_bin_func'].par_values[i_abfunc] ) )

                    point_x.append( dic['E_value'] )

                    er_point_y.append( dic['single_bin_func'].par_errors[i_abfunc] )


        # Open TGraphErrors object to fit
        gr = ROOT.TGraphErrors( len(point_y) )

        for ( i, E_value, par_value, par_error ) in zip(
            range(len(point_y)), point_x, point_y, er_point_y ):

            gr.SetPoint(
                i,
                E_value,
                par_value )

            gr.SetPointError(
                i,
                0.0,
                par_error )


        ########################################
        # Fitting: writing fit data to class objects
        ########################################

        # Specify fit across bins
        f1 = abfunc.Initialize_as_TF1()

        gr.Fit(f1,'Q')
        gr.Fit(f1,'Q')
        gr.Fit(f1,'Q')

        # Write fit results to lists in the class:
        for i in range( len( abfunc.par_initials ) ):
            abfunc.par_values.append( f1.GetParameter(i) )
            abfunc.par_errors.append( f1.GetParError(i) )


        ########################################
        # Drawing: Creating pdf, png and html
        ########################################

        plottitle = 'parameter [{0}] fit for {1}  |  {2} < eta < {3}'.format(
        i_abfunc, particle, eta_bounds[0], eta_bounds[1])

        gr.SetTitle( plottitle )
        gr.SetMarkerColor(4);
        gr.SetMarkerStyle(22);
        gr.SetMarkerSize(0.8);
        gr.GetXaxis().SetTitle( '{0} mc'.format( config['E_or_Pt_str'] ) );
        gr.GetYaxis().SetTitle( 'parameter {0}'.format(i_abfunc) );

        gr.Draw("AP")
        c1.Update()
        
        # Construct filename
        filename = 'par{0}-{1}-eta{2}'.format( i_abfunc, particle, i_eta )

        # Write pdf
        c1.Print("{0}/TFs/{1}".format( config['outputdir'], filename ), "pdf")

        # Write png
        print 'Writing {0}.png'.format( filename )
        img = ROOT.TImage.Create()
        img.FromPad(c1)
        img.WriteImage('{0}/TFs/{1}.png'.format( config['outputdir'], filename ) )


        # Write line to html. If html doesn't exist, create one.

        if not os.path.exists('{0}/{1}-overview.html'.format(
                config['outputdir'], i_abfunc) ) :

            # Open an html-file
            hf = open( '{0}/{1}-overview.html'.format(
                config['outputdir'], i_abfunc), 'w' )

            hf.write( '<html><body>\n' )
            hf.write( '<h1>Parameter {0} overview</h1>'.format(i_abfunc) )

            hf.write( 'SBF: {0}\n<br>ABF: {1}\n<br>\n<hr />'.format(
                TFobj.SingleBinFunc.str,
                abfunc.str ) )

            hf.write( '<h2>' )
            hf.write( 'Run: {0}\n<br>\n'.format( config['outputdir'] ) )
            hf.write( 'Sample: {0}\n<br>\n'.format( config['input_root_file_name'] ))
            #hf.write( '{0} out of {1} events used\n<br>\n'.format(
            #    config['events_used'],
            #    config['n_total_events'] ) )
            hf.write( '</h2>' )

        else:
            hf = open( '{0}/{1}-overview.html'.format(
                config['outputdir'], i_abfunc), 'a' )

        hf.write('<a href="TFs/{0}"><img width="700" src="TFs/{0}.png"></a>\n'.format(filename) )







########################################
# Main
########################################

def Fit_Across_Bins():

    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")
    ROOT.gStyle.SetOptFit(1011)

    # Import config.dat; check for existence
    if not os.path.isfile('config.dat'):
        print "Fit_Across_Bins: Error: Can't find configuration file config.dat"
        return 0

    print 'Fit_Across_Bins: Importing config.dat'
    pickle_f = open( 'config.dat', 'rb' )
    config = pickle.load( pickle_f )
    pickle_f.close()

    outputdir = config['outputdir']
    
    if not os.path.isdir(outputdir):
        print 'Directory {0} does not exist'.format(outputdir)

    if not os.path.isdir(outputdir+'/TFs'):
        os.makedirs(outputdir+'/TFs')

    # Import the dictionary of fit data from the pickle file
    print 'Importing fit data'
    pickle_f = open( config['SBF_fitted_hists_pickle_filename'] , 'rb' )
    fit_dicts = pickle.load( pickle_f )
    print 'Fitting across bins'

    # Determine size of fit dataset
    particles = fit_dicts.keys()
    n_particles = len(particles)

    n_eta_bins = len( fit_dicts[particles[0]] )
    n_E_bins = len( fit_dicts[particles[0]][0] )


    ########################################
    # Initializing the TF matrix
    ########################################

    TFmat = {}
    
    for particle in particles:
        TFmat[particle] = []

        for i_eta in range( n_eta_bins ):

            TFobj = TF( particle , i_eta )

            # Set the single bin function according to the first energy bin, since
            # the fit function will not change over energy.
            TFobj.SetSingleBinFunc( fit_dicts[particle][i_eta][0]['single_bin_func'])

            TFmat[particle].append( TFobj )
        

    ########################################
    # Creating the fit over bins plot for parameter 1 (mean) and 2 (rms)
    ########################################

    parfuncs = config['ABFunctions']

    # Delete any old html files, if present
    #   This is necessary because the Make_Fitting() function will otherwise append
    #   lines to existing html files.
    for particle in particles:
        for i_param in range(len(parfuncs[particle])):
            if os.path.isfile('{0}/{1}-overview.html'.format(outputdir, i_param) ):
                os.remove( '{0}/{1}-overview.html'.format(outputdir, i_param) )

    for particle in particles:
        for i_eta in range( n_eta_bins ):

            Make_AcrossBinFit(
                TFmat[particle][i_eta],
                fit_dicts[particle][i_eta],
                config )



    ########################################
    # Extra control plot: average of the 2 Gaussian means
    ########################################

    # Open an html-file
    hf = open( '{0}/par13-overview.html'.format(outputdir), 'w' )
    hf.write( '<html><body>\n<h1>Run Summary:\n</h1>\n<br>\n<hr />' )
    hf.write( '<h2>Title</h2>' )

    # Setup the canvas
    c1 = ROOT.TCanvas("c1","c1",500,400)
    c1.SetGrid()

    DG_rel_w = config['DG_rel_weight']

    #for particle in particles:
    for particle in ['b']:
        for i_eta in range( n_eta_bins ):

            fit_dicts_this_eta = fit_dicts[particle][i_eta]

            gr = ROOT.TGraphErrors( len(fit_dicts_this_eta) )

            for (i, dic) in enumerate(fit_dicts_this_eta):

                gr.SetPoint(
                    i,
                    dic['E_value'],
                    DG_rel_w * dic['single_bin_func'].par_values[1] \
                    + (1-DG_rel_w) * dic['single_bin_func'].par_values[3])

                gr.SetPointError(
                    i,
                    0.0,
                    DG_rel_w * dic['single_bin_func'].par_errors[1] \
                    + (1-DG_rel_w) * dic['single_bin_func'].par_errors[3])


            f2 = ROOT.TF1( "fit2", "[0]+[1]*x" )
            gr.Fit(f2,'Q')

            plottitle = 'Average of parameter [1] and [3] for {0}  |  {1} < eta < {2}'.format( particle, dic['eta_bounds'][0], dic['eta_bounds'][1] )

            gr.SetTitle( plottitle )
            gr.SetMarkerColor(4);
            gr.SetMarkerStyle(22);
            gr.SetMarkerSize(0.8);
            gr.GetXaxis().SetTitle( '{0} mc'.format(config['E_or_Pt_str']) );
            gr.GetYaxis().SetTitle( 'Avg. of [1] and [3]' );

            gr.Draw("AP")
            c1.Update()

            filename = 'avgpar1and3-{0}-{1}'.format( particle, i_eta )

            # Write png
            print 'Writing {0}.png'.format( filename )
            img = ROOT.TImage.Create()
            img.FromPad(c1)
            img.WriteImage('{0}/TFs/{1}.png'.format( outputdir, filename ) )

            # Write line to html
            hf.write('<a href="TFs/{0}.png"><img width="700" src="TFs/{0}.png"></a>\n'.format(filename) )



    print "Writing Transfer Functions to {0}/TFMatrix.dat".format(outputdir)

    picklef = open( '{0}/TFMatrix.dat'.format(outputdir), 'wb' )
    pickle.dump( TFmat , picklef )



########################################
# End of main
########################################   

def main():
    Fit_Across_Bins()

if __name__ == "__main__":
    main()
