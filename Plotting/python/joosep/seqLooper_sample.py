import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms

process = cms.Process("seqLooper")

process.inputs = cms.VPSet([
	cms.PSet(
		name = cms.string("step1"),
		type = cms.string("TTHSampleInput"),
		nJobsTotal = cms.int32(10),
		nJobCurrent = cms.int32(1),
		samples = cms.VPSet([
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
	for seq in seqlist:
		arr += [cms.PSet(
			name = cms.string(seq),
		)]
	process.sequences = cms.VPSet(arr)

#These sequences will be run
buildSequences([
	"MEAnalysisSeq",
	"slSeq",
	"dlSeq",
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
		name = cms.string("sl_analyzer"),
		type = cms.string("LeptonAnalyzer"),
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
		name = cms.string("dl_analyzer"),
		type = cms.string("LeptonAnalyzer"),
	),
])