#a simple test config to run on a ttbar sample
#used for scram b runtests (automatic testing)
from TTH.TTHNtupleAnalyzer.Taggers_cfg import *

process.source.fileNames = cms.untracked.vstring([
#    'file:///scratch/gregor/TTbarH_HToBB_M-125_13TeV_pythia6_MiniAOD.root',
#    'file:///scratch/gregor/TTJets_MSDecaysCKM_central_Tune4C_13TeV_MiniAOD.root'
#    'file:///scratch/gregor/Phys14DR_ZPrimeToTTJets_M2000GeV_W20GeV_Tune4C_13TeV.root'
#    'file:///scratch/gregor/Phys14_PU20bx25_ZPrimeToTTJets_M2000GeV_W20GeV_Tune4C_13TeV.root'    
#    'file:///scratch/gregor/ZPrimeToTTJets_M1000GeV_W10GeV_PU20bx25_MiniAOD.root'
#    'file:///scratch/gregor/WJetsToLNu_HT-200to400_PU20bx25_MiniAOD.root'
#    'file:///scratch/gregor/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8.root'
#    'file:///scratch/gregor/QCD_Pt-300to470_TuneZ2star_13TeV_pythia6.root'
     'file:///scratch/gregor/zprime_3tev_miniaodv2.root'
#     'file:///scratch/gregor/RunIISpring15DR74_ZprimeToTT_M-1000_W-10_TuneCUETP8M1_13TeV_Asympt50ns.root'    
])

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
process.TFileService.fileName = "ttbar_step1.root"
