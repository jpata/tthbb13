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

files["zprime_m750"]  = "ntop_v20_zprime_m750_1p_13tev-tagging"     
files["zprime_m1250"] = "ntop_v20_zprime_m1250_1p_13tev-tagging"     
files["zprime_m2000"] = "ntop_v20_zprime_m2000_1p_13tev-tagging"     
files["qcd_170_300"]  = "ntop_v20_qcd_170_300_pythia8_13tev-tagging"
files["qcd_470_600"]  = "ntop_v20_qcd_470_600_pythia8_13tev-tagging"
files["qcd_800_1000"] = "ntop_v20_qcd_800_1000_pythia8_13tev-tagging"


weighted_files = {}
for k,v in files.iteritems():
    weighted_files[k] = basepath + v + "-weighted.root"

pairs = { 
    "pt-200-to-300" : ["zprime_m750", "qcd_170_300"],
    "pt-470-to-600" : ["zprime_m1250", "qcd_470_600"],
    "pt-800-to-1000" : ["zprime_m2000", "qcd_800_1000"],
}

ranges = {"zprime_m750"      : [201, 299],
          "zprime_m1000"     : [301, 469],
          "zprime_m1250"     : [471, 599], 
          "zprime_m2000_low" : [601, 799],
          "zprime_m2000"     : [801, 999],
          "zprime_m3000"     : [1001, 1399], 
          "zprime_m4000"     : [1401, 1799],

          "qcd_170_300"      : [201, 299],
          "qcd_300_470"      : [301, 469],
          "qcd_470_600"      : [471, 599],
          "qcd_800_1000"     : [801, 999],
       }


eta_max = 1.5
fiducial_cuts = {}
for k,v in ranges.iteritems():
    fiducial_cuts[k] = "((pt>{0})&&(pt<{1})&&(fabs(eta)<{2}))".format(v[0], v[1], eta_max)


