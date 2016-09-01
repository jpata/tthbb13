"""
We want the Lumi of our data.

Use the BRILCALC tool [1]
which currently only runs on lxplus. 

Prerequisite:
Install brilcalc for your lxplus account following the instructions at
[1].

What this script does:
- create a temporary directory
- gather all the json files for which we want the lumi calculated
- add a script to be executed on lxplus
- scp the temp directory to lxplus
- remote execute the script
- and copy back the output
- and display the lumis

[1] http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html#brilcalc]

"""

import os
import sys
import shutil
import subprocess

lxplus_username = "gregor"
dataset_name = "Aug29c"

processes = ["SingleMuon",
             "SingleElectron",
             "MuonEG",
             "DoubleEG",
             "DoubleMuon",
             "BTagCSV",
] 

dataset_base = "src/TTH/MEAnalysis/gc/datasets/"
tmpdir_name = "LUMICALC_TEMP"


# Prepare a new and empty temp directory
if os.path.isdir(tmpdir_name):
    shutil.rmtree(tmpdir_name)
os.mkdir(tmpdir_name)

# Copy all the json files there
for process in processes:
    shutil.copy(
        os.path.join(os.environ["CMSSW_BASE"], dataset_base, dataset_name, process + ".json"),
        tmpdir_name)

# Now build the shell script
out = open(os.path.join(tmpdir_name, "runme.sh"), "w")
out.write("export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH\n")
for process in processes:
    out.write('brilcalc lumi -b "STABLE BEAMS" --normtag=/afs/cern.ch/user/l/lumipro/public/normtag_file/normtag_DATACERT.json -i {0}.json -u /pb -o {0}.out\n'.format(process))
out.close()

# scp to lxplus
scp_command = ["scp", "-r", tmpdir_name, lxplus_username + "@lxplus.cern.ch:"]
print subprocess.Popen(scp_command, stdout=subprocess.PIPE).communicate()[0]

# remote execute
print "Next command is remote execute - this may take a while"
run_command = ["ssh", lxplus_username + "@lxplus.cern.ch", "cd {0}; bash runme.sh".format(tmpdir_name)]
print subprocess.Popen(run_command, stdout=subprocess.PIPE).communicate()[0]

# get back the output
scp_back_command = ["scp", "-r", lxplus_username + "@lxplus.cern.ch:"+tmpdir_name, tmpdir_name+"_OUT"]
print subprocess.Popen(scp_back_command, stdout=subprocess.PIPE).communicate()[0]

# and analyze it
for process in processes:
    inf = open(os.path.join(tmpdir_name+"_OUT", process + ".out"), "r")
    
    # Look for:
    # #Summary:
    # #nfill,nrun,nls,ncms,totdelivered(/pb),totrecorded(/pb)
    # #66,269,101502,101495,12165.673,11629.565
    # and extract the totrecorded
    while True:
        line1 = inf.readline()
        if "Summary" in line1:
            line2 = inf.readline()
            line3 = inf.readline().strip()        
            print "'{0}': {1},".format(process,line3.split(",")[-1])
            break


            
