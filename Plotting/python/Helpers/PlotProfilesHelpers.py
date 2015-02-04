#!/usr/bin/env python
"""
Helpers for making profile plots of 2d distributions.

Use ROOT TTrees as input.
"""

########################################
# Import standard Python modules
########################################

import sys
import copy
import pickle

########################################
# Import ROOT and setup with style
########################################

import ROOT

from TTH.Plotting.Helpers.PrepareRootStyle import myStyle

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()

ROOT.TH1.SetDefaultSumw2()


########################################
# Import private helpers
########################################

import TTH.Plotting.Helpers.OutputDirectoryHelper as OutputDirectoryHelper


########################################
# Define and crate output directory
########################################

output_dir = "OutputProfiles/"

# Create directory and subdirectories for all filetypes
OutputDirectoryHelper.CreateOutputDirs( output_dir )

dic_all_profiles = {}


########################################
# Class plotSettings
########################################

class plotSettings:
    """ Helper class to collect the options to set-up the
    pileup-profile plots.
    """

    # List that stores all plotSettings objects so we can loop over
    # them automatically
    li_all_plots = []
    
    def __init__(self, 
                 sample, 
                 x_variable,
                 y_variable,
                 cuts             = "",
                 nbins_x          = 40,
                 min_x            = 0,
                 max_x            = 0,
                 nbins_y          = 40,
                 min_y            = 0,
                 max_y            = 0,
                 log_y            = False,                 
                 ybars_are_sigma  = False,
                 overlay_eff      = False,
                 overlay_eff_file = "",
                 do_legend        = True,
                 legend_origin_x  = 0.62,
                 legend_origin_y  = 0.74, 
                 legend_size_x    = 0.3,
                 legend_size_y    = 0.2,
                 name_prefix      = "",
                 eval_at          = 0,
                 sample_type      = "single", 
                 ):

       """ Constructor
       Arguments:

       sample          : [] sample to use for this plot (lookup via dic_files)
                       : - can either be a string -> process one sample
                       :     (set sample_type to single)
                       : - or a list with exactly two entries -> friend them
                       :     (second entry vars can accessed by friend.X)
                       :     (set sample_type to friends)
                       : - or a list with arbitrary number of entries ->
                       :     process one after the other and add them before doing profiles
                       :     (set sample_type to multiple)
                       : - or a list of lists with (two entries each)
                       :     treat each pair as friends and add them up
                       :     (set sample_type to multiple_friends)
                       :      
       x_variable      : [string] variable to put on the x-axis
       y_variable      : [string] variable to put on the y-axis
       cuts            : [string] cuts to apply on the ntuple
       nbins_x         : [int] number of bins for the x-axis
       min_x           : [float] minimal value for x-axis
       min_y           : [float] minimal value for y-axis
       nbins_y         : [int] number of bins for the y-axis
       max_x           : [float] maximal value for x-axis
       max_y           : [float] maximal value for y-axis
       log_y           : [bool] draw the y-axis using a log-scale
       ybars_are_sigma : [bool] If set to true the vertical bars show the standard
                                 deviation instead of the error on the mean.
       overlay_eff     : [bool] If true: Overlay with the boundaries so that the efficiency
                                exceeds a threshold.
       overlay_eff_file: [string] file from which the efficiency shapes are read in
       do_legend       : [bool] Draw a legend
       legend_origin_x : [float] position of the left? edge of the legend
       legend_origin_y : [float] position of the upper? edge of the legend
       legend_size_x   : [float] horizontal extension of the legen
       legend_size_y   : [float] vertical extension of the legend        
       name_prefix     : [string] prefix to the name (so we can show the same vars w different cuts)
       sample_type     : [string] single/friends/multiple/multiple_friends (see sample above for details)
       """
       
       # Pass the argument variables

       # Since sample can be of different types
       # treat/check properly here
       # Single
       if sample_type == "single":           
           # Make sure sample is a string
           if not isinstance(sample, str):
               print "sample_type is set to single but sample looks loke this:"
               print sample
               print "Exiting..."
               sys.exit()

       # Friends
       elif sample_type == "friends":
           # Make sure sample is a list with two entries
           if (not isinstance(sample, list)) or (not len(sample)==2):
               print "sample_type is set to friends but sample looks loke this:"
               print sample
               print "Exiting..."
               sys.exit()               

       # Multiple single samples
       elif sample_type == "multiple":
           # Make sure sample is a list
           if (not isinstance(sample, list)):
               print "sample_type is set to multiple but sample looks loke this:"
               print sample
               print "Exiting..."
               sys.exit()               
       
       # Multiple friends
       elif sample_type == "multiple_friends":
           # Make sure sample is a list of lists with each len==2
           if ( (not isinstance(sample, list)) or                     # list
                (not all( [ isinstance(x, list) for x in sample])) or # of lists 
                (not all( [len(x)==2 for x in sample])) ):            # with 2 entries           
               print "sample_type is set to multiple_friends but sample looks loke this:"
               print sample
               print "Exiting..."
               sys.exit()               
    
       # refuse other sample_types
       else: 
           print "sample_type=", sample_type, " is invalid. Exiting.."
           sys.exit()
       # End of if/elif/else sample_type

       # Now we know that the sample argument has the proper content, take it
       self.sample_type = sample_type
       self.sample      = copy.deepcopy(sample)

       # Get all other variables
       self.x_variable  = x_variable         
       self.y_variable  = y_variable         
       self.cuts        = cuts

       self.nbins_x     = nbins_x
       self.min_x       = min_x
       self.max_x       = max_x
       self.nbins_y     = nbins_y
       self.min_y       = min_y
       self.max_y       = max_y
       self.log_y       = log_y

       self.ybars_are_sigma = ybars_are_sigma

       self.overlay_eff      = overlay_eff
       self.overlay_eff_file = overlay_eff_file

       self.do_legend       = do_legend
       self.legend_origin_x = legend_origin_x
       self.legend_origin_y = legend_origin_y
       self.legend_size_x   = legend_size_x
       self.legend_size_y   = legend_size_y

       self.name_prefix     = name_prefix

       self.eval_at         = eval_at

       # Autogenerate a name from sample and variable names
       if sample_type == "single":
           self.name        = "_".join([name_prefix, sample, x_variable, y_variable])
       elif sample_type == "friends":
           self.name        = "_".join([name_prefix, sample[0], sample[1],x_variable, y_variable])
       elif sample_type == "multiple":
           self.name        = "_".join([name_prefix, "multiple", sample[0], x_variable, y_variable])
       else:
           self.name        = "_".join([name_prefix, "multfriends", sample[0][0], sample[0][1], x_variable, y_variable])

       # And add object to master list
       self.li_all_plots.append( self )
    # End of Constructor
# End of class plotSettings definition

########################################
# Loop and make all plots
########################################

def makePlots( dic_files, 
               default_treename = "tree",
               extra_prefix = ""
           ):
    """ Draw all the plots defined using the plotSettings class.
    Argument:
    dic_files : (dictionary string/string) key: samplename
                                           value: path/to/root.file
    """                                           

    # Count the profiles so we can give them
    # unique names
    i_histo = 0
                             
    for plot in plotSettings.li_all_plots:

        plot_name = extra_prefix + plot.name

        # Initialize a square Canvas
        c = ROOT.TCanvas("","",800,800)

        # To be able to add multiple samples we have to have a loop here
        # (in the case of single/friends we just run one iteration)
        # transform the plot.sample member into something we can properly loop over
        # single          = [x]
        # friend          = [ [x0,x1] ] 
        # multiple        = [x, y, z]
        # multiple_friend = [ [x0,x1], [y0,y1], [z0,z1]]
        li_samples = []
        if plot.sample_type == "single" or plot.sample_type == "friends":
            li_samples.append( plot.sample )
        else:
            li_samples = plot.sample

        # Begin the sample llop
        for i_sample, sample in enumerate(li_samples):

            # Special treatment for sample:
            # if sample is a string: read it
            # if sample is a tuple: 
            #   read both
            #   order by run/event number
            #   make friends
            if isinstance( sample, str):
                # Sample is a string
                print "Opening: ", dic_files[  sample ], "for reading"

                # if the dic_files entry is a string: just open using default treename
                # otherwise treat it as tuple: filename, treename
                if isinstance( dic_files[ sample ], str):
                    input_file = ROOT.TFile( dic_files[ sample ], "READ" )  
                    input_tree = getattr(input_file, default_treename)            
                else:
                    input_file = ROOT.TFile( dic_files[ sample ][0], "READ" )  
                    input_tree = getattr(input_file, dic_files[ sample ][1])            
            else:
                # Sample is a tuple

                # open files
                input_file    = ROOT.TFile( dic_files[ sample[0] ], "READ" )  
                friend_file   = ROOT.TFile( dic_files[ sample[1] ], "READ" )  

                # Get the Trees
                input_tree  = input_file.Get(input_treename)
                friend_tree = friend_file.Get(input_treename)

                # Order the trees according to run/event number
                input_tree.BuildIndex( "RunNumber", "EventNumber")
                friend_tree.BuildIndex("RunNumber", "EventNumber")

                # befriend the trees
                input_tree.AddFriend(friend_tree,"friend")
            # done getting the input file(s)

            # Draw the 2d distribution
            htmp_name = "htmp"+str(i_histo)

            # build the drawing-string from a list
            # (easier to read than '+' clutter)
            li_draw_string = [plot.y_variable,
                              ":", plot.x_variable,                     
                              ">>", htmp_name,
                              "(",  str(int(plot.nbins_x)),
                              ",",  str(plot.min_x), 
                              ",",  str(plot.max_x),
                              ",",  str(int(plot.nbins_y)),
                              ",",  str(plot.min_y), 
                              ",",  str(plot.max_y),                     
                              ")"]
            draw_string = "".join(li_draw_string)

            if plot.sample_type == "multiple":
                input_tree.Draw( draw_string, plot.cuts[i_sample])
            else:
                input_tree.Draw( draw_string, plot.cuts)
            i_histo += 1

            # Retrieve 2d histogram and close input file
            htmp = ROOT.gDirectory.Get(htmp_name)
            htmp.SetDirectory(0)
            input_file.Close()

            # If we are proecessing the first (or only) sample
            # just rename it
            if i_sample == 0:
                h2d = htmp
            # Add later instances
            else:
                h2d.Add(htmp)

        # end of sample loop


        # Add a nice legend
        legend = ROOT.TLegend( plot.legend_origin_x,
                               plot.legend_origin_y,
                               plot.legend_origin_x + plot.legend_size_x,
                               plot.legend_origin_y + plot.legend_size_y )        
        legend.SetBorderSize(1) 
        legend.SetFillColor(0)
        legend.SetTextSize(0.05)      
        legend.SetBorderSize(0)

        # Make a TProfile from the TH2
        if plot.ybars_are_sigma:
            # Make the vertical bars show the standard deviation
            # (1,-1 are the default arguments to ProfileX, we 
            #   are just supplying them so we can also give the last option "s"
            #   which gives us the sigma)
            prof  = h2d.ProfileX(  str(i_histo), 1,-1,"s" )
        else:
            # Make the vertical bars show the error on the mean
            prof  = h2d.ProfileX(  str(i_histo))
        i_histo += 1 
    
        # Set the axis-range
        if not plot.min_x == plot.max_x:
            prof.SetAxisRange(plot.min_x, plot.max_x, "x")
        if not plot.min_y == plot.max_y:
            prof.SetAxisRange( plot.min_y, plot.max_y, "y") 

        # Add axis labels
        prof.GetXaxis().SetTitle(plot.x_variable) 
        prof.GetYaxis().SetTitle(plot.y_variable) 
        
        # Line width and Coloring
        prof.SetLineColor( ROOT.kRed) 
        prof.SetLineWidth(2)           
        
        # Draw the Profile
        tmp_h=prof.Clone()
        tmp_h.Draw("")   
        prof.SetFillColor( ROOT.kRed-4 )
        prof.SetFillStyle( 3253 )   
        prof.Draw("E2 SAME")
        prof.SetDirectory(0)

        
        f1 = ROOT.TF1("","1.05 + 0.00230*x  -6.44e-06*x^2")
        f1.SetRange(0,300)

        f2 = ROOT.TF1("","1.69  -0.00193*x + 6.09e-07*x^2",300,500)
        f2.SetRange(300,500)
        f2.SetLineColor(ROOT.kBlue)

        f3 = ROOT.TF1("","1.89  -0.00274*x + 1.43e-06*x^2",500,2000)
        f3.SetRange(500,2000)

        f = ROOT.TF1("fit_fun_qcd","[0]+[1]*sqrt(x)+[2]/x+[3]/(x*x)+[4]/(x*x*x)",220,2000)
        f.SetParameter(0,1)  
        f.SetParameter(1,1)  
        f.SetParameter(2,0.5)
        f.SetLineColor(ROOT.kRed)
        prof.Fit(f, "R")
        f.Print()

        f1.Draw("SAME")
        f2.Draw("SAME")
        f3.Draw("SAME")

        print "adding to dic:", prof
        dic_all_profiles[ plot_name ] = prof
    
        # Add to legend and draw it
        if plot.do_legend:
            if isinstance( plot.sample, str):
                legend.AddEntry( prof, plot.sample, "LF" )
            else:
                legend.AddEntry( prof, plot.sample[0]+" / "+plot.sample[1], "LF" )
                
        # Draw the legend
        if plot.do_legend:
            legend.Draw()

        # Save the results to a file (in different formats)
        OutputDirectoryHelper.ManyPrint( c, output_dir, plot_name.replace("/","_") )

    # end of plot-loop

    # Save profiles in pickle format to allow later access
    for k,v in dic_all_profiles.iteritems():
        print k,v
    pickle_out_file = open( extra_prefix + "profiles_out.pickle","w")
    pickle.dump( dic_all_profiles, pickle_out_file )
    pickle_out_file.close()


# end of def makePlots()
