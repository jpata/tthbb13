import ROOT
ROOT.gROOT.SetBatch(True)

import matplotlib
import matplotlib.pyplot as plt

import numpy as np

import rootpy
import rootpy.io
from rootpy.plotting.root2matplotlib import errorbar, bar, hist, fill_between
from collections import OrderedDict

import pandas

from weighting import get_weight

import sklearn
import sklearn.metrics
from sklearn.ensemble import GradientBoostingClassifier
import math


matplotlib.rc("axes", labelsize=24)
matplotlib.rc("axes", titlesize=16)

path = "/Users/joosep/Documents/tth/data/ntp/v12/Sep4_fullrun/"
samples = {
    "tth_amcatnlo": [
        path + "/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hbb.root",
        #path + "/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8_hX.root",
    ],
    "tth_phys14": [
        "/Users/joosep/Documents/tth/data/ntp/v10_phys14/Aug20_564f1b8_phys14_ref1/tth_13tev_amcatnlo_pu20bx25_hbb.root"
    ],
    
    
    "ttjets_amcatnlo": [
        path + "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttbb.root",
        path + "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_tt2b.root",
        path + "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttb.root",
        path + "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttcc.root",
        path + "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ttll.root",
    ],
    "ttjets_phys14": [
        "/Users/joosep/Documents/tth/data/ntp/v10_phys14/Aug20_564f1b8_phys14_ref1/ttjets_13tev_madgraph_pu20bx25_phys14.root"
    ],
    "tth_powheg": [
        path + "ttHTobb_M125_13TeV_powheg_pythia8_hbb.root",
        #path + "ttHTobb_M125_13TeV_powheg_pythia8_hX.root",
    ],
    "ttjets_powheg": [
        path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb.root",
        path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b.root",
        path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb.root",
        path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc.root",
        path + "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll.root",
    ],
}

def process_sample_hist(fnames, hname, func, bins, cut, **kwargs):
    tt = ROOT.TChain("tree")
    for fn in fnames:
        tt.Add(fn)
    ROOT.gROOT.cd()
    hs = {}
    h = ROOT.gROOT.Get(hname)
    if h:
        h.Delete()
    h = ROOT.TH1D(hname, "", bins[0], bins[1], bins[2])
    hname = h.GetName()
    h = rootpy.asrootpy(h)
    h.SetDirectory(ROOT.gROOT)
    n = tt.Draw("{0} >> {1}".format(func, hname), cut)
    print n, h.Integral()
    if kwargs.get("norm", False):
        if h.Integral()>0:
            h.Scale(1.0 / h.Integral())
    return h
    
def make_df_hist(bins, x, w=1.0):
    h = rootpy.plotting.Hist(*bins)
    a = np.array(x).astype("float64")
    if isinstance(w, float):
        b = np.repeat(w, len(a)).astype("float64")
    else:
        b = np.array(w).astype("float64")
    h.FillN(len(a), a, b)
    return h
# 
# def augment(d, varlist):
#     d = d[varlist+["id" ,"genWeight"]]
#     newd = copy.deepcopy(d)
#     for c in varlist:
#         m = d[c].mean()
#         s = d[c].std()
#         perturb = np.random.normal(m, s, len(d))
#         newd[c] += perturb
#     ret = pandas.concat((d, newd))
#     return ret
# 
# def augment_multi(d, varlist, n):
#     if n>0:
#         return augment_multi(augment(d, varlist), varlist, n-1)
#     else:
#         return augment(d, varlist)
#         


def cls_hists(cls, df, var, bins=None):
    if bins is None:
        bins = (101,0.0,1.0)

    probs1 = cls.predict_proba(df[df["id"]==1][var])[:, 1]
    probs2 = cls.predict_proba(df[df["id"]==0][var])[:, 1]

    h1 = make_df_hist(bins, probs1, df[df["id"]==1]["genWeight"])
    h2 = make_df_hist(bins, probs2, df[df["id"]==0]["genWeight"])

    # h1 = make_df_hist(bins, probs1)
    # h2 = make_df_hist(bins, probs2)

    # h1tr = make_df_hist(bins, probs1tr)
    # h2tr = make_df_hist(bins, probs2tr)

    for h in [h1, h2]:
        h.Scale(1.0 / h.Integral())
    return h1, h2
    
    
def draw_cls_hists(cls, d1, d2, var):
    h1, h2 = cls_hists(cls, d1, var)
    h1tr, h2tr = cls_hists(cls, d2, var)

    h1.color = "red"
    h2.color = "blue"
    h1tr.color = "red"
    h2tr.color = "blue"

    errorbar(h1)
    errorbar(h2)
    h1tr.linestyle = "dashed"
    h2tr.linestyle = "dashed"
    hist(h1tr, ls="--")
    hist(h2tr, ls="--")
    
def draw_roc(cls, df_test, var, df_train=None):
    h1, h2 = cls_hists(cls, df_test, var)
    
    r, e = calc_roc(h1, h2)
    if not df_train is None:
        h1tr, h2tr = cls_hists(cls, df_train, var)
        rtr, etr = calc_roc(h1tr, h2tr)
    plt.figure(figsize=(6,6))
    plt.grid()
    plt.plot([0,1],[0,1], color="black")
    plt.errorbar(r[:, 0], r[:, 1], e[:, 0], e[:, 1], marker="o", label="test")
    if not df_train is None:
        plt.errorbar(rtr[:, 0], rtr[:, 1], etr[:, 0], etr[:, 1], marker="x", label="train")
    plt.axvline(0.5, color="black", ls="--")
    plt.yticks(np.linspace(0,1,11));
    plt.ylim(0,1)
    plt.xlim(0,1)
    try:
        a = sklearn.metrics.auc(r[:, 0], r[:, 1])
    except ValueError as e:
        print "ROC is not sorted, probably negative weights"
        a = -1
    return a
    

def draw_cls_importance(cls, var):
    plt.grid()
    labs = []
    imps = []
    for v, i in sorted(zip(var, cls.feature_importances_), key=lambda x: x[1], reverse=True):
        labs += [v]
        imps += [i]
    plt.bar(range(len(imps)), imps);
    plt.xticks(np.array(range(len(labs)))+0.5, labs, rotation=90, fontsize=16)
    

def auc(df_test, df_train, ntrees=100, rate=0.02, depth=2, min1=12, min2=12, sub=0.8, ntrain=1.0):
    print ntrees, rate, depth, min1, min2, sub, ntrain
    if ntrees>2000 or ntrees<10:
        return 1.0
    try:
        cls = GradientBoostingClassifier(
            n_estimators=int(ntrees), learning_rate=rate,
            max_depth=int(depth),
            min_samples_split=int(min1),
            min_samples_leaf=int(min2),
            subsample=sub,
            verbose=False
        )

        df_train_shuf = df_train.iloc[np.random.permutation(np.arange(len(df_train)))]
        if ntrain>1.0:
            df_train_shuf = df_train_shuf[:int(len(df_train_shuf)*ntrain)]
        cls = cls.fit(df_train_shuf[var], df_train_shuf["id"])
    except Exception as e:
        return 1.0
    
    h1, h2, h1tr, h2tr = cls_hists(cls, df_test, df_train)
    
    r, e = calc_roc(h1, h2)
    A = sklearn.metrics.auc(r[:, 0], r[:, 1])
    print A
    return A
    
def compare(df, bins, v):
    h1 = make_df_hist(bins, df[df["id"]==1][v], df[df["id"]==1]["genWeight"])
    h2 = make_df_hist(bins, df[df["id"]==2][v], df[df["id"]==2]["genWeight"])

    h1.color = "red"
    h2.color = "blue"

    h1.Scale(1.0/h1.Integral())

    h2.Scale(1.0/h2.Integral())
    errorbar(h1)
    errorbar(h2)
    hist(h1, ls="-")
    hist(h2, ls="-")
    
def mc_stack(hlist, colors="auto"):
    if colors=="auto":
        coloriter = iter(plt.cm.jet(np.linspace(0,1,len(hlist))))
        for h in hlist:
            h.color = next(coloriter)
    elif isinstance(colors, list) and len(colors) == len(hlist):
        for h, c in zip(hlist, colors):
            h.color = c

    for h in hlist:
        h.fillstyle = "solid"

    #FIXME: Temporary workaround for failed fill, only works when hatch is specified
    r = hist(hlist, stacked=True, hatch=".", lw=2)
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

# def make_uoflow(h):
#     widths = list(h.xwidth())
#     edgs = list(h.xedgesl())
#     h2 = rootpy.plotting.Hist(h.nbins()+2, edgs[0] - widths[0], edgs[-1] + widths[-1])
#     nb = h.GetNbinsX()
#     for i in range(0,nb+2):
#         h2.SetBinContent(i+1, h.GetBinContent(i))
#         h2.SetBinError(i+1, h.GetBinError(i))
#     h2.SetEntries(h.GetEntries())
#     return h2


def make_uoflow(h):
    nb = h.GetNbinsX()
    #h.SetBinEntries(1, h.GetBinEntries(0) + h.GetBinEntries(1))
    #h.SetBinEntries(nb+1, h.GetBinEntries(nb) + h.GetBinEntries(nb + 1))
    h.SetBinContent(1, h.GetBinContent(0) + h.GetBinContent(1))
    h.SetBinContent(nb+1, h.GetBinContent(nb) + h.GetBinContent(nb + 1))
    h.SetBinError(1, math.sqrt(h.GetBinError(0)**2 + h.GetBinError(1)**2))
    h.SetBinError(nb+1, math.sqrt(h.GetBinError(nb)**2 + h.GetBinError(nb + 1)**2))
    return h

def draw_data_mc(tf, hname, samples, **kwargs):

    do_pseudodata = kwargs.get("do_pseudodata", False)
    xlabel = kwargs.get("xlabel", hname.replace("_", " "))
    yunit = kwargs.get("yunit", "")
    ylabel = kwargs.get("ylabel", "auto")
    rebin = kwargs.get("rebin", 1)
    title_extended = kwargs.get("title_extended", "")
    do_legend = kwargs.get("do_legend", True)
    colors = kwargs.get("colors", "auto")

    hs = OrderedDict()
    for sample, sample_name in samples:
        h = tf.get(sample + "/" + hname).Clone()
        hs[sample] = make_uoflow(h)
        #print hs[sample].GetBinLowEdge(0), hs[sample].GetBinLowEdge(hs[sample].GetNbinsX()+1)
        hs[sample].Scale(get_weight(sample))
        hs[sample].title = sample_name + " ({0:.1f})".format(hs[sample].Integral())
        hs[sample].rebin(rebin)

    c = plt.figure(figsize=(6,6))
    if do_pseudodata:
        a1 = plt.axes([0.0,0.22, 1.0, 0.8])
    else:
        a1 = plt.axes()
        
    plt.title("CMS preliminary simulation\n $\sqrt{s} = 13$ TeV"+title_extended,
        y=0.96, x=0.04,
        horizontalalignment="left", verticalalignment="top"
    )
    r = mc_stack(hs.values(), colors=colors)
    
    hsig = hs[samples[0][0]].Clone()
    tot_mc = sum(hs.values())
    hsig.Rebin(2)
    hsig.Scale(0.2 * tot_mc.Integral() / hsig.Integral())
    hsig.title = samples[0][1] + " norm"
    hsig.linewidth=2
    hsig.fillstyle = None
    hist([hsig])
    
    tot_mc.title = "pseudodata"
    tot_mc.color = "black"

    tot_bg = sum([hs[k] for k in hs.keys() if "tth" not in k])

    if do_pseudodata:
        pseudodata = tot_mc.Clone()#dice(tot_mc, nsigma=1.0)
        errorbar(pseudodata)

    if do_legend:
        plt.legend(loc=(1.1,0.0), numpoints=1)
    if ylabel == "auto":
        ylabel = "events / {0:.0f} {1}".format(hs.values()[0].get_bin_width(1), yunit)
    plt.ylabel(ylabel)
    if not do_pseudodata:
        plt.xlabel(xlabel)
    #hide x ticks on main panel
    ticks = a1.get_xticks()
    if do_pseudodata:
        a1.get_xaxis().set_visible(False)
    print ticks
    
    a1.set_ylim(bottom=0, top=1.1*a1.get_ylim()[1])
    a1.grid(zorder=100000)

    a2 = a1
    if do_pseudodata:
        a2 = plt.axes([0.0,0.0, 1.0, 0.18], sharex=a1)

        plt.xlabel(xlabel)
        a2.grid()

        data_minus_bg = pseudodata - tot_mc
        data_minus_bg.Divide(pseudodata)

        bg_unc_u = r["tot"] - r["tot_u"]
        bg_unc_d = r["tot"] - r["tot_d"]

        bg_unc_u.Divide(r["tot"])
        bg_unc_d.Divide(r["tot"])

        if do_pseudodata:
            errorbar(data_minus_bg)

        fill_between(bg_unc_u, bg_unc_d,
            color="black", hatch="////",
            alpha=1.0, linewidth=0, facecolor="none", edgecolor="black", zorder=10,
        )
        plt.ylabel("$\\frac{\mathrm{data} - \mathrm{mc}}{\mathrm{data}}$", fontsize=16)
        plt.axhline(0.0, color="black")
        #a2.set_ylim(-1,1)
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

def match_histogram(sample, var, cut):
    hs = process_sample_hist(
        sample, "hs",
        var,
        (250,0,250),
        cut
    )
    hs.Scale(1.0 / hs.Integral())

    nb = 0
    labels = []
    h = rootpy.plotting.Hist(30,0,30)
    for i in range(0,3):
        for j in range(0,3):
            for k in range(0,3):
                nb += 1
                h.SetBinContent(nb, hs.GetBinContent(1 + 100*i+10*j+k))
                h.SetBinError(nb, hs.GetBinError(1 + 100*i+10*j+k))
                #print nb, i,j,k,h.GetBinContent(nb)
                labels += ["%d%d%d"%(i,j,k)]
    
    return h
    
def get_pairs_file(pairs, **kwargs):
    ps = []
    for pair in pairs:
        tf, hn1, hn2, label = pair
        h1 = tf.get(hn1).Clone()
        h2 = tf.get(hn2).Clone()
        ps += [(h1, h2, label)]
    return ps
    
    
def draw_rocs(pairs, **kwargs):
    rebin = kwargs.get("rebin", 1)

    #c = plt.figure(figsize=(6,6))
    #plt.axes()
    plt.plot([0.0,1.0],[0.0,1.0], color="black")
    plt.xlim(0,1)
    plt.ylim(0,1)

    
    rs = []
    es = []
    for pair in pairs:
        h1, h2, label = pair
        h1.rebin(rebin)
        h2.rebin(rebin)
        r, e = calc_roc(h1, h2)
        rs += [r]
        es += [e]

    for (r, e, pair) in zip(rs, es, pairs):
        h1, h2, label = pair
        plt.errorbar(r[:, 0], r[:, 1], xerr=e[:, 0], yerr=e[:, 1], label=label)

    plt.legend(loc=2)

def draw_shape(f, samples, hn, **kwargs):
    rebin = kwargs.get("rebin", 1)

    hs = []
    for s in samples:
        h = f.get(s[0] + hn).Clone()
        h.Scale(1.0 / h.Integral())
        h.rebin(rebin)
        h.title = s[1]
        hs += [h]

    coloriter = iter(plt.cm.jet(np.linspace(0,1,len(hs))))

    for h in hs:
        h.color = next(coloriter)
        errorbar(h)
    plt.legend()
    for h in hs:
        hist(h, lw=1, ls="-")

def train(df, var, cut, **kwargs):
    df_sel = df[df.eval(cut)]
    ntrain_1 = int(sum(df_sel["id"]==1) * 0.5)
    ntrain_2 = int(sum(df_sel["id"]==0) * 0.5)
    weight = kwargs.get("weight", None)

    if weight:
        print "weighted", sum(df_sel[df_sel["id"]==1][weight]), sum(df_sel[df_sel["id"]==0][weight])
        print "unweighted", sum(df_sel["id"]==1), sum(df_sel["id"]==0)
        
    df_train = pandas.concat((df_sel[df_sel["id"]==1][:ntrain_1], df_sel[df_sel["id"]==0][:ntrain_2]))
    df_test = pandas.concat((df_sel[df_sel["id"]==1][ntrain_1:], df_sel[df_sel["id"]==0][ntrain_2:]))

    df_train_shuf = df_train.iloc[np.random.permutation(np.arange(len(df_train)))]
    
    cls = GradientBoostingClassifier(
        n_estimators=kwargs.get("ntrees", 200),
        learning_rate=kwargs.get("learning_rate", 0.1),
        max_depth=kwargs.get("depth", 2),
        min_samples_split=kwargs.get("min1", 1),
        min_samples_leaf=kwargs.get("min2", 1),
        subsample=kwargs.get("subsample", 1.0),
        verbose=True
    )

    if not weight:
        cls = cls.fit(df_train_shuf[var], df_train_shuf["id"])
    else:
        cls = cls.fit(df_train_shuf[var], df_train_shuf["id"], df_train_shuf[weight])

    return cls, df_test, df_train

def syst_comparison(sn, l, **kwargs):
    h0 = tf.get(sn + l[0]).Clone()
    h1 = tf.get(sn + l[1]).Clone()
    h2 = tf.get(sn + l[2]).Clone()
    
    for ih, h in enumerate([h0, h1, h2]):
        h.Scale(10000)
        h.title = l[ih]
        h.title = h.title.replace("_", "")
        h.title += " ({0:.2f})".format(h.Integral())
    rb = kwargs.get("rebin", 1)
    h0.rebin(rb)
    h1.rebin(rb)
    h2.rebin(rb)

    a1 = plt.axes([0.0,0.52,1.0,0.5])
    errorbar(h0)
    h1.linewidth = 2
    h2.linewidth = 2
    hist(h1, color="blue")
    hist(h2, color="red")

    fill_between(h1, h2, hatch="////", facecolor="none", edgecolor="black", lw=0, zorder=10)

    h1n = h1.Clone()
    h2n = h2.Clone()
    plt.legend(numpoints=1, loc="best")
    h1n.Scale(h0.Integral() / h1n.Integral())
    h2n.Scale(h0.Integral() / h2n.Integral())
    
    h1n.linestyle = "dashed"
    h2n.linestyle = "dashed"
    hist(h1n, color="blue")
    hist(h2n, color="red")
    
    #plt.ylim(bottom=0)
    plt.axhline(0.0)
    a2 = plt.axes([0.0,0.0,1.0,0.48],sharex=a1)
    
    h1r = h1.Clone()
    h1r.Divide(h0)
    h2r = h2.Clone()
    h2r.Divide(h0)
    h1r.color = "blue"
    h2r.color = "red"
    errorbar(h1r, color="blue")
    errorbar(h2r, color="red")
    plt.axhline(1.0, color="black")
    #fill_between(h1, h2, hatch="\\\\", facecolor="none", edgecolor="black", lw=0, zorder=10)
