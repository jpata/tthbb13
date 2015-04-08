"""Manage ntuples for higgs-tagging (nhiggs)"""

#######################################
# Imports
######################################

import sys

from TTH.TTHNtupleAnalyzer.CrabHelpers import submit, status, kill, download, download_globus, hadd, cleanup


#######################################
# Configuration
#####################################

# Ntuple name/version and samples to include
name = "nhiggs"
version = "v10"
li_samples = [
    "rad_hh4b_m800_13tev_20bx25",
    "rad_hh4b_m1600_13tev_20bx25",
    "qcd_170_300_pythia8_13tev_phys14_20bx25",
    "qcd_300_470_pythia8_13tev_phys14_20bx25",
    "qcd_470_600_pythia8_13tev_phys14_20bx25",
    "qcd_600_800_pythia8_13tev_phys14_20bx25",
]

cmssw_config_path = '/shome/gregor/TTH-73X/CMSSW/src/TTH/TTHNtupleAnalyzer/python/'
config_script_name = 'HiggsTaggers_cfg.py'
storage_path = '/scratch/gregor/'

#######################################
# Actual work
#####################################

# Decide what to do
actions = ["submit", "status", "kill", "download", "download_globus", "hadd", "cleanup"]

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

elif action == "download_globus":
    for sample_shortname in li_samples:
        download_globus(name, sample_shortname, version, storage_path, glob_string = "output-tagging*.root")    


# Cleanup
elif action == "cleanup":
    for sample_shortname in li_samples:
        cleanup(name, sample_shortname, version, storage_path, infile_glob="*.root")    


# Hadd
elif action == "hadd":
    for sample_shortname in li_samples:
        hadd(name, sample_shortname, version, storage_path)    

