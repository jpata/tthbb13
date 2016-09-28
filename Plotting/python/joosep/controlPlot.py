import pdb

import ROOT
import logging


import matplotlib
from matplotlib import rc
import matplotlib.pyplot as plt

import sys, os, copy
import os.path
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
#    ("qcd_ht300to500", "qcd ht 300 500"),
#    ("qcd_ht300to500", "qcd ht 300 500"),
#    ("qcd_ht500to700", "qcd ht 500 700"),
#    ("qcd_ht700to1000", "qcd ht 700 1."),
#    ("qcd_ht1000to1500", "qcd ht 1. 1.5"),
#    ("qcd_ht1500to2000", "qcd ht 1.5 2."),
#    ("qcd_ht2000toinf", "qcd ht 2. inf "),



]
procs = [x[0] for x in procs_names]


syst_pairs = []

syst_pairs.extend([
    ("_puUp", "_puDown"),
    ("_CMS_scale_jUp", "_CMS_scale_jDown"),
    ("_CMS_res_jUp", "_CMS_res_jDown"),
    ("_CMS_ttH_CSVcferr1Up", "_CMS_ttH_CSVcferr1Down"),
    ("_CMS_ttH_CSVcferr2Up", "_CMS_ttH_CSVcferr2Down"),
    ("_CMS_ttH_CSVhfUp", "_CMS_ttH_CSVhfDown"),
    ("_CMS_ttH_CSVhfstats1Up", "_CMS_ttH_CSVhfstats1Down"),
    ("_CMS_ttH_CSVhfstats2Up", "_CMS_ttH_CSVhfstats2Down"),
    ("_CMS_ttH_CSVjesUp", "_CMS_ttH_CSVjesDown"),
    ("_CMS_ttH_CSVlfUp", "_CMS_ttH_CSVlfDown"),
    ("_CMS_ttH_CSVlfstats1Up", "_CMS_ttH_CSVlfstats1Down"),
    ("_CMS_ttH_CSVlfstats2Up", "_CMS_ttH_CSVlfstats2Down")
])

#optional function f: TH1D -> TH1D to blind data
def blind(h):
    hc = h.Clone()
    for i in range(h.GetNbinsX()+1):
        hc.SetBinContent(i, 0)
        hc.SetBinError(i, 0)
    return hc

def plot_syst_updown(nominal, up, down):
    plt.figure(figsize=(6,6))
    heplot.barhist(nominal, color="black")
    heplot.barhist(up, color="red")
    heplot.barhist(down, color="blue")

def blind_mem(h):
    h = h.Clone()
    for ibin in range(1, h.GetNbinsX()+1):
        if ibin >= h.GetNbinsX()/2:
            h.SetBinContent(ibin, 0)
            h.SetBinError(ibin, 0)
    return h

def no_blind(h):
    return h

blind_funcs = {
    "blind_mem": blind_mem,
    "no_blind": no_blind,
}

def plot_worker(kwargs):
    #temporarily disable true latex for fast testing
    rc('text', usetex=False)
    matplotlib.use('PS') #needed on T3

    inf = rootpy.io.File(kwargs.pop("infile"))
    outname = kwargs.pop("outname")
    histname = kwargs.pop("histname")
    procs = kwargs.pop("procs")
    signal_procs = kwargs.pop("signal_procs")
    do_syst = kwargs.pop("do_syst")
   
    if kwargs.has_key("blindFunc"):
        blind = kwargs.pop("blindFunc")
        if blind_funcs.has_key(blind):
            kwargs["blindFunc"] = blind_funcs[blind]

    fig = plt.figure(figsize=(6,6))
    ret = plotlib.draw_data_mc(
        inf,
        histname,
        procs,
        signal_procs,
        **kwargs
    )
    

    logging.info("saving {0}".format(outname))
    plotlib.svfg(outname + ".pdf")
    plotlib.svfg(outname + ".png")
    plt.clf()

    if do_syst:
        for samp, sampname in procs:
            hnom = ret["nominal"][samp]
            for systUp, systDown in kwargs["systematics"]:
                syst_name = systUp[1:-2]
                hup = ret["systematic"][systUp][samp]
                hdown = ret["systematic"][systDown][samp]
                plot_syst_updown(hnom, hup, hdown)
                outname_syst = os.path.join(outname, syst_name, samp)
                logging.info("saving systematic {0}".format(outname_syst))
                plotlib.svfg(outname_syst + ".pdf")
                plotlib.svfg(outname_syst + ".pdf")
                plt.clf()

    inf.Close()

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
        "systematics": syst_pairs,
        "do_syst": True,
        "blindFunc": "blind_mem" if "mem" in variable else "no_blind",
    }

if __name__ == "__main__":


    # Plot for all SL categories
    simple_vars = [
        "jetsByPt_0_pt", 
        "leps_0_pt",  
        "btag_LR_4b_2b_btagCSV_logit",
        "common_mem"
    ]

    cats = [
        "sl_jge6_tge4",
        "dl_jge4_tge4",
    ]

    args = []

    args += [get_base_plot(
        "/mnt/t3nfs01/data01/shome/jpata/tth/sw/CMSSW/src/TTH/MEAnalysis/rq/results/fa2ce3d2-edce-4482-b1f7-eda9e46bd1b7/",
        "test", "categories", cat, var) for cat in cats for var in simple_vars 
    ]

    for arg in args:
        plot_worker(arg)

