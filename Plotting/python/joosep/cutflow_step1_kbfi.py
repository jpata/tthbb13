import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms

process = cms.Process("MEAnalysisNew")

process.fwliteInput = cms.PSet(
    samples = cms.VPSet([
        cms.PSet(
             fileName=cms.string("/hdfs/cms/store/user/jpata/tth/nov19_3a4602f/tthbb.root"),
             nickName=cms.string("tthbb_13TeV"),
             type=cms.int32(3),
             process=cms.int32(0)
        ),
        cms.PSet(
             fileName=cms.string("/hdfs/cms/store/user/jpata/tth/nov19_3a4602f/ttjets.root"),
             nickName=cms.string("ttjets_13TeV"),
             type=cms.int32(3),
             process=cms.int32(1)
        ),
        ]),
        evLimits=cms.vint32(0, -1)
)
