"""Manage ntuples for toptagging (ntop) """

#######################################
# Imports
######################################

import sys

from TTH.TTHNtupleAnalyzer.CrabHelpers import submit, status, download, hadd


#######################################
# Configuration
#####################################

# Ntuple name/version and samples to include
name = "ntop"
version = "v3c"
li_samples = [#"qcd_120_170_pythia6_13tev", ok
              #"qcd_170_300_pythia6_13tev", ok
              #"qcd_300_470_pythia6_13tev", ok
              #"qcd_470_600_pythia6_13tev", ok
              "qcd_600_800_pythia6_13tev", 
              # "qcd_800_1000_pythia6_13tev, ok
              # "qcd_1000_1400_pythia6_13tev", ok
              #"qcd_1400_1800_pythia6_13tev", ok
              #"qcd_1800_inf_pythia6_13tev", ok
              "zprime_m1000_1p_13tev",
              #"zprime_m1250_1p_13tev", ok
              #"zprime_m1500_1p_13tev", ok
              #"zprime_m2000_1p_13tev", ok
              "zprime_m3000_1p_13tev", 
              # "zprime_m4000_1p_13tev" ok
              ]

cmssw_config_path = '/shome/gregor/TTH-72X/CMSSW/src/TTH/TTHNtupleAnalyzer/python/'
config_script_name = 'Taggers_cfg.py'
storage_path = '/scratch/gregor/'

#######################################
# Actual work
#####################################

# Decide what to do
actions = ["submit", "status", "download", "hadd"]

if not len(sys.argv) == 2:
    print "Invalid number of arguments"
    print "Usage: {0} {1}".format(sys.argv[0], "/".join(actions))
    sys.exit()

action = sys.argv[1]

if not action in actions:
    print "Invalid action"
    print "Usage: {0} {1}".format(sys.argv[0], "/".join(actions))
    sys.exit()

# Submit
if action == "submit":
    for sample_shortname in li_samples:
        submit(name,
               sample_shortname,  
               version,
               cmssw_config_path = cmssw_config_path,
               cmssw_config_script = config_script_name,
               blacklist = [])

# Status
if action == "status":
    for sample_shortname in li_samples:
        status(name,
               sample_shortname,  
               version)

# Download
elif action == "download":
    for sample_shortname in li_samples:
        download(name, sample_shortname, version, storage_path)    

# Hadd
elif action == "hadd":
    for sample_shortname in li_samples:
        hadd(name, sample_shortname, version, storage_path)    

