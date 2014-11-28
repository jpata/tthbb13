#!/usr/bin/env python
"""
Set a nice ROOT Style.
Based on old ATLAS Style.

Usage in plotting scripts:
  import ROOT
  from PrepareRootStyle import myStyle
  ROOT.gROOT.SetStyle("myStyle")
  ROOT.gROOT.ForceStyle()
"""


import ROOT
ROOT.gStyle.SetPalette(1)

myStyle = ROOT.TStyle("myStyle","myStyle")

icol=0 # WHITE
myStyle.SetFrameBorderMode(icol)
myStyle.SetFrameFillColor(icol)
myStyle.SetCanvasBorderMode(icol)
myStyle.SetCanvasColor(icol)
myStyle.SetPadBorderMode(icol)
myStyle.SetPadColor(icol)
myStyle.SetStatColor(icol)

# set the paper & margin sizes
myStyle.SetPaperSize(20,26)

# set margin sizes
myStyle.SetPadTopMargin(0.05)
myStyle.SetPadRightMargin(0.05)
myStyle.SetPadBottomMargin(0.16)
myStyle.SetPadLeftMargin(0.16)

# set title offsets (for axis label)
myStyle.SetTitleXOffset(1.45)
myStyle.SetTitleYOffset(1.4)

# Helvetica
font=42 
tsize=0.05
myStyle.SetTextFont(font)

myStyle.SetTextSize(tsize)
myStyle.SetLabelFont(font,"x")
myStyle.SetTitleFont(font,"x")
myStyle.SetLabelFont(font,"y")
myStyle.SetTitleFont(font,"y")
myStyle.SetLabelFont(font,"z")
myStyle.SetTitleFont(font,"z")

myStyle.SetLabelSize(tsize,"x")
myStyle.SetTitleSize(tsize,"x")
myStyle.SetLabelSize(tsize,"y")
myStyle.SetTitleSize(tsize,"y")
myStyle.SetLabelSize(tsize,"z")
myStyle.SetTitleSize(tsize,"z")

# use bold lines and markers
myStyle.SetMarkerStyle(20)
myStyle.SetMarkerSize(1.2)
myStyle.SetHistLineWidth(2)
myStyle.SetLineStyleString(2,"[12 12]") # postscript dashes

# get rid of X error bars 
#myStyle.SetErrorX(0.001)
# get rid of error bar caps
myStyle.SetEndErrorSize(0.)

# do not display any of the standard histogram decorations
myStyle.SetOptTitle(0)
myStyle.SetOptStat(0)
myStyle.SetOptFit(0)

# put tick marks on top and RHS of plots
myStyle.SetPadTickX(1)
myStyle.SetPadTickY(1)
