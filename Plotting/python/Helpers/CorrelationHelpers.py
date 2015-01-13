#!/usr/bin/env python
"""
"""

########################################
# Imports and setup ROOT with style
########################################

import math
import glob
import copy
import os

import ROOT

# initializer: simple creation of bag-of-object classes
from Initializer import initializer

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
   from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
   from TTH.Plotting.Helpers.HistogramHelpers import Count
   import TTH.Plotting.Helpers.OutputDirectoryHelper as OutputDirectoryHelper
else:
   from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
   from TTH.Plotting.python.Helpers.HistogramHelpers import Count
   import TTH.Plotting.python.Helpers.OutputDirectoryHelper as OutputDirectoryHelper

ROOT.gStyle.SetPadLeftMargin(0.2)
ROOT.gStyle.SetPadRightMargin(0.1)
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.25)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()

ROOT.gStyle.SetPadLeftMargin(0.26)
ROOT.gStyle.SetPadRightMargin(0.1)
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.29)

ROOT.gROOT.ForceStyle()


# Black-Body-Spectrum
# Reasons why it is nicer:
# http://root.cern.ch/drupal/content/rainbow-color-map
ROOT.gStyle.SetPalette(53)
# make the colors smoother
ROOT.gStyle.SetNumberContours(100)

ROOT.gStyle.SetPaintTextFormat("3.2f");

ROOT.TH1.SetDefaultSumw2()


########################################
# Define and crate output directory
########################################

output_dir = "OutputCorrelations/"

# Create directory and subdirectories for all filetypes
OutputDirectoryHelper.CreateOutputDirs( output_dir )


########################################
# Helper Classes
########################################

class corr():
   """ Helper class to store all information for a set of correlation tests."""
   @initializer
   def __init__(self, 
                name,                
                sample_name,
                li_vars,
                fiducial_cut = "(1)"):
      """ Constructor. Arguments:
      name                : (string) name of the corr
      sample_name         : (string) sample to process
      vars                : list of variable (from VariableHelpers) objects 
      fiducial_cut        : (string) fiducial cut (numerator and denominator)
      """
      pass
# end of class var
      

########################################
# Prepare Canvas
########################################

c = ROOT.TCanvas("","",800,800)


########################################
# Make the Plots
########################################

def MakePlots(corrs, files, input_treename = 'tree'):
   
   # Count the draw commands. This way wec can
   # assign unique names to the histograms:
   # htmpX
   i_draw = 0

   # Loop over the list of plots

   li_h2d = []

   for corr in corrs:

      # open file
      infile = ROOT.TFile(files[corr.sample_name])
      # Get the Tree
      input_tree = infile.Get(input_treename)

      all_events = input_tree.GetEntries()
      passed_fiducial = Count(input_tree, corr.fiducial_cut)

      cut_fraction = {}
      corr_factor = {}

      # Loop over pairs of variables:
      for ivar1, var1 in enumerate(corr.li_vars):
         
         cut_fraction[var1.name] = {}
         corr_factor[var1.name] = {}

         for ivar2, var2 in enumerate(corr.li_vars):
            
            if ivar2 > ivar1:
               continue

            # Total cut is
            # fiducial + range(var1) + extra cut(var1) + range(var2) + extra_cut(var2)
            cut = "("
            cut += "({0})".format(corr.fiducial_cut)
            cut += "&&({0}>={1})".format(var1.name, var1.range_min)
            cut += "&&({0}<={1})".format(var1.name, var1.range_max)
            cut += "&&({0})".format(var1.extra_cut)
            cut += "&&({0}>={1})".format(var2.name, var2.range_min)
            cut += "&&({0}<={1})".format(var2.name, var2.range_max)
            cut += "&&({0})".format(var2.extra_cut)
            cut += ")"
            
            passed_cut = Count(input_tree, cut)
            cut_fraction[var1.name][var2.name] = 1.*passed_cut/passed_fiducial
            
            # draw the variable and save into 
            # a histogram
            htmp_name = "htmp"+str(i_draw)

            # build the drawing-string from a list
            # (easier to read than '+' clutter)
            li_draw_string = [var2.name,
                              ":", var1.name,                     
                              ">>", htmp_name,
                              "(",  "100",
                              ",",  str(var1.range_min), 
                              ",",  str(var1.range_max),
                              ",",  "100",
                              ",",  str(var2.range_min),
                              ",",  str(var2.range_max),
                              ")"]
            draw_string = "".join(li_draw_string)

            # and actually draw      
            input_tree.Draw( draw_string, cut )

            # Retrieve the histogram
            h_tmp = getattr(ROOT, htmp_name)
            h = h_tmp.Clone()
            h.SetDirectory(0)
            i_draw += 1

            corr_factor[var1.name][var2.name] = abs(h.GetCorrelationFactor())

            # reduce number of ticks on x-axis
            h.GetXaxis().SetNdivisions(5,5,0)

            # Nice spacing between axis and labeks
            h.GetYaxis().SetTitleOffset(1.5)
            h.GetYaxis().SetTitleOffset(1.5)

            h.GetXaxis().SetTitle( var1.name )
            h.GetYaxis().SetTitle( var2.name )
            h.Draw( "COLZ" )
      
            OutputDirectoryHelper.ManyPrint( c, output_dir, "{0}_{1}_{2}_{3}".format(corr.name, 
                                                                                     corr.sample_name,
                                                                                     var1.name.replace("/","_"), 
                                                                                     var2.name.replace("/","_")))
         # End var2 loop
      # End var1 loop


      ROOT.gStyle.SetPalette(1)   

      h_cut_fraction = ROOT.TH2F("","", 
                                 len(corr.li_vars), -0.5, -0.5 + len(corr.li_vars),
                                 len(corr.li_vars), -0.5, -0.5 + len(corr.li_vars))

      h_corr_factor = ROOT.TH2F("","", 
                                len(corr.li_vars), -0.5, -0.5 + len(corr.li_vars),
                                len(corr.li_vars), -0.5, -0.5 + len(corr.li_vars))

      for ivar1, var1 in enumerate(corr.li_vars):         

         h_cut_fraction.GetXaxis().SetBinLabel(ivar1+1, var1.pretty_name)
         h_cut_fraction.GetYaxis().SetBinLabel(ivar1+1, var1.pretty_name)

         h_corr_factor.GetXaxis().SetBinLabel(ivar1+1, var1.pretty_name)
         h_corr_factor.GetYaxis().SetBinLabel(ivar1+1, var1.pretty_name)


         for ivar2, var2 in enumerate(corr.li_vars):

            if ivar2 > ivar1:
               continue

            h_cut_fraction.SetBinContent(ivar1+1, ivar2+1, cut_fraction[var1.name][var2.name])
            h_corr_factor.SetBinContent(ivar1+1, ivar2+1, corr_factor[var1.name][var2.name])

            
      for h2d in [h_cut_fraction, h_corr_factor]:         
         h2d.LabelsOption("v","X")
         h2d.GetXaxis().SetLabelSize(0.035)
         h2d.GetYaxis().SetLabelSize(0.035)
         h2d.GetZaxis().SetLabelSize(0.03)

      if corr.name == "all":
         draw_opts = "COLZ"
      else:
         draw_opts = "COLZ TEXT"

      

      h_cut_fraction.Draw( draw_opts )
      OutputDirectoryHelper.ManyPrint(c, output_dir, "{0}_{1}_cut_fraction".format(corr.name, corr.sample_name))

      h_corr_factor.Draw( draw_opts )
      OutputDirectoryHelper.ManyPrint(c, output_dir, "{0}_{1}_corr_factor".format(corr.name, corr.sample_name))
         

   # End corr loop
# 
            
            


