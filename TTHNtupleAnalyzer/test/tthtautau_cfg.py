#a simple test config to run on a ttbar sample
#used for scram b runtests (automatic testing)
from TTH.TTHNtupleAnalyzer.Main_cfg import *

process.source.fileNames = cms.untracked.vstring([
	'/store/mc/Phys14DR/TTbarH_HToTauTau_M-125_13TeV_amcatnlo-pythia8-tauola/MINIAODSIM/AVE30BX50_tsg_PHYS14_ST_V1-v1/10000/14E130D0-43A8-E411-BBFD-C4346BC08440.root'
])
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))
process.TFileService.fileName = "tthtautau_step1.root"
