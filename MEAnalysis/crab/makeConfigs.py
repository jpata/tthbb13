#!/usr/bin/env python
import os, sys

dname_dict = {
    "ttHTobb_M125_13TeV_powheg_pythia8_2000": "/ttHTobb_M125_13TeV_powheg_pythia8/arizzi-VHBB_HEPPY_V14_ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1-c2fe7dabe0847de4b91e3409460df03d/USER",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000": "/TT_TuneCUETP8M1_13TeV-powheg-pythia8/arizzi-VHBB_HEPPY_V14_TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1-c768f5d1cdee91c788d0c4b7fd93ee3e/USER"
}

username = os.getenv("USER")
if __name__ == "__main__":
    githash = sys.argv[1]
    datasets = sys.argv[2:]
    
    for dataset in datasets:
        infile = open("heppy_crab_config.py").read()
        if not os.path.isfile(dataset):
            raise FileError("could not find file list corresponding to dataset={0}".format(dataset)) 
        dname = dataset.split("/")[-1]
        dname = dname[0:dname.find(".dat")]
        #get the corresponding DAS dataset name

        infile = infile.replace("DATASET", '"datasets/' + dname + '.dat"')
        infile = infile.replace("FULLDAS", '"' + dname_dict[dname] + '"')
        infile = infile.replace("DNAME", '"' + dname + '"')
        infile = infile.replace("USERNAME", username)
        infile = infile.replace("GITHASH", githash)
        of = open("cfg_{0}.py".format(dname), "w")
        of.write(infile)
        of.close()
        print "wrote {0} to {1}".format(dname, of.name)
    
