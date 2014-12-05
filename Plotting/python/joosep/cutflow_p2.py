import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms

process = cms.Process("MEAnalysisNew")

process.fwliteInput = cms.PSet(
    outFile = cms.string("outfile_p2.root"),
    samples = cms.VPSet([
        cms.PSet(
                 fileName=cms.string("/Users/joosep/Documents/tth/step2/s1_nov19_3a4602f__s2_b7e13a1/tthbb.root"),
                 nickName=cms.string("tthbb_13TeV"),
                 type=cms.int32(3),
                 process=cms.int32(0)
        ),
        cms.PSet(
                 fileName=cms.string("/Users/joosep/Documents/tth/step2/s1_nov19_3a4602f__s2_b7e13a1/ttjets.root"),
                 nickName=cms.string("ttjets_13TeV"),
                 type=cms.int32(3),
                 process=cms.int32(1)
        ),
        cms.PSet(
                 fileName=cms.string("/Users/joosep/Documents/tth/Apr23_2014/MEAnalysisNew_all_rec_std_TTH125.root"),
                 nickName=cms.string("tthbb_8TeV_ME"),
                 type=cms.int32(1),
                 process=cms.int32(0)
        ),
        cms.PSet(
                 fileName=cms.string("/Users/joosep/Documents/tth/Apr23_2014/MEAnalysisNew_all_rec_std_TTJets_nC.root"),
                 nickName=cms.string("ttjets_8TeV_ME"),
                 type=cms.int32(1),
                 process=cms.int32(1)
        ),
        cms.PSet(
                 fileName=cms.string("/Users/joosep/Documents/tth/MEAnalysisNew_all_ntuplizeAll_v3_rec_std_TTH125.root"),
                 nickName=cms.string("tthbb_8TeV_noME"),
                 type=cms.int32(0),
                 process=cms.int32(0)

        ),
        cms.PSet(
                 fileName=cms.string("/Users/joosep/Documents/tth/MEAnalysisNew_all_ntuplizeAll_v3_rec_std_TTJets_nC.root"),
                 nickName=cms.string("ttjets_8TeV_noME"),
                 type=cms.int32(0),
                 process=cms.int32(1)

        ),
        ]),
evLimits=cms.vint32(39482527, 78965054)
)
