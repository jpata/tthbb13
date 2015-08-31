print "loaded heppy_crab_fake_pset.py"
import FWCore.ParameterSet.Config as cms
process = cms.Process('FAKE')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring("root://xrootd-cms.infn.it///store/user/jpata/VHBBHeppyV12/ttHTobb_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V12_ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/150723_082022/0000/tree_1.root::0::1000"))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)
