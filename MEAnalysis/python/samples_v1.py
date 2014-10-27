import FWCore.ParameterSet.Config as cms
samples = cms.VPSet(
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets'),
        nickName = cms.string('TTJets'),
        color    = cms.int32(1),
        xSec     = cms.double(1.0)
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tthbb'),
        nickName = cms.string('TTHBB125'),
        color    = cms.int32(2),
        xSec     = cms.double(1.0)
    ),
)
