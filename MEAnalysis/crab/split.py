#!/usr/bin/env python
import sys, os

def prepare_crab_list(infile, dataset, perjob, outfile):
    """
    makes a crab-compatible file list.
    events per file are specified in the filename with a separator: ___
    """
    curname = None
    datasets = {}
    for line in open(infile).readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        if line.startswith("["):
            if curname:
                datasets[curname] = datafiles
            datafiles = []
            curname = line[1:-1]
        elif "root" in line:
            l0, l1 = line.split("=") 
            datafiles += [(l0.strip(), int(l1.strip()))]
   
    #add last dataset
    datasets[curname] = datafiles
    print "datasets:", list(datasets.keys())
   
    #get total number of events in chosen dataset
    try:
        mydata = datasets[dataset]
    except Exception as e:
        print "ERROR: could not find dataset", dataset
        raise e
    total = sum([d[1] for d in mydata])
    l = []
    for df, nd, in mydata:
        cur = 0
        while cur < nd-perjob:
            l += [(df, cur, perjob)]
            cur += perjob
    of = open(outfile, "w")
    n = 0
    for fn, cur, perjob in l:
        of.write("{0}___{1}___{2}\n".format(fn, cur, perjob))
        n += 1
    of.close()
    print "wrote {0} lines to {1}".format(n, outfile)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "{0} ../gc/datasets/infile.dat name_of_dataset datasets/name_of_dataset.dat events_per_job".format(sys.argv[0])
        sys.exit(1) 
    infile = sys.argv[1]
    dataset = sys.argv[2]
    outfile = sys.argv[3]
    perjob = int(sys.argv[4])
    
    prepare_crab_list(infile, dataset, perjob, outfile)
