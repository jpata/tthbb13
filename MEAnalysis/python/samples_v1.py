import FWCore.ParameterSet.Config as cms
import glob, os

#Set the default file path (access via xrootd)
pathToFile    = cms.string("root://cmsxrootd.fnal.gov//store/user/jpata/tth/s1_eb733a1/")

#Configure the site-specific file path
import os
hn = os.environ["HOSTNAME"]
vo = os.environ.get("VO_CMS_DEFAULT_SE", "")
if "kbfi" in hn or "comp-" in hn or "kbfi" in vo:
    pfPath = "/hdfs/cms/store/user/jpata/tth/s1_eb733a1/"
    lfPrefix = "file:/"
elif "psi" in hn or "psi" in vo:
    pfPath = "/pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/s1_eb733a1/"
    lfPrefix = "dcap://t3se01.psi.ch:22125/"
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
        nGen     = cms.int64(-1),
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
        nGen     = cms.int64(-1),
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets_13tev_pythia8_pu20bx25_phys14'),
        nickName = cms.string('ttjets_13tev_pythia8_pu20bx25_phys14'),
        color    = cms.int32(1),
        perJob   = cms.uint32(100000),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(-1),
    ),

#tt + H
    #Spring14
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev'),
        nickName = cms.string('tth_hbb_13tev'),
        color    = cms.int32(2),
        xSec     = cms.double(xsec[("tthbb", "13TeV")]),
        nGen     = cms.int64(-1),
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
        nGen     = cms.int64(-1),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(0), #1 - bd_csv, 0 - bd_cisvv2
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev_amcatnlo_pu40bx50_phys14'),
        nickName = cms.string('tth_hbb_13tev_amcatnlo_pu40bx50_phys14'),
        color    = cms.int32(2),
        xSec     = cms.double(xsec[("tthbb", "13TeV")]),
        nGen     = cms.int64(-1),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(0), #1 - bd_csv, 0 - bd_cisvv2
    ),
)

if __name__=="__main__":


    for (i, s) in enumerate(samples):
        samp_path = pfPath + "/" + s.name.value()

        mdfile = samp_path + ".dat"
        print "looking for metadata in", mdfile
        if os.path.isfile(mdfile):
            print "Metadata found, getting list of files"
            metadata = open(mdfile)
            try:
                fs = map(lambda x: x.strip(), metadata.readlines())
            except Exception as e:
                print "ERROR: could not read metadata", e
                fs = []                              
            samples[i].subFiles = cms.vstring(map(
                lambda x: lfPrefix + x, fs)
            )
        else:
            print "Metadata not found, assuming merged file"
            samples[i].subFiles = cms.vstring([
                pathToFile.value() + "/" + samplePrefix.value() + s.name.value() + ".root"]
            )


    for s in samples:
        print "[/{0}]".format(s.nickName.value())
        for sf in s.subFiles:
            print sf
