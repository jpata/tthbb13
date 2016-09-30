
#!/usr/bin/env python
"""
Plot the limits
"""

########################################
# Imports 
########################################

import matplotlib as mpl
mpl.use('Agg')

import os, sys, math
import uuid
import matplotlib.pyplot as plt


from TTH.Plotting.Datacards.CombineHelper import get_limits
import TTH.Plotting.joosep.plotlib as plotlib
import numpy as np


########################################
# Configuration
########################################

# Where to get the data from
limits_base = "/mnt/t3nfs01/data01/shome/gregor/VHBB-8019/CMSSW_8_0_19/src/TTH/MEAnalysis/rq/results/5d570727-dc2f-4c89-b27b-80bec0c03324/limits/"

# List of plots
# plots: list with two entries
#          -first entry: desired output filename
#          -second entry: list of limit names to include in plot
plots = [
    ["total_sldl",["group_sldl_7cat", "group_sldl_7cat_blrsplit", "group_sldl_7cat_bdt", "group_sldl_7cat_2d"]],
    ["total_sl",["group_sl_7cat", "group_sl_7cat_blrsplit", "group_sl_7cat_bdt", "group_sl_7cat_2d"]],

    ["sl_2d", ["sl_jge6_t2_bdtL", 	"sl_jge6_t2_bdtH", 	"sl_jge6_t3_bdtL", 	"sl_jge6_t3_bdtH", 	 	"sl_jge6_tge4_bdtL", "sl_jge6_tge4_bdtH", 	"sl_j5_t3_bdtL", 	"sl_j5_t3_bdtH", 	"sl_j5_tge4_bdtL", 	"sl_j5_tge4_bdtH", 	"sl_j4_t3_bdtL", 	"sl_j4_t3_bdtH", 	"sl_j4_tge4_bdtL", 	"sl_j4_tge4_bdtH"]],

    ["sl_7cat_blrsplit", ["sl_jge6_t2_blrL", 	"sl_jge6_t2_blrH", 	"sl_jge6_t3_blrL", 	"sl_jge6_t3_blrH", 	 	"sl_jge6_tge4_blrL", "sl_jge6_tge4_blrH", 	"sl_j5_t3_blrL", 	"sl_j5_t3_blrH", 	"sl_j5_tge4_blrL", 	"sl_j5_tge4_blrH", 	"sl_j4_t3_blrL", 	"sl_j4_t3_blrH", 	"sl_j4_tge4_blrL", 	"sl_j4_tge4_blrH"]],

    ["sl", ["sl_j4_t3", 	"sl_j4_tge4", 	"sl_j5_t3", 	"sl_j5_tge4", 	"sl_jge6_t2", 	"sl_jge6_t3", 	"sl_jge6_tge4"]],
    ["sl_bdt", ["sl_j4_t3_bdt", 	"sl_j4_tge4_bdt", 	"sl_j5_t3_bdt", 	"sl_j5_tge4_bdt", 	"sl_jge6_t2_bdt", 	"sl_jge6_t3_bdt", 	"sl_jge6_tge4_bdt"]],

]


	


	
     

	


    
nice_names = {
    "sl_j4_t3"          : "SL: =4j =3b",
    "sl_j4_tge4"        : "SL: =4j $\geq$3b",
    "sl_j5_t3"          : "SL: =5j = 3b",
    "sl_j5_tge4"        : "SL: =5j $\geq$4b",
    "sl_jge6_t2"        : "SL: $\geq$6j  =2b",
    "sl_jge6_t3"        : "SL: $\geq$6j  =3b",
    "sl_jge6_tge4"      : "SL: $\geq$6j  $\geq$4b",
    "sl_jge6_tge4_blrL" : "SL: $\geq$6j  $\geq$4b, low BLR",
    "sl_jge6_tge4_blrH" : "SL: $\geq$6j  $\geq$4b, high BLR",

    "sl_j4_t3_bdt"          : "SL: =4j =3b",
    "sl_j4_tge4_bdt"        : "SL: =4j $\geq$3b",
    "sl_j5_t3_bdt"          : "SL: =5j = 3b",
    "sl_j5_tge4_bdt"        : "SL: =5j $\geq$4b",
    "sl_jge6_t2_bdt"        : "SL: $\geq$6j  =2b",
    "sl_jge6_t3_bdt"        : "SL: $\geq$6j  =3b",
    "sl_jge6_tge4_bdt"      : "SL: $\geq$6j  $\geq$4b",
    
    "dl_j3_t2"      : "DL: =3j =2b",
    "dl_j3_t3"      : "DL: =3j =3b",
    "dl_jge4_t2"    : "DL: $\geq$4j =2b",
    "dl_jge4_t3"    : "DL: $\geq$4j =3b",
    "dl_jge4_tge4"  : "DL: $\geq$4j $\geq$4b",
    
    "group_sl"      : "SL comb.",
    "group_sl_7cat" : "SL comb. (7 cats)",
    "group_dl"      : "DL comb.",

    "group_sldl_7cat" : "SL(MEM) + DL",
    "group_sldl_7cat_blrsplit": "SL(MEM+BLR) + DL",
    "group_sldl_7cat_bdt" : "SL(BDT, 7cat) + DL",
    "group_sldl_7cat_2d" : "SL(2d) + DL",

    "group_sl_7cat" : "SL(MEM)",
    "group_sl_7cat_blrsplit": "SL(MEM+BLR)",
    "group_sl_7cat_bdt" : "SL(BDT, 7cat)",
    "group_sl_7cat_2d" : "SL(2d)",

    "sl_jge6_t2_bdtL"     :   "sl_jge6_t2_bdtL",
    "sl_jge6_t2_bdtH"     :   "sl_jge6_t2_bdtH" ,
    "sl_jge6_t3_bdtL"     :   "sl_jge6_t3_bdtL", 
    "sl_jge6_t3_bdtH"     :   "sl_jge6_t3_bdtH", 
    "sl_jge6_tge4_bdtL"   :   "sl_jge6_tge4_bdtL",
    "sl_jge6_tge4_bdtH"   :   "sl_jge6_tge4_bdtH",
    "sl_j5_t3_bdtL"       :   "sl_j5_t3_bdtL",   
    "sl_j5_t3_bdtH"       :   "sl_j5_t3_bdtH",   
    "sl_j5_tge4_bdtL"     :   "sl_j5_tge4_bdtL", 
    "sl_j5_tge4_bdtH"     :   "sl_j5_tge4_bdtH", 
    "sl_j4_t3_bdtL"       :   "sl_j4_t3_bdtL" ,  
    "sl_j4_t3_bdtH"       :   "sl_j4_t3_bdtH" ,  
    "sl_j4_tge4_bdtL"     :   "sl_j4_tge4_bdtL", 
    "sl_j4_tge4_bdtH"     :   "sl_j4_tge4_bdtH", 

    "sl_jge6_t2_blrL"     :   "sl_jge6_t2_blrL",
    "sl_jge6_t2_blrH"     :   "sl_jge6_t2_blrH" ,
    "sl_jge6_t3_blrL"     :   "sl_jge6_t3_blrL", 
    "sl_jge6_t3_blrH"     :   "sl_jge6_t3_blrH", 
    "sl_jge6_tge4_blrL"   :   "sl_jge6_tge4_blrL",
    "sl_jge6_tge4_blrH"   :   "sl_jge6_tge4_blrH",
    "sl_j5_t3_blrL"       :   "sl_j5_t3_blrL",   
    "sl_j5_t3_blrH"       :   "sl_j5_t3_blrH",   
    "sl_j5_tge4_blrL"     :   "sl_j5_tge4_blrL", 
    "sl_j5_tge4_blrH"     :   "sl_j5_tge4_blrH", 
    "sl_j4_t3_blrL"       :   "sl_j4_t3_blrL" ,  
    "sl_j4_t3_blrH"       :   "sl_j4_t3_blrH" ,  
    "sl_j4_tge4_blrL"     :   "sl_j4_tge4_blrL", 
    "sl_j4_tge4_blrH"     :   "sl_j4_tge4_blrH", 
















}


########################################
# Actual work
########################################

# Get unique list of limits we need
# (one limit might be use din more than one plot)
all_limits = []
for plot in plots:
    all_limits.extend(plot[1])
all_limits = list(set(all_limits))

# Get the limits
lims = {}
for k in all_limits:
    lims[k] = get_limits(os.path.join(limits_base,"higgsCombineshapes_group_{0}.Asymptotic.mH120.root".format(k)))

# Do the plots
for plot in plots:

    plot_name = plot[0]
    cats = plot[1]

    plt.clf()

    plt.figure(figsize=(5, 5))
    ax = plt.axes()
    plotlib.brazilplot(
        axes=ax,
        limits=lims,
        categories=cats,
        category_names=[nice_names[cat] for cat in cats],
    )

    plotlib.svfg("limits/{0}.png".format(plot_name))
