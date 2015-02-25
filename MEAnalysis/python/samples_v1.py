import FWCore.ParameterSet.Config as cms
import glob, os
import ConfigParser

#Set the default file path (access via xrootd)
pathToFile    = cms.string("root://cmsxrootd.fnal.gov//store/user/jpata/tth/s1_eb733a1/")

#Configure the site-specific file path
import os
hn = os.environ["HOSTNAME"]
vo = os.environ.get("VO_CMS_DEFAULT_SE", "")

def pfn_to_lfn(fn):
    return fn[fn.find("/store"):]


if "kbfi" in hn or "comp-" in hn or "kbfi" in vo:
    storepath = "/hdfs/cms/"
    pfPath = "/hdfs/cms/store/user/jpata/tth/s1_eb733a1/"
    lfPrefix = "file://"
    def lfn_to_pfn(fn):
        return "file:///hdfs/cms" + fn
elif "psi" in hn or "psi" in vo:
    pfPath = "/pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/s1_eb733a1/"
    lfPrefix = "dcap://t3se01.psi.ch:22125/"
    def lfn_to_pfn(fn):
        return "dcap://t3se01.psi.ch:22125/pnfs/psi.ch/cms/trivcat" + fn
else:
    print "Warning: host '{0}' VO '{1}' is unknown, using xrootd".format(hn, vo)
    pfPath = "/store/user/jpata/tth/s1_eb733a1/"
    lfPrefix = "root://cmsxrootd.fnal.gov/"

pathToFile = cms.string(lfPrefix + pfPath)

samplePrefix = cms.string("TTHbb_s1_eb733a1_")

#List all the step1 samples

#Cross-sections from
# $t \bar{t} + \mathrm{jets}$ - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, $M_{top} = 172.5$ GeV
# ttH - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV, $M_H = 125.0$ GeV
xsec = {}
xsec[("ttjets", "8TeV")] = 252.89
xsec[("ttjets", "13TeV")] = 508.5

xsec[("tthbb", "8TeV")] = 0.1302*0.569

#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#s_13_0_TeV
xsec[("tthbb", "13TeV")] = 0.5085*0.569

samples = cms.VPSet(

#tt + jets
    #Spring14
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets_13tev'),
        nickName = cms.string('ttjets_13tev'),
        color    = cms.int32(1),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(25360410),
        perJob   = cms.uint32(100000),
        bdisc    = cms.int32(1), #1 - bd_csv, 0 - bd_cisvv2
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        nickName = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        color    = cms.int32(1),
        perJob   = cms.uint32(100000),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(25405611),
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets_13tev_pythia8_pu20bx25_phys14'),
        nickName = cms.string('ttjets_13tev_pythia8_pu20bx25_phys14'),
        color    = cms.int32(1),
        perJob   = cms.uint32(100000),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(2861229),
    ),

#tt + H
    #Spring14
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev'),
        nickName = cms.string('tth_hbb_13tev'),
        color    = cms.int32(2),
        xSec     = cms.double(xsec[("tthbb", "13TeV")]),
        nGen     = cms.int64(97520),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(1), #1 - bd_csv, 0 - bd_cisvv2
    ),
#Old Spring14 sample
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev_5b21f5f'),
        nickName = cms.string('tth_hbb_13tev_5b21f5f'),
        color    = cms.int32(2),
        xSec     = cms.double(xsec[("tthbb", "13TeV")]),
        nGen     = cms.int64(97520),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(1), #1 - bd_csv, 0 - bd_cisvv2
    ),

    #Phys14
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev_amcatnlo_pu20bx25_phys14'),
        nickName = cms.string('tth_hbb_13tev_amcatnlo_pu20bx25_phys14'),
        color    = cms.int32(2),
        xSec     = cms.double(xsec[("tthbb", "13TeV")]),
        nGen     = cms.int64(199700),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(0), #1 - bd_csv, 0 - bd_cisvv2
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev_amcatnlo_pu40bx50_phys14'),
        nickName = cms.string('tth_hbb_13tev_amcatnlo_pu40bx50_phys14'),
        color    = cms.int32(2),
        xSec     = cms.double(xsec[("tthbb", "13TeV")]),
        nGen     = cms.int64(199500),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(0), #1 - bd_csv, 0 - bd_cisvv2
    ),
)

def initialize_from_cfgfile(fn, samples):
    fi = open(fn)
    section = None
    data = {}
    for line in fi.readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        if line.startswith("["):
            section = line[1:-1]
            if not data.has_key(section):
                data[section] = []
            else:
                raise Exception("duplicate dataset {0}".format(section))
        elif len(line.split("=")) == 2:
            fn, n = line.split("=")
            fn = fn.strip()
            data[section] += [(fn, int(n))]
    for sample in samples:
        nick = sample.nickName.value()
        if data.has_key(nick):
            sample.subFiles = cms.vstring(
                [lfn_to_pfn(x[0]) for x in data[nick]]
            )
            sample.nGen = cms.int64(
                sum([x[1] for x in data[nick]])
            )

import ROOT
def get_file_size(fn):
    try:
        pfn = lfn_to_pfn(fn)
        tf = ROOT.TFile.Open(pfn)
        if tf==None or tf.IsZombie():
            raise FileError("Could not open file {0}".format(pfn))
        tt = tf.Get("tthNtupleAnalyzer/events")
        if tt==None:
            raise KeyError("Could not get tthNtupleAnalyzer/events from file")

        n = int(tt.GetEntries())
        tf.Close()
        del tf
        print pfn, n
        return n
    except Exception as e:
        print e
        return -1

if __name__=="__main__":

    for (i, s) in enumerate(samples):
        samp_path = pfPath + "/" + s.name.value()

        mdfile = samp_path + ".dat"
        print "looking for metadata in", mdfile
        if os.path.isfile(mdfile):
            print "Metadata found, getting list of files"
            metadata = open(mdfile)
            try:
                pfns = map(lambda x: x.strip(), metadata.readlines())
            except Exception as e:
                print "ERROR: could not read metadata", e
                pfns = []
            #pfns = pfns[1:10]
            lfns = map(pfn_to_lfn , pfns)
            sizes = map(lambda x: get_file_size(x), pfns)
            goodfiles = filter(lambda x: x[1]>0, zip(pfns, sizes))
            samples[i].subFiles = cms.vstring([x[0] for x in goodfiles])
            samples[i].fileSizes = cms.vint32([x[1] for x in goodfiles])

        else:
            print "Metadata not found, assuming merged file"
            samples[i].subFiles = cms.vstring([
                pathToFile.value() + "/" + samplePrefix.value() + s.name.value() + ".root"]
            )
            samples[i].fileSizes = cms.vint32([])

    of = open("step1_{0}.dat".format(vo), "w")

    for s in samples:
        of.write("[{0}]\n".format(s.nickName.value()))
        for (sf, n) in zip(s.subFiles, s.fileSizes):
            of.write("{0} = {1}\n".format(sf, n))
    of.close()
