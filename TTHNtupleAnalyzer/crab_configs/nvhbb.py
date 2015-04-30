"""Download ntuples from HEPPY VHbb productions"""

#######################################
# Imports
######################################

import sys

from TTH.TTHNtupleAnalyzer.CrabHelpers import submit, status, kill, download, download_globus, hadd, cleanup


#######################################
# Configuration
#####################################

# Ntuple name/version and samples to include
name = "VHBB_HEPPY"
version = "V11_G01"
li_samples = [
    "ttbar_13tev_phys14_20bx25",
]

storage_path = '/scratch/gregor/'

#######################################
# Actual work
#####################################

# Decide what to do
actions = ["download_globus", "hadd", "cleanup"]

if not len(sys.argv) == 2:
    print "Invalid number of arguments"
    print "Usage: {0} {1}".format(sys.argv[0], "/".join(actions))
    sys.exit()

action = sys.argv[1]

if not action in actions:
    print "Invalid action"
    print "Usage: {0} {1}".format(sys.argv[0], "/".join(actions))
    sys.exit()

# Download
elif action == "download_globus":
    for sample_shortname in li_samples:
        download_globus(name, sample_shortname, version, storage_path, glob_string = "tree_*.root", isVHBBHEPPY = True)    


# Cleanup
elif action == "cleanup":
    for sample_shortname in li_samples:
        cleanup(name, sample_shortname, version, storage_path, infile_glob="*.root")    


# Hadd
elif action == "hadd":
    for sample_shortname in li_samples:
        hadd(name, sample_shortname, version, storage_path)    

