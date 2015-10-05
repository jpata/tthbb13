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

from TTH.MEAnalysis.MEAnalysis_heppy import sequence, samples
from TTH.MEAnalysis.samples_base import lfn_to_pfn
from TTH.MEAnalysis.samples_v12 import samples

firstEvent = int(os.environ["SKIP_EVENTS"])
nEvents = int(os.environ["MAX_EVENTS"])

fns = os.environ["FILE_NAMES"].split()

dataset = os.environ["DATASETPATH"]

# Added by Thomas:
#dataset = 'V11_tth_13tev'

print 'Dataset:'
print dataset
print 'Filenames:'
print fns

#Create a list of samples to run
#fill the subFiles of the samples from
#the supplied file names
good_samp = []
print "processing dataset={0}".format(dataset)

for ns in range(len(samples)):
    if samples[ns].name.value() == dataset:
        samples[ns].skip = False
        samples[ns].subFiles = map(lfn_to_pfn, samples[ns].subFiles ) #DS
        good_samp += [samples[ns]]
    else:
        print "skipping", samples[ns].name.value()
        samples[ns].skip = True

if len(good_samp) != 1:
    raise Exception("Need to specify at least one sample: dataset={0}, subfiles={1}".format(dataset, fns))
assert(len(good_samp) == 1)

print 'Running over sample: {0}'.format(good_samp)

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
    sample_ngen = s.nGen.value()
    if (sample_ngen<0):
        sample_ngen = getSampleNGen(s)
    inputSample = cfg.Component(
        'tth',
        files = s.subFiles.value(),
        tree_name = "tree",
        n_gen = sample_ngen,
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
