#!/usr/bin/env python
import os
import PhysicsTools.HeppyCore.framework.config as cfg
import ROOT
import imp

import itertools

#pickle and transfer function classes to load transfer functions
import cPickle as pickle
import TTH.MEAnalysis.TFClasses as TFClasses

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

#Creates a new configuration object based on MEAnalysis_cfg_heppy
conf = Conf()

#Load transfer functions from pickle file
pi_file = open(conf.general["transferFunctionsPickle"] , 'rb')
conf.tf_matrix = pickle.load(pi_file)
pi_file.close()

#Load the input sample dictionary
#Samples are configured in the Conf object, by default, we use samples_vhbb
print "loading samples from", conf.general["sampleFile"]
samplefile = imp.load_source("samplefile", conf.general["sampleFile"])
from samplefile import samples_dict

#input component
#several input components can be declared,
#and added to the list of selected components
inputSamples = []
for sn in sorted(samples_dict.keys()):
    s = samples_dict[sn]
    inputSample = cfg.Component(
        s.nickName.value(),
        files = map(lfn_to_pfn, s.subFiles.value()),
        tree_name = "tree",
        n_gen = s.nGen.value(),
        xs = s.xSec.value()
    )
    inputSample.isMC = s.isMC.value()
    inputSample.perJob = s.perJob.value()
    #use sample only if not skipped and subFiles defined
    if s.skip.value() == False and len(s.subFiles.value())>0:
        inputSamples.append(inputSample)

print "Processing samples", [s.name for s in inputSamples]

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

evtweight = cfg.Analyzer(
    MECoreAnalyzers.EventWeightAnalyzer,
    'eventweight',
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

mva = cfg.Analyzer(
    MECoreAnalyzers.MVAVarAnalyzer,
    'mva',
    _conf = conf
)

treevar = cfg.Analyzer(
    MECoreAnalyzers.TreeVarAnalyzer,
    'treevar',
    _conf = conf
)
from TTH.MEAnalysis.metree import getTreeProducer
treeProducer = getTreeProducer(conf)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence([
    evtid_filter,
    evtweight,
    evs,
    leps,
    jets,
    btaglr,
    mva,
    wtag,
    mecat,
    genrad,
    gentth,
    mem_analyzer,
    treevar,
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

    #Process all samples in the sample list
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

        #Configure the number of events to run
        from PhysicsTools.HeppyCore.framework.looper import Looper
        nEvents = samp.perJob


        kwargs = {}
        if conf.general.get("eventWhitelist", None) is None:
            kwargs["nEvents"] = nEvents
        kwargs["firstEvent"] = conf.general.get("firstEvent", 0)
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
