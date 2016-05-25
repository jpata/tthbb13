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
    dic_files["tth"] = filename_base + "/store/user/gregor/tth/VHBBHeppyV21_tthbbV9_g00/ttHTobb_M125_13TeV_powheg_pythia8/VHBBHeppyV21_tthbbV9_g00/160523_112144/0000/tree_1.root"


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

combinedPlot("dr_top",
              [plot( "good",
                     "higgsCandidate_dr_top",
                     '(higgsCandidate_dr_genHiggs<1.2)',
                     "tth"),
               plot( "good, pt>200",
                     "higgsCandidate_dr_top",
                     '((higgsCandidate_dr_genHiggs<1.2)&&(genHiggs_pt>200))',
                     "tth"),
               plot( "bad",
                     "higgsCandidate_dr_top",
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

combinedPlot("mass",
              [plot( "good",
                     "higgsCandidate_mass",
                     '(higgsCandidate_dr_genHiggs<1.2)',
                     "tth"),
               plot( "good, pt>200",
                     "higgsCandidate_mass",
                     '((higgsCandidate_dr_genHiggs<1.2)&&(genHiggs_pt>200))',
                     "tth"),
               plot( "bad",
                     "higgsCandidate_mass",
                     '(higgsCandidate_dr_genHiggs>2.0)',
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


combinedPlot("mass_softdrop",
              [plot( "good",
                     "higgsCandidate_mass_softdrop",
                     '(higgsCandidate_dr_genHiggs<1.2)',
                     "tth"),
               plot( "good pt>200",
                     "higgsCandidate_mass_softdrop",
                     '((higgsCandidate_dr_genHiggs<1.2)&&(genHiggs_pt>200))',
                     "tth"),
               plot( "bad",
                     "higgsCandidate_mass_softdrop",
                     '(higgsCandidate_dr_genHiggs>2.0)',
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

combinedPlot("mass_softdropz2b1",
              [plot( "good",
                     "higgsCandidate_mass_softdropz2b1",
                     '(higgsCandidate_dr_genHiggs<1.2)',
                     "tth"),
               plot( "good, pt>200",
                     "higgsCandidate_mass_softdropz2b1",
                     '((higgsCandidate_dr_genHiggs<1.2)&&(genHiggs_pt>200))',
                     "tth"),
               plot( "bad",
                     "higgsCandidate_mass_softdropz2b1",
                     '(higgsCandidate_dr_genHiggs>2.0)',
                     "tth"),
           ],
              80, 0, 500,
              label_x   = "Mass",
              label_y   = "Higgs Candidates",
              axis_unit = "GeV",
              legend_text_size= 0.03,
              log_y     = False,
              normalize = True)

combinedPlot("mass_pruned",
              [plot( "good",
                     "higgsCandidate_mass_pruned",
                     '(higgsCandidate_dr_genHiggs<1.2)',
                     "tth"),
               plot( "good, pt>200",
                     "higgsCandidate_mass_pruned",
                     '((higgsCandidate_dr_genHiggs<1.2)&&(genHiggs_pt>200))',
                     "tth"),
               plot( "bad",
                     "higgsCandidate_mass_pruned",
                     '(higgsCandidate_dr_genHiggs>2.0)',
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

combinedPlot("mass_subjetfiltered12",
              [plot( "good",
                     "higgsCandidate_sj12mass_subjetfiltered",
                     '(higgsCandidate_dr_genHiggs<1.2)',
                     "tth"),
               plot( "good, pt>200",
                     "higgsCandidate_sj12mass_subjetfiltered",
                     '((higgsCandidate_dr_genHiggs<1.2)&&(genHiggs_pt>200))',
                     "tth"),
               plot( "bad",
                     "higgsCandidate_sj12mass_subjetfiltered",
                     '(higgsCandidate_dr_genHiggs>2.0)',
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

combinedPlot("nsub",
              [plot( "good",
                     "higgsCandidate_n_subjettiness",
                     '(higgsCandidate_dr_genHiggs<1.2)',
                     "tth"),
               plot( "good, pt>200",
                     "higgsCandidate_n_subjettiness",
                     '((higgsCandidate_dr_genHiggs<1.2)&&(genHiggs_pt>200))',
                     "tth"),
               plot( "bad",
                     "higgsCandidate_n_subjettiness",
                     '(higgsCandidate_dr_genHiggs>2.0)',
                     "tth"),
           ],
              80, 0, 1,
              label_x   = "#tau_{2}/#tau_{1}",
              label_y   = "Higgs Candidates",
              axis_unit = "GeV",
              legend_text_size= 0.03,
              legend_origin_x = 0.7, 
              legend_origin_y = 0.8, 
              log_y     = False,
              normalize = True)


combinedPlot("nsub32",
              [plot( "good",
                     "higgsCandidate_tau3/higgsCandidate_tau2",
                     '(higgsCandidate_dr_genHiggs<1.2)',
                     "tth"),
               plot( "good, pt>200",
                     "higgsCandidate_tau3/higgsCandidate_tau2",
                     '((higgsCandidate_dr_genHiggs<1.2)&&(genHiggs_pt>200))',
                     "tth"),
               plot( "bad",
                     "higgsCandidate_tau3/higgsCandidate_tau2",
                     '(higgsCandidate_dr_genHiggs>2.0)',
                     "tth"),
           ],
              80, 0, 1,
              label_x   = "#tau_{2}/#tau_{1}",
              label_y   = "Higgs Candidates",
              axis_unit = "GeV",
              legend_text_size= 0.03,
              legend_origin_x = 0.7, 
              legend_origin_y = 0.8, 
              log_y     = False,
              normalize = True)

combinedPlot("nsub21",
              [plot( "good",
                     "higgsCandidate_tau2/higgsCandidate_tau1",
                     '(higgsCandidate_dr_genHiggs<1.2)',
                     "tth"),
               plot( "good, pt>200",
                     "higgsCandidate_tau2/higgsCandidate_tau1",
                     '((higgsCandidate_dr_genHiggs<1.2)&&(genHiggs_pt>200))',
                     "tth"),
               plot( "bad",
                     "higgsCandidate_tau2/higgsCandidate_tau1",
                     '(higgsCandidate_dr_genHiggs>2.0)',
                     "tth"),
           ],
              80, 0, 1,
              label_x   = "#tau_{2}/#tau_{1}",
              label_y   = "Higgs Candidates",
              axis_unit = "GeV",
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






