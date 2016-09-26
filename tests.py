#!/usr/bin/env python
"""
Simple test runner for the workflow scripts.
"""

from TTH.Plotting.test_sparsinator import *
from TTH.Plotting.test_MakeCategory import *
from TTH.MEAnalysis.test_MEAnalysis_heppy import *

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    #test_MEAnalysis("/store/user/jpata/tth/tth_Jul31_V24_v1/ttHTobb_M125_13TeV_powheg_pythia8/tth_Jul31_V24_v1/160731_130548/0000/tree_1.root")
    #test_sparsinator(read_inputs("MEAnalysis/gc/datasets/tth_Jul31_V24_v1/SingleMuon.txt")[:5], "SingleMuon")
    #test_sparsinator(read_inputs("MEAnalysis/gc/datasets/tth_Jul31_V24_v1/ttHTobb_M125_13TeV_powheg_pythia8.txt")[:5], "ttHTobb_M125_13TeV_powheg_pythia8.txt")
    #test_MakeCategory("sl_jge6_tge4")
    unittest.main()
