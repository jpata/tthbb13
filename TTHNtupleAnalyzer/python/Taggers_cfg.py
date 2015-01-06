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
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CATopJetParameters_cfi import *


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
    )

process.ca08PFJetsCHSPruned = process.ca08PFJetsCHS.clone(
    cms.PSet(nFilt = cms.int32(2),
             zcut = cms.double(0.1),
             rcut_factor = cms.double(0.5)),
    usePruning = cms.bool(True),
    useExplicitGhosts = cms.bool(True),
    )

process.ca08PFJetsCHSTrimmed = process.ca08PFJetsCHS.clone(
    useTrimming = cms.bool(True),
    rFilt = cms.double(0.2),
    trimPtFracMin = cms.double(0.03),
    useExplicitGhosts = cms.bool(True)
    )

process.ca08PFJetsCHSSoftDrop = process.ca08PFJetsCHS.clone(
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.1),
        beta = cms.double(0.0),
        useExplicitGhosts = cms.bool(True),
)

process.ca15PFJetsCHSFiltered = process.ca15PFJetsCHS.clone(
    useFiltering = cms.bool(True),
    nFilt = cms.int32(3),
    rFilt = cms.double(0.3),
    useExplicitGhosts = cms.bool(True),
)

process.ca15PFJetsCHSPruned = process.ca15PFJetsCHS.clone(
        cms.PSet(nFilt = cms.int32(2),
                 zcut = cms.double(0.1),
                 rcut_factor = cms.double(0.5)),
        usePruning = cms.bool(True),
        useExplicitGhosts = cms.bool(True),
)

process.ca15PFJetsCHSTrimmed = process.ca15PFJetsCHS.clone(
        useTrimming = cms.bool(True),
        rFilt = cms.double(0.2),
        trimPtFracMin = cms.double(0.03),
        useExplicitGhosts = cms.bool(True)
)

process.ca15PFJetsCHSSoftDrop = process.ca15PFJetsCHS.clone(
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.1),
        beta = cms.double(0.0),
        useExplicitGhosts = cms.bool(True)
)



# CMS Top Tagger Jets
process.cmsTopTagCa08PFJetsCHS = cms.EDProducer(
        "CATopJetProducer",
        PFJetParameters,
        AnomalousCellParameters,
        CATopJetParameters,
        jetAlgorithm = cms.string("CambridgeAachen"),
        rParam = cms.double(0.8),
        writeCompound = cms.bool(True)
    )
process.cmsTopTagCa08PFJetsCHS.src = cms.InputTag('chs')
process.cmsTopTagCa08PFJetsCHS.doAreaFastjet = cms.bool(True)
process.cmsTopTagCa08PFJetsCHS.jetPtMin = cms.double(200.0)

process.cmsTopTagCa15PFJetsCHS = cms.EDProducer(
        "CATopJetProducer",
        PFJetParameters,
        AnomalousCellParameters,
        CATopJetParameters,
        jetAlgorithm = cms.string("CambridgeAachen"),
        rParam = cms.double(1.5),
        writeCompound = cms.bool(True)
    )
process.cmsTopTagCa15PFJetsCHS.src = cms.InputTag('chs')
process.cmsTopTagCa15PFJetsCHS.doAreaFastjet = cms.bool(True)
process.cmsTopTagCa15PFJetsCHS.jetPtMin = cms.double(200.0)


# CMS Top Tagger Infos
process.ca08CMSTopTagInfos = cms.EDProducer("CATopJetTagger",
                                            src = cms.InputTag("cmsTopTagCa08PFJetsCHS"),
                                            TopMass = cms.double(173),
                                            TopMassMin = cms.double(0.),
                                            TopMassMax = cms.double(250.),
                                            WMass = cms.double(80.4),
                                            WMassMin = cms.double(0.0),
                                            WMassMax = cms.double(200.0),
                                            MinMassMin = cms.double(0.0),
                                            MinMassMax = cms.double(200.0),
                                            verbose = cms.bool(False))


process.ca15CMSTopTagInfos = cms.EDProducer("CATopJetTagger",
                                            src = cms.InputTag("cmsTopTagCa15PFJetsCHS"),
                                            TopMass = cms.double(173),
                                            TopMassMin = cms.double(0.),
                                            TopMassMax = cms.double(250.),
                                            WMass = cms.double(80.4),
                                            WMassMin = cms.double(0.0),
                                            WMassMax = cms.double(200.0),
                                            MinMassMin = cms.double(0.0),
                                            MinMassMax = cms.double(200.0),
                                            verbose = cms.bool(False))



# Nsubjettiness for groomed and ungroomed fatjets
process.NjettinessCA08 = cms.EDProducer("NjettinessAdder",
                                        src=cms.InputTag("ca08PFJetsCHS"),
                                        Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                        # variables for measure definition : 
                                        measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                        beta = cms.double(1.0),              # CMS default is 1
                                        R0 = cms.double( 0.8 ),              # CMS default is jet cone size
                                        Rcutoff = cms.double( -999.0),       # not used by default
                                        # variables for axes definition :
                                        axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                        nPass = cms.int32(-999),             # not used by default
                                        akAxesR0 = cms.double(-999.0)        # not used by default
                            )




process.NjettinessCA08Filtered = cms.EDProducer("NjettinessAdder",
                                                src=cms.InputTag("ca08PFJetsCHSFiltered"),
                                                Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                                # variables for measure definition : 
                                                measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                                beta = cms.double(1.0),              # CMS default is 1
                                                R0 = cms.double( 0.8 ),              # CMS default is jet cone size
                                                Rcutoff = cms.double( -999.0),       # not used by default
                                                # variables for axes definition :
                                                axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                                nPass = cms.int32(-999),             # not used by default
                                                akAxesR0 = cms.double(-999.0)        # not used by default
                            )

process.NjettinessCA08Pruned = cms.EDProducer("NjettinessAdder",
                                              src=cms.InputTag("ca08PFJetsCHSPruned"),
                                              Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                              # variables for measure definition : 
                                              measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                              beta = cms.double(1.0),              # CMS default is 1
                                              R0 = cms.double( 0.8 ),              # CMS default is jet cone size
                                              Rcutoff = cms.double( -999.0),       # not used by default
                                              # variables for axes definition :
                                              axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                              nPass = cms.int32(-999),             # not used by default
                                              akAxesR0 = cms.double(-999.0)        # not used by default

                            )


process.NjettinessCA08Trimmed = cms.EDProducer("NjettinessAdder",
                                               src=cms.InputTag("ca08PFJetsCHSTrimmed"),
                                               Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                               # variables for measure definition : 
                                               measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                               beta = cms.double(1.0),              # CMS default is 1
                                               R0 = cms.double( 0.8 ),              # CMS default is jet cone size
                                               Rcutoff = cms.double( -999.0),       # not used by default
                                               # variables for axes definition :
                                               axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                               nPass = cms.int32(-999),             # not used by default
                                               akAxesR0 = cms.double(-999.0)        # not used by default
                            )

process.NjettinessCA08SoftDrop = cms.EDProducer("NjettinessAdder",
                                               src=cms.InputTag("ca08PFJetsCHSSoftDrop"),
                                               Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                               # variables for measure definition : 
                                               measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                               beta = cms.double(1.0),              # CMS default is 1
                                               R0 = cms.double( 0.8 ),              # CMS default is jet cone size
                                               Rcutoff = cms.double( -999.0),       # not used by default
                                               # variables for axes definition :
                                               axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                               nPass = cms.int32(-999),             # not used by default
                                               akAxesR0 = cms.double(-999.0)        # not used by default
                            )

process.NjettinessCA15 = cms.EDProducer("NjettinessAdder",
                                        src=cms.InputTag("ca15PFJetsCHS"),
                                        Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                        # variables for measure definition : 
                                        measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                        beta = cms.double(1.0),              # CMS default is 1
                                        R0 = cms.double( 1.5 ),              # CMS default is jet cone size
                                        Rcutoff = cms.double( -999.0),       # not used by default
                                        # variables for axes definition :
                                        axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                        nPass = cms.int32(-999),             # not used by default
                                        akAxesR0 = cms.double(-999.0)        # not used by default
                            )

process.NjettinessCA15Filtered = cms.EDProducer("NjettinessAdder",
                                                src=cms.InputTag("ca15PFJetsCHSFiltered"),
                                                Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                                # variables for measure definition : 
                                                measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                                beta = cms.double(1.0),              # CMS default is 1
                                                R0 = cms.double( 1.5 ),              # CMS default is jet cone size
                                                Rcutoff = cms.double( -999.0),       # not used by default
                                                # variables for axes definition :
                                                axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                                nPass = cms.int32(-999),             # not used by default
                                                akAxesR0 = cms.double(-999.0)        # not used by default
                            )

process.NjettinessCA15Pruned = cms.EDProducer("NjettinessAdder",
                                              src=cms.InputTag("ca15PFJetsCHSPruned"),
                                              Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                              # variables for measure definition : 
                                              measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                              beta = cms.double(1.0),              # CMS default is 1
                                              R0 = cms.double( 1.5 ),              # CMS default is jet cone size
                                              Rcutoff = cms.double( -999.0),       # not used by default
                                              # variables for axes definition :
                                              axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                              nPass = cms.int32(-999),             # not used by default
                                              akAxesR0 = cms.double(-999.0)        # not used by default
)

process.NjettinessCA15Trimmed = cms.EDProducer("NjettinessAdder",
                                               src=cms.InputTag("ca15PFJetsCHSTrimmed"),
                                               Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                               # variables for measure definition : 
                                               measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                               beta = cms.double(1.0),              # CMS default is 1
                                               R0 = cms.double( 1.5 ),              # CMS default is jet cone size
                                               Rcutoff = cms.double( -999.0),       # not used by default
                                               # variables for axes definition :
                                               axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                               nPass = cms.int32(-999),             # not used by default
                                               akAxesR0 = cms.double(-999.0)        # not used by default
                            )

process.NjettinessCA15SoftDrop = cms.EDProducer("NjettinessAdder",
                                               src=cms.InputTag("ca15PFJetsCHSSoftDrop"),
                                               Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                               # variables for measure definition : 
                                               measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                               beta = cms.double(1.0),              # CMS default is 1
                                               R0 = cms.double( 1.5 ),              # CMS default is jet cone size
                                               Rcutoff = cms.double( -999.0),       # not used by default
                                               # variables for axes definition :
                                               axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                               nPass = cms.int32(-999),             # not used by default
                                               akAxesR0 = cms.double(-999.0)        # not used by default
                            )

# Schedule Shower Deconstruction
process.SDCA08 = cms.EDProducer("SDProducer",
                                FatjetName = cms.string("ca08PFJetsCHS"),
                                MicrojetCone = cms.double(0.2))

process.SDCA15 = cms.EDProducer("SDProducer",
                                FatjetName = cms.string("ca15PFJetsCHS"),
                                MicrojetCone = cms.double(0.2))


# Setup fatjet collections to store
li_fatjets_objects = ['ca08PFJetsCHS',  
                      'ca08PFJetsCHSFiltered',  
                      'ca08PFJetsCHSPruned',  
                      'ca08PFJetsCHSTrimmed',  
                      'ca08PFJetsCHSSoftDrop',  
                      'ca15PFJetsCHS',  
                      'ca15PFJetsCHSFiltered',  
                      'ca15PFJetsCHSPruned',  
                      'ca15PFJetsCHSTrimmed' ,
                      'ca15PFJetsCHSSoftDrop'  ]

li_fatjets_nsubs = ['NjettinessCA08', 
                    'NjettinessCA08Filtered', 
                    'NjettinessCA08Pruned', 
                    'NjettinessCA08Trimmed', 
                    'NjettinessCA08SoftDrop', 
                    'NjettinessCA15', 
                    'NjettinessCA15Filtered', 
                    'NjettinessCA15Pruned', 
                    'NjettinessCA15Trimmed',
                    'NjettinessCA15SoftDrop' ]

li_fatjets_sds = ['SDCA08', 
                  'None', 
                  'None', 
                  'None', 
                  'None', 
                  'SDCA15', 
                  'None', 
                  'None', 
                  'None',
                  'None' ]

li_fatjets_branches =  ['ca08',           
                        'ca08filtered',           
                        'ca08pruned',           
                        'ca08trimmed',           
                        'ca08softdrop',           
                        'ca15',           
                        'ca15filtered',           
                        'ca15pruned',           
                        'ca15trimmed',
                        'ca15softdrop']

li_fatjets_is_basic_jets = [0] * len(li_fatjets_objects)

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

        fatjetsObjects  = cms.vstring(li_fatjets_objects),
        fatjetsNsubs    = cms.vstring(li_fatjets_nsubs),
        fatjetsSDs      = cms.vstring(li_fatjets_sds),
        fatjetsBranches = cms.vstring(li_fatjets_branches),
        fatjetsIsBasicJets = cms.vint32(li_fatjets_is_basic_jets),                                           

        httObjects  = cms.vstring(['LooseMultiRHTTJetsCHS']),                                           
        httBranches = cms.vstring(['looseMultiRHTT']),                                           
       
        cmsttObjects  = cms.vstring(['cmsTopTagCa08PFJetsCHS', 'cmsTopTagCa15PFJetsCHS']),
        cmsttInfos    = cms.vstring(['ca08CMSTopTagInfos',     'ca15CMSTopTagInfos']),
        cmsttBranches = cms.vstring(['ca08cmstt',              'ca15cmstt']),

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

        rho = cms.InputTag("fixedGridRhoAll"),
        jecFile = cms.FileInPath("Summer13_V4_DATA_UncertaintySources_AK5PFchs.txt")
)

process.TFileService = cms.Service("TFileService",
	fileName = cms.string(options.outputFile)
)



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
        process.ca08PFJetsCHSSoftDrop *

        process.ca15PFJetsCHSFiltered * 
        process.ca15PFJetsCHSPruned   * 
        process.ca15PFJetsCHSTrimmed  * 
        process.ca15PFJetsCHSSoftDrop *

        process.NjettinessCA08 *        
        process.NjettinessCA08Filtered *        
        process.NjettinessCA08Pruned *        
        process.NjettinessCA08Trimmed *        
        process.NjettinessCA08SoftDrop *        

        process.NjettinessCA15 *        
        process.NjettinessCA15Filtered *        
        process.NjettinessCA15Pruned *        
        process.NjettinessCA15Trimmed *        
        process.NjettinessCA15SoftDrop *        

        process.cmsTopTagCa08PFJetsCHS *
        process.cmsTopTagCa15PFJetsCHS *
        process.ca08CMSTopTagInfos * 
        process.ca15CMSTopTagInfos * 

        process.SDCA08 * 
        process.SDCA15 * 

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

