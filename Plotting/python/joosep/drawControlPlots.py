import sys
import matplotlib
matplotlib.use('Agg')
sys.path += ["/Users/joosep/Documents/heplot/"]
import heplot, rootpy
import numpy as np
import matplotlib.pyplot as plt
import pandas
import rootpy.plotting.root2matplotlib as rplt
import ROOT, plotlib, heplot

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

slist = [
 ('ttH_hbb', 'ttHbb'),
 ('ttbarPlusBBbar', 'ttbarPlusBBbar'),
 ('ttbarPlusB', 'ttbarPlusB'),
 ('ttbarPlus2B', 'ttbarPlus2B'),
 ('ttbarPlusCCbar', 'ttbarPlusCCbar'),
 ('ttbarOther', 'ttbarOther')
]

sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_15/src/TTH/Plotting/python/joosep/")
inf = rootpy.io.File("/Users/joosep/Dropbox/tth/ControlPlotsSparse.root")

for cat in [
    # "sl_mu_j5_t2_boostedHiggs",
    # "sl_mu_j5_t3_boostedHiggs",
    # "sl_mu_j5_tge4_boostedHiggs",
    # "sl_mu_jge6_t2_boostedHiggs",
    # "sl_mu_jge6_t3_boostedHiggs",
    # "sl_el_j5_t2_boostedHiggs", 
    # "sl_el_j5_t3_boostedHiggs",
    # "sl_el_j5_tge4_boostedHiggs",
    # "sl_el_jge6_t2_boostedHiggs",
    # "sl_el_jge6_t3_boostedHiggs",

    #"sl_mu",
    "sl_mu_j5_t2",
    #"sl_mu_j5_t2_boostedHiggsOnly",
    #"sl_mu_j5_t2_boostedTopOnly",
    #"sl_mu_j5_t2_boostedHiggsTop",
    "sl_mu_j5_t3",
    "sl_mu_j5_tge4",
    "sl_mu_jge6_t2",
    "sl_mu_jge6_t3",
    "sl_mu_jge6_tge4",

    #"sl_el",
    "sl_el_j5_t2",
    "sl_el_j5_t2_boostedHiggs",
    "sl_el_j5_t2_boostedTop",
    "sl_el_j5_t3",
    "sl_el_j5_tge4",
    "sl_el_jge6_t2",
    "sl_el_jge6_t3",
    "sl_el_jge6_tge4",

    "dl_mumu_j3_t2",
    "dl_ee_j3_t2",
    "dl_emu_j3_t2",

    "dl_mumu_jge3_t3",
    "dl_ee_jge3_t3",
    "dl_emu_jge3_t3",

    "dl_mumu_jge4_t2",
    "dl_ee_jge4_t2",
    "dl_emu_jge4_t2",

    "dl_mumu_jge4_tge4",
    "dl_ee_jge4_tge4",
    "dl_emu_jge4_tge4",
    ]:
    print cat
    for distr, kdict in [
        #("nhiggsCandidate", {"log":True}),
        ("jet0_btagCSV", {"rebin":1, "log":True}),
        ("jet0_btagBDT", {"rebin":1, "log":True}),
        ("jet0_pt", {"rebin":1, "log":True, "xunit":"GeV"}),

        ("jet1_btagCSV", {"rebin":1, "log":True}),
        ("jet1_btagBDT", {"rebin":1, "log":True}),
        ("jet1_pt", {"rebin":1, "log":True, "xunit":"GeV"}),
        ("numJets", {}),
        ("nBCSVM", {}),
        ("btag_LR_4b_2b_logit", {}),

        #("higgsCandidate_pt", {"rebin":1, "log":True, "xunit":"GeV"}),
        #("higgsCandidate_bbtag", {"rebin":1}),
        #("topCandidate_pt", {"rebin":1, "log":True, "xunit":"GeV"}),
        #("topCandidate_mass", {"rebin":1, "xunit":"GeV"}),
    ]:
        print distr
        if not "boosted" in cat and "Candidate" in distr:
            continue
        r = plotlib.draw_data_mc(
            inf,
            cat + "/" + distr,
            slist,
            dataname=getDataname(cat), xlabel=plotlib.varnames[distr],
            xunit=kdict.get("xunit", ""),
            legend_fontsize=10, legend_loc="best", colors=plotlib.samplecolors,
            do_legend=True,
            rebin=kdict.get("rebin", 1),
            show_overflow = True, title_extended="\n$\\mathcal{L}=2.12\\ \\mathrm{fb}^{-1}$"
        )
        if kdict.get("log", False):
            r[0].set_yscale("log")
            r[0].set_ylim(bottom=1, top=r[3]["tot"].GetMaximum()*10)
        
        #plt.rc('text', usetex=False)
        r[0].set_title(cat.replace("_", " "), x=0.98, y=1.01, ha="right", va="bottom", fontsize=18)
        #plt.rc('text', usetex=True)

        #plotlib.svfg("{0}_{1}.pdf".format(distr, cat))
        plotlib.svfg("plots/{0}_{1}.png".format(cat, distr))
        plt.clf()
        del r


###
### Signal over Background ratio plot
###

categories = [
    "sl_mu_j5_t2", "sl_mu_j5_t3", "sl_mu_j5_tge4", "sl_mu_jge6_t2", "sl_mu_jge6_t3", "sl_mu_jge6_tge4",
    "sl_mu_j5_t2", "sl_el_j5_t3", "sl_el_j5_tge4", "sl_el_jge6_t2", "sl_el_jge6_t3", "sl_el_jge6_tge4",
    "dl_mumu_j3_t2", "dl_mumu_jge4_t2", "dl_mumu_jge3_t3", "dl_mumu_jge4_tge4",
    "dl_ee_j3_t2", "dl_ee_jge4_t2", "dl_ee_jge3_t3", "dl_ee_jge4_tge4",
    "dl_emu_j3_t2", "dl_emu_jge4_t2", "dl_emu_jge3_t3", "dl_emu_jge4_tge4",
]
print "Preparing S/sqrt(B)"
plt.figure(figsize=(8,6))
xs, xs_num, ys, es = plotlib.get_sb_cats(inf, categories, "")
plt.bar(xs_num, ys, 0.5, color="gray")
plt.errorbar(xs_num+0.25, ys, es, color="black", ls="none", elinewidth=2)
plt.xlim(0,len(xs))
plt.xticks(xs_num+0.25, [x.replace("_", " ") for x in xs], rotation=90, fontsize=16);
plt.ylabel("$S / \sqrt{B}$")
plotlib.svfg("plots/sob.png")
plt.clf()


# 
# categories = [
#     "sl_mu_j5_t2_boostedTop", "sl_mu_j5_t3_boostedTop", "sl_mu_j5_tge4_boostedTop", "sl_mu_jge6_t2_boostedTop", "sl_mu_jge6_t3_boostedTop", "sl_mu_jge6_tge4_boostedTop",
#     "sl_el_j5_t2_boostedTop", "sl_el_j5_t3_boostedTop", "sl_el_j5_tge4_boostedTop", "sl_el_jge6_t2_boostedTop", "sl_el_jge6_t3_boostedTop", "sl_el_jge6_tge4_boostedTop",
#     "sl_mu_j5_t2_boostedHiggs", "sl_mu_j5_t3_boostedHiggs", "sl_mu_j5_tge4_boostedHiggs", "sl_mu_jge6_t2_boostedHiggs", "sl_mu_jge6_t3_boostedHiggs", "sl_mu_jge6_tge4_boostedHiggs",
#     "sl_el_j5_t2_boostedHiggs", "sl_el_j5_t3_boostedHiggs", "sl_el_j5_tge4_boostedHiggs", "sl_el_jge6_t2_boostedHiggs", "sl_el_jge6_t3_boostedHiggs", "sl_el_jge6_tge4_boostedHiggs",
# ]
# print "Preparing S/sqrt(B)"
# plt.figure(figsize=(8,6))
# xs, xs_num, ys, es = plotlib.get_sb_cats(inf, categories, "")
# plt.bar(xs_num, ys, 0.5, color="gray")
# plt.errorbar(xs_num+0.25, ys, es, color="black", ls="none", elinewidth=2)
# plt.xlim(0,len(xs))
# plt.xticks(xs_num+0.25, [x.replace("_", " ") for x in xs], rotation=90, fontsize=16);
# plt.ylabel("$S / \sqrt{B}$")
# plotlib.svfg("plots/sob_boosted.png")
# plt.clf()


for cat in ["sl_mu", "sl_el", "dl_mumu", "dl_ee", "dl_emu"]:
    hs1 = inf.get("ttH_hbb/{0}/btag_LR_4b_2b_logit".format(cat))
    hb1 = inf.get("ttbarOther/{0}/btag_LR_4b_2b_logit".format(cat))
    hb2 = inf.get("ttbarPlusCCbar/{0}/btag_LR_4b_2b_logit".format(cat))
    hb3 = inf.get("ttbarPlusBBbar/{0}/btag_LR_4b_2b_logit".format(cat))
    hb4 = inf.get("ttbarPlus2B/{0}/btag_LR_4b_2b_logit".format(cat))
    hb5 = inf.get("ttbarPlusB/{0}/btag_LR_4b_2b_logit".format(cat))

    plt.figure(figsize=(6, 6))
    heplot.barhist(hs1, color="red", label="tt+H", lw=2, scaling="normed", rebin=4)
    heplot.barhist(hb1, color="blue", label="tt+ll", lw=2, scaling="normed", rebin=4)
    heplot.barhist(hb2, color="green", label="tt+cc", lw=2, scaling="normed", rebin=4)
    heplot.barhist(hb3, color="orange", label="tt+bb", lw=2, scaling="normed", rebin=4)
    heplot.barhist(hb4, color="purple", label="tt+2b", lw=2, scaling="normed", rebin=4)
    heplot.barhist(hb5, color="black", label="tt+b", lw=2, scaling="normed", rebin=4)
    plt.legend(loc="best")
    plotlib.svfg("plots/{0}_btag_lr.png".format(cat))

    r1, e1 = plotlib.calc_roc(hs1, hb1)
    r2, e2 = plotlib.calc_roc(hs1, hb2)
    r3, e3 = plotlib.calc_roc(hs1, hb3)
    r4, e4 = plotlib.calc_roc(hs1, hb4)
    r5, e5 = plotlib.calc_roc(hs1, hb5)
    plt.figure(figsize=(6,6))
    plt.plot(r1[:, 0], r1[:, 1], color="blue", label="tt+ll")
    plt.plot(r2[:, 0], r2[:, 1], color="green", label="tt+cc")
    plt.plot(r3[:, 0], r3[:, 1], color="orange", label="tt+bb")
    plt.plot(r4[:, 0], r4[:, 1], color="purple", label="tt+2b")
    plt.plot(r5[:, 0], r5[:, 1], color="black", label="tt+b")
    plt.grid()

    plt.yscale("log")
    plt.ylim(10**-5, 1)
    plt.xlim(0,1)

    plt.xlabel("tt+H(bb) efficiency")
    plt.ylabel("tt+X efficiency")
    plt.legend(loc="best")
    plotlib.svfg("plots/{0}_btag_lr_roc.png".format(cat))
