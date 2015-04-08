files = {}

#files["tth"] = "nhiggs_v5_tth_hbb_13tev-tagging"     
#files["ttj"] = "nhiggs_v5_ttj_13tev-tagging"     

# V8
files["rad_hh4b_m800"]  = "nhiggs_v8_rad_hh4b_m800_13tev_20bx25-tagging"     
files["rad_hh4b_m1600"] = "nhiggs_v8_rad_hh4b_m1600_13tev_20bx25-tagging"     
files["qcd_170_300"] = "nhiggs_v8_qcd_170_300_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_300_470"] = "nhiggs_v8_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_470_600"] = "nhiggs_v8_qcd_470_600_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_600_800"] = "nhiggs_v8_qcd_600_800_pythia8_13tev_phys14_20bx25-tagging"

# V10
#files["rad_hh4b_m800"]  = "nhiggs_v10_rad_hh4b_m800_13tev_20bx25-tagging"     
#files["rad_hh4b_m1600"] = "nhiggs_v10_rad_hh4b_m1600_13tev_20bx25-tagging"     
#files["qcd_170_300"]    = "nhiggs_v10_qcd_170_300_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_300_470"]    = "nhiggs_v10_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_470_600"]    = "nhiggs_v10_qcd_470_600_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_600_800"]    = "nhiggs_v10_qcd_600_800_pythia8_13tev_phys14_20bx25-tagging"


files["rad_hh4b_m800_170_300"] = files["rad_hh4b_m800"]
files["rad_hh4b_m800_300_470"] = files["rad_hh4b_m800"]
files["rad_hh4b_m1600_470_600"] = files["rad_hh4b_m1600"]
files["rad_hh4b_m1600_600_800"] = files["rad_hh4b_m1600"]

           
fiducial_cuts = {
    "tth" : "(pt > 150)",
    "ttj" : "(pt > 150)",

    "tth_150_200" : "((pt  > 150)&&(pt  <= 200))",
    "ttj_150_200" : "((pt > 150)&&(pt <= 200))",

    "tth_200_300" : "((pt  > 200)&&(pt  <= 300))",
    "ttj_200_300" : "((pt > 200)&&(pt <= 300))",

    "tth_200_300" : "((pt  > 200)&&(pt  <= 300))",
    "ttj_200_300" : "((pt > 200)&&(pt <= 300))",

    "tth_300_800" : "((pt  > 300)&&(pt  <= 800))",
    "ttj_300_800" : "((pt > 300)&&(pt <= 800))",

    "rad_hh4b_m800_170_300" : "((pt > 170) && (pt <= 300))",
    "rad_hh4b_m800_300_470" : "((pt > 300) && (pt <= 470))",
    "rad_hh4b_m1600_470_600" : "((pt > 470) && (pt <= 600))",
    "rad_hh4b_m1600_600_800" : "((pt > 600) && (pt <= 800))",

    "qcd_170_300" : "((pt > 170) && (pt <= 300))",
    "qcd_300_470" : "((pt > 300) && (pt <= 470))",
    "qcd_470_600" : "((pt > 470) && (pt <= 600))",
    "qcd_600_800" : "((pt > 600) && (pt <= 800))",
}

pairs = { 
    "pt-170-to-300" : ["qcd_170_300", "rad_hh4b_m800_170_300"],
    "pt-300-to-470" : ["qcd_300_470", "rad_hh4b_m800_300_470"],
    "pt-470-to-600" : ["qcd_470_600", "rad_hh4b_m1600_470_600"],
    "pt-600-to-800" : ["qcd_600_800", "rad_hh4b_m1600_600_800"],

}


