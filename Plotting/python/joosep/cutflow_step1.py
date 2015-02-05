import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms

process = cms.Process("MEAnalysisNew")

process.fwliteInput = cms.PSet(
    samples = cms.VPSet([
        cms.PSet(
                 fileName=cms.string("/home/joosep/mac-docs/tth/data/jan28_8a4239/TTHbb_s1_8a4239_tth_hbb_13tev_pu20bx25_phys14.root"),
                 treeName=cms.string("tthNtupleAnalyzer/events"),
                 nickName=cms.string("tthbb_13TeV"),
                 type=cms.int32(3),
                 process=cms.int32(0)
        ),
        cms.PSet(
                 fileName=cms.string("/home/joosep/mac-docs/tth/data/jan28_8a4239/ttjets_small.root"),
                 treeName=cms.string("events"),
                 nickName=cms.string("ttjets_13TeV"),
                 type=cms.int32(3),
                 process=cms.int32(1)
        ),
        ]),
        evLimits=cms.vint32(0, -1)
)
