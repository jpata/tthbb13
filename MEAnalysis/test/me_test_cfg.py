import os
from TTH.MEAnalysis.MEAnalysis_cfg import *

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
process.fwliteInput.debug = cms.untracked.int32(4)
process.fwliteInput.evLimits = cms.vint32(0, 100)
