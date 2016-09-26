from TTH.Plotting.Datacards.AnalysisSpecificationSL import data_samples, base_samples, ttjets_powheg, signal_processes, common_shape_uncertainties, common_scale_uncertainties, scale_uncertainties, make_control_categories, input_file
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Sample, Category, Analysis, make_csv_categories_abstract, make_csv_groups_abstract


fh_data = [data_samples["BTagCSV"]]

print "scale_uncertainties:",scale_uncertainties

fh_categories = [
    # == 4 jets, == 4 tags
    Category(
        name = "fh_jge8_tge4",
        cuts = [("numJets", 8, 9), ("nBCSVM", 4, 5)],
        samples = base_samples + ttjets_powheg, ## ADDME: + qcd
        data_samples = fh_data,
        signal_processes = signal_processes,
        common_shape_uncertainties = common_shape_uncertainties,
        common_scale_uncertainties = common_scale_uncertainties,
        scale_uncertainties = scale_uncertainties,
        discriminator = "mem_FH_4w2h2t_p",
        src_histogram = "fh/sparse"
    ),
#   EXAMPLE FROM DL
#    # >= 4 jets, >= 4 tags
#    Category(
#        name = "had_jge4_tge4",
#        cuts = [("numJets", 4, 8), ("nBCSVM", 4, 8)],
#        samples = base_samples + ttjets_powheg,
#        data_samples = had_data,
#        signal_processes = signal_processes,
#        common_shape_uncertainties = common_shape_uncertainties,
#        common_scale_uncertainties = common_scale_uncertainties,
#        scale_uncertainties = scale_uncertainties,
#        discriminator = "mem_had_0w2h2t_p",
#        src_histogram = "dl/sparse"
#    ),
]

all_cats = make_control_categories(fh_categories)

analysis = Analysis(
    samples = base_samples,
    categories = all_cats,
    sparse_input_file = input_file,
    groups = {
        "fh": fh_categories,
    },
    do_fake_data = True,
    do_stat_variations = True
)

#add single-category groups
for cat in fh_categories:
    analysis.groups[cat.full_name] = [cat]

analyses = {"FH" : analysis}

def make_csv_categories():
    return make_csv_categories_abstract(analyses)

def make_csv_groups():
    return make_csv_groups_abstract(analyses)


