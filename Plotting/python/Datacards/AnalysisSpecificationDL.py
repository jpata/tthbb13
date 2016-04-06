from TTH.Plotting.Datacards.AnalysisSpecificationSL import data_samples, base_samples, signal_processes, common_shape_uncertainties, lumi, common_scale_uncertainties, scale_uncertainties, make_control_categories
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Sample, Category, Analysis, make_csv_categories_abstract, make_csv_groups_abstract

dl_data = [data_samples["DoubleMuon"], data_samples["MuonEG"], data_samples["DoubleEG"]]

dl_categories = [
    # >= 4 jets, >= 4 tags
    Category(
        name = "dl_jge4_tge4",
        cuts = [("numJets", 4, 8), ("nBCSVM", 4, 8)],
        samples = base_samples,
        data_samples = dl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_DL_0w2h2t",
        src_histogram = "dl/sparse"
    ),
    
    # >= 4 jets, == 3 tags
    Category(
        name = "dl_jge4_t3",
        cuts = [("numJets", 4, 8), ("nBCSVM", 3, 4)],
        samples = base_samples,
        data_samples = dl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_DL_0w2h2t",
        src_histogram = "dl/sparse"
    ),
    
    # >= 4 jets, == 2 tags
    Category(
        name = "dl_jge4_t2",
        cuts = [("numJets", 4, 8), ("nBCSVM", 2, 3)],
        samples = base_samples,
        data_samples = dl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_DL_0w2h2t",
        src_histogram = "dl/sparse"
    ),
    
    # == 3 jets, == 3 tags
    Category(
        name = "dl_j3_t3",
        cuts = [("numJets", 3, 4), ("nBCSVM", 3, 4)],
        samples = base_samples,
        data_samples = dl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_DL_0w2h2t",
        src_histogram = "dl/sparse"
    ),
    
    # == 3 jets, == 2 tags
    Category(
        name = "dl_j3_t2",
        cuts = [("numJets", 3, 4), ("nBCSVM", 2, 3)],
        samples = base_samples,
        sparse_input_file = "/mnt/t3nfs01/data01/shome/gregor/sparse_Apr1.root",
        data_samples = dl_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_DL_0w2h2t",
        src_histogram = "dl/sparse"
    ),
]

all_cats = make_control_categories(dl_categories)

analysis = Analysis(
    samples = base_samples,
    categories = all_cats,
    sparse_input_file = "/mnt/t3nfs01/data01/shome/gregor/sparse_Apr1.root",
    groups = {
        "dl": dl_categories,
    },
    do_fake_data = True,
    do_stat_variations = True
)

#add single-category groups
for cat in dl_categories:
    analysis.groups[cat.full_name] = [cat]

analyses = {"DL" : analysis}

def make_csv_categories():
    return make_csv_categories_abstract(analyses)

def make_csv_groups():
    return make_csv_groups_abstract(analyses)


