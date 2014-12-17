#!/usr/bin/env python
"""
Schedule the testing of different variable/method-sets with TMVA
"""

########################################
# Imports 
########################################

import pickle

import ROOT

from TTH.Plotting.Helpers.TMVAHelpers import doTMVA
from TTH.Plotting.Helpers.PrepareRootStyle import myStyle




ROOT.gROOT.SetStyle("myStyle")
ROOT.gROOT.ForceStyle()


########################################
# Helper Class to store: 
#  -variables
#  -methods
#  -name
########################################

class TMVASetup:
    def __init__( self, 
                  name,
                  li_methods,
                  li_vars,
                  treeNameSig  = "tree",
                  treeNameBkg  = "tree",
              ):
        self.name        = "TMVA_" + name + ".root"
        self.li_methods  = li_methods
        self.li_vars     = li_vars
        self.treeNameSig = treeNameSig
        self.treeNameBkg = treeNameBkg
    # end of init
# end of TMVASetup class


########################################
# Configuration
########################################

run_TMVA = False

basepath = '/scratch/gregor/'
infnameSig   = "ntop_v8_zprime_m2000_1p_13tev-tagging.root"
infnameBkg   = "ntop_v8_qcd_800_1000_pythia8_13tev-tagging.root"

# Common options
li_methods      = ["Likelihood"]

li_TMVAs = []


#li_TMVAs.append( TMVASetup( "m",  li_methods, [[ "ca15_mass",0,2000]]))
#li_TMVAs.append( TMVASetup( "filtered m",  li_methods, [[ "ca15filtered_mass",0,2000]]))
#li_TMVAs.append( TMVASetup( "pruned m",  li_methods, [[ "ca15pruned_mass",0,2000]]))
#li_TMVAs.append( TMVASetup( "trimmed_m",  li_methods, [[ "ca15trimmed_mass",0,2000]]))
#li_TMVAs.append( TMVASetup( "softdrop m",  li_methods, [[ "ca15softdrop_mass",0,2000]]))

#li_TMVAs.append( TMVASetup( "#tau_{3}/#tau_{2}",  li_methods, [[ "ca15_tau3/ca15_tau2",0,2]]))
#li_TMVAs.append( TMVASetup( "filtered #tau_{3}/#tau_{2}",  li_methods, [[ "ca15filtered_tau3/ca15filtered_tau2",0,2]]))
#li_TMVAs.append( TMVASetup( "pruned #tau_{3}/#tau_{2}",  li_methods, [[ "ca15pruned_tau3/ca15pruned_tau2",0,2]]))
#li_TMVAs.append( TMVASetup( "trimmed #tau_{3}/#tau_{2}",  li_methods,[[ "ca15trimmed_tau3/ca15trimmed_tau2",0,2]]))
#li_TMVAs.append( TMVASetup( "softdrop #tau_{3}/#tau_{2}",  li_methods, [[ "ca15softdrop_tau3/ca15softdrop_tau2",0,2]]))


li_TMVAs.append( TMVASetup( "CMSS minMass",  li_methods,[["ca15cmstt_minMass", 0, 2000]]))
li_TMVAs.append( TMVASetup( "HTT m",  li_methods, [ ['looseMultiRHTT_mass', 0, 2000]]))
li_TMVAs.append( TMVASetup( "HTT fw",  li_methods, [[ "looseMultiRHTT_fW", 0, 1.0]]))
li_TMVAs.append( TMVASetup( "HTT #Delta R_{min,exp}",  li_methods, [[ "looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected", -3, 3]]))


########################################
# doTMVA
########################################

if run_TMVA:
    for TMVAops in li_TMVAs:
        doTMVA( basepath + infnameSig, 
                basepath + infnameBkg,
                TMVAops.name,
                TMVAops.li_methods,
                TMVAops.li_vars,
                treeNameSig  = TMVAops.treeNameSig,
                treeNameBkg  = TMVAops.treeNameBkg,
        )
        

li_colors = [ROOT.kRed,      ROOT.kBlue+1,     ROOT.kBlack, 
             ROOT.kOrange-1, ROOT.kViolet+1,   ROOT.kGreen+1,
             ROOT.kGray,     ROOT.kYellow,
         ]*10


########################################
# Extract histograms from files
########################################

li_hs    = []
li_names = []

di_cut_fracs = {}

for TMVAops in li_TMVAs:    
    f = ROOT.TFile( TMVAops.name, "READ" )
    
    for method in li_methods:
        h = f.FindObjectAny("MVA_" + method + "_rejBvsS")
        hc = h.Clone()
        hc.SetDirectory(0)
        li_hs.append( hc )
        name = TMVAops.name.replace(".root","").replace("TMVA_","")
        li_names.append( name  )

    f_pickle = open( TMVAops.name.replace(".root",".dat"), "r")
    di_cut_fracs[name] = pickle.load(f_pickle)
    
        
# end loop over infiles


########################################
# And draw them
########################################

c = ROOT.TCanvas( "","", 800, 800)

legend_origin_x     = 0.2
legend_origin_y     = 0.25
legend_size_x       = 0.3
legend_size_y       = 0.045 * len(li_hs)

legend = ROOT.TLegend( legend_origin_x, 
                       legend_origin_y,
                       legend_origin_x + legend_size_x,
                       legend_origin_y + legend_size_y )
legend.SetBorderSize(1) 
legend.SetFillColor(0)
legend.SetTextSize(0.04)      
legend.SetBorderSize(0)


h_bg = ROOT.TH2F("","",100,0,1,100,0,1)

h_bg.GetXaxis().SetTitle( "#varepsilon(S)" )      
h_bg.GetYaxis().SetTitle( "1-#varepsilon(B)" )      
h_bg.Draw()



for i_h, h in enumerate(li_hs):

    cut_fraction_signal = di_cut_fracs[li_names[i_h]]["sig"] 
    cut_fraction_bg = di_cut_fracs[li_names[i_h]]["bg"] 

    print li_names[i_h], cut_fraction_signal, cut_fraction_bg

    h.GetXaxis().SetLimits(0.0,cut_fraction_signal)

    for ibin in range(1, h.GetXaxis().GetNbins()):
        eff_b = 1 - h.GetBinContent(ibin)
        eff_b_new = eff_b * cut_fraction_bg
        h.SetBinContent(ibin, 1-eff_b_new)


    h.SetLineColor( li_colors[i_h] )
    h.SetLineWidth( 2)    
    legend.AddEntry( h, li_names[i_h], "L" )


for h in li_hs:    
    h.Draw("SAME")
legend.Draw()

#line  = ROOT.TLine()
#line.SetLineColor( ROOT.kBlack )
#line.SetLineWidth( 2 )
#line.DrawLine( 0, 1, 1, 0 )

c.Print("ROC.png")

