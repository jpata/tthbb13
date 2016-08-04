#!/usr/bin/env python
import os, logging, imp, itertools
import PhysicsTools.HeppyCore.framework.config as cfg

import ROOT
ROOT.gROOT.SetBatch(True)

#pickle and transfer function classes to load transfer functions
import cPickle as pickle
import TTH.MEAnalysis.TFClasses as TFClasses
import sys
sys.modules["TFClasses"] = TFClasses

#Import the default list of samples
from TTH.MEAnalysis.samples_base import getSitePrefix

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
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import conf_to_str

#Creates a new configuration object based on MEAnalysis_cfg_heppy
conf = Conf

#Load transfer functions from pickle file
logging.info("loading pickle file {0}".format(conf.general["transferFunctionsPickle"]))
pi_file = open(conf.general["transferFunctionsPickle"] , 'rb')
conf.tf_matrix = pickle.load(pi_file)

#Pre-compute the TF formulae
# eval_gen:specifies how the transfer functions are interpreted
#     If True, TF [0] - reco, x - gen
#     If False, TF [0] - gen, x - reco
#FIXME!!!: remove this flag in future versions!
eval_gen=False
conf.tf_formula = {}
for fl in ["b", "l"]:
    conf.tf_formula[fl] = {}
    for bin in [0, 1]:
            conf.tf_formula[fl][bin] = conf.tf_matrix[fl][bin].Make_Formula(eval_gen)

pi_file.close()

logging.info("loading pickle file {0}".format(conf.general["transferFunctions_sj_Pickle"]))
#Load the subjet transfer functions from pickle file
pi_file = open(conf.general["transferFunctions_sj_Pickle"] , 'rb')
conf.tf_sj_matrix = pickle.load(pi_file)
pi_file.close()
    

#Event contents are defined here
#This is work in progress
from TTH.MEAnalysis.vhbb_utils import EventAnalyzer

logging.info("creating analyzers")

#This analyzer reads branches from event.input (the TTree/TChain) to event.XYZ (XYZ is e.g. jets, leptons etc)
evs = cfg.Analyzer(
    EventAnalyzer,
    'events',
)

#Here we define all the main analyzers
import TTH.MEAnalysis.MECoreAnalyzers as MECoreAnalyzers

#
counter = cfg.Analyzer(
    MECoreAnalyzers.CounterAnalyzer,
    'counter',
    _conf = conf
)

evtid_filter = cfg.Analyzer(
    MECoreAnalyzers.EventIDFilterAnalyzer,
    'eventid',
    _conf = conf
)

pvana = cfg.Analyzer(
    MECoreAnalyzers.PrimaryVertexAnalyzer,
    'pvana',
    _conf = conf
)

trigger = cfg.Analyzer(
    MECoreAnalyzers.TriggerAnalyzer,
    'trigger',
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
    _conf = conf,
    btagAlgo = "btagCSV"
)

##calculates the b-tag likelihood ratio
#btaglr_bdt = cfg.Analyzer(
#    MECoreAnalyzers.BTagLRAnalyzer,
#    'btaglr_bdt',
#    _conf = conf,
#    btagAlgo = "btagBDT"
#)

#calculates the b-tag likelihood ratio
qglr = cfg.Analyzer(
    MECoreAnalyzers.QGLRAnalyzer,
    'qglr',
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

subjet_analyzer = cfg.Analyzer(
    MECoreAnalyzers.SubjetAnalyzer,
    'subjet',
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

brnd = cfg.Analyzer(
    MECoreAnalyzers.BTagRandomizerAnalyzer,
    'brand',
    _conf = conf
)

commoncls = cfg.Analyzer(
    MECoreAnalyzers.CommonClassifierAnalyzer,
    'brand',
    _conf = conf
)

treevar = cfg.Analyzer(
    MECoreAnalyzers.TreeVarAnalyzer,
    'treevar',
    _conf = conf
)
from TTH.MEAnalysis.metree import getTreeProducer
logging.info("building TreeProducer")
treeProducer = getTreeProducer(conf)
logging.info("building sequence")

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence([
    counter,
    evtid_filter,
    evs,
    pvana,
    trigger,
    leps,
    jets,
    brnd,
    btaglr,
    #btaglr_bdt,
    qglr,
    wtag,
    mecat,
    genrad,
    gentth,
    subjet_analyzer,
    commoncls,
    mem_analyzer,
    mva,
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
    components = [],

    #Using this sequence
    sequence = sequence,

    #save output to these services
    services = [output_service],

    #This defines how events are loaded
    events_class = Events
)

if __name__ == "__main__":
    print "Running MEAnalysis heppy main loop"
    logging.basicConfig(filename="MEAnalysis_heppy.log", level=logging.INFO)

    #input component
    #several input components can be declared,
    #and added to the list of selected components
    def prepareInputSamples(sampleFile=conf.general["sampleFile"]):
        print "loading samples from", sampleFile
        samplefile = imp.load_source("samplefile", sampleFile)
        from samplefile import samples_dict
        inputSamples = []
        for sn in sorted(samples_dict.keys()):
            s = samples_dict[sn]
            inputSample = cfg.Component(
                s.name.value(),
                files = map(getSitePrefix, s.subFiles.value()),
                tree_name = s.treeName.value(),
            )
            inputSample.isMC = s.isMC.value()
            inputSamples.append(inputSample)
        return inputSamples, samples_dict
    
    logging.info("preparing input samples")
    inputSamples, samples_dict = prepareInputSamples(conf.general["sampleFile"])
    
    #Process all samples in the sample list
    for samp in inputSamples:
        logging.info("processing sample {0}".format(samp))

        #Load the data event model
        if not samp.isMC:
            from TTH.MEAnalysis.VHbbTree_data import EventAnalyzer
            evs = cfg.Analyzer(
                EventAnalyzer,
                'events',
            )
            sequence[2] = evs

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
        nEvents = 300

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

        logging.info("creating looper")
        import cProfile, time
        p = cProfile.Profile(time.clock)
        p.runcall(looper.loop)
        p.print_stats()

        #execute the code
        #looper.loop()

        tf = looper.setup.services["outputfile"].file 
        tf.cd()
        ts = ROOT.TNamed("config", conf_to_str(Conf))
        ts.Write("", ROOT.TObject.kOverwrite)
        
        #write the output
        looper.write()
    #print summaries
    # for analyzer in looper.analyzers:
    #     print analyzer.name, "counters = {\n", analyzer.counters, "}"
