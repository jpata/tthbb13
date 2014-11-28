#!/usr/bin/env python
"""
Plotting script that provides common functions needed to prepare
efficiency plots. Efficiencies are calculated using TGraphAsymmErrors
"""

########################################
# Import common Python modules
########################################

import array
import copy
import sys
import os
import pickle


########################################
# Import ROOT and prepare style
########################################

import ROOT
from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()

ROOT.TH1.SetDefaultSumw2()


########################################
# Import private support code
########################################

import TTH.Plotting.Helpers.OutputDirectoryHelper as OutputDirectoryHelper
import TTH.Plotting.Helpers.RebinHelper as RebinHelper


########################################
# Define and crate output directory
########################################

output_dir = "../OutputPlotsEffs/"

# Create directory and subdirectories for all filetypes
OutputDirectoryHelper.CreateOutputDirs( output_dir )



########################################
# Class plotList
########################################

class plotList:
    """ Helper class to store the options for multiple efficiency
    curves that are combined into one file/graph. Each efficiency is a
    plotSettings object.
    """
    
    # List that stores all plotList objects so we can produce them 
    # automatically
    li_all_plot_lists = []

    def __init__(self, 
                 li_plots,
                 outname,
                 min_x               = 0,
                 max_x               = 900,
                 nbins_x             = 100,
                 min_y               = 0,
                 max_y               = 1.1,
                 rebin               = [],
                 log_y               = False,
                 xtitle              = "p_{T, Gen.} [GeV]",
                 ytitle              = "Tagging Efficiency",
                 legend_origin_x     = 0.168,
                 legend_origin_y     = 0.87, 
                 legend_size_x       = 0.1,
                 legend_size_y       = 0.1,
                 do_legend           = False,
                 li_colors           = False,
                 y_label_offset      = False,
                 do_write_thresholds = False,
                 ):
        """ Constructor for plotList object.
        Arguments:
        li_plots        : [list] List of plotSettings objects to put
                                 into one graph
        outname         : [string] name of the output file 
                          (filetype suffix is added automatically)                          
        min_x           : [float]  Minimal x-value
        max_x           : [float]  Maximal x-value
        nbins_x         : [int]    Number of bins for x-axis        
        min_y           : [float]  Minimal y-value
        max_y           : [float]  Maximal y-value
        rebin           : [list of ints] If given: use for irregular binning of
                                         histograms prior to division
        log_y           : [bool]   Use a logarithmic scale for the y-axis
        legend_origin_x : [float] position of the left? edge of the legend
        legend_origin_y : [float] position of the upper? edge of the legend
        legend_size_x   : [float] horizontal extension of the legen
        legend_size_y   : [float] vertical extension of the legend        
        do_legend       : [bool] should we make a legend?
        li_colors       : [list] list to override the default color scheme
        y_label_offset  : [float] additional offset for the label
                          of the y-axis
       do_write_thresholds : [bool] write out the thresholds. This
       means for each efficiency curve the minimum and maximum values
       so that the efficiency exceeds given thresholds are
       recorded. Assumes that the different curves have labels of the
       form X..X' and mean(X,X') is used as x-value (the
       crossing-points are the y-values). X should for example be
       truetop_pt. This is mainly for use in PlotEff.py. The
       thresholds are saved as a dictionary in a pickle file (the
       format is described below where the dictionary is initialized)                         
        """
        
        # Take all the arguments given to the constructor
        self.li_plots = li_plots
        self.outname     = outname

        self.min_x       = min_x
        self.max_x       = max_x
        self.nbins_x     = nbins_x
        self.min_y       = min_y
        self.max_y       = max_y         
        self.log_y       = log_y

        #list: deep copy
        self.rebin       = [x for x in rebin] 

        self.xtitle      = xtitle
        self.ytitle      = ytitle

        self.legend_origin_x = legend_origin_x
        self.legend_origin_y = legend_origin_y
        self.legend_size_x   = legend_size_x
        self.legend_size_y   = legend_size_y
        self.do_legend       = do_legend
        
        self.y_label_offset = y_label_offset          
        
        self.do_write_thresholds = do_write_thresholds

        if not li_colors:
            self.li_colors = [ROOT.kRed,      ROOT.kBlue+1,     ROOT.kBlack, 
                              ROOT.kOrange-1, ROOT.kViolet+1,   ROOT.kGreen+1,
                              ROOT.kGray,     ROOT.kYellow,
                              ]*10
        else:
            self.li_colors = copy.deepcopy(li_colors)            

        self.li_marker_styles = [20,21,22,23,24]*100

        # And add the newly created object
        # to the master list
        self.li_all_plot_lists.append( self )
    # end of constructor
# end of plotList class defintion


########################################
# Class plotSettings
########################################

class plotSettings:
    """ Helper class to define an individual efficiency curve. Use
    together with plotList to create a proper graphic. 
    """

    def __init__(self, 
                 sample,
                 var,                
                 cuts_numerator,                   
                 cuts_denominator,                   
                 legend,
                 ev_weight = "(1)",
                 calc_99_point = False,
                 input_treename     = "SpartyJet_Tree"
                 # rebin = 0,
                 ):
       """ Constructor.
       sample        : [string] Name of the sample/version. Mapped to a file
                                via dic_files that is given as argument to
                                doPlots()
       var           : [string] Name of the variable to plot the efficiency for
       cuts_num      : [string] Cuts for the Numerator
       cuts_denom    : [string] Cuts for the Denominator
       legend        : [string] String to label this curve
       ev_weight     : [string] Branchname to look up per-event weights
       x_title       : [string] Label to use for the x-axis
       y_title       : [string] Label to use for the y-axis
       calc_99_point : [bool]   Calculate (and print to terminal) the x-axis
                                value for which a right-integrated efficiency
                                of >= 99% is reached.
       
       input_treename : [string] name of the tree in the input file
       """
       
       # Assign the arguments from the constructor
       self.sample     = sample
       self.var        = var
       self.cuts_num   = cuts_numerator         
       self.cuts_denom = cuts_denominator
       self.legend     = legend
       
       self.ev_weight = ev_weight


       self.calc_99_point = calc_99_point

       self.input_treename = input_treename
       # self.rebin       = rebin
       
    # end of constructor
# end of plotSettings class defintion


       
########################################
# Class doPlots
########################################

def doPlots( dic_files ):
    ''' Main worker function. Loop over all plotList objects in
    li_all_plot_lists and make all graphs. dic_files provides a
    mapping from samplenames to filenames.
    '''

    ########################################
    # Initialize some stuff
    ########################################

    # Count the draw commands. This way wec can
    # assign unique names to the histograms:
    # htmpX 
    i_draw = 0

    ########################################
    # loop over all plotList objects
    ########################################

    for plot_list in plotList.li_all_plot_lists:

        # Store all graphs in list - this avoids autodeletion and therefore
        # segfaults when drawing the legend
        li_gr = []

        # Initialize a square Canvas
        c = ROOT.TCanvas("","",600,600)
    
        # If needed: prepare a legend
        if plot_list.do_legend:
            legend = ROOT.TLegend( plot_list.legend_origin_x,
                                   plot_list.legend_origin_y,
                                   plot_list.legend_origin_x + plot_list.legend_size_x,
                                   plot_list.legend_origin_y + plot_list.legend_size_y )
            legend.SetBorderSize(1) 
            legend.SetFillColor(0)
            legend.SetTextSize(0.04)      
            legend.SetBorderSize(0)

        # If we want to write out thresholds, create the object
        # the structure is
        # pickle-file named thresholds-plot_list.outname.pickle
        # file containts one object, the dictionary dic_thresholds
        # key: threshold value (string "0.3", "0.4")
        # value: list: [ [xval, ymin, ymax], [xval,ymin,ymax],...]
        # xval is read fromt the legend of the plot
        # ymin and ymax are determined (these are actually x-values in the system 
        #    of the efficiency curve (-;
        if plot_list.do_write_thresholds:
            dic_thresholds = {}
            dic_thresholds["0.3"] = []
            dic_thresholds["0.4"] = []


        ########################################
        # loop over all plots in the list
        ########################################
        
        for i_plot, plot in enumerate(plot_list.li_plots):

          # Check if the sample is in dic_files
          if not plot.sample in dic_files.keys():
              print plot.sample, " not found in dic_files"
              print "Available keys are: "
              for k in dic_files.keys():
                  print "   ",k              
              print "Exiting..."
              sys.exit()
    
          # Open the file and retrieve tree for the sample
          input_file = ROOT.TFile( dic_files[ plot.sample ], "READ" )  
          input_tree = getattr(input_file, plot.input_treename)

          # draw the numerator and save into h_num
          htmp_name = "htmp"+str(i_draw)

          # Force TH1D or we'll get TH1F !!!
          tmp_num =  ROOT.TH1D(htmp_name,htmp_name,plot_list.nbins_x,plot_list.min_x,plot_list.max_x)

          # build the drawing-string from a list
          # (easier to read than '+' clutter)
          li_draw_string = [plot.var, 
                            ">>", htmp_name]
          # and actually draw
          # weight is applied by multiplying with cutstring
          draw_string = "".join(li_draw_string)
          input_tree.Draw( draw_string, plot.ev_weight+"*("+plot.cuts_num+")")
          h_num = ROOT.gDirectory.Get(htmp_name)
          h_num.SetDirectory(0)
          i_draw += 1

          # draw the denominator and save into h_denom
          htmp_name = "htmp"+str(i_draw)

          # Force TH1D or we'll get TH1F !!!
          tmp_denom =  ROOT.TH1D(htmp_name,htmp_name,plot_list.nbins_x,plot_list.min_x,plot_list.max_x)

          # build the drawing-string from a list
          # (easier to read than '+' clutter)
          li_draw_string = [plot.var, 
                            ">>", htmp_name]
          draw_string = "".join(li_draw_string)
          # and actually draw
          # weight is applied by multiplying with cutstring
          input_tree.Draw(  draw_string, plot.ev_weight+"*("+plot.cuts_denom+")") 
          h_denom = ROOT.gDirectory.Get(htmp_name)
          h_denom.SetDirectory(0)
          i_draw += 1
          
          input_file.Close()
          
          # Optional: Rebinning (with irregular bins)
          if len(plot_list.rebin):
              li_hs = RebinHelper.rebinHistos( [h_num, h_denom], plot_list.rebin)
              h_num   = li_hs[0]
              h_denom = li_hs[1]
    
                        
          max_bin = h_num.GetNbinsX()
          
          # Optional: calculate the x-value after which
          # the right-integrated efficiency exceeds 99%
          
          if plot.calc_99_point:

              max_bin = h_num.GetNbinsX()
              
              eff_bin = -1
              
              for i_bin in range(max_bin+2):
                  integral_num   = float(h_num.Integral(i_bin, max_bin+1))
                  integral_denom = float(h_denom.Integral(i_bin, max_bin+1))

                  if integral_denom >0:
                      if integral_num/integral_denom >= 0.99:
                          eff_bin= i_bin
                          break
              if eff_bin>=0:
                  print plot.sample, plot.cuts_num,">= 99% at: ", h_num.GetBinCenter(eff_bin) - h_num.GetBinWidth(eff_bin)/2.
              
          # y-scale logarithmic yes/no
          c.SetLogy( plot_list.log_y )

          # put the two plots into a list so we can apply some 
          # settings more quickly
          li_hs = [h_num, h_denom]

          # x- and y-range
          if not plot_list.min_x == plot_list.max_x:
              [h.SetAxisRange(plot_list.min_x, plot_list.max_x, "x") for h in li_hs]
          if not plot_list.min_y == plot_list.max_y:
              [h.SetAxisRange( plot_list.min_y, plot_list.max_y, "y") for h in li_hs]      

          # Empty the overflow
          h_num.SetBinContent( h_num.GetNbinsX()+1, 0)
          h_denom.SetBinContent( h_num.GetNbinsX()+1, 0)
                
           
          # turn on to see the content of num and denom!
          #for i_bin in range(max_bin+2):
          #    print i_bin, h_num.GetXaxis().GetBinCenter(i_bin), h_num.GetBinContent(i_bin), h_denom.GetBinContent( i_bin)

          # prepare the TGraph object and divide the histograms
          gr = ROOT.TGraphAsymmErrors( h_num.GetNbinsX() )
          gr.SetName( str(i_draw ) )
          gr.BayesDivide( h_num, h_denom)

          # Store the graph (otherwise we get segfaults from drawing the
          # legend) 
          li_gr.append(gr)

          # Make the graph look nice      
          color = plot_list.li_colors.pop(0)
          gr.SetMarkerColor( color )
          gr.SetLineColor( color )
          gr.SetLineWidth(2)
          gr.SetMarkerStyle( plot_list.li_marker_styles.pop(0) )
          
          # Write out the points where the efficiency exceeds given thresholds.
          # Explained in detail in the doc-string of plotList and above, where the
          # dic is initialized
          if plot_list.do_write_thresholds:

              # find out which efficiency curve we are looking at from the label
              # format (for example) 300..400
              [min_pt, max_pt] = plot.legend.split('..')
              min_pt = float(min_pt)
              max_pt = float(max_pt)
              mid_pt = (min_pt + max_pt)/2.
              
              # loop over the keys ie. "0.3", "0.4"
              for threshold_str in dic_thresholds.keys():
          
                  # convert to float
                  threshold = float(threshold_str)

                  # We will go from left to right.
                  #
                  # Note where we first exceed the threshold
                  # as left_edge (will be ymin in the output)
                  # Then where we first fall below as right_edge
                  # (will be y_max in the output)                  
                  passed_threshold = False
                  left_edge =   -1 
                  right_edge =  -1

                  # Loop over the points
                  for i_point in range(h_num.GetNbinsX()):

                      # ROOT.Double objects are necessary because
                      # GetPoint will fill them for us
                      x = ROOT.Double(0)
                      y = ROOT.Double(0)
                      
                      # get the point
                      gr.GetPoint(i_point, x, y)

                      # Check if we exceed the threshold (if we have not done before)
                      if not passed_threshold and y > threshold:
                          left_edge = x
                          passed_threshold = True
                      # If we were already above, check if we are below now
                      if passed_threshold and y < threshold:
                          right_edge = x    
                          break
                  # End of point loop

                  # if we were above and below again, record the point
                  if (not left_edge == -1 ) and (not right_edge == -1 ):
                      dic_thresholds[threshold_str].append( [mid_pt, 
                                                             float(left_edge), 
                                                             float(right_edge)])

              # end of loop over different thresholds
          # end of if do_write_thresholds
          if plot_list.do_legend:
              legend.AddEntry( gr, plot.legend, "LP" )   
                    
          # Do all the actual plotting when we are at the last graph
          # so file opening/closing does not confuse the poor 
          # histgrams and graphs
          if i_plot == len(plot_list.li_plots)-1:

              # Init the background TH2
              h_bg = ROOT.TH2F("","",100,plot_list.min_x,plot_list.max_x,100,plot_list.min_y,plot_list.max_y)

              # Make it look pretty
              h_bg.GetXaxis().SetLabelOffset(0.012)
              if plot_list.y_label_offset:
                  h_bg.GetYaxis().SetTitleOffset(plot_list.y_label_offset)
              h_bg.GetXaxis().SetTitle(plot_list.xtitle) 
              h_bg.GetYaxis().SetTitle(plot_list.ytitle)
              h_bg.GetXaxis().SetNdivisions(5,5,0)
              h_bg.Draw()

              # Draw the graphs
              for graph in li_gr:
                  graph.Draw("P SAME")      
                  
              # Add the legend
              if plot_list.do_legend:
                  legend.Draw()

              # Save the results to a file (in different formats)
              OutputDirectoryHelper.ManyPrint( c, output_dir, plot_list.outname.replace("/","_") )
              
              # If required - write out for which value the eff curves
              #  exceed a threshold
              if plot_list.do_write_thresholds:              
                  pickle_outfile = open( plot_list.outname + ".pickle", "w")
                  pickle.dump( dic_thresholds, pickle_outfile )
                  pickle_outfile.close()
              
          # End of if i_plot == last plot
       # End individual plot loop
    # End plot_list loop              
# End doPlots function
