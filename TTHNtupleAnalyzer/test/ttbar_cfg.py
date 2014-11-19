#a simple test config to run on a ttbar sample
#used for scram b runtests (automatic testing)
from TTH.TTHNtupleAnalyzer.Main_cfg import *

process.source.fileNames = cms.untracked.vstring([
		'/store/results/top/StoreResults/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/USER/Spring14dr_PU_S14_POSTLS170_V6AN1_miniAOD706p1_814812ec83fce2f620905d2bb30e9100-v2/00000/0012F41F-FA17-E411-A1FF-0025905A48B2.root'
])
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
