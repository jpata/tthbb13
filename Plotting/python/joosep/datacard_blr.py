from datacard import Datacard

Datacard.analysis_categories = [
    "sl_jge6_tge4_blrH",
    "sl_jge6_tge4_blrL"
]

Datacard.shape_uncertainties = {}
Datacard.scale_uncertainties = {}
for cat in Datacard.analysis_categories:
    Datacard.shape_uncertainties[cat] = Datacard.total_shape_uncert
    Datacard.scale_uncertainties[cat] = Datacard.common_scale_uncertainties

Datacard.output_datacardname = "shapes_blr.txt"
