import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms

process = cms.Process("MEAnalysisNew")

process.fwliteInput = cms.PSet(
	outFile = cms.string("outfile2.root"),
	elePt=cms.double(-1),
	muPt=cms.double(-1),

    samples = cms.VPSet([
        cms.PSet(
            fileNamesS1=cms.vstring([]),
            fileNamesS2=cms.vstring(["/Users/joosep/Documents/tth/data/old/s2/MEAnalysisNew_all_ntuplizeAll_v3_rec_std_TTH125.root"]),
            nickName=cms.string("tthbb_8TeV_noME"),
            fractionToProcess=cms.double(1.0),
            totalEvents=cms.int64(-1),
            type=cms.int32(0), #NOME_8TEV
            process=cms.int32(0), #TTHBB
            skip=cms.bool(False),
        ),
        cms.PSet(
            fileNamesS1=cms.vstring([]),
            fileNamesS2=cms.vstring(["/Users/joosep/Documents/tth/data/old/s2/MEAnalysisNew_all_rec_std_TTH125.root"]),
            nickName=cms.string("tthbb_8TeV_ME"),
            fractionToProcess=cms.double(1.0),
            totalEvents=cms.int64(-1),
            type=cms.int32(1), #ME_8TEV
            process=cms.int32(0), #TTHBB
            skip=cms.bool(False),
        ),
        cms.PSet(
            fileNamesS1=cms.vstring(["/home/joosep/mac-docs/tth/data/s1_eb733a1/s1/TTHbb_s1_eb733a1_tth_hbb_13tev_amcatnlo_pu20bx25_phys14.root"]),
            fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/s1_eb733a1/s2/tth_hbb_13tev_amcatnlo_pu20bx25_phys14.root"]),
            nickName=cms.string("tthbb_13TeV_phys14"),
            fractionToProcess=cms.double(1.0),
            totalEvents=cms.int64(-1),
            type=cms.int32(3), #ME_13TeV
            process=cms.int32(0), #TTHBB
            skip=cms.bool(False),
        ),
    ]),
    evLimits=cms.vint64(0, -1)
)
