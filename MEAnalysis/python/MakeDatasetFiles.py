########################################
# Imports
########################################

import os
import sys
import pdb
import json
import subprocess


########################################
# Initialize
########################################

das_client = "../crab_vhbb/das_client.py"
output_base = "../gc/datasets"

if not len(sys.argv)==2:
    print "Wrong number of command line arguments"
    print "Example: python {0} VHBBHeppyV21_tthbbV6".format(sys.argv[0])
    sys.exit()
else:
    version = sys.argv[1]
    
# Create directory for version under output_base
outdir = os.path.join(output_base, version)

if not os.path.exists(outdir):
    os.makedirs(outdir)


########################################
# Get List of Datasets
########################################
    
datasets_json = subprocess.Popen(["python",
                                  das_client, 
                                 "--format=json", 
                                  '--query=dataset dataset=/*/*{0}*/USER'.format(version)], 
                                 stdout=subprocess.PIPE).stdout.read()

print datasets_json

datasets_di = json.loads(datasets_json)
datasets = datasets_di["data"][0]["hints"][0]["results"][0]["examples"]

print "Got {0} datasets".format(len(datasets))


########################################
# And add .txt for each of them
########################################

for ds in datasets:

    print "Doing", ds
    
    # Extract sample
    # Example:
    # /TTTo2L2Nu_13TeV-powheg/jpata-VHBBHeppyV21_tthbbV6_TTTo2L2Nu_13TeV-powheg__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1-827a43512a0ceecb1e2aee5987443e5a/USER
    # Yields:
    # sample = TTTo2L2Nu_13TeV-powheg
    sample  = ds.split("/")[1]

    ofile = open(os.path.join(outdir,sample+".txt"),"w")

    ofile.write("[{0}]\n".format(sample))
        
    files_json = subprocess.Popen(["python",
                                   das_client, 
                                   '--format=json',
                                   '--limit=0',
                                   '--query=file dataset=' + ds + r' instance=prod/phys03'], 
                                  stdout=subprocess.PIPE).stdout.read()
    
    files_di = json.loads(files_json)

    print "Got {0} files".format(len(files_di['data']))

    for f in  files_di['data']:
        name    = f["file"][0]["name"]
        nevents = f["file"][0]["nevents"]        
        ofile.write("{0} = {1}\n".format(name, nevents))
    ofile.close()

    



    

