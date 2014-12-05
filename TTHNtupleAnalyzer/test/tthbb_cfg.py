#a simple test config to run on a ttbar sample
#used for scram b runtests (automatic testing)
from TTH.TTHNtupleAnalyzer.Main_cfg import *

process.source.fileNames = cms.untracked.vstring([
	'/store/mc/Spring14miniaod/TTbarH_HToBB_M-125_13TeV_pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/0E97DD3E-2209-E411-8A04-003048945312.root'
])
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))
process.TFileService.fileName = "tthbb_step1.root"
