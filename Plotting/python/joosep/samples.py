import FWCore.ParameterSet.Config as cms

samples = cms.VPSet([
#old 8 TeV samples
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["~bianchi/CMSSW_5_3_3_patch2/src/Bianchi/TTHStudies/root//MEAnalysisNew_all_ntuplizeAll_v3_rec_std_TTH125.root"]),
        nickName=cms.string("tthbb_8TeV_noME"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(0), #NOME_8TEV
        process=cms.int32(0), #TTHBB
        skip=cms.bool(False),
    ),
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["~bianchi/CMSSW_5_3_3_patch2/src/Bianchi/TTHStudies/root/files/byLLR/Apr23_2014/MEAnalysisNew_all_rec_std_TTH125.root"]),
        nickName=cms.string("tthbb_8TeV_ME"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(1), #ME_8TEV
        process=cms.int32(0), #TTHBB
        skip=cms.bool(False),
    ),
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["~bianchi/CMSSW_5_3_3_patch2/src/Bianchi/TTHStudies/root//MEAnalysisNew_all_ntuplizeAll_v3_rec_std_TTJets_nC.root"]),
        nickName=cms.string("ttjets_8TeV_noME"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(0), #NOME_8TEV
        process=cms.int32(1), #TTJETS
        skip=cms.bool(False),
    ),
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["~bianchi/CMSSW_5_3_3_patch2/src/Bianchi/TTHStudies/root/files/byLLR/Apr23_2014/MEAnalysisNew_all_rec_std_TTJets_nC.root"]),
        nickName=cms.string("ttjets_8TeV_ME"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(1), #ME_8TEV
        process=cms.int32(1), #TTJETS
        skip=cms.bool(False),
    ),

#New phys14 processing
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/ntp/v10/me2/tth_13tev.root"]),
        nickName=cms.string("tth_13TeV_phys14"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(3), #ME_13TeV
        process=cms.int32(0), #TTHBB
        skip=cms.bool(False),
    ),
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/ntp/v10/me2/ttjets_13tev_madgraph_pu20bx25_phys14.root"]),
        nickName=cms.string("ttjets_13TeV_phys14"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(3), #ME_13TeV
        process=cms.int32(1), #TTJETS
        skip=cms.bool(False),
    ),
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/ntp/v10/me2/ttjets_13tev_madgraph_pu20bx25_phys14_ttbb.root"]),
        nickName=cms.string("ttjets_13TeV_phys14_bb"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(3), #ME_13TeV
        process=cms.int32(1), #TTJETS
        skip=cms.bool(False),
    ),
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/ntp/v10/me2/ttjets_13tev_madgraph_pu20bx25_phys14_ttb.root"]),
        nickName=cms.string("ttjets_13TeV_phys14_b"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(3), #ME_13TeV
        process=cms.int32(1), #TTJETS
        skip=cms.bool(False),
    ),
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/ntp/v10/me2/ttjets_13tev_madgraph_pu20bx25_phys14_ttcc.root"]),
        nickName=cms.string("ttjets_13TeV_phys14_cc"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(3), #ME_13TeV
        process=cms.int32(1), #TTJETS
        skip=cms.bool(False),
    ),
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/ntp/v10/me2/ttjets_13tev_madgraph_pu20bx25_phys14_ttll.root"]),
        nickName=cms.string("ttjets_13TeV_phys14_ll"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(3), #ME_13TeV
        process=cms.int32(1), #TTJETS
        skip=cms.bool(False),
    ),
])

samples_dict = {s.nickName.value(): s for s in samples}
