import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms
import os
import copy

#configure the job index through the environment
jobIdx = int(os.environ.get("JOBINDEX", 1))

#Create a process
process = cms.Process("looper")

#Configures the job output file
process.outputs = cms.PSet(
	outFileName = cms.string("output_{0}.root".format(jobIdx)),
)

#Configures the input files
#if first (last) event == -1, use 0 (Nentries-1)
#otherwise, process in specified range (inclusive)
process.inputs = cms.VPSet([
	cms.PSet(
		type = cms.string("TChainInput"),
		name = cms.string("tth"),
		treeName = cms.string("tree"),
		files = cms.VPSet([
			cms.PSet(
				fileName=cms.string(
					"/home/joosep/mac-docs/tth/data/ntp/v10/me6/tth_13tev.root"
				)
			)
		]),
		firstEvent=cms.int64(-1), #first event index
		lastEvent=cms.int64(-1) #last event index (inclusive)

	),
	cms.PSet(
		type = cms.string("TChainInput"),
		name = cms.string("ttjets"),
		treeName = cms.string("tree"),
		files = cms.VPSet([
			cms.PSet(
				fileName=cms.string(
					"/home/joosep/mac-docs/tth/data/ntp/v10/me6/ttjets_13tev_madgraph_pu20bx25_phys14.root"
				)
			)
		]),
		firstEvent=cms.int64(0), #first event index
		lastEvent=cms.int64(500000-1) #laste event index (inclusive)
	)
		
])

#The analysis is run as a series of Analyzers, each of which is
#defined through a PSet.
#Analyzers can be grouped to Sequences which are VPSets (list of PSets) and
#are executed linearly. An analyzer can be executed in multiple sequences,
#the program takes care of keeping the outputs separate.
#An Analyzer can filter an event, in which case the current sequence is not
#processed further. A sequence can depend on other sequences having passed the event
#giving the opportunity to construct logical clauses.
#All sequences are run in series as defined in the VPSet process.sequences,
#which lists the name and dependencies of each sequence to run.

#Define the single-lepton selection sequence
process.SL = cms.VPSet([

	#Select SL events
	cms.PSet(
		type = cms.string("IntSelector"),
		name = cms.string("is_sl"),
		branch = cms.string("is_sl"),
		value = cms.int32(1)
	),
	
	#Save jet and b-tag histograms for events passing SL
	cms.PSet(
		type = cms.string("JetHistogramAnalyzer"),
		name = cms.string("jets"),
	),
	cms.PSet(
		type = cms.string("BTagHistogramAnalyzer"),
		name = cms.string("btags"),
	),
])


#Define the quark gen-level matching sequences
#Require exactly 2 matches
process.match_wq = cms.VPSet([
	cms.PSet(
		type = cms.string("IntSelector"),
		name = cms.string("match_wq"),
		branch = cms.string("nMatch_wq"),
		value = cms.int32(2)
	),
])

process.match_hb = cms.VPSet([
	cms.PSet(
		type = cms.string("IntSelector"),
		name = cms.string("match_hb"),
		branch = cms.string("nMatch_hb"),
		value = cms.int32(2)
	),
])

process.match_tb = cms.VPSet([
	cms.PSet(
		type = cms.string("IntSelector"),
		name = cms.string("match_tb"),
		branch = cms.string("nMatch_tb"),
		value = cms.int32(2)
	),
])


#Define the "old" ME categories, requiring
#successful categorization based on njets, Wmass and number of b-tags
for i in [1,2,3]: #cat 1-3
	#btag L and H
	for btag_cut, btag_name in [
			(0, "L"), #btag low region (unimplemented)
			(1, "H") #btag high region
		]:
		cat = cms.VPSet([
			cms.PSet(
				type = cms.string("IntSelector"),
				name = cms.string("cat" + str(i)),
				branch = cms.string("cat"),
				value = cms.int32(i)
			),
			cms.PSet(
				type = cms.string("IntSelector"),
				name = cms.string("BTag"+btag_name),
				branch = cms.string("cat_btag"),
				value = cms.int32(btag_cut)
			),
		])
		setattr(process, "cat"+str(i) + btag_name, cat)

#List of all sequences that will be run
seqs = []

#Simple helper function to book sequences in a list
def addSeq(seqs, name, req=[]):
	seqs += [cms.PSet(
		name = cms.string(name),
		dependsOn = cms.vstring(req),
	)]
	
#Now book the sequences
addSeq(seqs, "SL")
for x in ["match_wq", "match_hb", "match_tb"]:
	addSeq(seqs, x, ["SL"])
for i in [1,2,3]:
	addSeq(seqs, "cat" + str(i) + "H", ["SL"])
	addSeq(seqs, "cat" + str(i) + "H" + "_MEM", ["SL"])

#Define the histograms that are drawn after evaluating the ME
analyzers = [
	cms.PSet(
		type = cms.string("JetHistogramAnalyzer"),
		name = cms.string("jets"),
	),
	cms.PSet(
		type = cms.string("BTagHistogramAnalyzer"),
		name = cms.string("btags"),
	),
	#Histograms for gen-level matching
	cms.PSet(
		type = cms.string("MatchAnalyzer"),
		name = cms.string("match"),
	),
]

#Define various ME histograms
#This is based on MEAnalysis_cfg_heppy.config.mem["methodsToRun"]
for i in range(6):
	analyzers += [
		cms.PSet(
			type = cms.string("MEAnalyzer"),
			name = cms.string("mem"+str(i)),
			label = cms.string(str(i)),
			MEindex = cms.int32(i),
		),
	]

#Add the ME histograms
process.cat1H_MEM = cms.VPSet(analyzers)
process.cat2H_MEM = cms.VPSet(analyzers)
process.cat3H_MEM = cms.VPSet(analyzers)

for (nj0, nj1, nt0, nt1) in [
	(5, 6, 2, 3), #5 jets, 2 tags
	(6, 999, 2, 3), #>= 6 jets, 2 tags
	(6, 999, 3, 4), #>= 6 jets, 3 tags
	(6, 999, 4, 999) #>= 6 jets, >=4 tags
	]:
	seq = cms.VPSet([
	
		#Select the required number of jets and tags
		cms.PSet(
			type = cms.string("IntRangeSelector"),
			name = cms.string("nj" + str(nj0)),
			branch = cms.string("njets"),
			low = cms.int32(nj0),
			high = cms.int32(nj1),
		),
		cms.PSet(
			type = cms.string("IntRangeSelector"),
			name = cms.string("nt" + str(nt0)),
			branch = cms.string("nBCSVM"),
			low = cms.int32(nt0),
			high = cms.int32(nt1),
		),
		
		#Draw histograms
		cms.PSet(
			type = cms.string("JetHistogramAnalyzer"),
			name = cms.string("jets"),
		),
		cms.PSet(
			type = cms.string("BTagHistogramAnalyzer"),
			name = cms.string("btags"),
		),
		
		cms.PSet(
			type = cms.string("MatchAnalyzer"),
			name = cms.string("match"),
		)] + analyzers
	)
	
	#add the sequence requiring no matching
	name = "JetTag{0}J{1}T".format(nj0, nt0)
	setattr(process, name, seq)
	
	#Book the histograms that run after requiring matching
	for x in [
		"wq", "hb", "tb", #2 matches for any W(qq), h(bb), t(b)
		"full", #H(bb), t(b), W(qq) all matched
		"wq_tb" #t(b), W(qq) matched
		]:
		setattr(process, name + "_match_" + x, copy.deepcopy(seq))
	
	#Here add the booked histograms to the sequence
	#dependsOn acts like an AND if-clause
	#dependsOn names have to match the names used in setattr
	#i.e. dependsOn(X) <-> process.X = myseq
	addSeq(seqs, name, ["SL"])
	for x in ["wq", "hb", "tb"]:
		addSeq(seqs, name + "_match_" + x, ["SL", "match_" + x])
	addSeq(seqs, name + "_match_full", ["SL", "match_wq", "match_hb", "match_tb"])
	addSeq(seqs, name + "_match_wq_tb", ["SL", "match_wq", "match_tb"])

#Finally, feed all the sequences in to process  
process.sequences = cms.VPSet(
	seqs
)

print process.dumpPython()
