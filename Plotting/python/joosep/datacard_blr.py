from datacard import Datacard

Datacard.analysis_categories = [
    "sl_j4_t3_blrH",
    "sl_j4_t3_blrL",
    "sl_j5_t3_blrH",
    "sl_j5_t3_blrL",
    "sl_jge6_t3_blrH",
    "sl_jge6_t3_blrL",
    "sl_jge6_tge4_blrH",
    "sl_jge6_tge4_blrL"
]

Datacard.shape_uncertainties = {}
Datacard.scale_uncertainties = {}
for cat in Datacard.analysis_categories:
    Datacard.shape_uncertainties[cat] = Datacard.total_shape_uncert
    Datacard.scale_uncertainties[cat] = Datacard.common_scale_uncertainties

Datacard.output_datacardname = "shapes_blr.txt"
