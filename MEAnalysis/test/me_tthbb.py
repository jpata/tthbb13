import os
from TTH.MEAnalysis.MEAnalysis_cfg import *

process.fwliteInput.pathToFile = cms.string(os.environ["CMSSW_BASE"])

process.fwliteInput.ordering = cms.string("")

process.fwliteInput.samples = cms.VPSet(
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tthbb_step1'),
        nickName = cms.string('TTHBB'),
        color    = cms.int32(1),
        bdisc    = cms.int32(1), #use the old CSV discriminant
        xSec     = cms.double(1.0)
    )
)
process.fwliteInput.debug = cms.untracked.int32(0)
process.fwliteInput.evLimits = cms.vint32(0, -1)
process.fwliteInput.ntuplizeAll = cms.untracked.int32(1)
process.fwliteInput.outFileName = cms.string("tthbb_step2.root")
process.fwliteInput.switchoffOL = cms.untracked.int32(0)
process.fwliteInput.speedup     = cms.untracked.int32(0)
