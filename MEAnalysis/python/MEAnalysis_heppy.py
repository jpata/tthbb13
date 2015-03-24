#!/usr/bin/env python
import os
import PhysicsTools.HeppyCore.framework.config as cfg
import ROOT
import imp

import itertools

#Import the default list of samples
from TTH.MEAnalysis.samples_vhbb import samples, sample_version, lfn_to_pfn

#Create configuration object based on environment variables
#if one runs with ME_CONF=/path/to/conffile.py, then the configuration is loaded from that file
#otherwise, the default config is used
if os.environ.has_key("ME_CONF"):
    print "Loading ME config from", os.environ["ME_CONF"]
    meconf = imp.load_source("meconf", os.environ["ME_CONF"])
    from meconf import Conf
else:
    print "Loading ME config from TTH.MEAnalysis.MEAnalysis_cfg_heppy"
    from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf

#Creates a new configuration object
conf = Conf()

#Load the input sample dictionary
#Samples are configured in the Conf object, by default, we use samples_vhbb
print "loading samples from", conf.general["sampleFile"]
samplefile = imp.load_source("samplefile", conf.general["sampleFile"])
from samplefile import samples_dict

#input component
#several input components can be declared,
#and added to the list of selected components
inputSamples = []
for s in samples_dict.values():
    inputSample = cfg.Component(
        s.nickName.value(),
        files = map(lfn_to_pfn, s.subFiles.value()),
        tree_name = "tree"
    )
    inputSample.isMC = s.isMC.value()
    inputSample.perJob = s.perJob.value()
    #use sample only if not skipped and subFiles defined
    if s.skip.value() == False and len(s.subFiles.value())>0:
        inputSamples.append(inputSample)

#Event contents are defined here
#This is work in progress
from TTH.MEAnalysis.VHbbTree import *

#This analyzer reads branches from event.input (the TTree/TChain) to event.XYZ (XYZ is e.g. jets, leptons etc)
evs = cfg.Analyzer(
    EventAnalyzer,
    'events',
)

#Here we define all the main analyzers
import TTH.MEAnalysis.MECoreAnalyzers as MECoreAnalyzers

#
evtid_filter = cfg.Analyzer(
    MECoreAnalyzers.EventIDFilterAnalyzer,
    'eventid',
    _conf = conf
)

#This class performs lepton selection and SL/DL disambiguation
leps = cfg.Analyzer(
    MECoreAnalyzers.LeptonAnalyzer,
    'leptons',
    _conf = conf
)

#This class performs jet selection and b-tag counting
jets = cfg.Analyzer(
    MECoreAnalyzers.JetAnalyzer,
    'jets',
    _conf = conf
)

#calculates the number of matched simulated B, C quarks for tt+XY matching
genrad = cfg.Analyzer(
    MECoreAnalyzers.GenRadiationModeAnalyzer,
    'genrad',
    _conf = conf
)

#calculates the b-tag likelihood ratio
btaglr = cfg.Analyzer(
    MECoreAnalyzers.BTagLRAnalyzer,
    'btaglr',
    _conf = conf
)

#assigns the ME category based on leptons, jets and the bLR
mecat = cfg.Analyzer(
    MECoreAnalyzers.MECategoryAnalyzer,
    'mecat',
    _conf = conf
)

#performs W-tag calculation on pairs of untagged jets
wtag = cfg.Analyzer(
    MECoreAnalyzers.WTagAnalyzer,
    'wtag',
    _conf = conf
)

#Calls the C++ MEM integrator with good_jets, good_leptons and
#the ME category
mem_analyzer = cfg.Analyzer(
    MECoreAnalyzers.MEAnalyzer,
    'mem',
    _conf = conf
)


gentth = cfg.Analyzer(
    MECoreAnalyzers.GenTTHAnalyzer,
    'gentth',
    _conf = conf
)

#Defines the output TTree
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
#Specifies what to save for jets
jetType = NTupleObjectType("jetType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("id", lambda x : x.id),
    NTupleVariable("btagCSV", lambda x : x.btagCSV),
    NTupleVariable("mcFlavour", lambda x : x.mcFlavour, type=int),
    NTupleVariable("mcMatchId", lambda x : x.mcMatchId, type=int),
    NTupleVariable("hadronFlavour", lambda x : x.hadronFlavour, type=int),
    NTupleVariable("mcPt", lambda x : x.mcPt),
    NTupleVariable("mcEta", lambda x : x.mcEta),
    NTupleVariable("mcPhi", lambda x : x.mcPhi),
    NTupleVariable("mcM", lambda x : x.mcM),
])
#Specifies what to save for leptons
leptonType = NTupleObjectType("leptonType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("pdgId", lambda x : x.pdgId),
    #NTupleVariable("mcPt", lambda x : x.mcPt),
    #NTupleVariable("mcEta", lambda x : x.mcEta),
    #NTupleVariable("mcPhi", lambda x : x.mcPhi),
    #NTupleVariable("mcMass", lambda x : x.mcMass),
])

memType = NTupleObjectType("memType", variables = [
    NTupleVariable("p", lambda x : x.p),
    NTupleVariable("p_err", lambda x : x.p_err),
    NTupleVariable("chi2", lambda x : x.chi2),
    NTupleVariable("time", lambda x : x.time),
    NTupleVariable("error_code", lambda x : x.error_code, type=int),
    NTupleVariable("efficiency", lambda x : x.efficiency),
    NTupleVariable("nperm", lambda x : x.num_perm, type=int),
])

#Create the output TTree writer
treeProducer = cfg.Analyzer(
    class_object = AutoFillTreeProducer,
    verbose = False,
    vectorTree = True,
    globalVariables = [
        NTupleVariable(
            "Wmass", lambda ev: ev.Wmass,
            help="best W boson mass from untagged pair (untagged by CSVM)"
        ),
        NTupleVariable(
            "is_sl", lambda ev: ev.is_sl,
            help="event is single-lepton"
        ),
        NTupleVariable(
            "is_dl", lambda ev: ev.is_dl,
            help="event is di-lepton"
        ),

        NTupleVariable(
            "cat", lambda ev: ev.catn,
            type=int,
            help="ME category"
        ),

        NTupleVariable(
            "cat_gen", lambda ev: ev.n_cat_gen,
            type=int,
            help="top decay category (-1 unknown, 0 single-leptonic, 1 di-leptonic, 2 fully hadronic)"
        ),

        NTupleVariable(
            "nGenBHiggs", lambda ev: len(ev.b_quarks_h),
            type=int,
            help="Number of generated b from higgs"
        ),

        NTupleVariable(
            "nGenBTop", lambda ev: len(ev.b_quarks_t),
            type=int,
            help="Number of generated b from top"
        ),

        NTupleVariable(
            "nGenQW", lambda ev: len(ev.l_quarks_w),
            type=int,
            help="Number of generated quarks from W"
        ),

        NTupleVariable(
            "nGenNuTop", lambda ev: len(ev.nu_top),
            type=int,
            help="Number of generated nu from top"
        ),

        NTupleVariable(
            "nGenLepTop", lambda ev: len(ev.lep_top),
            type=int,
            help="Number of generated charged leptons from top"
        ),

        NTupleVariable(
            "btag_LR_4b_2b_old", lambda ev: ev.btag_LR_4b_2b_old,
            help="B-tagging likelihood ratio: 4b vs 2b (8TeV CSV curves)"
        ),
        NTupleVariable(
            "btag_LR_4b_2b", lambda ev: ev.btag_LR_4b_2b,
            help="B-tagging likelihood ratio: 4b vs 2b"
        ),
        NTupleVariable(
            "btag_LR_4b_2b_alt", lambda ev: ev.btag_LR_4b_2b_alt,
            help="B-tagging likelihood ratio: 4b vs 2b with multi-dimensional pt/eta binning for CSV"
        ),
        NTupleVariable(
            "nMatchSimB", lambda ev: ev.nMatchSimB if hasattr(ev, "nMatchSimB") else 0,
            type=int,
            help="number of gen B not matched to top decay"
        ),
        NTupleVariable(
            "nMatchSimC", lambda ev: ev.nMatchSimC if hasattr(ev, "nMatchSimC") else 0,
            type=int,
            help="number of gen C not matched to W decay"
        ),

        NTupleVariable(
            "nBCSVM", lambda ev: ev.nBCSVM if hasattr(ev, "nBCSVM") else 0,
            type=int,
            help="Number of good jets passing CSVM"
        ),
        NTupleVariable(
            "nBCSVT", lambda ev: ev.nBCSVT if hasattr(ev, "nBCSVT") else 0,
            type=int,
            help="Number of good jets passing CSVT"
        ),
        NTupleVariable(
            "nBCSVL", lambda ev: ev.nBCSVL if hasattr(ev, "nBCSVL") else 0,
            type=int,
            help="Number of good jets passing CSVL"
        ),

        NTupleVariable(
            "nTrueBTaggedCSVM", lambda ev: ev.n_tagwp_tagged_true_bjets if hasattr(ev, "n_tagwp_tagged_true_bjets") else 0,
            type=int,
            help=""
        ),

        NTupleVariable(
            "nTrueBTaggedLR", lambda ev: ev.n_lr_tagged_true_bjets if hasattr(ev, "n_lr_tagged_true_bjets") else 0,
            type=int,
            help=""
        ),

        NTupleVariable(
            "nMatch_wq", lambda ev: ev.nMatch_wq if hasattr(ev, "nMatch_wq") else 0,
            type=int,
            help=""
        ),
        NTupleVariable(
            "nMatch_wq_btag", lambda ev: ev.nMatch_wq_btag if hasattr(ev, "nMatch_wq_btag") else 0,
            type=int,
            help=""
        ),

        NTupleVariable(
            "nMatch_tb", lambda ev: ev.nMatch_tb if hasattr(ev, "nMatch_tb") else 0,
            type=int,
            help=""
        ),
        NTupleVariable(
            "nMatch_tb_btag", lambda ev: ev.nMatch_tb_btag if hasattr(ev, "nMatch_tb_btag") else 0,
            type=int,
            help=""
        ),

        NTupleVariable(
            "nMatch_hb", lambda ev: ev.nMatch_hb if hasattr(ev, "nMatch_hb") else 0,
            type=int,
            help=""
        ),
        NTupleVariable(
            "nMatch_hb_btag", lambda ev: ev.nMatch_hb_btag if hasattr(ev, "nMatch_hb_btag") else 0,
            type=int,
            help=""
        ),

        NTupleVariable(
            "lheNj", lambda ev: ev.input.lheNj if hasattr(ev.input, "lheNj") else 0,
            type=int,
            help=""
        ),
        NTupleVariable(
            "lheNb", lambda ev: ev.input.lheNb if hasattr(ev.input, "lheNb") else 0,
            type=int,
            help=""
        ),
        NTupleVariable(
            "lheNc", lambda ev: ev.input.lheNc if hasattr(ev.input, "lheNc") else 0,
            type=int,
            help=""
        ),
        NTupleVariable(
            "lheNg", lambda ev: ev.input.lheNg if hasattr(ev.input, "lheNg") else 0,
            type=int,
            help=""
        ),
    ],
    #FIXME: fill these from the VHbb ntuples
    globalObjects = {},
    collections = {
    #standard dumping of objects
        "b_quarks_t" : NTupleCollection("GenBFromTop", leptonType, 3, help=""),
        "b_quarks_h" : NTupleCollection("GenBFromHiggs", leptonType, 3, help=""),
        "l_quarks_w" : NTupleCollection("GenQFromW", leptonType, 5, help=""),
        "good_jets" : NTupleCollection("jets", jetType, 8, help="Selected jets"),
        "good_leptons" : NTupleCollection("leps", leptonType, 2, help="Selected leptons"),
        "mem_results_tth" : NTupleCollection("mem_tth", memType, len(conf.mem["methodsToRun"]), help="MEM tth"),
        "mem_results_ttbb" : NTupleCollection("mem_ttbb", memType, len(conf.mem["methodsToRun"]), help="MEM ttbb"),
    }
)

#Override the default fillCoreVariables function, which
#by default looks for FWLite variables
#FIXME: this is a hack to run heppy on non-EDM formats. Better to propagate it to heppy
def fillCoreVariables(self, tr, event, isMC):
    for x in ["run", "lumi", "evt", "xsec", "nTrueInt", "puWeight", "genWeight"]:
        tr.fill(x, getattr(event.input, x))
AutoFillTreeProducer.fillCoreVariables = fillCoreVariables

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence([
    evtid_filter,
    evs,
    leps,
    jets,
    genrad,
    btaglr,
    wtag,
    mecat,
    gentth,
    mem_analyzer,
    treeProducer
])

#Book the output file
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='tree.root',
    option='recreate'
)

#finalization of the configuration object.
from PhysicsTools.HeppyCore.framework.chain import Chain as Events
config = cfg.Config(
    #Run across these inputs
    components = inputSamples,

    #Using this sequence
    sequence = sequence,

    #save output to these services
    services = [output_service],

    #This defines how events are loaded
    events_class = Events
)

if __name__ == "__main__":
    print "Running MEAnalysis heppy main loop"

    for samp in inputSamples:
        print "processing sample ", samp
        config = cfg.Config(
            #Run across these inputs
            components = [samp],

            #Using this sequence
            sequence = sequence,

            #save output to these services
            services = [output_service],

            #This defines how events are loaded
            events_class = Events
        )
        from PhysicsTools.HeppyCore.framework.looper import Looper
        nEvents = samp.perJob

        kwargs = {}
        if conf.general.get("eventWhitelist", None) is None:
            kwargs["nEvents"] = nEvents
        looper = Looper(
            'Loop_'+samp.name,
            config,
            nPrint = 0,
            **kwargs
        )

        #execute the code
        looper.loop()

        #write the output
        looper.write()

    #print summaries
    # for analyzer in looper.analyzers:
    #     print analyzer.name, "counters = {\n", analyzer.counters, "}"
