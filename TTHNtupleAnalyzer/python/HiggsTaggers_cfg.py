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

# Necessary so we can import HiggsTaggers_cfg.py from ordinary python
# scripts and extract the fatjets
try:
   options.parseArguments()
except:
   pass

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


#####################################
# Ungroomed Fatjets
#####################################

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

fj_name = "ca15PFJetsCHSTrimmedR2F4"
branch_name = 'ca15trimmedr2f4'
setattr(process, fj_name, fj_ca15.clone(
        useTrimming = cms.bool(True),
        rFilt = cms.double(0.2),
        trimPtFracMin = cms.double(0.04),
        useExplicitGhosts = cms.bool(True)))
li_fatjets_objects.append(fj_name)        
li_fatjets_branches.append(branch_name)

fj_name = "ca15PFJetsCHSTrimmedR2F6"
branch_name = 'ca15trimmedr2f6'
setattr(process, fj_name, fj_ca15.clone(
        useTrimming = cms.bool(True),
        rFilt = cms.double(0.2),
        trimPtFracMin = cms.double(0.06),
        useExplicitGhosts = cms.bool(True)))
li_fatjets_objects.append(fj_name)        
li_fatjets_branches.append(branch_name)

fj_name = "ca15PFJetsCHSTrimmedR2F8"
branch_name = 'ca15trimmedr2f8'
setattr(process, fj_name, fj_ca15.clone(
        useTrimming = cms.bool(True),
        rFilt = cms.double(0.2),
        trimPtFracMin = cms.double(0.08),
        useExplicitGhosts = cms.bool(True)))
li_fatjets_objects.append(fj_name)        
li_fatjets_branches.append(branch_name)

fj_name = "ca15PFJetsCHSSoftDropZ15b00"
branch_name = 'ca15softdropz15b00'
setattr(process, fj_name, fj_ca15.clone(
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.15),
        beta = cms.double(0.0),
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

fj_name = "ca15PFJetsCHSSoftDropZ30b20"
branch_name = 'ca15softdropz30b20'
setattr(process, fj_name, fj_ca15.clone(
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.3),
        beta = cms.double(2.0),
        useExplicitGhosts = cms.bool(True)))
li_fatjets_objects.append(fj_name)
li_fatjets_branches.append(branch_name)

fj_name = "ca15PFJetsCHSSoftDropZ30b30"
branch_name = 'ca15softdropz30b30'
setattr(process, fj_name, fj_ca15.clone(
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.3),
        beta = cms.double(3.0),
        useExplicitGhosts = cms.bool(True)))
li_fatjets_objects.append(fj_name)
li_fatjets_branches.append(branch_name)

fj_name = "ca15PFJetsCHSSoftDropZ30b100"
branch_name = 'ca15softdropz30b100'
setattr(process, fj_name, fj_ca15.clone(
        useSoftDrop = cms.bool(True),
        zcut = cms.double(0.3),
        beta = cms.double(10.0),
        useExplicitGhosts = cms.bool(True)))
li_fatjets_objects.append(fj_name)
li_fatjets_branches.append(branch_name)

print li_fatjets_branches 

#####################################
# NSubjettiness
#####################################

li_fatjets_nsubs = []
for fj_name in li_fatjets_objects:

   nsub_name = fj_name + "Njettiness"

   setattr(process, nsub_name, cms.EDProducer("NjettinessAdder",
                                              src=cms.InputTag(fj_name),
                                              Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                              # variables for measure definition : 
                                              measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                              beta = cms.double(1.0),              # CMS default is 1
                                              R0 = cms.double(1.5),              # CMS default is jet cone size
                                              Rcutoff = cms.double( -999.0),       # not used by default
                                              # variables for axes definition :
                                              axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                              nPass = cms.int32(-999),             # not used by default
                                              akAxesR0 = cms.double(-999.0)        # not used by default
                                      ))
   li_fatjets_nsubs.append(nsub_name)


#####################################
# QJets
#####################################

# Qjets need a RNG
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService")

li_fatjets_qvols = []
for i_fj, fj_name in enumerate(li_fatjets_objects):
        
   qvol_fatjets = ["ca15PFJetsCHS"]
   
   r = "15"

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
                                                   jetRad= cms.double(1.5),
                                                   jetAlgo=cms.string("CA"),
                                                   preclustering = cms.int32(50)))

        setattr(process.RandomNumberGeneratorService, qvol_name, cms.PSet(initialSeed = cms.untracked.uint32(i_fj),
                                                                          engineName = cms.untracked.string('TRandom3')))


        li_fatjets_qvols.append(qvol_name)
   else:
        li_fatjets_qvols.append('None')


#####################################
# b-tagging
#####################################

# Add b-tagging information for all fatjets
process.my_btagging = cms.Sequence()
li_fatjets_btags = []
for fatjet_name in li_fatjets_objects:

        # Define the names
        impact_info_name          = fatjet_name + "ImpactParameterTagInfos"
        sv_tag_info_name          = fatjet_name + "SecondaryVertexTagInfos"
        isv_info_name             = fatjet_name + "pfInclusiveSecondaryVertexFinderTagInfos"        
        csvv2_computer_name       = fatjet_name + "combinedSecondaryVertexV2Computer"
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
                sv_tag_info_name, 
                process.pfSecondaryVertexTagInfos.clone(                
                        trackIPTagInfos = cms.InputTag(impact_info_name),                        
                ))
        getattr(process, sv_tag_info_name).trackSelection.jetDeltaRMax = cms.double(delta_r)
        getattr(process, sv_tag_info_name).vertexCuts.maxDeltaRToJetAxis = cms.double(delta_r)


        setattr(process,
                isv_info_name,                
                process.pfInclusiveSecondaryVertexFinderTagInfos.clone(
                        extSVCollection               = cms.InputTag('slimmedSecondaryVertices'),
                        trackIPTagInfos               = cms.InputTag(impact_info_name),
                        extSVDeltaRToJet              = cms.double(delta_r)
                ))
        getattr(process, isv_info_name).vertexCuts.maxDeltaRToJetAxis = cms.double(delta_r)
        

        setattr(process,
                csvv2_computer_name,
                process.candidateCombinedSecondaryVertexV2Computer.clone())
        getattr(process, csvv2_computer_name).trackSelection.jetDeltaRMax       = cms.double(delta_r) 
        getattr(process, csvv2_computer_name).trackPseudoSelection.jetDeltaRMax = cms.double(delta_r) 
        
        setattr(process,
                csvv2ivf_name,
                process.pfCombinedInclusiveSecondaryVertexV2BJetTags.clone(
                        tagInfos = cms.VInputTag(cms.InputTag(impact_info_name),
                                                 cms.InputTag(isv_info_name)),
                        jetTagComputer = cms.string(csvv2_computer_name,)
                ))

        # Add modules to sequence
        for module_name in [impact_info_name,
                            sv_tag_info_name,         
                            isv_info_name,              
                            csvv2ivf_name]:              
                process.my_btagging += getattr(process, module_name)

        # remember the module that actually produces the b-tag
        # discriminator so we can pass it to the NTupelizer
        li_fatjets_btags.append(csvv2ivf_name)

# end of loop over fatjets


#####################################
# NTupelizer
#####################################

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
        fatjetsSDs      = cms.vstring(["None"]*len(li_fatjets_objects)),
        fatjetsQvols    = cms.vstring(li_fatjets_qvols),
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
                
# Schedule b-tagging and Ntupelizer
for x in [process.my_btagging,
          process.tthNtupleAnalyzer]:
        process.p += x
