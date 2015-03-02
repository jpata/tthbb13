from TTH.MEAnalysis.samples_v1 import *

#basepath = "/home/joosep/mac-docs/tth/data/ntp/"
#basepath = "root://cmsxrootd.fnal.gov/"
basepath = "/home/joosep/v9/"

samples = cms.VPSet([
#tt + jets
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        nickName = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        color    = cms.int32(1),
        perJob   = cms.uint32(100000),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([basepath + "tree_1.root"]),
        isMC     = cms.bool(True)
    ),
#tt + H
    #Spring14
    cms.PSet(
        skip     = cms.bool(True),
        name     = cms.string('tth_hbb_13tev'),
        nickName = cms.string('tth_hbb_13tev'),
        color    = cms.int32(2),
        xSec     = cms.double(xsec[("tthbb", "13TeV")]),
        nGen     = cms.int64(-1),
        perJob   = cms.uint32(1000),
        subFiles = cms.vstring([]),
        isMC     = cms.bool(True)
    ),
])
