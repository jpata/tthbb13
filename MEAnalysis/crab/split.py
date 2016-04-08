#!/usr/bin/env python
import sys, os

from transferData import dsname_repl

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
            for repls in dsname_repl:
                l0 = l0.replace(repls[0], repls[1])
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
    
    n = 0
    if perjob > 0:
        for df, nd, in mydata:
            cur = 0
            if perjob > nd:
                l += [(df, cur, nd)]
                print "cannot split file {2}: file has {0} but perjob is {1}".format(nd, perjob, df)
            while cur < nd-perjob:
                l += [(df, cur, perjob)]
                cur += perjob
        of = open(outfile, "w")
        for fn, cur, perjob in l:
            fns = "{0}___{1}___{2}\n".format(fn, cur, perjob)
            if len(fns) > 255:
                raise Exception("too long filename: {0}".format(fns))
            of.write(fns)
            n += 1
        of.close()
    else:
        of = open(outfile, "w")
        for df, nd, in mydata:
            l += [df]
            of.write("{0}\n".format(df))
            n += 1
        of.close()
    print "wrote {0} lines to {1}".format(n, outfile)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "{0} ../gc/datasets/infile.dat datasets/name_of_dataset.dat events_per_job".format(sys.argv[0])
        sys.exit(1) 
    infile = sys.argv[1]
    outfile = sys.argv[2]
    perjob = int(sys.argv[3])
    dataset = infile.split("/")[-1].split(".")[0]

    prepare_crab_list(infile, dataset, perjob, outfile)

