import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms
import os
import copy
import ROOT

#configure the job index through the environment
JOBINDEX = os.environ.get("JOBINDEX", "all")
CHUNKSIZE = 100000

if JOBINDEX == "all":
    runChunks = False
else:
    runChunks = True

#Create a process
process = cms.Process("looper")

#Configures the job output file
process.outputs = cms.PSet(
    outFileName = cms.string("output_{0}.root".format(JOBINDEX)),
)

samples = {
    "tth": cms.PSet(
        type = cms.string("TChainInput"),
        name = cms.string("tth"),
        treeName = cms.string("tree"),
        files = cms.VPSet([
            cms.PSet(
                fileName=cms.string(
                    "/home/joosep/mac-docs/tth/data/ntp/v10/me/tth_13tev.root"
                )
            )
        ]),
        firstEvent=cms.int64(-1), #first event index
        lastEvent=cms.int64(-1), #last event index (inclusive)
        sampleTypeMajor = cms.uint32(1),
    ),
    "ttjets": cms.PSet(
        type = cms.string("TChainInput"),
        name = cms.string("ttjets"),
        treeName = cms.string("tree"),
        files = cms.VPSet([
            cms.PSet(
                fileName=cms.string(
                    "/home/joosep/mac-docs/tth/data/ntp/v10/me/ttjets_13tev_madgraph_pu20bx25_phys14.root"
                )
            )
        ]),
        firstEvent=cms.int64(0), #first event index
        lastEvent=cms.int64(-1), #last event index (inclusive)
        sampleTypeMajor = cms.uint32(2),
    ),
    "ttjets_bb": cms.PSet(
        type = cms.string("TChainInput"),
        name = cms.string("ttjets_bb"),
        treeName = cms.string("tree"),
        files = cms.VPSet([
            cms.PSet(
                fileName=cms.string(
                    "/home/joosep/mac-docs/tth/data/ntp/v10/me/ttjets_13tev_madgraph_pu20bx25_phys14_ttbb.root"
                )
            )
        ]),
        firstEvent=cms.int64(0), #first event index
        lastEvent=cms.int64(-1), #last event index (inclusive)
        sampleTypeMajor = cms.uint32(2),
    ),
    "ttjets_b": cms.PSet(
        type = cms.string("TChainInput"),
        name = cms.string("ttjets_b"),
        treeName = cms.string("tree"),
        files = cms.VPSet([
            cms.PSet(
                fileName=cms.string(
                    "/home/joosep/mac-docs/tth/data/ntp/v10/me/ttjets_13tev_madgraph_pu20bx25_phys14_ttb.root"
                )
            )
        ]),
        firstEvent=cms.int64(0), #first event index
        lastEvent=cms.int64(-1), #last event index (inclusive)
        sampleTypeMajor = cms.uint32(2),
    ),
    "ttjets_cc": cms.PSet(
        type = cms.string("TChainInput"),
        name = cms.string("ttjets_cc"),
        treeName = cms.string("tree"),
        files = cms.VPSet([
            cms.PSet(
                fileName=cms.string(
                    "/home/joosep/mac-docs/tth/data/ntp/v10/me/ttjets_13tev_madgraph_pu20bx25_phys14_ttcc.root"
                )
            )
        ]),
        firstEvent=cms.int64(0), #first event index
        lastEvent=cms.int64(-1), #last event index (inclusive)
        sampleTypeMajor = cms.uint32(2),
    ),
    "ttjets_ll": cms.PSet(
        type = cms.string("TChainInput"),
        name = cms.string("ttjets_ll"),
        treeName = cms.string("tree"),
        files = cms.VPSet([
            cms.PSet(
                fileName=cms.string(
                    "/home/joosep/mac-docs/tth/data/ntp/v10/me/ttjets_13tev_madgraph_pu20bx25_phys14_ttll.root"
                )
            )
        ]),
        firstEvent=cms.int64(0), #first event index
        lastEvent=cms.int64(-1), #last event index (inclusive)
        sampleTypeMajor = cms.uint32(2),
    )
}

if runChunks:
    chunks = []
    for sample in ["tth", "ttjets", "ttjets_bb", "ttjets_b", "ttjets_cc", "ttjets_ll"]:
        samp = samples[sample]
        fns = map(lambda x: x.fileName.value(), samp.files)
        tchain = ROOT.TChain("tree")
        for fn in fns:
            tchain.AddFile(fn)
        n = tchain.GetEntries()
        for i in range(0, n, CHUNKSIZE):
            samp = copy.deepcopy(samp)
            samp.firstEvent = i
            samp.lastEvent = i + CHUNKSIZE - 1
            chunks += [
                samp
            ]
    process.inputs = cms.VPSet([chunks[int(JOBINDEX)]])
    print "Running job", JOBINDEX, "/", len(chunks)-1, "(inclusive)"
else:
    #Configures the input files
    #if first (last) event == -1, use 0 (Nentries-1)
    #otherwise, process in specified range (inclusive)
    process.inputs = cms.VPSet([
        samples["tth"],
        samples["ttjets_bb"],
        samples["ttjets_b"],
        samples["ttjets_cc"],
        samples["ttjets_ll"],
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


#List of all sequences that will be run
seqs = []

#Simple helper function to book sequences in a list
def addSeq(seqs, name, req=[]):
    seqs += [cms.PSet(
        name = cms.string(name),
        dependsOn = cms.vstring(req),
    )]


def add_matching(seqs, seq, name, prereqs):
    setattr(process, name, copy.deepcopy(seq))
    addSeq(seqs, name, prereqs)
    #Book the histograms that run after requiring matching
    for x in [
        "wq", "hb", "tb",
        "w2_h2_t2",
        "w2_h0_t2",
        "w1_h2_t2",
        "w1_h0_t2",
        "w0_h2_t2",
        "w0_h0_t2"
        ]:
        #setattr(process, name + "_match_" + x, copy.deepcopy(seq))
        setattr(process, name + "_match_" + x + "_btag", copy.deepcopy(seq))

    #Here add the booked histograms to the sequence
    #dependsOn acts like an AND if-clause
    #dependsOn names have to match the names used in setattr
    #i.e. dependsOn(X) <-> process.X = myseq
    #
    #addSeq(seqs, name, ["SL"])
    #for x in ["wq", "hb", "tb"]:
    #    addSeq(seqs, name + "_match_" + x, prereqs + [name, "match2_" + x])
    #    addSeq(seqs, name + "_match_" + x + "_btag", prereqs + [name, "match2_" + x + "_btag"])
    #addSeq(seqs, name + "_match_w0_h2_t2", prereqs + [name, "match0_wq", "match2_hb", "match2_tb"])
    #addSeq(seqs, name + "_match_w0_h0_t2", prereqs + [name, "match0_wq", "match2_tb"])

    #addSeq(seqs, name + "_match_w1_h2_t2", prereqs + [name, "match1_wq", "match2_hb", "match2_tb"])
    #addSeq(seqs, name + "_match_w1_h0_t2", prereqs + [name, "match1_wq", "match2_tb"])

    #addSeq(seqs, name + "_match_w2_h2_t2", prereqs + [name, "match2_wq", "match2_hb", "match2_tb"])
    #addSeq(seqs, name + "_match_w2_h0_t2", prereqs + [name, "match2_wq", "match2_tb"])

    #2 quarks from W matched
    addSeq(seqs, name + "_match_w2_h2_t2_btag", prereqs + [name, "match2_wq_btag", "match2_hb_btag", "match2_tb_btag"])
    addSeq(seqs, name + "_match_w2_h0_t2_btag", prereqs + [name, "match2_wq_btag", "match2_tb_btag"])

    #1 quark from W matched
    addSeq(seqs, name + "_match_w1_h2_t2_btag", prereqs + [name, "match1_wq_btag", "match2_hb_btag", "match2_tb_btag"])
    addSeq(seqs, name + "_match_w1_h0_t2_btag", prereqs + [name, "match1_wq_btag", "match2_tb_btag"])

    #0 quark from W matched
    addSeq(seqs, name + "_match_w0_h2_t2_btag", prereqs + [name, "match0_wq_btag", "match2_hb_btag", "match2_tb_btag"])
    addSeq(seqs, name + "_match_w0_h0_t2_btag", prereqs + [name, "match0_wq_btag", "match2_tb_btag"])


#Define the single-lepton selection sequence
process.SL = cms.VPSet([

    #Require gen-level process
    cms.PSet(
        type = cms.string("GenLevelAnalyzer"),
        name = cms.string("gen"),
    ),

    #Select SL events
    cms.PSet(
        type = cms.string("IntSelector"),
        name = cms.string("is_sl"),
        branch = cms.string("is_sl"),
        value = cms.int32(1)
    ),

    #Save jet and b-tag histograms for events passing SL
    cms.PSet(
        type = cms.string("LeptonHistogramAnalyzer"),
        name = cms.string("leps"),
    ),
    cms.PSet(
        type = cms.string("JetHistogramAnalyzer"),
        name = cms.string("jets"),
    ),
    cms.PSet(
        type = cms.string("BTagHistogramAnalyzer"),
        name = cms.string("btags"),
    ),
])
#Now book the sequence so that it is run
addSeq(seqs, "SL")

for (nmu, nel, name) in [(1,1,"em"), (2,0,"mm"), (0,2,"ee")]:
    seq = cms.VPSet([
        #Require gen-level process
        cms.PSet(
            type = cms.string("GenLevelAnalyzer"),
            name = cms.string("gen"),
        ),

        cms.PSet(
            type = cms.string("IntSelector"),
            name = cms.string("is_dl"),
            branch = cms.string("is_dl"),
            value = cms.int32(1)
        ),
        cms.PSet(
            type = cms.string("IntSelector"),
            name = cms.string("n_mu_tight"),
            branch = cms.string("n_mu_tight"),
            value = cms.int32(nmu)
        ),
        cms.PSet(
            type = cms.string("IntSelector"),
            name = cms.string("n_el_tight"),
            branch = cms.string("n_el_tight"),
            value = cms.int32(nel)
        ),

        #Save jet and b-tag histograms for events passing SL
        cms.PSet(
            type = cms.string("LeptonHistogramAnalyzer"),
            name = cms.string("leps"),
        ),
        cms.PSet(
            type = cms.string("JetHistogramAnalyzer"),
            name = cms.string("jets"),
        ),
        cms.PSet(
            type = cms.string("BTagHistogramAnalyzer"),
            name = cms.string("btags"),
        ),
    ])

    setattr(process, "DL"+name, seq)
    addSeq(seqs, "DL"+name)

#Define the quark gen-level matching sequences
for x in ["wq", "hb", "tb"]:

    #number of required matches
    for n in [0, 1, 2]:
        name = "match{1}_{0}".format(x, n)
        s1 = cms.VPSet([
            cms.PSet(
                type = cms.string("IntSelector"),
                name = cms.string(name),
                branch = cms.string("nMatch_{0}".format(x)),
                value = cms.int32(n)
            ),
        ])
        setattr(process, name, s1)
        addSeq(seqs, name)

        s2 = cms.VPSet([
            cms.PSet(
                type = cms.string("IntSelector"),
                name = cms.string(name + "_btag"),
                branch = cms.string("nMatch_{0}_btag".format(x)),
                value = cms.int32(n)
            ),
        ])
        setattr(process, name + "_btag", s2)
        addSeq(seqs, name + "_btag")

#Define the histograms that are drawn after evaluating the ME
analyzers = [
    cms.PSet(
        type = cms.string("LeptonHistogramAnalyzer"),
        name = cms.string("leps"),
    ),
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
for i in range(9):
    analyzers += [
        cms.PSet(
            type = cms.string("MEAnalyzer"),
            name = cms.string("mem"+str(i)),
            MEindex = cms.int32(i),
        ),
    ]
analyzers += [
    cms.PSet(
        type = cms.string("MEMultiHypoAnalyzer"),
        name = cms.string("mem_comb"),
        formula = cms.string("([0]*[6]) / ([0]*[6] + 0.15*([1]*[7]))"),
    ),
]

#Define the "old" ME categories, requiring
#successful categorization based on njets, Wmass and number of b-tags
for i in [1, 2, 3, 6]: #cat 1-3
    #btag L and H
    for btag_cut, btag_name in [
        (-1, "L"), #btag low region (unimplemented)
        (1, "H") #btag high region
    ]:
        procs = [
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
        ]
        procs += analyzers
        cat = cms.VPSet(procs)

        name = "cat" + str(i) + btag_name
        if i != 6:
            addSeq(seqs, name, ["SL"])
            add_matching(seqs, cat, name, ["SL"])
        else:
            for n in ["ee", "em", "mm"]:
                addSeq(seqs, name+n, ["DL"+n])
                add_matching(seqs, cat, name+n, ["DL"+n])

#Matches are always calculated
for x in [
    "match0_wq", "match0_hb", "match0_tb",
    "match1_wq", "match1_hb", "match1_tb",
    "match2_wq", "match2_hb", "match2_tb"
    ]:
    addSeq(seqs, x, [])

for (nj0, nj1, nt0, nt1) in [
    (4, 5, 1, 2), #4 jets, 1 tags
    (4, 5, 2, 3), #4 jets, 2 tags
    (5, 6, 2, 3), #5 jets, 2 tags
    (5, 6, 3, 4), #5 jets, 3 tags
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
    add_matching(seqs, seq, name+"SL", ["SL"])
    for n in ["ee", "em", "mm"]:
        add_matching(seqs, seq, name+n, ["DL"+n])

#Finally, feed all the sequences in to process
process.sequences = cms.VPSet(
    seqs
)

print process.dumpPython()
