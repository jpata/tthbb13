#!/usr/bin/env python
"""
Helpers to calculate mutual information.

Inspired by 1408.3122
"""

########################################
# Imports and setup ROOT with style
########################################

import math
import glob
import copy
import ROOT
from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle

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


ROOT.gErrorIgnoreLevel = 1

########################################
# Import private support code
########################################

# initializer: simple creation of bag-of-object classes
from Initializer import initializer

import TTH.Plotting.python.Helpers.OutputDirectoryHelper as OutputDirectoryHelper


########################################
# Define and crate output directory
########################################

output_dir = "OutputMutualInformation/"

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
                fiducial_cut = "(1)"):
      """ Constructor. Arguments:
      name                    : (string) name of the mutual information set
      sample_name_signal      : (string) signal sample to process
      sample_name_background  : (string) background sample to process
      vars                    : list of variable (from VariableHelpers) objects 
      fiducial_cut            : (string) fiducial cut (numerator and denominator)
      """
      pass
# end of class mi


########################################
# CalculateEntropy
########################################

def CalculateEntropy(h, verbose = False):
   """ Calculate and return the Shannon Entropy (base 2) of a histogram."""

   total = h.Integral()
   checksum = 0
   entropy = 0.
   for i_bin in range(1, h.GetXaxis().GetNbins()+1):
      width = h.GetBinWidth(i_bin)
      p = 1. * h.Integral(i_bin, i_bin)/total
      if p>0:
         checksum += p
         entropy -= p*math.log(p,2) 
         
   if verbose:
      print "checksum = ", checksum
   return entropy
# End of CalculateEntropy      


########################################
# Prepare Canvas
########################################

c = ROOT.TCanvas("","",800,800)


########################################
# Make the Plots
########################################

def MakePlots(mis, files, input_treename = 'tree'):

   # Some configuration
   f = 0.5 # fraction of signal events in combined samplke
           # Normalize samples so this value come out
           # Has the advantage that H(T)=1
           
   # Binning
   n_bins_one_var_one_sample = 400
   n_bins_one_var_two_sample = 400
   n_bins_two_var_one_sample = 50  # this is per axis, total bins -> n^2
   n_bins_two_var_two_sample = 50  # this is per axis, total bins -> n^2
   

   # Count the draw commands. This way wec can
   # assign unique names to the histograms:
   # htmpX
   i_draw = 0

   # Loop over the list of plots
   li_h2d = []

   for mi in mis:

      # open files
      infile_sig = ROOT.TFile(files[mi.sample_name_signal])
      infile_bkg = ROOT.TFile(files[mi.sample_name_background])

      # Get the Trees
      input_tree_sig = infile_sig.Get(input_treename)
      input_tree_bkg = infile_bkg.Get(input_treename)

      # Count events
      passed_fiducial_sig = input_tree_sig.Draw("(1)", mi.fiducial_cut)
      passed_fiducial_bkg = input_tree_bkg.Draw("(1)", mi.fiducial_cut)

      # Calculate overall additional background weight so that:
      # signal / signal+background = f
      # (set extra weight for signal to 1 as the overall normalization does not matter!)
      extra_weight_sig = 1.
      extra_weight_bkg = (passed_fiducial_sig - f * passed_fiducial_sig)/(f * passed_fiducial_bkg)

      mi_result  = {}

      # Loop over pairs of variables:
      for ivar1, var1 in enumerate(mi.li_vars):
         
         #cut_fraction[var1.name] = {}
         #corr_factor[var1.name] = {}

         for ivar2, var2 in enumerate(mi.li_vars):
            
            if ivar2 < ivar1:
               continue

            if ivar2 > ivar1:
               continue

               
            if (ivar1 == ivar2):

               # For the diagonal we want to calculate:
               # I(T;A) = H(sig,bkg)[A] - f * H(sig)[A] - (1-f) * H(bkg)[A]

               # Total cut is
               # fiducial + range(var1) + extra cut(var1) + range(var2) + extra_cut(var2)
               cut = "("
               cut += "({0})".format(mi.fiducial_cut)
               cut += "&&({0}>={1})".format(var1.name, var1.range_min)
               cut += "&&({0}<={1})".format(var1.name, var1.range_max)
               cut += "&&({0})".format(var1.extra_cut)
               cut += ")"

               cut_and_weight_sig = "{0}*{1}".format(cut, extra_weight_sig)
               cut_and_weight_bkg = "{0}*{1}".format(cut, extra_weight_bkg)

               
               # Build the temporary names for our histograms
               tmp_name_sig = "htmp{0}".format(i_draw)
               i_draw += 1
               tmp_name_bkg = "htmp{0}".format(i_draw)
               i_draw += 1
               tmp_name_sigbkg_sig = "htmp{0}".format(i_draw)
               i_draw += 1
               tmp_name_sigbkg_bkg = "htmp{0}".format(i_draw)
               i_draw += 1

               
               # build the drawing-strings
               # Signal Alone
               draw_string_sig = "{0}>>{1}({2},{3},{4})".format(var1.name, 
                                                                tmp_name_sig,
                                                                n_bins_one_var_one_sample,
                                                                var1.range_min,
                                                                var1.range_max)


               # Background Alone
               draw_string_bkg = "{0}>>{1}({2},{3},{4})".format(var1.name, 
                                                                tmp_name_bkg,
                                                                n_bins_one_var_one_sample,
                                                                var1.range_min,
                                                                var1.range_max)

               # Signal for signal+background
               # (need separate as the binning will be different from sig/bkg alone)
               draw_string_sigbkg_sig = "{0}>>{1}({2},{3},{4})".format(var1.name, 
                                                                       tmp_name_sigbkg_sig,
                                                                       n_bins_one_var_two_sample,
                                                                       var1.range_min,
                                                                       var1.range_max)


               # Background for signal+background
               # (need separate as the binning will be different from sig/bkg alone)
               draw_string_sigbkg_bkg = "{0}>>{1}({2},{3},{4})".format(var1.name, 
                                                                       tmp_name_sigbkg_bkg,
                                                                       n_bins_one_var_two_sample,
                                                                       var1.range_min,
                                                                       var1.range_max)

               # and actually draw      
               input_tree_sig.Draw(draw_string_sig, cut_and_weight_sig)
               input_tree_bkg.Draw(draw_string_bkg, cut_and_weight_bkg)
               input_tree_sig.Draw(draw_string_sigbkg_sig, cut_and_weight_sig)
               input_tree_bkg.Draw(draw_string_sigbkg_bkg, cut_and_weight_bkg)
               
               # Retrieve the histograms
               h_sig = getattr(ROOT, tmp_name_sig).Clone()
               h_bkg = getattr(ROOT, tmp_name_bkg).Clone()
               h_sigbkg_sig = getattr(ROOT, tmp_name_sigbkg_sig).Clone()
               h_sigbkg_bkg = getattr(ROOT, tmp_name_sigbkg_bkg).Clone()                              
               h_sig.SetDirectory(0)
               h_bkg.SetDirectory(0)
               h_sigbkg_sig.SetDirectory(0)
               h_sigbkg_bkg.SetDirectory(0)

               # Combine signal/background
               h_sigbkg = h_sigbkg_sig
               h_sigbkg.Add(h_sigbkg_bkg)

               # Calculate entropies
               entropy_sig = CalculateEntropy(h_sig)
               entropy_bkg = CalculateEntropy(h_bkg)
               entropy_sigbkg = CalculateEntropy(h_sigbkg)
               
               # Calculate Mutual Information
               I = entropy_sigbkg  - f * entropy_sig  - (1-f) * entropy_bkg
               
               print "H_sig = {0} \t H_bkg = {1} \t H_sigbkg = {2} \t I = {3}".format(entropy_sig,
                                                                                      entropy_bkg,
                                                                                      entropy_sigbkg,
                                                                                      I)
                              
               
               h_sig.Draw()
               h_bkg.Draw("SAME")

               clean_name = var1.name.replace("/","_")
               clean_name = clean_name.replace("(","")
               clean_name = clean_name.replace(")","")
               
               c.Print(clean_name + ".pdf")

               h_sigbkg.Draw()
               c.Print(clean_name + "_sum.pdf")

         # End var2 loop
      # End var1 loop


      ROOT.gStyle.SetPalette(1)   

         

   # End mi loop
# 
            
            


