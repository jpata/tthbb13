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

# First create the ungroomed CA08 and CA15 fatjet collections:

# CA, R=0.8, pT > 200 GeV
process.ca08PFJetsCHS = cms.EDProducer(
        "FastjetJetProducer",
        PFJetParameters,
        AnomalousCellParameters,
        jetAlgorithm = cms.string("CambridgeAachen"),
        rParam       = cms.double(0.8),
    )
process.ca08PFJetsCHS.src      = cms.InputTag("chs")
process.ca08PFJetsCHS.jetPtMin = cms.double(200)


# CA, R=1.5, pT > 200 GeV
process.ca15PFJetsCHS = cms.EDProducer(
        "FastjetJetProducer",
        PFJetParameters,
        AnomalousCellParameters,
        jetAlgorithm = cms.string("CambridgeAachen"),
        rParam       = cms.double(1.5),
    )
process.ca15PFJetsCHS.src      = cms.InputTag("chs")
process.ca15PFJetsCHS.jetPtMin = cms.double(200)


# Add grooming for the CA08 and CA15 fatjets
process.ca08PFJetsCHSFiltered = process.ca08PFJetsCHS.clone(
    useFiltering = cms.bool(True),
    nFilt = cms.int32(3),
    rFilt = cms.double(0.3),
    useExplicitGhosts = cms.bool(True),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets")
    )

process.ca08PFJetsCHSPruned = process.ca08PFJetsCHS.clone(
    cms.PSet(nFilt = cms.int32(2),
             zcut = cms.double(0.1),
             rcut_factor = cms.double(0.5)),
    usePruning = cms.bool(True),
    useExplicitGhosts = cms.bool(True),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets")
    )

process.ca08PFJetsCHSTrimmed = process.ca08PFJetsCHS.clone(
    useTrimming = cms.bool(True),
    rFilt = cms.double(0.2),
    trimPtFracMin = cms.double(0.03),
    useExplicitGhosts = cms.bool(True)
    )

process.ca15PFJetsCHSFiltered = process.ca15PFJetsCHS.clone(
    useFiltering = cms.bool(True),
    nFilt = cms.int32(3),
    rFilt = cms.double(0.3),
    useExplicitGhosts = cms.bool(True),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets")
    )

process.ca15PFJetsCHSPruned = process.ca15PFJetsCHS.clone(
    cms.PSet(nFilt = cms.int32(2),
             zcut = cms.double(0.1),
             rcut_factor = cms.double(0.5)),
    usePruning = cms.bool(True),
    useExplicitGhosts = cms.bool(True),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets")
    )

process.ca15PFJetsCHSTrimmed = process.ca15PFJetsCHS.clone(
    useTrimming = cms.bool(True),
    rFilt = cms.double(0.2),
    trimPtFracMin = cms.double(0.03),
    useExplicitGhosts = cms.bool(True)
    )


# Nsubjettiness for groomed and ungroomed fatjets
process.NjettinessCA08 = cms.EDProducer("NjettinessAdder",
                                        src=cms.InputTag("ca08PFJetsCHS"),
                                        cone=cms.double(0.8),
                                        Njets = cms.vuint32(1,2,3),
                            )

process.NjettinessCA08Filtered = cms.EDProducer("NjettinessAdder",
                                                src=cms.InputTag("ca08PFJetsCHSFiltered"),
                                                cone=cms.double(0.8),
                                                Njets = cms.vuint32(1,2,3),
                            )

process.NjettinessCA08Pruned = cms.EDProducer("NjettinessAdder",
                                                src=cms.InputTag("ca08PFJetsCHSPruned"),
                                                cone=cms.double(0.8),
                                                Njets = cms.vuint32(1,2,3),
                            )

process.NjettinessCA08Trimmed = cms.EDProducer("NjettinessAdder",
                                                src=cms.InputTag("ca08PFJetsCHSTrimmed"),
                                                cone=cms.double(0.8),
                                                Njets = cms.vuint32(1,2,3),
                            )

process.NjettinessCA15 = cms.EDProducer("NjettinessAdder",
                                        src=cms.InputTag("ca15PFJetsCHS"),
                                        cone=cms.double(1.5),
                                        Njets = cms.vuint32(1,2,3),
                            )

process.NjettinessCA15Filtered = cms.EDProducer("NjettinessAdder",
                                                src=cms.InputTag("ca15PFJetsCHSFiltered"),
                                                cone=cms.double(1.5),
                                                Njets = cms.vuint32(1,2,3),
                            )

process.NjettinessCA15Pruned = cms.EDProducer("NjettinessAdder",
                                                src=cms.InputTag("ca15PFJetsCHSPruned"),
                                                cone=cms.double(1.5),
                                                Njets = cms.vuint32(1,2,3),
                            )

process.NjettinessCA15Trimmed = cms.EDProducer("NjettinessAdder",
                                                src=cms.InputTag("ca15PFJetsCHSTrimmed"),
                                                cone=cms.double(1.5),
                                                Njets = cms.vuint32(1,2,3),
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
        fatjetsObjects  = cms.vstring(  ['ca08PFJetsCHS',  'ca08PFJetsCHSFiltered',  'ca08PFJetsCHSPruned',  'ca08PFJetsCHSTrimmed',  'ca15PFJetsCHS',  'ca15PFJetsCHSFiltered',  'ca15PFJetsCHSPruned',  'ca15PFJetsCHSTrimmed'  ]),
        fatjetsNsubs    = cms.vstring(  ['NjettinessCA08', 'NjettinessCA08Filtered', 'NjettinessCA08Pruned', 'NjettinessCA08Trimmed', 'NjettinessCA15', 'NjettinessCA15Filtered', 'NjettinessCA15Pruned', 'NjettinessCA15Trimmed' ]),
        fatjetsBranches = cms.vstring(  ['ca08',           'ca08filtered',           'ca08pruned',           'ca08trimmed',           'ca15',           'ca15filtered',           'ca15pruned',           'ca15trimmed'           ]),
        fatjetsIsBasicJets = cms.vint32([0,                 1,                        1,                      0,                       0,                1,                        1,                      0]),                                           

        httObjects  = cms.vstring(['LooseMultiRHTTJetsCHS']),                                           
        httBranches = cms.vstring(['looseMultiRHTT']),                                           
        
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


process.LooseMultiRHTTJetsCHS = cms.EDProducer(
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
     minCandMass = cms.double(0.),
     maxCandMass = cms.double(1000),
     massRatioWidth = cms.double(100.),
     minM23Cut = cms.double(0.),
     minM13Cut = cms.double(0.),
     maxM13Cut = cms.double(2.),
)


process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = "PLS170_V7AN1"

process.p = cms.Path(
        process.chs *

        process.ca08PFJetsCHS *
        process.ca15PFJetsCHS *

        process.ca08PFJetsCHSFiltered * 
        process.ca08PFJetsCHSPruned   * 
        process.ca08PFJetsCHSTrimmed  * 

        process.ca15PFJetsCHSFiltered * 
        process.ca15PFJetsCHSPruned   * 
        process.ca15PFJetsCHSTrimmed  * 

        process.NjettinessCA08 *        
        process.NjettinessCA08Filtered *        
        process.NjettinessCA08Pruned *        
        process.NjettinessCA08Trimmed *        

        process.NjettinessCA15 *        
        process.NjettinessCA15Filtered *        
        process.NjettinessCA15Pruned *        
        process.NjettinessCA15Trimmed *        

	process.LooseMultiRHTTJetsCHS * 
       
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

