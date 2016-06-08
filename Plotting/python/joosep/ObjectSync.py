import TTH.Plotting.Helpers.CompareDistributionsHelpers as compare_utils
from TTH.Plotting.Helpers.CompareDistributionsHelpers import combinedPlot, plot
from TTH.MEAnalysis.samples_base import getSitePrefix
from TTH.Plotting.Datacards.sparse import save_hdict
import os

import ROOT
ROOT.TH1.SetDefaultSumw2(True)

DATASETPATH = os.environ["DATASETPATH"]
FILE_NAMES = os.environ["FILE_NAMES"].split()

combinedPlot(
    "numJets",
    [
        plot("sl", "numJets", "is_sl", "sample"),
        plot("sl_JESUp", "numJets_JESUp", "is_sl", "sample"),
        plot("sl_JESDown", "numJets_JESDown", "is_sl", "sample"),
    ],
    10,
    0,
    10,
)

combinedPlot(
    "nBCSVM",
    [
        plot("sl", "nBCSVM", "is_sl", "sample"),
        plot("sl_JESUp", "nBCSVM_JESUp", "is_sl", "sample"),
        plot("sl_JESDown", "nBCSVM_JESDown", "is_sl", "sample"),
    ],
    10,
    0,
    10,
)

combinedPlot(
    "jets_pt_0",
    [
        plot("sl", "jets_pt[0]", "is_sl", "sample"),
        plot("sl_bTagWeight", "jets_pt[0]", "bTagWeight * is_sl", "sample"),
        plot("sl_allWeight", "jets_pt[0]", "bTagWeight * puWeight * is_sl", "sample"),
    ] + [
        plot("sl_bTagWeight_{0}".format(bw), "jets_pt[0]", "bTagWeight_{0} * is_sl".format(bw), "sample") for
        bw in [a+b for a in ["HF", "JES", "LF", "cErr1", "cErr2", "HFStats1", "HFStats2", "LFStats1", "LFStats2"] for b in ["Up", "Down"]] 
    ],
    100,
    0,
    400,
)

combinedPlot(
    "jets_eta_0",
    [
        plot("sl_j4", "jets_eta[0]", "is_sl", "sample"),
    ],
    100,
    -5,
    5,
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
    ],
    100,
    0,
    1,
)

#combinedPlot(
#    "jets_btagCMVA",
#    [
#        plot("sl_all", "jets_btagCMVA", "is_sl", "sample"),
#        plot("sl_b", "jets_btagCMVA", "is_sl && abs(jets_hadronFlavour)==5", "sample"),
#        plot("sl_c", "jets_btagCMVA", "is_sl && abs(jets_hadronFlavour)==4", "sample"),
#        plot("sl_l", "jets_btagCMVA", "is_sl && abs(jets_hadronFlavour)!=5 && abs(jets_hadronFlavour)!=4", "sample"),
#    ] + [
#        plot("sl_bTagWeight_{0}".format(bw), "jets_btagCMVA", "bTagWeight_{0} * is_sl".format(bw), "sample") for
#        bw in [a+b for a in ["HF", "JES", "LF", "cErr1", "cErr2", "HFStats1", "HFStats2", "LFStats1", "LFStats2"] for b in ["Up", "Down"]] 
#    ],
#    100,
#    -1,
#    1,
#)

files = {"sample": (map(getSitePrefix, FILE_NAMES), "tree")}

ret = compare_utils.createHistograms(
    files
)

ret2 = {}
for (k,v) in ret.items():
    ret2[DATASETPATH + "/" + k] = v

save_hdict(
    "out.root",
    ret2
)

