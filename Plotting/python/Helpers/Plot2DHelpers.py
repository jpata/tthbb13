#!/usr/bin/env python
"""
Backend for making 2D plots.

Use NTuples as input.
"""

########################################
# Imports and setup ROOT with style
########################################

import math
import glob
import copy
import ROOT
from TTH.Plotting.Helpers.PrepareRootStyle import myStyle

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()

ROOT.gStyle.SetPadLeftMargin(0.16)
ROOT.gStyle.SetPadRightMargin(0.2)

# Black-Body-Spectrum
# Reasons why it is nicer:
# http://root.cern.ch/drupal/content/rainbow-color-map
ROOT.gStyle.SetPalette(53)
# make the colors smoother
ROOT.gStyle.SetNumberContours(100)

ROOT.TH1.SetDefaultSumw2()


########################################
# Import private support code
########################################

import TTH.Plotting.Helpers.OutputDirectoryHelper as OutputDirectoryHelper


########################################
# Define and crate output directory
########################################

output_dir = "OutputPlot2D/"

# Create directory and subdirectories for all filetypes
OutputDirectoryHelper.CreateOutputDirs( output_dir )


########################################
# Helper Class to Configure Plots
########################################

class plot():
   """ Helper class to store plotting options """
   def __init__(self, 
                name,
                var_x, 
                var_y, 
                cut,
                sample,
                nbins_x,
                min_x,
                max_x,
                nbins_y,
                min_y,
                max_y,
                min_z               = -1,
                max_z               = -1,
                log_z               = False,
                label_x             = "",
                label_y             = "",                
                axis_unit           = "",
                extra_text          = "",
                extra_text_x        = 0.2,
                extra_text_y        = 0.87,
                normalize           = False,
                htt_masscuts        = False,
                check_2dmasscut_eff = False,
                draw_opts           = "COLZ",
                li_integral_borders = [],                                
                ):
      """ Constructor. Arguments:
      name                : (string) name to use for writing the file
      var_x               : (string) variable to plot on the x-axis 
      var_y               : (string) variable to plot on the y-axis 
      cut                 : (string) cut to apply
      sample              : (string) sample to use for this plot 
                          : can also be a tuple of strings
                          : then the second entry of the tuple is added 
                          : as friend to the first
                          : (variables can be accesed with the prefix friend.)
      nbins_x             : (int) number of bins to use for the x-axis
      min_x               : (float) minimal x-value
      max_x               : (float) maximal x-value
      nbins_y             : (int) number of bins to use for the y-axis
      min_y               : (float) minimal y-value
      max_y               : (float) maximal y-value
      min_z               : (float) minimal z-value
      max_z               : (float) maximal z-value
      log_z               : (bool) logarithmic z-axis
      label_x             : (string) label for the x-axis (unit is added)
      label_y             : (string) label for the y-axis ( / binwidth and unit are added) 
      axis_unit           : (string) unit for the x-axis (added to x- and y-labels)
      extra_text          : (string) extra text to put on the plot (such as a label)
      extra_text_x        : (float) position of the left corner of the extra text
      extra_text_y        : (float) position of the top corner of the extra text
      normalize           : (bool) normalize the integral to 1
      htt_masscuts        : (bool) Overlay with mass-ratios for the HEPTopTagger
                            Useful for the atan/m23m123 plane
      check_2dmasscut_eff : (bool) Calculate which fraction of entries
                                   passes the cuts in the m23/m123 and 
                                   atan(m13/m12) plane for the HEPToptagger. 
                                   Please only use with 2d plots of these
                                   variables. Efficiency is printed to stdout.   
      draw_opts           : (string) draw options (defaults to COLZ)
      li_integral_borders : (list) integral borders. Example  [ [xmin_1,xmax_1,ymin_1, ymin_1], 
                                                                 [xmin_2,xmax_2,ymin_2, ymin_2]]
                                   
      """
      self.name                = name
      self.var_x               = var_x
      self.var_y               = var_y      
      self.cut                 = cut
      self.nbins_x             = nbins_x
      self.min_x               = min_x
      self.max_x               = max_x
      self.nbins_y             = nbins_y
      self.min_y               = min_y
      self.max_y               = max_y
      self.min_z               = min_z
      self.max_z               = max_z
      self.log_z               = log_z
      self.label_x             = label_x
      self.label_y             = label_y
      self.axis_unit           = axis_unit
      self.extra_text          = extra_text
      self.extra_text_x        = extra_text_x
      self.extra_text_y        = extra_text_y
      self.normalize           = normalize
      self.htt_masscuts        = htt_masscuts
      self.check_2dmasscut_eff = check_2dmasscut_eff
      self.draw_opts           = draw_opts

      self.li_integral_borders = copy.deepcopy(li_integral_borders)
      
      # Since sample can be a tuple or a string
      # make sure that we deep-copy the tuple
      if isinstance(sample, str):
         self.sample              = sample
      else:
         self.sample = [x for x in sample]
      # end of special treatment of sample

      

########################################
# Prepare Canvas
########################################

c = ROOT.TCanvas("","",800,800)



########################################
# Make the Plots
########################################

def MakePlots( 
   dic_input_files,
   li_plots,
   input_treename = 'tree'):
   ''' Create the requested 2D Plots.
   
   Arguments:
   dic_input_files: [dictionary] Locations of the input files.
                      keys: samplenames
                      values: path/to/root.file
                        
   li_plot        : [list] List of plot objects to drae (see class def above)                  
   input_treename : [string] name of the tree in the NTuples
   '''
   
   # Count the draw commands. This way wec can
   # assign unique names to the histograms:
   # htmpX
   i_draw = 0

   # Loop over the list of plots

   li_h2d = []

   for plot in li_plots:      

      # Special treatment for sample:
      # if sample is a string: read it
      # if sample is a tuple: 
      #   read both
      #   order by run/event number
      #   make friends
      if isinstance(plot.sample, str):
         # Sample is a string

         # open file
         infile = ROOT.TFile(dic_input_files[plot.sample])
         # Get the Tree
         input_tree = infile.Get(input_treename)
         print input_tree

      else:
         # Sample is a tuple

         # open files
         infile        = ROOT.TFile(dic_input_files[plot.sample[0]])
         infile_friend = ROOT.TFile(dic_input_files[plot.sample[1]])

         # Get the Trees
         input_tree        = infile.Get(input_treename)
         input_tree_friend = infile_friend.Get(input_treename)

         # Order the trees according to run/event number
         input_tree.BuildIndex("RunNumber", "EventNumber")
         input_tree_friend.BuildIndex("RunNumber", "EventNumber")
         
         # befriend the trees
         input_tree.AddFriend(input_tree_friend,"friend")
      # done getting the input file(s)

      # draw the variable and save into 
      # a histogram
      htmp_name = "htmp"+str(i_draw)

      # build the drawing-string from a list
      # (easier to read than '+' clutter)
      li_draw_string = [plot.var_y,
                        ":", plot.var_x,                     
                        ">>", htmp_name,
                        "(",  str(int(plot.nbins_x)),
                        ",",  str(plot.min_x), 
                        ",",  str(plot.max_x),
                        ",",  str(int(plot.nbins_y)),
                        ",",  str(plot.min_y), 
                        ",",  str(plot.max_y),                     
                        ")"]
      draw_string = "".join(li_draw_string)

      # and actually draw      
      print input_tree.Draw( draw_string, "("+plot.cut+")" )

      # Retrieve the histogram
      h_tmp = getattr(ROOT, htmp_name)
      h = h_tmp.Clone()
      h.SetDirectory(0)
      i_draw += 1

      print "Integral = ", h.Integral()

      if plot.normalize:
         h.Scale( 1./h.Integral() )

      # reduce number of ticks on x-axis
      h.GetXaxis().SetNdivisions(5,5,0)

      # Nice spacing between axis and labeks
      h.GetYaxis().SetTitleOffset(1.5)
      h.GetYaxis().SetTitleOffset(1.5)

      #stack.SetMinimum(0)
      h.GetYaxis().SetLimits(plot.min_y,plot.max_y)

      # Optional: set the range of the z-axis
      if (not plot.min_z  == -1) and (not plot.max_z == -1):
         print "Setting z range"
         h.GetZaxis().SetLimits(plot.min_z,plot.max_z)
         h.GetZaxis().SetRangeUser(plot.min_z,plot.max_z)
         
      c.SetLogz( plot.log_z )
          
      h.GetXaxis().SetTitle( plot.label_x )      
      h.GetYaxis().SetTitle( plot.label_y )      
      h.Draw( plot.draw_opts )
      
      # Get the number of bins for the two axes
      nbinsx = h.GetNbinsX()
      nbinsy = h.GetNbinsY()

      # Calculate and print integrals
      # loop over borders
      for integral_borders in plot.li_integral_borders:
         [xmin, xmax, ymin, ymax] = integral_borders
         xmin_bin =  h.GetXaxis().FindBin( xmin )
         xmax_bin =  h.GetXaxis().FindBin( xmax )
         ymin_bin =  h.GetXaxis().FindBin( ymin )
         ymax_bin =  h.GetXaxis().FindBin( ymax )
         print plot.name, "x=",str(xmin)+".."+str(xmax),"y=",str(ymin)+".."+str(ymax),":",h.Integral(xmin_bin,
                                                                                 xmax_bin,
                                                                                 ymin_bin,
                                                                                 ymax_bin)
      # End of loop over integral boardwers

     
      # Optional: Extra Text
      if plot.extra_text:
         l.DrawLatex( plot.extra_text_x, 
                      plot.extra_text_y, 
                      plot.extra_text )
                      
      
      # Save the results to a file (in different formats)
      OutputDirectoryHelper.ManyPrint( c, output_dir, plot.name )

      li_h2d.append( h)

   # End of loop over plots

   return li_h2d
   
# End of MakePlots()




