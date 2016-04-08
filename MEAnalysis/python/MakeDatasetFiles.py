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

import argparse
parser = argparse.ArgumentParser(description='Prepares dataset lists from DAS')
parser.add_argument('--version', action="store", help="DAS pattern to search, also the output directory")
parser.add_argument('--datasetfile', action="store", help="Input file with datasets")
args = parser.parse_args()

version = args.version

# Create directory for version under output_base
outdir = os.path.join(output_base, version)

if not os.path.exists(outdir):
    os.makedirs(outdir)

########################################
# Get List of Datasets
########################################

#no specified input dataset list
if not args.datasetfile:
    datasets_json = subprocess.Popen(["python",
                                    das_client, 
                                    "--format=json",
                                    "--limit=0",
                                    '--query=dataset dataset=/*/*{0}*/USER instance=prod/phys03'.format(version)], 
                                    stdout=subprocess.PIPE).stdout.read()
    
    datasets_di = json.loads(datasets_json)
    datasets = [
        d["dataset"][0]["name"] for d in datasets_di["data"]
    ]
    
    print "Got {0} datasets".format(len(datasets))
    
    ds_list = []
    dupe = False
    for dataset in datasets:
        print dataset
        ds_name = dataset.split("/")[1]
        if ds_name in ds_list:
            dupe = True
        ds_list += [ds_name]
    if dupe:
        raise Exception("Found duplicate datasets, please disambiguate manually")
else:
    datasets = filter(
        lambda x: len(x)>0,
        map(lambda x: x.strip(),
            open(args.datasetfile).readlines()
        )
    )
########################################
# And add .txt for each of them
########################################

samples_processed = []
for ds in datasets:

    print "Doing", ds
    
    # Extract sample
    # Example:
    # /TTTo2L2Nu_13TeV-powheg/jpata-VHBBHeppyV21_tthbbV6_TTTo2L2Nu_13TeV-powheg__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1-827a43512a0ceecb1e2aee5987443e5a/USER
    # Yields:
    # sample = TTTo2L2Nu_13TeV-powheg
    sample  = ds.split("/")[1]
    if sample in samples_processed:
        raise Exception("Duplicate sample {0}".format(sample))
    samples_processed += [sample]
    
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

    



    
