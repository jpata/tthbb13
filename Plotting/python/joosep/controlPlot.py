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

inf = "/mnt/t3nfs01/data01/shome/jpata/tth/gc/makecategory/GC41c32de9adb2/SL_7cat/sl_jge6_tge4.root"
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
    plotlib.svfg("./{0}".format(outname))
    inf.Close()

args = [
    {
    "infile": inf,
    "histname": "/".join([category, variable]),
    "outname": "_".join([category, variable]),
    "procs": procs_names,
    "signal_procs": ["ttH_hbb"],
    "dataname": "data", #data_obs for fake data
    "rebin": 2,
    "xlabel": variable_name,
    "xunit": "GeV",
    "legend_fontsize": 10,
    "legend_loc": "best",
    "colors": [plotlib.colors.get(p) for p in procs],
    "do_legend": True,
    "show_overflow": True,
    "title_extended": r"$,\ \mathcal{L}=9.2,\ \mathrm{fb}^{-1}$, ",
    "systematics": [],
    "blindFunc": blind,
    }
]

if __name__ == "__main__":
    for i in range(1000):
        a = copy.deepcopy(args[0])
        a["outname"] = "plot_{0}.pdf".format(i)
        args += [a]
    
    import multiprocessing
    pool = multiprocessing.Pool(10)
    pool.map(plot_worker, args)
    pool.close()
