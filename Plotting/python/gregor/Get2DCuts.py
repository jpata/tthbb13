
#!/usr/bin/env python
"""
"""

########################################
# Imports 
########################################

import os
import array

import ROOT

########################################
# Configuration
########################################


basepath = "/mnt/t3nfs01/data01/shome/gregor/VHBB-8019/CMSSW_8_0_19/src/TTH/MEAnalysis/rq/results/db158a19-b9fb-4520-acde-d7348299a926/categories/"

to_process = [
    ["common_bdt", ["sl_j4_t3_bdt", "sl_j4_tge4_bdt", "sl_j5_t3_bdt", "sl_j5_tge4_bdt", "sl_jge6_t2_bdt", "sl_jge6_t3_bdt", "sl_jge6_tge4_bdt"]],
    ["common_bdt", ["dl_jge4_tge4_bdt", "dl_jge4_t3_bdt", "dl_j3_t3_bdt"]]
]

	

for var_cats in to_process:
    
    var = var_cats[0]
    cats = var_cats[1]



    for cat in cats:

        fn = os.path.join(basepath, cat + ".root")
        f = ROOT.TFile.Open(fn)

        h = f.Get("ttH_hbb/{0}/{1}".format(cat,var)).Clone()

        q = array.array( 'd', [0.])
        h.GetQuantiles( 1, q, array.array( 'd', [0.5]))
        print var, cat, h.GetBinCenter(h.FindBin(q[0]))
