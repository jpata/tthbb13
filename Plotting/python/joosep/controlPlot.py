import ROOT
import logging

import matplotlib
from matplotlib import rc
#temporarily disable true latex for fast testing
rc('text', usetex=False)
matplotlib.use('PS') #needed on T3
import matplotlib.pyplot as plt

import sys, os, copy
from collections import OrderedDict
import heplot, plotlib

import rootpy
from rootpy.plotting import Hist
from rootpy.plotting import root2matplotlib as rplt

procs_names = [
    ("ttH_hbb", "tt+H(bb)"),
    ("ttH_nonhbb", "tt+H(non-bb)"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc")
]
procs = [x[0] for x in procs_names]

#optional function f: TH1D -> TH1D to blind data
def blind(h):
    hc = h.Clone()
    for i in range(h.GetNbinsX()+1):
        hc.SetBinContent(i, 0)
        hc.SetBinError(i, 0)
    return hc

def plot_worker(kwargs):
    inf = rootpy.io.File(kwargs.pop("infile"))
    outname = kwargs.pop("outname")
    histname = kwargs.pop("histname")
    procs = kwargs.pop("procs")
    signal_procs = kwargs.pop("signal_procs")

    fig = plt.figure(figsize=(6,6))
    r = plotlib.draw_data_mc(
        inf,
        histname,
        procs,
        signal_procs,
        **kwargs
    )
    logging.info("saving {0}".format(outname))
    path = os.path.dirname(outname)
    if not os.path.isdir(path):
        os.makedirs(path)
    plotlib.svfg(outname + ".pdf")
    inf.Close()


def get_base_plot(basepath, analysis, category, variable):
    s = "{0}/{1}/{2}".format(basepath, analysis, category)
    return {
        "infile": s + ".root",
        "histname": "/".join([category, variable]),
        "outname": "/".join(["out", s, variable]),
        "procs": procs_names,
        "signal_procs": ["ttH_hbb"],
        "dataname": "data", #data_obs for fake data
        "rebin": 1,
        "xlabel": plotlib.varnames[variable],
        "xunit": plotlib.varunits[variable],
        "legend_fontsize": 12,
        "legend_loc": "best",
        "colors": [plotlib.colors.get(p) for p in procs],
        "do_legend": True,
        "show_overflow": True,
        "title_extended": r"$,\ \mathcal{L}=12.9\ \mathrm{fb}^{-1}$, ",
        "systematics": [],
        #"blindFunc": blind,
    }

if __name__ == "__main__":

    vars_base = ["jetsByPt_0_pt"]

    cats_sl = [
        "sl_j4_t3", "sl_j4_tge4",
        "sl_j5_t3", "sl_j5_tge4",
        "sl_jge6_t2", "sl_jge6_t3", "sl_jge6_tge4",
    ]

    cats_dl = [
        "dl_j3_t2",
        "dl_j3_t3",
        "dl_jge4_t2",
        "dl_jge4_t3",
        "dl_jge4_tge4",
    ]


    args = [
        get_base_plot(".", "SL_7cat", cat, var) for cat in cats_sl for var in vars_base
    ]

    args += [get_base_plot(".", "DL", cat, var) for cat in cats_dl for var in vars_base]


    import multiprocessing
    pool = multiprocessing.Pool(4)
    pool.map(plot_worker, args)
    pool.close()

    # map(plot_worker, args)
