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

files["zprime_m750"]  = "ntop_v25_zprime_m750_1p_13tev-tagging"     
files["zprime_m1250"] = "ntop_v25_zprime_m1250_1p_13tev-tagging"     
files["zprime_m2000"] = "ntop_v25_zprime_m2000_1p_13tev-tagging"     
files["qcd_170_300"]  = "ntop_v25_qcd_170_300_pythia8_13tev-tagging"
files["qcd_470_600"]  = "ntop_v25_qcd_470_600_pythia8_13tev-tagging"
files["qcd_800_1000"] = "ntop_v25_qcd_800_1000_pythia8_13tev-tagging"


weighted_files = {}
for k,v in files.iteritems():
    weighted_files[k] = basepath + v + "-weighted.root"

pairs = { 
    "pt-200-to-300" : ["zprime_m750", "qcd_170_300"],
    "pt-470-to-600" : ["zprime_m1250", "qcd_470_600"],
    "pt-800-to-1000" : ["zprime_m2000", "qcd_800_1000"],
}

# [Minimal pT, Maximal pT, |eta|]
ranges = {"zprime_m750"      : [201, 299,   2.5],
          "zprime_m1000"     : [301, 469,   2.5],
          "zprime_m1250"     : [471, 599,   2.2], 
          "zprime_m2000_low" : [601, 799,   2.2],
          "zprime_m2000"     : [801, 999,   1.8],
          "zprime_m3000"     : [1001, 1399, 1.6], 
          "zprime_m4000"     : [1401, 1799, 1.4],

          "qcd_170_300"      : [201, 299, 2.5],
          "qcd_300_470"      : [301, 469, 2.5],
          "qcd_470_600"      : [471, 599, 2.2],
          "qcd_800_1000"     : [801, 999, 1.8],
       }

fiducial_cuts = {}
for k,v in ranges.iteritems():
    fiducial_cuts[k] = "((pt>{0})&&(pt<{1})&&(fabs(eta)<{2}))".format(v[0], v[1], v[2])


