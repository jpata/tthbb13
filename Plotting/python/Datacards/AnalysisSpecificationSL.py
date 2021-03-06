from TTH.MEAnalysis.samples_base import xsec
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Sample, DataSample, Category, Analysis, make_csv_categories_abstract, make_csv_groups_abstract
from TTH.Plotting.joosep.sparsinator import PROCESS_MAP, TRIGGERPATH_MAP
from TTH.MEAnalysis import samples_base
from TTH.MEAnalysis.inputs import sparse_data

import copy
from copy import deepcopy

input_file = sparse_data["Aug11"].infile
ngen = sparse_data["Aug11"].ngen
lumi = sparse_data["Aug11"].lumi
blr_cuts = sparse_data["Aug11"].blr_cuts

do_stat_variations = False
do_fake_data = True

#Here we define all the shape uncertainties. For inputs, we expect input histograms
# like {process}/{channel}/{input}_{systematic}
# where process={ttH_hbb,...}, channel={sl,dl,...}, input={sparse}
common_shape_uncertainties = {
    "CMS_scale_j"          : 1,
    "CMS_res_j"            : 1,
    "pu"                   : 1,
    "CMS_ttH_CSVcferr1"       : 1,
    "CMS_ttH_CSVcferr2"       : 1,
    "CMS_ttH_CSVhf"           : 1,
    "CMS_ttH_CSVhfstats1"     : 1,
    "CMS_ttH_CSVhfstats2"     : 1,
    "CMS_ttH_CSVjes"          : 1,
    "CMS_ttH_CSVlf"           : 1,
    "CMS_ttH_CSVlfstats1"     : 1,
    "CMS_ttH_CSVlfstats2"     : 1,
}

common_scale_uncertainties = {
    "lumi" : 1.045
}

scale_uncertainties = {
    "ttH_hbb" : {
        "QCDscale_ttH" : 1.133,
        "pdf_gg" : 1.083,
    },
    #"ttH_nonhbb" : {
    #  # "QCDscale_ttH" : 1.133,
    #  # "pdf_gg" : 1.083,
    #},
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

#Here we define the signal processes, which will be fed into combine using special
#flags
signal_processes = ["ttH_hbb", "ttH_nonhbb"]

base_samples = [
    Sample(
        input_name = "ttHTobb_M125_13TeV_powheg_pythia8",
        output_name = "ttH_hbb",
        xs_weight = samples_base.xsec_sample["ttHTobb_M125_13TeV_powheg_pythia8"]/ngen["ttHTobb_M125_13TeV_powheg_pythia8"]
    ),
    Sample(
        input_name = "ttHToNonbb_M125_13TeV_powheg_pythia8",
        output_name = "ttH_nonhbb",
        xs_weight = samples_base.xsec_sample["ttHToNonbb_M125_13TeV_powheg_pythia8"]/ngen["ttHToNonbb_M125_13TeV_powheg_pythia8"]
    ),
]

def splitByTriggerPath(samples):
    """
    Given a list of samples, add a cut on a trigger path (SLmu, SLele etc)
    and normalize to the given luminosity.
    """
    out = []
    _lumis = {
        "m": lumi["SingleMuon"],
        "e": lumi["SingleElectron"],
        "mm": lumi["DoubleMuon"],
        "em": lumi["MuonEG"],
        "ee": lumi["DoubleEG"],
        "fh": lumi["BTagCSV"],
    }

    for name, trigpath in TRIGGERPATH_MAP.items():
        for samp in samples:
            newsamp = Sample(
                input_name = samp.input_name,
                output_name = samp.output_name,
                xs_weight = _lumis[name] * samp.xs_weight,
                cuts = samp.cuts + [("triggerPath", trigpath, trigpath+1)]
            )
            out += [newsamp]
    return out

#For tt+jets, we need to apply the selection that splits the sample into
#different tt+jets categories (ttbarPlusBBbar, ttbarPlusCCbar etc)
def processCut(proc):
    n = PROCESS_MAP[proc]
    return ("process", n, n+1)

ttjets_powheg = [
    Sample(
        input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8",
        output_name = tt,
        xs_weight = samples_base.xsec_sample["TT_TuneCUETP8M1_13TeV-powheg-pythia8"]/ngen["TT_TuneCUETP8M1_13TeV-powheg-pythia8"],
        cuts = [processCut(tt)]
    ) for tt in [
        "ttbarOther", "ttbarPlusBBbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusCCbar"
    ]
]

ttjets_split = [
    Sample(
        input_name = "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        output_name = tt,
        xs_weight = samples_base.xsec_sample["TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]/ngen["TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"],
        cuts = [processCut(tt)]
    ) for tt in [
        "ttbarOther", "ttbarPlusBBbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusCCbar"
    ]
]

ttjets_split += [
    Sample(
        input_name = "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        output_name = tt,
        xs_weight = samples_base.xsec_sample["TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]/ngen["TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"],
        cuts = [processCut(tt)]
    ) for tt in [
        "ttbarOther", "ttbarPlusBBbar", "ttbarPlus2B", "ttbarPlusB", "ttbarPlusCCbar"
    ]
]

#Need to normalize each trigger path with the corresponding luminosity
base_samples = splitByTriggerPath(base_samples)
ttjets_split = splitByTriggerPath(ttjets_split)
ttjets_powheg = splitByTriggerPath(ttjets_powheg)

# On the data samples, we only need to choose the events that pass the correct
# trigger path, e.g. in SingleMuon, the ones that passed the singlemuon selection
data_samples = {
    "SingleMuon": DataSample(
        input_name = "SingleMuon",
        output_name = "data",
        lumi = lumi["SingleMuon"],
        cuts = [("triggerPath", 1, 2)]
    ),
    "SingleElectron": DataSample(
        input_name = "SingleElectron",
        output_name = "data",
        lumi = lumi["SingleElectron"],
        cuts = [("triggerPath", 2, 3)]
    ),

    "DoubleMuon": DataSample(
        input_name = "DoubleMuon",
        output_name = "data",
        lumi = lumi["DoubleMuon"],
        cuts = [("triggerPath", 3, 4)]
    ),
    "MuonEG": DataSample(
        input_name = "MuonEG",
        output_name = "data",
        lumi = lumi["MuonEG"],
        cuts = [("triggerPath", 4, 5)]
    ),
    "DoubleEG": DataSample(
        input_name = "DoubleEG",
        output_name = "data",
        lumi = lumi["DoubleEG"],
        cuts = [("triggerPath", 5, 6)]
    ),

    "BTagCSV": DataSample(
        input_name = "BTagCSV",
        output_name = "data",
        lumi = lumi["BTagCSV"],
        cuts = [("triggerPath", 6, 7)]
    ),
}

#For single-leptonic analyses, use these data samples
sl_data = [data_samples["SingleMuon"], data_samples["SingleElectron"]]

#now define the analysis categories
sl_categories = [
    # >= 6 jets, >= 4 tags
    Category(
        name = "sl_jge3",
        cuts = [("numJets", 3, 8)],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "numJets",
        src_histogram = "sl/sparse"
    ),

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
        discriminator = "btag_LR_4b_2b_btagCMVA_logit",
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
        discriminator = "btag_LR_4b_2b_btagCMVA_logit",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    # >= 6 jets, == 3 tags, high blr
    Category(
        name = "sl_jge6_t3_blrH",
        cuts = [("numJets", 6, 8), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_btagCSV_logit", blr_cuts["sl_jge6_t3"], 20)],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "btag_LR_4b_2b_btagCMVA_logit",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    # >= 6 jets, == 3 tags, low blr
    Category(
        name = "sl_jge6_t3_blrL",
        cuts = [("numJets", 6, 8), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_btagCSV_logit", -20, blr_cuts["sl_jge6_t3"])],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "btag_LR_4b_2b_btagCMVA_logit",
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
        discriminator = "btag_LR_4b_2b_btagCSV_logit",
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
        discriminator = "btag_LR_4b_2b_btagCMVA_logit",
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
        discriminator = "btag_LR_4b_2b_btagCMVA_logit",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    Category(
        name = "sl_j5_t3_blrH",
        cuts = [("numJets", 5, 6), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_btagCSV_logit", blr_cuts["sl_j5_t3"], 20)],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "btag_LR_4b_2b_btagCMVA_logit",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    # == 5 jets, == 3 tags, low blr
    Category(
        name = "sl_j5_t3_blrL",
        cuts = [("numJets", 5, 6), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_btagCSV_logit", -20, blr_cuts["sl_j5_t3"])],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "btag_LR_4b_2b_btagCSV_logit",
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
        discriminator = "btag_LR_4b_2b_btagCMVA_logit",
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
        discriminator = "btag_LR_4b_2b_btagCMVA_logit",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    # == 4 jets, == 3 tags
    Category(
        name = "sl_j4_t3_blrH",
        cuts = [("numJets", 4, 5), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_btagCSV_logit", blr_cuts["sl_j4_t3"], 20)],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "btag_LR_4b_2b_btagCMVA_logit",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
    
    Category(
        name = "sl_j4_t3_blrL",
        cuts = [("numJets", 4, 5), ("nBCSVM", 3, 4), ("btag_LR_4b_2b_btagCSV_logit", -20, blr_cuts["sl_j4_t3"])],
        samples = base_samples + ttjets_powheg,
        data_samples = sl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "btag_LR_4b_2b_btagCSV_logit",
        rebin=1,
        src_histogram = "sl/sparse"
    ),
]

control_variables = [
    "jetsByPt_0_pt",
    "btag_LR_4b_2b_btagCSV_logit",
#    "btag_LR_4b_2b_btagCMVA_logit"
]
def make_control_categories(input_categories):
    all_cats = copy.deepcopy(input_categories)
    for discr in control_variables:
        for cat in input_categories:
            #Update only the discriminator, note that this is hacky and may not
            #work in the future, because we assume the object is final
            #after the constructor
            newcat_d = cat.__dict__
            newcat_d["discriminator"] = discr
            newcat_d["do_limit"] = False
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
        "sl": [c for c in sl_categories if c.do_limit],
    },
    do_fake_data = do_fake_data,
    do_stat_variations = do_stat_variations
)
for icat in range(len(analysis_ttjets_split.categories)):
    analysis_ttjets_split.categories[icat].samples = base_samples + ttjets_split 
 
# sl_categories_bdt = filter(lambda x: x.discriminator == "common_bdt", all_cats)
# 
# analysis_bdt = Analysis(
#     samples = base_samples + ttjets_powheg,
#     categories = sl_categories_bdt,
#     sparse_input_file = input_file,
#     groups = {
#         "sl": sl_categories_bdt,
#     },
#     do_fake_data = do_fake_data,
#     do_stat_variations = do_stat_variations
# )

#add single-category groups
for cat in sl_categories:
    analysis.groups[cat.full_name] = [cat]
# for cat in sl_categories_bdt:
#     analysis_bdt.groups[cat.full_name] = [cat]

# Dictionary of all analyses we consider
analyses = {
    "SL_7cat" : analysis,
    "SL_ttjets_split" : analysis_ttjets_split,
    #"SL_7cat_bdt" : analysis_bdt
}
