""" ntop: Manage submission of ntuples for toptagging (ntop) """

from TTH.TTHNtupleAnalyzer.CrabHelpers import submit

# What to do
version = "v2"
li_samples = ["zprime_m2000_1p_13tev", "qcd_300_470_pythia6_13tev"]

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
