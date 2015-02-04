"""Manage ntuples for toptagging (ntop) """

#######################################
# Imports
######################################

import sys

from TTH.TTHNtupleAnalyzer.CrabHelpers import submit, status, kill, download, download_globus, hadd


#######################################
# Configuration
#####################################

# Ntuple name/version and samples to include
name = "ntop"
version = "v19"
li_samples = [
 #   "qcd_170_300_pythia8_13tev",
 #   "qcd_300_470_pythia8_13tev",
 #   "qcd_470_600_pythia8_13tev",
 #   "qcd_600_800_pythia8_13tev",    
 #   "qcd_800_1000_pythia8_13tev",    

 #   "zprime_m500_1p_13tev",
 #   "zprime_m750_1p_13tev",

 #   "zprime_m1000_1p_13tev",
 #   "zprime_m1250_1p_13tev", 
 #   "zprime_m1500_1p_13tev", 
 #   "zprime_m2000_1p_13tev",
 #   "zprime_m3000_1p_13tev", 
 #   "zprime_m4000_1p_13tev",
]

cmssw_config_path = '/shome/gregor/TTH-73X/CMSSW/src/TTH/TTHNtupleAnalyzer/python/'
config_script_name = 'Taggers_cfg.py'
storage_path = '/scratch/gregor/'

#######################################
# Actual work
#####################################

# Decide what to do
actions = ["submit", "status", "kill", "download", "download_globus", "hadd"]

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
               template_filename = "c_TEMPLATE_script.py",
               blacklist = ["T1_US_FNAL"])

# Status
if action == "status":
    for sample_shortname in li_samples:
        status(name,
               sample_shortname,  
               version)

# Kill
if action == "kill":
    for sample_shortname in li_samples:
        kill(name,
             sample_shortname,  
             version)

# Download
elif action == "download":
    for sample_shortname in li_samples:
        download(name, sample_shortname, version, storage_path)    

# Download / Globus
elif action == "download_globus":
    for sample_shortname in li_samples:
        download_globus(name, sample_shortname, version, storage_path, "gregor", "*tagging*")    

# Hadd
elif action == "hadd":
    for sample_shortname in li_samples:
        hadd(name, 
             sample_shortname, 
             version, 
             storage_path, 
             infile_glob = "*tagging*.root*", 
             outfile_suffix = "-tagging")    

