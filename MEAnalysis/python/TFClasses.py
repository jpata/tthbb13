########################################
# Classes
########################################

import re
import os
import ROOT
import copy

class TF:

    def __init__(self, particle, i_eta):
        self.i_eta = i_eta
        self.particle = particle

        self.SingleBinFunc = ""
        self.AcrossBinFuncs = []


    def SetSingleBinFunc( self, single_bin_func ):
        self.SingleBinFunc = single_bin_func.str
        for i in range( len(single_bin_func.par_initials) ):
            self.AcrossBinFuncs.append( function() )

    
    def SetAcrossBinFunc( self, i_par, across_bin_func ):
        self.AcrossBinFuncs[i_par] = copy.deepcopy(across_bin_func)


    def Make_Fitting( self, fit_dicts, outputdir ): 

        # Setup the canvas
        c1 = ROOT.TCanvas("c1","c1",500,400)
        c1.SetGrid()

        for par_num in range( len( self.AcrossBinFuncs )):

            # Don't perform any fitting for empty functions
            if self.AcrossBinFuncs[par_num].str == "1":
                continue

            ########################################
            # Creating and filling TGraph object
            ########################################

            gr = ROOT.TGraphErrors( len(fit_dicts) )

            for (i_E, dic) in enumerate(fit_dicts):

                gr.SetPoint(
                    i_E,
                    dic['E_value'],
                    abs( dic['single_bin_func'].par_values[par_num] ) )

                gr.SetPointError(
                    i_E,
                    0.0,
                    dic['single_bin_func'].par_errors[par_num] )


            ########################################
            # Fitting: writing fit data to class objects
            ########################################

            # Specify fit across bins
            f1 = self.AcrossBinFuncs[par_num].Initialize_as_TF1()

            gr.Fit(f1,'Q')

            # Write fit results to lists in the class:
            for i in range( len( self.AcrossBinFuncs[par_num].par_initials ) ):
                self.AcrossBinFuncs[par_num].par_values.append( f1.GetParameter(i) )
                self.AcrossBinFuncs[par_num].par_errors.append( f1.GetParError(i) )


            ########################################
            # Drawing: Creating pdf, png and html
            ########################################

            dic0 = fit_dicts[0]

            plottitle = 'parameter {0} fit for {1}  |  {2} < eta < {3}'.format(
            par_num, dic0['type'], dic0['eta_bounds'][0], dic0['eta_bounds'][1])

            gr.SetTitle( plottitle )
            gr.SetMarkerColor(4);
            gr.SetMarkerStyle(22);
            gr.SetMarkerSize(0.8);
            gr.GetXaxis().SetTitle( 'E mc' );
            gr.GetYaxis().SetTitle( 'parameter {0}'.format(par_num) );

            gr.Draw("AP")
            c1.Update()
            
            # Construct filename
            filename = 'par{0}-{1}-eta{2}'.format(
                par_num, dic['type'], dic['i_eta'] )

            # Write pdf
            c1.Print("{0}/TFs/{1}".format( outputdir, filename ),"pdf")

            # Write png
            print 'Writing {0}.png'.format( filename )
            img = ROOT.TImage.Create()
            img.FromPad(c1)
            img.WriteImage('{0}/TFs/{1}.png'.format( outputdir, filename ) )


            # Write line to html. If html doesn't exist, create one.

            if not os.path.exists('{0}/{1}-overview.html'.format(
                    outputdir, par_num) ) :

                # Open an html-file
                hf = open( '{0}/{1}-overview.html'.format(
                    outputdir, par_num), 'w' )
                hf.write( '<html><body>\n<h1>Run Summary:\n</h1>\n<br>\n<hr />' )
                hf.write( '<h2>Title</h2>' )

            else:
                hf = open( '{0}/{1}-overview.html'.format(
                    outputdir, par_num), 'a' )

            hf.write('<a href="TFs/{0}.png"><img width="700" src="TFs/{0}.png"></a>\n'.format(filename) )


    def Make_Formula(self, print_info = False):

        SBF = self.SingleBinFunc

        # First value is not used (would correspond with the [0]-variable)
        output_par_values = [0]

        # Renumber the formula's in the across-bin-functions

        shift = 1
        for (par_num, func) in enumerate( self.AcrossBinFuncs ):

            ABFstr = func.str

            # For 'empty' functions, just replace by the shift and store 1.0
            if ABFstr == '1':
                SBF = SBF.replace(
                    '[{0}]'.format(par_num), '[{0}REPLACED]'.format(shift) )
                output_par_values.append( 1.0 )
                shift += 1
                continue

            else:

                # For non-empty functions, loop over the parameters and replace
                # with the shift, plus a 'REPLACED'-tag.
                # The 'REPLACED'-tag is removed at the end. It is needed to prevent
                # double replacement.
                for i_param in range( len( func.par_initials )):

                    ABFstr = ABFstr.replace(
                        '[{0}]'.format(i_param), '[{0}REPLACED]'.format(shift) )
                    shift += 1
                    output_par_values.append( func.par_values[i_param] )

                # 'x' in the ABFs will be [0] (the MC energy) in the end:
                ABFstr = ABFstr.replace( 'x', '[0REPLACED]' )

                SBF = SBF.replace('[{0}]'.format(par_num), '({0})'.format(ABFstr) )

        SBF = SBF.replace( 'REPLACED', '')


        # Construct the TF1 object        
        f1 = ROOT.TF1( "fit1", SBF, 0, 150 )

        # Set the parameters
        for i in range( 1, len( output_par_values ) ):
            f1.SetParameter( i, output_par_values[i] )

        if print_info:
            # Printing
            print '    Replaced SingleBinFunc:'
            print '    {0}'.format(SBF)

            print '    x = Reconstructed Energy, [0] = MC energy (or quark energy)'
            print '    Other parameters:'
            for i in range( 1, len( output_par_values ) ):
                print '      [{0}] = {1}'.format( i, f1.GetParameter(i) )

        return f1




class function:

    counter = 0

    def __init__(self, str = "1", par_initials = [] ):
        self.str = str
        self.par_initials = par_initials
        self.par_values = []
        self.par_errors = []

    def Initialize_as_TF1( self, hist = 'none' ):

        f1 = ROOT.TF1( "h{0}".format(self.counter), self.str )
        self.counter +=1

        # Set the initial values for parameters of the fit.
        #   Allowed are numbers, valid python expressions, and the strings
        #   'int', 'mean' and 'rms' if a histogram is given as an argument.
        #   These are then automatically replaced by the values for the integral,
        #   mean and rms respectively.
        for i in range( len( self.par_initials ) ):
            
            init_var_str = self.par_initials[i]

            if hist is not 'none':
                init_var_str = init_var_str.replace(
                    "int",
                    str( hist.Integral() ) )

                init_var_str = init_var_str.replace(
                    "mean",
                    str( hist.GetMean() ) )

                init_var_str = init_var_str.replace(
                    "rms",
                    str( hist.GetRMS() ) )

            f1.SetParameter( i, eval( init_var_str ) )

        return f1

    def Check_function( self ):

        # Check format of fit_function

        # Get list of used variables in function
        fitvars = re.findall( r'\[([0-9]+)\]', self.str )

        # Convert to int types and sort
        index_var = []   
        for var in fitvars:
            index_var.append( int(var) )
        index_var.sort()

        for index, name in enumerate(index_var):
            # Check if fit function skipped a number
            if index != name:
                print 'Error: fit parameter mismatch'
                print '    Fit function parameters are missing'
                print '    Variable [{0}] found, expected [{1}]'.format(name,index)
                return 1
            # Check if there are more parameters in the function than initialized
            if name > len( self.par_initials )-1:
                print 'Error: fit parameter mismatch'
                print '    Some fit function parameters are not initialized'
                print '    Variable [{0}] found, but only {1} parameter(s) initialized'.format( name, len( self.par_initials ) )
                return 1

        # Check if there are more parameters initialized than are in the fit function
        if len( self.par_initials ) > len(index_var):
            print 'Error: fit parameter mismatch'
            print '    {0} fit parameters initialized, but only {1} found in fit function'.format( len(self.par_initials), len(index_var) )
            return 1
        
        # Exiting without problems
        return 0
