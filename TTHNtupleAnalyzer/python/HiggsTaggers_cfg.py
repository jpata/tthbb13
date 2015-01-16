# Tagger_cfg.py
# cmsRun configuration file for producing NTuples for Top & Higgs-Tagging Studies

import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
import os
import socket

hostname = socket.gethostname()

options = VarParsing('analysis')
options.register ('skipEvents',
	0,
	VarParsing.multiplicity.singleton,
	VarParsing.varType.int,
	"Skip this number of events"
)

process = cms.Process("Demo")
options.parseArguments()

# Load some standard configuration files
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("RecoBTag.Configuration.RecoBTag_cff") # this loads all available b-taggers

# Load the necessary conditions 
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')


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


# First create the ungroomed CA15 fatjet collection:

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


# Add grooming
process.ca15PFJetsCHSFiltered = process.ca15PFJetsCHS.clone(
    useFiltering = cms.bool(True),
    nFilt = cms.int32(2),
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


# Nsubjettiness for groomed and ungroomed fatjets
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


# Setup fatjet collections to store
li_fatjets_objects = ['ca15PFJetsCHS',  
                      'ca15PFJetsCHSFiltered',  
                      'ca15PFJetsCHSPruned',  
                      'ca15PFJetsCHSTrimmed' ,
                      'ca15PFJetsCHSSoftDrop'  ]

li_fatjets_nsubs = ['NjettinessCA15', 
                    'NjettinessCA15Filtered', 
                    'NjettinessCA15Pruned', 
                    'NjettinessCA15Trimmed',
                    'NjettinessCA15SoftDrop' ]

li_fatjets_sds = ['None', 
                  'None', 
                  'None', 
                  'None',
                  'None' ]

li_fatjets_branches =  ['ca15',           
                        'ca15filtered',           
                        'ca15pruned',           
                        'ca15trimmed',
                        'ca15softdrop']

li_fatjets_is_basic_jets = [0] * len(li_fatjets_objects)


# Add b-tagging information for all fatjets
process.my_btagging = cms.Sequence()
li_fatjets_btags = []
for fatjet_name in li_fatjets_objects:

        # Define the names
        impact_info_name          = fatjet_name + "ImpactParameterTagInfos"
        track_count_high_eff_name = fatjet_name + "TrackCountHighEff"
        track_count_high_pur_name = fatjet_name + "TrackCountHighPur"
        jet_prob_name             = fatjet_name + "JetProbability"
        jet_bprob_name            = fatjet_name + "JetBProbability"
        sv_tag_info_name          = fatjet_name + "SecondaryVertexTagInfos"
        ssv_high_eff_btags_name   = fatjet_name + "SimpleSecondaryVertexHighEffBJetTags"
        ssv_high_pur_btags_name   = fatjet_name + "SimpleSecondaryVertexHighPurBJetTags"
        csv_btags_name            = fatjet_name + "pfCombinedSecondaryVertexBJetTags"
        isv_info_name             = fatjet_name + "pfInclusiveSecondaryVertexFinderTagInfos"        
        csvv2ivf_name             = fatjet_name + "pfCombinedInclusiveSecondaryVertexV2BJetTags"        

        if "08" in fatjet_name:
                delta_r = 0.8
        else:
                delta_r = 1.5


        # Setup the modules
        setattr(process, 
                impact_info_name, 
                process.pfImpactParameterTagInfos.clone(
                        primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
                        candidates = cms.InputTag("packedPFCandidates"),
                        jets = cms.InputTag(fatjet_name),
                        maxDeltaR= cms.double(delta_r)
                ))

        setattr(process,
                track_count_high_eff_name,                
                process.pfTrackCountingHighEffBJetTags.clone(
                        tagInfos = cms.VInputTag(cms.InputTag(impact_info_name))
                        ))

        setattr(process,
                track_count_high_pur_name,                
                process.pfTrackCountingHighPurBJetTags.clone(
                        tagInfos = cms.VInputTag(cms.InputTag(impact_info_name))
                        ))

        setattr(process,
                jet_prob_name,
                process.pfJetProbabilityBJetTags.clone(
                        tagInfos = cms.VInputTag(cms.InputTag(impact_info_name))
                        ))

        setattr(process,
                jet_bprob_name,
                process.pfJetBProbabilityBJetTags.clone(
                        tagInfos = cms.VInputTag(cms.InputTag(impact_info_name))
                ))

        setattr(process,
                sv_tag_info_name, 
                process.pfSecondaryVertexTagInfos.clone(                
                        trackIPTagInfos = cms.InputTag(impact_info_name) 
                ))

        setattr(process,
                ssv_high_eff_btags_name,                
                process.pfSimpleSecondaryVertexHighEffBJetTags.clone(
                        tagInfos = cms.VInputTag(cms.InputTag(sv_tag_info_name))
                ))

        setattr(process,
                ssv_high_pur_btags_name,                
                process.pfSimpleSecondaryVertexHighPurBJetTags.clone(
                        tagInfos = cms.VInputTag(cms.InputTag(sv_tag_info_name))
                ))

        setattr(process,
                csv_btags_name,
                process.pfCombinedSecondaryVertexBJetTags.clone(
                        tagInfos = cms.VInputTag(cms.InputTag(impact_info_name),
                                                 cms.InputTag(sv_tag_info_name))
                ))

        setattr(process,
                isv_info_name,                
                process.pfInclusiveSecondaryVertexFinderTagInfos.clone(
                        extSVCollection = cms.InputTag('slimmedSecondaryVertices'),
                        trackIPTagInfos = cms.InputTag(impact_info_name),

                ))

        setattr(process,
                csvv2ivf_name,
                process.pfCombinedInclusiveSecondaryVertexV2BJetTags.clone(
                        tagInfos = cms.VInputTag(cms.InputTag(impact_info_name),
                                                 cms.InputTag(isv_info_name))
                ))


        # Add modules to sequence
        for module_name in [impact_info_name,
                            track_count_high_eff_name,
                            track_count_high_pur_name,
                            jet_prob_name,
                            jet_bprob_name,          
                            sv_tag_info_name,         
                            ssv_high_eff_btags_name,  
                            ssv_high_pur_btags_name,  
                            csv_btags_name,           
                            isv_info_name,              
                            csvv2ivf_name]:              
                process.my_btagging += getattr(process, module_name)

        # remember the module that actually produces the b-tag
        # discriminator so we can pass it to the NTupelizer
        li_fatjets_btags.append(csvv2ivf_name)

# end of loop over fatjets




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
        fatjetsBtags    = cms.vstring(li_fatjets_btags),
        fatjetsBranches = cms.vstring(li_fatjets_branches),
        fatjetsIsBasicJets = cms.vint32(li_fatjets_is_basic_jets),                                           

        httObjects  = cms.vstring([]),                                           
        httBranches = cms.vstring([]),                                           
       
        cmsttObjects  = cms.vstring([]),
        cmsttInfos    = cms.vstring([]),
        cmsttBranches = cms.vstring([]),

	jetMult_min   = cms.untracked.int32(-99),
	jetPt_min     = cms.untracked.double(15.),
	muPt_min_     = cms.untracked.double(15.),
	elePt_min_    = cms.untracked.double(15.),
	tauPt_min_    = cms.untracked.double(15.),

        genPartonPt_min = cms.untracked.double(150.),

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




process.p = cms.Path(

        process.chs *
        process.ca15PFJetsCHS *

        process.ca15PFJetsCHSFiltered * 
        process.ca15PFJetsCHSPruned   * 
        process.ca15PFJetsCHSTrimmed  * 
        process.ca15PFJetsCHSSoftDrop *

        process.NjettinessCA15 *        
        process.NjettinessCA15Filtered *        
        process.NjettinessCA15Pruned *        
        process.NjettinessCA15Trimmed *        
        process.NjettinessCA15SoftDrop *        

        process.my_btagging *
        
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

