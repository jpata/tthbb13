from TTH.Plotting.Datacards.AnalysisSpecification import *

dl_categories = [
    # >= 4 jets, >= 4 tags
    Category(
        name = "dl_jge4_tge4",
        cuts = [("numJets", 4, 8), ("nBCSVM", 4, 8)],
        samples = base_samples,
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
    groups = {
        "dl": dl_categories,
    },
    do_fake_data = True,
    do_stat_variations = True
)

#add single-category groups
for cat in dl_categories:
    analysis.groups[cat.full_name] = [cat]
