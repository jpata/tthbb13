import TTH.Plotting.Helpers.CompareDistributionsHelpers as compare_utils
from TTH.Plotting.Helpers.CompareDistributionsHelpers import combinedPlot, plot
from TTH.MEAnalysis.samples_base import getSitePrefix
from TTH.MEAnalysis.samples import samples
from TTH.Plotting.Datacards.sparse import save_hdict
import os

import ROOT
ROOT.TH1.SetDefaultSumw2(True)

DATASETPATH = os.environ["DATASETPATH"]
sample = DATASETPATH.split("__")[1]
FILE_NAMES = os.environ["FILE_NAMES"].split()
samp = samples[sample]

combinedPlot(
    "numJets",
    [
        plot("sl", "numJets", "is_sl", "sample"),
        plot("dl", "numJets", "is_dl", "sample"),
    ] + [
        plot("sl_JESUp", "numJets_JESUp", "is_sl", "sample"),
        plot("sl_JESDown", "numJets_JESDown", "is_sl", "sample"),
        plot("sl_JERUp", "numJets_JERUp", "is_sl", "sample"),
        plot("sl_JERDown", "numJets_JERDown", "is_sl", "sample"),
        plot("dl_JESUp", "numJets_JESUp", "is_dl", "sample"),
        plot("dl_JESDown", "numJets_JESDown", "is_dl", "sample"),
        plot("dl_JERUp", "numJets_JERUp", "is_dl", "sample"),
        plot("dl_JERDown", "numJets_JERDown", "is_dl", "sample"),
    ] if samp["isMC"] else [],
    10,
    0,
    10,
)

combinedPlot(
    "nBCSVM",
    [
        plot("sl", "nBCSVM", "is_sl", "sample"),
        plot("dl", "nBCSVM", "is_dl", "sample"),
        plot("sl_j4", "nBCSVM", "is_sl && numJets==4", "sample"),
        plot("sl_j5", "nBCSVM", "is_sl && numJets==5", "sample"),
        plot("sl_jge6", "nBCSVM", "is_sl && numJets>=6", "sample"),
        plot("dl_j3", "nBCSVM", "is_sl && numJets==3", "sample"),
        plot("dl_jge4", "nBCSVM", "is_sl && numJets>=4", "sample"),
    ] + [
        plot("sl_JESUp", "nBCSVM_JESUp", "is_sl", "sample"),
        plot("sl_JESDown", "nBCSVM_JESDown", "is_sl", "sample"),
        plot("sl_JERUp", "nBCSVM_JERUp", "is_sl", "sample"),
        plot("sl_JERDown", "nBCSVM_JERDown", "is_sl", "sample"),
        plot("dl_JESUp", "nBCSVM_JESUp", "is_dl", "sample"),
        plot("dl_JESDown", "nBCSVM_JESDown", "is_dl", "sample"),
        plot("dl_JERUp", "nBCSVM_JERUp", "is_dl", "sample"),
        plot("dl_JERDown", "nBCSVM_JERDown", "is_dl", "sample"),
    ] if samp["isMC"] else [],
    10,
    0,
    10,
)

combinedPlot(
    "jets_pt_0",
    [
        plot("sl", "jets_pt[0]", "is_sl", "sample"),
    ] + ([
        plot("sl_JESUp", "jets_pt[0]*jets_corr_JESUp[0]/jets_corr[0]", "is_sl", "sample"),
        plot("sl_JESDown", "jets_pt[0]*jets_corr_JESDown[0]/jets_corr[0]", "is_sl", "sample"),
        plot("sl_bTagWeight", "jets_pt[0]", "bTagWeight * is_sl", "sample"),
        plot("sl_allWeight", "jets_pt[0]", "bTagWeight * puWeight * is_sl", "sample"),
    ] + [
        plot("sl_bTagWeight_{0}".format(bw), "jets_pt[0]", "bTagWeight_{0} * is_sl".format(bw), "sample") for
        bw in [a+b for a in ["HF", "JES", "LF", "cErr1", "cErr2", "HFStats1", "HFStats2", "LFStats1", "LFStats2"] for b in ["Up", "Down"]] 
    ]) if samp["isMC"] else [],
    100,
    0,
    400,
)

combinedPlot(
    "jets_eta_0",
    [
        plot("sl", "jets_eta[0]", "is_sl", "sample"),
    ] + ([
        plot("sl_JESUp", "jets_eta[0]*jets_corr_JESUp[0]/jets_corr[0]", "is_sl", "sample"),
        plot("sl_JESDown", "jets_eta[0]*jets_corr_JESDown[0]/jets_corr[0]", "is_sl", "sample"),
        plot("sl_bTagWeight", "jets_eta[0]", "bTagWeight * is_sl", "sample"),
        plot("sl_allWeight", "jets_eta[0]", "bTagWeight * puWeight * is_sl", "sample"),
    ] + [
        plot("sl_bTagWeight_{0}".format(bw), "jets_eta[0]", "bTagWeight_{0} * is_sl".format(bw), "sample") for
        bw in [a+b for a in ["HF", "JES", "LF", "cErr1", "cErr2", "HFStats1", "HFStats2", "LFStats1", "LFStats2"] for b in ["Up", "Down"]] 
    ]) if samp["isMC"] else [],
    100,
    -5,
    5,
)

combinedPlot(
    "leps_pt_0",
    [
        plot("sl", "leps_pt[0]", "is_sl", "sample"),
        plot("dl", "leps_pt[0]", "is_dl", "sample"),
    ],
    100,
    0,
    300,
)

combinedPlot(
    "leps_pdgId_0",
    [
        plot("sl", "leps_pdgId[0]", "is_sl", "sample"),
        plot("dl", "leps_pdgId[0]", "is_dl", "sample"),
    ],
    30,
    -15,
    15,
)

combinedPlot(
    "leps_pt_1",
    [
        plot("dl", "leps_pt[1]", "is_dl", "sample"),
    ],
    100,
    0,
    300,
)

combinedPlot(
    "jets_btagCSV",
    [
        plot("sl_all", "jets_btagCSV", "is_sl", "sample"),
        plot("sl_b", "jets_btagCSV", "is_sl && abs(jets_hadronFlavour)==5", "sample"),
        plot("sl_c", "jets_btagCSV", "is_sl && abs(jets_hadronFlavour)==4", "sample"),
        plot("sl_l", "jets_btagCSV", "is_sl && abs(jets_hadronFlavour)!=5 && abs(jets_hadronFlavour)!=4", "sample"),
    ] + [
        plot("sl_bTagWeight_{0}".format(bw), "jets_btagCSV", "bTagWeight_{0} * is_sl".format(bw), "sample") for
        bw in [a+b for a in ["HF", "JES", "LF", "cErr1", "cErr2", "HFStats1", "HFStats2", "LFStats1", "LFStats2"] for b in ["Up", "Down"]] 
    ] if samp["isMC"] else [],
    100,
    0,
    1,
)

combinedPlot(
    "jets_btagCMVA",
    [
        plot("sl_all", "jets_btagCMVA", "is_sl", "sample"),
        plot("sl_b", "jets_btagCMVA", "is_sl && abs(jets_hadronFlavour)==5", "sample"),
        plot("sl_c", "jets_btagCMVA", "is_sl && abs(jets_hadronFlavour)==4", "sample"),
        plot("sl_l", "jets_btagCMVA", "is_sl && abs(jets_hadronFlavour)!=5 && abs(jets_hadronFlavour)!=4", "sample"),
    ] + [
        plot("sl_bTagWeight_{0}".format(bw), "jets_btagCMVA", "bTagWeight_{0} * is_sl".format(bw), "sample") for
        bw in [a+b for a in ["HF", "JES", "LF", "cErr1", "cErr2", "HFStats1", "HFStats2", "LFStats1", "LFStats2"] for b in ["Up", "Down"]] 
    ] if samp["isMC"] else [],
    100,
    -1,
    1,
)

combinedPlot(
    "btag_LR_4b_2b_btagCSV",
    [
        plot("sl_jge4", "btag_LR_4b_2b_btagCSV", "is_sl && numJets>=4", "sample"),
        plot("dl_jge4", "btag_LR_4b_2b_btagCSV", "is_dl && numJets>=4", "sample"),
    ],
    100,
    0,
    1,
)

combinedPlot(
    "btag_LR_4b_2b_btagCMVA",
    [
        plot("sl_jge4", "btag_LR_4b_2b_btagCMVA", "is_sl && numJets>=4", "sample"),
        plot("dl_jge4", "btag_LR_4b_2b_btagCMVA", "is_dl && numJets>=4", "sample"),
    ],
    100,
    0,
    1,
)

files = {"sample": (map(getSitePrefix, FILE_NAMES), "tree")}

ret = compare_utils.createHistograms(
    files
)

ret2 = {}
for (k,v) in ret.items():
    ret2[sample + "/" + k] = v

save_hdict(
    "out.root",
    ret2
)

