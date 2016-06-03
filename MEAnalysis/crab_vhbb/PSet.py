print "loaded heppy_crab_fake_pset.py"
import FWCore.ParameterSet.Config as cms
import PhysicsTools.PythonAnalysis.LumiList as LumiList
process = cms.Process('FAKE')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("file:///scratch/jpata/C2EC599F-7C1B-E611-BCA9-B083FECF837B.root"),
    lumisToProcess = LumiList.LumiList(filename = 'file.json').getVLuminosityBlockRange()
)
process.source.lumisToProcess = process.source.lumisToProcess[0:1]
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)
