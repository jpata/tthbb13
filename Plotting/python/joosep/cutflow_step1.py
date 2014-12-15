import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms

process = cms.Process("MEAnalysisNew")

process.fwliteInput = cms.PSet(
    samples = cms.VPSet([
        cms.PSet(
                 fileName=cms.string("/Users/joosep/Documents/tth/step1/nov19_3a4602f/tthbb.root"),
                 treeName=cms.string("tthNtupleAnalyzer/events"),
                 nickName=cms.string("tthbb_13TeV"),
                 type=cms.int32(3),
                 process=cms.int32(0)
        ),
        cms.PSet(
                 fileName=cms.string("/Users/joosep/Documents/tth/step1/nov19_3a4602f/ttjets.root"),
                 treeName=cms.string("events"),
                 nickName=cms.string("ttjets_13TeV"),
                 type=cms.int32(3),
                 process=cms.int32(1)
        ),
        ]),
        evLimits=cms.vint32(0, -1)
)
