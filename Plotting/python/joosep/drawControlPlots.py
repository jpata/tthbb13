import sys
sys.path += ["/Users/joosep/Documents/heplot/"]
import heplot, rootpy
import numpy as np
import matplotlib.pyplot as plt
import pandas
import rootpy.plotting.root2matplotlib as rplt
import ROOT, plotlib, heplot

slist = [
 ('ttH_hbb', 'ttHbb'),
 ('ttbarPlusBBbar', 'ttbarPlusBBbar'),
 ('ttbarPlusB', 'ttbarPlusB'),
 ('ttbarPlus2B', 'ttbarPlus2B'),
 ('ttbarPlusCCbar', 'ttbarPlusCCbar'),
 ('ttbarOther', 'ttbarOther')
]

sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_15/src/TTH/Plotting/python/joosep/")
inf = rootpy.io.File("/Users/joosep/Desktop/ControlPlotsSparse.root")

for cat in [
    "sl_mu_j5_t3_boostedHiggs", "sl_mu_j5_tge4_boostedHiggs",
    "sl_mu_jge6_t2_boostedHiggs", "sl_mu_jge6_t3_boostedHiggs",
    "sl_el_j5_t3_boostedHiggs", "sl_el_j5_tge4_boostedHiggs",
    "sl_el_jge6_t2_boostedHiggs", "sl_el_jge6_t3_boostedHiggs",
    ]:
    print cat
    for distr, kdict in [
        #("jet0_btagCSV", {"rebin":10, "log":True}),
        #("jet0_pt", {"rebin":10, "log":True, "xunit":"GeV"}),
        #("higgsCandidate_pt", {"rebin":10, "log":True, "xunit":"GeV"}),
        #("higgsCandidate_eta", {"rebin":10}),
        ("higgsCandidate_bbtag", {"rebin":10}),
    ]:
        print distr
        r = plotlib.draw_data_mc(
            inf,
            cat + "/" + distr,
            slist,
            dataname=["SingleMuon" if "mu" in cat else "SingleElectron"], xlabel=plotlib.varnames[distr],
            xunit=kdict.get("xunit", ""),
            legend_fontsize=10, legend_loc="best", colors=plotlib.samplecolors,
            do_legend=True,
            rebin=kdict.get("rebin", 1),
            show_overflow = True, title_extended="\n$\\mathcal{L}=1.28\\ \\mathrm{fb}^{-1}$"
        )
        if kdict.get("log", False):
            r[0].set_yscale("log")
            r[0].set_ylim(bottom=1, top=r[3]["tot"].GetMaximum()*10)
        #plotlib.svfg("{0}_{1}.pdf".format(distr, cat))
        plotlib.svfg("{0}_{1}.png".format(distr, cat))
        plt.clf()
