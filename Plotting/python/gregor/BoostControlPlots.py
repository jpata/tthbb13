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
    dic_files["tth"] = filename_base + "/store/user/jpata/tth/VHBBHeppyV21_tthbbV9_test3/TT_TuneEE5C_13TeV-powheg-herwigpp/VHBBHeppyV21_tthbbV9_test3/160602_131703/0000/tree_10.root"

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

to_plot = [
    ["n_fatjets",              "nfatjets",                                 10, -0.5, 9.5, ],
    ["pt_fatjet_1",            "fatjets_pt[0]",                            50, 0, 800,    ],
    ["pt_fatjet_2",            "fatjets_pt[1]",                            50, 0, 800,    ],
    ["eta_fatjet_1",           "fatjets_eta[0]",                           50, -3, 3,     ],
    ["eta_fatjet_2",           "fatjets_eta[1]",                           50, -3, 3,     ],
    ["pt_nonW_1",              "topCandidatesSync_sjNonWpt[0]",            50, 0, 500,    ],
    ["pt_nonW_2",              "topCandidatesSync_sjNonWpt[1]",            50, 0, 500,    ],
    ["pt_W1_1",                "topCandidatesSync_sjW1pt[0]",              50, 0, 500,    ],
    ["pt_W1_2",                "topCandidatesSync_sjW1pt[1]",              50, 0, 500,    ],
    ["pt_W2_1",                "topCandidatesSync_sjW2pt[0]",              50, 0, 500,    ],
    ["pt_W2_2",                "topCandidatesSync_sjW2pt[1]",              50, 0, 500,    ],
    ["csv_nonW_1",             "topCandidatesSync_sjNonWbtag[0]",          50, -1, 1.,    ],
    ["csv_nonW_2",             "topCandidatesSync_sjNonWbtag[1]",          50, -1, 1.,    ],
    ["csv_W1_1",               "topCandidatesSync_sjW1btag[0]",            50, -1, 1.,    ],
    ["csv_W1_2",               "topCandidatesSync_sjW1btag[1]",            50, -1, 1.,    ],
    ["csv_W2_1",               "topCandidatesSync_sjW2btag[0]",            50, -1, 1.,    ],
    ["csv_W2_2",               "topCandidatesSync_sjW2btag[1]",            50, -1, 1.,    ],
    ["pt_top_1",               "topCandidatesSync_pt[0]",                  50, 0, 800,    ],
    ["pt_top_2",               "topCandidatesSync_pt[1]",                  50, 0, 800,    ],
    ["eta_top_1",              "topCandidatesSync_eta[0]",                 50, -3, 3,     ],
    ["eta_top_2",              "topCandidatesSync_eta[1]",                 50, -3, 3,     ],
    ["m_top_1",                "topCandidatesSync_mass[0]",                50, 0, 500,    ],
    ["m_top_2",                "topCandidatesSync_mass[1]",                50, 0, 500,    ],
    ["pt_sf_filterjet1_1",     "higgsCandidate_sj1pt_subjetfiltered[0]",   50, 0, 500,    ],
    ["pt_sf_filterjet1_2",     "higgsCandidate_sj1pt_subjetfiltered[1]",   50, 0, 500,    ],
    ["pt_sf_filterjet2_1",     "higgsCandidate_sj2pt_subjetfiltered[0]",   50, 0, 500,    ],
    ["pt_sf_filterjet2_2",     "higgsCandidate_sj2pt_subjetfiltered[1]",   50, 0, 500,    ],
    ["pt_sf_filterjet3_1",     "higgsCandidate_sj3pt_subjetfiltered[0]",   50, 0, 500,    ],
    ["pt_sf_filterjet3_2",     "higgsCandidate_sj3pt_subjetfiltered[1]",   50, 0, 500,    ],
    ["csv_sf_filterjet1_1",    "higgsCandidate_sj1btag_subjetfiltered[0]", 50, -1, 1.     ],
    ["csv_sf_filterjet1_2",    "higgsCandidate_sj1btag_subjetfiltered[1]", 50, -1, 1.     ],
    ["csv_sf_filterjet2_1",    "higgsCandidate_sj2btag_subjetfiltered[0]", 50, -1, 1.     ],
    ["csv_sf_filterjet2_2",    "higgsCandidate_sj2btag_subjetfiltered[1]", 50, -1, 1.     ],
    ["csv_sf_filterjet3_1",    "higgsCandidate_sj3btag_subjetfiltered[0]", 50, -1, 1.     ],
    ["csv_sf_filterjet3_2",    "higgsCandidate_sj3btag_subjetfiltered[1]", 50, -1, 1.     ],
    ["pt_pruned_subjet1_1",    "higgsCandidate_sj1pt_pruned[0]",           50, 0, 500,    ],
    ["pt_pruned_subjet1_2",    "higgsCandidate_sj1pt_pruned[1]",           50, 0, 500,    ],
    ["pt_pruned_subjet2_1",    "higgsCandidate_sj2pt_pruned[0]",           50, 0, 500,    ],
    ["pt_pruned_subjet2_2",    "higgsCandidate_sj2pt_pruned[1]",           50, 0, 500,    ],
    ["csv_pruned_subjet1_1",   "higgsCandidate_sj1btag_pruned[0]",         50, -1, 1.     ],
    ["csv_pruned_subjet1_2",   "higgsCandidate_sj1btag_pruned[1]",         50, -1, 1.     ],
    ["csv_pruned_subjet2_1",   "higgsCandidate_sj2btag_pruned[0]",         50, -1, 1.     ],
    ["csv_pruned_subjet2_2",   "higgsCandidate_sj2btag_pruned[1]",         50, -1, 1.     ],
    ["pt_sd_subjet1_1",        "higgsCandidate_sj1pt_softdrop[0]",         50, 0, 500,    ],
    ["pt_sd_subjet1_2",        "higgsCandidate_sj1pt_softdrop[1]",         50, 0, 500,    ],
    ["pt_sd_subjet2_1",        "higgsCandidate_sj2pt_softdrop[0]",         50, 0, 500,    ],
    ["pt_sd_subjet2_2",        "higgsCandidate_sj2pt_softdrop[1]",         50, 0, 500,    ],
    ["csv_sd_subjet1_1",       "higgsCandidate_sj1btag_softdrop[0]",       50, -1, 1.     ],
    ["csv_sd_subjet1_2",       "higgsCandidate_sj1btag_softdrop[1]",       50, -1, 1.     ],
    ["csv_sd_subjet2_1",       "higgsCandidate_sj2btag_softdrop[0]",       50, -1, 1.     ],
    ["csv_sd_subjet2_2",       "higgsCandidate_sj2btag_softdrop[1]",       50, -1, 1.     ],
    ["pt_sdz2b1_subjet1_1",    "higgsCandidate_sj1pt_softdropz2b1[0]",     50, 0, 500,    ],
    ["pt_sdz2b1_subjet1_2",    "higgsCandidate_sj1pt_softdropz2b1[1]",     50, 0, 500,    ],
    ["pt_sdz2b1_subjet2_1",    "higgsCandidate_sj2pt_softdropz2b1[0]",     50, 0, 500,    ],
    ["pt_sdz2b1_subjet2_2",    "higgsCandidate_sj2pt_softdropz2b1[1]",     50, 0, 500,    ],
    ["csv_sdz2b1_subjet1_1",   "higgsCandidate_sj1btag_softdropz2b1[0]",   50, -1, 1.     ],
    ["csv_sdz2b1_subjet1_2",   "higgsCandidate_sj1btag_softdropz2b1[1]",   50, -1, 1.     ],
    ["csv_sdz2b1_subjet2_1",   "higgsCandidate_sj2btag_softdropz2b1[0]",   50, -1, 1.     ],
    ["csv_sdz2b1_subjet2_2",   "higgsCandidate_sj2btag_softdropz2b1[1]",   50, -1, 1.     ],
]

for plt in to_plot:
    [name, variable, nbins, minx, maxx] = plt

    combinedPlot(name, 
                  [plot( "foo",
                         variable, 
                         '(1)',
                         "tth")],
                  nbins, minx, maxx,
                  label_x   = name,
                  label_y   = "Entries",
                  axis_unit = "",
                  log_y     = False,
                  draw_legend = False,
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






