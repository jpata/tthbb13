import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/RunIISpring16MiniAODv2/ttHTobb_M125_13TeV_powheg_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/40000/9C1A9584-A439-E611-AD48-0090FAA573B0.root'),
    lumisToProcess = cms.untracked.VLuminosityBlockRange("1:5002-1:5002", "1:5024-1:5024")
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.output = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('tree.root'),
    logicalFileName = cms.untracked.string('')
)


process.out = cms.EndPath(process.output)
