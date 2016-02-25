import os
import FWCore.ParameterSet.Config as cms
from TTH.MEAnalysis.samples_base import *
import ROOT

path1 = "/scratch/jpata/gfalFS/T2_CH_CSCS/pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/tthbb13/VHBBHeppyV20/Feb22_updatebdt_withme/"
getSize = False

def fnTransform(fn):
    return fn.replace(
        "/scratch/jpata/gfalFS/T2_CH_CSCS/pnfs/lcg.cscs.ch/cms/trivcat",
        "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat"
    )

samples = os.listdir(path1)
print samples

sampfiles = {}
samples_dict = {}

samp_py = open("samples.py", "w")
samp_py.write("samples_dict = {\n")
for sample in samples:
    samplepath = os.path.join(path1, sample)
    sampfiles = []
    for (dirpath, dirnames, filenames) in os.walk(samplepath):
        if "failed" in dirpath:
            continue
        filenames = filter(lambda x: ".root" in x, filenames)
        sampfiles += map(lambda x: os.path.join(dirpath, x), filenames)
    sampfiles = map(lambda x: x.replace("/hdfs/cms", ""), sampfiles)
    isMC = True
    
    outfile = open(sample+".dat", "w")
    outfile.write("[{0}]\n".format(sample))
    
    nGenEff = 0
    for f in sampfiles:
        if len(f) > 240:
            #we can't submit crab jobs on filenames that are too long, need to catch them early
            #https://github.com/dmwm/CRABServer/issues/5146
            #raise Exception("sample {0} has long filename {1}".format(sample, f))
            pass
        #pfn = lfn_to_pfn("file://" + f)
        pfn = fnTransform(f) 
        tf = ROOT.TFile.Open(pfn)
        if (tf == None or tf is None or tf.IsZombie()):
            print "could not read file {0}, {1}, {2}".format(pfn, tf)
        else:
            tt = tf.Get("tree")
            if (tt == None):
                print "could not read tree"
            else:
                outfile.write("{0} = {1}\n".format(f, int(tt.GetEntries())))
                if getSize:
                    hcn = tf.Get("CountNegWeight")
                    hcp = tf.Get("CountPosWeight")
                    if hcn == None or hcp == None:
                        continue
                    nGenEff += hcp.GetBinContent(1) - hcn.GetBinContent(1)
        tf.Close()
    outfile.close()

    if "Single" in sample or "Double" in sample or "MuonEG" in sample:
        isMC = False
    
    nick = samples_nick.get(sample, sample)
    x = """    
        "{0}": cms.PSet(
            name     = cms.string("{0}"),
            nickname = cms.string("{2}"),
            xSec     = cms.double(xsec_sample.get("{0}", 1)),
            nGen     = cms.int64({3}),
            skip     = cms.bool(False),
            isMC     = cms.bool({1}),
            subFiles = cms.vstring(get_files("{0}")),
        ),
    """.format(sample, isMC, nick, int(nGenEff))
    samp_py.write(x)

samp_py.write("}\n")
samp_py.close()
