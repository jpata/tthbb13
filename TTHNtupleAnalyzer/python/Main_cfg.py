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

# Necessary so we can import Main_cfg.py from ordinary python
# scripts and extract the fatjets
try:
   options.parseArguments()
except:
   pass



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


process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = "PLS170_V7AN1"


# Select candidates that would pass CHS requirements
# This can be used as input for HTT and other jet clustering algorithms
process.chs = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV"))


#####################################
# Ungroomed Fatjets
#####################################

from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *

# Setup fatjet collections to store
li_fatjets_objects = []
li_fatjets_branches = []

# CA, R=1.5, pT > 200 GeV
fj_name = "ca15PFJetsCHS"
branch_name = 'ca15'
setattr(process, fj_name, cms.EDProducer(
        "FastjetJetProducer",
        PFJetParameters,
        AnomalousCellParameters,
        jetAlgorithm = cms.string("CambridgeAachen"),
        rParam       = cms.double(1.5)))
getattr(process, fj_name).src = cms.InputTag("chs")
getattr(process, fj_name).jetPtMin = cms.double(200)
li_fatjets_objects.append(fj_name)
li_fatjets_branches.append(branch_name)
fj_ca15 = getattr(process, fj_name) # We will re-use this one


#####################################
# Groomed Fatjets
#####################################

fj_name = "ca15PFJetsCHSTrimmedR2F6"
branch_name = 'ca15trimmedr2f6'
setattr(process, fj_name, fj_ca15.clone(
        useTrimming = cms.bool(True),
        rFilt = cms.double(0.2),
        trimPtFracMin = cms.double(0.06),
        useExplicitGhosts = cms.bool(True)))
li_fatjets_objects.append(fj_name)        
li_fatjets_branches.append(branch_name)

fj_name = "ca15PFJetsCHSSoftDropZ20b10"
branch_name = 'ca15softdropz20b10'
setattr(process, fj_name, fj_ca15.clone(
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.2),
        beta = cms.double(1.0),
        useExplicitGhosts = cms.bool(True)))
li_fatjets_objects.append(fj_name)
li_fatjets_branches.append(branch_name)


#####################################
# Helpers: GetRadiusFromName / GetRadiusStringFromName
#####################################

def GetRadiusFromName(name):       
   if "08" in fj_name:
      return 0.8 
   elif "15" in fj_name:
      return 1.5
   else:
      print "Invalid jet radius!"
      sys.exit()

def GetRadiusStringFromName(name):        
   if "08" in fj_name:
      return "08"
   elif "15" in fj_name:
      return "15"
   else:
      print "Invalid jet radius!"
      sys.exit()


#####################################
# NSubjettiness
#####################################

li_fatjets_nsubs = []
for fj_name in li_fatjets_objects:

   nsub_name = fj_name + "Njettiness"
        
   r = GetRadiusFromName(fj_name)

   setattr(process, nsub_name, cms.EDProducer("NjettinessAdder",
                                              src=cms.InputTag(fj_name),
                                              Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                              # variables for measure definition : 
                                              measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                              beta = cms.double(1.0),              # CMS default is 1
                                              R0 = cms.double(r),              # CMS default is jet cone size
                                              Rcutoff = cms.double( -999.0),       # not used by default
                                              # variables for axes definition :
                                              axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                              nPass = cms.int32(-999),             # not used by default
                                              akAxesR0 = cms.double(-999.0)        # not used by default
                                      ))
   li_fatjets_nsubs.append(nsub_name)



#####################################
#  HEPTopTagger
#####################################

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


#####################################
#  Trigger
#####################################

#trigger paths are now saved in ntuple
from TTH.TTHNtupleAnalyzer.triggers_MC_cff import *
#print '**** TRIGGER PATHS ****'
#counter = 0
#for trigger in triggerPathNames:
#	print "[%s] = %s" % (counter, trigger)
#	counter += 1


#####################################
# QJets
#####################################

# Qjets need a RNG
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService")

li_fatjets_qvols = []
for i_fj, fj_name in enumerate(li_fatjets_objects):

   r = GetRadiusFromName(fj_name)           
        
   qvol_fatjets = ["ca08PFJetsCHS", "ca15PFJetsCHS"]

   if fj_name in qvol_fatjets:

           qvol_name = fj_name + "QJetVolatility"

           setattr(process, qvol_name, cms.EDProducer("QjetsAdder",
                                                      src=cms.InputTag(fj_name),
                                                      zcut=cms.double(0.1),
                                                      dcutfctr=cms.double(0.5),
                                                      expmin=cms.double(0.0),
                                                      expmax=cms.double(0.0),
                                                      rigidity=cms.double(0.1),
                                                      ntrial = cms.int32(50),
                                                      cutoff=cms.double(10.0),
                                                      jetRad= cms.double(r),
                                                      jetAlgo=cms.string("CA"),
                                                      preclustering = cms.int32(50)))

           setattr(process.RandomNumberGeneratorService, qvol_name, cms.PSet(initialSeed = cms.untracked.uint32(i_fj),
                                                                             engineName = cms.untracked.string('TRandom3')))


           li_fatjets_qvols.append(qvol_name)

   else:
           li_fatjets_qvols.append('None')




#####################################
# NTupelizer
#####################################

li_fatjets_is_basic_jets = [0] * len(li_fatjets_objects)
li_fatjets_btags         = ["None"] * len(li_fatjets_objects)
li_fatjets_sds           = ["None"] * len(li_fatjets_objects)

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

        fatjetsObjects  = cms.vstring(li_fatjets_objects),
        fatjetsNsubs    = cms.vstring(li_fatjets_nsubs),
        fatjetsSDs      = cms.vstring(li_fatjets_sds),
        fatjetsBtags    = cms.vstring(li_fatjets_btags),
        fatjetsQvols    = cms.vstring(li_fatjets_qvols),
        fatjetsBranches = cms.vstring(li_fatjets_branches),
        fatjetsIsBasicJets = cms.vint32(li_fatjets_is_basic_jets),                                           
                                           
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
	 #   # 'againstElectronLoose',
	 #   # 'againstElectronLooseMVA5',
		# 'againstElectronMVA5category',
		# 'againstElectronMVA5raw',
	 #   # 'againstElectronMedium',
		# 'againstElectronMediumMVA5',
		# 'againstElectronTight',
		# 'againstElectronTightMVA5',
		# 'againstElectronVLooseMVA5',
	 #   # 'againstElectronVTightMVA5',
	 #   # 'againstMuonLoose',
	 #   # 'againstMuonLoose2',
	 #   # 'againstMuonLoose3',
		# 'againstMuonLooseMVA',
	 #   # 'againstMuonMVAraw',
	 #   # 'againstMuonMedium',
	 #   # 'againstMuonMedium2',
		# 'againstMuonMediumMVA',
	 #   # 'againstMuonTight',
	 #   # 'againstMuonTight2',
	 #   # 'againstMuonTight3',
		# 'againstMuonTightMVA',
	 #   # 'byCombinedIsolationDeltaBetaCorrRaw3Hits',
	 #   # 'byIsolationMVA3newDMwLTraw',
	 #   # 'byIsolationMVA3newDMwoLTraw',
	 #   # 'byIsolationMVA3oldDMwLTraw',
	 #   # 'byIsolationMVA3oldDMwoLTraw',
	 #   # 'byLooseCombinedIsolationDeltaBetaCorr3Hits',
	 #   # 'byLooseIsolationMVA3newDMwLT',
	 #   # 'byLooseIsolationMVA3newDMwoLT',
	 #   # 'byLooseIsolationMVA3oldDMwLT',
	 #   # 'byLooseIsolationMVA3oldDMwoLT',
	 #   # 'byMediumCombinedIsolationDeltaBetaCorr3Hits',
	 #   # 'byMediumIsolationMVA3newDMwLT',
	 #   # 'byMediumIsolationMVA3newDMwoLT',
	 #   # 'byMediumIsolationMVA3oldDMwLT',
	 #   # 'byMediumIsolationMVA3oldDMwoLT',
	 #   # 'byTightCombinedIsolationDeltaBetaCorr3Hits',
	 #   # 'byTightIsolationMVA3newDMwLT',
	 #   # 'byTightIsolationMVA3newDMwoLT',
	 #   # 'byTightIsolationMVA3oldDMwLT',
	 #   # 'byTightIsolationMVA3oldDMwoLT',
	 #   # 'byVLooseIsolationMVA3newDMwLT',
	 #   # 'byVLooseIsolationMVA3newDMwoLT',
	 #   # 'byVLooseIsolationMVA3oldDMwLT',
	 #   # 'byVLooseIsolationMVA3oldDMwoLT',
	 #   # 'byVTightIsolationMVA3newDMwLT',
	 #   # 'byVTightIsolationMVA3newDMwoLT',
	 #   # 'byVTightIsolationMVA3oldDMwLT',
	 #   # 'byVTightIsolationMVA3oldDMwoLT',
	 #   # 'byVVTightIsolationMVA3newDMwLT',
	 #   # 'byVVTightIsolationMVA3newDMwoLT',
	 #   # 'byVVTightIsolationMVA3oldDMwLT',
	 #   # 'byVVTightIsolationMVA3oldDMwoLT',
		# 'chargedIsoPtSum',
		# 'decayModeFinding',
		# 'decayModeFindingNewDMs',
		# 'neutralIsoPtSum',
		# 'puCorrPtSum'
		"decayModeFinding",
		"byLooseCombinedIsolationDeltaBetaCorr3Hits",
		"byMediumCombinedIsolationDeltaBetaCorr3Hits",
		"byTightCombinedIsolationDeltaBetaCorr3Hits",
		"byVLooseIsolationMVA3oldDMwoLT",
		"byLooseIsolationMVA3oldDMwoLT",
		"byMediumIsolationMVA3oldDMwoLT",
		"byTightIsolationMVA3oldDMwoLT",
		"byVTightIsolationMVA3oldDMwoLT",
		"byVVTightIsolationMVA3oldDMwoLT",
		"againstElectronVLooseMVA5",
		"againstElectronLooseMVA5",
		"againstElectronMediumMVA5",
		"againstElectronTightMVA5",
		"againstElectronVTightMVA5",
		"againstMuonLoose3",
		"againstMuonTight3",

		]),
	rho=cms.InputTag("fixedGridRhoAll"),
	jecFile=cms.FileInPath("TTH/TTHNtupleAnalyzer/data/Summer13_V4_DATA_UncertaintySources_AK5PFchs.txt")
)

process.TFileService = cms.Service("TFileService",
	fileName = cms.string(options.outputFile)
	#closeFileFast = cms.untracked.bool(True)
)




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


#####################################
# Schedule Algorithms
#####################################

process.p = cms.Path(process.chs)

# Schedule all fatjets
for fj_name in li_fatjets_objects:
   process.p += getattr(process, fj_name)

# Schedule NSubjettiness
for nsub_name in li_fatjets_nsubs:
   if nsub_name == "None":
      continue
   else:
      process.p += getattr(process, nsub_name)

# Schedule QJet Volatility
for qvol_name in li_fatjets_qvols:
   if qvol_name == "None":
      continue
   else:
      process.p += getattr(process, qvol_name)       

# Schedule HEPTopTagger and Ntupelizer
for x in [process.HTTJetsCHS,
          process.MultiRHTTJetsCHS,
          process.tthNtupleAnalyzer]:
        process.p += x


if "TTH_DEBUG" in os.environ:
	process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
	process.printTree = cms.EDAnalyzer("ParticleListDrawer",
		maxEventsToPrint = cms.untracked.int32(-1),
		printVertex = cms.untracked.bool(True),
		src = cms.InputTag("prunedGenParticles")
	)
	process.p += process.printTree

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

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
