#!/usr/bin/env python
import os, sys

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
        infile = infile.replace("FULLDAS", '"' + dname + '"')
        infile = infile.replace("DNAME", '"' + dname + '"')
        infile = infile.replace("USERNAME", username)
        infile = infile.replace("GITHASH", githash)
        of = open("cfg_{0}.py".format(dname), "w")
        of.write(infile)
        of.close()
        print "wrote {0} to {1}".format(dname, of.name)
    
