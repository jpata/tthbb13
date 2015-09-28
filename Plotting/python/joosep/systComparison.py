import sys
sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_5/src/TTH/Plotting/python/joosep/")
from plotlib import *
from samples import sample_shortname, samples_dict, colors, cut_map
import rootpy

tf = rootpy.io.File("/Users/joosep/Dropbox/tth/datacards/ref2_spring15/Datacard-2015-09-28-1640/ControlPlots.root")

cuts_dl = [
    ["dl_j3_t2", ["mem_DL_0w2h2t"]],
    ["dl_jge3_tge3", ["mem_DL_0w2h2t"]],
    ["dl_jge4_t2", ["mem_DL_0w2h2t"]],
    ["dl_jge4_tge4", ["mem_DL_0w2h2t"]],
]

cuts_sl = [

    ["sl_j4_t3", ["mem_SL_0w2h2t"]],
    ["sl_j4_t4", ["mem_SL_0w2h2t"]],
    ["sl_j5_t3", ["mem_SL_0w2h2t"]],
    ["sl_j5_tge4", ["mem_SL_0w2h2t"]],
    ["sl_jge6_t2", ["mem_SL_0w2h2t"]],
    ["sl_jge6_t3", ["mem_SL_0w2h2t"]],
    ["sl_jge6_tge4", ["mem_SL_0w2h2t"]],
]
sl_k = [k[0] + "/jet0_pt" for k in cuts_sl]

processes = [
    "ttH_hbb",
    "ttH_nohbb",
    "ttbarPlus2B",
    "ttbarPlusB",
    "ttbarPlusBBbar",
    "ttbarPlusCCbar",
    "ttbarOther",
]
slist = [(s, sample_shortname[s]) for s in ["ttH_hbb", "ttbarPlusBBbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusCCbar", "ttbarOther", "ttw_wqq", "ttw_wlnu", "ttz_zqq", "ttz_zllnunu"]]
collist = [colors.get(s[0], (0.4,0.4,0.4)) for s in slist]

for s in sl_k:
    cuts = cut_map[s.split("/")[0]]

    draw_data_mc(tf, s, slist, xlabel="leading jet $p_T$ [GeV]",
        yunit="GeV", title_extended=", L=10 $\mathrm{fb}^{-1}$, " + cuts, do_pseudodata=False, do_legend=False,
        colors = collist
    );
    plt.savefig("{0}.png".format(s.replace("/", "__")), bbox_inches='tight', pad_inches=1)
    plt.clf()

    s = s.replace("jet0_pt", "mem_SL_0w2h2t")
    a1, a2, hs = draw_data_mc(tf, s, slist, xlabel="MEM discriminator",
        ylabel="events / bin", title_extended=", L=10 $\mathrm{fb}^{-1}$, " + cuts, do_pseudodata=False, do_legend=False,
        colors=collist
    );
    plt.savefig("{0}.png".format(s.replace("/", "__")), bbox_inches='tight', pad_inches=1)
    plt.clf()
# for proc in processes:
#     for cat, varlist in cuts_sl+cuts_dl:
#         for sname, systpair in [
#             ("CMS_ttH_CSVHF", ["_CMS_ttH_CSVHFUp", "_CMS_ttH_CSVHFDown"]),
#             ("CMS_ttH_CSVLF", ["_CMS_ttH_CSVLFUp", "_CMS_ttH_CSVLFDown"]),
#             ("CMS_ttH_CSVStats1", ["_CMS_ttH_CSVStats1Up", "_CMS_ttH_CSVStats1Down"]),
#             ("CMS_ttH_CSVStats2", ["_CMS_ttH_CSVStats2Up", "_CMS_ttH_CSVStats2Down"]),
#             ("JES", ["_CMS_scale_jUp", "_CMS_scale_jDown"])
#         ]:
#             for var in varlist:
#                 print proc, cat, sname
#                 plt.figure(figsize=(6,6))
#                 ax = plt.axes()
#                 syst_comparison(tf, "{0}/{1}/{2}".format(proc, cat, var), [""]+systpair, rebin=1)
#                 #plt.tight_layout()
#                 plt.savefig("{0}__{1}__{2}__{3}.png".format(var, proc, cat, sname), bbox_inches='tight', pad_inches=1)
#                 plt.clf()
#             #plt.xlabel(r"leading jet $\mathrm{\xi}_{\mathrm{CSVv2}}$")
