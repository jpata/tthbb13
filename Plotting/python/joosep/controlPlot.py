import ROOT
import rootpy

import matplotlib
from matplotlib import rc
#temporarily disable true latex for fast testing
rc('text', usetex=False)
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from rootpy.plotting import root2matplotlib as rplt

import sys, os
import heplot, plotlib

from rootpy.plotting import Hist
from collections import OrderedDict

inf = rootpy.io.File("/Users/joosep/sl_jge6_tge4.root")
procs_names = [
    ("ttH_hbb", "tt+H(bb)"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc")
]
procs = [x[0] for x in procs_names]

category = "sl_jge6_tge4"
variable = "jetsByPt_0_pt"
variable_name = "jet $p_t$"

fig = plt.figure(figsize=(6,6))

#optional function f: TH1D -> TH1D to blind data
def blind(h):
    hc = h.Clone()
    for i in range(h.GetNbinsX()+1):
        hc.SetBinContent(i, 0)
        hc.SetBinError(i, 0)
    return hc

r = plotlib.draw_data_mc(
    inf,
    "{0}/{1}".format(category, variable),
    procs_names,
    ["ttH_hbb"],
    dataname="data", #data_obs for fake data
    rebin=2,
    xlabel=variable,
    xunit="GeV",
    legend_fontsize=10, legend_loc="best",
    colors=[plotlib.colors.get(p) for p in procs],
    do_legend=True,
    show_overflow=True,
    title_extended="$,\\ \\mathcal{L}=9.2,\\ \\mathrm{fb}^{-1}$, ",
    systematics=[],
    blindFunc=blind,
    #do_pseudodata=True
)
plotlib.svfg("./out.pdf")
