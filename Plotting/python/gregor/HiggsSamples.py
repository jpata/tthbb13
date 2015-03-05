files = {}

files["tth"] = "nhiggs_v5_tth_hbb_13tev-tagging"     
files["ttj"] = "nhiggs_v5_ttj_13tev-tagging"     

files["rad_hh4b_m800"] = "nhiggs_v6_rad_hh4b_m800_13tev_20bx25"     

files["tth_150_200"] = files["tth"]
files["ttj_150_200"] = files["ttj"]

files["tth_200_300"] = files["tth"]
files["ttj_200_300"] = files["ttj"]

files["tth_300_800"] = files["tth"]
files["ttj_300_800"] = files["ttj"]

files["rad_hh4b_m800_170_300"] = files["rad_hh4b_m800"]
files["rad_hh4b_m800_300_470"] = files["rad_hh4b_m800"]
files["rad_hh4b_m800_470_800"] = files["rad_hh4b_m800"]

           
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
    "rad_hh4b_m800_470_800" : "((pt > 470) && (pt <= 800))",



}

pairs = { 
    "pt-150-to-200" : ["tth_150_200", "ttj_150_200"],
    "pt-200-to-300" : ["tth_200_300", "ttj_200_300"],
    "pt-300-to-800" : ["tth_300_800", "ttj_300_800"],
}


