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
pathToFile = cms.string(lfPrefix + pfPath)

samplePrefix = cms.string("TTHbb_s1_eb733a1_")

#List all the step1 samples

#Cross-sections from
# $t \bar{t} + \mathrm{jets}$ - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, $M_{top} = 172.5$ GeV
# ttH - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV, $M_H = 125.0$ GeV
samples = cms.VPSet(
#tt + jets
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets_13tev'),
        nickName = cms.string('ttjets_13tev'),
        color    = cms.int32(1),
        xSec     = cms.double(508.5),
        perJob   = cms.uint32(100000),
        bdisc    = cms.int32(1), #1 - bd_csv, 0 - bd_cisvv2
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        nickName = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        color    = cms.int32(1),
        perJob   = cms.uint32(100000),
        xSec     = cms.double(508.5)
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets_13tev_pythia8_pu20bx25_phys14'),
        nickName = cms.string('ttjets_13tev_pythia8_pu20bx25_phys14'),
        color    = cms.int32(1),
        perJob   = cms.uint32(100000),
        xSec     = cms.double(508.5)
    ),

#tt + H
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev'),
        nickName = cms.string('TTHBB125'),
        color    = cms.int32(2),
        xSec     = cms.double(0.1302*0.569),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(1), #1 - bd_csv, 0 - bd_cisvv2
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev_amcatnlo_pu20bx25_phys14'),
        nickName = cms.string('tth_hbb_13tev_amcatnlo_pu20bx25_phys14'),
        color    = cms.int32(2),
        xSec     = cms.double(0.1302*0.569),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(0), #1 - bd_csv, 0 - bd_cisvv2
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev_amcatnlo_pu40bx50_phys14'),
        nickName = cms.string('tth_hbb_13tev_amcatnlo_pu40bx50_phys14'),
        color    = cms.int32(2),
        xSec     = cms.double(0.1302*0.569),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(0), #1 - bd_csv, 0 - bd_cisvv2
    ),
)

#for (i, s) in enumerate(samples):
#    samp_path = pfPath + "/" + s.name.value()
#    if os.path.isfile(samp_path + ".dat"):
#        metadata = open(samp_path + ".dat")
#        fs = map(lambda x: x.strip(), metadata.readlines())
#        #fs = glob.glob(samp_path + "/*.root")
#        samples[i].subFiles = cms.vstring(map(lambda x: lfPrefix + x, fs))
#    else:
#        samples[i].subFiles = cms.vstring([pathToFile.value() + "/" + samplePrefix.value() + s.name.value() + ".root"])
if __name__=="__main__":
    for s in samples:
        print "[/{0}]".format(s.nickName.value())
        for sf in s.subFiles:
            print sf
