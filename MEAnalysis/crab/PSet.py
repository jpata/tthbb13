print "loaded heppy_crab_fake_pset.py"
import FWCore.ParameterSet.Config as cms
process = cms.Process('FAKE')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("/store/t3groups/ethz-higgs/run2/VHBBHeppyV14/ttHTobb_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V14_ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_084144/0000/tree_1.root___0___500"
))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)
