#!/usr/bin/env python
import os, sys

infile = open("heppy_crab_config.py").read()

username = os.getenv("USER")
if __name__ == "__main__":
    datasets = sys.argv[1:]
    
    for dataset in datasets:
        if not os.path.isfile(dataset):
            raise FileError("could not find file list corresponding to dataset={0}".format(dataset))
        dname = dataset.split("/")[-1]
        dname = dname[0:dname.find(".dat")]
        infile = infile.replace("DATASET", '"' + dname + '"')
        infile = infile.replace("USERNAME", username)
        of = open("cfg_{0}.py".format(dname), "w")
        of.write(infile)
        of.close()
        print "wrote {0} to {1}".format(dname, of.name)
    
