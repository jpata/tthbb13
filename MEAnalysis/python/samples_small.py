#This file knows about all the TTH samples as produced by the VHbb group
#LFN to PFN resolution is done with code in samples_base
#Cross-sections also defined in samples_base
from TTH.MEAnalysis.samples_base import *
import copy

sample_version = "local"

#nickName - string to identify the sample
#name - full name of the sample, currently same as nickName
#perJob - the number of events per job for the MEM code (unused) [events per job]
#xSec - the cross-section [pb]
#nGen - the number of true generated events in the MC sample, used for normalization [number of events]
#       if nGen == -1, then assumed to be unknown and taken from counter histogram in file
#Subfiles - list of strings with PFN/LFN for the files.
#Skip - boolean which controls if the sample is processed or not by default

#ttjets_13tev_amcatnlo_pu20bx25_spring15 39709360.0 26437549.0 13271811.0
basesamples = cms.VPSet([

    ##tt + H
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev_powheg_pu20bx25_spring15'),
        nickName = cms.string('tth_hbb_13tev_powheg_pu20bx25_spring15'),
        xSec     = cms.double(0.5058),
        nGen     = cms.int64(-1),
        perJob   = cms.uint32(1000),
        subFiles = cms.vstring([
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_10/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_11/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_12/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_13/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_14/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_15/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_16/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_17/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_18/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_19/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_1/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_20/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_21/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_22/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_23/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_24/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_25/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_26/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_2/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_3/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_4/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_5/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_6/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_7/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_8/tree.root",
            "file:///shome/jpata/tth/sw/CMSSW/src/VHbbAnalysis/Heppy/test/Loop_tth_9/tree.root",
        ]),
        isMC     = cms.bool(True)
    ),
])

samples = []
for sample in basesamples:
    i = 0
    for f in sample.subFiles:
        newsamp = copy.deepcopy(sample)
        newsamp.subFiles = [f]
        newsamp.name = newsamp.name.value() + "_{0}".format(i) 
        samples += [newsamp]
        i += 1

#fill sample number of generated
for s in samples:
    if s.nGen.value() < 0:
        s.nGen = cms.int64(getSampleNGen(s))
        print s.name, "ngen", s.nGen
#This contains the samples, but accessible by nickName
samples_dict = {s.name.value(): s for s in samples}
if __name__ == "__main__":
    for sn, sample in samples_dict.items():
        print sample
