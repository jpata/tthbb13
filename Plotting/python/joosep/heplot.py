import matplotlib
import rootpy.plotting.root2matplotlib as rplt
import matplotlib.pyplot as plt
#from rootpy.plotting import Hist, Hist2D, HistStack
#from rootpy.io.file import root_open
import sys
import numpy as np
import matplotlib.gridspec as gridspec
import math
from matplotlib.ticker import AutoMinorLocator

#matplotlib.rc('font', family='sans-serif') 
matplotlib.rc('font', serif='Arial') 
matplotlib.rc('text', usetex='true') 
matplotlib.rcParams.update({'font.size': 16})

def normalize(h):
    if (h.Integral() > 0):
        h.Scale(1.0 / h.Integral())

def round_mult(x):
    p = int(math.log(x, 10))
    m = math.pow(10, p)
    print "pre", p, m, x/m
    if (x/m < 2):
        p = p - 1
        m = math.pow(10, p)
        print "by 2", p, m, x/m
    return m, int(math.ceil(x/m)) * m

def set_hist_axes(h, ax):
    ax.grid(which="major", lw=1, ls="-")
    ax.grid(which="minor", lw=1, ls="--")
    ax.grid(which="minor", lw=0, ls="--", axis="x")
    spacing, top = round_mult(h.GetMaximum())
    ax.set_yticks(np.arange(0, top+1, spacing))
    ax.set_yticks(np.arange(0, top+1, spacing/5), minor=True)
    ax.set_xticks(np.arange(h.GetBinLowEdge(1), h.GetBinLowEdge(h.GetNbinsX()) + h.GetBinWidth(1), h.GetBinWidth(1)), minor=True)
    ax.set_ylim(bottom=0, top=top)

def as_array(x):
    
#     dims = []
#     if x.GetNbinsX()>0:
#         dims += [x.GetNbinsX()+2]
#     if x.GetNbinsY()>0:
#         dims += [x.GetNbinsY()+2]
#     if x.GetNbinsZ()>0:
#         dims += [x.GetNbinsZ()+2]
    arr = np.zeros((x.GetNbinsX(), x.GetNbinsY(), x.GetNbinsZ()), dtype=np.float64)
    for i in range(1, x.GetNbinsX() + 1):
        for j in range(1, x.GetNbinsY() + 1):
            for k in range(1, x.GetNbinsZ() + 1):
                arr[i-1, j-1, k-1] = x.GetBinContent(i,j,k)
    # print arr
    if x.GetNbinsZ() == 1:
        arr = arr.sum(2)
    elif x.GetNbinsY() == 1 and x.GetNbinsZ() == 1:
        arr = arr.sum((1,2))
    elif x.GetNbinsZ() == 1:
        arr = arr.sum(2)
    elif x.GetNbinsY() == 1:
        arr = arr.sum(1)
    return arr#.sum(1).sum(1)

def barhist(h, **kwargs):
    """
    Draws a ROOT TH1 histogram h as a pyplot line.

    kwargs:
        color,
        lw,
        fillstyle,
        label,
        scaling: number of "normed",
        rebin: number
    """
    col = kwargs.pop("color", "blue")

    #b = rplt.errorbar(h, xerr=False, color=col, mec=col, ms=0, ecolor=col, **kwargs)
    lw = kwargs.pop("lw", 1)
    fs = kwargs.pop("fillstyle", False)
    lab = kwargs.pop("label", "")
    scaling = kwargs.pop("scaling", 1.0)
    rebin = kwargs.pop("rebin", 1)
    kwargs_d = dict(kwargs)
    
    if scaling == "normed":
        if h.Integral()>0:
            scaling = 1.0 / h.Integral()
        else:
            scaling = 0.0
    h = h.Clone()
    h.Scale(scaling)    
    h.Rebin(rebin)
    h.fillstyle = "hollow"
    b = rplt.bar(h, lw=0, color="none", ecolor=col, label=None, **kwargs)
    xs = []
    ys = []
    for _b in b:
        xs += [_b.xy[0], _b.xy[0]+_b.get_width()]
        ys += [_b.xy[1]+_b.get_height(), _b.xy[1]+_b.get_height()]
        _b.set_hatch(fs)
        _b.set_color(col)
        plt.gca().add_patch(_b)
    #kwargs_d.pop("lw")
    kwargs_d.pop("edgecolor", "")
    kwargs_d.pop("stacked", "")
    #plt.xticks(np.arange(min(xs), max(xs), (max(xs)-min(xs)) / ))
    plt.plot(xs, ys, color=col, lw=lw, label=lab, **kwargs_d)
    return b

def stackhist(histograms, **kwargs):
    stack = HistStack(histograms, drawstyle='HIST E1 X0')
    b = barhist(stack, stacked=True)
    return b

def matshow(ax, hpt, **kwargs):
    arr = as_array(hpt)
    #print arr

    #Need to rotate 90 degrees ccw to conform to ROOT-s standard
    arr = np.rot90(arr) 
    #print arr
    assert(len(arr.shape) == 2) 
    ret = ax.matshow(arr,
        cmap="hot",
        interpolation="none",
        #origin="lower",
        aspect="auto",
        extent=[
            hpt.GetXaxis().GetBinLowEdge(1),
            hpt.GetXaxis().GetBinLowEdge(hpt.GetNbinsX()) + hpt.GetXaxis().GetBinWidth(hpt.GetNbinsX()),
            hpt.GetYaxis().GetBinLowEdge(1),
            hpt.GetYaxis().GetBinLowEdge(hpt.GetNbinsY()) + hpt.GetYaxis().GetBinWidth(hpt.GetNbinsY()),
        ]
    )
    
    return ret

def ratio_axes(fig):
    gs = gridspec.GridSpec(2, 1, height_ratios=[2,1])
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax1.tick_params(
        axis='both',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='on',
        top='on',
        width=1, 
        labelbottom='off'  # labels along the bottom edge are off
    )
    ax2.tick_params(
        axis='both',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='on',
        top='on', 
        width=1, 
    )
   
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_minor_locator(AutoMinorLocator())

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.02, bottom=0.1, left=0.1, right=0.9, top=0.9)
    #ax2.yaxis.set_ticks_position('right')
    #fig.subplots_adjust(hspace=0.2)
    return ax1, ax2
    
def grouped_histograms_sameax(grouped, **kwargs):
    """
    g = dt.groupby("cl")
    
    gs = g.apply(
        lambda x: np.histogram(
            x["pt"],
            bins=np.linspace(20, 400, 11)
        )
    )
    fig = plt.figure(figsize=(10,10))
    ax = plt.axes()
    grouped_histograms_sameax(gs, keynames=["b", "c", "udsg"], ax=ax)

    """
    ks = grouped.keys()
    keynames = kwargs.get("keynames", [str(k) for k in ks])
    ax = kwargs.get("ax", None)
    if ax is None:
        ax = plt.axes()
    
    errors = kwargs.get("errors", None)
    scaling = kwargs.get("scaling", None)
    linestyle = kwargs.get("ls", "-")
    colcycle = ax._get_lines.color_cycle
    for k, kn in zip(ks, keynames):
        col = colcycle.next()
        ys = grouped[k][0]
        xs = grouped[k][1]
        
        if errors is None:
            es = np.sqrt(ys)
        elif errors=="histogram":
            es =  grouped[k][2]
        elif errors==False:
            es =  0.0 * ys
        if scaling is None:
            I = 1.0
        elif scaling=="normalize":
            I = float(np.sum(ys))
        
        ys = ys/I
        es = es/I
        ys = list(ys)
        ys.append(ys[-1])
        es = list(es)
        es.append(es[-1])
        xs = list(xs)
        plt.step(xs, ys, color=col, label=kn,lw=2, where="post", ls=linestyle)
        xs.append(xs[-1])
        plt.errorbar(xs[:-1]+np.diff(xs)/2, ys, es, color=col, lw=2, ls="")

def grouped_errorbars(grouped, **kwargs):
    ks = grouped.keys()
    ax = kwargs.get("ax", plt.axes())
    colcycle = ax._get_lines.color_cycle
    col = colcycle.next()
    xs = range(len(ks))
    xnames = kwargs.get("xnames", map(str, ks))
    ys = [grouped[k][0] for k in ks]
    es = np.array([grouped[k][1] for k in ks])
    plt.xticks(xs, xnames)
    ax.plot(xs, ys, marker="o", color=col, label=kwargs.get("label", ""))
    ax.fill_between(xs, es[:, 0], es[:, 1], alpha=0.2, color=col, interpolate=True)
