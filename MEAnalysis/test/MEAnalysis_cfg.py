from TTH.MEAnalysis.MEAnalysis_cfg import *
import os

process.fwliteInput.evLimits = cms.vint32([0, -1])
process.fwliteInput.verbose = cms.bool(False)
process.fwliteInput.printout = cms.untracked.int32(1)
process.fwliteInput.debug = cms.untracked.int32(4)
process.fwliteInput.speedup = cms.untracked.int32(1)
process.fwliteInput.fixNumEvJob = cms.untracked.int32(0)

process.fwliteInput.pathToFile = cms.string(os.environ["CMSSW_BASE"])
process.fwliteInput.ordering = cms.string("")
process.fwliteInput.samples = cms.VPSet(
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('output'),
        nickName = cms.string('TTJets'),
        color    = cms.int32(1),
        xSec     = cms.double(1.0)
    )
)
