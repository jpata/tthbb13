#!/usr/bin/env python

#Need to enable ROOT batch mode to prevent it from importing libXpm, which may cause a crash
import ROOT
ROOT.gROOT.SetBatch(True)

import os
#pickle and transfer function classes to load transfer functions
import cPickle as pickle
#to prevent pickle import error
#== CMSSW:    File "MEAnalysis_heppy.py", line 33, in <module>
#== CMSSW:      conf.tf_matrix = pickle.load(pi_file)
#== CMSSW:    File "/cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/6.02.00-odfocd4/lib/ROOT.py", line 353, in _importhook
#== CMSSW:      return _orig_ihook( name, glbls, lcls, fromlist, level )
#== CMSSW:  ImportError: No module named TFClasses
import TTH.MEAnalysis.TFClasses as TFClasses
import sys
sys.modules["TFClasses"] = TFClasses

from TTH.MEAnalysis.MEAnalysis_heppy import sequence
from TTH.MEAnalysis.samples import samples_dict
from TTH.MEAnalysis.samples_base import getSitePrefix
import FWCore.ParameterSet.Config as cms

firstEvent = int(os.environ["SKIP_EVENTS"])
nEvents = int(os.environ["MAX_EVENTS"])
fns = os.environ["FILE_NAMES"].split()
dataset = os.environ["DATASETPATH"].split("__")[-1]

good_samp = []
print "processing dataset={0}".format(dataset)
print "event range firstEvent={0} nEvents={1}".format(firstEvent, nEvents)

for ns in samples_dict.keys():
    if samples_dict[ns].name.value() == dataset:
        samples_dict[ns].skip = cms.untracked.bool(False)
        samples_dict[ns].subFiles = map(getSitePrefix, fns ) #DS
        good_samp += [samples_dict[ns]]
    else:
        print "skipping", samples_dict[ns].name.value()
        samples_dict[ns].skip = cms.untracked.bool(True)

if len(good_samp) != 1:
    raise Exception("Need to specify at least one sample: dataset={0}, subfiles={1}, good_samp={2}".format(dataset, fns, good_samp))
assert(len(good_samp) == 1)

print 'Running over sample: {0}'.format(good_samp)

outFileName = os.environ["GC_SCRATCH"] + "/output.root"

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
for sn, s in samples_dict.items():
    inputSample = cfg.Component(
        'tth',
        files = s.subFiles.value(),
        tree_name = s.treeName.value(),
        n_gen = 1.0,
        xs = 1.0
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
    nEvents=nEvents
)

looper.loop()
looper.write()
