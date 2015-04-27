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

#files["zprime_m750"]  = "ntop_v33a_zprime_m750_1p_13tev-tagging"     
#files["zprime_m1250"] = "ntop_v33_zprime_m1250_1p_13tev-tagging"     
#files["zprime_m2000"] = "ntop_v33_zprime_m2000_1p_13tev-tagging"     
#files["qcd_170_300"]  = "ntop_v33_qcd_170_300_pythia8_13tev-tagging"
#files["qcd_470_600"]  = "ntop_v33_qcd_470_600_pythia8_13tev-tagging"
#files["qcd_800_1000"] = "ntop_v33_qcd_800_1000_pythia8_13tev-tagging"

#files["zprime_m750"]  = "ntop_v36_zprime_m750_1p_13tev-tagging"     
#files["zprime_m1000"] = "ntop_v36_zprime_m1000_1p_13tev-tagging"     
#files["zprime_m1250"] = "ntop_v36_zprime_m1250_1p_13tev-tagging"     
#files["zprime_m2000"] = "ntop_v36_zprime_m2000_1p_13tev-tagging"     
#files["zprime_m2000_low"] = "ntop_v36_zprime_m2000_low_1p_13tev-tagging"     
#files["qcd_170_300"]  = "ntop_v36_qcd_170_300_pythia8_13tev-tagging"
#files["qcd_300_470"]  = "ntop_v36_qcd_300_470_pythia8_13tev-tagging"
#files["qcd_470_600"]  = "ntop_v36_qcd_470_600_pythia8_13tev-tagging"
#files["qcd_600_800"]  = "ntop_v36_qcd_600_800_pythia8_13tev-tagging"
#files["qcd_800_1000"] = "ntop_v36_qcd_800_1000_pythia8_13tev-tagging"
#
#files["zprime_m1000_phys14"] = "ntop_v36_zprime_m1000_1p_13tev_phys14_20bx25-tagging"     
#files["zprime_m2000_phys14"] = "ntop_v36_zprime_m2000_1p_13tev_phys14_20bx25-tagging"     
#files["zprime_m2000_low_phys14"] = "ntop_v36_zprime_m2000_low_1p_13tev_phys14_20bx25-tagging"     
#files["qcd_300_470_phys14"]  = "ntop_v36b_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_470_600_phys14"]  = "ntop_v36b_qcd_470_600_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_600_800_phys14"]  = "ntop_v36b_qcd_600_800_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_800_1000_phys14"] = "ntop_v36b_qcd_800_1000_pythia8_13tev_phys14_20bx25-tagging"


#files["zprime_m1000"] = "ntop_v37_zprime_m1000_1p_13tev_phys14_20bx25-tagging"     
#files["qcd_300_470"]  = "ntop_v37_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"

#files["zprime_m1000"] = "ntop_v39_zprime_m1000_1p_13tev_phys14_20bx25-tagging"     
#files["qcd_300_470"]  = "ntop_v39_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"


#files["zprime_m1000_low"] = "ntop_v40_zprime_m1000_low_1p_13tev_phys14_20bx25-tagging"     
#files["zprime_m1000"]     = "ntop_v40_zprime_m1000_1p_13tev_phys14_20bx25-tagging"     
#files["zprime_m2000_low"] = "ntop_v40_zprime_m2000_low_1p_13tev_phys14_20bx25-tagging"     
#files["zprime_m2000"]     = "ntop_v40_zprime_m2000_1p_13tev_phys14_20bx25-tagging"     
#files["qcd_170_300"]      = "ntop_v40_qcd_170_300_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_300_470"]      = "ntop_v40_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_470_600"]      = "ntop_v40_qcd_470_600_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_600_800"]      = "ntop_v40_qcd_600_800_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_800_1000"]     = "ntop_v40_qcd_800_1000_pythia8_13tev_phys14_20bx25-tagging"

files["zprime_m1000_low"] = "ntop_v42_zprime_m1000_low_1p_13tev_phys14_20bx25-tagging"     
files["zprime_m1000"]     = "ntop_v42_zprime_m1000_1p_13tev_phys14_20bx25-tagging"     
files["zprime_m2000_low"] = "ntop_v42_zprime_m2000_low_1p_13tev_phys14_20bx25-tagging"     
files["zprime_m2000"]     = "ntop_v42_zprime_m2000_1p_13tev_phys14_20bx25-tagging"     
files["qcd_170_300"]      = "ntop_v42_qcd_170_300_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_300_470"]      = "ntop_v42_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_470_600"]      = "ntop_v42_qcd_470_600_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_600_800"]      = "ntop_v42_qcd_600_800_pythia8_13tev_phys14_20bx25-tagging"
files["qcd_800_1000"]     = "ntop_v42_qcd_800_1000_pythia8_13tev_phys14_20bx25-tagging"

#files["zprime_m1000_low"] = "ntop_v43_zprime_m1000_low_1p_13tev_phys14_20bx25-tagging"     
#files["zprime_m1000"]     = "ntop_v43_zprime_m1000_1p_13tev_phys14_20bx25-tagging"     
#files["zprime_m2000_low"] = "ntop_v43_zprime_m2000_low_1p_13tev_phys14_20bx25-tagging"     
#files["zprime_m2000"]     = "ntop_v43_zprime_m2000_1p_13tev_phys14_20bx25-tagging"     
#files["qcd_170_300"]      = "ntop_v43_qcd_170_300_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_300_470"]      = "ntop_v43_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_600_800"]      = "ntop_v43_qcd_600_800_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_800_1000"]     = "ntop_v43_qcd_800_1000_pythia8_13tev_phys14_20bx25-tagging"

#files["zprime_m1000_low"] = "ntop_v44_zprime_m1000_low_1p_13tev_phys14_20bx25-tagging"     
#files["zprime_m1000"]     = "ntop_v44_zprime_m1000_1p_13tev_phys14_20bx25-tagging"     
#files["zprime_m2000_low"] = "ntop_v44_zprime_m2000_low_1p_13tev_phys14_20bx25-tagging"     
#files["zprime_m2000"]     = "ntop_v44_zprime_m2000_1p_13tev_phys14_20bx25-tagging"     
#files["qcd_170_300"]      = "ntop_v44_qcd_170_300_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_300_470"]      = "ntop_v44_qcd_300_470_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_600_800"]      = "ntop_v44_qcd_600_800_pythia8_13tev_phys14_20bx25-tagging"
#files["qcd_800_1000"]     = "ntop_v44_qcd_800_1000_pythia8_13tev_phys14_20bx25-tagging"



weighted_files = {}
for k,v in files.iteritems():
    weighted_files[k] = basepath + v + "-weighted.root"

pairs = { 
    "pt-200-to-300" : ["zprime_m1000_low", "qcd_170_300"],
    "pt-300-to-470" : ["zprime_m1000", "qcd_300_470"],
 ###   "pt-470-to-600" : ["zprime_m1250", "qcd_470_600"],
    "pt-600-to-800" : ["zprime_m2000_low", "qcd_600_800"],
    "pt-800-to-1000" : ["zprime_m2000", "qcd_800_1000"],
}

# [Minimal pT, Maximal pT, |eta|]
ranges = {#zprime_m750"      : [201, 299,   2.4, 0.8, "ca15"],
    "zprime_m750"      : [201, 299,   2.4, 0.8, "ca15"],
    "zprime_m1000_low" : [201, 299,   2.4, 0.8, "ca15"],
    "zprime_m1000"     : [301, 469,   2.4, 0.8, "ca15"],
    "zprime_m1250"     : [471, 599,   2.1, 0.6, "ca08"], 
    "zprime_m2000_low" : [601, 799,   2.1, 0.6, "ca08"],
    "zprime_m2000"     : [801, 999,   1.5, 0.6, "ca08"],
    "zprime_m3000"     : [1001, 1399, 1.5, 0.6, "ca08"], 
    "zprime_m4000"     : [1401, 1799, 1.3, 0.6, "ca08"],
    
    "qcd_170_300"      : [201, 299, 2.4, 0.8, "ca15"],
    "qcd_300_470"      : [301, 469, 2.4, 0.8, "ca15"],
    "qcd_470_600"      : [471, 599, 2.1, 0.6, "ca08"],
    "qcd_600_800"      : [601, 799, 2.1, 0.6, "ca08"],
    "qcd_800_1000"     : [801, 999, 1.5, 0.6, "ca08"],
       }

sample_names = {"zprime_m750"      : "Top, 200..300",
                "zprime_m1000"     : "Top, 300..470",
                "zprime_m1250"     : "Top, 470..600", 
                "zprime_m2000_low" : "Top, 600..800",
                "zprime_m2000"     : "Top, 800..1000",
                "zprime_m3000"     : "Top, 1000..1400", 
                "zprime_m4000"     : "Top, 1400..2000",
                
                "qcd_170_300"      : "QCD, 200..300",
                "qcd_300_470"      : "QCD, 300..470",
                "qcd_470_600"      : "QCD, 470..600",
                "qcd_600_800"      : "QCD, 600..800",
                "qcd_800_1000"     : "QCD, 800..10000",
            }

other_sample_names = {
                      "zprime_m1000_low" : "Signal (200..300 GeV)",                      
                      "zprime_m1000"     : "Signal (300..470 GeV)",                      
                      "zprime_m2000_low" : "Signal (600..800 GeV)",                      
                      "zprime_m2000"     : "Signal (800..1000 GeV)",                      
                      "qcd_170_300"      : "BG (200..300 GeV)",
                      "qcd_300_470"      : "BG (300..470 GeV)",
                      "qcd_600_800"      : "BG (600..800 GeV)",
                      "qcd_800_1000"      : "BG (800..1000 GeV)",
            }



fiducial_cuts = {}
for k,v in ranges.iteritems():
    fiducial_cuts[k] = "((pt>{0})&&(pt<{1})&&(fabs(eta)<{2})&&(top_size<{3}))".format(v[0], v[1], v[2], v[3])


