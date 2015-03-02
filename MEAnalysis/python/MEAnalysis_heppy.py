#!/usr/bin/env python
import os
import PhysicsTools.HeppyCore.framework.config as cfg
import ROOT

import itertools

from TTH.MEAnalysis.samples_vhbb import samples

# input component
# several input components can be declared,
# and added to the list of selected components
inputSamples = []
for s in samples:
    inputSample = cfg.Component(
        'tth',
        files = s.subFiles.value(),
        tree_name = "tree"
    )
    inputSample.isMC = s.isMC.value()
    inputSamples.append(inputSample)

selectedComponents  = inputSamples

from tree import *
evs = cfg.Analyzer(
    EventAnalyzer,
    'events',
)

lep_hists = {}
for x in ["mu", "good_sl_mu", "good_dl_mu", "el", "good_sl_el", "good_dl_el", "good_sl_lep", "good_dl_lep"]:
    lep_hists[x] = ROOT.TH1D("n_lep_"+x, "Number of leptons " + x, 5, 0, 5)

class Conf:
    def __init__(self):
        self.leptons = {
            "mu": {
                "tight": {
                    "pt": 30,
                    "eta":2.1,
                    "iso": 0.12
                },
                "tight_veto": {
                    "pt": 0.0,
                    "eta": 0.0,
                    "iso": 0.0,
                },
                "loose": {
                    "pt": 20,
                    "eta": 2.4,
                    "iso": 0.2,
                },
                "loose_veto": {
                    "pt": 0.0,
                    "eta": 0.0,
                    "iso": 0.0,
                },
                "isotype": "relIso03",
                "dxy": 0.2,

            },
            "el": {
                "tight": {
                    "pt": 30,
                    "eta": 2.5,
                    "iso": 0.1
                },
                "tight_veto": {
                    "pt": 20,
                    "eta": 2.5,
                    "iso": 0.15,
                },
                "loose": {
                    "pt": 20,
                    "eta": 2.2,
                    "iso": 0.15,
                },
                "loose_veto": {
                    "pt": 10,
                    "eta": 2.2,
                    "iso": 0.04,
                },
                "isotype": "relIso03",
                "dxy": 0.04,
            }
        }
        self.leptons["mu"]["tight_veto"] = self.leptons["mu"]["loose"]

        self.jets = {
            "pt": 40,
            "eta": 2.5,
            "btagAlgo": "btagCSV",
            "btagWP": "CSVM",
            "btagWPs": {"CSVM": ("btagCSV", 0.9)}
        }

conf = Conf()

import TTH.MEAnalysis.MECoreAnalyzers as MECoreAnalyzers

leps = cfg.Analyzer(
    MECoreAnalyzers.LeptonAnalyzer,
    'leptons',
    _conf = conf
)

jets = cfg.Analyzer(
    MECoreAnalyzers.JetAnalyzer,
    'jets',
    _conf = conf
)

genrad = cfg.Analyzer(
    MECoreAnalyzers.GenRadiationModeAnalyzer,
    'genrad',
    _conf = conf
)
btaglr = cfg.Analyzer(
    MECoreAnalyzers.BTagLRAnalyzer,
    'btaglr',
    _conf = conf
)

mecat = cfg.Analyzer(
    MECoreAnalyzers.MECategoryAnalyzer,
    'mecat',
    _conf = conf
)

wtag = cfg.Analyzer(
    MECoreAnalyzers.WTagAnalyzer,
    'wtag',
    _conf = conf
)

from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
treeProducer = cfg.Analyzer(
    class_object=AutoFillTreeProducer,
    verbose=False,
    vectorTree = True,
    globalVariables	= [
        NTupleVariable(
            "Wmass", lambda ev: ev.Wmass,
            help="best W boson mass from untagged pair (untagged by CSVM)"
        ),
        NTupleVariable(
            "Wmass2", lambda ev: ev.Wmass2,
            help="best W boson mass from untagged pair (untagged by LR)"
        ),
        NTupleVariable(
            "cat", lambda ev: ev.catn,
            type=int,
            help="ME category"
        ),
        NTupleVariable(
            "btag_LR_4b_2b", lambda ev: ev.btag_LR_4b_2b,
            help="B-tagging likelihood ratio: 4b vs 2b"
        ),
        NTupleVariable(
            "nMatchSimB", lambda ev: ev.nMatchSimB if hasattr(ev, "nMatchSimB") else 0,
            type=int,
            help=""
        ),
        NTupleVariable(
            "nMatchSimC", lambda ev: ev.nMatchSimC if hasattr(ev, "nMatchSimC") else 0,
            type=int,
            help=""
        ),
    ],
    globalObjects = {},
    collections = {}
)

#Override the default fillCoreVariables function, which
#by default looks for FWLite variables
def fillCoreVariables(self, tr, event, isMC):
    for x in ["run", "lumi", "evt", "xsec", "nTrueInt", "puWeight", "genWeight"]:
        tr.fill(x, getattr(event.input, x))
AutoFillTreeProducer.fillCoreVariables = fillCoreVariables

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    evs,
    leps,
    jets,
    #genrad,
    btaglr,
    mecat,
    wtag,
    treeProducer
])

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
config = cfg.Config( components = selectedComponents,
    sequence = sequence,
    services = [output_service],
    events_class = Events
)

print config

from PhysicsTools.HeppyCore.framework.looper import Looper
looper = Looper( 'Loop', config, nPrint = 0, nEvents = 1000)
looper.loop()
looper.write()

for analyzer in looper.analyzers:
    print analyzer.name, "counters = {\n", analyzer.counters, "}"
