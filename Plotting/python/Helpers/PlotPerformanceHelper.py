#!/usr/bin/env python
"""
Helpers to calculate mutual information.

Inspired by 1408.3122
"""
 
########################################
# Imports and setup ROOT with style
########################################

import os
import sys
import math
import glob
import copy
import pickle

import ROOT

# initializer: simple creation of bag-of-object classes
from Initializer import initializer

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
   from TTH.Plotting.Helpers.PrepareRootStyle import myStyle
   from TTH.Plotting.Helpers.HistogramHelpers import Count
   import TTH.Plotting.Helpers.OutputDirectoryHelper as OutputDirectoryHelper
   from TTH.Plotting.gregor.TopTaggingVariables import *
# Without
else:
   from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
   from TTH.Plotting.python.Helpers.HistogramHelpers import Count
   import TTH.Plotting.python.Helpers.OutputDirectoryHelper as OutputDirectoryHelper
   from TTH.Plotting.python.gregor.TopTaggingVariables import *

ROOT.gStyle.SetPadLeftMargin(0.19)
ROOT.gStyle.SetPadRightMargin(0.16)
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.21)

ROOT.gStyle.SetPadTickX(0)
ROOT.gStyle.SetPadTickY(0)

ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()

ROOT.gStyle.SetPadTickX(0)
ROOT.gStyle.SetPadTickY(0)
ROOT.gStyle.SetTickLength(0)
ROOT.gStyle.SetTickLength(0,"y")


ROOT.gStyle.SetPadLeftMargin(0.33)
ROOT.gStyle.SetPadRightMargin(0.1)
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.34)

ROOT.gROOT.ForceStyle()


# Black-Body-Spectrum
# Reasons why it is nicer:
# http://root.cern.ch/drupal/content/rainbow-color-map
ROOT.gStyle.SetPalette(53)
# make the colors smoother
ROOT.gStyle.SetNumberContours(100)

ROOT.gStyle.SetPaintTextFormat("3.0f");

ROOT.TH1.SetDefaultSumw2()

ROOT.gErrorIgnoreLevel = 1

# Global variable to count drawn histograms for unique naming
i_draw = 0 

pickle_directory = "MIPickle"

########################################
# Define and crate output directory
########################################

output_dir = "/shome/gregor/new_results/OutputPlotPerformance/"

# Create directory and subdirectories for all filetypes
OutputDirectoryHelper.CreateOutputDirs( output_dir )


########################################
# Helper Classes
########################################

class mi():
   """ Helper class to store all information for a set of mutual information plots."""
   @initializer
   def __init__(self, 
                name,                
                sample_name_signal,
                sample_name_background,
                li_vars,
                fiducial_cut_signal     = "(1)",
                fiducial_cut_background = "(1)",
                diagonal_only = False,
                read_from_pickle = False,
                extra_text = [],
   ):
      """ Constructor. Arguments:
      name                    : (string) name of the mutual information set
      sample_name_signal      : (string) signal sample to process
      sample_name_background  : (string) background sample to process
      vars                    : list of variable (from VariableHelpers) objects 
      fiducial_cut_signal     : (string) fiducial cut (numerator and denominator)
      fiducial_cut_background : (string) fiducial cut (numerator and denominator)
      diagonal_only           : (bool) only check variable/truth, not variable pairs
      read_from_pickle        : (bool) use stored input
      extra_test              : (list of strings) text to put on the canvas
      """
      
      if ((fiducial_cut_signal == "(1)") and (not (fiducial_cut_background == "(1)")) or
          (not (fiducial_cut_signal == "(1)")) and (fiducial_cut_background == "(1)")):
         print "One of fiducial cut signal/background is (1). This is probably wrong!"
         sys.exit()

      
# end of class mi


########################################
# Prepare Canvas
########################################

c = ROOT.TCanvas("","",800,800)
c.SetLogz(1)

########################################
# Make the Plots
########################################

def MakePlots(mis, files, input_treename = 'tree', extra_text = []):

   # Some configuration
   f = 0.5 # fraction of signal events in combined samplke
           # Normalize samples so this value come out
           # Has the advantage that H(T)=1
           
   # Binning
   n_bins_one_var_one_sample = 400
   n_bins_one_var_two_sample = 400
   n_bins_two_var_one_sample = 60  # this is per axis, total bins -> n^2
   n_bins_two_var_two_sample = 60  # this is per axis, total bins -> n^2
   
   # Loop over the list of plots
   li_h2d = []

   for mi in mis:

      if mi.read_from_pickle:
      
        
         
         f_pickle = open("{0}/{1}_mi.pickle".format(pickle_directory,mi.name), "r")
         mi_result = pickle.load(f_pickle)
         f_pickle.close()
      
      else:
      
         # open files
         infile_sig = ROOT.TFile(files[mi.sample_name_signal])
         infile_bkg = ROOT.TFile(files[mi.sample_name_background])

         # Get the Trees
         input_tree_sig = infile_sig.Get(input_treename)
         input_tree_bkg = infile_bkg.Get(input_treename)

         # Count events
         passed_fiducial_sig = Count(input_tree_sig, mi.fiducial_cut_signal)
         passed_fiducial_bkg = Count(input_tree_bkg, mi.fiducial_cut_background)

         # Calculate overall additional background weight so that:
         # signal / signal+background = f
         # (set extra weight for signal to 1 as the overall normalization does not matter!)
         extra_weight_sig = 1.
         extra_weight_bkg = (passed_fiducial_sig - f * passed_fiducial_sig)/(f * passed_fiducial_bkg)

         mi_result  = {}

         f_gr = open("fixedR_MI_ROC_single_pt-300-to-470_out_gr.dat", "rb")
         f_gr2 = open("fixedR_MI_ROC_double_pt-300-to-470_out_gr.dat", "rb")
         li = pickle.load(f_gr)
         li.extend(pickle.load(f_gr2))
         di = {}
         for x in li:
            di[x[1]]=x[0]
                        
         # Loop over pairs of variables:
         for ivar1, var1 in enumerate(mi.li_vars):


            
            mi_result[var1.name] = {}
            for ivar2, var2 in enumerate(mi.li_vars):


               
               key1 = variable.di[var1.name].pretty_name.replace("Mass", "m").replace("Mass", "m")
               key2 = variable.di[var2.name].pretty_name.replace("Mass", "m").replace("Mass", "m")               

               if ivar1==ivar2:
                  gr = di[key1]                  
               else:
                  if key1 + " " + key2 in di.keys():
                     gr = di[key1 + " " + key2]
                  elif key2 + " " + key1 in di.keys():
                     gr = di[key2 + " " + key1]
                  else:
                     print "Did not find:", key1, key2, "in:"
                     for k in di.keys():
                        print k
                     sys.exit()

               mi_result[var1.name][var2.name] = 1/gr.Eval(0.3)

                  
                  

            # End var2 loop
         # End var1 loop

      ROOT.gStyle.SetPalette(1)   
      
      h_mi = ROOT.TH2F("","", 
                       len(mi.li_vars), -0.5, -0.5 + len(mi.li_vars),
                       len(mi.li_vars), -0.5, -0.5 + len(mi.li_vars))      

      for ivar1, var1 in enumerate(mi.li_vars):         

         h_mi.GetXaxis().SetBinLabel(ivar1+1, var1.pretty_name)
         h_mi.GetYaxis().SetBinLabel(ivar1+1, var1.pretty_name)

         for ivar2, var2 in enumerate(mi.li_vars):

            if ivar2 > ivar1:
               continue

            if mi.diagonal_only and ivar1 > ivar2:
               continue

            h_mi.SetBinContent(ivar1+1, ivar2+1, mi_result[var1.name][var2.name])


      h_mi.LabelsOption("v","X")
      h_mi.GetXaxis().SetLabelSize(0.038)
      h_mi.GetYaxis().SetLabelSize(0.038)
      h_mi.GetZaxis().SetLabelSize(0.03)
      
      h_mi.GetXaxis().SetNdivisions(0)
      h_mi.GetYaxis().SetNdivisions(0)

      draw_opts = "COLZ TEXT"
      
      if not mi.read_from_pickle:
         
         if not os.path.exists(pickle_directory):
            os.makedirs(pickle_directory)
         
         f_pickle = open("{0}/{1}_mi.pickle".format(pickle_directory, mi.name), "w")
         pickle.dump(mi_result, f_pickle)
         f_pickle.close()

      h_mi.Draw(draw_opts)
      h_mi.Draw("sameaxis")

      txt = ROOT.TText()
      txt.SetTextFont(61)
      txt.SetTextSize(0.05)
      txt.DrawTextNDC(0.35, 0.89, "CMS")
   
      txt.SetTextFont(52)
      txt.SetTextSize(0.04)
      txt.DrawTextNDC(0.35, 0.85, "Simulation Preliminary")
      
      txt.SetTextFont(41)
      txt.DrawTextNDC(0.83, 0.96, "13 TeV")



      y_extra_text =  0.8
      
      l_txt = ROOT.TLatex()    
      l_txt.SetTextSize(0.03)

      for line in mi.extra_text:
         l_txt.DrawLatexNDC(0.35, y_extra_text, line)
         y_extra_text -= 0.035




      if mi.diagonal_only:
         OutputDirectoryHelper.ManyPrint(c, output_dir, "{0}_diag".format(mi.name))
      else:
         OutputDirectoryHelper.ManyPrint(c, output_dir, "{0}".format(mi.name))
   # End mi loop
# End MakePlots
            
            


