import pdb

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

DO_PARALLEL = False

procs_names = [
    ("ttH_hbb", "tt+H(bb)"),
    ("ttH_nonhbb", "tt+H(non-bb)"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc"),
]
procs = [x[0] for x in procs_names]

def plot_worker(kwargs):
    inf = rootpy.io.File(kwargs.pop("infile"))

    histname = kwargs.pop("histname")
    procs = kwargs.pop("procs")
    signal_procs = kwargs.pop("signal_procs")
    do_syst = kwargs.pop("do_syst")

    fig = plt.figure(figsize=(6,6))
    ret = plotlib.draw_data_mc(
        inf,
        histname,
        procs,
        signal_procs,
        **kwargs
    )    
    inf.Close()

    return ret["counts"]

    
def get_base_plot(basepath, outpath, analysis, category, variable):
    s = "{0}/{1}/{2}".format(basepath, analysis, category)
    return {
        "infile": s + ".root",
        "histname": "/".join([category, variable]),
        "outname": "/".join(["out", outpath, analysis, category, variable]),
        "procs": procs_names,
        "signal_procs": ["ttH_hbb"],
        "dataname": "data", #data_obs for fake data
        "rebin": 1,
        "xlabel": plotlib.varnames[variable] if variable in plotlib.varnames.keys() else "PLZ add me to Varnames", 
        "xunit": plotlib.varunits[variable] if variable in plotlib.varunits.keys() else "" ,
        "legend_fontsize": 12,
        "legend_loc": "best",
        "colors": [plotlib.colors.get(p) for p in procs],
        "do_legend": True,
        "show_overflow": True,
        "title_extended": r"$,\ \mathcal{L}=00.0\ \mathrm{fb}^{-1}$, ",
        "do_syst": False,
    }

if __name__ == "__main__":

    cats_sl = [
        "sl_jge6_t2", "sl_jge6_t3", "sl_jge6_tge4_blrL", "sl_jge6_tge4_blrH"]

#GC682c0f46bbb3
    version = "GC47652568915d"

    var = "jetsByPt_0_pt"

    counts = {}

    for cat in cats_sl:
        counts[cat] = plot_worker(get_base_plot("/mnt/t3nfs01/data01/shome/gregor/tth/gc/makecategory/"+version,
                                                "Aug12", 
                                                "SL_7cat", 
                                                cat, 
                                                var))
    
    
    samples = counts["sl_jge6_t2"].keys()

    counts["all"] = {}

    for sample in samples:
    
        counts["all"][sample] = 0
    
        for cat in cats_sl:
            counts["all"][sample] += counts[cat][sample]

    for sample in samples:
        print "{0: <30}: {1: >7.0f} {2: >7.4f} {3: >7.4f} {4: >7.4f} {5: >7.4f}".format(sample, 
                                                                                        counts["all"][sample], 
                                                                                        counts[cats_sl[0]][sample]/counts["all"][sample], 
                                                                                        counts[cats_sl[1]][sample]/counts["all"][sample], 
                                                                                        counts[cats_sl[2]][sample]/counts["all"][sample],
                                                                                        counts[cats_sl[3]][sample]/counts["all"][sample])


        
    
    

