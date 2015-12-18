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
ROOT.gStyle.SetPadRightMargin(0.14)
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


ROOT.gStyle.SetPadLeftMargin(0.25)
ROOT.gStyle.SetPadRightMargin(0.14)
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.26)

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
                li_vars,
                pickle_file_name,
                extra_text = [],
                error = False
   ):
      """ Constructor. Arguments:
      name                    : (string) name of the mutual information set=
      vars                    : list of variable (from VariableHelpers) objects 
      extra_test              : (list of strings) text to put on the canvas
      """
      pass

      
# end of class mi


def interpolate(gr, e=0.3):
   
   es_left = -1
   es_right = 1

   eb_left = -1
   eb_right = 1

   erlo_left = -1
   erlo_right = -1
   
   erhi_left = -1
   erhi_right = -1

   i_left = -1
   i_right = -1
 
   n = gr.GetN()
   
   for i in range(1, n):



      x = ROOT.Double()
      y = ROOT.Double()
      gr.GetPoint(i, x, y)

      print x

      if x <= e and abs(x-e) <= abs(es_left-e):
         i_left = i
         es_left = x
         eb_left = y

         erlo_left = gr.GetErrorYlow(i)
         erhi_left = gr.GetErrorYhigh(i)


      if x >= e and abs(x-e) <= abs(es_right-e):
         i_right = i
         es_right = x
         eb_right = y

         erlo_right = gr.GetErrorYlow(i)
         erhi_right = gr.GetErrorYhigh(i)
                  


   # TODO: Handle i_left == i_right

   # Linear interpolation: y = a*x +b
   # x: signal efficiency
   # y: bg rejection   
   b_eb = (eb_left - eb_right)/(es_left-es_right)   
   a_eb = eb_left - b_eb*es_left

   print "Interpolate: ", es_left, es_right

   return a_eb + e*b_eb, max(erlo_left, erlo_right), max(erhi_left, erhi_right), abs(es_left-es_right)
   
      
   

########################################
# Prepare Canvas
########################################

c = ROOT.TCanvas("","",800,800)
c.SetLogz(1)

########################################
# Make the Plots
########################################

def MakePlots(mis, extra_text = []):
              
   # Loop over the list of plots
   li_h2d = []

   for mi in mis:
      
      mi_result  = {}

      f_gr = open(mi.pickle_file_name, "rb")

      li = pickle.load(f_gr)
      di = {}
      for x in li:
         di[x[1]]=x[0]

      # Loop over pairs of variables:
      for ivar1, var1 in enumerate(mi.li_vars):

         mi_result[var1.name] = {}
         for ivar2, var2 in enumerate(mi.li_vars):

            key1 = variable.di[var1.name].pretty_name.replace("Mass", "m").replace("Mass", "m").replace("r_{cut}","rcut")
            key2 = variable.di[var2.name].pretty_name.replace("Mass", "m").replace("Mass", "m").replace("r_{cut}","rcut")

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



            
            eb, erlo, erhi,delta = interpolate(gr)
            mi_result[var1.name][var2.name] = 1/gr.Eval(0.3), max(erlo/(eb*eb), erhi/(eb*eb)), delta


         # End var2 loop
      # End var1 loop

      ROOT.gStyle.SetPalette(1)   
      
      h_mi = ROOT.TH2F("","", 
                       len(mi.li_vars), -0.5, -0.5 + len(mi.li_vars),
                       len(mi.li_vars), -0.5, -0.5 + len(mi.li_vars))      

      if mi.error:
         h_mi.SetMarkerSize(0.7)

      for ivar1, var1 in enumerate(mi.li_vars):         

         if var1.pretty_name_short:
            h_mi.GetXaxis().SetBinLabel(ivar1+1, var1.pretty_name_short)
            h_mi.GetYaxis().SetBinLabel(ivar1+1, var1.pretty_name_short)
         else:
            h_mi.GetXaxis().SetBinLabel(ivar1+1, var1.pretty_name)
            h_mi.GetYaxis().SetBinLabel(ivar1+1, var1.pretty_name)

         print var1, var1.pretty_name_short

         for ivar2, var2 in enumerate(mi.li_vars):

            if ivar2 > ivar1:
               continue

            h_mi.SetBinContent(ivar1+1, ivar2+1, mi_result[var1.name][var2.name][0])
            h_mi.SetBinError(ivar1+1, ivar2+1, mi_result[var1.name][var2.name][2]*100)


      h_mi.LabelsOption("v","X")
      h_mi.GetXaxis().SetLabelSize(0.040)
      h_mi.GetYaxis().SetLabelSize(0.040)
      h_mi.GetZaxis().SetLabelSize(0.032)
      
      h_mi.GetXaxis().SetNdivisions(0)
      h_mi.GetYaxis().SetNdivisions(0)
      
      if mi.error:
         draw_opts = "COLZ TEXT ERROR"
      else:
         draw_opts = "COLZ TEXT"

      h_mi.Draw(draw_opts)
      h_mi.Draw("sameaxis")

      txt = ROOT.TText()
      txt.SetTextFont(61)
      txt.SetTextSize(0.05)
      txt.DrawTextNDC(0.26, 0.89, "CMS")
   
      txt.SetTextFont(52)
      txt.SetTextSize(0.04)
      txt.DrawTextNDC(0.26, 0.85, "Simulation Preliminary")
      
      txt.SetTextFont(41)
      txt.DrawTextNDC(0.83, 0.96, "13 TeV")






      y_extra_text =  0.8
      
      l_txt = ROOT.TLatex()    
      l_txt.SetTextSize(0.03)

      for line in mi.extra_text:
         l_txt.DrawLatexNDC(0.26, y_extra_text, line)
         y_extra_text -= 0.035

      l_txt.SetTextSize(0.04)
      l_txt.SetTextAngle(90)
      l_txt.DrawLatexNDC(0.95, 0.8, "z-score")

      OutputDirectoryHelper.ManyPrint(c, output_dir, "{0}".format(mi.name))
   # End mi loop
# End MakePlots
            
            


