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
# Without
else:
   from TTH.Plotting.python.Helpers.PrepareRootStyle import myStyle
   from TTH.Plotting.python.Helpers.HistogramHelpers import Count
   import TTH.Plotting.python.Helpers.OutputDirectoryHelper as OutputDirectoryHelper

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

ROOT.gStyle.SetPaintTextFormat("3.2f");

ROOT.TH1.SetDefaultSumw2()

ROOT.gErrorIgnoreLevel = 1

# Global variable to count drawn histograms for unique naming
i_draw = 0 

pickle_directory = "MIPickle"

########################################
# Define and crate output directory
########################################

output_dir = "/shome/gregor/new_results/OutputMutualInformation/"

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
# CalculateEntropy
########################################

def CalculateEntropy(hs, n_extra_events, verbose = False):
   """ Calculate and return the Shannon Entropy (base 2) of histograms."""

   # As sometimes variables can be ill defined we need to be able to deal with 
   # -> multiple histograms: for example a TH2 and two TH1 where one variable each is ill-defined
   # an extra number of events that passed the fiducial cut but fail both variable selections

   # n_extra_events: If a variable is only defined for a subset of
   # events we need to take this into account when calculating the
   # entropy
   total = sum([h.Integral() for h in hs]) + n_extra_events
   checksum = 0
   entropy = 0.

   # Add events failing the cuts to entropy
   p_extra = 1. * n_extra_events / total
   if p_extra > 0:
      checksum += p_extra
      entropy -= p_extra*math.log(p_extra,2) 

   # Loop over histograms
   for h in hs:
      # 1d Histograms
      if type(h) in [ROOT.TH1F, ROOT.TH1D]:
         for i_bin in range(1, h.GetXaxis().GetNbins()+1):

            p = 1. * h.GetBinContent(i_bin)/total
            if p>0:
               checksum += p
               entropy -= p*math.log(p,2) 

      # 2d Histograms
      elif type(h) in [ROOT.TH2F, ROOT.TH2D]:

         for i_bin_x in range(1, h.GetXaxis().GetNbins()+1):
            for i_bin_y in range(1, h.GetYaxis().GetNbins()+1):

               p = 1. * h.GetBinContent(i_bin_x, i_bin_y)/total
               if p>0:
                  checksum += p
                  entropy -= p*math.log(p,2) 
      
      # Invalid Histogram type
      else:
         print "Ivalid type {0} for histogram in CalculateEntropy".format(type(h))
         print "Exiting"
      # End of handling different histogram dimensions
   # End of loop over histograms

   if verbose:
      print "checksum = ", checksum

   return entropy

# End of CalculateEntropy      


########################################
# MakeHistogram
########################################

def MakeHistogram(tree, variables, n_bins, cuts):
   """ Produce a histgrom for given variables, number of bins per axis
   and cuts from a ROOT tree"""

   global i_draw

   tmp_name = "htmp{0}".format(i_draw)
   i_draw += 1

   # Make a TH1
   if len(variables)==1:
      draw_string = "{0}>>{1}({2},{3},{4})".format(variables[0].name, 
                                                   tmp_name,
                                                   n_bins,
                                                   variables[0].range_min,
                                                   variables[0].range_max)

   # Make a TH2
   elif len(variables)==2:
      draw_string = "{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(variables[1].name,  # y
                                                                   variables[0].name,  # x
                                                                   tmp_name,
                                                                   n_bins,
                                                                   variables[0].range_min,
                                                                   variables[0].range_max,
                                                                   n_bins,
                                                                   variables[1].range_min,
                                                                   variables[1].range_max)

   # Otherwise fail
   else:
      print "Invalid number of variables: ", len(variables)
      print "Exiting.."
      sys.exit()

   tree.Draw(draw_string, cuts)
   h = getattr(ROOT, tmp_name).Clone()
   h.SetDirectory(0)

   return h
# End of MakeHistogram


########################################
# Prepare Canvas
########################################

c = ROOT.TCanvas("","",800,800)


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

         # Loop over pairs of variables:
         for ivar1, var1 in enumerate(mi.li_vars):

            mi_result[var1.name] = {}

            for ivar2, var2 in enumerate(mi.li_vars):

               # Diagonal
               if (ivar1 == ivar2):

                  # For the diagonal we want to calculate:
                  # I(T;A) = H(sig,bkg)[A] - f * H(sig)[A] - (1-f) * H(bkg)[A]

                  # Total cut is
                  # fiducial + range(var1) + extra cut(var1)
                  cut_and_weight_sig = "("
                  cut_and_weight_sig += "({0})".format(mi.fiducial_cut_signal)
                  cut_and_weight_sig += "&&({0}>={1})".format(var1.name, var1.range_min)
                  cut_and_weight_sig += "&&({0}<={1})".format(var1.name, var1.range_max)
                  cut_and_weight_sig += "&&({0})".format(var1.extra_cut)
                  cut_and_weight_sig += ")*{0}".format(extra_weight_sig)

                  cut_and_weight_bkg = "("
                  cut_and_weight_bkg += "({0})".format(mi.fiducial_cut_background)
                  cut_and_weight_bkg += "&&({0}>={1})".format(var1.name, var1.range_min)
                  cut_and_weight_bkg += "&&({0}<={1})".format(var1.name, var1.range_max)
                  cut_and_weight_bkg += "&&({0})".format(var1.extra_cut)
                  cut_and_weight_bkg += ")*{0}".format(extra_weight_bkg)

                  h_sig = MakeHistogram(input_tree_sig, [var1], n_bins_one_var_one_sample, cut_and_weight_sig)
                  h_bkg = MakeHistogram(input_tree_bkg, [var1], n_bins_one_var_one_sample, cut_and_weight_bkg)
                  h_sigbkg_sig = MakeHistogram(input_tree_sig, [var1], n_bins_one_var_two_sample, cut_and_weight_sig)
                  h_sigbkg_bkg = MakeHistogram(input_tree_bkg, [var1], n_bins_one_var_two_sample, cut_and_weight_bkg)

                  # Combine signal/background
                  h_sigbkg = h_sigbkg_sig
                  h_sigbkg.Add(h_sigbkg_bkg)

                  # Also count events that pass fiducial but not variable selection cuts
                  # Inverted cut is 
                  # fiducial + (! range(var1)) + (! extra cut(var1))
                  inverted_cut_and_weight_sig = "("
                  inverted_cut_and_weight_sig += "({0})".format(mi.fiducial_cut_signal)
                  inverted_cut_and_weight_sig += "&&(({0}<{1})".format(var1.name, var1.range_min)
                  inverted_cut_and_weight_sig += " ||({0}>{1})".format(var1.name, var1.range_max)
                  inverted_cut_and_weight_sig += " ||(!({0})))".format(var1.extra_cut)
                  inverted_cut_and_weight_sig += ")*{0}".format(extra_weight_sig)

                  inverted_cut_and_weight_bkg = "("
                  inverted_cut_and_weight_bkg += "({0})".format(mi.fiducial_cut_background)
                  inverted_cut_and_weight_bkg += "&&(({0}<{1})".format(var1.name, var1.range_min)
                  inverted_cut_and_weight_bkg += " ||({0}>{1})".format(var1.name, var1.range_max)
                  inverted_cut_and_weight_bkg += " ||(!({0})))".format(var1.extra_cut)
                  inverted_cut_and_weight_bkg += ")*{0}".format(extra_weight_bkg)

                  # Count events with inverted cut
                  cnt_inv_sig = Count(input_tree_sig, inverted_cut_and_weight_sig)
                  cnt_inv_bkg = Count(input_tree_bkg, inverted_cut_and_weight_bkg)

                  # Calculate entropies
                  entropy_sig = CalculateEntropy([h_sig], cnt_inv_sig)
                  entropy_bkg = CalculateEntropy([h_bkg], cnt_inv_bkg)
                  entropy_sigbkg = CalculateEntropy([h_sigbkg], cnt_inv_sig + cnt_inv_bkg)


               # Below Diagonal
               elif ivar2 < ivar1:

                  if mi.diagonal_only:
                     continue

                  # For the off-diagonal we want to calculate:
                  # I(T;A,B) = H(sig,bkg)[A,B] - f * H(sig)[A,B] - (1-f) * H(bkg)[A,B]

                  # We need to take into account 4 contributions
                  # var1 and var2 valid        -> cut, this is a TH2
                  # var1 valid, var2 invalid   -> inverted_cut_v2, this is a TH1
                  # var1 invalid, var2 valid   -> inverted_cut_v1, this is a TH1
                  # var1 invalid, var2 invalid -> inverted_cut_v1v2, this is number


                  # ----- var1 valid, var2 valid -----
                  # Total cut is
                  # fiducial + range(var1) + extra cut(var1) + range(var2) + extra_cut(var2)
                  cut_and_weight_sig = "("
                  cut_and_weight_sig += "({0})".format(mi.fiducial_cut_signal)
                  cut_and_weight_sig += "&&({0}>={1})".format(var1.name, var1.range_min)
                  cut_and_weight_sig += "&&({0}<={1})".format(var1.name, var1.range_max)
                  cut_and_weight_sig += "&&({0})".format(var1.extra_cut)
                  cut_and_weight_sig += "&&({0}>={1})".format(var2.name, var2.range_min)
                  cut_and_weight_sig += "&&({0}<={1})".format(var2.name, var2.range_max)
                  cut_and_weight_sig += "&&({0})".format(var2.extra_cut)
                  cut_and_weight_sig += ")*{0}".format(extra_weight_sig)

                  cut_and_weight_bkg = "("
                  cut_and_weight_bkg += "({0})".format(mi.fiducial_cut_background)
                  cut_and_weight_bkg += "&&({0}>={1})".format(var1.name, var1.range_min)
                  cut_and_weight_bkg += "&&({0}<={1})".format(var1.name, var1.range_max)
                  cut_and_weight_bkg += "&&({0})".format(var1.extra_cut)
                  cut_and_weight_bkg += "&&({0}>={1})".format(var2.name, var2.range_min)
                  cut_and_weight_bkg += "&&({0}<={1})".format(var2.name, var2.range_max)
                  cut_and_weight_bkg += "&&({0})".format(var2.extra_cut)
                  cut_and_weight_bkg += ")*{0}".format(extra_weight_bkg)

                  h_sig = MakeHistogram(input_tree_sig, [var1, var2], n_bins_two_var_one_sample, cut_and_weight_sig)
                  h_bkg = MakeHistogram(input_tree_bkg, [var1, var2], n_bins_two_var_one_sample, cut_and_weight_bkg)
                  h_sigbkg_sig = MakeHistogram(input_tree_sig, [var1, var2], n_bins_two_var_two_sample, cut_and_weight_sig)
                  h_sigbkg_bkg = MakeHistogram(input_tree_bkg, [var1, var2], n_bins_two_var_two_sample, cut_and_weight_bkg)

                  # Combine signal/background
                  h_sigbkg = h_sigbkg_sig
                  h_sigbkg.Add(h_sigbkg_bkg)


                  # ----- var1 invalid, var2 valid -----
                  # inverted cut var1  is
                  # fiducial AND (!range(var1) OR !extra_cut(var1)) AND (range(var2) AND extra_cut(var2))
                  cut_and_weight_sig_inv_var1 = "("
                  cut_and_weight_sig_inv_var1 += "({0})".format(mi.fiducial_cut_signal)
                  cut_and_weight_sig_inv_var1 += "&&(({0}<{1})".format(var1.name, var1.range_min)
                  cut_and_weight_sig_inv_var1 += " ||({0}>{1})".format(var1.name, var1.range_max)
                  cut_and_weight_sig_inv_var1 += " ||(!({0})))".format(var1.extra_cut)
                  cut_and_weight_sig_inv_var1 += "&&({0}>={1})".format(var2.name, var2.range_min)
                  cut_and_weight_sig_inv_var1 += "&&({0}<={1})".format(var2.name, var2.range_max)
                  cut_and_weight_sig_inv_var1 += "&&(({0}))".format(var2.extra_cut)
                  cut_and_weight_sig_inv_var1 += ")*{0}".format(extra_weight_sig)

                  cut_and_weight_bkg_inv_var1 = "("
                  cut_and_weight_bkg_inv_var1 += "({0})".format(mi.fiducial_cut_background)
                  cut_and_weight_bkg_inv_var1 += "&&(({0}<{1})".format(var1.name, var1.range_min)
                  cut_and_weight_bkg_inv_var1 += " ||({0}>{1})".format(var1.name, var1.range_max)
                  cut_and_weight_bkg_inv_var1 += " ||(!({0})))".format(var1.extra_cut)
                  cut_and_weight_bkg_inv_var1 += "&&({0}>={1})".format(var2.name, var2.range_min)
                  cut_and_weight_bkg_inv_var1 += "&&({0}<={1})".format(var2.name, var2.range_max)
                  cut_and_weight_bkg_inv_var1 += "&&(({0}))".format(var2.extra_cut)
                  cut_and_weight_bkg_inv_var1 += ")*{0}".format(extra_weight_bkg)

                  h_sig_inv1 = MakeHistogram(input_tree_sig, [var2], n_bins_one_var_one_sample, cut_and_weight_sig_inv_var1)
                  h_bkg_inv1 = MakeHistogram(input_tree_bkg, [var2], n_bins_one_var_one_sample, cut_and_weight_bkg_inv_var1)
                  h_sigbkg_sig_inv1 = MakeHistogram(input_tree_sig, [var2], n_bins_one_var_two_sample, cut_and_weight_sig_inv_var1)
                  h_sigbkg_bkg_inv1 = MakeHistogram(input_tree_bkg, [var2], n_bins_one_var_two_sample, cut_and_weight_bkg_inv_var1)

                  # Combine signal/background
                  h_sigbkg_inv1 = h_sigbkg_sig_inv1
                  h_sigbkg_inv1.Add(h_sigbkg_bkg_inv1)


                  # ----- var1 valid, var2 invalid -----
                  # fiducial AND (range(var1) AND extra_cut(var1)) AND (!range(var2) OR !extra_cut(var2))
                  cut_and_weight_sig_inv_var2 = "("
                  cut_and_weight_sig_inv_var2 += "({0})".format(mi.fiducial_cut_signal)
                  cut_and_weight_sig_inv_var2 += "&&({0}>={1})".format(var1.name, var1.range_min)
                  cut_and_weight_sig_inv_var2 += "&&({0}<={1})".format(var1.name, var1.range_max)
                  cut_and_weight_sig_inv_var2 += "&&(({0}))".format(var1.extra_cut)
                  cut_and_weight_sig_inv_var2 += "&&(({0}<{1})".format(var2.name, var2.range_min)
                  cut_and_weight_sig_inv_var2 += " ||({0}>{1})".format(var2.name, var2.range_max)
                  cut_and_weight_sig_inv_var2 += " ||(!({0})))".format(var2.extra_cut)
                  cut_and_weight_sig_inv_var2 += ")*{0}".format(extra_weight_sig)

                  cut_and_weight_bkg_inv_var2 = "("
                  cut_and_weight_bkg_inv_var2 += "({0})".format(mi.fiducial_cut_background)
                  cut_and_weight_bkg_inv_var2 += "&&({0}>={1})".format(var1.name, var1.range_min)
                  cut_and_weight_bkg_inv_var2 += "&&({0}<={1})".format(var1.name, var1.range_max)
                  cut_and_weight_bkg_inv_var2 += "&&(({0}))".format(var1.extra_cut)
                  cut_and_weight_bkg_inv_var2 += "&&(({0}<{1})".format(var2.name, var2.range_min)
                  cut_and_weight_bkg_inv_var2 += " ||({0}>{1})".format(var2.name, var2.range_max)
                  cut_and_weight_bkg_inv_var2 += " ||(!({0})))".format(var2.extra_cut)
                  cut_and_weight_bkg_inv_var2 += ")*{0}".format(extra_weight_bkg)

                  h_sig_inv2 = MakeHistogram(input_tree_sig, [var1], n_bins_one_var_one_sample, cut_and_weight_sig_inv_var2)
                  h_bkg_inv2 = MakeHistogram(input_tree_bkg, [var1], n_bins_one_var_one_sample, cut_and_weight_bkg_inv_var2)
                  h_sigbkg_sig_inv2 = MakeHistogram(input_tree_sig, [var1], n_bins_one_var_two_sample, cut_and_weight_sig_inv_var2)
                  h_sigbkg_bkg_inv2 = MakeHistogram(input_tree_bkg, [var1], n_bins_one_var_two_sample, cut_and_weight_bkg_inv_var2)

                  h_sigbkg_inv2 = h_sigbkg_sig_inv2
                  h_sigbkg_inv2.Add(h_sigbkg_bkg_inv2)


                  # ----- var1 invalid, var2 invalid -----
                  # inverted cut  is
                  # fiducial AND (!range(var1) OR !extra cut(var1)) AND (!range(var2) OR !extra_cut(var2))
                  inverted_cut_and_weight_sig = "("
                  inverted_cut_and_weight_sig += "({0})".format(mi.fiducial_cut_signal)
                  inverted_cut_and_weight_sig += "&&(({0}<{1})".format(var1.name, var1.range_min)
                  inverted_cut_and_weight_sig += " ||({0}>{1})".format(var1.name, var1.range_max)
                  inverted_cut_and_weight_sig += " ||(!({0})))".format(var1.extra_cut)
                  inverted_cut_and_weight_sig += "&&(({0}<{1})".format(var2.name, var2.range_min)
                  inverted_cut_and_weight_sig += " ||({0}>{1})".format(var2.name, var2.range_max)
                  inverted_cut_and_weight_sig += " ||(!({0})))".format(var2.extra_cut)
                  inverted_cut_and_weight_sig += ")*{0}".format(extra_weight_sig)

                  inverted_cut_and_weight_bkg = "("
                  inverted_cut_and_weight_bkg += "({0})".format(mi.fiducial_cut_background)
                  inverted_cut_and_weight_bkg += "&&(({0}<{1})".format(var1.name, var1.range_min)
                  inverted_cut_and_weight_bkg += " ||({0}>{1})".format(var1.name, var1.range_max)
                  inverted_cut_and_weight_bkg += " ||(!({0})))".format(var1.extra_cut)
                  inverted_cut_and_weight_bkg += "&&(({0}<{1})".format(var2.name, var2.range_min)
                  inverted_cut_and_weight_bkg += " ||({0}>{1})".format(var2.name, var2.range_max)
                  inverted_cut_and_weight_bkg += " ||(!({0})))".format(var2.extra_cut)
                  inverted_cut_and_weight_bkg += ")*{0}".format(extra_weight_bkg)

                  cnt_inv_sig = Count(input_tree_sig, inverted_cut_and_weight_sig)
                  cnt_inv_bkg = Count(input_tree_bkg, inverted_cut_and_weight_bkg)               

                  # ----- Put everything together -----
                  # Calculate entropies
                  entropy_sig = CalculateEntropy([h_sig, h_sig_inv1, h_sig_inv2], cnt_inv_sig)
                  entropy_bkg = CalculateEntropy([h_bkg, h_bkg_inv1, h_bkg_inv2], cnt_inv_bkg)
                  entropy_sigbkg = CalculateEntropy([h_sigbkg, h_sigbkg_inv1, h_sigbkg_inv2], cnt_inv_sig + cnt_inv_bkg)

               # Above Diagonal
               else:
                  continue
               # End of Diagonal vs Off-Diagonal difference

               # Calculate Mutual Information
               I = entropy_sigbkg  - f * entropy_sig  - (1-f) * entropy_bkg

               print "{0} / {1}:\t H_sig = {2:.3f} \t H_bkg = {3:.3f} \t H_sigbkg = {4:.3f} \t I = {5:.3f}".format(var1.name,
                                                                                                   var2.name,
                                                                                                   entropy_sig,
                                                                                                   entropy_bkg,
                                                                                                   entropy_sigbkg,
                                                                                                   I)

               mi_result[var1.name][var2.name] = I
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
         OutputDirectoryHelper.ManyPrint(c, output_dir, "{0}_mi_diag".format(mi.name))
      else:
         OutputDirectoryHelper.ManyPrint(c, output_dir, "{0}_mi".format(mi.name))
   # End mi loop
# End MakePlots
            
            


