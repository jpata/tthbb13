import TTH.Plotting.Helpers.CompareDistributionsHelpers as compare_utils
from TTH.Plotting.Helpers.CompareDistributionsHelpers import combinedPlot, plot
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.Plotting.Datacards.sparse import save_hdict
import os, sys

import TTH.MEAnalysis.MEAnalysis_cfg_heppy as cfg

import ROOT
ROOT.TH1.SetDefaultSumw2(True)

btag_weights_suff = [
    b+"_"+a for a in ["cferr1", "cferr2", "hf", "hfstats1", "hfstats2", "jes", "lf", "lfstats1", "lfstats2"] for b in ["up", "down"]
]

btag_weights_csv = ["btagWeightCSV_" + suff for suff in btag_weights_suff]
btag_weights_cmva = ["btagWeightCMVAV2_" + suff for suff in btag_weights_suff]

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Prepares dataset lists from DAS')
    parser.add_argument('--cfg', action="store", help="path to analysis configuration", required=True)
    args = parser.parse_args()

    an_name, analysis = analysisFromConfig(args.cfg)

    DATASETPATH = os.environ["DATASETPATH"]
    prefix, sample_name = get_prefix_sample(DATASETPATH)
    FILE_NAMES = os.environ["FILE_NAMES"].split()
    
    sample = analysis.get_sample(sample_name)

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
        ] if not sample.is_data else [],
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
        ] if not sample.is_data else [],
        10,
        0,
        10,
    )

    combinedPlot(
        "nBCMVAM",
        [
            plot("sl", "nBCMVAM", "is_sl", "sample"),
            plot("dl", "nBCMVAM", "is_dl", "sample"),
            plot("sl_j4", "nBCMVAM", "is_sl && numJets==4", "sample"),
            plot("sl_j5", "nBCMVAM", "is_sl && numJets==5", "sample"),
            plot("sl_jge6", "nBCMVAM", "is_sl && numJets>=6", "sample"),
            plot("dl_j3", "nBCMVAM", "is_sl && numJets==3", "sample"),
            plot("dl_jge4", "nBCMVAM", "is_sl && numJets>=4", "sample"),
        ] + [
            plot("sl_JESUp", "nBCMVAM_JESUp", "is_sl", "sample"),
            plot("sl_JESDown", "nBCMVAM_JESDown", "is_sl", "sample"),
            plot("sl_JERUp", "nBCMVAM_JERUp", "is_sl", "sample"),
            plot("sl_JERDown", "nBCMVAM_JERDown", "is_sl", "sample"),
            plot("dl_JESUp", "nBCMVAM_JESUp", "is_dl", "sample"),
            plot("dl_JESDown", "nBCMVAM_JESDown", "is_dl", "sample"),
            plot("dl_JERUp", "nBCMVAM_JERUp", "is_dl", "sample"),
            plot("dl_JERDown", "nBCMVAM_JERDown", "is_dl", "sample"),
        ] if not sample.is_data else [],
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
            plot("sl_bTagWeightCSV", "jets_pt[0]", "btagWeightCSV * is_sl", "sample"),
            plot("sl_allWeightCSV", "jets_pt[0]", "btagWeightCSV * puWeight * is_sl", "sample"),
        ] + [
            plot("sl_bTagWeightCSV_{0}".format(bw), "jets_pt[0]", "{0} * is_sl".format(bw), "sample") for
            bw in btag_weights_csv
        ]) if not sample.is_data else [],
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
            plot("sl_bTagWeightCSV", "jets_eta[0]", "btagWeightCSV * is_sl", "sample"),
            plot("sl_allWeightCSV", "jets_eta[0]", "btagWeightCSV * puWeight * is_sl", "sample"),
        ] + [
            plot("sl_bTagWeightCSV_{0}".format(bw), "jets_eta[0]", "{0} * is_sl".format(bw), "sample") for
            bw in btag_weights_csv
        ]) if not sample.is_data else [],
        100,
        -5,
        5,
    )

    combinedPlot(
        "leps_pt_0",
        [
            plot("sl", "leps_pt[0]", "is_sl", "sample"),
            plot("dl", "leps_pt[0]", "is_dl", "sample"),
        ] + [
            plot("sl_triggerWeight", "leps_pt[0]", "triggerEmulationWeight * (is_sl)", "sample"),
            plot("dl_triggerWeight", "leps_pt[0]", "triggerEmulationWeight * (is_dl)", "sample"),
        ] if sample.schema == "mc" else [],
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
            plot("sl_all", "jets_btagCSV", "btagWeightCSV * (is_sl)", "sample"),
            plot("sl_b", "jets_btagCSV", "btagWeightCSV * (is_sl && abs(jets_hadronFlavour) == 5)", "sample"),
            plot("sl_c", "jets_btagCSV", "btagWeightCSV * (is_sl && abs(jets_hadronFlavour) == 4)", "sample"),
            plot("sl_l", "jets_btagCSV", "btagWeightCSV * (is_sl && abs(jets_hadronFlavour) != 5 && abs(jets_hadronFlavour) != 4)", "sample"),
        ] + [
            plot("sl_bTagWeightCSV_{0}".format(bw), "jets_btagCSV", "{0} * (is_sl)".format(bw), "sample") for
            bw in btag_weights_csv 
        ] if not sample.is_data else [],
        100,
        0,
        1,
    )

    combinedPlot(
        "jets_btagCMVA",
        [
            plot("sl_all", "jets_btagCMVA", "btagWeightCMVAV2 * (is_sl)", "sample"),
            plot("sl_b", "jets_btagCMVA", "btagWeightCMVAV2 * (is_sl && abs(jets_hadronFlavour) == 5)", "sample"),
            plot("sl_c", "jets_btagCMVA", "btagWeightCMVAV2 * (is_sl && abs(jets_hadronFlavour) == 4)", "sample"),
            plot("sl_l", "jets_btagCMVA", "btagWeightCMVAV2 * (is_sl && abs(jets_hadronFlavour) != 5 && abs(jets_hadronFlavour) != 4)", "sample"),
        ] + [
            plot("sl_bTagWeightCMVA_{0}".format(bw), "jets_btagCMVA", "{0} * is_sl".format(bw), "sample") for
            bw in btag_weights_cmva
        ] if not sample.is_data else [],
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
    
    combinedPlot(
        "mem",
        [
            plot("sl_jge6_tge4", "mem_tth_SL_2w2h2t_p / (mem_tth_SL_2w2h2t_p + 0.1 * mem_ttbb_SL_2w2h2t_p)", "is_sl && numJets>=6 && nBCSVM>=4", "sample"),
            plot("sl_jge6_t3", "mem_tth_SL_2w2h2t_p / (mem_tth_SL_2w2h2t_p + 0.1 * mem_ttbb_SL_2w2h2t_p)", "is_sl && numJets>=6 && nBCSVM==3 && log(btag_LR_4b_2b_btagCSV/(1.0 - btag_LR_4b_2b_btagCSV))>{0}".format(cfg.Conf.mem["blr_cuts"]["sl_jge6_t3"]), "sample"),
            plot("sl_j5_tge4", "mem_tth_SL_1w2h2t_p / (mem_tth_SL_1w2h2t_p + 0.1 * mem_ttbb_SL_1w2h2t_p)", "is_sl && numJets==5 && nBCSVM>=4", "sample"),
            plot("sl_j5_t3", "mem_tth_SL_1w2h2t_p / (mem_tth_SL_1w2h2t_p + 0.1 * mem_ttbb_SL_1w2h2t_p)", "is_sl && numJets==5 && nBCSVM==3 && log(btag_LR_4b_2b_btagCSV/(1.0 - btag_LR_4b_2b_btagCSV))>{0}".format(cfg.Conf.mem["blr_cuts"]["sl_j5_t3"]), "sample"),
            plot("sl_j4_tge4", "mem_tth_SL_0w2h2t_p / (mem_tth_SL_0w2h2t_p + 0.1 * mem_ttbb_SL_0w2h2t_p)", "is_sl && numJets==4 && nBCSVM>=4", "sample"),
            plot("sl_j4_t3", "mem_tth_SL_0w2h2t_p / (mem_tth_SL_0w2h2t_p + 0.1 * mem_ttbb_SL_0w2h2t_p)", "is_sl && numJets==4 && nBCSVM==3 && log(btag_LR_4b_2b_btagCSV/(1.0 - btag_LR_4b_2b_btagCSV))>{0}".format(cfg.Conf.mem["blr_cuts"]["sl_j4_t3"]), "sample"),
            plot("dl_jge4_tge4", "mem_tth_DL_0w2h2t_p / (mem_tth_DL_0w2h2t_p + 0.1 * mem_ttbb_DL_0w2h2t_p)", "is_dl && numJets>=4 && nBCSVM>=4", "sample"),
            plot("dl_jge4_t3", "mem_tth_DL_0w2h2t_p / (mem_tth_DL_0w2h2t_p + 0.1 * mem_ttbb_DL_0w2h2t_p)", "is_dl && numJets>=4 && nBCSVM==3 && log(btag_LR_4b_2b_btagCSV/(1.0 - btag_LR_4b_2b_btagCSV))>{0}".format(cfg.Conf.mem["blr_cuts"]["dl_jge4_t3"]), "sample"),
        ],
        6,
        0,
        1,
    )

    files = {
        "sample": (map(getSitePrefix, FILE_NAMES), "tree")
    }
    print "mapping over files", files

    ret = compare_utils.createHistograms(
        files
    )

    ret2 = {}
    for (k,v) in ret.items():
        ret2[sample_name + "/" + k] = v

    save_hdict(
        "out.root",
        ret2
    )

