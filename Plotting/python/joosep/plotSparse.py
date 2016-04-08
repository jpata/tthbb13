import ROOT
import rootpy
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rootpy.plotting import root2matplotlib as rplt

import sys
sys.path += ["/Users/joosep/Documents/heplot"]
import heplot

import sparse
import plotlib
import os

from rootpy.plotting import Hist
from collections import OrderedDict

def get_yields(inf, samplelist, cutname, variable):
    yields = OrderedDict()
    for sample, nick in plotlib.samplelist:
        h = inf.Get("{0}/{1}/{2}".format(sample, cutname, variable))
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
    plotlib.svfg("output/plots/pie_{0}_yields.png".format(cutname))
    plotlib.svfg("output/plots/pie_{0}_yields.pdf".format(cutname))
    htmlout.write('<a href="output/plots/pie_{0}_yields.pdf"><img width="300" src="output/plots/pie_{0}_yields.png"></a>\n'.format(cutname))
    plt.clf()
    del fig

def analysis_report(analysis):
    pass

def escape(s):
    return s.replace("_", "")

def category_report(htmlout_master, path, category):
    htmlout = open("output/{0}.html".format(category.full_name), "w")

    htmlout_master.write('<a href="{0}.html">{0}</a>\n'.format(category.full_name))
    htmlout_master.write('<br>')

    inf_name = path + category.name + ".root"
    inf = rootpy.io.File(inf_name)
    procs = category.processes
    procs_names = []
    for proc in procs:
        procs_names += [(proc, escape(proc))]

    cn = escape(category.name)

    syst_pairs = [
        ("_CMS_scale_jUp", "_CMS_scale_jDown"),
        ("_CMS_ttH_CSVLFUp", "_CMS_ttH_CSVLFDown"),
        ("_CMS_ttH_CSVHFUp", "_CMS_ttH_CSVHFDown"),
        ("_CMS_ttH_CSVHFStats1Up", "_CMS_ttH_CSVHFStats1Down"),
        ("_CMS_ttH_CSVHFStats2Up", "_CMS_ttH_CSVHFStats2Down"),
        ("_CMS_ttH_CSVLFStats1Up", "_CMS_ttH_CSVLFStats1Down"),
        ("_CMS_ttH_CSVLFStats2Up", "_CMS_ttH_CSVLFStats2Down"),
        ("_CMS_ttH_CSVcErr1Up", "_CMS_ttH_CSVcErr1Down"),
        ("_CMS_ttH_CSVcErr2Up", "_CMS_ttH_CSVcErr2Down"),
    ]

    htmlout.write('<h2>{0}</h2>\n'.format(category.full_name))

    fig = plt.figure(figsize=(6,6))
    r = plotlib.draw_data_mc(
        inf,
        "{0}/{1}".format(category.name, category.discriminator),
        procs_names,
        dataname=["data"],
        xlabel=plotlib.varnames[category.discriminator],
        xunit="",
        legend_fontsize=10, legend_loc="best",
        colors=[plotlib.colors.get(p) for p in procs],
        do_legend=True,
        show_overflow=True,
        title_extended="$,\\ \\mathcal{L}=2.6,\\ \\mathrm{fb}^{-1}$, " + cn,
        systematics=syst_pairs,
        #blindFunc=blind,
        #do_pseudodata=True
    )
    plotlib.svfg("output/plots/{0}/{1}.pdf".format(category.discriminator, category.name))
    plotlib.svfg("output/plots/{0}/{1}.png".format(category.discriminator, category.name))
    htmlout.write('<a href="plots/{0}/{1}.pdf"><img width="600" src="plots/{0}/{1}.png"></a>\n'.format(
        category.discriminator, category.name
    ))
    plt.clf()
    del fig
    
    
    #Plot the shapes of all the components
    fig = plt.figure(figsize=(6,6))
    table = []
    for k, v in r[2].items():
        if k == "data":
            continue
        heplot.barhist(v, color=plotlib.colors.get(k, "gray"), lw=2, scaling="normed", label=dict(plotlib.samplelist)[k])
        table += [(k, v.Integral())]
    plt.xlabel(plotlib.varnames[category.discriminator])
    plt.legend(loc="best", numpoints=1, prop={'size': 10}, ncol=2, frameon=False)
    plt.ylim(bottom=0)
    plt.title(cn)
    plotlib.svfg("output/plots/{0}/{1}_shapes.pdf".format(
        category.discriminator, category.name
    ))
    plotlib.svfg("output/plots/{0}/{1}_shapes.png".format(
        category.name, category.discriminator
    ))
    htmlout.write('<a href="plots/{0}/{1}_shapes.pdf"><img width="600" src="plots/{0}/{1}_shapes.png"></a>\n'.format(
        category.name, category.discriminator
    ))
    plt.clf()
    del fig
    
    systout_fn = "output/{0}_{1}_discriminator.html".format(
        category.name, category.discriminator
    )
    systout = open(systout_fn, "w")
    syst_pairs = [r[4].keys()[i:i+2] for i in range(0,len(r[4].keys()),2)]
    
    #plot the systematic variations
    if category.do_limit:
        for s1, s2 in syst_pairs:
            syst_name = s1.replace("Up", "")
            print syst_name
            systout.write('<h2>{0}</h2>\n'.format(syst_name))
            for sample in r[2].keys():
                fig = plt.figure(figsize=(6,6))
                heplot.barhist(r[2][sample], color="black", label="nominal")
                heplot.barhist(r[4][s1][sample], color="red", label="up")
                heplot.barhist(r[4][s2][sample], color="blue", label="down")
                plt.title(cn + " " + syst_name.replace("_", "") + " " + sample.replace("_", ""))
                p = "plots/{0}/syst{1}".format(category.discriminator, syst_name)
                if not os.path.exists(p):
                    os.makedirs(p)
                plotlib.svfg("output/plots/{2}/syst{1}/{0}_{3}.pdf".format(category.discriminator, syst_name, category.name, sample))
                #plotlib.svfg("output/plots/{2}/syst{1}/{0}_{3}.png".format(category.discriminator, syst_name, category.name, sample))
                systout.write(
                    '<a href="plots/{2}/syst{1}/{0}_{3}.pdf"><img width="300" src="plots/{2}/syst{1}/{0}_{3}.png"></a>\n'.format(
                        category.discriminator, syst_name, category.name, sample)
                )
                plt.clf()
                del fig
        systout.close()
        htmlout.write('<br><br><br>systematics: <a href="{0}"> link </a>\n'.format(os.path.basename(systout_fn)))
    
    htmlout.close()
    #matplotlib.pyplot.close("all")

from TTH.Plotting.Datacards.AnalysisSpecification import analysis
htmlout_master = open("output/index.html", "w")
for cat in analysis.categories:
    print cat.full_name
    category_report(
        htmlout_master,
        "/Users/joosep/Documents/tth/data/histograms/GC45c610484aa0/AnalysisSpecification/",
        cat
    )

# 
# from TTH.Plotting.Datacards.AnalysisSpecificationDL import analysis
# for cat in analysis.categories[:1]:
#     print cat.full_name
#     category_report(
#         htmlout_master,
#         "/Users/joosep/Documents/tth/data/histograms/GC45c610484aa0/AnalysisSpecificationDL/",
#         cat
#     )

htmlout_master.close()

# 
# if __name__ == "__main__":
#     htmlout_master = open("output/index.html", "w")
# 
#     for varname in variables:
#         root_out = "out.root"
#         inf = rootpy.io.File(root_out)
#         htmlout = open("output/{0}.html".format(varname), "w")
#         htmlout_master.write('<a href="{0}.html">{0}</a>\n'.format(varname))
#         htmlout_master.write('<br>')
#         yields_categories = OrderedDict()
#         for cutname in cuts:
# 
#             htmlout.write('<h2>{0}</h2>\n'.format(cutname))
#             cn = cutname.replace("_", "")
#             fig = plt.figure(figsize=(6,6))
#             r = plotlib.draw_data_mc(
#                 inf,
#                 "{0}/{1}".format(cutname, varname),
#                 plotlib.samplelist,
#                 dataname=["data"],
#                 xlabel=plotlib.varnames[varname],
#                 xunit="",
#                 legend_fontsize=10, legend_loc="best",
#                 colors=[plotlib.colors.get(s[0]) for s in plotlib.samplelist],
#                 do_legend=True,
#                 show_overflow=True,
#                 title_extended="$,\\ \\mathcal{L}=2.6,\\ \\mathrm{fb}^{-1}$, " + cn,
#                 systematics=[
#                     ("_CMS_scale_jUp", "_CMS_scale_jDown"),
#                     ("_CMS_ttH_CSVLFUp", "_CMS_ttH_CSVLFDown"),
#                     ("_CMS_ttH_CSVHFUp", "_CMS_ttH_CSVHFDown"),
#                     ("_CMS_ttH_CSVHFStats1Up", "_CMS_ttH_CSVHFStats1Down"),
#                     ("_CMS_ttH_CSVHFStats2Up", "_CMS_ttH_CSVHFStats2Down"),
#                     ("_CMS_ttH_CSVLFStats1Up", "_CMS_ttH_CSVLFStats1Down"),
#                     ("_CMS_ttH_CSVLFStats2Up", "_CMS_ttH_CSVLFStats2Down"),
#                     ("_CMS_ttH_CSVcErr1Up", "_CMS_ttH_CSVcErr1Down"),
#                     ("_CMS_ttH_CSVcErr2Up", "_CMS_ttH_CSVcErr2Down"),
#                 ],
#                 #blindFunc=blind,
#                 #do_pseudodata=True
#             )
#             
#             plotlib.svfg("output/plots/{1}_{0}.pdf".format(cutname, varname))
#             plotlib.svfg("output/plots/{1}_{0}.png".format(cutname, varname))
#             htmlout.write('<a href="plots/{1}_{0}.pdf"><img width="600" src="plots/{1}_{0}.png"></a>\n'.format(cutname, varname))
#             plt.clf()
#             del fig
#             
#             fig = plt.figure(figsize=(6,6))
#             table = []
#             for k, v in r[2].items():
#                 if k == "data":
#                     continue
#                 heplot.barhist(v, color=plotlib.colors.get(k, "gray"), lw=2, scaling="normed", label=dict(plotlib.samplelist)[k])
#                 table += [(k, v.Integral())]
#             plt.xlabel(plotlib.varnames["common_bdt"])
#             plt.legend(loc="best", numpoints=1, prop={'size': 10}, ncol=2, frameon=False)
#             plt.ylim(bottom=0)
#             plt.title(cn)
#             plotlib.svfg("output/plots/{0}/{1}_shapes.pdf".format(varname, cutname))
#             plotlib.svfg("output/plots/{0}/{1}_shapes.png".format(varname, cutname))
#             htmlout.write('<a href="plots/{0}/{1}_shapes.pdf"><img width="600" src="plots/{0}/{1}_shapes.png"></a>\n'.format(varname, cutname))
#             plt.clf()
#             del fig
#             
#             
#             if varname == "common_bdt":
#                 yields = get_yields(inf, plotlib.samplelist, cutname, "common_bdt")
#                 plot_yields(cn, yields, htmlout)
#                 yields_categories[cutname] = yields
#             
#                 htmlout.write('<br>\n')
#                 htmlout.write('<br>\n')
#                 htmlout.flush()
#             
#             systout_fn = "output/{0}_{1}.html".format(varname, cutname)
#             systout = open(systout_fn, "w")
#             syst_pairs = [r[4].keys()[i:i+2] for i in range(0,len(r[4].keys()),2)]
#             
#             for s1, s2 in syst_pairs:
#                 syst_name = s1.replace("Up", "")
#                 systout.write('<h2>{0}</h2>\n'.format(syst_name))
#                 for sample in r[2].keys():
#                     fig = plt.figure(figsize=(6,6))
#                     heplot.barhist(r[2][sample], color="black", label="nominal")
#                     heplot.barhist(r[4][s1][sample], color="red", label="up")
#                     heplot.barhist(r[4][s2][sample], color="blue", label="down")
#                     plt.title(cn + " " + syst_name.replace("_", "") + " " + sample.replace("_", ""))
#                     p = "plots/{0}/syst{1}".format(varname, syst_name)
#                     if not os.path.exists(p):
#                         os.makedirs(p)
#                     plotlib.svfg("output/plots/{0}/syst{1}/{2}_{3}.pdf".format(varname, syst_name, cutname, sample))
#                     plotlib.svfg("output/plots/{0}/syst{1}/{2}_{3}.png".format(varname, syst_name, cutname, sample))
#                     systout.write('<a href="plots/{0}/syst{1}/{2}_{3}.pdf"><img width="300" src="plots/{0}/syst{1}/{2}_{3}.png"></a>\n'.format(varname, syst_name, cutname, sample))
#                     plt.clf()
#                     del fig
#             systout.close()
#             htmlout.write('<br><br>systematics: <a href="{0}"> link </a>\n'.format(systout_fn))
#             matplotlib.pyplot.close("all")
