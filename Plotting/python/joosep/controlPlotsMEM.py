import sys
import rootpy
import numpy as np
import matplotlib.pyplot as plt
import pandas
import rootpy.plotting.root2matplotlib as rplt
sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_15/src/TTH/Plotting/python/joosep/")
sys.path.append("/Users/joosep/Documents/heplot/")
import ROOT, plotlib, heplot

inf = rootpy.io.File("/Users/joosep/Dropbox/tth/ControlPlotsMEM.root")
def dataname(channel):
    if "sl" in channel:
        if "el" in channel:
            return "SingleElectron"
        elif "mu" in channel:
            return "SingleMuon"
    elif "dl" in channel:
        return "Dilepton"

for channel in [
    #"sl_mu",
    
    #"sl_jge4_mu",
    "sl_j4_t3_mu",
    #"sl_j4_t4_mu",
    
    "sl_j5_t3_mu",
    #"sl_j5_tge4_mu",
    
    #"sl_jge6_mu",
    "sl_jge6_t2_mu",
    "sl_jge6_t3_mu",
    "sl_jge6_tge4_mu",

    #"sl_el",
    
    #"sl_jge4_el",
    "sl_j4_t3_el",
    #"sl_j4_t4_el",
    
    "sl_j5_t3_el",
    #"sl_j5_tge4_el",
    
    #"sl_jge6_el",
    "sl_jge6_t2_el",
    "sl_jge6_t3_el",
    "sl_jge6_tge4_el"

    ]:
    for var in [
        #"njets",
        #"ntags",
        "lep0_pt",
        #"lep0_eta",
        "jet0_pt",
        #"jet1_pt",
        "jet0_eta",
        #"jet1_eta",
        "btag_LR_4b_2b_logit",
        "jet0_btagCSV",
        "jet0_btagBDT",
        #"nfatjets",
        #"fatjets_pt",
        #"fatjets_eta",
        #"jet1_btagCSV",
        "topCandidate_pt",
        "topCandidate_mass",
        "topCandidate_fRec",
        "topCandidate_Ropt",
        "topCandidate_RoptCalc",
        "topCandidate_n_subjettiness",
        "higgsCandidate_pt",
        "higgsCandidate_mass",
        "higgsCandidate_mass_pruned",
        #"higgsCandidate_mass_softdrop",
        "higgsCandidate_bbtag",
        "higgsCandidate_n_subjettiness",
        "higgsCandidate_dr_top"
        #"lep0_pt", "lep1_pt"
        ]:
        
        r = plotlib.draw_data_mc(
            inf,
            channel + "/" + var,
            plotlib.samplelist,
            dataname=["SingleElectron", "SingleMuon"], xlabel=plotlib.varnames[var], xunit=plotlib.varunits.get(var, "bin"),
            legend_fontsize=6, legend_loc="best", colors=plotlib.samplecolors,
            show_overflow = True,
            title_extended="\n$\\mathcal{L}=1.28\\ \\mathrm{fb}^{-1}$"
        )
        if var in ["njets", "ntags"] or "btag" in var:
            r[0].set_yscale("log")
            r[0].set_ylim(bottom=1)
        plotlib.svfg(channel + "_" + var + ".png", dpi=400)


for channel in [
    "dl_j3_t2",
    "dl_jge3_t3",
    "dl_jge4_t2",
    "dl_jge4_tge4"
    ]:
    for var in [
        "lep0_pt", "lep1_pt",
        #"lep0_eta", "lep1_eta",
        "jet0_pt", "jet1_pt",
        "jet0_eta", "jet1_eta",
        "btag_LR_4b_2b_logit",
        "jet0_btagCSV",
        "jet0_btagBDT",
        #"lep0_pt", "lep1_pt"
        ]:
        
        r = plotlib.draw_data_mc(
            inf,
            channel + "/" + var,
            plotlib.samplelist,
            dataname=["DoubleMuon", "DoubleEG", "MuonEG"], xlabel=plotlib.varnames[var], xunit=plotlib.varunits.get(var, "bin"),
            legend_fontsize=6, legend_loc="best", colors=plotlib.samplecolors,
            show_overflow = True,
            title_extended="\n$\\mathcal{L}=1.28\\ \\mathrm{fb}^{-1}$"
        )
        if "btag" in var:
            r[0].set_yscale("log")
            r[0].set_ylim(bottom=1)
        plotlib.svfg(channel + "_" + var + ".png", dpi=400)
