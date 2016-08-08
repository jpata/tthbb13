#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import sys
import pdb
import glob
import pickle

from TTH.Plotting.Helpers.CompareDistributionsHelpers import *


########################################
# Configuration
########################################

filename_base = "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat"

dic_files = {"tth":([],"tree"), 
             "ttbar":([],"tree")}
if "FILE_NAMES" in os.environ.keys():

    for f in os.environ["FILE_NAMES"].split(" "):
        fn = filename_base + f
        
        if  "TT_TuneEE5C_13TeV-powheg-herwigpp" in fn:
            dic_files["ttbar"][0].append(fn)
                 
        elif "ttHTobb_M125_13TeV_powheg_pythia8" in fn:
            dic_files["tth"][0].append(fn)

    print dic_files
else:
    dic_files["tth"] = filename_base + "/store/user/jpata/tth/Jul7_pilot_v1/ttHTobb_M125_13TeV_powheg_pythia8/Jul7_pilot_v1/160707_100154/0000/tree_383.root"


output_dir = "./"

# Run on batch to produce pickle files with histograms
# Run locally to turn these into plots

# Local
if len(sys.argv) > 1:
    CREATE      = False
    DRAW        = True
    input_files = glob.glob(sys.argv[1]+"*.pkl")
# Batch
else:
    CREATE      = True
    DRAW        = False

########################################
# Define the plots
########################################

combinedPlot("dr_genHiggs",
              [plot( "higgs",
                     "higgsCandidate_dr_genHiggs",
                     '(1)',
                     "tth")],
              60, -1.1, 6.0,
              label_x   = "#Delta R(Higgs Candidate, True Higgs)",
              label_y   = "Higgs Candidates",
              axis_unit = "",
              log_y     = False,
              draw_legend = False,
              normalize = True)

combinedPlot("dr_genTop",
              [plot( "Higgs",
                     "higgsCandidate_dr_genTop",
                     '(higgsCandidate_dr_genHiggs<1.2)',
                     "tth"),
               plot( "Top",
                     "higgsCandidate_dr_genTop",
                     '(higgsCandidate_dr_genHiggs>2.0)',
                     "tth"),
           ],
              60, -1.1, 6.0,
              label_x   = "#Delta R(Higgs Candidate, True Top)",
              label_y   = "Higgs Candidates",
              axis_unit = "",
              legend_text_size= 0.03,
              legend_origin_x = 0.7, 
              legend_origin_y = 0.8, 
              log_y     = False,
              draw_legend = True,
              normalize = True)


cut_other     = '((higgsCandidate_dr_genTop>2.0)||(higgsCandidate_dr_genTop<-0.1))&&((higgsCandidate_dr_genHiggs>2.0)||(higgsCandidate_dr_genHiggs<-0.1))'
cut_top       = '(higgsCandidate_dr_genTop<1.2)&&((higgsCandidate_dr_genHiggs>2.0)||(higgsCandidate_dr_genHiggs<-0.1))'
cut_higgs     = '(higgsCandidate_dr_genHiggs<1.2)&&((higgsCandidate_dr_genTop>2.0)||(higgsCandidate_dr_genTop<-0.1))'
cut_higgs_200 = "( ({0}) && (higgsCandidate_pt>=200) && (higgsCandidate_pt<300))".format(cut_higgs)
cut_higgs_300 = "( ({0}) && (higgsCandidate_pt>=300))".format(cut_higgs)

masses = [ ["mass", "Ungroomed Mass", "higgsCandidate_mass"],
           ["mass_softdrop", "Softdrop (z=0.1, #beta=0) Mass", "higgsCandidate_mass_softdrop"],
           ["mass_softdropz2b1","Softdrop (z=0.2, #beta=1) Mass", "higgsCandidate_mass_softdropz2b1"],
           ["mass_softdropfilt", "Softdrop (z=0.1, #beta=0)+Filter Mass", "higgsCandidate_mass_softdropfilt"],
           ["mass_softdropz2b1filt","Softdrop (z=0.2, #beta=1)+Filter Mass", "higgsCandidate_mass_softdropz2b1filt"],
           ["mass_pruned", "Pruned Mass", "higgsCandidate_mass_pruned"],
           ["mass_subjetfiltered12pt", "Massdrop/Filtered Mass (2 jets, p_{T})", "higgsCandidate_sj12masspt_subjetfiltered"],
           ["mass_subjetfiltered12b", "Massdrop/Filtered Mass (2 jets, b)", "higgsCandidate_sj12massb_subjetfiltered"],
           ["mass_subjetfiltered123pt", "Massdrop/Filtered Mass (3 jets)", "higgsCandidate_sj123masspt_subjetfiltered"]
]

#for variables in masses:
#    name        = variables[0]
#    pretty_name = variables[1]
#    var         = variables[2]
#
#    combinedPlot(name,
#                 [plot( "Higgs (200<p_{T}<300)",
#                        var,
#                        cut_higgs_200,
#                        "tth"),
#                  plot( "Higgs, p_{T}>300",
#                        var, 
#                        cut_higgs_300,
#                        "tth"),
#                  plot( "Top",
#                        var,
#                        cut_top,
#                        "tth"),
#              ],
#                 80, 0, 500,
#                 label_x   = pretty_name,
#                 label_y   = "Higgs Candidates",
#                 axis_unit = "GeV",
#                 legend_text_size= 0.03,
#                 legend_origin_x = 0.62, 
#                 legend_origin_y = 0.8, 
#                 log_y     = False,
#                 normalize = True)
#
#combinedPlot("masscomp",
#             [plot( "SD (z2b1), Higgs, p_{T}>300",
#                    "higgsCandidate_mass_softdropz2b1", 
#                    cut_higgs_300,
#                    "tth"),
#              plot( "SD (z2b1), Top",
#                    "higgsCandidate_mass_softdropz2b1", 
#                    cut_top,
#                    "tth"),
#              plot( "MDF (2b), Higgs, p_{T}>300",
#                    "higgsCandidate_sj12massb_subjetfiltered", 
#                    cut_higgs_300,
#                    "tth"),
#              plot( "MDF (2b), Top",
#                    "higgsCandidate_sj12massb_subjetfiltered", 
#                    cut_top,
#                    "tth"),
#
#          ],
#             80, 0, 500,
#             label_x   = "Mass",
#             label_y   = "Higgs Candidates",
#             axis_unit = "GeV",
#             legend_text_size= 0.03,
#             legend_origin_x = 0.62, 
#             legend_origin_y = 0.8, 
#             log_y     = False,
#             normalize = True)
#
#
#combinedPlot("masscomp_notnorm",
#             [plot( "SD (z2b1), Higgs, p_{T}>300",
#                    "higgsCandidate_mass_softdropz2b1", 
#                    cut_higgs_300,
#                    "tth"),
#              plot( "SD (z2b1), Top",
#                    "higgsCandidate_mass_softdropz2b1", 
#                    cut_top,
#                    "tth"),
#              plot( "MDF (2b), Higgs, p_{T}>300",
#                    "higgsCandidate_sj12massb_subjetfiltered", 
#                    cut_higgs_300,
#                    "tth"),
#              plot( "MDF (2b), Top",
#                    "higgsCandidate_sj12massb_subjetfiltered", 
#                    cut_top,
#                    "tth"),
#
#          ],
#             80, 0, 500,
#             label_x   = "Mass",
#             label_y   = "Higgs Candidates",
#             axis_unit = "GeV",
#             legend_text_size= 0.03,
#             legend_origin_x = 0.62, 
#             legend_origin_y = 0.8, 
#             log_y     = False,
#             normalize = False)
#
#combinedPlot("bcomp",
#             [plot( "bbtag, Higgs, p_{T} > 300",
#                    "higgsCandidate_bbtag", 
#                    cut_higgs_300,
#                    "tth"),
#              plot( "bbtag, Top",
#                    "higgsCandidate_bbtag", 
#                    cut_top,
#                    "tth"),
#              plot( "2nd subjet b-tag, Higgs, p_{T} > 300",
#                    "higgsCandidate_secondbtag_subjetfiltered", 
#                    cut_higgs_300,
#                    "tth"),
#              plot( "2nd subjet b-tag, Top",
#                    "higgsCandidate_secondbtag_subjetfiltered", 
#                    cut_top,
#                    "tth"),
#
#          ],
#             80, -1, 1,
#             label_x   = "Tagging Score",
#             label_y   = "Higgs Candidates",
#             axis_unit = "",
#             legend_text_size= 0.03,
#             legend_origin_x = 0.62, 
#             legend_origin_y = 0.8, 
#             log_y     = False,
#             normalize = True)
#
#
#
#
#combinedPlot("nsub32",
#              [plot( "Higgs (200<p_{T}<300)",
#                     "higgsCandidate_tau3/higgsCandidate_tau2",
#                     cut_higgs_200,
#                     "tth"),
#               plot( "Higgs, p_{T}>300",
#                     "higgsCandidate_tau3/higgsCandidate_tau2",
#                     cut_higgs_300,
#                     "tth"),
#               plot( "Top",
#                     "higgsCandidate_tau3/higgsCandidate_tau2",
#                     cut_top,
#                     "tth"),
#           ],
#              80, 0, 1,
#              label_x   = "#tau_{3}/#tau_{2}",
#              label_y   = "Higgs Candidates",
#              axis_unit = "",
#              legend_text_size= 0.03,
#              legend_origin_x = 0.62, 
#              legend_origin_y = 0.8, 
#              log_y     = False,
#              normalize = True)
#
#combinedPlot("nsub21",
#              [plot( "Higgs (200<p_{T}<300)",
#                     "higgsCandidate_tau2/higgsCandidate_tau1",
#                     cut_higgs_200, 
#                     "tth"),
#               plot( "Higgs, p_{T}>300",
#                     "higgsCandidate_tau2/higgsCandidate_tau1",
#                     cut_higgs_300,
#                     "tth"),
#               plot( "Top",
#                     "higgsCandidate_tau2/higgsCandidate_tau1",
#                     cut_top, 
#                     "tth"),
#           ],
#              80, 0, 1,
#              label_x   = "#tau_{2}/#tau_{1}",
#              label_y   = "Higgs Candidates",
#              axis_unit = "",
#              legend_text_size= 0.03,
#              legend_origin_x = 0.62, 
#              legend_origin_y = 0.8, 
#              log_y     = False,
#              normalize = True)
#

combinedPlot("bbtag",
              [plot( "Higgs (200<p_{T}<300)",
                     "higgsCandidate_bbtag",
                     cut_higgs_200, 
                     "tth"),
               plot( "Higgs, p_{T}>300",
                     "higgsCandidate_bbtag",
                     cut_higgs_300,
                     "tth"),
               plot( "Top (ttH)",
                     "higgsCandidate_bbtag",
                     cut_top, 
                     "tth"),
               plot( "Top (ttbar)",
                     "higgsCandidate_bbtag",
                     cut_top, 
                     "ttbar"),
               plot( "Other ",
                     "higgsCandidate_bbtag",
                     cut_other, 
                     "ttbar"),
           ],
              80, -1, 1,
              label_x   = "bb tag",
              label_y   = "Higgs Candidates",
              axis_unit = "",
              legend_text_size= 0.03,
              legend_origin_x = 0.62, 
              legend_origin_y = 0.7, 
              log_y     = False,
              normalize = True)

combinedPlot("bbtag_bg",
              [plot( "Higgs, p_{T}>300",
                     "higgsCandidate_bbtag",
                     cut_higgs_300,
                     "tth"),                  
               plot( "top",
                     "higgsCandidate_bbtag",
                     cut_top,
                     "ttbar"),                
               plot( "ttb",
                     "higgsCandidate_bbtag",
                     "(" + cut_other + ")&&(ttCls==51)" , 
                     "ttbar"),
               plot( "tt2b",
                     "higgsCandidate_bbtag",
                     "(" + cut_other + ")&&(ttCls==52)" , 
                     "ttbar"),
               plot( "ttbb",
                     "higgsCandidate_bbtag",
                     "(" + cut_other + ")&&((ttCls==53)||(ttCls==54)||(ttCls==55)||(ttCls==56))" , 
                     "ttbar"),
               plot( "ttcc",
                     "higgsCandidate_bbtag",
                     "(" + cut_other + ")&&((ttCls==41)||(ttCls==42)||(ttCls==43)||(ttCls==44)||(ttCls==45))" , 
                     "ttbar"),
               plot( "ttll",
                     "higgsCandidate_bbtag",
                     "(" + cut_other + ")&&((ttCls==0)||(ttCls<0))",
                     "ttbar"),
           ],
              50, -1, 1,
              label_x   = "bb tag",
              label_y   = "Higgs Candidates",
              axis_unit = "",
              legend_text_size= 0.03,
              legend_origin_x = 0.62, 
              legend_origin_y = 0.7, 
              log_y     = False,
              normalize = True)

combinedPlot("secondcandbtag_bg",
              [plot( "Higgs, p_{T}>300",
                     "higgsCandidate_secondbtag_subjetfiltered",
                     cut_higgs_300,
                     "tth"),  
               plot( "top",
                     "higgsCandidate_secondbtag_subjetfiltered",
                     cut_top,
                     "ttbar"),                
               plot( "ttb",
                     "higgsCandidate_secondbtag_subjetfiltered",
                     "(" + cut_other + ")&&(ttCls==51)" , 
                     "ttbar"),
               plot( "tt2b",
                     "higgsCandidate_secondbtag_subjetfiltered",
                     "(" + cut_other + ")&&(ttCls==52)" , 
                     "ttbar"),
               plot( "ttbb",
                     "higgsCandidate_secondbtag_subjetfiltered",
                     "(" + cut_other + ")&&((ttCls==53)||(ttCls==54)||(ttCls==55)||(ttCls==56))" , 
                     "ttbar"),
               plot( "ttcc",
                     "higgsCandidate_secondbtag_subjetfiltered",
                     "(" + cut_other + ")&&((ttCls==41)||(ttCls==42)||(ttCls==43)||(ttCls==44)||(ttCls==45))" , 
                     "ttbar"),
               plot( "ttll",
                     "higgsCandidate_secondbtag_subjetfiltered",
                     "(" + cut_other + ")&&((ttCls==0)||(ttCls<0))",
                     "ttbar"),
           ],
              50, 0, 1,
              label_x   = "bb tag",
              label_y   = "Higgs Candidates",
              axis_unit = "",
              legend_text_size= 0.03,
              legend_origin_x = 0.62, 
              legend_origin_y = 0.7, 
              log_y     = False,
              normalize = True)

#combinedPlot("secondbtag",
#              [plot( "Higgs (200<p_{T}<300)",
#                     "higgsCandidate_secondbtag_subjetfiltered",
#                     cut_higgs_200, 
#                     "tth"),
#               plot( "Higgs, p_{T}>300",
#                     "higgsCandidate_secondbtag_subjetfiltered",
#                     cut_higgs_300,
#                     "tth"),
#               plot( "Top",
#                     "higgsCandidate_secondbtag_subjetfiltered",
#                     cut_top, 
#                     "tth"),
#           ],
#              80, 0, 1,
#              label_x   = "2nd subjet b-tag",
#              label_y   = "Higgs Candidates",
#              axis_unit = "",
#              legend_text_size= 0.03,
#              legend_origin_x = 0.62, 
#              legend_origin_y = 0.8, 
#              log_y     = False,
#              normalize = True)


def calc_roc(h1, h2):

    h1 = h1.Clone()
    h2 = h2.Clone()

    if h1.Integral()>0:
        h1.Scale(1.0 / h1.Integral())
    if h2.Integral()>0:
        h2.Scale(1.0 / h2.Integral())

    gr = ROOT.TGraph()
    
    for i in range(0, h1.GetNbinsX()+2):
        I1 = h1.Integral(0, h1.GetNbinsX())
        I2 = h2.Integral(0, h2.GetNbinsX())
        if I1>0 and I2>0:            
            gr.SetPoint(gr.GetN(), 
                        h1.Integral(i, h1.GetNbinsX()) / I1,
                        h2.Integral(i, h2.GetNbinsX()) / I2)     

    return gr



if CREATE:
    dic_histos = createHistograms(dic_files)
    
    f = open(os.path.join(output_dir, "histos.pkl"), "wb")
    pickle.dump(dic_histos, f)
    f.close()


if DRAW:
    dic_histos = {}
    for input_file in input_files:
        
        print "Adding", input_file
        
        f = open(input_file, "rb")
        tmp_dic_histos = pickle.load(f)

        for k,v in tmp_dic_histos.iteritems():
            if k in dic_histos.keys():
                dic_histos[k].Add(v)
            else:
                dic_histos[k] = v.Clone()

    drawHistograms(dic_histos, output_dir)


    c = ROOT.TCanvas()

    print dic_histos.keys()


    for background in ["ttb", "ttbb", "ttcc", "tt2b", "ttll", "top"]:

        

        bbtag_sig = "bbtag_bg_" + "Higgs, p_{T}>300"
        bbtag_bkg = "bbtag_bg_" + background
        secondbtag_sig = "secondcandbtag_bg_" + "Higgs, p_{T}>300"
        secondbtag_bkg = "secondcandbtag_bg_" + background

        roc_bbtag = calc_roc(dic_histos[bbtag_sig],
                             dic_histos[bbtag_bkg])

        roc_secondbtag = calc_roc(dic_histos[secondbtag_sig],
                                  dic_histos[secondbtag_bkg])


        roc_bbtag.SetLineColor(ROOT.kRed)
        roc_secondbtag.SetLineColor(ROOT.kBlue)

        roc_bbtag.SetLineWidth(2)
        roc_secondbtag.SetLineWidth(2)

        legend_origin_x     = 0.25
        legend_origin_y     = 0.7
        legend_size_x       = 0.3
        legend_size_y       = 0.08

        legend = ROOT.TLegend( legend_origin_x, 
                               legend_origin_y,
                               legend_origin_x + legend_size_x,
                               legend_origin_y + legend_size_y )
        legend.SetBorderSize(1) 
        legend.SetFillColor(0)
        legend.SetTextSize(0.04)      
        legend.SetBorderSize(0)

        legend.AddEntry( roc_bbtag, "bb-tag", "L" )
        legend.AddEntry( roc_secondbtag, "Second subjet b-tag", "L" )

        h_bg = ROOT.TH2F("","",100,0,1.,100,0.,1)    
        h_bg.GetXaxis().SetTitle( "#varepsilon(S)" )      
        h_bg.GetYaxis().SetTitle( "1-#varepsilon(B)" )      
        h_bg.Draw()

        roc_bbtag.Draw("SAME")
        roc_secondbtag.Draw("SAME")

        legend.Draw()

        c.Print("ROC_" + background + ".png")





