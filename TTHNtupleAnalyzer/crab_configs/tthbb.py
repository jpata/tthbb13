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
name = "TTHbb"
version = "s1_5b21f5f"
li_samples = [
"tth_hbb_13tev",
"ttjets_13tev",
"ttjets_13tev_phys14",
"ttjets_13tev_phys14_pythia8",
"ttjets_13tev_phys14_pythia8_pu40bx50",
"t_t_13tev_phys14",
"tbar_t_13tev_phys14",
"tth_hbb_13tev_pu40bx50",
"ttjets_13tev_pu40bx50"
]

cmssw_config_path = '/home/joosep/TTH/CMSSW/src/TTH/TTHNtupleAnalyzer/python/'
config_script_name = 'Main_cfg.py'
storage_path = '/scratch/joosep'

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
			   site = "T2_EE_Estonia",
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

