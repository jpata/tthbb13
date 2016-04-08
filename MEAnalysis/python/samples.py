# THIS IS AN AUTOGENERATED FILE
# Made by prepareSamples.py
# do NOT modify (except to skip individual samples)


from TTH.MEAnalysis.samples_base import *
import FWCore.ParameterSet.Config as cms

version = "VHBBHeppyV21_tthbbV6"
datasetpath = "src/TTH/MEAnalysis/gc/datasets/VHBBHeppyV21_tthbbV6/"
samples_dict = {
    
        "TTTo2L2Nu_13TeV-powheg": cms.PSet(
            name     = cms.string("TTTo2L2Nu_13TeV-powheg"),
            nickname = cms.string("TTTo2L2Nu_13TeV-powheg"),
            xSec     = cms.double("1"),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            treeName = cms.string("vhbb/tree"),
            subFiles = cms.vstring(get_files(datasetpath + "TTTo2L2Nu_13TeV-powheg.txt")),
        ),
        
        "ttHTobb_M125_13TeV_powheg_pythia8": cms.PSet(
            name     = cms.string("ttHTobb_M125_13TeV_powheg_pythia8"),
            nickname = cms.string("ttH_Hbb"),
            xSec     = cms.double("0.2934045"),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            treeName = cms.string("vhbb/tree"),
            subFiles = cms.vstring(get_files(datasetpath + "ttHTobb_M125_13TeV_powheg_pythia8.txt")),
        ),
        
        "TT_TuneCUETP8M1_13TeV-powheg-pythia8": cms.PSet(
            name     = cms.string("TT_TuneCUETP8M1_13TeV-powheg-pythia8"),
            nickname = cms.string("TT_TuneCUETP8M1_13TeV-powheg-pythia8"),
            xSec     = cms.double("831.76"),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            treeName = cms.string("vhbb/tree"),
            subFiles = cms.vstring(get_files(datasetpath + "TT_TuneCUETP8M1_13TeV-powheg-pythia8.txt")),
        ),
        
        "ttHToNonbb_M125_13TeV_powheg_pythia8": cms.PSet(
            name     = cms.string("ttHToNonbb_M125_13TeV_powheg_pythia8"),
            nickname = cms.string("ttH_Hnonbb"),
            xSec     = cms.double("0.2150955"),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            treeName = cms.string("vhbb/tree"),
            subFiles = cms.vstring(get_files(datasetpath + "ttHToNonbb_M125_13TeV_powheg_pythia8.txt")),
        ),
        
        "TTToSemiLeptonic_13TeV-powheg": cms.PSet(
            name     = cms.string("TTToSemiLeptonic_13TeV-powheg"),
            nickname = cms.string("TTToSemiLeptonic_13TeV-powheg"),
            xSec     = cms.double("1"),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            treeName = cms.string("vhbb/tree"),
            subFiles = cms.vstring(get_files(datasetpath + "TTToSemiLeptonic_13TeV-powheg.txt")),
        ),
    }
