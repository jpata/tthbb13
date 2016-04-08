print "loaded heppy_crab_fake_pset.py"
import FWCore.ParameterSet.Config as cms
process = cms.Process('FAKE')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("/store/group/phys_higgs/hbb/ntuples/V16pre/ttHTobb_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V16pre_ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151117_175129/0000/tree_1.root___0___5000")
)
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)
