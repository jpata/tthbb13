# Tagger_cfg.py
# cmsRun configuration file for producing NTuples for Top & Higgs-Tagging Studies

import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
import os

options = VarParsing('analysis')
options.register ('skipEvents',
	0,
	VarParsing.multiplicity.singleton,
	VarParsing.varType.int,
	"Skip this number of events"
)

process = cms.Process("Demo")
options.parseArguments()

#enable debugging printout
if "TTH_DEBUG" in os.environ:
	process.load("FWCore.MessageLogger.MessageLogger_cfi")
	process.MessageLogger = cms.Service("MessageLogger",
		   destinations=cms.untracked.vstring('cout', 'debug'),
		   debugModules=cms.untracked.vstring('*'),
		   cout=cms.untracked.PSet(threshold=cms.untracked.string('INFO')),
		   debug=cms.untracked.PSet(threshold=cms.untracked.string('DEBUG')),

	)
else:
	process.load("FWCore.MessageService.MessageLogger_cfi")
	process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.source = cms.Source("PoolSource",
	# replace 'myfile.root' with the source file you want to use
	fileNames = cms.untracked.vstring([]),
	skipEvents = cms.untracked.uint32(options.skipEvents)
)

# Select candidates that would pass CHS requirements
# This can be used as input for HTT and other jet clustering algorithms
process.chs = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV"))

# Add stand-alone fat-jet collection 
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
process.ca15PFJetsCHS = cms.EDProducer(
        "FastjetJetProducer",
        PFJetParameters,
        AnomalousCellParameters,
        jetAlgorithm = cms.string("CambridgeAachen"),
        rParam       = cms.double(1.5),
    )
process.ca15PFJetsCHS.src      = cms.InputTag("chs")
process.ca15PFJetsCHS.jetPtMin = cms.double(200)


# Calculate n-subjettiness for stand-alone fatjets
process.Njettiness = cms.EDProducer("NjettinessAdder",
                                    src=cms.InputTag("ca15PFJetsCHS"),
                                    cone=cms.double(1.5)
                            )

process.tthNtupleAnalyzer = cms.EDAnalyzer('TTHNtupleAnalyzer',
	isMC = cms.bool(True),
	vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
	muons = cms.InputTag("slimmedMuons"),
	electrons = cms.InputTag("slimmedElectrons"),
	taus = cms.InputTag("slimmedTaus"),
	jets = cms.InputTag("slimmedJets"),
	genjets = cms.InputTag("slimmedGenJets"),

	packed = cms.InputTag("packedGenParticles"),
	pruned = cms.InputTag("prunedGenParticles"),
	mets = cms.InputTag("slimmedMETs"),
	lhe = cms.InputTag("externalLHEProducer"),

        triggerIdentifiers = cms.vstring([]),
        triggerIdentifiersForMatching = cms.vstring([]),

        # take ca15PFJetsCHS jets, add the Njettiness values and store them as jet_fat
        fatjetsObjects  = cms.vstring(['ca15PFJetsCHS']),
        fatjetsNsubs    = cms.vstring(['Njettiness']),
        fatjetsBranches = cms.vstring(['fat']),

        httObjects  = cms.vstring(['HTTJetsCHS', 'MultiRHTTJetsCHS']),                                           
        httBranches = cms.vstring(['toptagger', 'toptagger2']),                                           
        
	jetMult_min   = cms.untracked.int32(-99),
	jetPt_min     = cms.untracked.double(15.),
	muPt_min_     = cms.untracked.double(15.),
	elePt_min_    = cms.untracked.double(15.),
	tauPt_min_    = cms.untracked.double(15.),

	bits	  = cms.InputTag("TriggerResults","","HLT"),
	objects   = cms.InputTag("selectedPatTrigger"),
	prescales = cms.InputTag("patTrigger"),

	eleIdentifiers = cms.vstring([]),
	tauIdentifiers = cms.vstring([]),
)

process.TFileService = cms.Service("TFileService",
	fileName = cms.string(options.outputFile)
)

process.load('RecoJets.JetProducers.caTopTaggers_cff')

from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.PFJetParameters_cfi import *

process.HTTJetsCHS = cms.EDProducer(
	"HTTTopJetProducer",
	PFJetParameters.clone(src = cms.InputTag('chs'),
						  doAreaFastjet = cms.bool(True),
						  doRhoFastjet = cms.bool(False),
						  jetPtMin = cms.double(100.0)
					   ),
	AnomalousCellParameters,
	algorithm = cms.int32(1),
	jetAlgorithm = cms.string("CambridgeAachen"),
	rParam = cms.double(1.5),
	mode = cms.int32(0),
	minFatjetPt = cms.double(200.),
	minCandPt = cms.double(200.),
	minSubjetPt = cms.double(30.),
	writeCompound = cms.bool(True),
	minCandMass = cms.double(0.),
	maxCandMass = cms.double(20000.),
)

process.MultiRHTTJetsCHS = cms.EDProducer(
     "HTTTopJetProducer",
     PFJetParameters.clone( src = cms.InputTag('chs'),
                            doAreaFastjet = cms.bool(True),
                            doRhoFastjet = cms.bool(False),
                            jetPtMin = cms.double(100.0)
                        ),
     AnomalousCellParameters,
     multiR = cms.bool(True),
     algorithm = cms.int32(1),
     jetAlgorithm = cms.string("CambridgeAachen"),
     rParam = cms.double(1.5),
     mode = cms.int32(4),
     minFatjetPt = cms.double(200.),
     minCandPt = cms.double(200.),
     minSubjetPt = cms.double(30.),
     writeCompound = cms.bool(True),
     minCandMass = cms.double(100.),
     maxCandMass = cms.double(250.),
     massRatioWidth = cms.double(30.),
)


process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = "PLS170_V7AN1"

process.p = cms.Path(
	#process.hepTopTagPFJetsCHS *
	#process.hepTopTagInfos *
        process.chs *
        process.ca15PFJetsCHS *
        process.Njettiness *        
	process.HTTJetsCHS *
	process.MultiRHTTJetsCHS *
	process.tthNtupleAnalyzer
)

if "TTH_DEBUG" in os.environ:
	process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
	process.printTree = cms.EDAnalyzer("ParticleListDrawer",
		maxEventsToPrint = cms.untracked.int32(-1),
		printVertex = cms.untracked.bool(True),
		src = cms.InputTag("prunedGenParticles")
	)
	process.p += process.printTree

