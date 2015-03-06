from TTH.MEAnalysis.samples_v1 import *

basepath = "/home/joosep/mac-docs/tth/data/ntp/"
sample_version = "VHbb_V9"

samples = cms.VPSet(
#tt + jets
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        nickName = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        color    = cms.int32(1),
        perJob   = cms.uint32(100000),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(25405611),
        subFiles = cms.vstring([basepath + "ttjets_13tev_madgraph_pu20bx25_phys14.root"]),
        isMC     = cms.bool(True)
    ),
# #tt + H
#     #Spring14
#     cms.PSet(
#         skip     = cms.bool(False),
#         name     = cms.string('tth_hbb_13tev'),
#         nickName = cms.string('tth_hbb_13tev'),
#         color    = cms.int32(2),
#         xSec     = cms.double(xsec[("tthbb", "13TeV")]),
#         nGen     = cms.int64(97520),
#         perJob   = cms.uint32(1000),
#         bdisc    = cms.int32(1), #1 - bd_csv, 0 - bd_cisvv2
#     ),
)
