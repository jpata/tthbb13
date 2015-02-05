"""Manage ntuples for toptagging (ntop) """

#######################################
# Imports
######################################

import sys, os

from TTH.TTHNtupleAnalyzer.CrabHelpers import submit, status, download, hadd, get_lfn, hadd_from_file, replicate
from collections import Counter

#######################################
# Configuration
#####################################

# Ntuple name/version and samples to include
name = "TTHbb"
version = "s1_eb733a1"
li_samples = [
    "tth_hbb_13tev",
    "ttjets_13tev",
    "t_t_13tev_amcatnlo_pu20bx25_phys14",
    "tbar_t_13tev_amcatnlo_pu20bx25_phys14",
    "tth_hbb_13tev_amcatnlo_pu20bx25_phys14",
    "tth_hbb_13tev_amcatnlo_pu40bx50_phys14",
    "ttjets_13tev_madgraph_pu20bx25_phys14",
    "ttjets_13tev_pythia8_pu20bx25_phys14",
    "ttjets_13tev_pythia8_pu40bx50_phys14",
    "tth_htautau_13tev_amcatnlo_pu30bx50_phys14"
]

cmssw_config_path = os.environ["CMSSW_BASE"] + '/src/TTH/TTHNtupleAnalyzer/python/'
config_script_name = 'Main_cfg.py'
storage_path = '/scratch/joosep'
tier_prefix = '/hdfs/cms/'

#######################################
# Actual work
#####################################

# Decide what to do
actions = ["submit", "status", "download", "hadd", "haddfiles", "replicate"]

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
        stat = status(name,
               sample_shortname,
               version,
               parse=True
        )
        #print stat
        sm = Counter(map(lambda x: x["State"], stat.values()))
        if sum(sm.values())>0:
            done_pc = float(sm.get("finished", 0)) / float(sum(sm.values()))
        else:
            done_pc = -1
        print "{0} {1:.2f} {2}".format(sample_shortname, done_pc, sm.items())
        lfns = get_lfn(name,
               sample_shortname,
               version,
               stat
        )
        working_dir = "crab_{0}_{1}_{2}/crab_{0}_{1}_{2}".format(name, version, sample_shortname)
        of = open(working_dir + "/files.txt", "w")
        nf = 0
        for k in stat.keys():
            if stat[k]["State"] == "finished":
                if lfns.has_key(int(k)):
                    of.write(tier_prefix + lfns[int(k)] + "\n")
                    nf += 1
        of.close()
        print "wrote {0} files".format(nf)

# Download
elif action == "download":
    for sample_shortname in li_samples:
        download(name, sample_shortname, version, storage_path)

# Hadd
elif action == "hadd":
    for sample_shortname in li_samples:
        hadd(name, sample_shortname, version, storage_path)

elif action == "haddfiles":
    ofile = open("to-replica.txt", "w")
    for sample_shortname in li_samples:
        ofname = hadd_from_file(name, sample_shortname, version, storage_path)
        if not ofname:
            print "ERROR: could not hadd ", sample_shortname
            continue
        ofile.write(ofname + "\n")
    ofile.close()


elif action == "replicate":
    replicate("to-replica.txt", "T2_EE_Estonia", "/store/user/jpata/tth/" + version)



