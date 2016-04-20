# Tagger_cfg.py
# cmsRun configuration file for producing NTuples for Top & Higgs-Tagging Studies

import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
import os
import sys
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
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load("RecoBTag.Configuration.RecoBTag_cff") # this loads all available b-taggers


process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')
#process.GlobalTag = GlobalTag(process.GlobalTag, '76X_mcRun2_asymptotic_RunIIFall15DR76_v1')


#process.load("CondCore.DBCommon.CondDBCommon_cfi")
#from CondCore.DBCommon.CondDBSetup_cfi import *
#
#process.jec = cms.ESSource("PoolDBESSource",
#      DBParameters = cms.PSet(
#        messageLevel = cms.untracked.int32(0)
#        ),
#      timetype = cms.string('runnumber'),
#      toGet = cms.VPSet(
#      cms.PSet(
#            record = cms.string('JetCorrectionsRecord'),
#            tag    = cms.string('JetCorrectorParametersCollection_Summer15_25nsV6_MC_AK4PFchs'),
#            label  = cms.untracked.string('AK4PFchs')
#            ),
#      ), 
#      connect = cms.string('sqlite:Summer15_25nsV6_MC.db')
#)
### add an es_prefer statement to resolve a possible conflict from simultaneous connection to a global tag
#process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')


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


#process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",ignoreTotal = cms.untracked.int32(1) )




#####################################
# Input Objects
#####################################

# Select candidates that would pass CHS requirements
# This can be used as input for HTT and other jet clustering algorithms
process.chs = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV"))


process.load('CommonTools/PileupAlgos/Puppi_cff')
## e.g. to run on miniAOD
process.puppi.candName = cms.InputTag('packedPFCandidates')
process.puppi.vertexName = cms.InputTag('offlineSlimmedPrimaryVertices')
process.puppi.clonePackedCands = cms.bool(True)

# Ghost particle collection used for Hadron-Jet association 
from PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi import selectedHadronsAndPartons
process.selectedHadronsAndPartons = selectedHadronsAndPartons.clone(
    particles = "prunedGenParticles"
)

#####################################
# Ungroomed Fatjets
#####################################

DO_R15 = False
DO_R08 = True

from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CATopJetParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *


# Setup fatjet collections to store
li_fatjets_objects            = []
li_fatjets_initial_objects    = []
li_fatjets_branches           = []
li_ungroomed_fatjets_objects  = []
li_ungroomed_fatjets_branches = []


# First create the ungroomed fatjet collections
# These are the ones that get all the groomers applied to later on

if DO_R08:
   ## AntiKt, R=0.8, pT > 200 GeV, CHS
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
   li_fatjets_initial_objects.append(fj_name)
   li_fatjets_branches.append(branch_name)
   li_ungroomed_fatjets_objects.append(fj_name)
   li_ungroomed_fatjets_branches.append(branch_name)

   ## AntiKt, R=0.8, pT > 200 GeV, PUPPI
   fj_name = "ak08PFJetsPUPPI"
   branch_name = 'ak08puppi'
   setattr(process, fj_name, cms.EDProducer(
           "FastjetJetProducer",
           PFJetParameters,
           AnomalousCellParameters,
           jetAlgorithm = cms.string("AntiKt"),
           rParam       = cms.double(0.8)))
   getattr(process, fj_name).src = cms.InputTag("puppi")
   getattr(process, fj_name).jetPtMin = cms.double(200)
   li_fatjets_objects.append(fj_name)
   li_fatjets_branches.append(branch_name)
   li_fatjets_initial_objects.append(fj_name)
   li_ungroomed_fatjets_objects.append(fj_name)
   li_ungroomed_fatjets_branches.append(branch_name)

   ## AntiKt, R=0.8, pT > 200 GeV, GEN
   fj_name = "ak08PFJetsGEN"
   branch_name = 'ak08gen'
   setattr(process, fj_name, cms.EDProducer(
           "FastjetJetProducer",
           PFJetParameters,
           AnomalousCellParameters,
           jetAlgorithm = cms.string("AntiKt"),
           rParam       = cms.double(0.8)))
   getattr(process, fj_name).src = cms.InputTag("packedGenParticles")
   getattr(process, fj_name).jetPtMin = cms.double(200)
   getattr(process, fj_name).jetType = cms.string('GenJet')
   li_fatjets_objects.append(fj_name)
   li_fatjets_initial_objects.append(fj_name)
   li_fatjets_branches.append(branch_name)
   li_ungroomed_fatjets_objects.append(fj_name)
   li_ungroomed_fatjets_branches.append(branch_name)

if DO_R15:
   # CA, R=1.5, pT > 200 GeV, CHS
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
   li_fatjets_initial_objects.append(fj_name)
   li_fatjets_branches.append(branch_name)
   li_ungroomed_fatjets_objects.append(fj_name)
   li_ungroomed_fatjets_branches.append(branch_name)

   # CA, R=1.5, pT > 200 GeV, PUPPI
   fj_name = "ca15PFJetsPUPPI"
   branch_name = 'ca15puppi'
   setattr(process, fj_name, cms.EDProducer(
           "FastjetJetProducer",
           PFJetParameters,
           AnomalousCellParameters,
           jetAlgorithm = cms.string("CambridgeAachen"),
           rParam       = cms.double(1.5)))
   getattr(process, fj_name).src = cms.InputTag("puppi")
   getattr(process, fj_name).jetPtMin = cms.double(200)
   li_fatjets_objects.append(fj_name)
   li_fatjets_initial_objects.append(fj_name)
   li_fatjets_branches.append(branch_name)
   li_ungroomed_fatjets_objects.append(fj_name)
   li_ungroomed_fatjets_branches.append(branch_name)


#####################################
# AK 0.8 constituents
#####################################

if DO_R08:
   process.ak8PFJetsCHSConstituents = cms.EDFilter("MiniAODJetConstituentSelector",
                                                   src = cms.InputTag("ak08PFJetsCHS"),
                                                   cut = cms.string("pt>0")
                                                )

   process.ak8PFJetsPUPPIConstituents = cms.EDFilter("MiniAODJetConstituentSelector",
                                                   src = cms.InputTag("ak08PFJetsPUPPI"),
                                                   cut = cms.string("pt>0")
                                                )

#####################################
# Helpers: GetRadiusFromName / GetRadiusStringFromName
#####################################

def GetRadiusFromName(name):       

   if "08" in name:
      return 0.8 
   elif "15" in name:
      return 1.5
   else:
      print "Invalid jet radius!"
      sys.exit()

def GetRadiusStringFromName(name):        
   if "08" in name:
      return "08"
   elif "15" in name:
      return "15"
   else:
      print "Invalid jet radius!"
      sys.exit()

def GetAlgoFromName(name):       
   if ("ca08" in name.lower()) or ("ca15" in name.lower()):
      return "ca"
   elif "ak08" in name.lower():
      return "ak"
   else:
      print "Invalid jet algorithm!"
      sys.exit()


#####################################
# Groomed Fatjets
#####################################

for ungroomed_fj_name, ungroomed_branch_name in zip(li_ungroomed_fatjets_objects,
                                            li_ungroomed_fatjets_branches):

   ungroomed_fj = getattr(process, ungroomed_fj_name)

   r = GetRadiusFromName(fj_name)

   #####################################
   # Trimming (for btag)
   #####################################

   name = "trimmedr2f3forbtag"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
      useTrimming = cms.bool(True),
      rFilt = cms.double(0.2),
      trimPtFracMin = cms.double(0.03),
      useExplicitGhosts = cms.bool(True),
      writeCompound = cms.bool(True),
      jetCollInstanceName=cms.string("SubJets"),
   ))
   li_fatjets_objects.append(fj_name)     
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "trimmedr2f6forbtag"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
      useTrimming = cms.bool(True),
      rFilt = cms.double(0.2),
      trimPtFracMin = cms.double(0.06),
      useExplicitGhosts = cms.bool(True),
      writeCompound = cms.bool(True),
      jetCollInstanceName=cms.string("SubJets"),
   ))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "softdropz10b00forbtag"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.1),
           beta = cms.double(0.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True),
           writeCompound = cms.bool(True),
           jetCollInstanceName=cms.string("SubJets")
   ))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "softdropz20b10forbtag"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.2),
           beta = cms.double(1.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True),
           writeCompound = cms.bool(True),
           jetCollInstanceName=cms.string("SubJets")
   ))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "filteredn3r2forbtag"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
      useFiltering = cms.bool(True),
      nFilt = cms.int32(3),
      rFilt = cms.double(0.2),
      useExplicitGhosts = cms.bool(True),
      writeCompound = cms.bool(True),
      jetCollInstanceName=cms.string("SubJets")
   ))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "filteredn3r3forbtag"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
      useFiltering = cms.bool(True),
      nFilt = cms.int32(3),
      rFilt = cms.double(0.3),
      useExplicitGhosts = cms.bool(True),
      writeCompound = cms.bool(True),
      jetCollInstanceName=cms.string("SubJets")
   ))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "prunedn3z10rfac50forbtag"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
      usePruning = cms.bool(True),
      nFilt = cms.int32(3),
      zcut = cms.double(0.1),
      rcut_factor = cms.double(0.5),
      useExplicitGhosts = cms.bool(True),
      writeCompound = cms.bool(True),
      jetCollInstanceName=cms.string("SubJets")
   ))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)



   #####################################
   # Filtering
   #####################################

   name = "filteredn3r2"
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
        useFiltering = cms.bool(True),
        nFilt = cms.int32(3),
        rFilt = cms.double(0.2),
        useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)     
   li_fatjets_initial_objects.append(ungroomed_fj_name)      
   li_fatjets_branches.append(branch_name)

   name = "filteredn3r3"
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
        useFiltering = cms.bool(True),
        nFilt = cms.int32(3),
        rFilt = cms.double(0.3),
        useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "filteredn5r2"
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
        useFiltering = cms.bool(True),
        nFilt = cms.int32(5),
        rFilt = cms.double(0.2),
        useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)


   #####################################
   # Pruning
   #####################################

   name = "prunedn3z10rfac50"
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
        usePruning = cms.bool(True),
        nFilt = cms.int32(3),
        zcut = cms.double(0.1),
        rcut_factor = cms.double(0.5),
        useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)       
   li_fatjets_initial_objects.append(ungroomed_fj_name)    
   li_fatjets_branches.append(branch_name)


   #####################################
   # Trimming
   #####################################

   name = "trimmedr2f3"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
      useTrimming = cms.bool(True),
      rFilt = cms.double(0.2),
      trimPtFracMin = cms.double(0.03),
      useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)     
   li_fatjets_initial_objects.append(ungroomed_fj_name)      
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
   li_fatjets_initial_objects.append(ungroomed_fj_name)      
   li_fatjets_branches.append(branch_name)

   name = "trimmedr2f9"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
      useTrimming = cms.bool(True),
      rFilt = cms.double(0.2),
      trimPtFracMin = cms.double(0.09),
      useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)


   #####################################
   # Softdrop
   #####################################

   name = "softdropz10bm10"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.1),
           beta = cms.double(-1.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "softdropz10b00"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.1),
           beta = cms.double(0.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "softdropz10b10"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.1),
           beta = cms.double(1.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "softdropz10b20"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.1),
           beta = cms.double(2.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "softdropz15bm10"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.15),
           beta = cms.double(-1.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)     
   li_fatjets_initial_objects.append(ungroomed_fj_name)      
   li_fatjets_branches.append(branch_name)

   name = "softdropz15b00"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.15),
           beta = cms.double(0.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)     
   li_fatjets_initial_objects.append(ungroomed_fj_name)      
   li_fatjets_branches.append(branch_name)

   name = "softdropz15b10"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.15),
           beta = cms.double(1.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "softdropz15b20"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.15),
           beta = cms.double(2.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)


   name = "softdropz20b00"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.2),
           beta = cms.double(0.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)      
   li_fatjets_initial_objects.append(ungroomed_fj_name)     
   li_fatjets_branches.append(branch_name)

   name = "softdropz20bm10"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.2),
           beta = cms.double(-1.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "softdropz20b10"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.2),
           beta = cms.double(1.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)

   name = "softdropz20b20"   
   fj_name = ungroomed_fj_name + name
   branch_name = ungroomed_branch_name + name
   setattr(process, fj_name, ungroomed_fj.clone(
           useSoftDrop = cms.bool(True),
           zcut = cms.double(0.2),
           beta = cms.double(2.0),
           R0 = cms.double(r),
           useExplicitGhosts = cms.bool(True)))
   li_fatjets_objects.append(fj_name)        
   li_fatjets_initial_objects.append(ungroomed_fj_name)   
   li_fatjets_branches.append(branch_name)



#####################################
# JetCorrectors
#####################################

# AK8 / PF + CHS
process.corrL2 = cms.EDProducer(
    'LXXXCorrectorProducer',
    level     = cms.string('L2Relative'),
    algorithm = cms.string('AK8PFchs')
    )

process.corrL3 = cms.EDProducer(
    'LXXXCorrectorProducer',
    level     = cms.string('L3Absolute'),
    algorithm = cms.string('AK8PFchs')
    )

# L2L3 
process.corrL2L3 = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.VInputTag('corrL2','corrL3')
    )
process.corrL2L3chain = cms.Sequence(
    process.corrL2 * process.corrL3 * process.corrL2L3
)

# AK8 / PUPPI
process.corrL2Puppi = cms.EDProducer(
    'LXXXCorrectorProducer',
    level     = cms.string('L2Relative'),
    algorithm = cms.string('AK8PFPuppi')
    )

process.corrL3Puppi = cms.EDProducer(
    'LXXXCorrectorProducer',
    level     = cms.string('L3Absolute'),
    algorithm = cms.string('AK8PFPuppi')
    )

# L2L3 
process.corrL2L3Puppi = cms.EDProducer(
    'ChainedJetCorrectorProducer',
    correctors = cms.VInputTag('corrL2Puppi','corrL3Puppi')
    )
process.corrL2L3Puppichain = cms.Sequence(
    process.corrL2Puppi * process.corrL3Puppi * process.corrL2L3Puppi
)

corrector_ak8      = "corrL2L3"
corrector_ak8Puppi = "corrL2L3Puppi"

li_fatjets_correctors = []

for fj_obj_name in li_fatjets_objects:

   if "forbtag"  in fj_obj_name:
      print "NOT correcting subjets"
      li_fatjets_correctors.append("None")

   elif "GEN" in fj_obj_name:
      print "NOT correcting genjets"
      li_fatjets_correctors.append("None")

   elif "PUPPI" in fj_obj_name:
      if "ak08" in fj_obj_name:         
         li_fatjets_correctors.append(corrector_ak8Puppi)
      elif "ca15" in fj_obj_name:
         print "NOT correcting CA15 jets"
         li_fatjets_correctors.append("None")
      else:
         print "Could not find algorithm for", fj_obj_name
         sys.exit()

   elif "CHS" in fj_obj_name:
      if "ak08" in fj_obj_name:
         li_fatjets_correctors.append(corrector_ak8)
      elif "ca15" in fj_obj_name:
         print "NOT correcting CA15 jets"
         li_fatjets_correctors.append("None")
      else:
         print "Could not find algorithm for", fj_obj_name
         sys.exit()

   else:
      print "Could not find algorithm for", fj_obj_name
      sys.exit()


#####################################
# Flavour Infos
#####################################

li_fatjets_flavour_infos = []

for fj_obj_name in li_fatjets_objects:
   
   # These are subjets - don't need the flavour info at the moment
   if "forbtag" in fj_obj_name:
         li_fatjets_flavour_infos.append("None")
         continue

   # First extract algorithm and distance parameter
   if GetAlgoFromName(fj_obj_name) == "ca":
      algo = "CambridgeAachen"
   elif GetAlgoFromName(fj_obj_name) == "ak":
      algo = "AntiKt"
   r_param = GetRadiusFromName(fj_obj_name)

   flavour_info_name = fj_obj_name + "FlavourInfo"
   li_fatjets_flavour_infos.append(flavour_info_name)

   # Ungroomed Fatjet
   if fj_obj_name in li_ungroomed_fatjets_objects:
         setattr(process, flavour_info_name, cms.EDProducer("JetFlavourClustering",
                                                           jets           = cms.InputTag(fj_obj_name),
                                                           bHadrons       = cms.InputTag("selectedHadronsAndPartons","bHadrons"),
                                                           cHadrons       = cms.InputTag("selectedHadronsAndPartons","cHadrons"),
                                                           partons        = cms.InputTag("selectedHadronsAndPartons","algorithmicPartons"),
                                                           jetAlgorithm   = cms.string(algo),
                                                           rParam         = cms.double(r_param),
                                                           ghostRescaling = cms.double(1e-18),
                                                           hadronFlavourHasPriority = cms.bool(True)))
   # Ungroomed Fatjet
   else:
      for ungroomed_name in  li_ungroomed_fatjets_objects:
         if ungroomed_name in fj_obj_name:
            setattr(process, flavour_info_name, cms.EDProducer("JetFlavourClustering",
                                                              jets           = cms.InputTag(ungroomed_name),
                                                              groomedJets    = cms.InputTag(fj_obj_name),
                                                              bHadrons       = cms.InputTag("selectedHadronsAndPartons","bHadrons"),
                                                              cHadrons       = cms.InputTag("selectedHadronsAndPartons","cHadrons"),
                                                              partons        = cms.InputTag("selectedHadronsAndPartons","algorithmicPartons"),
                                                              jetAlgorithm   = cms.string(algo),
                                                              rParam         = cms.double(r_param),
                                                              ghostRescaling = cms.double(1e-18),
                                                              hadronFlavourHasPriority = cms.bool(True)))



#process.printEvent = cms.EDAnalyzer("printJetFlavourInfo",
#                                    jetFlavourInfos    = cms.InputTag("jetFlavourInfos"),
#                                    #subjetFlavourInfos = cms.InputTag("jetFlavourInfosAK8PFJets","SubJets"),
#                                    #groomedJets        = cms.InputTag("ak8PFJetsPruned"),
#)
#
#####################################
# NSubjettiness
#####################################

li_fatjets_nsubs = []
for fj_name in li_fatjets_objects:

   if "forbtag" in fj_name:
      li_fatjets_nsubs.append("None")

   else:
      nsub_name = fj_name + "Njettiness"

      r = GetRadiusFromName(fj_name)


      setattr(process, nsub_name, cms.EDProducer("NjettinessAdder",
                                                 src=cms.InputTag(fj_name),
                                                 Njets=cms.vuint32(1,2,3),          # compute 1-, 2-, 3- subjettiness
                                                 # variables for measure definition : 
                                                 measureDefinition = cms.uint32( 0 ), # CMS default is normalized measure
                                                 beta = cms.double(1.0),              # CMS default is 1
                                                 R0 = cms.double(r),                  # CMS default is jet cone size
                                                 Rcutoff = cms.double( +999.0),       # not used by default
                                                 # variables for axes definition :
                                                 axesDefinition = cms.uint32( 6 ),    # CMS default is 1-pass KT axes
                                                 nPass = cms.int32(+999),             # not used by default
                                                 akAxesR0 = cms.double(+999.0)        # not used by default
                                         ))
      li_fatjets_nsubs.append(nsub_name)


#####################################
# Shower Deconstruction
#####################################

li_fatjets_sds = []
for fj_name in li_fatjets_objects:
        
   # For Local Testing
   #sd_path = "../data/"
   # For Grid Submission
   sd_path = "src/TTH/TTHNtupleAnalyzer/data/"
        
   sd_fatjets = []
   #sd_fatjets = li_ungroomed_fatjets_objects
   
   r = GetRadiusStringFromName(fj_name)
   input_card = sd_path + "sd_input_card_{0}.dat".format(r)

   
   
   if fj_name in sd_fatjets:
        sd_name = fj_name + "SD"
        setattr(process, sd_name+"1", cms.EDProducer("SDProducer",
                                                     FatjetName = cms.string(fj_name),
                                                     MicrojetCone = cms.double(0.1), 
                                                     InputCard = cms.string(input_card)))

        setattr(process, sd_name+"2", cms.EDProducer("SDProducer",
                                                     FatjetName = cms.string(fj_name),
                                                     MicrojetCone = cms.double(0.2), 
                                                     InputCard = cms.string(input_card)))

        setattr(process, sd_name+"3", cms.EDProducer("SDProducer",
                                                     FatjetName = cms.string(fj_name),
                                                     MicrojetCone = cms.double(0.3), 
                                                     InputCard = cms.string(input_card)))

        li_fatjets_sds.append(sd_name)
   else:
        li_fatjets_sds.append('None')


#####################################
# QJets
#####################################

# Qjets need a RNG
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService")

li_fatjets_qvols = []
for i_fj, fj_name in enumerate(li_fatjets_objects):

   r = GetRadiusFromName(fj_name)           
   algo = GetAlgoFromName(fj_name)           
   
   qvol_fatjets = []#li_ungroomed_fatjets_objects

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
                                                      jetAlgo=cms.string(algo.upper()),
                                                      preclustering = cms.int32(50)))

           setattr(process.RandomNumberGeneratorService, qvol_name, cms.PSet(initialSeed = cms.untracked.uint32(i_fj),
                                                                             engineName = cms.untracked.string('TRandom3')))


           li_fatjets_qvols.append(qvol_name)

   else:
           li_fatjets_qvols.append('None')



#####################################
# CMS Top Tagger
#####################################

li_cmstt_objects  = []
li_cmstt_infos    = []
li_cmstt_branches = []

if DO_R08:
   # CMS TopTagger run on AK8 constituents!
   process.cmsTopTagAk08PFJetsCHS = cms.EDProducer(
           "CATopJetProducer",
           PFJetParameters,
           AnomalousCellParameters,
           CATopJetParameters,
           jetAlgorithm = cms.string("CambridgeAachen"), # CA is correct here! We already run on AK constituents! see below..
           rParam = cms.double(0.8),
           writeCompound = cms.bool(True),           
   )

   process.cmsTopTagAk08PFJetsCHS.jetCollInstanceName = cms.string("SubJets")
   process.cmsTopTagAk08PFJetsCHS.src = cms.InputTag("ak8PFJetsCHSConstituents", "constituents")
   process.cmsTopTagAk08PFJetsCHS.doAreaFastjet = cms.bool(True)
   process.cmsTopTagAk08PFJetsCHS.jetPtMin = cms.double(200.0)

   process.ak08CMSTopTagInfos = cms.EDProducer("CATopJetTagger",
                                               src = cms.InputTag("cmsTopTagAk08PFJetsCHS"),
                                               TopMass = cms.double(173),
                                               TopMassMin = cms.double(0.),
                                               TopMassMax = cms.double(250.),
                                               WMass = cms.double(80.4),
                                               WMassMin = cms.double(0.0),
                                               WMassMax = cms.double(200.0),
                                               MinMassMin = cms.double(0.0),
                                               MinMassMax = cms.double(200.0),
                                               verbose = cms.bool(False))

   li_cmstt_objects.append("cmsTopTagAk08PFJetsCHS")
   li_cmstt_infos.append("ak08CMSTopTagInfos")
   li_cmstt_branches.append("ak08cmstt")



   process.cmsTopTagAk08PFJetsPUPPI = cms.EDProducer(
           "CATopJetProducer",
           PFJetParameters,
           AnomalousCellParameters,
           CATopJetParameters,
           jetAlgorithm = cms.string("CambridgeAachen"), # CA is correct here! We already run on AK constituents! see below..
           rParam = cms.double(0.8),
           writeCompound = cms.bool(True),           
   )

   process.cmsTopTagAk08PFJetsPUPPI.jetCollInstanceName = cms.string("SubJets")
   process.cmsTopTagAk08PFJetsPUPPI.src = cms.InputTag("ak8PFJetsPUPPIConstituents", "constituents")
   process.cmsTopTagAk08PFJetsPUPPI.doAreaFastjet = cms.bool(True)
   process.cmsTopTagAk08PFJetsPUPPI.jetPtMin = cms.double(200.0)

   process.ak08PUPPICMSTopTagInfos = cms.EDProducer("CATopJetTagger",
                                               src = cms.InputTag("cmsTopTagAk08PFJetsPUPPI"),
                                               TopMass = cms.double(173),
                                               TopMassMin = cms.double(0.),
                                               TopMassMax = cms.double(250.),
                                               WMass = cms.double(80.4),
                                               WMassMin = cms.double(0.0),
                                               WMassMax = cms.double(200.0),
                                               MinMassMin = cms.double(0.0),
                                               MinMassMax = cms.double(200.0),
                                               verbose = cms.bool(False))

   li_cmstt_objects.append("cmsTopTagAk08PFJetsPUPPI")
   li_cmstt_infos.append("ak08PUPPICMSTopTagInfos")
   li_cmstt_branches.append("ak08puppicmstt")

if DO_R15:
   process.cmsTopTagCa15PFJetsCHS = cms.EDProducer(
           "CATopJetProducer",
           PFJetParameters,
           AnomalousCellParameters,
           CATopJetParameters,
           jetAlgorithm = cms.string("CambridgeAachen"),
           rParam = cms.double(1.5),
           writeCompound = cms.bool(True),
    )
   process.cmsTopTagCa15PFJetsCHS.jetCollInstanceName = cms.string("SubJets")
   process.cmsTopTagCa15PFJetsCHS.src = cms.InputTag('chs')
   process.cmsTopTagCa15PFJetsCHS.doAreaFastjet = cms.bool(True)
   process.cmsTopTagCa15PFJetsCHS.jetPtMin = cms.double(200.0)

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
                                               verbose = cms.bool(False),
   )

   li_cmstt_objects.append("cmsTopTagCa15PFJetsCHS")
   li_cmstt_infos.append("ca15CMSTopTagInfos")
   li_cmstt_branches.append("ca15cmstt")



   process.cmsTopTagCa15PFJetsPUPPI = cms.EDProducer(
           "CATopJetProducer",
           PFJetParameters,
           AnomalousCellParameters,
           CATopJetParameters,
           jetAlgorithm = cms.string("CambridgeAachen"),
           rParam = cms.double(1.5),
           writeCompound = cms.bool(True),
    )
   process.cmsTopTagCa15PFJetsPUPPI.jetCollInstanceName = cms.string("SubJets")
   process.cmsTopTagCa15PFJetsPUPPI.src = cms.InputTag('puppi')
   process.cmsTopTagCa15PFJetsPUPPI.doAreaFastjet = cms.bool(True)
   process.cmsTopTagCa15PFJetsPUPPI.jetPtMin = cms.double(200.0)

   process.ca15PUPPICMSTopTagInfos = cms.EDProducer("CATopJetTagger",
                                                    src = cms.InputTag("cmsTopTagCa15PFJetsPUPPI"),
                                                    TopMass = cms.double(173),
                                                    TopMassMin = cms.double(0.),
                                                    TopMassMax = cms.double(250.),
                                                    WMass = cms.double(80.4),
                                                    WMassMin = cms.double(0.0),
                                                    WMassMax = cms.double(200.0),
                                                    MinMassMin = cms.double(0.0),
                                                    MinMassMax = cms.double(200.0),
                                                    verbose = cms.bool(False),
   )

   li_cmstt_objects.append("cmsTopTagCa15PFJetsPUPPI")
   li_cmstt_infos.append("ca15PUPPICMSTopTagInfos")
   li_cmstt_branches.append("ca15puppicmstt")


#####################################
# b-tagging
#####################################

# Add b-tagging information for all fatjets
process.my_btagging = cms.Sequence()


li_fatjets_btags = []
li_cmstt_btags = []


for collection in ["fatjets", "cmstt"]:

   if collection == "fatjets":
      input_list = li_fatjets_objects
      output_list = li_fatjets_btags
   elif collection == "cmstt":
      input_list = li_cmstt_objects
      output_list = li_cmstt_btags

   for fatjet_name in input_list:

      if (collection == "fatjets" and "forbtag" in fatjet_name) or (collection == "cmstt"):

         # Define the names
         impact_info_name          = fatjet_name + "ImpactParameterTagInfos"
         sv_info_name              = fatjet_name + "secondaryVertexTagInfos"
         isv_info_name             = fatjet_name + "pfInclusiveSecondaryVertexFinderTagInfos"                 
         soft_mu_info_name         = fatjet_name + "softMuonTagInfos"
         soft_el_info_name         = fatjet_name + "softPFElectronsTagInfos"
         csvv2_computer_name       = fatjet_name + "combinedSecondaryVertexV2Computer"
         csvv2ivf_name             = fatjet_name + "pfCombinedInclusiveSecondaryVertexV2BJetTags"        
         cmva_name                 = fatjet_name + "combinedMVAV2BJetTags"

         delta_r = GetRadiusFromName(fatjet_name)

         # Setup the modules
         setattr(process, 
                 impact_info_name, 
                 process.pfImpactParameterTagInfos.clone(
                    primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
                    candidates = cms.InputTag("packedPFCandidates"),
                    jets = cms.InputTag(fatjet_name, "SubJets"),
                 ))
         getattr(process, impact_info_name).explicitJTA = cms.bool(True)

         setattr(process,
                 isv_info_name,                
                 process.pfInclusiveSecondaryVertexFinderTagInfos.clone(
                    extSVCollection               = cms.InputTag('slimmedSecondaryVertices'),
                    trackIPTagInfos               = cms.InputTag(impact_info_name),                
                 ))
         getattr(process, isv_info_name).useSVClustering = cms.bool(True)

         if GetAlgoFromName(fatjet_name) == "ca":
            getattr(process, isv_info_name).jetAlgorithm = cms.string("CambridgeAachen")
         elif GetAlgoFromName(fatjet_name) == "ak":
            getattr(process, isv_info_name).jetAlgorithm = cms.string("AntiKt")

         original_fatjet_name = fatjet_name
         original_fatjet_name = original_fatjet_name.replace("trimmedr2f6forbtag","")
         original_fatjet_name = original_fatjet_name.replace("softdropz10b00forbtag","")
         original_fatjet_name = original_fatjet_name.replace("softdropz20b10forbtag","")
         original_fatjet_name = original_fatjet_name.replace("filteredn3r2forbtag","")
         original_fatjet_name = original_fatjet_name.replace("filteredn3r3forbtag","")
         original_fatjet_name = original_fatjet_name.replace("prunedn3z10rfac50forbtag","")
         original_fatjet_name = original_fatjet_name.replace("cmsTopTagCa08PFJetsCHS","ca08PFJetsCHS")
         original_fatjet_name = original_fatjet_name.replace("cmsTopTagCa15PFJetsCHS","ca15PFJetsCHS")
         original_fatjet_name = original_fatjet_name.replace("cmsTopTagAk08PFJetsCHS","ak08PFJetsCHS")
         original_fatjet_name = original_fatjet_name.replace("cmsTopTagCa08PFJetsPUPPI","ca08PFJetsPUPPI")
         original_fatjet_name = original_fatjet_name.replace("cmsTopTagCa15PFJetsPUPPI","ca15PFJetsPUPPI")
         original_fatjet_name = original_fatjet_name.replace("cmsTopTagAk08PFJetsPUPPI","ak08PFJetsPUPPI")

         getattr(process, isv_info_name).rParam = cms.double(delta_r)
         getattr(process, isv_info_name).fatJets  =  cms.InputTag(original_fatjet_name)
         getattr(process, isv_info_name).groomedFatJets  =  cms.InputTag(fatjet_name)

         setattr(process,
                 csvv2_computer_name,
                 process.candidateCombinedSecondaryVertexV2Computer.clone())

         setattr(process,
                 csvv2ivf_name,
                 process.pfCombinedInclusiveSecondaryVertexV2BJetTags.clone(
                    tagInfos = cms.VInputTag(cms.InputTag(impact_info_name),
                                             cms.InputTag(isv_info_name)),
                    jetTagComputer = cms.string(csvv2_computer_name,)
                 ))
         
#         setattr(process,
#                 sv_info_name,
#                 process.secondaryVertexTagInfos.clone(
#                    extSVCollection     = cms.InputTag('slimmedSecondaryVertices'),
#                    trackIPTagInfos = cms.InputTag(impact_info_name), 
#                 ))
#
#         setattr(process,
#                 soft_mu_info_name,
#                 process.softMuonTagInfos.clone(
#                    primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
#                    jets = cms.InputTag(fatjet_name, "SubJets"),
#                    leptons = cms.InputTag("slimmedMuonds"),
#                 ))
#
#         setattr(process,
#                 soft_el_info_name,
#                 process.softPFElectronsTagInfos.clone(
#                    primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
#                    jets = cms.InputTag(fatjet_name, "SubJets"),
#                    electrons = cms.InputTag("slimmedElectrons"),
#                    )
#                 )
#
#         setattr(process,
#                 cmva_name,
#                 process.combinedMVAV2BJetTags.clone(             
#                    tagInfos = cms.VInputTag(
#                       cms.InputTag(impact_info_name), 
#                       cms.InputTag(sv_info_name), 
#                       cms.InputTag(isv_info_name),
#                       cms.InputTag(soft_mu_info_name),
#                       cms.InputTag(soft_el_info_name))))
#         
         
         # Add modules to sequence
         for module_name in [
               impact_info_name,
               isv_info_name,              
               #soft_mu_info_name,
               #soft_el_info_name,
               #sv_info_name,
               #cmva_name,
               csvv2ivf_name]:              
            process.my_btagging += getattr(process, module_name)

         # remember the module that actually produces the b-tag
         # discriminator so we can pass it to the NTupelizer
         output_list.append(csvv2ivf_name)

      else:
         output_list.append("None")

   # end of loop over fatjets
# end of loop over collections

#####################################
#  HEPTopTagger
#####################################

li_htt_branches = []

for input_object in ["chs", "puppi"]:
   
   name = "looseOptRHTT"
   if not input_object == "chs":
      name += input_object

   setattr(process, name, cms.EDProducer(
        "HTTTopJetProducer",
        PFJetParameters.clone( src = cms.InputTag(input_object),
                               doAreaFastjet = cms.bool(True),
                               doRhoFastjet = cms.bool(False),
                               jetPtMin = cms.double(100.0)
                           ),
        AnomalousCellParameters,
        jetCollInstanceName=cms.string("SubJets"),
        optimalR = cms.bool(True),
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
        maxM13Cut = cms.double(2.)))
   li_htt_branches.append(name)


#####################################
# NTupelizer
#####################################

li_fatjets_use_subjets = []
for fj in li_fatjets_objects:
   if "forbtag" in fj:
      li_fatjets_use_subjets.append(1)
   else:
      li_fatjets_use_subjets.append(0)

li_fatjets_is_gen = []
for fj in li_fatjets_objects:
   if "GEN" in fj:
      li_fatjets_is_gen.append(1)
   else:
      li_fatjets_is_gen.append(0)



process.tthNtupleAnalyzer = cms.EDAnalyzer('TTHNtupleAnalyzer',
	isMC = cms.bool(True),
	vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
	muons = cms.InputTag("slimmedMuons"),
	electrons = cms.InputTag("slimmedElectrons"),
	taus = cms.InputTag("slimmedTaus"),
	jets = cms.InputTag("slimmedJets"),
	genjets = cms.InputTag("slimmedGenJets"),
	generator = cms.InputTag("generator"),
        pupInfo   = cms.InputTag("slimmedAddPileupInfo"),                                   
         
	packed = cms.InputTag("packedGenParticles"),
	pruned = cms.InputTag("prunedGenParticles"),
	mets = cms.InputTag("slimmedMETs"),
	lhe = cms.InputTag("externalLHEProducer"),

        fatjetsObjects        = cms.vstring(li_fatjets_objects),
        fatjetsInitialObjects = cms.vstring(li_fatjets_initial_objects),
        fatjetsNsubs          = cms.vstring(li_fatjets_nsubs),
        fatjetsSDs            = cms.vstring(li_fatjets_sds),
        fatjetsBtags          = cms.vstring(li_fatjets_btags),
        fatjetsQvols          = cms.vstring(li_fatjets_qvols),
        fatjetsBranches       = cms.vstring(li_fatjets_branches),
        fatjetsUsesubjets     = cms.vint32(li_fatjets_use_subjets),                                           
        fatjetsIsgen          = cms.vint32(li_fatjets_is_gen),                                         
        fatjetsFlavourInfos   = cms.vstring(li_fatjets_flavour_infos),                                           
        fatjetsCorrectors     = cms.vstring(li_fatjets_correctors),                                           
        
        httObjects  = cms.vstring(li_htt_branches), # Using branch names also as object names
        httBranches = cms.vstring(li_htt_branches),                                           
                                           
        cmsttObjects  = cms.vstring(li_cmstt_objects),
        cmsttInfos    = cms.vstring(li_cmstt_infos),
        cmsttBranches = cms.vstring(li_cmstt_branches),
        cmsttBtags    = cms.vstring(li_cmstt_btags),

        particleCandidates = cms.InputTag("puppi"),
                                          
#        genPartonStatus = cms.untracked.int32(3),
)


process.TFileService = cms.Service("TFileService",
	fileName = cms.string(options.outputFile)
)


#####################################
# Schedule Algorithms
#####################################

process.p = cms.Path(process.chs)

process.p += process.puppi

process.p += process.selectedHadronsAndPartons

# Schedule AK08 Constituents
if DO_R08:
   process.p += process.ak08PFJetsCHS
   process.p += process.ak8PFJetsCHSConstituents
   process.p += process.ak08PFJetsPUPPI
   process.p += process.ak8PFJetsPUPPIConstituents



# Schedule all fatjets
for fj_name in li_fatjets_objects:   
   if not fj_name in ["ak08PFJetsCHS", "ak08PFJetsPUPPI"]: # Already added that before because we need it for AK08 Constituents
      process.p += getattr(process, fj_name)

# Schedule flavour info
for info_name in li_fatjets_flavour_infos:
   if not info_name == "None":
      process.p += getattr(process, info_name)

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
                
# Schedule Shower Deconstruction
for sd_name in li_fatjets_sds:
   if sd_name == "None":
      continue
   else:
      process.p += getattr(process, sd_name+"1")
      process.p += getattr(process, sd_name+"2")
      process.p += getattr(process, sd_name+"3")

# Schedule HEPTopTagger
for htt_name in li_htt_branches:
   process.p += getattr(process, htt_name)

# Schedule CMS Top Tagger
for x in li_cmstt_objects + li_cmstt_infos:
   process.p += getattr(process, x)

#process.p += process.jetFlavourInfos
#process.p += process.printEvent

process.p += process.corrL2L3chain
process.p += process.corrL2L3Puppichain

# Schedule b-tagging and Ntupelizer
for x in [process.my_btagging,
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


print li_fatjets_flavour_infos
