import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms
import os

jobIdx = int(os.environ.get("JOBINDEX", 1))
process = cms.Process("seqLooper")

process.outputs = cms.PSet(
	outFileName = cms.string("output_{0}.root".format(jobIdx))
)

process.inputs = cms.VPSet([
	cms.PSet(
		name = cms.string("step1"),
		type = cms.string("TTHSampleInput"),
		nJobsTotal = cms.int32(4),
		nJobCurrent = cms.int32(jobIdx),
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

			cms.PSet(
				fileNamesS1=cms.vstring([]),
				fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/old/s2/MEAnalysisNew_all_ntuplizeAll_v3_rec_std_TTJets_nC.root"]),
				nickName=cms.string("ttjets_8TeV_noME"),
				fractionToProcess=cms.double(1.0),
				totalEvents=cms.int64(-1),
				type=cms.int32(0), #NOME_8TEV
				process=cms.int32(1), #TTJETS
				skip=cms.bool(False),
			),
			cms.PSet(
				fileNamesS1=cms.vstring([]),
				fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/old/s2/MEAnalysisNew_all_rec_std_TTJets_nC.root"]),
				nickName=cms.string("ttjets_8TeV_ME"),
				fractionToProcess=cms.double(1.0),
				totalEvents=cms.int64(-1),
				type=cms.int32(1), #ME_8TEV
				process=cms.int32(1), #TTJETS
				skip=cms.bool(False),
			),
			cms.PSet(
				fileNamesS1=cms.vstring([]),
				fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/s1_eb733a1/s2/ttjets_13tev_madgraph_pu20bx25_phys14.root"]),
				nickName=cms.string("ttjets_13TeV_phys14"),
				fractionToProcess=cms.double(1.0),
				totalEvents=cms.int64(-1),
				type=cms.int32(3), #ME_13TeV
				process=cms.int32(1), #TTJETS
				skip=cms.bool(True),
			),
		])
	)
])

def buildSequences(seqlist):
	arr = []
	for (seq, deps) in seqlist:
		arr += [cms.PSet(
			name = cms.string(seq),
			dependsOn = cms.vstring(deps),
		)]
	process.sequences = cms.VPSet(arr)

#These sequences will be run
buildSequences([
	("MEAnalysisSeq", []),
	("slSeq", ["MEAnalysisSeq"]),
	("slCatLSeq", ["MEAnalysisSeq", "slSeq"]),
	("slCatHSeq", ["MEAnalysisSeq", "slSeq"]),
	("sl4TagSeq", ["MEAnalysisSeq", "slSeq"]),
	("dlSeq", ["MEAnalysisSeq"]),
	("dlCatLSeq", ["MEAnalysisSeq", "dlSeq"]),
	("dlCatHSeq", ["MEAnalysisSeq", "dlSeq"]),
	("dl4TagSeq", ["MEAnalysisSeq", "dlSeq"]),
	#("PrintSeq", []),

])

process.MEAnalysisSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("seq1Events"),
		type = cms.string("EventPrinterAnalyzer"),
		printAll = cms.bool(False),
		processEvery = cms.int32(50000),
	),
	cms.PSet(
		name = cms.string("tth_metree"),
		type = cms.string("TTHMETreeAnalyzer"),
	),
])

process.slSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("SL"),
		type = cms.string("BoolSelector"),
		branch = cms.string("tth_metree__is_sl"),
		value = cms.bool(True),
	),
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
])

process.slCatLSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("SL"),
		type = cms.string("BoolSelector"),
		branch = cms.string("tth_metree__is_sl"),
		value = cms.bool(True),
	),
	cms.PSet(
		name = cms.string("SL_catL"),
		type = cms.string("IntSelector"),
		branch = cms.string("tth_metree__btag_lr_high_low"),
		value = cms.int32(0),
	),
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
	cms.PSet(
		name = cms.string("meplots"),
		type = cms.string("MEDiscriminatorAnalyzer"),
	),
])

process.slCatHSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("SL"),
		type = cms.string("BoolSelector"),
		branch = cms.string("tth_metree__is_sl"),
		value = cms.bool(True),
	),
	cms.PSet(
		name = cms.string("SL_catH"),
		type = cms.string("IntSelector"),
		branch = cms.string("tth_metree__btag_lr_high_low"),
		value = cms.int32(1),
	),
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
	cms.PSet(
		name = cms.string("meplots"),
		type = cms.string("MEDiscriminatorAnalyzer"),
	),
])

process.sl4TagSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("SL"),
		type = cms.string("BoolSelector"),
		branch = cms.string("tth_metree__is_sl"),
		value = cms.bool(True),
	),
	cms.PSet(
		name = cms.string("SL_4tag"),
		type = cms.string("IntSelector"),
		branch = cms.string("tth_metree__numTagsM"),
		value = cms.int32(4),
	),
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
	cms.PSet(
		name = cms.string("meplots"),
		type = cms.string("MEDiscriminatorAnalyzer"),
	),
])

process.dlSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("DL"),
		type = cms.string("BoolSelector"),
		branch = cms.string("tth_metree__is_dl"),
		value = cms.bool(True),
	),
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
])

process.dlCatLSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("DL"),
		type = cms.string("BoolSelector"),
		branch = cms.string("tth_metree__is_dl"),
		value = cms.bool(True),
	),
	cms.PSet(
		name = cms.string("DL_catL"),
		type = cms.string("IntSelector"),
		branch = cms.string("tth_metree__btag_lr_high_low"),
		value = cms.int32(0),
	),
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
	cms.PSet(
		name = cms.string("meplots"),
		type = cms.string("MEDiscriminatorAnalyzer"),
	),
])

process.dlCatHSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("DL"),
		type = cms.string("BoolSelector"),
		branch = cms.string("tth_metree__is_dl"),
		value = cms.bool(True),
	),
	cms.PSet(
		name = cms.string("DL_catH"),
		type = cms.string("IntSelector"),
		branch = cms.string("tth_metree__btag_lr_high_low"),
		value = cms.int32(1),
	),
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
	cms.PSet(
		name = cms.string("meplots"),
		type = cms.string("MEDiscriminatorAnalyzer"),
	),
])

process.dl4TagSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("DL"),
		type = cms.string("BoolSelector"),
		branch = cms.string("tth_metree__is_dl"),
		value = cms.bool(True),
	),
	cms.PSet(
		name = cms.string("DL_4tag"),
		type = cms.string("IntSelector"),
		branch = cms.string("tth_metree__numTagsM"),
		value = cms.int32(4),
	),
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
	cms.PSet(
		name = cms.string("meplots"),
		type = cms.string("MEDiscriminatorAnalyzer"),
	),
])

process.PrintSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("printer"),
		type = cms.string("TTHEventPrinterAnalyzer"),
	),
])