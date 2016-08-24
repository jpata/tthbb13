#!/usr/bin/env python
########################################
# Imports
########################################

import os
import sys
import pdb
import json
import subprocess
import time

from FWCore.PythonUtilities.LumiList import LumiList

########################################
# Initialize
########################################

#/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_5/external/slc6_amd64_gcc530/bin/das_client.py
#das_client = os.path.join(
#    os.environ["CMSSW_RELEASE_BASE"],
#    "external",
#    os.environ["SCRAM_ARCH"],
#    "bin",
#    "das_client.py"
#)
das_client = "/afs/cern.ch/user/v/valya/public/das_client.py"
output_base = os.path.join(
    os.environ["CMSSW_BASE"],
    "src/TTH/MEAnalysis/gc/datasets/",
)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Prepares dataset lists from DAS')
    parser.add_argument('--version', action="store", help="DAS pattern to search, also the output directory")
    parser.add_argument('--datasetfile', action="store", help="Input file with datasets")
    parser.add_argument('--instance', action="store", help="DBS instance", default="prod/phys03")
    parser.add_argument('--limit', action="store", help="max files per dataset", default=0)
    parser.add_argument('--debug', action="store", help="debug mode", default=False)
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
        cmds = [ 
            das_client, 
            "--format=json",
            "--limit=0",
            '--query=dataset dataset=/*/*{0}*/USER instance={1}'.format(version, args.instance)
        ]
        if args.debug:
            print " ".join(cmds)
        datasets_json = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout.read()
        if args.debug:
            print datasets_json
        
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
       
        ofile_fn = os.path.join(outdir, sample + ".txt")
        ofile = open(ofile_fn, "w")
    
        ofile.write("[{0}__{1}]\n".format(version, sample))
            
        files_json = subprocess.Popen([
            "python {0} --query='file dataset={1} instance={2}' --format=json --limit={3}".format(
            das_client, ds, args.instance, args.limit)
            ], stdout=subprocess.PIPE, shell=True
        ).stdout.read()
        files_di = json.loads(files_json)
        
        files_run_lumi_json = subprocess.Popen([
            "python {0} --query='file,run,lumi dataset={1} instance={2}' --format=json --limit={3}".format(
            das_client, ds, args.instance, args.limit)
            ], stdout=subprocess.PIPE, shell=True
        ).stdout.read()
        files_run_lumi = json.loads(files_run_lumi_json)
        
        try:
            print "Got {0} files".format(len(files_di['data']))
        except Exception as e:
            print "Could not parse 'data' in output json"
            print files_di
            raise e
        lumis_dict = {}
        for fi in files_run_lumi["data"]:
            fn = fi["file"][0]["name"]
            lumis_dict[fn] = {}
            for run, lumis in zip(fi["run"], fi["lumi"]):
                run_num = run["run_number"]
                if not lumis_dict[fn].has_key(run_num):
                    lumis_dict[fn][run_num] = []
                lumis_dict[fn][run_num] += lumis["number"]

        lumis = []
        for ifile, fi in enumerate(files_di['data']):
            name = None
            try:
                name = fi["file"][0]["name"]
            except Exception as e:
                print "Could not parse file name", fi
                name = None
            
            if name:
                try:
                    nevents = fi["file"][0]["nevents"]
                except Exception as e:
                    print "Could not parse nevents", fi["file"][0]
                    nevents = 0

                tmp_lumis = LumiList(compactList = lumis_dict[name])
                lumis += [tmp_lumis]
                ofile.write("{0} = {1}\n".format(name, nevents))
            #merge lumi files

        #merge lumi files
        total_lumis = LumiList()
        for i in range(len(lumis)):
            total_lumis = total_lumis | lumis[i]
        total_lumis.writeJSON(fileName=ofile_fn.replace(".txt", ".json"))
        #end loop over files

        ofile.close()
        #sleep so as to not overload the DAS server
        time.sleep(60)
