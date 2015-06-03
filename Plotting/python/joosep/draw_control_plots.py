import ROOT
ROOT.gROOT.SetBatch(True)

import matplotlib
import matplotlib.pyplot as plt

import numpy as np

import rootpy
import rootpy.io
from rootpy.plotting.root2matplotlib import errorbar, bar, hist, fill_between
from collections import OrderedDict

from weighting import get_weight

matplotlib.rc("axes", labelsize=24)
matplotlib.rc("axes", titlesize=20)

def mc_stack(hlist, colors="auto"):
    if colors=="auto":
        coloriter = iter(plt.cm.jet(np.linspace(0,1,len(hlist))))
        for h in hlist:
            h.color = next(coloriter)
    elif isinstance(colors, list) and len(color) == len(hlist):
        for h, c in zip(hlist, colors):
            h.color = c

    for h in hlist:
        h.fillstyle = "solid"

    r = hist(hlist, stacked=True)
    htot = sum(hlist)
    htot.color="black"

    htot_u = htot.Clone()
    htot_d = htot.Clone()
    for i in range(1, htot.nbins()+1):
        htot_u.set_bin_content(i, htot.get_bin_content(i) + htot.get_bin_error(i))
        htot_d.set_bin_content(i, htot.get_bin_content(i) - htot.get_bin_error(i))

    htot_u.color="black"
    htot_d.color="black"

    fill_between(htot_u, htot_d,
        color="black", hatch="////",
        alpha=1.0, linewidth=0, facecolor="none", edgecolor="black", zorder=10,
    )

    return {"tot":htot, "tot_u":htot_u, "tot_d":htot_d}

def dice(h, nsigma=1.0):
    hret = h.clone()
    for i in range(1, h.nbins()+1):
        m, e = h.get_bin_content(i), h.get_bin_error(i)
        if e<=0:
            e = 1.0
        n = np.random.normal(m, nsigma*e)
        hret.set_bin_content(i, n)
    return hret

def draw_data_mc(tf, hname, samples, **kwargs):

    do_pseudodata = kwargs.get("do_pseudodata", False)
    xlabel = kwargs.get("xlabel", hname.replace("_", " "))
    yunit = kwargs.get("yunit", "")
    ylabel = kwargs.get("ylabel", "auto")
    rebin = kwargs.get("rebin", 1)
    title_extended = kwargs.get("title_extended", "")
    do_legend = kwargs.get("do_legend", True)

    hs = OrderedDict()
    for sample, sample_name in samples:
        hs[sample] = tf.get(sample + "/" + hname).Clone()
        hs[sample].Scale(get_weight(sample))
        hs[sample].title = sample_name
        hs[sample].rebin(rebin)

    c = plt.figure(figsize=(6,6))
    a1 = plt.axes([0.0,0.2, 1.0, 0.8])
    plt.grid()
    plt.title("CMS preliminary simulation\n $\sqrt{s} = 13$ TeV"+title_extended,
        y=0.96, x=0.04,
        horizontalalignment="left", verticalalignment="top"
    )
    r = mc_stack(hs.values())

    tot_mc = sum(hs.values())
    tot_mc.title = "pseudodata"
    tot_mc.color = "black"

    tot_bg = sum([hs[k] for k in hs.keys() if "tth" not in k])

    pseudodata = dice(tot_mc, nsigma=1.0)

    if do_pseudodata:
        errorbar(pseudodata)

    if do_legend:
        plt.legend(loc=1, numpoints=1)
    if ylabel == "auto":
        ylabel = "events / {0:.0f} {1}".format(hs.values()[0].get_bin_width(1), yunit)
    plt.ylabel(ylabel)

    #hide x ticks on main panel
    ticks = a1.get_xticks()
    a1.set_xticklabels([])

    a1.set_ylim(bottom=0, top=1.1*a1.get_ylim()[1])

    a2 = plt.axes([0.0,0.0, 1.0, 0.2])

    plt.xlabel(xlabel)
    a2.grid()

    data_minus_bg = pseudodata - tot_mc
    data_minus_bg.divide(pseudodata)

    bg_unc_u = r["tot"] - r["tot_u"]
    bg_unc_d = r["tot"] - r["tot_d"]

    bg_unc_u.divide(pseudodata)
    bg_unc_d.divide(pseudodata)

    if do_pseudodata:
        errorbar(data_minus_bg)

    fill_between(bg_unc_u, bg_unc_d,
        color="black", hatch="////",
        alpha=1.0, linewidth=0, facecolor="none", edgecolor="black", zorder=10,
    )
    plt.ylabel("$\\frac{\mathrm{data} - \mathrm{mc}}{\mathrm{data}}$", fontsize=16)
    plt.axhline(0.0, color="black")
    a2.set_ylim(-1,1)
    #hide last tick on ratio y axes
    a2.set_yticks(a2.get_yticks()[:-1]);
    a2.set_xticks(ticks);
    return a1, a2, hs


def draw_mem_data_mc(*args, **kwargs):
    a1, a2, hs = draw_data_mc(*args, **kwargs)
    plt.sca(a1)
    h = hs["tth_13TeV_phys14"].Clone()
    h.fillstyle = "hollow"
    h.linewidth = 2
    h.title = h.title + " x10"
    h.Scale(10)
    hist(h)
    plt.legend(loc=(1.01,0.0))
    a1.set_ylim(bottom=0)
    return a1, a2, hs

def calc_roc(h1, h2):
    h1 = h1.Clone()
    h2 = h2.Clone()
    h1.Scale(1.0 / h1.Integral())
    h2.Scale(1.0 / h2.Integral())
    roc = np.zeros((h1.GetNbinsX()+2, 2))
    err = np.zeros((h1.GetNbinsX()+2, 2))
    e1 = ROOT.Double(0)
    e2 = ROOT.Double(0)
    for i in range(0, h1.GetNbinsX()+2):
        I1 = h1.Integral(0, h1.GetNbinsX())
        I2 = h2.Integral(0, h2.GetNbinsX())
        if I1>0 and I2>0:
            roc[i, 0] = float(h1.IntegralAndError(i, h1.GetNbinsX()+2, e1)) / I1
            roc[i, 1] = float(h2.IntegralAndError(i, h1.GetNbinsX()+2, e2)) / I2
            err[i, 0] = e1
            err[i, 1] = e2
    return roc, err

def draw_rocs(tf, pairs, **kwargs):
    rebin = kwargs.get("rebin", 1)

    c = plt.figure(figsize=(6,6))
    plt.axes()
    plt.plot([0.0,1.0],[0.0,1.0], color="black")
    plt.xlim(0,1)
    plt.ylim(0,1)

    rs = []
    es = []
    for pair in pairs:
        hn1, hn2, label = pair
        h1 = tf.get(hn1).Clone()
        h2 = tf.get(hn2).Clone()
        h1.rebin(rebin)
        h2.rebin(rebin)
        r, e = calc_roc(h1, h2)
        rs += [r]
        es += [e]

    for (r, e, pair) in zip(rs, es, pairs):
        hn1, hn2, label = pair
        plt.errorbar(r[:, 0], r[:, 1], e[:, 0], e[:, 1], label=label)

    plt.legend(loc=2)
