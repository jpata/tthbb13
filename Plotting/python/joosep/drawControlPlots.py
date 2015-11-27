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
import tabulate
from collections import OrderedDict

backgrounds = ["ttbarOther", "ttbarPlusBBbar", "ttbarPlusB", "ttbarPlus2B", "ttbarPlusCCbar"]

slist = [
 ('ttH_hbb', 'ttHbb'),
 ('ttbarPlusBBbar', 'ttbarPlusBBbar'),
 ('ttbarPlusB', 'ttbarPlusB'),
 ('ttbarPlus2B', 'ttbarPlus2B'),
 ('ttbarPlusCCbar', 'ttbarPlusCCbar'),
 ('ttbarOther', 'ttbarOther')
]

input_file = "/Users/joosep/Dropbox/tth/ControlPlotsSparse.root"

outfile = open("report.html", "w")
outfile.write("<h1>ttH report</h1>\n")
outfile.write("input file: {0}<br>\n".format(input_file))

for sample in slist:
    outfile.write("sample {0}<br>\n".format(sample[0]))

sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_15/src/TTH/Plotting/python/joosep/")
inf = rootpy.io.File(input_file)


sl_channels = ["sl_mu_j5_t2", "sl_mu_j5_t3", "sl_mu_j5_tge4", "sl_mu_jge6_t2", "sl_mu_jge6_t3", "sl_mu_jge6_tge4"]
dl_channels = ["dl_mumu_j3_t2", "dl_mumu_jge3_t3", "dl_mumu_jge4_t2", "dl_mumu_jge4_tge4"]

def writeSyncTable(channels, title):
    outfile.write("<h2>{0}</h2>\n".format(title))
    table_hists, table = plotlib.sync_table(
        inf,
        channels,
        backgrounds
    )
    outfile.write(
        tabulate.tabulate(table, tablefmt="html", headers=channels)
    )

writeSyncTable(sl_channels, "SL mu")
writeSyncTable([ch.replace("mu", "el") for ch in sl_channels], "SL el")

writeSyncTable(dl_channels, "DL mumu")
writeSyncTable([ch.replace("mumu", "ee") for ch in dl_channels], "DL ee")
writeSyncTable([ch.replace("mumu", "emu") for ch in dl_channels], "DL emu")

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
outfile.write("<br><img src=\"plots/sob.png\" style=\"width:600px;height:600px;\"> <br>\n")
plt.clf()

categories = [
    "sl_mu_j5_t2_boostedTopOnly", "sl_mu_j5_t3_boostedTopOnly", "sl_mu_j5_tge4_boostedTopOnly", "sl_mu_jge6_t2_boostedTopOnly", "sl_mu_jge6_t3_boostedTopOnly", "sl_mu_jge6_tge4_boostedTopOnly",
    "sl_el_j5_t2_boostedTopOnly", "sl_el_j5_t3_boostedTopOnly", "sl_el_j5_tge4_boostedTopOnly", "sl_el_jge6_t2_boostedTopOnly", "sl_el_jge6_t3_boostedTopOnly", "sl_el_jge6_tge4_boostedTopOnly",
    "sl_mu_j5_t2_boostedHiggsOnly", "sl_mu_j5_t3_boostedHiggsOnly", "sl_mu_j5_tge4_boostedHiggsOnly", "sl_mu_jge6_t2_boostedHiggsOnly", "sl_mu_jge6_t3_boostedHiggsOnly", "sl_mu_jge6_tge4_boostedHiggsOnly",
    "sl_el_j5_t2_boostedHiggsOnly", "sl_el_j5_t3_boostedHiggsOnly", "sl_el_j5_tge4_boostedHiggsOnly", "sl_el_jge6_t2_boostedHiggsOnly", "sl_el_jge6_t3_boostedHiggsOnly", "sl_el_jge6_tge4_boostedHiggsOnly",
]
print "Preparing S/sqrt(B)"
plt.figure(figsize=(8,6))
xs, xs_num, ys, es = plotlib.get_sb_cats(inf, categories, "")
plt.bar(xs_num, ys, 0.5, color="gray")
plt.errorbar(xs_num+0.25, ys, es, color="black", ls="none", elinewidth=2)
plt.xlim(0,len(xs))
plt.xticks(xs_num+0.25, [x.replace("_", " ") for x in xs], rotation=90, fontsize=16);
plt.ylabel("$S / \sqrt{B}$")
outfile.write("<br><img src=\"plots/sob_boosted.png\" style=\"width:600px;height:600px;\"> <br>\n")
plt.clf()


outfile.write("<h1>B-tag likelihood ratio</h1>\n")
blr_cuts = OrderedDict()
for cat in [
    "sl",
    "sl_j5_t2",
    "sl_j5_t3",
    "sl_j5_tge4",
    "sl_jge6_t2",
    "sl_jge6_t3",
    "sl_jge6_tge4",

    #"dl",
    "dl_j3_t2",
    "dl_jge3_t3",
    "dl_jge4_t2",
    "dl_jge4_tge4",
    ]:
    outfile.write("<h2>Category: {0}</h2>\n".format(cat))
    hs1 = inf.get("ttH_hbb/{0}/btag_LR_4b_2b_logit".format(cat))
    hb1 = inf.get("ttbarOther/{0}/btag_LR_4b_2b_logit".format(cat))
    hb2 = inf.get("ttbarPlusCCbar/{0}/btag_LR_4b_2b_logit".format(cat))
    hb3 = inf.get("ttbarPlusBBbar/{0}/btag_LR_4b_2b_logit".format(cat))
    hb4 = inf.get("ttbarPlus2B/{0}/btag_LR_4b_2b_logit".format(cat))
    hb5 = inf.get("ttbarPlusB/{0}/btag_LR_4b_2b_logit".format(cat))

    idx = plotlib.get_cut_at_eff(hs1, 0.5)
    blr_cut = hs1.GetBinLowEdge(idx)
    blr_cuts[cat] = blr_cut

    outfile.write("blr cut at 50% ttH efficiency: {0} <br>\n".format(blr_cut))
    plt.figure(figsize=(6, 6))
    heplot.barhist(hs1, color="red", label="tt+H", lw=2, scaling="normed", rebin=4)
    heplot.barhist(hb1, color="blue", label="tt+ll", lw=2, scaling="normed", rebin=4)
    heplot.barhist(hb2, color="green", label="tt+cc", lw=2, scaling="normed", rebin=4)
    heplot.barhist(hb3, color="orange", label="tt+bb", lw=2, scaling="normed", rebin=4)
    heplot.barhist(hb4, color="purple", label="tt+2b", lw=2, scaling="normed", rebin=4)
    heplot.barhist(hb5, color="black", label="tt+b", lw=2, scaling="normed", rebin=4)
    plt.legend(loc="best")
    fname = "plots/{0}_btag_lr.png".format(cat)
    plotlib.svfg(fname)
    outfile.write("<br><img src=\"{0}\" style=\"width:600px;height:600px;\"> <br>\n".format(fname))

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
    fname = "plots/{0}_btag_lr_roc.png".format(cat)
    plotlib.svfg(fname)
    outfile.write("<br><img src=\"{0}\" style=\"width:600px;height:600px;\"> <br>\n".format(fname))

outfile.write("<h3>B-tag likelihood cuts</h3>\n")
for cname, cut in blr_cuts.items():
    outfile.write("<br>{0}: {1}\n".format(cname, cut))

outfile.write("<h1>MEM</h1>\n")
for cat, var in [
    ("sl_mu_jge6_tge4_blrH", "mem_SL_0w2h2t"),
    ("sl_mu_jge6_t3_blrH", "mem_SL_0w2h2t"),
    ("sl_mu_jge6_tge4_blrH", "mem_SL_2w2h2t"),
    ("sl_mu_jge6_t3_blrH", "mem_SL_2w2h2t"),
    ]:
    outfile.write("<h2>Category: {0} variable: {1}</h2>\n".format(cat, var))

    hs = inf.get("ttH_hbb/{0}/{1}".format(cat, var))
    hbkgs = [inf.get("{0}/{1}/{2}".format(bkg, cat, var)) for bkg in backgrounds]
    hbkg = sum(hbkgs)
    plt.figure(figsize=(6,6))
    heplot.barhist(hs, scaling="normed", color="red", label="sig", lw=2)
    heplot.barhist(hbkg, scaling="normed", color="blue", label="bkg", lw=2)
    plt.xlabel(plotlib.varnames[var])
    plt.ylabel("fraction of events")
    plt.legend(loc="best")
    fname = "plots/{0}_{1}.png".format(cat, var)
    plotlib.svfg(fname)
    outfile.write("<br><img src=\"{0}\" style=\"width:600px;height:600px;\"> <br>\n".format(fname))

    rocs = [plotlib.calc_roc(hs, hb) for hb in [hbkg] + hbkgs]
    plt.figure(figsize=(6,6))
    labels = ["bkg"] + backgrounds
    for (r, e), l in zip(rocs, labels):
        lw = 1
        if l == "bkg":
            lw = 2
        plt.plot(r[:, 0], r[:, 1], label=l, lw=lw)
    plt.legend(loc="best")
    plt.xlabel("tt+H(bb) eff.")
    plt.ylabel("tt+jets eff.")
    fname = "plots/{0}_{1}_roc.png".format(cat, var)
    plotlib.svfg(fname)
    outfile.write("<br><img src=\"{0}\" style=\"width:600px;height:600px;\"> <br>\n".format(fname))

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
    "sl_mu_j5_t2_boostedHiggsOnly",
    "sl_mu_j5_t2_boostedTopOnly",
    "sl_mu_j5_t2_boostedHiggsTop",
    "sl_mu_j5_t3",
    "sl_mu_j5_tge4",
    "sl_mu_jge6_t2",
    "sl_mu_jge6_t3",
    "sl_mu_jge6_tge4",
    # 
    # #"sl_el",
    "sl_el_j5_t2",
    "sl_el_j5_t3",
    "sl_el_j5_tge4",
    "sl_el_jge6_t2",
    "sl_el_jge6_t3",
    "sl_el_jge6_tge4",
    # 
    "dl_mumu_j3_t2",
    "dl_ee_j3_t2",
    "dl_emu_j3_t2",
    # 
    "dl_mumu_jge3_t3",
    "dl_ee_jge3_t3",
    "dl_emu_jge3_t3",
    # 
    "dl_mumu_jge4_t2",
    "dl_ee_jge4_t2",
    "dl_emu_jge4_t2",
    # 
    "dl_mumu_jge4_tge4",
    "dl_ee_jge4_tge4",
    "dl_emu_jge4_tge4",
    ]:
    print cat
    outfile.write("<h2>Category: {0}</h2>\n".format(cat))

    for distr, kdict in [
        #("nhiggsCandidate", {"log":True}),
        ("numJets", {}),
        ("nBCSVM", {}),
        #("nPVs", {}),
        ("btag_LR_4b_2b_logit", {"rebin":5}),

        ("jet0_pt", {"rebin":5, "log":True, "xunit":"GeV"}),
        ("jet0_btagCSV", {"rebin":5, "log":True}),
        #("jet0_btagBDT", {"rebin":1, "log":True}),

        ("jet1_pt", {"rebin":5, "log":True, "xunit":"GeV"}),
        ("jet1_btagCSV", {"rebin":5, "log":True}),
        #("jet1_btagBDT", {"rebin":1, "log":True}),

        ("higgsCandidate_pt", {"rebin":5, "log":True, "xunit":"GeV"}),
        ("higgsCandidate_bbtag", {"rebin":5}),
        ("topCandidate_pt", {"rebin":5, "log":True, "xunit":"GeV"}),
        ("topCandidate_mass", {"rebin":5, "xunit":"GeV"}),

    ]:
        if not "boosted" in cat and "Candidate" in distr:
            continue
        outfile.write("<h3>Variable: {0}</h2>\n".format(distr))
        r = plotlib.draw_data_mc(
            inf,
            cat + "/" + distr,
            slist,
            dataname=plotlib.getDataname(cat), xlabel=plotlib.varnames[distr],
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
        fname = "plots/{0}_{1}.png".format(cat, distr)
        plotlib.svfg(fname)
        outfile.write("<br><img src=\"{0}\" style=\"width:600px;height:600px;\"> <br>\n".format(fname))
        plt.clf()
        del r

outfile.close()
