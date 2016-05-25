"""Manage ntuples for toptagging (ntop) """

#######################################
# Imports
######################################

import sys

import TTH.TTHNtupleAnalyzer.CrabHelpers as CH


#######################################
# Configuration
#####################################

# Ntuple name/version and samples to include
name = "ntop"
version = "x6"
li_samples = [
    "zprime_m1000",
    #"qcd_300_470"
]

cmssw_config_path = '/shome/gregor/TOP-763/CMSSW_7_6_3/src/TTH/TTHNtupleAnalyzer/python/'
config_script_name = 'Taggers_cfg.py'
storage_path = '/scratch/gregor/'

#######################################
# Actual work
#####################################

# Decide what to do
actions = ["submit", "status", "kill", "download", "download_globus", "cleanup", "hadd"]

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
        CH.submit(name,
               sample_shortname,  
               version,
               cmssw_config_path = cmssw_config_path,
               cmssw_config_script = config_script_name,
               #site = "T3_CH_PSI",
               blacklist = [])

# Status
if action == "status":
    for sample_shortname in li_samples:
        CH.status(name,
               sample_shortname,  
               version)

# Kill
if action == "kill":
    for sample_shortname in li_samples:
        CH.kill(name,
             sample_shortname,  
             version)

# Download
elif action == "download":
    for sample_shortname in li_samples:
        CH.download(name, sample_shortname, version, storage_path)    

# Download
elif action == "download_globus":
    for sample_shortname in li_samples:
        CH.download_globus(name, sample_shortname, version, storage_path, glob_string = "output*tagg*.root", 
                           #site = "T3_CH_PSI"
        ) 

# Cleanup
elif action == "cleanup":
    for sample_shortname in li_samples:
        CH.cleanup(name, sample_shortname, version, storage_path, infile_glob="*.root")    

# Hadd
elif action == "hadd":
    for sample_shortname in li_samples:
        CH.hadd(name, sample_shortname, version, storage_path)    

