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

#New Spring14 processing
    cms.PSet(
        fileNamesS1=cms.vstring(["/hdfs/cms/store/user/jpata/tth/s1_eb733a1/TTHbb_s1_eb733a1_tth_hbb_13tev.root"]),
        fileNamesS2=cms.vstring(["/hdfs/cms/store/user/jpata/tth/s1_eb733a1__s2_3f71e05/tth_hbb_13tev.root"]),
        nickName=cms.string("tthbb_13TeV_spring14__s1_eb733a1__s2_3f71e05"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(3), #ME_13TeV
        process=cms.int32(0), #TTHBB
        skip=cms.bool(False),
    ),
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["/home/joosep/tth/gc/GC0b22bb43fb47/ttjets_13tev.root"]),
        nickName=cms.string("ttjets_13TeV_spring14__s1_eb733a1__s2_3f71e05"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(3), #ME_13TeV
        process=cms.int32(1), #TTJETS
        skip=cms.bool(True),
    ),

#New phys14 processing
    cms.PSet(
        fileNamesS1=cms.vstring(["/hdfs/cms/store/user/jpata/tth/s1_eb733a1/TTHbb_s1_eb733a1_tth_hbb_13tev_amcatnlo_pu20bx25_phys14.root"]),
        fileNamesS2=cms.vstring(["/hdfs/cms/store/user/jpata/tth/s1_eb733a1__s2_3f71e05/tth_hbb_13tev_amcatnlo_pu20bx25_phys14.root"]),
        nickName=cms.string("tthbb_13TeV_phys14"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(3), #ME_13TeV
        process=cms.int32(0), #TTHBB
        skip=cms.bool(False),
    ),
    cms.PSet(
        fileNamesS1=cms.vstring([]),
        fileNamesS2=cms.vstring(["/home/joosep/tth/gc/GC0b22bb43fb47/ttjets_13tev_madgraph_pu20bx25_phys14.root"]),
        nickName=cms.string("ttjets_13TeV_phys14"),
        fractionToProcess=cms.double(1.0),
        totalEvents=cms.int64(-1),
        type=cms.int32(3), #ME_13TeV
        process=cms.int32(1), #TTJETS
        skip=cms.bool(True),
    ),

#Old spring14 samples
    cms.PSet(
       fileNamesS1=cms.vstring([]),
       fileNamesS2=cms.vstring(["/hdfs/cms/store/user/jpata/tth/step2/s1_nov19_3a4602f__s2_b7e13a1/tthbb.root"]),
       nickName=cms.string("tthbb_13TeV_spring14__s1_3a4602f__s2_b7e13a1"),
       fractionToProcess=cms.double(1.0),
       totalEvents=cms.int64(-1),
       type=cms.int32(3),
       process=cms.int32(0),
       skip=cms.bool(False),
   ),
   cms.PSet(
       fileNamesS1=cms.vstring([]),
       fileNamesS2=cms.vstring(["/hdfs/cms/store/user/jpata/tth/step2/s1_nov19_3a4602f__s2_b7e13a1/ttjets.root"]),
       nickName=cms.string("ttjets_13TeV_spring14__s1_3a4602f__s2_b7e13a1"),
       fractionToProcess=cms.double(1.0),
       totalEvents=cms.int64(-1),
       type=cms.int32(3),
       process=cms.int32(1),
       skip=cms.bool(False),
   ),
])
