import ROOT
ROOT.gROOT.SetBatch(True)

import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import os

import rootpy
import rootpy.io
from rootpy.plotting.root2matplotlib import errorbar, bar, hist, fill_between
from collections import OrderedDict

import pandas

import sklearn
import sklearn.metrics
from sklearn.ensemble import GradientBoostingClassifier
import math

import matplotlib.patches as mpatches
import matplotlib.lines as mlines

matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})

matplotlib.rc("axes", labelsize=24)
matplotlib.rc("axes", titlesize=16)

#All the colors of the various processes
#extracted using the apple color picker tool
colors = {
    "ttbarOther": (251, 102, 102),
    "ttbarPlusCCbar": (204, 2, -0),
    "ttbarPlusB": (153, 51, 51),
    "ttbarPlusBBbar": (102, 0, 0),
    "ttbarPlus2B": (80, 0, 0),
    "ttH": (44, 62, 167),
    "ttH_hbb": (44, 62, 167),
    "ttH_nonhbb": (39, 57, 162),
    "other": (251, 73, 255),
}

#create floats of colors from 0..1
for cn, c in colors.items():
    colors[cn] = (c[0]/255.0, c[1]/255.0, c[2]/255.0)

#list of all categories and their ROOT cuts
cats = {
    'dl_j3_t2': "(is_dl==1) & (numJets==3) & (nBCSVM==2)",
    'dl_jge3_t3': "(is_dl==1) & (numJets>=3) & (nBCSVM==3)",
    'dl_j3_t3': "(is_dl==1) & (numJets==3) & (nBCSVM==3)",
    'dl_jge4_t3': "(is_dl==1) & (numJets>=4) & (nBCSVM==3)",
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

#List of sample filenames -> short names suitable for latex
samplelist = [
    ("ttH_hbb", "ttHbb"),
    ("ttH_nonhbb", "ttHnonbb"),
    ("ttbarPlusBBbar", "ttbarPlusBBbar"),
    ("ttbarPlusB", "ttbarPlusB"),
    ("ttbarPlus2B", "ttbarPlus2B"),
    ("ttbarPlusCCbar", "ttbarPlusCCbar"),
    ("ttbarOther", "ttbarOther"),
]
samplecolors = [colors[sn[0]] for sn in samplelist]

#list of all variable names, suitable for latex
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
    "topCandidate_masscal": "top candidate $M$ [GeV]",
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
    "ntopCandidate": "$N_{\\mathrm{HTTv2}}$",
    "common_bdt": "BDT"
}

#the units for variables
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
    """
    Takes a list of files and projects a 1D histogram with the specified cut.
    fnames (list of strings): list of filenames to be opened
    hname (string): name of the output histogram, must be unique
    func (string): the function (ROOT string) to be evaluated
    bins (3-tuple): the (nbins, low, high) of the histograms
    cut (string): the weight and cut string (ROOT format) to be evaluated.
    
    returns: TH1D in the gROOT directory
    """

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

def mc_stack(
    hlist,
    hs_syst,
    systematics,
    colors="auto"
    ):
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
        color="black", hatch="////////",
        alpha=1.0, linewidth=0, facecolor="none", edgecolor="black", zorder=10,
    )

    #add systematic uncertainties
    hstat = htot_u - htot_d
    errs = np.array([y for y in hstat.y()])
    errs = np.abs(errs)

    htot_usyst = htot.Clone()
    htot_dsyst = htot.Clone()
    for systUp, systDown in systematics:
        errs_syst_up = np.array([y for y in sum(hs_syst[systUp].values()).y()])
        errs_syst_down = np.array([y for y in sum(hs_syst[systDown].values()).y()])
        errs_syst = np.abs(errs_syst_up - errs_syst_down)
        errs = np.power(errs, 2) + np.power(errs_syst, 2)
        errs = np.sqrt(errs)
    for i in range(len(errs)):
        htot_usyst.SetBinContent(i+1, htot_usyst.GetBinContent(i+1) + errs[i]/2)
        htot_dsyst.SetBinContent(i+1, htot_dsyst.GetBinContent(i+1) - errs[i]/2)

    fill_between(htot_usyst, htot_dsyst,
        color="gray", hatch="\\\\\\\\",
        alpha=1.0, linewidth=0, facecolor="none", edgecolor="gray", zorder=10,
    )

    return {"hists":r, "tot":htot, "tot_u":htot_u, "tot_d":htot_d, "tot_usyst":htot_usyst, "tot_dsyst":htot_dsyst}

def dice(h, nsigma=1.0):
    hret = h.clone()
    for i in range(1, h.nbins()+1):
        m, e = h.get_bin_content(i), h.get_bin_error(i)
        if e<=0:
            e = 1.0
        n = np.random.normal(m, nsigma*e)
        hret.set_bin_content(i, n)
    return hret

def make_uoflow(h):
    nb = h.GetNbinsX()
    #h.SetBinEntries(1, h.GetBinEntries(0) + h.GetBinEntries(1))
    #h.SetBinEntries(nb+1, h.GetBinEntries(nb) + h.GetBinEntries(nb + 1))
    h.SetBinContent(1, h.GetBinContent(0) + h.GetBinContent(1))
    h.SetBinContent(nb+1, h.GetBinContent(nb) + h.GetBinContent(nb + 1))
    h.SetBinError(1, math.sqrt(h.GetBinError(0)**2 + h.GetBinError(1)**2))
    h.SetBinError(nb+1, math.sqrt(h.GetBinError(nb)**2 + h.GetBinError(nb + 1)**2))

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


def getHistograms(tf, samples, hname):
    hs = OrderedDict()
    for sample, sample_name in samples:
        try:
            h = tf.get(sample + "/" + hname).Clone()
        except rootpy.io.file.DoesNotExist as e:
            continue
        hs[sample] = h
    for sample, sample_name in samples:
        if not hs.has_key(sample):
            if len(hs)>0:
                hs[sample] = 0.0*hs.values()[0].Clone()
            else:
                return hs
    return hs

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
    blindFunc = kwargs.get("blindFunc", None)

    #array of up-down pairs for systematic names, e.g. _CMS_scale_jUp/Down
    systematics = kwargs.get("systematics", [])

    hs = OrderedDict()
    hs_syst = OrderedDict()
    hs = getHistograms(tf, samples, hname)

    #get the systematically variated histograms
    for systUp, systDown in systematics:
        hs_syst[systUp] = getHistograms(tf, samples, hname+systUp)
        hs_syst[systDown] = getHistograms(tf, samples, hname+systDown)
        if len(hs_syst[systUp])==0 or len(hs_syst[systDown])==0:
            print "Could not read histograms for {0}".format(hname+systUp)

    sample_d = dict(samples)
    for hd in [hs] + hs_syst.values():
        for (sample, h) in hd.items():
            make_uoflow(h)
            #print hs[sample].GetBinLowEdge(0), hs[sample].GetBinLowEdge(hs[sample].GetNbinsX()+1)
            #hs[sample].Scale(get_weight(sample))
            h.title = sample_d[sample] + " ({0:.1f})".format(h.Integral())
            h.rebin(rebin)
            if show_overflow:
                fill_overflow(h)
            
    c = plt.figure(figsize=(6,6))
    if do_pseudodata or dataname:
        a1 = plt.axes([0.0,0.22, 1.0, 0.8])
    else:
        a1 = plt.axes()
        
    c.suptitle("$\\textbf{CMS}$ preliminary $\sqrt{s} = 13$ TeV"+title_extended,
        y=1.02, x=0.02,
        horizontalalignment="left", verticalalignment="bottom", fontsize=16
    )
    if len(hs) == 0:
        raise KeyError("did not find any histograms for MC")
    r = mc_stack(hs.values(), hs_syst, systematics, colors=colors)
    
    #Create the normalized signal shape
    hsig = hs[samples[0][0]].Clone()
    tot_mc = sum(hs.values())
    #hsig.Rebin(2)
    if hsig.Integral()>0:
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
        data = tot_mc.Clone()
        data.title = "pseudodata"
        if blindFunc:
            data = blindFunc(data)
        idata = data.Integral()
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
        if blindFunc:
            data = blindFunc(data)
        data.title = "data ({0})".format(data.Integral())
        idata = data.Integral()

    if data and (blindFunc is None):
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
        patches += [mpatches.Patch(facecolor="none", edgecolor="black", label="stat", hatch="////////")]
        patches += [mpatches.Patch(facecolor="none", edgecolor="gray", label="stat+syst", hatch="\\\\\\\\")]
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

        bg_unc_usyst = r["tot_usyst"]
        bg_unc_dsyst = r["tot_dsyst"]

        bg_unc_usyst.Divide(r["tot"])
        bg_unc_dsyst.Divide(r["tot"])
        if blindFunc:
            data = blindFunc(data)
        errorbar(data)

        fill_between(
            bg_unc_u, bg_unc_d,
            color="black", hatch="////////",
            alpha=1.0, linewidth=0, facecolor="none", edgecolor="black", zorder=10,
        )

        fill_between(
            bg_unc_usyst, bg_unc_dsyst,
            color="gray", hatch="\\\\\\\\",
            alpha=1.0, linewidth=0, facecolor="none", edgecolor="gray", zorder=10,
        )
        plt.title("data={0:.1f}\ MC={1:.1f}".format(idata, r["tot"].Integral()), x=0.01, y=0.8, fontsize=10, horizontalalignment="left")
        plt.ylabel("$\\frac{\mathrm{data}}{\mathrm{pred.}}$", fontsize=16)
        plt.axhline(1.0, color="black")
        a2.set_ylim(0, 2)
        #hide last tick on ratio y axes
        a2.set_yticks(a2.get_yticks()[:-1]);
        a2.set_xticks(ticks);
    return a1, a2, hs, r, hs_syst

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

#def match_histogram(sample, var, cut):
#    hs = process_sample_hist(
#        sample, "hs",
#        var,
#        (250,0,250),
#        cut
#    )
#    hs.Scale(1.0 / hs.Integral())
#
#    nb = 0
#    labels = []
#    h = rootpy.plotting.Hist(30,0,30)
#    for i in range(0,3):
#        for j in range(0,3):
#            for k in range(0,3):
#                nb += 1
#                h.SetBinContent(nb, hs.GetBinContent(1 + 100*i+10*j+k))
#                h.SetBinError(nb, hs.GetBinError(1 + 100*i+10*j+k))
#                #print nb, i,j,k,h.GetBinContent(nb)
#                labels += ["%d%d%d"%(i,j,k)]
#    
#    return h
    
#def get_pairs_file(pairs, **kwargs):
#    ps = []
#    for pair in pairs:
#        tf, hn1, hn2, label = pair
#        h1 = tf.get(hn1).Clone()
#        if isinstance(hn2, str):
#            h2 = tf.get(hn2).Clone()
#        elif isinstance(hn2, list):
#            h2 = tf.get(hn2[0]).Clone()
#            for _hn2 in hn2[1:]:
#                h2 += tf.get(_hn2).Clone()
#        ps += [(h1, h2, label)]
#    return ps
    
    
#def draw_rocs(pairs, **kwargs):
#    rebin = kwargs.get("rebin", 1)
#
#    #c = plt.figure(figsize=(6,6))
#    #plt.axes()
#    plt.plot([0.0,1.0],[0.0,1.0], color="black")
#    plt.xlim(0,1)
#    plt.ylim(0,1)
#
#    
#    rs = []
#    es = []
#    for pair in pairs:
#        h1, h2, label = pair
#        h1.rebin(rebin)
#        h2.rebin(rebin)
#        r, e = calc_roc(h1, h2)
#        rs += [r]
#        es += [e]
#
#    for (r, e, pair) in zip(rs, es, pairs):
#        h1, h2, label = pair
#        plt.errorbar(r[:, 0], r[:, 1], xerr=e[:, 0], yerr=e[:, 1], label=label)
#
#    plt.legend(loc=2)

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

def svfg(fn, **kwargs):
    path = os.path.dirname(fn)
    if not os.path.exists(path):
        os.makedirs(path)
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

def get_cut_at_eff(h, eff):
    h = h.Clone()
    h.Scale(1.0 / h.Integral())
    hc = h.GetCumulative()
    bins = np.array([hc.GetBinContent(i) for i in range(1, hc.GetNbinsX()+1)])
    idx = np.searchsorted(bins, eff)
    return idx

def brazilplot(lims, ks, knames):
    ax = plt.axes()
    ls = []
    errs = np.zeros((len(ks), 4))
    i = 0
    for k in ks:
        l = lims[k][0][2]
        ls += [l]
        errs[i,0] = lims[k][0][1]
        errs[i,1] = lims[k][0][3]
        errs[i,2] = lims[k][0][0]
        errs[i,3] = lims[k][0][4]
        #print k, ls[i], errs[i,0], errs[i,1]
        i += 1
    #print ls
    ys = np.array(range(len(ks)))
    for y, l, e1, e2, e3, e4 in zip(ys, ls, errs[:, 0], errs[:, 1], errs[:, 2], errs[:, 3]):
        ax.add_line(plt.Line2D([l, l], [y, y+1.0], lw=2, color="black", ls="-"))
        #print l, y
        plt.text(l*1.1, y+0.5, "{0:.2f}".format(l), horizontalalignment="left", verticalalignment="center")
        ax.barh(y+0.1, (e4-e3), left=e3, color=np.array([254, 247, 2])/255.0, lw=0)
        ax.barh(y+0.1, (e2-e1), left=e1, color=np.array([51, 247, 2])/255.0 , lw=0)
    plt.xlim(0, len(ks))
    plt.ylim(ys[0], ys[-1]+1)
    plt.yticks(ys+0.5, knames, verticalalignment="center", fontsize=18, ha="left")
    plt.xlabel("$\mu$")
    yax = ax.get_yaxis()
    # find the maximum width of the label on the major ticks
    pad = 200
    yax.set_tick_params(pad=pad)

    #plt.grid()


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
