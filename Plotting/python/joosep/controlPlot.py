import ROOT
import logging

import matplotlib
from matplotlib import rc
#temporarily disable true latex for fast testing
rc('text', usetex=False)
matplotlib.use('PS') #needed on T3
import matplotlib.pyplot as plt

import sys, os, copy
from collections import OrderedDict
import heplot, plotlib

import rootpy
from rootpy.plotting import Hist
from rootpy.plotting import root2matplotlib as rplt

DO_SYSTEMATICS = False
DO_PARALLEL = False

procs_names = [
    ("ttH_hbb", "tt+H(bb)"),
    ("ttH_nonhbb", "tt+H(non-bb)"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc")
]
procs = [x[0] for x in procs_names]


syst_pairs = []

if DO_SYSTEMATICS:
    syst_pairs.extend([
        ("_puUp", "_puaDown"),
        ("_CMS_scale_jUp", "_CMS_scale_jDown"),
        ("_CMS_res_jUp", "_CMS_res_jDown"),
        ("_CMS_ttH_CSVcferr1Up", "_CMS_ttH_CSVcferr1Down"),
        ("_CMS_ttH_CSVcferr2Up", "_CMS_ttH_CSVcferr2Down"),
        ("_CMS_ttH_CSVhfUp", "_CMS_ttH_CSVhfDown"),
        ("_CMS_ttH_CSVhfstats1Up", "_CMS_ttH_CSVhfstats1Down"),
        ("_CMS_ttH_CSVhfstats2Up", "_CMS_ttH_CSVhfstats2Down"),
        ("_CMS_ttH_CSVjesUp", "_CMS_ttH_CSVjesDown"),
        ("_CMS_ttH_CSVlfUp", "_CMS_ttH_CSVlfDown"),
        ("_CMS_ttH_CSVlfstats1Up", "_CMS_ttH_CSVlfstats1Down"),
        ("_CMS_ttH_CSVlfstats2Up", "_CMS_ttH_CSVlfstats2Down")
    ])

#optional function f: TH1D -> TH1D to blind data
def blind(h):
    hc = h.Clone()
    for i in range(h.GetNbinsX()+1):
        hc.SetBinContent(i, 0)
        hc.SetBinError(i, 0)
    return hc

def plot_syst_updown(nominal, up, down):
    plt.figure(figsize=(6,6))
    heplot.barhist(nominal, color="black")
    heplot.barhist(up, color="red")
    heplot.barhist(down, color="blue")

def plot_worker(kwargs):
    inf = rootpy.io.File(kwargs.pop("infile"))
    outname = kwargs.pop("outname")
    histname = kwargs.pop("histname")
    procs = kwargs.pop("procs")
    signal_procs = kwargs.pop("signal_procs")
    do_syst = kwargs.pop("do_syst")

    fig = plt.figure(figsize=(6,6))
    ret = plotlib.draw_data_mc(
        inf,
        histname,
        procs,
        signal_procs,
        **kwargs
    )
    logging.info("saving {0}".format(outname))
    path = os.path.dirname(outname)
    if not os.path.isdir(path):
        os.makedirs(path)
    plotlib.svfg(outname + ".pdf")
    plt.clf()

    if do_syst:
        for samp, sampname in procs:
            hnom = ret["nominal"][samp]
            for systUp, systDown in kwargs["systematics"]:
                syst_name = systUp[1:-2]
                path_with_syst = os.path.join(path, os.path.basename(outname), syst_name)
                hup = ret["systematic"][systUp][samp]
                hdown = ret["systematic"][systDown][samp]
                plot_syst_updown(hnom, hup, hdown)
                if not os.path.isdir(path_with_syst):
                    os.makedirs(path_with_syst)
                outname_syst = os.path.join(path_with_syst, samp)
                logging.info("saving systematic {0}".format(outname_syst))
                plotlib.svfg(outname_syst)
                plt.clf()

    inf.Close()


def get_base_plot(basepath, outpath, analysis, category, variable):
    s = "{0}/{1}/{2}".format(basepath, analysis, category)
    return {
        "infile": s + ".root",
        "histname": "/".join([category, variable]),
        "outname": "/".join(["out", outpath, analysis, category, variable]),
        "procs": procs_names,
        "signal_procs": ["ttH_hbb"],
        "dataname": "data", #data_obs for fake data
        "rebin": 1,
        "xlabel": plotlib.varnames[variable] if variable in plotlib.varnames.keys() else "PLZ add me to Varnames", 
        "xunit": plotlib.varunits[variable] if variable in plotlib.varunits.keys() else "" ,
        "legend_fontsize": 12,
        "legend_loc": "best",
        "colors": [plotlib.colors.get(p) for p in procs],
        "do_legend": True,
        "show_overflow": True,
        "title_extended": r"$,\ \mathcal{L}=00.0\ \mathrm{fb}^{-1}$, ",
        "systematics": syst_pairs,
        "do_syst": True,
        #"blindFunc": blind,
    }

if __name__ == "__main__":


    # Plot for all SL categories
    sl_vars = ["jetsByPt_0_pt", 
               "jetsByPt_1_pt", 
               "jetsByPt_2_pt", 
               "jetsByPt_0_btagCSV", 
               "jetsByPt_0_eta", 
               "jetsByPt_1_eta", 
               "jetsByPt_2_eta", 
               "fatjetByPt_0_pt",  
               "fatjetByPt_0_eta",  
               "fatjetByPt_0_mass",
               "leps_0_pt",  
               "leps_0_eta",  
               "numJets",  
               "nBCSVM",  
               "btag_LR_4b_2b_btagCSV_logit"]

    # Plot for all DL categories
    dl_vars = ["jetsByPt_0_pt", "leps_0_pt"]

    # Top Tagging variables
    top_vars = ["topCandidate_fRec",
                "topCandidate_pt",
                "topCandidate_ptcal",
                "topCandidate_mass",
                "topCandidate_masscal",
                "topCandidate_n_subjettiness",
            ]

    # Higgs tagging variables
    higgs_vars = [
        "higgsCandidate_secondbtag_subjetfiltered", 
        "higgsCandidate_bbtag", 
        "higgsCandidate_tau1", 
        "higgsCandidate_tau2", 
        "higgsCandidate_mass", 
        "higgsCandidate_mass_softdropz2b1filt", 
        "higgsCandidate_sj12massb_subjetfiltered", 
        "higgsCandidate_sj12masspt_subjetfiltered",             
    ]

    # Event classification variables
    class_vars = ["multiclass_class",
                  "multiclass_proba_ttb",
                  "multiclass_proba_tt2b",
                  "multiclass_proba_ttbb",
                  "multiclass_proba_ttcc",
                  "multiclass_proba_ttll"
    ]

    cats_sl = [
        "sl_j4_t3", "sl_j4_tge4",
        "sl_j5_t3", "sl_j5_tge4",
        "sl_jge6_t2", "sl_jge6_t3", "sl_jge6_tge4",
    ]

    cats_dl = [
        "dl_j3_t2",
        "dl_j3_t3",
        "dl_jge4_t2",
        "dl_jge4_t3",
        "dl_jge4_tge4",
    ]
    
    version = "GC70f0703561df"

    args = []

    args += [get_base_plot(
            "/mnt/t3nfs01/data01/shome/gregor/tth/gc/makecategory/"+version,
            "Aug12", "SL_7cat", cat, var) for cat in cats_sl for var in sl_vars]

    args += [get_base_plot(
            "/mnt/t3nfs01/data01/shome/gregor/tth/gc/makecategory/"+version,
            "Aug12", "DL", cat, var) for cat in cats_dl for var in dl_vars]

    args += [get_base_plot(
            "/mnt/t3nfs01/data01/shome/gregor/tth/gc/makecategory/"+version,
            "Aug12", "SL_7cat", cat, var) for cat in  ["sl_j4_t3"] for var in higgs_vars + top_vars]

    args += [get_base_plot(
            "/mnt/t3nfs01/data01/shome/gregor/tth/gc/makecategory/"+version,
            "Aug12", "SL_7cat", cat, var) for cat in ["sl_jge6_tge4"] for var in class_vars]
    

    if DO_PARALLEL:
        import multiprocessing
        pool = multiprocessing.Pool(4)
        pool.map(plot_worker, args)
        pool.close()
    else:
        for arg in args:
            plot_worker(arg)

