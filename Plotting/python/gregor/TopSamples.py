import socket # to get the hostname

if socket.gethostname() == "t3ui12":
    basepath = '/scratch/gregor/'
else:
    basepath = '/Users/gregor/'


files = {}

#files["zprime_m750"]      = "ntop_v18a_zprime_m750_1p_13tev-tagging"     
#files["zprime_m1000"]     = "ntop_v18a_zprime_m1000_1p_13tev-tagging"     
#files["zprime_m1250"]     = "ntop_v18a_zprime_m1250_1p_13tev-tagging"     
#files["zprime_m2000_low"] = "ntop_v18_zprime_m2000_low_1p_13tev-tagging"     
#files["zprime_m2000"]     = "ntop_v18_zprime_m2000_1p_13tev-tagging"     
#files["zprime_m3000"]     = "ntop_v18b_zprime_m3000_1p_13tev-tagging"     
#files["zprime_m4000"]     = "ntop_v18b_zprime_m4000_1p_13tev-tagging"     
#
#files["qcd_170_300"] = "ntop_v18a_qcd_170_300_pythia8_13tev-tagging"
##files["qcd_300_470"] = "ntop_v15c_qcd_300_470_pythia8_13tev-tagging"
#files["qcd_470_600"] = "ntop_v18a_qcd_470_600_pythia8_13tev-tagging"
#files["qcd_800_1000"] = "ntop_v18_qcd_800_1000_pythia8_13tev-tagging"

#files["zprime_m750"]  = "ntop_v21_zprime_m750_1p_13tev-tagging"     
#files["zprime_m1250"] = "ntop_v21_zprime_m1250_1p_13tev-tagging"     
#files["zprime_m2000"] = "ntop_v21_zprime_m2000_1p_13tev-tagging"     
#files["qcd_170_300"]  = "ntop_v21a_qcd_170_300_pythia8_13tev-tagging"
#files["qcd_470_600"]  = "ntop_v21a_qcd_470_600_pythia8_13tev-tagging"
#files["qcd_800_1000"] = "ntop_v21_qcd_800_1000_pythia8_13tev-tagging"

#files["zprime_m2000"] = "ntop_v19_zprime_m2000_1p_13tev-tagging"     
#files["qcd_800_1000"] = "ntop_v19_qcd_800_1000_pythia8_13tev-tagging"

#files["zprime_m750"]  = "ntop_v27_zprime_m750_1p_13tev-tagging"     
#files["zprime_m1250"] = "ntop_v27_zprime_m1250_1p_13tev-tagging"     
#files["zprime_m2000"] = "ntop_v27_zprime_m2000_1p_13tev-tagging"     
#files["qcd_170_300"]  = "ntop_v27_qcd_170_300_pythia8_13tev-tagging"
#files["qcd_470_600"]  = "ntop_v27_qcd_470_600_pythia8_13tev-tagging"
#files["qcd_800_1000"] = "ntop_v27_qcd_800_1000_pythia8_13tev-tagging"

#files["zprime_m2000"] = "ntop_v26_zprime_m2000_1p_13tev-tagging"     
#files["qcd_800_1000"] = "ntop_v26_qcd_800_1000_pythia8_13tev-tagging"

#files["zprime_m2000"] = "ntop_v31_zprime_m2000_1p_13tev-tagging"     
#files["qcd_800_1000"] = "ntop_v31_qcd_800_1000_pythia8_13tev-tagging"

#files["zprime_m2000"] = "ntop_v32_zprime_m2000_1p_13tev-tagging"     
#files["qcd_800_1000"] = "ntop_v32_qcd_800_1000_pythia8_13tev-tagging"

files["zprime_m750"]  = "ntop_v33a_zprime_m750_1p_13tev-tagging"     
files["zprime_m1250"] = "ntop_v33_zprime_m1250_1p_13tev-tagging"     
files["zprime_m2000"] = "ntop_v33_zprime_m2000_1p_13tev-tagging"     
files["qcd_170_300"]  = "ntop_v33_qcd_170_300_pythia8_13tev-tagging"
files["qcd_470_600"]  = "ntop_v33_qcd_470_600_pythia8_13tev-tagging"
files["qcd_800_1000"] = "ntop_v33_qcd_800_1000_pythia8_13tev-tagging"




weighted_files = {}
for k,v in files.iteritems():
    weighted_files[k] = basepath + v + "-weighted.root"

pairs = { 
    "pt-200-to-300" : ["zprime_m750", "qcd_170_300"],
    "pt-470-to-600" : ["zprime_m1250", "qcd_470_600"],
    "pt-800-to-1000" : ["zprime_m2000", "qcd_800_1000"],
}

# [Minimal pT, Maximal pT, |eta|]
ranges = {"zprime_m750"      : [201, 299,   2.4, 0.8, "ca15"],
          "zprime_m1000"     : [301, 469,   2.4, 0.8, "ca15"],
          "zprime_m1250"     : [471, 599,   2.1, 0.6, "ca08"], 
          "zprime_m2000_low" : [601, 799,   2.1, 0.6, "ca08"],
          "zprime_m2000"     : [801, 999,   1.5, 0.6, "ca08"],
          "zprime_m3000"     : [1001, 1399, 1.5, 0.6, "ca08"], 
          "zprime_m4000"     : [1401, 1799, 1.3, 0.6, "ca08"],

          "qcd_170_300"      : [201, 299, 2.4, 0.8, "ca15"],
          "qcd_300_470"      : [301, 469, 2.4, 0.8, "ca15"],
          "qcd_470_600"      : [471, 599, 2.1, 0.6, "ca08"],
          "qcd_800_1000"     : [801, 999, 1.5, 0.6, "ca08"],
       }

fiducial_cuts = {}
for k,v in ranges.iteritems():
    fiducial_cuts[k] = "((pt>{0})&&(pt<{1})&&(fabs(eta)<{2})&&(top_size<{3}))".format(v[0], v[1], v[2], v[3])


