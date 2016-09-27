
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
limits_base = "/mnt/t3nfs01/data01/shome/gregor/VHBB-8019/CMSSW_8_0_19/src/TTH/MEAnalysis/rq/results/9a1a848d-7783-4140-8bc4-36a153738067/limits/"

# List of plots
# plots: list with two entries
#          -first entry: desired output filename
#          -second entry: list of limit names to include in plot
plots = [
    ["sl",["sl_j4_t3", "sl_j4_tge4", "sl_j5_t3", "sl_j5_tge4", "sl_jge6_t2", "sl_jge6_t3", "sl_jge6_tge4", "group_sl"]],
    ["dl",["dl_j3_t2", "dl_j3_t3", "dl_jge4_t2", "dl_jge4_t3", "dl_jge4_tge4","group_dl"]],
    ["comb", ["group_sl", "group_dl", "group_sldl"]]
]

nice_names = {
    "sl_j4_t3"    : "SL: =4j =3b",
    "sl_j4_tge4"  : "SL: =4j $\geq$3b",
    "sl_j5_t3"    : "SL: =5j = 3b",
    "sl_j5_tge4"  : "SL: =5j $\geq$4b",
    "sl_jge6_t2"  : "SL: $\geq$6j  =2b",
    "sl_jge6_t3"  : "SL: $\geq$6j  =3b",
    "sl_jge6_tge4": "SL: $\geq$6j  $\geq$4b",
    
    "dl_j3_t2"    : "DL: =3j =2b",
    "dl_j3_t3"    : "DL: =3j =3b",
    "dl_jge4_t2"  : "DL: $\geq$4j =2b",
    "dl_jge4_t3"  : "DL: $\geq$4j =3b",
    "dl_jge4_tge4": "DL: $\geq$4j $\geq$4b",
    
    "group_sl"    : "SL comb.",
    "group_dl"    : "DL comb.",
    "group_sldl"  : "SL+DL comb.",
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
