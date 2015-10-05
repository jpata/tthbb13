print "loaded heppy_crab_fake_pset.py"
import FWCore.ParameterSet.Config as cms
process = cms.Process('FAKE')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("/store/user/jpata/VHBBHeppyV12/TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBB_HEPPY_V12_TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/150723_083110/0000/tree_60.root___0___5000"
))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)
