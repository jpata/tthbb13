print "loaded heppy_crab_fake_pset.py"
import FWCore.ParameterSet.Config as cms
process = cms.Process('FAKE')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:///shome/jpata/tth/sw-76/CMSSW/src/TTH/MEAnalysis/crab_vhbb/00F20861-40B8-E511-B593-001EC9B2189E.root'),
    lumisToProcess = cms.untracked.VLuminosityBlockRange("1:1954-1:1954")
)
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)
