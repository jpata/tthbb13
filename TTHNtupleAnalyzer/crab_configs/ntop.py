""" ntop: Manage submission of ntuples for toptagging (ntop) """

from TTH.TTHNtupleAnalyzer.CrabHelpers import submit

# What to do
version = "v3"
li_samples = ["qcd_120_170_pythia6_13tev",
              "qcd_170_300_pythia6_13tev",
              "qcd_300_470_pythia6_13tev",
              "qcd_470_600_pythia6_13tev",
              "qcd_600_800_pythia6_13tev",
              "qcd_800_1000_pythia6_13tev",
              "qcd_1000_1400_pythia6_13tev",
              "qcd_1400_1800_pythia6_13tev",
              "qcd_1800_inf_pythia6_13tev",
              "zprime_m1000_1p_13tev",
              "zprime_m1250_1p_13tev",
              "zprime_m1500_1p_13tev",
              "zprime_m2000_1p_13tev",
              "zprime_m3000_1p_13tev",
              "zprime_m4000_1p_13tev"]

# Submit all samples
for sample_shortname in li_samples:
    submit("ntop", 
           sample_shortname,  
           version,
           cmssw_config_path = '/shome/gregor/TTH-72X/CMSSW/src/TTH/TTHNtupleAnalyzer/python/',
           cmssw_config_script = "Taggers_cfg.py",
           blacklist = ["T1_US_FNAL"]
    )
# end of li_samples loop    
