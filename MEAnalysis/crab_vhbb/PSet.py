print "loaded heppy_crab_fake_pset.py"
import FWCore.ParameterSet.Config as cms
process = cms.Process('FAKE')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("root://xrootd.ba.infn.it//store/data/Run2015D/SingleElectron/MINIAOD/16Dec2015-v1/20000/00050EF1-F9A6-E511-86B2-0025905A48D0.root"),
    lumisToProcess = cms.untracked.VLuminosityBlockRange("1:1954-1:1954")
)
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)
