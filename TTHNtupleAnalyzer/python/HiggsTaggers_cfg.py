
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

li_ungroomed_fatjets_objects = []
li_ungroomed_fatjets_branches = []

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
li_ungroomed_fatjets_objects.append(fj_name)
li_ungroomed_fatjets_branches.append(branch_name)
fj_ca15 = getattr(process, fj_name) # We will re-use this one


# AK, R=0.8, pT > 200 GeV
fj_name = "ak08PFJetsCHS"
branch_name = 'ak08'
setattr(process, fj_name, cms.EDProducer(
        "FastjetJetProducer",
        PFJetParameters,
        AnomalousCellParameters,
        jetAlgorithm = cms.string("AntiKt"),
        rParam       = cms.double(0.8)))
getattr(process, fj_name).src = cms.InputTag("chs")
getattr(process, fj_name).jetPtMin = cms.double(200)
li_fatjets_objects.append(fj_name)
li_fatjets_branches.append(branch_name)
li_ungroomed_fatjets_objects.append(fj_name)
li_ungroomed_fatjets_branches.append(branch_name)
fj_ak08 = getattr(process, fj_name) # We will re-use this one


#####################################
# Groomed Fatjets
#####################################

for ungroomed_fj_name, ungroomed_branch_name in zip(li_ungroomed_fatjets_objects,
                                            li_ungroomed_fatjets_branches):
   ungroomed_fj = getattr(process, ungroomed_fj_name)

   name = "trimmedr2f3"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
      useTrimming = cms.bool(True),
      rFilt = cms.double(0.2),
      trimPtFracMin = cms.double(0.03),
      useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "trimmedr2f6"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
      useTrimming = cms.bool(True),
      rFilt = cms.double(0.2),
      trimPtFracMin = cms.double(0.06),
      useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "trimmedr2f10"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
      useTrimming = cms.bool(True),
      rFilt = cms.double(0.2),
      trimPtFracMin = cms.double(0.1),
      useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "softdropz10b00"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.1),
           beta = cms.double(0.0),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "softdropz15b00"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.15),
           beta = cms.double(0.0),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "softdropz15b10"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.15),
           beta = cms.double(1.0),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "softdropz15b20"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.15),
           beta = cms.double(2.0),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "softdropz20b10"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.20),
           beta = cms.double(0.1),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "softdropz30b10"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.30),
           beta = cms.double(0.1),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "softdropz30b15"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.30),
           beta = cms.double(0.15),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)
#
#   if "ca15" in ungroomed_fj_name:
#      name = "massdrop"
#      fj_name = ungroomed_fj_name + name
#      branch_name = ungroomed_branch_name + name
#      setattr(process, fj_name, ungroomed_fj.clone(
#         useMassDropTagger = cms.bool(True),
#         muCut = cms.double(0.667),
#         yCut = cms.double(0.08),
#         useExplicitGhosts = cms.bool(True)))
#      li_fatjets_objects.append(fj_name)        
#      li_fatjets_branches.append(branch_name)
#
#   if "ca15" in ungroomed_fj_name:
#      name = "massdropfiltered"
#      fj_name = ungroomed_fj_name + name
#      branch_name = ungroomed_branch_name + name
#      setattr(process, fj_name, ungroomed_fj.clone(
#         useMassDropTagger = cms.bool(True),
#         useFiltering = cms.bool(True),
#         muCut = cms.double(0.667),
#         yCut = cms.double(0.08),
#         nFilt = cms.int32(3),
#         rFilt = cms.double(0.3),		     
#         useExplicitGhosts = cms.bool(True)))
#      li_fatjets_objects.append(fj_name)        
#      li_fatjets_branches.append(branch_name)
#
   name = "filteredn3r3"
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
        useFiltering = cms.bool(True),
        nFilt = cms.int32(3),
        rFilt = cms.double(0.3),
        useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "filteredn3r2"
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
        useFiltering = cms.bool(True),
        nFilt = cms.int32(3),
        rFilt = cms.double(0.2),
        useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "filteredn2r3"
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
        useFiltering = cms.bool(True),
        nFilt = cms.int32(2),
        rFilt = cms.double(0.3),
        useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "filteredn2r2"
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
        useFiltering = cms.bool(True),
        nFilt = cms.int32(2),
        rFilt = cms.double(0.2),
        useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)

   name = "prunedn2z10rfac50"
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
        usePruning = cms.bool(True),
        nFilt = cms.int32(2),
        zcut = cms.double(0.1),
        rcut_factor = cms.double(0.5),
        useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_branches.append(branch_name)


#####################################
# QJets
#####################################

# We want to test a few different settings of qjets
# So we set the qvol of all the already scheduled fatjets to "None"
# And then add a new clone of the ungroomed fatjet for eahc qvol
# setting we like to check

li_fatjets_qvols = ["None"] * len(li_fatjets_objects)

# Qjets need a RNG
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService")
seed = 42

for ungroomed_fj_name, ungroomed_branch_name in zip(li_ungroomed_fatjets_objects, li_ungroomed_fatjets_branches):
   continue
   
   if "ak08" in ungroomed_fj_name:
      algorithm = "AK"
      cone_size = 0.8
   elif "ca15" in ungroomed_fj_name:
      algorithm = "CA"
      cone_size = 1.5

   for qvol_alpha in [0, 0.01, 0.1, 1, 100]:
            
      qvol_string = "QVol" + str(qvol_alpha).replace(".","p")
      
      new_fj_name = ungroomed_fj_name + qvol_string
      new_branch_name = ungroomed_branch_name + qvol_string

      # Clone the fatjet
      setattr(process, new_fj_name, getattr(process, ungroomed_fj_name).clone())

      # Add the process to calculate QJetVolatility
      qvol_name = new_fj_name + "QJetVolatility"
      setattr(process, qvol_name, cms.EDProducer("QjetsAdder",
                                                 src=cms.InputTag(new_fj_name),
                                                 zcut=cms.double(0.1),
                                                 dcutfctr=cms.double(0.5),
                                                 expmin=cms.double(0.0),
                                                 expmax=cms.double(0.0),
                                                 rigidity=cms.double(qvol_alpha),
                                                 ntrial = cms.int32(50),
                                                 cutoff=cms.double(10.0),
                                                 jetRad= cms.double(cone_size),
                                                 jetAlgo=cms.string(algorithm),
                                                 preclustering = cms.int32(50)))
      
      setattr(process.RandomNumberGeneratorService, qvol_name, cms.PSet(initialSeed = cms.untracked.uint32(seed),
                                                                        engineName = cms.untracked.string('TRandom3')))
      seed += 1

      li_fatjets_objects.append(new_fj_name)        
      li_fatjets_branches.append(new_branch_name)
      li_fatjets_qvols.append(qvol_name)

      
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
        fatjetsBtags    = cms.vstring(["None"]*len(li_fatjets_objects)),
        fatjetsBranches = cms.vstring(li_fatjets_branches),
        fatjetsUsesubjets = cms.vint32(li_fatjets_is_basic_jets),                                           

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
                
# Schedule  Ntupelizer
for x in [process.tthNtupleAnalyzer]:
        process.p += x
