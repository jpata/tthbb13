files = {}

#files["tth"] = "nhiggs_v5_tth_hbb_13tev-tagging"     
#files["ttj"] = "nhiggs_v5_ttj_13tev-tagging"     

# V8
#files["rad_hh4b_m800"]  = "nhiggs_v8_rad_hh4b_m800_13tev_20bx25-tagging"     
#files["rad_hh4b_m1600"] = "nhiggs_v8_rad_hh4b_m1600_13tev_20bx25-tagging"     
#files["qcd_170_300"] = "nhiggs_v8_qcd_170_300_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_300_470"] = "nhiggs_v8_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_470_600"] = "nhiggs_v8_qcd_470_600_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_600_800"] = "nhiggs_v8_qcd_600_800_pythia8_13tev_phys14_20bx25-tagging"

# V10
files["rad_hh4b_m800_170_300"]  = "nhiggs_v10_rad_hh4b_m800_low_13tev_20bx25-tagging"     
files["rad_hh4b_m800_300_470"]  = "nhiggs_v10_rad_hh4b_m800_13tev_20bx25-tagging"     
files["rad_hh4b_m1600_470_600"] = "nhiggs_v10_rad_hh4b_m1600_low_13tev_20bx25-tagging"     
files["rad_hh4b_m1600_600_800"] = "nhiggs_v10_rad_hh4b_m1600_13tev_20bx25-tagging"     
files["qcd_170_300"]    = "nhiggs_v10_qcd_170_300_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_300_470"]    = "nhiggs_v10_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_470_600"]    = "nhiggs_v10_qcd_470_600_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_600_800"]    = "nhiggs_v10_qcd_600_800_pythia8_13tev_phys14_20bx25-tagging"


pairs = { 
    "pt-170-to-300" : ["qcd_170_300", "rad_hh4b_m800_170_300"],
    "pt-300-to-470" : ["qcd_300_470", "rad_hh4b_m800_300_470"],
    "pt-470-to-600" : ["qcd_470_600", "rad_hh4b_m1600_470_600"],
    "pt-600-to-800" : ["qcd_600_800", "rad_hh4b_m1600_600_800"],
}

ranges = {
    "rad_hh4b_m800_170_300"      : [170, 300, "ca15"],
    "rad_hh4b_m800_300_470"      : [300, 470, "ca15"],
    "rad_hh4b_m1600_470_600"     : [470, 600, "ak08"],
    "rad_hh4b_m1600_600_800"     : [600, 800, "ak08"],
    "qcd_170_300"                : [170, 300, "ca15"],
    "qcd_300_470"                : [300, 470, "ca15"],
    "qcd_470_600"                : [470, 600, "ak08"],
    "qcd_600_800"                : [600, 800, "ak08"],
}

fiducial_cuts = {k:"((pt>{0})&&(pt<{1})&&({2}trimmedr2f6_mass>90))".format(v[0], v[1], v[2]) for k,v in ranges.iteritems()}

sample_names = {
    "rad_hh4b_m800_170_300"      : "Sig. (170..300 GeV)",
    "rad_hh4b_m800_300_470"      : "Sig. (300..470 GeV)",
    "rad_hh4b_m1600_470_600"     : "Sig. (470..600 GeV)",
    "rad_hh4b_m1600_600_800"     : "Sig. (600..800 GeV)",
    "qcd_170_300"                : "Bgd. (170..300 GeV)",
    "qcd_300_470"                : "Bgd. (300..470 GeV)",
    "qcd_470_600"                : "Bgd. (470..600 GeV)",
    "qcd_600_800"                : "Bgd. (600..800 GeV)",
}



