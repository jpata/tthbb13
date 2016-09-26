#!/usr/bin/env python
"""
The backend helper scripts for comparing different
samples/cuts/variables from ROOT TTrees.
"""

########################################
# Imports and setup ROOT with style
########################################

import sys
import glob
import os
import ROOT

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
   import TTH.Plotting.Helpers.OutputDirectoryHelper as OutputDirectoryHelper
   from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
# Without CMSSW
else:
   import TTH.Plotting.python.Helpers.OutputDirectoryHelper as OutputDirectoryHelper
   from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle

# initializer: simple creation of bag-of-object classes
from Initializer import initializer

myStyle.SetPadLeftMargin(0.18)
myStyle.SetPadTopMargin(0.06)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


########################################
# class combinedPlot:
########################################

class combinedPlot:
   """Helper Class to Configure Plots"""
   
   # Static member variable. Add all objects to this list
   # to be able to draw them at once.
   li_combined_plots = []

   @initializer
   def __init__(self, 
                name,
                li_plots,
                nbins_x,
                min_x,
                max_x,
                max_y           = None,
                label_x         = "",
                label_y         = "",                
                axis_unit       = "",
                log_y           = False,
                normalize       = False,
                draw_legend     = True,
                legend_origin_x = 0.52,
                legend_origin_y = 0.7, 
                legend_size_x   = 0.2,
                legend_size_y   = -1,
                legend_text_size= 0.05,
                ):
      """ Constructor. Arguments:
      name            : (string) name for output file
      li_plots        : (list of plot objects) plots to combine
      nbins_x         : (int) number of bins to use for the x-axis
      min_x           : (float) minimal x-value
      max_x           : (float) maximal x-value
      max_y           : (float) maximal y-value
      label_x         : (string) label for the x-axis (unit is added)
      label_y         : (string) label for the y-axis ( / binwidth and unit are added) 
      axis_unit       : (string) unit for the x-axis (added to x- and y-labels)
      log_y           : (bool) logarithmic y-axis
      normalize       : (bool) area-normalize the graphs
      draw_legend     : (bool) draw the legend
      legend_origin_x : (float) position of the left? edge of the legend
      legend_origin_y : (float) position of the upper? edge of the legend
      legend_size_x   : (float) horizontal extension of the legen
      legend_size_y   : (float) vertical extension of the legend        
      legend_text_size: (float) text size of the legend        
      """

      # Add to the static member for keeping track of all objects
      self.__class__.li_combined_plots.append( self )
# End of class combinedPlot


class plot:
   @initializer
   def __init__(self, 
                name,
                var,
                cut,
                from_file,
                scale_cut="",
                fit = None,
             ):
      """ Constructor. Arguments:
      name        : (string) name to use for the legend
      var         : (string) variable to plot
      cut         : (string) cut to apply
      from_file   : (string, key in dic_files): which distribution to draw
      scale_cut   : (string) scale the histogram by 1/#entries passing the cut
      fit         : (TF1) function to fit. Warning: fitting only works if
                            exactly one plot is added to combinedPlots
      """
      pass
# End of class plot      


########################################
# Formatting/nice text defintions
########################################

# List of nice plotting colors
li_colors = [ROOT.kBlack, 
             ROOT.kRed, 
             ROOT.kBlue, 
             28, 
             #ROOT.kOrange, 
             ROOT.kGray, 
             ROOT.kGreen, 
             ROOT.kMagenta, 
             ROOT.kCyan,
             ROOT.kOrange+3
          ]*10

# List of nice line style
li_line_styles = [1]*len(li_colors) + [4]*len(li_colors) + [2]*len(li_colors)



c = ROOT.TCanvas("","",800,800)



########################################
# Create histograms
########################################

def createHistograms(dic_files):

    # Dictionary to store the histograms in
    # key: combinedPlot.name _ plot.name
    dic_histos = {}

    # Count the draw commands. This way wec can
    # assign unique names to the histograms:
    # htmpX
    i_draw = 0

    for cp in combinedPlot.li_combined_plots:

       for p in cp.li_plots:

           # open file and get tree

           # dic_files can have three different kinds of value
           # - a string: this is then a filename, use "tree" as treename
           # - a tuple: (filename, treename)
           # - a tuple: ('list of filenames', treename)
           # Using a Chain instead of a Tree of flexibility
           # ONLY FILENAME GIVEN
           if isinstance( dic_files[p.from_file], str ):
              input_tree = ROOT.TChain("tree")
              input_tree.Add(dic_files[p.from_file])
           # FILENAME AND TREENAME FIVEN
           elif isinstance( dic_files[p.from_file][0], str ):
              input_tree = ROOT.TChain(dic_files[p.from_file][1])
              input_tree.Add(dic_files[p.from_file][0])
           # LIST OF FILENAMES AND TREENAME FIVEN
           else:
               input_tree = ROOT.TChain(dic_files[p.from_file][1])
               
               if len(dic_files[p.from_file][0])==0:
                  print "Skipping", p.from_file
                  continue
               
               for fn in dic_files[p.from_file][0]:
                  input_tree.Add(fn)

           # end openeing input file
  
           # draw the variable and save into 
           # a histogram
           htmp_name = "htmp"+str(i_draw)

           # build the drawing-string from a list
           # (easier to read than '+' clutter)
           li_draw_string = [p.var, 
                             ">>", htmp_name,
                             "(",  str(int(cp.nbins_x)),
                             ",",  str(cp.min_x), 
                             ",",  str(cp.max_x),
                             ")"]

           draw_string = "".join(li_draw_string)
           # and actually draw
           
           input_tree.Draw( draw_string, p.cut )

           # Retrieve the histogram
           h = ROOT.gDirectory.Get(htmp_name).Clone()
           h.SetDirectory(0)

           # Optional: scale the histogram by 1/#entries passing a cut
           if not(p.scale_cut==""):
              htmp_cut_name= "htmp_cut"+str(i_draw)
              li_cut_string = [p.var, 
                                ">>", htmp_cut_name]

              cut_string = "".join(li_cut_string)
           
              input_tree.Draw( cut_string, p.scale_cut , "goff")

              # Retrieve the histogram
              h_cut = ROOT.gDirectory.Get(htmp_cut_name).Clone()
              h_cut.SetDirectory(0)
           
              n_entries_cut=h_cut.Integral()
              if(n_entries_cut==0):
                 print "No entry passing the cut"
              else:
                 h.Scale(1./n_entries_cut)

           i_draw += 1
        
           # Save the histogram in the dictionary
           dic_histos[cp.name + "_" + p.name] = h

       # end of variable loop
       # end of input_file loop

    return dic_histos
# end of createHistograms


########################################
# Draw Histograms
########################################

def drawHistograms(dic_histos, output_dir):

    # Define and create output directory
    OutputDirectoryHelper.CreateOutputDirs( output_dir )

    # Loop over combinedPlots
    for cp in combinedPlot.li_combined_plots:

        if cp.legend_size_y==-1:
           cp.legend_size_y = cp.legend_text_size * 1.25 * len(cp.li_plots)

        # Init the Legend
        leg = ROOT.TLegend( cp.legend_origin_x,
                            cp.legend_origin_y,
                            cp.legend_origin_x + cp.legend_size_x,
                            cp.legend_origin_y + cp.legend_size_y )
        leg.SetFillColor(0)
        leg.SetLineColor(0)
        leg.SetTextSize(cp.legend_text_size)
        leg.SetShadowColor(0)



        # Optional: normalize area to one
        if cp.normalize:
           for p in cp.li_plots:
              h = dic_histos[cp.name + "_" + p.name]
              if h.Integral():
                 h.Scale( 1/h.Integral())
                  
        # If not set, determine the y-range
        if cp.max_y == None:

            # Find the maximum y-value of the histgorams
            found_max = max([dic_histos[cp.name + "_" + p.name].GetMaximum() for p in cp.li_plots])

            # Set the y-range accordingly
            # extend furhter for logarithmic y-axes
            if cp.log_y:
                cp.max_y = 2*found_max
            else:
                cp.max_y = 1.25*found_max
                # End of cp.max_y == None

        # Loop over plots
        for i_p, p in enumerate(cp.li_plots):

            # Get the histogram
            h = dic_histos[cp.name + "_" + p.name]

            # Get colors/ls
            color = li_colors[i_p]
            ls    = li_line_styles[i_p]

            # Colorize/set linestyle
            h.SetLineWidth( 3 )
            h.SetLineColor( color )
            h.SetLineStyle( ls )      
            h.SetFillColor(0)

            # add to legend
            leg.AddEntry( h, p.name, "L")


            # Adjust y-range        
            if cp.log_y:
                h.SetAxisRange(0.0001, cp.max_y,"y")
                h.GetYaxis().SetLimits(0.01,cp.max_y)
                c.SetLogy(True)
            else:
                h.SetAxisRange(0., cp.max_y,"y")
                h.GetYaxis().SetLimits(0,cp.max_y)
                c.SetLogy(False)
                # end of y-range adjusting

            # reduce number of ticks on x-axis
            h.GetXaxis().SetNdivisions(5,5,0)

            # Label the x-axis
            # proper adding of [units] to the x-axis label
            bin_width = h.GetBinWidth( 1 )
            if cp.axis_unit:
                h.GetXaxis().SetTitle( cp.label_x + " (" + cp.axis_unit + ")")
            else:
                h.GetXaxis().SetTitle( cp.label_x )

            # Label the y-axis
            #h.GetYaxis().SetTitle( cp.label_y + " / "+str(bin_width) +" "+ cp.axis_unit)
            h.GetYaxis().SetTitle( cp.label_y)
            h.GetYaxis().SetTitleOffset(1.7)

            print p.name, h.GetEntries()


            # Optional fit            
            if p.fit is not None:
               h.Fit(p.fit, "R")               

            # Draw the histogram
            if i_p == 0:

                h.GetYaxis().SetNdivisions(410)

                h.Draw()

                txt = ROOT.TText()
                txt.SetTextFont(61)
                txt.SetTextSize(0.05)
                txt.DrawTextNDC(0.23, 0.88, "CMS")

                txt.SetTextFont(52)
                txt.SetTextSize(0.04)
                txt.DrawTextNDC(0.23, 0.84, "Simulation Preliminary")

                txt.SetTextFont(41)
                txt.DrawTextNDC(0.85, 0.95, "13 TeV")

            else:
                h.Draw("SAME")
        
         
        # Draw the legend
        if cp.draw_legend:
           leg.Draw()
        
        # Save the results to a file (in different formats)
        OutputDirectoryHelper.ManyPrint( c, output_dir, cp.name )

    # end of loop over combinedPlots
# end of drawHistograms


########################################
# doWork
########################################

def doWork(dic_files, output_dir):
   """ doWork: Inclusive function (histogram making+drawing) for local use"""

   # First create the histograms
   dic_histos = createHistograms(dic_files)

   # And draw them
   drawHistograms(dic_histos, output_dir)

# end of doWork
