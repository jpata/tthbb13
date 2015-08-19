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
        self.AcrossBinFuncs = []


    def SetSingleBinFunc( self, single_bin_func ):
        self.SingleBinFunc = copy.deepcopy( single_bin_func )
        for i in range( len(single_bin_func.par_initials) ):
            self.AcrossBinFuncs.append( function() )

    
    def SetAcrossBinFunc( self, i_par, across_bin_func ):
        self.AcrossBinFuncs[i_par] = copy.deepcopy(across_bin_func)


    def Make_Fitting( self, fit_dicts, outputdir, Pt_or_E ): 

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

            skip_begin = 0
            skip_end = 0

            point_x = []
            point_y = []
            er_point_y = []


            for (i_E, dic) in enumerate(fit_dicts):

                if i_E >= skip_begin and i_E < (len(fit_dicts) - skip_end) and \
                    dic['single_bin_func'].par_values[3]>25.0 and \
                    dic['single_bin_func'].par_values[4]>2.5 :

                    point_y.append(
                        abs( dic['single_bin_func'].par_values[par_num] ) )

                    point_x.append( dic['E_value'] )

                    er_point_y.append( dic['single_bin_func'].par_errors[par_num] )


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



                """
                gr.SetPoint(
                    i_E-2,
                    dic['E_value'],
                    abs( dic['single_bin_func'].par_values[par_num] ) )

                gr.SetPointError(
                    i_E-2,
                    0.0,
                    dic['single_bin_func'].par_errors[par_num] )
                """

                

            ########################################
            # Fitting: writing fit data to class objects
            ########################################

            # Specify fit across bins
            f1 = self.AcrossBinFuncs[par_num].Initialize_as_TF1()

            gr.Fit(f1,'Q')
            gr.Fit(f1,'Q')
            gr.Fit(f1,'Q')

            # Write fit results to lists in the class:
            for i in range( len( self.AcrossBinFuncs[par_num].par_initials ) ):
                self.AcrossBinFuncs[par_num].par_values.append( f1.GetParameter(i) )
                self.AcrossBinFuncs[par_num].par_errors.append( f1.GetParError(i) )


            ########################################
            # Drawing: Creating pdf, png and html
            ########################################

            dic0 = fit_dicts[0]

            plottitle = 'parameter [{0}] fit for {1}  |  {2} < eta < {3}'.format(
            par_num, dic0['type'], dic0['eta_bounds'][0], dic0['eta_bounds'][1])

            gr.SetTitle( plottitle )
            gr.SetMarkerColor(4);
            gr.SetMarkerStyle(22);
            gr.SetMarkerSize(0.8);
            gr.GetXaxis().SetTitle( '{0} mc'.format(Pt_or_E) );
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


    def Make_Formula(self, set_reco = True, print_info = False):

        SBF = self.SingleBinFunc.str

        # First value is not set automatically
        #   (corresponds with [0], which should be set by the user outside of this class function)
        output_par_values = [0]

        # Renumber the formula's in the across-bin-functions

        shift = 1

        if set_reco:
            # Replace all x with [0REPLACED] now, so it won't be replaced twice
            # Careful not to replace the 'x' in 'exp'
            SBF = re.sub( r'([^e])x([^p])', r'\1[0REPLACED]\2', SBF )

            # This means [0] is now reconstructed, and x will be mc/gen

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

                if not set_reco:
                    # 'x' in the ABFs are the quark/mc/gen variable; should be [0] in end result:
                    #   ( [0] = gen, x = reco )
                    ABFstr = ABFstr.replace( 'x', '[0REPLACED]' )

                SBF = SBF.replace('[{0}]'.format(par_num), '({0})'.format(ABFstr) )

        SBF = SBF.replace( 'REPLACED', '')


        # Construct the TF1 object        
        f1 = ROOT.TF1( "fit1", SBF )

        # Set the parameters
        for i in range( 1, len( output_par_values ) ):
            f1.SetParameter( i, output_par_values[i] )

        if print_info:
            # Printing
            print '    Replaced SingleBinFunc:'
            print '    {0}'.format(SBF)

            if set_reco: print '    x = MC/Gen variable, [0] = Reconstructed variable (E or Pt)'
            else: print '    x = Reconstructed variable (E or Pt), [0] = MC/Gen variable'

            print '    Other parameters:'
            for i in range( 1, len( output_par_values ) ):
                print '      [{0}] = {1}'.format( i, f1.GetParameter(i) )

        return f1

    
    def Make_CDF(self):

        SBF = copy.deepcopy(self.SingleBinFunc)
        SBFstr = SBF.str
        
        if hasattr( SBF, 'Is_DG' ):

            ########################################
            # Replacing mean
            ########################################

            shift = 1

            # First element is ignored (corresponds with [0], which should be set outside
            #   this function)
            mean_values = [0]

            DG_mean_list = getattr( SBF, 'DG_mean' )


            # Get list (without duplicates) of the SBF variables used in the rms
            SBFvars_in_mean = []
            for DG_mean in DG_mean_list:
                SBFvars_in_mean.extend( re.findall( r'\[([0-9]+)\]', DG_mean ) )
            SBFvars_in_mean = list( set( SBFvars_in_mean ) )

            # Get a replacement for every SBF variable used
            for mean in SBFvars_in_mean:

                # Get the corresponding ABF
                ABFunc = copy.deepcopy( self.AcrossBinFuncs[ int(mean) ] )
                ABFstr = ABFunc.str

                # Shift parameters in ABF
                for i_param in range( len( ABFunc.par_initials )):

                    ABFstr = ABFstr.replace(
                        '[{0}]'.format(i_param), '[{0}REPLACED]'.format(shift) )
                    shift += 1

                    # Save also the values; need to set parameters right later
                    mean_values.append( ABFunc.par_values[i_param] )

                # Replace the x by [0] (mc/gen is set, cut-off is evaluated for)
                ABFstr = ABFstr.replace( 'x', '[0REPLACED]' )

                # Go through original mean list and replace the SBF variables
                for i in range( len( DG_mean_list )):
                    DG_mean_list[i] = DG_mean_list[i].replace( '[' + mean + ']' , ABFstr )

            DG_mean_list = [ i.replace( 'REPLACED', '' ) for i in DG_mean_list ]

            ########################################
            # Replacing RMS
            ########################################

            RMS_values = []

            DG_rms_list = getattr( SBF, 'DG_rms' )

            # Get list (without duplicates) of the SBF variables used in the rms
            SBFvars_in_RMS = []
            for DG_rms in DG_rms_list:
                SBFvars_in_RMS.extend( re.findall( r'\[([0-9]+)\]', DG_rms ) )
            SBFvars_in_RMS = list( set( SBFvars_in_RMS ) )

            # Get a replacement for every SBF variable used
            for RMS in SBFvars_in_RMS:

                # Get the corresponding ABF
                ABFunc = self.AcrossBinFuncs[ int(RMS) ]
                ABFstr = ABFunc.str

                # Shift parameters in ABF
                for i_param in range( len( ABFunc.par_initials )):

                    ABFstr = ABFstr.replace(
                        '[{0}]'.format(i_param), '[{0}REPLACED]'.format(shift) )
                    shift += 1

                    # Save also the values; need to set parameters right later
                    RMS_values.append( ABFunc.par_values[i_param] )

                # Replace the x by [0] (mc/gen is set, cut-off is evaluated for)
                ABFstr = ABFstr.replace( 'x', '[0REPLACED]' )

                # Go through original rms list and replace the SBF variables
                for i in range( len( DG_rms_list )):
                    DG_rms_list[i] = DG_rms_list[i].replace( '[' + RMS + ']' , '(' + ABFstr + ')')

            DG_rms_list = [ i.replace( 'REPLACED', '' ) for i in DG_rms_list ]


            # Construct the formula string the final CDF
            CDFstr = '{0}*ROOT::Math::normal_cdf((x-({1})),{2})+(1-{0})*'\
                'ROOT::Math::normal_cdf((x-({3})),{4})'.format(
                getattr( SBF, 'DG_rel_weight' ),
                DG_mean_list[0],
                DG_rms_list[0],
                DG_mean_list[1],
                DG_rms_list[1] )

            output_TF1 = ROOT.TF1( 'CDF', CDFstr )

            # Set the parameters
            mean_values.extend( RMS_values )


            for ( i, value ) in enumerate( mean_values ):
                if i > 0: output_TF1.SetParameter( i, value )
                #print '[{0}] = {1}'.format( i, output_TF1.GetParameter(i) )
            #print '\n{0}'.format( output_TF1.GetTitle() )

            return copy.deepcopy( output_TF1 )


        elif hasattr( SBF, 'Is_SG' ):

            ########################################
            # Replacing mean
            ########################################

            shift = 1

            # First element is ignored (corresponds with [0], which should be set outside
            #   this function)
            mean_values = [0]

            SG_mean = getattr( SBF, 'SG_mean' )

            # Get list (without duplicates) of the SBF variables used in the mean
            SBFvars_in_mean = re.findall( r'\[([0-9]+)\]', SG_mean )
            SBFvars_in_mean = list( set( SBFvars_in_mean ) )

            # Get a replacement for every SBF variable used
            for mean in SBFvars_in_mean:

                # Get the corresponding ABF
                ABFunc = self.AcrossBinFuncs[ int(mean) ]
                ABFstr = ABFunc.str

                # Shift parameters in ABF
                for i_param in range( len( ABFunc.par_initials )):

                    ABFstr = ABFstr.replace(
                        '[{0}]'.format(i_param), '[{0}REPLACED]'.format(shift) )
                    shift += 1

                    # Save also the values; need to set parameters right later
                    mean_values.append( ABFunc.par_values[i_param] )

                # Replace the x by [0] (mc/gen is set, cut-off is evaluated for)
                ABFstr = ABFstr.replace( 'x', '[0REPLACED]' )

                # Go through original mean list and replace the SBF variables
                SG_mean = SG_mean.replace( '[' + mean + ']' , ABFstr )

            SG_mean = SG_mean.replace( 'REPLACED', '' )

            ########################################
            # Replacing RMS
            ########################################

            RMS_values = []

            SG_rms = getattr( SBF, 'SG_rms' )

            # Get list (without duplicates) of the SBF variables used in the rms
            SBFvars_in_RMS = re.findall( r'\[([0-9]+)\]', SG_rms )
            SBFvars_in_RMS = list( set( SBFvars_in_RMS ) )

            # Get a replacement for every SBF variable used
            for RMS in SBFvars_in_RMS:

                # Get the corresponding ABF
                ABFunc = self.AcrossBinFuncs[ int(RMS) ]
                ABFstr = ABFunc.str

                # Shift parameters in ABF
                for i_param in range( len( ABFunc.par_initials )):

                    ABFstr = ABFstr.replace(
                        '[{0}]'.format(i_param), '[{0}REPLACED]'.format(shift) )
                    shift += 1

                    # Save also the values; need to set parameters right later
                    RMS_values.append( ABFunc.par_values[i_param] )

                # Replace the x by [0] (mc/gen is set, cut-off is evaluated for)
                ABFstr = ABFstr.replace( 'x', '[0REPLACED]' )

                # Go through original rms list and replace the SBF variables
                SG_rms = SG_rms.replace( '[' + RMS + ']' , '(' + ABFstr + ')')

            SG_rms = SG_rms.replace( 'REPLACED', '' )


            # Construct the formula string the final CDF
            CDFstr = 'ROOT::Math::normal_cdf((x-({0})),{1})'.format( SG_mean, SG_rms )

            output_TF1 = ROOT.TF1( 'CDF', CDFstr )

            # Set the parameters
            mean_values.extend( RMS_values )
            for ( i, value ) in enumerate( mean_values ):
                if i > 0: output_TF1.SetParameter( i, value )
                
                #print '[{0}] = {1}'.format( i, output_TF1.GetParameter(i) )
            #print '\n{0}'.format( output_TF1.GetTitle() )

            return output_TF1

        else:
            print 'Single Bin Function is not a single or double Gaussian; unable to build '\
                'analytic expression for the CDF.'
            return 0


    def Print_content(self):

        print 'Class: i_eta = {0}, particle = {1}'.format(
            self.i_eta, self.particle )

        print '    Single bin function:'
        print '    --------------'
        print '      fun: {0}'.format( self.SingleBinFunc.str )
        print '      init: {0}'.format( self.SingleBinFunc.par_initials )
        print '      param: {0}'.format( self.SingleBinFunc.par_values )
        print '      er par: {0}'.format( self.SingleBinFunc.par_errors )
        print '    --------------'

        print '    {0} Across bin functions found:'.format(
            len( self.AcrossBinFuncs ) )

        print '    --------------'
        for func in self.AcrossBinFuncs:
            print '      fun: {0}'.format( func.str )
            print '      init: {0}'.format( func.par_initials )
            print '      param: {0}'.format( func.par_values )
            print '      er par: {0}'.format( func.par_errors )
            print '    --------------'










class function:

    def __init__(self, str = "1", par_initials = [], par_limits = [] ):
        self.str = str
        self.par_initials = par_initials
        self.par_values = []
        self.par_errors = []
        self.par_limits = par_limits


    def Initialize_as_TF1( self, hist = 'none' ):

        f1 = ROOT.TF1( "hfit", self.str )

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

        # Set parameter limits for the parameters that are specified as absolute:
        for (parameter, lower_bound, upper_bound) in self.par_limits:
            f1.SetParLimits( parameter, lower_bound, upper_bound )

        # Set fit range
        if hasattr( self, 'fitrange' ):
            f1.SetRange( getattr(self, 'fitrange')[0] , getattr(self, 'fitrange')[1] )

        return f1


    def Check_function( self ):

        # Check format of fit_function

        # Get list of used variables in function
        fitvars = re.findall( r'\[([0-9]+)\]', self.str )

        # Convert to int types, filter out duplicates, and sort
        index_var = []   
        for var in fitvars:
            index_var.append( int(var) )
        index_var = list(set(index_var))
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
