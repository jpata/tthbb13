#!/usr/bin/env python

#Need to enable ROOT batch mode to prevent it from importing libXpm, which may cause a crash
import ROOT
ROOT.gROOT.SetBatch(True)

import os
#pickle and transfer function classes to load transfer functions
import cPickle as pickle
import TTH.MEAnalysis.TFClasses as TFClasses
import sys
sys.modules["TFClasses"] = TFClasses

from TTH.MEAnalysis.MEAnalysis_heppy import sequence
from TTH.MEAnalysis.samples_base import lfn_to_pfn
from TTH.MEAnalysis.samples_722sync import samples

firstEvent = int(os.environ["SKIP_EVENTS"])
nEvents = int(os.environ["MAX_EVENTS"])

fns = os.environ["FILE_NAMES"].split()
dataset = os.environ["DATASETPATH"]

#Create a list of samples to run
#fill the subFiles of the samples from
#the supplied file names
good_samp = []
for ns in range(len(samples)):
    if samples[ns].nickName.value() == dataset:
        samples[ns].skip = False
        samples[ns].subFiles = map(lfn_to_pfn, fns)
        good_samp += [samples[ns]]
    else:
        samples[ns].skip = True

assert(len(good_samp) == 1)
outFileName = os.environ["MY_SCRATCH"] + "/output.root"

import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname="tree.root",
    option='recreate'
)

inputSamples = []
for s in samples:
    inputSample = cfg.Component(
        'tth',
        files = s.subFiles.value(),
        tree_name = "tree",
        n_gen = s.nGen.value(),
        xs = s.xSec.value()
    )
    inputSample.isMC = s.isMC.value()
    if s.skip.value() == False:
        inputSamples.append(inputSample)

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

from PhysicsTools.HeppyCore.framework.looper import Looper
looper = Looper('Loop',
    config,
    nPrint = 0,
    firstEvent=firstEvent,
    nEvents = nEvents
)

looper.loop()
looper.write()
