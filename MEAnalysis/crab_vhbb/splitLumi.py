#!/usr/bin/env python
#This script downloads and splits the ttH sync files into pieces for easy parallel processing
from FWCore.PythonUtilities.LumiList import LumiList
import sys, subprocess
import os, multiprocessing

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def makeLumiBlocks(in_lumi_file, outdir, chunksize=5): 
    ll = LumiList(filename=in_lumi_file)
    lumis = ll.getLumis()
    nblock = 0
   
    blocks = []
    for lumiblock in chunks(lumis, chunksize):
        nblock += 1
        ll2 = LumiList(lumis=lumiblock)
        fn = outdir + "/block_{0}.json".format(nblock)
        of = open(fn, "w")
        of.write(str(ll2))
        of.close()
        blocks += [fn]
    return blocks

def getLumisInFiles(filenames):
    lumis = subprocess.Popen(
        ["edmLumisInFiles.py"] + filenames,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.read()
    return lumis

def getLumiListInFiles(filenames):
    lumis = getLumisInFiles(filenames)
    of = open("lumis.json", "w")
    of.write(lumis)
    of.close()
    return LumiList(filename="lumis.json")

def pickEvents(filenames, lumifile, outputFile):
    subprocess.Popen(
        ["cmsRun", "pickEvents_cfg.py", "inputFiles="+",".join(filenames),
        "lumifile=" + lumifile, "outputFile="+outputFile],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout.read()
    return outputFile

def pickEvents_mp(args):
    return pickEvents(*args)

if __name__ == "__main__":
    base_out = "/scratch/jpata/tth_sync"
    dataset = sys.argv[1]
    files = sys.argv[2:]
    print dataset
    lumis = getLumisInFiles(files)
    of = open("lumis.json", "w")
    of.write(lumis)
    of.close()
    outdir = os.path.join(base_out, dataset)
    os.makedirs(outdir)
    lumiblocks = makeLumiBlocks("lumis.json", outdir)

    print "picking events"
    #pick events in parallel
    args = []
    for nlumi, lumi in enumerate(lumiblocks):
        args += [(files, lumi, "{0}/block_{1}.root".format(outdir, nlumi))]
    pool = multiprocessing.Pool(5)
    split_files = pool.map(pickEvents_mp, args)
    pool.close()

    print split_files
