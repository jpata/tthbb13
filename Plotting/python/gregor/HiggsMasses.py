#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import sys
import glob
import pickle

from TTH.Plotting.Helpers.CompareDistributionsHelpers import *


########################################
# Configuration
########################################

filename_base = "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat"

dic_files = {}
if "FILE_NAMES" in os.environ.keys():
    dic_files["tth"] = ([filename_base + f for f in os.environ["FILE_NAMES"].split(" ")], "tree")
    print dic_files
else:
    dic_files["tth"] = filename_base + "/store/user/gregor/tth/VHBBHeppyV21_tthbbV9_g01/ttHTobb_M125_13TeV_powheg_pythia8/VHBBHeppyV21_tthbbV9_g01/160524_170959/0000/tree_100.root"

output_dir = "./"

# Run on batch to produce pickle files with histograms
# Run locally to turn these into plots

if len(sys.argv) > 1:
    CREATE      = False
    DRAW        = True
    input_files = glob.glob(sys.argv[1]+"*.pkl")
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
              [plot( "good",
                     "higgsCandidate_dr_genTop",
                     '(higgsCandidate_dr_genHiggs<1.2)',
                     "tth"),
               plot( "good, pt>200",
                     "higgsCandidate_dr_genTop",
                     '((higgsCandidate_dr_genHiggs<1.2)&&(genHiggs_pt>200))',
                     "tth"),
               plot( "bad",
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



cut_bad     = '(higgsCandidate_dr_genHiggs>2.0)'
cut_good    = '(higgsCandidate_dr_genHiggs<1.2)&&((higgsCandidate_dr_genTop>1.2)||(higgsCandidate_dr_genTop<-0.1))'
cut_good_pt = "( ({0}) && (genHiggs_pt>200))".format(cut_good)


masses = [ ["mass", "Ungroomed_mass", "higgsCandidate_mass"],
           ["mass_softdrop", "Softdrop (z=0.1, #beta=0) Mass", "higgsCandidate_mass_softdrop"],
           ["mass_softdropz2b1","Softdrop (z=0.2, #beta=1) Mass", "higgsCandidate_mass_softdropz2b1"],
           ["mass_pruned", "Pruned Mass", "higgsCandidate_mass_pruned"],
           ["mass_subjetfiltered12pt", "Massdrop/Filtered Mass (2 jets, p_{T})", "higgsCandidate_sj12masspt_subjetfiltered"],
           ["mass_subjetfiltered12b", "Massdrop/Filtered Mass (2 jets, b)", "higgsCandidate_sj12massb_subjetfiltered"],
           ["mass_subjetfiltered123pt", "Massdrop/Filtered Mass (3 jets)", "higgsCandidate_sj123masspt_subjetfiltered"]
]

for variables in masses:
    name        = variables[0]
    pretty_name = variables[1]
    var         = variables[2]

    combinedPlot(name,
                 [plot( "good",
                        var,
                        cut_good,
                        "tth"),
                  plot( "good, pt>200",
                        var, 
                        cut_good_pt,
                        "tth"),
                  plot( "bad",
                        var,
                        cut_bad,
                        "tth"),
              ],
                 80, 0, 500,
                 label_x   = pretty_name,
                 label_y   = "Higgs Candidates",
                 axis_unit = "GeV",
                 legend_text_size= 0.03,
                 legend_origin_x = 0.7, 
                 legend_origin_y = 0.8, 
                 log_y     = False,
                 normalize = True)

combinedPlot("masscomp",
             [plot( "SD (z2b1), good, pt>200",
                    "higgsCandidate_mass_softdropz2b1", 
                    cut_good_pt,
                    "tth"),
              plot( "SD (z2b1), bad",
                    "higgsCandidate_mass_softdropz2b1", 
                    cut_bad,
                    "tth"),
              plot( "MDF (2b), good, pt>200",
                    "higgsCandidate_sj12massb_subjetfiltered", 
                    cut_good_pt,
                    "tth"),
              plot( "MDF (2b), bad",
                    "higgsCandidate_sj12massb_subjetfiltered", 
                    cut_bad,
                    "tth"),

          ],
             80, 0, 500,
             label_x   = "Mass",
             label_y   = "Higgs Candidates",
             axis_unit = "GeV",
             legend_text_size= 0.03,
             legend_origin_x = 0.7, 
             legend_origin_y = 0.8, 
             log_y     = False,
             normalize = True)


combinedPlot("masscomp_notnorm",
             [plot( "SD (z2b1), good, pt>200",
                    "higgsCandidate_mass_softdropz2b1", 
                    cut_good_pt,
                    "tth"),
              plot( "SD (z2b1), bad",
                    "higgsCandidate_mass_softdropz2b1", 
                    cut_bad,
                    "tth"),
              plot( "MDF (2b), good, pt>200",
                    "higgsCandidate_sj12massb_subjetfiltered", 
                    cut_good_pt,
                    "tth"),
              plot( "MDF (2b), bad",
                    "higgsCandidate_sj12massb_subjetfiltered", 
                    cut_bad,
                    "tth"),

          ],
             80, 0, 500,
             label_x   = "Mass",
             label_y   = "Higgs Candidates",
             axis_unit = "GeV",
             legend_text_size= 0.03,
             legend_origin_x = 0.7, 
             legend_origin_y = 0.8, 
             log_y     = False,
             normalize = False)




combinedPlot("nsub32",
              [plot( "good",
                     "higgsCandidate_tau3/higgsCandidate_tau2",
                     cut_good,
                     "tth"),
               plot( "good, pt>200",
                     "higgsCandidate_tau3/higgsCandidate_tau2",
                     cut_good_pt,
                     "tth"),
               plot( "bad",
                     "higgsCandidate_tau3/higgsCandidate_tau2",
                     cut_bad,
                     "tth"),
           ],
              80, 0, 1,
              label_x   = "#tau_{3}/#tau_{2}",
              label_y   = "Higgs Candidates",
              axis_unit = "",
              legend_text_size= 0.03,
              legend_origin_x = 0.7, 
              legend_origin_y = 0.8, 
              log_y     = False,
              normalize = True)

combinedPlot("nsub21",
              [plot( "good",
                     "higgsCandidate_tau2/higgsCandidate_tau1",
                     cut_good, 
                     "tth"),
               plot( "good, pt>200",
                     "higgsCandidate_tau2/higgsCandidate_tau1",
                     cut_good_pt, 
                     "tth"),
               plot( "bad",
                     "higgsCandidate_tau2/higgsCandidate_tau1",
                     cut_bad, 
                     "tth"),
           ],
              80, 0, 1,
              label_x   = "#tau_{2}/#tau_{1}",
              label_y   = "Higgs Candidates",
              axis_unit = "",
              legend_text_size= 0.03,
              legend_origin_x = 0.7, 
              legend_origin_y = 0.8, 
              log_y     = False,
              normalize = True)


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






