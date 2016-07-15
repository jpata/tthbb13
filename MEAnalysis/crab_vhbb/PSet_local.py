import FWCore.ParameterSet.Config as cms
import os

process = cms.Process("FAKE")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        os.environ["FILE_NAMES"].split()
    ),
    skipEvents = cms.untracked.uint32(int(os.environ["SKIP_EVENTS"]))
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(int(os.environ["MAX_EVENTS"]))
)
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('tree.root')
)


process.out = cms.EndPath(process.output)


