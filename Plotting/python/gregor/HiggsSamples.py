files = {}

#files["tth"] = "nhiggs_v5_tth_hbb_13tev-tagging"     
#files["ttj"] = "nhiggs_v5_ttj_13tev-tagging"     

files["rad_hh4b_m800"] = "nhiggs_v7b_rad_hh4b_m800_13tev_20bx25-tagging"     

files["qcd_170_300"] = "nhiggs_v7b_qcd_170_300_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_300_470"] = "nhiggs_v7b_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_470_600"] = "nhiggs_v7b_qcd_470_600_pythia8_13tev_phys14_20bx25-tagging"

#files["tth_150_200"] = files["tth"]
#files["ttj_150_200"] = files["ttj"]

#files["tth_200_300"] = files["tth"]
#files["ttj_200_300"] = files["ttj"]

#files["tth_300_800"] = files["tth"]
#files["ttj_300_800"] = files["ttj"]

files["rad_hh4b_m800_170_300"] = files["rad_hh4b_m800"]
files["rad_hh4b_m800_300_470"] = files["rad_hh4b_m800"]
files["rad_hh4b_m800_470_600"] = files["rad_hh4b_m800"]

           
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
    "rad_hh4b_m800_470_600" : "((pt > 470) && (pt <= 600))",

    "qcd_170_300" : "((pt > 170) && (pt <= 300))",
    "qcd_300_470" : "((pt > 300) && (pt <= 470))",
    "qcd_470_600" : "((pt > 470) && (pt <= 600))",
}

pairs = { 
    "pt-170-to-300" : ["qcd_170_300", "rad_hh4b_m800_170_300"],
    "pt-300-to-470" : ["qcd_300_470", "rad_hh4b_m800_300_470"],

}


