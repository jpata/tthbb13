import ROOT
import rootpy
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rootpy.plotting import root2matplotlib as rplt

import sys
sys.path += ["/Users/joosep/Documents/heplot"]
import heplot

import plotlib
import os

from rootpy.plotting import Hist
from collections import OrderedDict

inf = rootpy.io.File("/Users/joosep/sl_jge6_tge4.root")
procs_names = [
    ("ttH_hbb", "tthbb"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc")
]

procs = [p[0] for p in procs_names]
category = "sl_jge6_tge4"
variable = "jetsByPt_0_pt"
variable_name = "$p_t$"

fig = plt.figure(figsize=(6,6))
r = plotlib.draw_data_mc(
    inf,
    "{0}/{1}".format(category, variable),
    procs_names,
    dataname="data",
    rebin=2,
    xlabel=variable,
    xunit="",
    legend_fontsize=10, legend_loc="best",
    colors=[plotlib.colors.get(p) for p in procs],
    do_legend=True,
    show_overflow=True,
    title_extended="$,\\ \\mathcal{L}=9.6,\\ \\mathrm{fb}^{-1}$, ",
    systematics=[],
    #blindFunc=blind,
    #do_pseudodata=True
)
plotlib.svfg("./out.pdf")
