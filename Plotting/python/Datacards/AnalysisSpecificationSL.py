from TTH.MEAnalysis.samples_base import xsec
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Sample, Category, Analysis, make_csv_categories_abstract, make_csv_groups_abstract
import copy
from copy import deepcopy

blr_cuts = {
    "sl_j4_t3": 1.1,
    "sl_j5_t3": 2.3,
    "sl_jge6_t3": 2.9,
}

input_file = "/mnt/t3nfs01/data01/shome/jpata/tth/gc/melooper/GCdf683f856c22/ControlPlots.root"

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
        xs_weight = 1.0
    ),
    Sample(
        input_name = "ttHToNonbb_M125_13TeV_powheg_pythia8/ttH_nonhbb",
        output_name = "ttH_nonhbb",
        xs_weight = 1.0
    ),
]

ttjets_powheg = [
    Sample(
        input_name = "TT_TuneEE5C_13TeV-powheg-herwigpp/{0}".format(tt),
        output_name = tt,
        xs_weight = 1.0
    ) for tt in ["ttbarOther", "ttbarPlusBBbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusCCbar"]
]

ttjets_split = [
    Sample(
        input_name = "{0}/{1}".format(sn, tt),
        output_name = tt,
        xs_weight = 1.0
    ) for sn in [
        "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        "TTTo2L2Nu_13TeV-powheg",
    ] for tt in ["ttbarOther", "ttbarPlusBBbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusCCbar"]
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
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_2w2h2t",
        src_histogram = "sl/sparse"
    ),
    
    # >= 6 jets, == 3 tags
    Category(
        name = "sl_jge6_t3",
        cuts = [("numJets", 6, 8), ("nBCSVM", 3, 4)],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_2w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    # >= 6 jets, == 3 tags, high blr
    Category(
        name = "sl_jge6_t3_blrH",
        cuts = [("numJets", 6, 8), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_logit", blr_cuts["sl_jge6_t3"], 20)],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_2w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    # >= 6 jets, == 3 tags, low blr
    Category(
        name = "sl_jge6_t3_blrL",
        cuts = [("numJets", 6, 8), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_logit", -20, blr_cuts["sl_jge6_t3"])],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_2w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    # >= 6 jets, == 2 tags
    Category(
        name = "sl_jge6_t2",
        cuts = [("numJets", 6, 8), ("nBCSVM", 2, 3)],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "btag_LR_4b_2b_logit",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    # == 5 jets, >= 4 tags
    Category(
        name = "sl_j5_tge4",
        cuts = [("numJets", 5, 6), ("nBCSVM", 4, 8)],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_1w2h2t",
        src_histogram = "sl/sparse"
    ),
    
    # == 5 jets, == 3 tags, high blr
    Category(
        name = "sl_j5_t3",
        cuts = [("numJets", 5, 6), ("nBCSVM", 3, 4)],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_1w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    Category(
        name = "sl_j5_t3_blrH",
        cuts = [("numJets", 5, 6), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_logit", blr_cuts["sl_j5_t3"], 20)],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_1w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    # == 5 jets, == 3 tags, low blr
    Category(
        name = "sl_j5_t3_blrL",
        cuts = [("numJets", 5, 6), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_logit", -20, blr_cuts["sl_j5_t3"])],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "btag_LR_4b_2b_logit",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    # == 4 jets, >= 4 tags
    Category(
        name = "sl_j4_tge4",
        cuts = [("numJets", 4, 5), ("nBCSVM", 4, 8)],
        samples = base_samples + ttjets_powheg,
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
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    # == 4 jets, == 3 tags
    Category(
        name = "sl_j4_t3_blrH",
        cuts = [("numJets", 4, 5), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_logit", blr_cuts["sl_j4_t3"], 20)],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_SL_0w2h2t",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    Category(
        name = "sl_j4_t3_blrL",
        cuts = [("numJets", 4, 5), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_logit", -20, blr_cuts["sl_j4_t3"])],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "btag_LR_4b_2b_logit",
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
    samples = base_samples + ttjets_powheg,
    categories = all_cats,
    sparse_input_file = input_file,
    groups = {
        "sl": sl_categories,
    },
    do_fake_data = do_fake_data,
    do_stat_variations = do_stat_variations
)


analysis_ttjets_split = Analysis(
    samples = base_samples + ttjets_split,
    categories = deepcopy(all_cats),
    sparse_input_file = input_file,
    groups = {
        "sl": sl_categories,
    },
    do_fake_data = do_fake_data,
    do_stat_variations = do_stat_variations
)
for icat in range(len(analysis_ttjets_split.categories)):
    analysis_ttjets_split.categories[icat].samples = base_samples + ttjets_split 

sl_categories_bdt = filter(lambda x: x.discriminator == "common_bdt", all_cats)

analysis_bdt = Analysis(
    samples = base_samples + ttjets_powheg,
    categories = sl_categories_bdt,
    sparse_input_file = input_file,
    groups = {
        "sl": sl_categories_bdt,
    },
    do_fake_data = do_fake_data,
    do_stat_variations = do_stat_variations
)

#add single-category groups
for cat in sl_categories:
    analysis.groups[cat.full_name] = [cat]
for cat in sl_categories_bdt:
    analysis_bdt.groups[cat.full_name] = [cat]

# Dictionary of all analyses we consider
analyses = {
    "SL" : analysis,
    "SL_ttjets_split" : analysis_ttjets_split,
    "SL_7cat_bdt" : analysis_bdt
}

def make_csv_categories():
    return make_csv_categories_abstract(analyses)

def make_csv_groups():
    return make_csv_groups_abstract(analyses)


