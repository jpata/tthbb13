import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
import os

options = VarParsing('analysis')
process = cms.Process("Demo")
options.parseArguments()

if len(options.inputFiles)==0:
		#options.inputFiles = cms.untracked.vstring(["/store/mc/Spring14miniaod/TTbarH_HToBB_M-125_13TeV_pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/0E97DD3E-2209-E411-8A04-003048945312.root"])
	options.inputFiles = cms.untracked.vstring(['/store/mc/Spring14miniaod/TTbarH_HToBB_M-125_13TeV_pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/0E97DD3E-2209-E411-8A04-003048945312.root',
							'/store/mc/Spring14miniaod/TTbarH_HToBB_M-125_13TeV_pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/D0242854-2209-E411-B361-003048C559CE.root'])


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
	)
)

from TTH.TTHNtupleAnalyzer.triggers_MC_cff import *
print '**** TRIGGER PATHS ****'
counter = 0
for trigger in triggerPathNames:
	print "[%s] = %s" % (counter, trigger)
	counter += 1

process.tthNtupleAnalyzer = cms.EDAnalyzer('TTHNtupleAnalyzer',
	isMC = cms.bool(True),
	vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
	muons = cms.InputTag("slimmedMuons"),
	electrons = cms.InputTag("slimmedElectrons"),
	taus = cms.InputTag("slimmedTaus"),
	jets = cms.InputTag("slimmedJets"),
	genjets = cms.InputTag("slimmedGenJets"),

	topjets1 = cms.InputTag("HTTJetsCHS"),
	topjetinfos1 = cms.InputTag("HTTJetsCHS"),
	topjetsubjets1 = cms.InputTag("HTTJetsCHS", "caTopSubJets"),

	topjets2 = cms.InputTag("MultiRHTTJetsCHS"),
	topjetinfos2 = cms.InputTag("MultiRHTTJetsCHS"),
	topjetsubjets2 = cms.InputTag("MultiRHTTJetsCHS", "caTopSubJets"),

	packed = cms.InputTag("packedGenParticles"),
	pruned = cms.InputTag("prunedGenParticles"),
	fatjets = cms.InputTag("slimmedJetsAK8"),
	mets = cms.InputTag("slimmedMETs"),
	lhe = cms.InputTag("externalLHEProducer"),

	triggerIdentifiers = triggerPathNames,
	#triggerIdentifiers=cms.vstring([]),
	triggerIdentifiersForMatching = cms.vstring([
			'HLT_Ele27_WP80_v*',
			'HLT_IsoMu24_eta2p1_v*',
			'HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*',
			]),
	#triggerIdentifiersForMatching=cms.vstring([]),

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
		])
)

process.TFileService = cms.Service("TFileService",
	fileName = cms.string(options.outputFile)
	#closeFileFast = cms.untracked.bool(True)
)

process.load('RecoJets.JetProducers.caTopTaggers_cff')

##need to override from pfNoPileUpJME which is not present in miniAOD
#process.hepTopTagPFJetsCHS.src = cms.InputTag("packedPFCandidates")
#
##NB: this module is actually not called, it's here just for reference
#caTopTagInfos = cms.EDProducer("CATopJetTagger",
#	src = cms.InputTag("cmsTopTagPFJetsCHS"),
#	TopMass = cms.double(173),
#	TopMassMin = cms.double(0.),
#	TopMassMax = cms.double(250.),
#	WMass = cms.double(80.4),
#	WMassMin = cms.double(0.0),
#	WMassMax = cms.double(200.0),
#	MinMassMin = cms.double(0.0),
#	MinMassMax = cms.double(200.0),
#	verbose = cms.bool(False)
#)
#
#process.hepTopTagInfos = caTopTagInfos.clone(
#	src = cms.InputTag("hepTopTagPFJetsCHS")
#)

from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.PFJetParameters_cfi import *

#process.HTTJetsCHSLoose = cms.EDProducer(
#   "HTTTopJetProducer",
#	#need to override from pfNoPileUpJME which is not present in miniAOD
#    #
#	PFJetParameters.clone(src = cms.InputTag('packedPFCandidates'),
#						 doAreaFastjet = cms.bool(True),
#						 doRhoFastjet = cms.bool(False),
#						 jetPtMin = cms.double(100.0)
#	),
#	AnomalousCellParameters,
#	algorithm = cms.int32(1),
#	jetAlgorithm = cms.string("CambridgeAachen"),
#	rParam = cms.double(1.5),
#	minFatjetPt = cms.double(100.),
#	minCandPt = cms.double(100.),
#	minSubjetPt = cms.double(20.),
#	writeCompound = cms.bool(True),
#	minCandMass = cms.double(0.),
#	maxCandMass = cms.double(10000.),
#	massRatioWidth = cms.double(50.),
#)


#for comparison with Thomas/Gregor 15.10.14
#process.HTTJetsCHS = cms.EDProducer(
#    "HTTTopJetProducer",
#    PFJetParameters.clone( src = cms.InputTag('packedPFCandidates'),
#                           doAreaFastjet = cms.bool(True),
#                           doRhoFastjet = cms.bool(False),
#                           jetPtMin = cms.double(100.0)
#                       ),
#    AnomalousCellParameters,
#    algorithm = cms.int32(1),
#    jetAlgorithm = cms.string("CambridgeAachen"),
#    rParam = cms.double(1.5),
#    mode = cms.int32(0),
#    minFatjetPt = cms.double(200.),
#    minCandPt = cms.double(0.),
#    minSubjetPt = cms.double(30.),
#    writeCompound = cms.bool(True),
#    minCandMass = cms.double(140.),
#    maxCandMass = cms.double(20000.),
#)
process.HTTJetsCHS = cms.EDProducer(
	"HTTTopJetProducer",
	PFJetParameters.clone(src = cms.InputTag('packedPFCandidates'),
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
    PFJetParameters.clone( src = cms.InputTag('particleFlow'),
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
    minCandPt = cms.double(0.),
    minSubjetPt = cms.double(30.),
    writeCompound = cms.bool(True),
    minCandMass = cms.double(0.),
    maxCandMass = cms.double(20000.),
    massRatioWidth = cms.double(15.),
)

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = "PLS170_V7AN1"

process.p = cms.Path(
	#process.hepTopTagPFJetsCHS *
	#process.hepTopTagInfos *
	process.HTTJetsCHS *
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
