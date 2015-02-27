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
		nJobsTotal = cms.int32(1),
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
			# cms.PSet(
			# 	fileNamesS1=cms.vstring(["/home/joosep/mac-docs/tth/data/s1_eb733a1/s1/TTHbb_s1_eb733a1_tth_hbb_13tev_amcatnlo_pu20bx25_phys14.root"]),
			# 	fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/s1_eb733a1/s2/tth_hbb_13tev_amcatnlo_pu20bx25_phys14.root"]),
			# 	nickName=cms.string("tthbb_13TeV_phys14"),
			# 	fractionToProcess=cms.double(1.0),
			# 	totalEvents=cms.int64(-1),
			# 	type=cms.int32(3), #ME_13TeV
			# 	process=cms.int32(0), #TTHBB
			# 	skip=cms.bool(False),
			# ),
			# cms.PSet(
			# 	fileNamesS1=cms.vstring([]),
			# 	fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/old/s2/MEAnalysisNew_all_ntuplizeAll_v3_rec_std_TTJets_nC.root"]),
			# 	nickName=cms.string("ttjets_8TeV_noME"),
			# 	fractionToProcess=cms.double(1.0),
			# 	totalEvents=cms.int64(-1),
			# 	type=cms.int32(0), #NOME_8TEV
			# 	process=cms.int32(1), #TTJETS
			# 	skip=cms.bool(False),
			# ),
			# cms.PSet(
			# 	fileNamesS1=cms.vstring([]),
			# 	fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/old/s2/MEAnalysisNew_all_rec_std_TTJets_nC.root"]),
			# 	nickName=cms.string("ttjets_8TeV_ME"),
			# 	fractionToProcess=cms.double(1.0),
			# 	totalEvents=cms.int64(-1),
			# 	type=cms.int32(1), #ME_8TEV
			# 	process=cms.int32(1), #TTJETS
			# 	skip=cms.bool(False),
			# ),
			# cms.PSet(
			# 	fileNamesS1=cms.vstring([]),
			# 	fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/s1_eb733a1/s2/ttjets_13tev_madgraph_pu20bx25_phys14.root"]),
			# 	nickName=cms.string("ttjets_13TeV_phys14"),
			# 	fractionToProcess=cms.double(1.0),
			# 	totalEvents=cms.int64(-1),
			# 	type=cms.int32(3), #ME_13TeV
			# 	process=cms.int32(1), #TTJETS
			# 	skip=cms.bool(True),
			# ),
		])
	)
])

def buildSequences(seqlist):
	print seqlist
	arr = []
	for (seq, deps) in seqlist:
		arr += [cms.PSet(
			name = cms.string(seq),
			dependsOn = cms.vstring(deps),
		)]
	process.sequences = cms.VPSet(arr)

#These sequences will be run
seqs = [
	("MEAnalysisSeq", []),
	
	("BTagLRPosSeq", ["MEAnalysisSeq"]),
	("BTagLRLowHighSeq", ["MEAnalysisSeq"]),
	("BTagLRLowSeq", ["MEAnalysisSeq"]),
	("BTagLRHighSeq", ["MEAnalysisSeq"]),
	("BTagCount4Seq", ["MEAnalysisSeq"]),

	#("catSeq", ["
	("slSeq", ["MEAnalysisSeq"]),
		("slBlrSeq", ["slSeq", "BTagLRPosSeq"]),
		("slCatLHSeq", ["slSeq", "BTagLRLowHighSeq"]),
		("slCatLSeq", ["slSeq", "BTagLRLowSeq"]),
		("slCatHSeq", ["slSeq", "BTagLRHighSeq"]),
		("sl4TagSeq", ["slSeq", "BTagCount4Seq"]),

	("dlSeq", ["MEAnalysisSeq"]),
		("dlBlrSeq", ["dlSeq", "BTagLRPosSeq"]),
		("dlCatLHSeq", ["dlSeq", "BTagLRLowHighSeq"]),
		("dlCatLSeq", ["dlSeq", "BTagLRLowSeq"]),
		("dlCatHSeq", ["dlSeq", "BTagLRHighSeq"]),
		("dl4TagSeq", ["dlSeq", "BTagCount4Seq"]),

]

for cat in range(1,7):
	cat_seq = cms.VPSet([
		cms.PSet(
			name = cms.string("cat{0}".format(cat)),
			type = cms.string("IntSelector"),
			branch = cms.string("tth_metree__cat"),
			value = cms.int32(cat),
		),
	])

	sname = "cat{0}Seq".format(cat)
	seqs.insert(2, (sname, ["MEAnalysisSeq",]))
	setattr(process, sname, cat_seq)

	for lep in ["sl", "dl"]:
		for lrcut in ["LH", "L", "H"]:
			seq = cms.VPSet([
				cms.PSet(
					name = cms.string("cplots"),
					type = cms.string("LeptonAnalyzer"),
				),
				cms.PSet(
					name = cms.string("meplots"),
					type = cms.string("MEDiscriminatorAnalyzer"),
				),
			])
			sname = "{0}Cat{1}{2}Seq".format(lep, cat, lrcut)
			seqs += [(sname, ["cat{0}Seq".format(cat), lep + "Cat" + lrcut + "Seq"])]
			setattr(process, sname, seq)
#end for cat

process.BTagLRPosSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("BlrPos"),
		type = cms.string("DoubleRangeSelector"),
		branch = cms.string("tth_metree__btag_LR"),
		low = cms.double(0.0),
		high = cms.double(1.0),
	),
])

process.BTagLRLowHighSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("catLH"),
		type = cms.string("IntRangeSelector"),
		branch = cms.string("tth_metree__btag_lr_high_low"),
		low = cms.int32(0),
		high = cms.int32(2),
	),
])

process.BTagLRLowSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("catL"),
		type = cms.string("IntSelector"),
		branch = cms.string("tth_metree__btag_lr_high_low"),
		value = cms.int32(0),
	),
])

process.BTagLRHighSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("catH"),
		type = cms.string("IntSelector"),
		branch = cms.string("tth_metree__btag_lr_high_low"),
		value = cms.int32(1),
	),
])

process.BTagCount4Seq = cms.VPSet([
	cms.PSet(
		name = cms.string("4tag"),
		type = cms.string("IntSelector"),
		branch = cms.string("tth_metree__numBTagM"),
		value = cms.int32(4),
	),
])

buildSequences(seqs)

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

process.slBlrSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
	cms.PSet(
		name = cms.string("meplots"),
		type = cms.string("MEDiscriminatorAnalyzer"),
	),
])


process.slCatLHSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
	cms.PSet(
		name = cms.string("meplots"),
		type = cms.string("MEDiscriminatorAnalyzer"),
	),
])

process.slCatLSeq = cms.VPSet([
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
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
])

process.dlBlrSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
	cms.PSet(
		name = cms.string("meplots"),
		type = cms.string("MEDiscriminatorAnalyzer"),
	),
])


process.dlCatLHSeq = cms.VPSet([
	cms.PSet(
		name = cms.string("cplots"),
		type = cms.string("LeptonAnalyzer"),
	),
	cms.PSet(
		name = cms.string("meplots"),
		type = cms.string("MEDiscriminatorAnalyzer"),
	),
])

process.dlCatLSeq = cms.VPSet([
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