from TTH.MEAnalysis.samples_base import xsec
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Sample, Category, Analysis, make_csv_categories_abstract, make_csv_groups_abstract
import copy

#generated by running MEAnalysis/gc/confs/counts.conf
#and aggregating the results with MEAnalysis/python/getCounts.py
ngen = {
    'TTTo2L2Nu_13TeV-powheg': 107696544.0,
    'ttHTobb_M125_13TeV_powheg_pythia8': 2774714.0,
    'TT_TuneCUETP8M1_13TeV-powheg-pythia8': 95846240.0,
    'TTToSemiLeptonic_13TeV-powheg': 223888000.0,
    'ttHToNonbb_M125_13TeV_powheg_pythia8':3945824.0,
}

lumi = 2500 # pb-1
do_stat_variations = False
do_fake_data = True

common_shape_uncertainties = {
    "CMS_scale_j"           : 1,
    "CMS_ttH_CSVLF"         : 1,
    "CMS_ttH_CSVHF"         : 1,
    "CMS_ttH_CSVcErr1"      : 1,
    "CMS_ttH_CSVcErr2"      : 1,
    "CMS_ttH_CSVHFStats1"   : 1,
    "CMS_ttH_CSVHFStats2"   : 1,
    "CMS_ttH_CSVLFStats1"   : 1,
    "CMS_ttH_CSVLFStats2"   : 1,
}

common_scale_uncertainties = {
    "lumi" : 1.045
}

scale_uncertainties = {
    "ttH_hbb" : {
        "QCDscale_ttH" : 1.133,
        "pdf_gg" : 1.083,
    },
    "ttH_nonhbb" : {
    },
    "ttbarPlus2B" : {
        "bgnorm_ttbarPlus2B" : 1.5,
        "QCDscale_ttbar" : 1.030,
        "pdf_gg" : 1.026,
    },
    "ttbarPlusB" : {
        "bgnorm_ttbarPlusB" : 1.5,
        "QCDscale_ttbar" : 1.030,
        "pdf_gg" : 1.026,
    },
    "ttbarPlusBBbar" : {
        "bgnorm_ttbarPlusBBbar" : 1.5,
        "QCDscale_ttbar" : 1.030,
        "pdf_gg" : 1.026,
    },
    "ttbarPlusCCbar" : {
        "bgnorm_ttbarPlusCCbar" : 1.5,
        "QCDscale_ttbar" : 1.030,
        "pdf_gg" : 1.026,
    },
    "ttbarOther" : {
        "QCDscale_ttbar" : 1.030,
        "pdf_gg" : 1.026,
    }
}


signal_processes = ["ttH_hbb", "ttH_nonhbb"]

base_samples = [
    Sample(
        input_name = "ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb",
        output_name = "ttH_hbb",
        xs_weight = lumi * xsec[("tthbb", "13TeV")] / ngen["ttHTobb_M125_13TeV_powheg_pythia8"]
    ),
    Sample(
        input_name = "ttHToNonbb_M125_13TeV_powheg_pythia8/ttH_nonhbb",
        output_name = "ttH_nonhbb",
        xs_weight = lumi * xsec[("tth_nonhbb", "13TeV")] / ngen["ttHToNonbb_M125_13TeV_powheg_pythia8"]
    ),
    Sample(
        input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8/ttbarOther",
        output_name = "ttbarOther",
        xs_weight = lumi * xsec[("ttjets", "13TeV")] / ngen["TT_TuneCUETP8M1_13TeV-powheg-pythia8"]
    ),
    Sample(
        input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8/ttbarPlus2B",
        output_name = "ttbarPlus2B",
        xs_weight = lumi * xsec[("ttjets", "13TeV")] / ngen["TT_TuneCUETP8M1_13TeV-powheg-pythia8"]
    ),
    Sample(
        input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8/ttbarPlusB",
        output_name = "ttbarPlusB",
        xs_weight = lumi * xsec[("ttjets", "13TeV")] / ngen["TT_TuneCUETP8M1_13TeV-powheg-pythia8"]
    ),
    Sample(
        input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8/ttbarPlusBBbar",
        output_name = "ttbarPlusBBbar",
        xs_weight = lumi * xsec[("ttjets", "13TeV")] / ngen["TT_TuneCUETP8M1_13TeV-powheg-pythia8"]
    ),
    Sample(
        input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8/ttbarPlusCCbar",
        output_name = "ttbarPlusCCbar",
        xs_weight = lumi * xsec[("ttjets", "13TeV")] / ngen["TT_TuneCUETP8M1_13TeV-powheg-pythia8"]
    ),
]
data_samples = {
    "SingleMuon": Sample(
        input_name = "SingleMuon/SingleMuon",
        output_name = "data",
        xs_weight = 1.0,
        cuts = [("leptonFlavour", 1, 2)]
    ),
    "SingleElectron": Sample(
        input_name = "SingleElectron/SingleElectron",
        output_name = "data",
        xs_weight = 1.0,
        cuts = [("leptonFlavour", 2, 3)]
    ),

    "DoubleMuon": Sample(
        input_name = "DoubleMuon/DoubleMuon",
        output_name = "data",
        xs_weight = 1.0,
        cuts = [("leptonFlavour", 3, 4)]
    ),
    "MuonEG": Sample(
        input_name = "MuonEG/MuonEG",
        output_name = "data",
        xs_weight = 1.0,
        cuts = [("leptonFlavour", 4, 5)]
    ),
    "DoubleEG": Sample(
        input_name = "DoubleEG/DoubleEG",
        output_name = "data",
        xs_weight = 1.0,
        cuts = [("leptonFlavour", 5, 6)]
    ),

}

sl_data = [data_samples["SingleMuon"], data_samples["SingleElectron"]]

sl_categories = [
    # >= 6 jets, >= 4 tags
    Category(
        name = "sl_jge6_tge4",
        cuts = [("numJets", 6, 8), ("nBCSVM", 4, 8)],
        samples = base_samples,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        src_histogram = "sl/sparse"
    ),
    
    # >= 6 jets, == 3 tags
    Category(
        name = "sl_jge6_t3",
        cuts = [("numJets", 6, 8), ("nBCSVM", 3, 4)],
        samples = base_samples,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    # >= 6 jets, == 2 tags
    Category(
        name = "sl_jge6_t2",
        cuts = [("numJets", 6, 8), ("nBCSVM", 2, 3)],
        samples = base_samples,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    # == 5 jets, >= 4 tags
    Category(
        name = "sl_j5_tge4",
        cuts = [("numJets", 5, 6), ("nBCSVM", 4, 8)],
        samples = base_samples,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        src_histogram = "sl/sparse"
    ),
    
    # == 5 jets, == 3 tags
    Category(
        name = "sl_j5_t3",
        cuts = [("numJets", 5, 6), ("nBCSVM", 3, 4)],
        samples = base_samples,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    # == 4 jets, >= 4 tags
    Category(
        name = "sl_j4_tge4",
        cuts = [("numJets", 4, 5), ("nBCSVM", 4, 8)],
        samples = base_samples,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        src_histogram = "sl/sparse"
    ),
    
    # == 4 jets, == 3 tags
    Category(
        name = "sl_j4_t3",
        cuts = [("numJets", 4, 5), ("nBCSVM", 3, 4)],
        samples = base_samples,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
]

control_variables = ["jet0_pt", "btag_LR_4b_2b_logit"]
def make_control_categories(input_categories):
    all_cats = copy.deepcopy(input_categories)
    for discr in control_variables + ["common_bdt"]:
        for cat in input_categories:
            newcat_d = cat.__dict__
            newcat_d["discriminator"] = discr
            newcat_d["do_limit"] = False
            if discr == "common_bdt":
                newcat_d["do_limit"] = True
            newcat = Category(**newcat_d)
            all_cats += [newcat]
    return all_cats

all_cats = make_control_categories(sl_categories)
analysis = Analysis(
    samples = base_samples,
    categories = all_cats,
    #sparse_input_file = "root://t3se01.psi.ch///store/user/jpata/tth/histograms/April2016A/sparse_Apr5.root",
    sparse_input_file = "/home/joosep/public_html/tth/histograms/April2016A/sparse_Apr5.root",
    groups = {
        "sl": sl_categories,
    },
    do_fake_data = do_fake_data,
    do_stat_variations = do_stat_variations
)

#add single-category groups
for cat in sl_categories:
    analysis.groups[cat.full_name] = [cat]

# Dictionary of all analyses we consider
analyses = {
    "SL_7cat" : analysis
}

def make_csv_categories():
    return make_csv_categories_abstract(analyses)

def make_csv_groups():
    return make_csv_groups_abstract(analyses)


