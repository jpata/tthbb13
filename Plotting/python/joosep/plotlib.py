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

import matplotlib.patches as mpatches
import matplotlib.lines as mlines

matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})

matplotlib.rc("axes", labelsize=24)
matplotlib.rc("axes", titlesize=16)

colors = {
    "ttbarOther": (251, 102, 102),
    "ttbarPlusCCbar": (204, 2, -0),
    "ttbarPlusB": (153, 51, 51),
    "ttbarPlusBBbar": (102, 0, 0),
    "ttbarPlus2B": (80, 0, 0),
    "ttH": (44, 62, 167),
    "ttHbb": (44, 62, 167),
    "ttHnonbb": (39, 57, 162),
    "other": (251, 73, 255),
}

for cn, c in colors.items():
    colors[cn] = (c[0]/255.0, c[1]/255.0, c[2]/255.0)

cats = {
    'dl_j3_t2': "(is_dl==1) & (numJets==3) & (nBCSVM==2)",
    'dl_jge3_t3': "(is_dl==1) & (numJets>=3) & (nBCSVM==3)",
    'dl_jge4_t2': "(is_dl==1) & (numJets>=4) & (nBCSVM==2)",
    'dl_jge4_tge4': "(is_dl==1) & (numJets>=4) & (nBCSVM>=4)",
    
    'sl_j4_t3': "(is_sl==1) & (numJets==4) & (nBCSVM==3)",
    'sl_j4_t4': "(is_sl==1) & (numJets==4) & (nBCSVM==4)",
    'sl_j5_t3': "(is_sl==1) & (numJets==5) & (nBCSVM==3)",
    'sl_j5_tge4': "(is_sl==1) & (numJets==5) & (nBCSVM>=4)",
    'sl_jge6_t2': "(is_sl==1) & (numJets>=6) & (nBCSVM==2)",
    'sl_jge6_t3': "(is_sl==1) & (numJets>=6) & (nBCSVM==3)",
    'sl_jge6_tge4': "(is_sl==1) & (numJets>=6) & (nBCSVM>=4)",
}
memcut = "& ((btag_LR_4b_2b>0.95) | ((is_sl==1) & (nBCSVM>=3)) | ((is_dl==1) & (nBCSVM>=2)))"


#List of sample filenames -> short names
samplelist = [
    ("ttHTobb_M125_13TeV_powheg_pythia8", "ttHbb"),
    ("TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb", "ttbarPlusBBbar"),
    ("TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb", "ttbarPlusB"),
    ("TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b", "ttbarPlus2B"),
    ("TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc", "ttbarPlusCCbar"),
    ("TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll", "ttbarOther"),
]
samplecolors = [colors[sn[1]] for sn in samplelist]

varnames = {
    "jet0_pt": "leading jet $p_T$ [GeV]",
    "jet1_pt": "subleading jet $p_T$ [GeV]",

    "jet0_btagCSV": "leading jet $b_{\\mathrm{CSV}}$",
    "jet1_btagCSV": "subleading jet $b_{\\mathrm{CSV}}$",

    "jet0_btagBDT": "leading jet $b_{\\mathrm{cMVAv2}}$",
    "jet1_btagBDT": "subleading jet $b_{\\mathrm{cMVAv2}}$",

    "jet0_eta": "leading jet $\eta$",
    "jet1_eta": "subleading jet $\eta$",

    "jet0_aeta": "leading jet $|\eta|$",
    "jet1_aeta": "subleading jet $|\eta|$",

    "lep0_pt": "leading lepton $p_T$ [GeV]",
    "lep1_pt": "subleading jet $p_T$ [GeV]",

    "lep0_eta": "leading lepton $|\eta|$ [GeV]",
    "lep1_eta": "subleading jet $|\eta|$ [GeV]",

    "njets": "$N_{\\mathrm{jets}}$",
    "ntags": "$N_{\\mathrm{CSVM}}$",

    "btag_LR_4b_2b_logit": "$\\log{[\\mathcal{F} / (1 - \\mathcal{F})]}$",
    "nfatjets": r"$N_{\mathcal{fatjets}}$",
    "topCandidate_pt": "top candidate $p_T$ [GeV]",
    "topCandidate_mass": "top candidate $M$ [GeV]",
    "topCandidate_fRec": "top candidate $f_{\\mathrm{rec}}$",
    "topCandidate_Ropt": "top candidate $R_{\\mathrm{opt}}$",
    "topCandidate_RoptCalc": "top candidate $R_{\\mathrm{opt}}, calc$",
    "topCandidate_n_subjettiness": "top candidate n-subjettiness$",

    "nhiggsCandidate": "Number of higgs candidates",
    "higgsCandidate_pt": "H candidate $p_T$ [GeV]",
    "higgsCandidate_eta": "H candidate $\eta$",
    "higgsCandidate_mass": "H candidate $M$ [GeV]",
    "higgsCandidate_mass_pruned": "H candidate pruned $M$ [GeV]",
    "higgsCandidate_mass_softdrop": "H candidate softdrop $M$ [GeV]",
    "higgsCandidate_bbtag": "H candidate bbtag",
    "higgsCandidate_n_subjettiness": "H candidate n-subjettiness",
    "higgsCandidate_dr_top":  "$\\Delta R_{h,t}$",
    "numJets": "$N_{\\mathrm{jets}}$",
    "nBCSVM": "$N_{\\mathrm{CSVM}}$",
    "btag_LR_4b_2b_logit": "$\\log{\\mathcal{F} / (1 - \\mathcal{F})}$",
    "mem_SL_0w2h2t": "mem SL 0w2h2t",
    "mem_SL_2w2h2t": "mem SL 2w2h2t",
    "mem_SL_2w2h2t_sj": "mem SL 2w2h2t sj",
    "mem_DL_0w2h2t": "mem DL 0w2h2t",
    "nPVs": "$N_{\\mathrm{PV}}$",

}

varunits = {
    "jet0_pt": "GeV",
    "jet1_pt": "GeV",
    "topCandidate_pt": "GeV",
    "topCandidate_mass": "GeV",
    "higgsCandidate_pt": "GeV",
    "higgsCandidate_mass": "GeV",
    "higgsCandidate_mass_pruned": "GeV",
    "higgsCandidate_mass_softdrop": "GeV",
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
    h.Sumw2()
    hname = h.GetName()
    h = rootpy.asrootpy(h)
    h.SetDirectory(ROOT.gROOT)
    n = tt.Draw("{0} >> {1}".format(func, hname), cut)
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

    return {"hists":r, "tot":htot, "tot_u":htot_u, "tot_d":htot_d}

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

def fill_overflow(hist):
    """
    Puts the contents of the overflow bin in the last visible bin
    """
    nb = hist.GetNbinsX()
    o = hist.GetBinContent(nb + 1)
    oe = hist.GetBinError(nb + 1)
    hist.SetBinContent(nb, hist.GetBinContent(nb) + o)
    hist.SetBinError(nb, math.sqrt(hist.GetBinError(nb)**2 + oe**2))
    
    #fixme recalculate error
    hist.SetBinContent(nb+1, 0)
    hist.SetBinError(nb+1, 0)

def draw_data_mc(tf, hname, samples, **kwargs):

    do_pseudodata = kwargs.get("do_pseudodata", False)
    dataname = kwargs.get("dataname", None)
    xlabel = kwargs.get("xlabel", hname.replace("_", " "))
    xunit = kwargs.get("xunit", "XUNIT")
    ylabel = kwargs.get("ylabel", "auto")
    rebin = kwargs.get("rebin", 1)
    title_extended = kwargs.get("title_extended", "")
    do_legend = kwargs.get("do_legend", True)
    legend_loc = kwargs.get("legend_loc", (1.1,0.1))
    legend_fontsize = kwargs.get("legend_fontsize", 6)
    colors = kwargs.get("colors", "auto")
    show_overflow = kwargs.get("show_overflow", False)

    hs = OrderedDict()
    for sample, sample_name in samples:
        try:
            h = tf.get(sample + "/" + hname).Clone()
        except rootpy.io.file.DoesNotExist as e:
            continue
            # if len(hs.values())>0:
            #     h = 0.0 * hs.values()[0].Clone()
            # else:
            #     h = rootpy.plotting.Hist(1, 0, 1)
        hs[sample] = make_uoflow(h)
        #print hs[sample].GetBinLowEdge(0), hs[sample].GetBinLowEdge(hs[sample].GetNbinsX()+1)
        #hs[sample].Scale(get_weight(sample))
        hs[sample].title = sample_name + " ({0:.1f})".format(hs[sample].Integral())
        hs[sample].rebin(rebin)
        if show_overflow:
            fill_overflow(hs[sample])
            
    c = plt.figure(figsize=(6,6))
    if do_pseudodata or dataname:
        a1 = plt.axes([0.0,0.22, 1.0, 0.8])
    else:
        a1 = plt.axes()
        
    c.suptitle("$\\textbf{CMS}$ preliminary\n $\sqrt{s} = 13$ TeV"+title_extended,
        y=0.98, x=0.02,
        horizontalalignment="left", verticalalignment="top"
    )
    r = mc_stack(hs.values(), colors=colors)
    
    #Create the normalized signal shape
    hsig = hs[samples[0][0]].Clone()
    tot_mc = sum(hs.values())
    #hsig.Rebin(2)
    hsig.Scale(0.2 * tot_mc.Integral() / hsig.Integral())
    hsig.title = samples[0][1] + " norm"
    hsig.linewidth=2
    hsig.fillstyle = None
    hist([hsig])
    
    tot_mc.title = "pseudodata"
    tot_mc.color = "black"

    tot_bg = sum([hs[k] for k in hs.keys() if "tth" not in k])
    
    data = None
    if do_pseudodata:
        data = tot_mc.Clone()#dice(tot_mc, nsigma=1.0)
        data.title = "pseudodata"
    elif dataname:
        datas = []
        for dn in dataname:
            try:
                h = tf.get(dn + "/" + hname)
                datas += [tf.get(dn + "/" + hname).Clone()]
            except rootpy.io.file.DoesNotExist:
                print "missing", dn, hname
        if len(datas)>0:
            data = sum(datas)
            data.rebin(rebin)
        else:
            data = tot_mc.Clone()
            data.Scale(0.0)
        data.title = "data ({0})".format(data.Integral())

    if data:
        if show_overflow:
            fill_overflow(data)
        for ibin in range(data.GetNbinsX()):
            if data.GetBinContent(ibin) == 0:
                data.SetBinError(ibin, 1)
        errorbar(data)

    if do_legend:
        patches = []
        if data:
            dataline = mlines.Line2D([], [], color='black', marker='o', label=data.title)
            patches += [dataline]
        for line, h in zip(r["hists"], hs.values()):
            #print h.title, line.get_color()
            patch = mpatches.Patch(color=line.get_color(), label=h.title)
            patches += [patch]
        plt.legend(handles=patches, loc=legend_loc, numpoints=1, prop={'size':legend_fontsize}, ncol=2, frameon=False)
    if ylabel == "auto":
        ylabel = "events / {0:.2f} {1}".format(hs.values()[0].get_bin_width(1), xunit)
    plt.ylabel(ylabel)
    if not data:
        plt.xlabel(xlabel)
    #hide x ticks on main panel
    ticks = a1.get_xticks()
    if data:
        a1.get_xaxis().set_visible(False)
    #print ticks
    
    a1.set_ylim(bottom=0, top=1.1*a1.get_ylim()[1])
    a1.grid(zorder=100000)

    a2 = a1
    
    #do ratio panel
    if data:
        a2 = plt.axes([0.0,0.0, 1.0, 0.18], sharex=a1)

        plt.xlabel(xlabel)
        a2.grid()
        
        data.Divide(tot_mc)
        for ibin in range(data.GetNbinsX()):
            bc = tot_mc.GetBinContent(ibin)
            if bc==0:
                data.SetBinContent(ibin, 0)
        bg_unc_u = r["tot_u"]
        bg_unc_d = r["tot_d"]

        bg_unc_u.Divide(r["tot"])
        bg_unc_d.Divide(r["tot"])

        errorbar(data)

        fill_between(
            bg_unc_u, bg_unc_d,
            color="black", hatch="////",
            alpha=1.0, linewidth=0, facecolor="none", edgecolor="black", zorder=10,
        )
        plt.ylabel("$\\frac{\mathrm{data}}{\mathrm{pred.}}$", fontsize=16)
        plt.axhline(1.0, color="black")
        a2.set_ylim(0, 2)
        #hide last tick on ratio y axes
        a2.set_yticks(a2.get_yticks()[:-1]);
        a2.set_xticks(ticks);
    return a1, a2, hs, r

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
    if h1.Integral()>0:
        h1.Scale(1.0 / h1.Integral())
    if h2.Integral()>0:
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
            roc[i, 1] = float(h2.IntegralAndError(i, h2.GetNbinsX()+2, e2)) / I2
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
        if isinstance(hn2, str):
            h2 = tf.get(hn2).Clone()
        elif isinstance(hn2, list):
            h2 = tf.get(hn2[0]).Clone()
            for _hn2 in hn2[1:]:
                h2 += tf.get(_hn2).Clone()
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

def syst_comparison(tf, sn, l, **kwargs):
    h0 = tf.get(sn + l[0]).Clone()
    h1 = tf.get(sn + l[1]).Clone()
    h2 = tf.get(sn + l[2]).Clone()
    
    for ih, h in enumerate([h0, h1, h2]):
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
    if h1n.Integral() > 0:
        h1n.Scale(h0.Integral() / h1n.Integral())
    if h2n.Integral() > 0:
        h2n.Scale(h0.Integral() / h2n.Integral())
    
    h1n.linestyle = "dashed"
    h2n.linestyle = "dashed"
    hist(h1n, color="blue")
    hist(h2n, color="red")
    
    #plt.ylim(bottom=0)
    plt.axhline(0.0)
    a2 = plt.axes([0.0,0.0,1.0,0.48],sharex=a1)

    h1r = h1n.Clone()
    h1r.Divide(h0)
    h2r = h2n.Clone()
    h2r.Divide(h0)
    h1r.color = "blue"
    h2r.color = "red"
    hist(h1r, color="blue")
    hist(h2r, color="red")
    a2.set_ylim(0.9, 1.1)
    plt.axhline(1.0, color="black")
    #fill_between(h1, h2, hatch="\\\\", facecolor="none", edgecolor="black", lw=0, zorder=10)


def svfg(fn, **kwargs):
    plt.savefig(fn, pad_inches=0.5, bbox_inches='tight', **kwargs)
    #plt.clf()


def get_yields(inf, cat, suffix, samples):
    hs = []
    for x in samples:
        try:
            h = inf.get("{0}{2}/{1}/jet0_pt".format(x, cat, suffix))
            hs += [h]
        except rootpy.io.DoesNotExist as e:
            pass
    if len(hs)==0:
        hs = [rootpy.plotting.Hist(10, 0, 1)]
    hs = sum(hs)
    
    e1 = ROOT.Double(0)
    i1 = hs.IntegralAndError(0, hs.GetNbinsX()+1, e1)
    return i1, e1

def get_sb(inf, cat, suffix):
    """
    Returns the S/sqrt(B) [sob] and error in a category.
    inf - input file (rootpy.io.File)
    cat - category string (e.g. "sl_mu_jge6_tge4")
    suffix - optional suffix string to append to samples (e.g. "_cfg_noME_jetPt20")

    returns (sob, error_sob)
    """

    signal = "ttH_hbb"
    backgrounds = ["ttbarOther", "ttbarPlusCCbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusBBbar"]
    
    i1, e1 = get_yields(inf, cat, suffix, [signal])
    i2, e2 = get_yields(inf, cat, suffix, backgrounds)

    sob = i1/np.sqrt(i2) if i2>0 else 0.0
    if i1>0 and i2>0:
        err_sob = sob * np.sqrt((e1/i1)**2 + (e2/i2)**2)
    else:
        err_sob = 0
    return i1/np.sqrt(i2), err_sob

def get_sb_cats(inf, categories, suffix=""):
    ys = []
    es = []
    xs = []
    for cat in categories:
        y, e = get_sb(inf, cat, suffix)
        xs += [cat]
        ys += [y]
        es += [e]
    xs_num = np.array(range(len(xs)))+0.5
    return xs, xs_num, ys, es


def getDataname(cat):
    if "sl_mu" in cat:
        return ["SingleMuon"]
    elif "sl_el" in cat:
        return ["SingleElectron"]
    elif "dl_mumu" in cat:
        return ["DoubleMuon"]
    elif "dl_ee" in cat:
        return ["DoubleEG"]
    elif "dl_emu" in cat:
        return ["MuonEG"]
    raise Exception("not recognized {0}".format(cat))


def sync_table(inf, cats, bkg):
    hd = {}
    for ic, cat in enumerate(cats):
        for sample in ["ttH_hbb"] + bkg + ["data"]:
            k = sample + "/" + "yields"
            if hd.has_key(k):
                h = hd[k]
            else:
                h = rootpy.plotting.Hist(len(cats), 0, len(cats))
            if sample == "data":
                categories_to_get = getDataname(cat)
            else:
                categories_to_get = [sample]
            y, e = get_yields(inf, cat, "", categories_to_get)
            h.SetBinContent(ic+1, y)
            h.SetBinError(ic+1, e)
            hd[k] = h

    table = []
    for sample in ["ttH_hbb"] + bkg + ["data"]:
        row = [sample]
        for ic, cat in enumerate(cats):
            i = hd[sample + "/yields"].GetBinContent(ic+1)
            row += [i]
        table += [row]
        
    d = np.array(table)[:, 1:].astype("f")
    table.insert(-1, ["total"] + [f for f in np.sum(d[0:-1, :], axis=0)])
    return hd, table

def get_cut_at_eff(h, eff):
    h = h.Clone()
    h.Scale(1.0 / h.Integral())
    hc = h.GetCumulative()
    bins = np.array([hc.GetBinContent(i) for i in range(1, hc.GetNbinsX()+1)])
    idx = np.searchsorted(bins, eff)
    return idx
