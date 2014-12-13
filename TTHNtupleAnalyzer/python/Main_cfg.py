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

if len(options.inputFiles)==0:
		#options.inputFiles = cms.untracked.vstring(["/store/mc/Spring14miniaod/TTbarH_HToBB_M-125_13TeV_pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/0E97DD3E-2209-E411-8A04-003048945312.root"])
	options.inputFiles = cms.untracked.vstring([
		'/store/mc/Spring14miniaod/TTbarH_HToBB_M-125_13TeV_pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/0E97DD3E-2209-E411-8A04-003048945312.root',
		'/store/mc/Spring14miniaod/TTbarH_HToBB_M-125_13TeV_pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/D0242854-2209-E411-B361-003048C559CE.root'
])


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
	fileNames = cms.untracked.vstring(
		options.inputFiles
	),
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
	rParam	   = cms.double(1.5),
)
process.ca15PFJetsCHS.src	  = cms.InputTag("chs")
process.ca15PFJetsCHS.jetPtMin = cms.double(200)

# Mass Drop Tagger for Higgs
process.ca15PFJetsCHSMDT = process.ca15PFJetsCHS.clone(
		useMassDropTagger = cms.bool(True),
		muCut = cms.double(0.667),
		yCut = cms.double(0.08),
		useExplicitGhosts = cms.bool(True),
		writeCompound = cms.bool(True),
		jetCollInstanceName=cms.string("SubJets"),
)

# Mass Drop Tagger + Filtering for Higgs
process.ca15PFJetsCHSMDTFiltered = process.ca15PFJetsCHS.clone(
		useMassDropTagger = cms.bool(True),
		useFiltering = cms.bool(True),
		muCut = cms.double(0.667),
		yCut = cms.double(0.08),
		nFilt = cms.int32(2),
		rFilt = cms.double(0.3),
		useExplicitGhosts = cms.bool(True),
		writeCompound = cms.bool(True),
		jetCollInstanceName=cms.string("SubJets"))


# Calculate n-subjettiness for stand-alone fatjets
process.Njettiness = cms.EDProducer("NjettinessAdder",
	src=cms.InputTag("ca15PFJetsCHS"),
	cone=cms.double(1.5),
	Njets = cms.vuint32(1,2,3),
)

process.NjettinessMDT = cms.EDProducer("NjettinessAdder",
	src=cms.InputTag("ca15PFJetsCHSMDT"),
	cone=cms.double(1.5),
	Njets = cms.vuint32(1,2,3),
	)

process.NjettinessMDTFiltered = cms.EDProducer("NjettinessAdder",
	src=cms.InputTag("ca15PFJetsCHSMDTFiltered"),
	cone=cms.double(1.5),
	Njets = cms.vuint32(1,2,3),
)

#trigger paths are now saved in ntuple
from TTH.TTHNtupleAnalyzer.triggers_MC_cff import *
#print '**** TRIGGER PATHS ****'
#counter = 0
#for trigger in triggerPathNames:
#	print "[%s] = %s" % (counter, trigger)
#	counter += 1

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

	# take ca15PFJetsCHS jets, add the Njettiness values and store them as jet_fat
	fatjetsObjects  = cms.vstring([  'ca15PFJetsCHS', 'ca15PFJetsCHSMDT', 'ca15PFJetsCHSMDTFiltered']),
	fatjetsNsubs	= cms.vstring([  'Njettiness',	'NjettinessMDT',	'NjettinessMDTFiltered']),
	fatjetsBranches = cms.vstring([  'fat',		   'fatMDT',		   'fatMDTFiltered']),
	fatjetsIsBasicJets = cms.vint32([ 0,			   1,				  1]),

	httObjects  = cms.vstring(['HTTJetsCHS', 'MultiRHTTJetsCHS']),
	httBranches = cms.vstring(['toptagger', 'toptagger2']),

	cmsttObjects  = cms.vstring([]),
	cmsttInfos	= cms.vstring([]),
	cmsttBranches = cms.vstring([]),

	triggerIdentifiers = triggerPathNames,
	#triggerIdentifiersForMatching = cms.vstring([
	#		'HLT_Ele27_WP80_v*',
	#		'HLT_IsoMu24_eta2p1_v*',
	#		'HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*',
	#		]),
	triggerIdentifiersForMatching = triggerPathNames,

	jetMult_min   = cms.untracked.int32(-99),
	jetPt_min	 = cms.untracked.double(15.),
	muPt_min_	 = cms.untracked.double(15.),
	elePt_min_	= cms.untracked.double(15.),
	tauPt_min_	= cms.untracked.double(15.),

	bits	  = cms.InputTag("TriggerResults","","HLT"),
	objects   = cms.InputTag("selectedPatTrigger"),
	prescales = cms.InputTag("patTrigger"),

	eleIdentifiers = cms.vstring([
		'eidLoose',
		'eidRobustHighEnergy',
		'eidRobustLoose',
		'eidRobustTight',
		'eidTight'
	]),
	tauIdentifiers = cms.vstring([
	   # 'againstElectronLoose',
	   # 'againstElectronLooseMVA5',
		'againstElectronMVA5category',
		'againstElectronMVA5raw',
	   # 'againstElectronMedium',
		'againstElectronMediumMVA5',
		'againstElectronTight',
		'againstElectronTightMVA5',
		'againstElectronVLooseMVA5',
	   # 'againstElectronVTightMVA5',
	   # 'againstMuonLoose',
	   # 'againstMuonLoose2',
	   # 'againstMuonLoose3',
		'againstMuonLooseMVA',
	   # 'againstMuonMVAraw',
	   # 'againstMuonMedium',
	   # 'againstMuonMedium2',
		'againstMuonMediumMVA',
	   # 'againstMuonTight',
	   # 'againstMuonTight2',
	   # 'againstMuonTight3',
		'againstMuonTightMVA',
	   # 'byCombinedIsolationDeltaBetaCorrRaw3Hits',
	   # 'byIsolationMVA3newDMwLTraw',
	   # 'byIsolationMVA3newDMwoLTraw',
	   # 'byIsolationMVA3oldDMwLTraw',
	   # 'byIsolationMVA3oldDMwoLTraw',
	   # 'byLooseCombinedIsolationDeltaBetaCorr3Hits',
	   # 'byLooseIsolationMVA3newDMwLT',
	   # 'byLooseIsolationMVA3newDMwoLT',
	   # 'byLooseIsolationMVA3oldDMwLT',
	   # 'byLooseIsolationMVA3oldDMwoLT',
	   # 'byMediumCombinedIsolationDeltaBetaCorr3Hits',
	   # 'byMediumIsolationMVA3newDMwLT',
	   # 'byMediumIsolationMVA3newDMwoLT',
	   # 'byMediumIsolationMVA3oldDMwLT',
	   # 'byMediumIsolationMVA3oldDMwoLT',
	   # 'byTightCombinedIsolationDeltaBetaCorr3Hits',
	   # 'byTightIsolationMVA3newDMwLT',
	   # 'byTightIsolationMVA3newDMwoLT',
	   # 'byTightIsolationMVA3oldDMwLT',
	   # 'byTightIsolationMVA3oldDMwoLT',
	   # 'byVLooseIsolationMVA3newDMwLT',
	   # 'byVLooseIsolationMVA3newDMwoLT',
	   # 'byVLooseIsolationMVA3oldDMwLT',
	   # 'byVLooseIsolationMVA3oldDMwoLT',
	   # 'byVTightIsolationMVA3newDMwLT',
	   # 'byVTightIsolationMVA3newDMwoLT',
	   # 'byVTightIsolationMVA3oldDMwLT',
	   # 'byVTightIsolationMVA3oldDMwoLT',
	   # 'byVVTightIsolationMVA3newDMwLT',
	   # 'byVVTightIsolationMVA3newDMwoLT',
	   # 'byVVTightIsolationMVA3oldDMwLT',
	   # 'byVVTightIsolationMVA3oldDMwoLT',
		'chargedIsoPtSum',
		'decayModeFinding',
		'decayModeFindingNewDMs',
		'neutralIsoPtSum',
		'puCorrPtSum'
		]),
	rho=cms.InputTag("fixedGridRhoAll"),
	jecFile=cms.FileInPath("TTH/TTHNtupleAnalyzer/data/Summer13_V4_DATA_UncertaintySources_AK5PFchs.txt")
)

process.TFileService = cms.Service("TFileService",
	fileName = cms.string(options.outputFile)
	#closeFileFast = cms.untracked.bool(True)
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

process.ak4PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
	minVtxNdof = cms.int32(4),
	vertexCollection = cms.string('offlineSlimmedPrimaryVertices'),
	algorithm = cms.string('AK4PF'),
	level = cms.string('L1Offset')
)

process.ak4PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
	algorithm = cms.string('AK4PF'),
	level = cms.string('L2Relative')
)

process.ak4PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
	algorithm = cms.string('AK4PF'),
	level = cms.string('L3Absolute')
)

process.ak4PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
	algorithm = cms.string('AK4PF'),
	level = cms.string('L2L3Residual')
)

process.ak4PFL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
	correctors = cms.vstring('ak4PFL1Fastjet',
		'ak4PFL2Relative',
		'ak4PFL3Absolute',
		'ak4PFResidual')
)

process.p = cms.Path(
	#process.hepTopTagPFJetsCHS *
	#process.hepTopTagInfos *
	process.chs *
	process.ca15PFJetsCHS *
	process.ca15PFJetsCHSMDT *
	process.ca15PFJetsCHSMDTFiltered *
	process.Njettiness *
	process.NjettinessMDT *
	process.NjettinessMDTFiltered *
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


#process.out = cms.OutputModule(
#	"PoolOutputModule",
#	fileName = cms.untracked.string("edm.root"),
#	# Drop per-event meta data from dropped objects
#	dropMetaData = cms.untracked.string("ALL"),
#	SelectEvents = cms.untracked.PSet(
#		SelectEvents = cms.vstring("*")
#	),
#	outputCommands = cms.untracked.vstring("keep *")
#)
#process.outpath = cms.EndPath(process.out)
