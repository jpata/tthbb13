import ROOT
import rootpy
import math
import matplotlib.pyplot as plt
from rootpy.plotting import root2matplotlib as rplt

import sys
sys.path += ["/Users/joosep/Documents/heplot"]
import heplot

sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_15/src/TTH/Plotting/python/joosep/")
sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_15/src/TTH/Plotting/python/Datacards/")
import sparse
import plotlib
import os

from rootpy.plotting import Hist
import Categorize, Cut
from collections import OrderedDict

def makeRule_SL(rules):
    outrules = OrderedDict()
    for rulename, rule in rules.items():
        outrules[rulename + "_mu"] = sparse.ProjectionRule(
            name=rule.name,
            cuts=rule.cuts + [("leptonFlavour", 1, 2)],
            project_axes=rule.project_axes,
            sample_filter=sparse.DataFilter("mu"),
            output_rename=sparse.DataRenameRule(rule),
            rebin=rule.rebin
        )
        outrules[rulename + "_el"] = sparse.ProjectionRule(
            name=rule.name,
            cuts=rule.cuts + [("leptonFlavour", 2, 3)],
            project_axes=rule.project_axes,
            sample_filter=sparse.DataFilter("el"),
            output_rename=sparse.DataRenameRule(rule),
            rebin=rule.rebin
        )
    return outrules


def get_yields(inf, samplelist, cutname, variable):
    yields = OrderedDict()
    for sample, nick in plotlib.samplelist:
        h = inf.Get("{0}/{1}/{2}/{2}".format(sample, cutname, variable))
        yields[sample] = h.Integral()
    return yields

def plot_yields(cutname, yields, htmlout):
    fig = plt.figure(figsize=(3,3))
    plt.pie(
        yields.values(),
        colors=[plotlib.colors[k] for k in yields.keys()]
    )
    s = yields["ttH_hbb"]
    b = sum([yields[k] for k in yields.keys() if k not in ["ttH_hbb"]])
    sob = s / b
    sosb = s / math.sqrt(b)
    plt.title(
        cutname +
        "\n$S={0:.2f}, B={1:.2f}$".format(s, b) +
        "\n$S/B = {0:.4f}, S/\sqrt{{B}} = {1:.4f}$".format(sob, sosb), y=0.94
    )
    plotlib.svfg("plots/{0}_yields.png".format(cutname))
    plotlib.svfg("plots/{0}_yields.pdf".format(cutname))
    htmlout.write('<a href="plots/{0}_yields.pdf"><img width="300" src="plots/{0}_yields.png"></a>\n'.format(cutname))
    plt.clf()
    del fig

if __name__ == "__main__":
    hsparse = Categorize.GetSparseHistograms(
        "/Users/joosep/Documents/tth/data/histograms/ControlPlotsSparse.root",
        ["ttH_hbb", "ttH_nonhbb"],
        [
            "ttbarPlus2B",
            "ttbarPlusB",
            "ttbarPlusBBbar",
            "ttbarPlusCCbar",
            "ttbarOther"
        ],
        category="sl",
        data=["SingleMuon", "SingleElectron"]
    )
    rules_bdt = OrderedDict()
    rules_mem = OrderedDict()

    cuts = [
        ("6j4t", [("numJets", 6, 8), ("nBCSVM", 4, 8)]),
        ("6j3t", [("numJets", 6, 8), ("nBCSVM", 3, 4)]),
        ("6j2t", [("numJets", 6, 8), ("nBCSVM", 2, 3)]),
        ("5j4t", [("numJets", 5, 6), ("nBCSVM", 4, 6)]),
        ("5j3t", [("numJets", 5, 6), ("nBCSVM", 3, 4)]),
        ("4j4t", [("numJets", 4, 5), ("nBCSVM", 4, 5)]),
        ("4j3t", [("numJets", 4, 5), ("nBCSVM", 3, 4)]),
    ]
    for cn, cut in cuts:
        rules_bdt[cn] = sparse.ProjectionRule(
            name=cn,
            cuts=cut,
            project_axes=["common_bdt"],
            rebin=4
        )
        rules_mem[cn] = sparse.ProjectionRule(
            name=cn,
            cuts=cut,
            project_axes=["mem_SL_0w2h2t"],
            rebin=6
        )
    
    inputs = OrderedDict()
    for hn, h in hsparse[0].items()+hsparse[1].items()+hsparse[4].items():
        inputs[sparse.InputKey(hn, "nominal")] = h
    for sample, systdicts in hsparse[2].items()+hsparse[3].items():
        for systname, hist in systdicts.items():
            inputs[sparse.InputKey(sample, systname)] = hist

    out_bdt = sparse.apply_rules(
        inputs,
        makeRule_SL(rules_bdt),
    )
    sparse.save_hdict("out_bdt.root", out_bdt)
    inf = rootpy.io.File("out_bdt.root")
    htmlout = open("index.html", "w")

    yields_categories = OrderedDict()
    for cutname, cut in cuts:

        htmlout.write('<h2>{0}</h2>\n'.format(cutname))
        
        fig = plt.figure(figsize=(6,6))
        r = plotlib.draw_data_mc(
            inf,
            "{0}/common_bdt/common_bdt".format(cutname),
            plotlib.samplelist,
            dataname=["data"],
            xlabel=plotlib.varnames["common_bdt"],
            xunit="",
            legend_fontsize=10, legend_loc="best",
            colors=[plotlib.colors.get(s[0]) for s in plotlib.samplelist],
            do_legend=True,
            show_overflow=True,
            title_extended="$,\\ \\mathcal{L}=2.6,\\ \\mathrm{fb}^{-1}$, " + cn,
            systematics=[
                ("_CMS_scale_jUp", "_CMS_scale_jDown"),
                ("_CMS_ttH_CSVLFUp", "_CMS_ttH_CSVLFDown"),
                ("_CMS_ttH_CSVHFUp", "_CMS_ttH_CSVHFDown"),
                ("_CMS_ttH_CSVHFStats1Up", "_CMS_ttH_CSVHFStats1Down"),
                ("_CMS_ttH_CSVHFStats2Up", "_CMS_ttH_CSVHFStats2Down"),
                ("_CMS_ttH_CSVLFStats1Up", "_CMS_ttH_CSVLFStats1Down"),
                ("_CMS_ttH_CSVLFStats2Up", "_CMS_ttH_CSVLFStats2Down"),
                ("_CMS_ttH_CSVcErr1Up", "_CMS_ttH_CSVcErr1Down"),
                ("_CMS_ttH_CSVcErr2Up", "_CMS_ttH_CSVcErr2Down"),
            ],
            #blindFunc=blind,
            #do_pseudodata=True
        )

        plotlib.svfg("plots/common_bdt_{0}.pdf".format(cutname))
        plotlib.svfg("plots/common_bdt_{0}.png".format(cutname))
        htmlout.write('<a href="plots/common_bdt_{0}.pdf"><img width="600" src="plots/common_bdt_{0}.png"></a>\n'.format(cutname))
        plt.clf()
        del fig

        fig = plt.figure(figsize=(6,6))
        table = []
        for k, v in r[2].items():
            if k == "data":
                continue
            heplot.barhist(v, color=plotlib.colors[k], lw=2, scaling="normed", label=dict(plotlib.samplelist)[k])
            table += [(k, v.Integral())]
        plt.xlabel(plotlib.varnames["common_bdt"])
        plt.legend(loc="best", numpoints=1, prop={'size': 10}, ncol=2, frameon=False)
        plt.ylim(bottom=0)
        plt.title(cutname)
        plotlib.svfg("plots/{0}_shapes.pdf".format(cutname))
        plotlib.svfg("plots/{0}_shapes.png".format(cutname))
        htmlout.write('<a href="plots/{0}_shapes.pdf"><img width="600" src="plots/{0}_shapes.png"></a>\n'.format(cutname))
        plt.clf()
        del fig

        systout = open("syst_{0}.html".format(cutname), "w")
        syst_pairs = [r[4].keys()[i:i+2] for i in range(0,len(r[4].keys()),2)]

        for s1, s2 in syst_pairs:
            syst_name = s1.replace("Up", "")
            systout.write('<h2>{0}</h2>\n'.format(syst_name))
            for sample in r[2].keys():
                #print cutname, syst_name, sample
                plt.figure(figsize=(6,6))
                heplot.barhist(r[2][sample], color="black", label="nominal")
                heplot.barhist(r[4][s1][sample], color="red", label="up")
                heplot.barhist(r[4][s2][sample], color="blue", label="down")
                plt.title(cutname + " " + syst_name.replace("_", "") + " " + sample.replace("_", ""))
                p = "plots/{0}".format(syst_name)
                if not os.path.exists(p):
                    os.makedirs(p)
                plotlib.svfg("plots/{0}/{1}_{2}.pdf".format(syst_name, cutname, sample))
                plotlib.svfg("plots/{0}/{1}_{2}.png".format(syst_name, cutname, sample))
                systout.write('<a href="plots/{0}/{1}_{2}.pdf"><img width="300" src="plots/{0}/{1}_{2}.png"></a>\n'.format(syst_name, cutname, sample))
        systout.close()
        htmlout.write('systematics: <a href="syst_{0}.html"> link </a>\n'.format(cutname))

        yields = get_yields(inf, plotlib.samplelist, cutname, "common_bdt")
        plot_yields(cutname, yields, htmlout)
        yields_categories[cutname] = yields

        htmlout.write('<br>\n')
        htmlout.write('<br>\n')

    
    #     
    # out_mem = sparse.apply_rules(
    #     inputs,
    #     makeRule_SL(rules_mem),
    # )
    # sparse.save_hdict("out_mem.root", out_mem)
