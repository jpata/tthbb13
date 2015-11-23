#This file knows about all the TTH samples as produced by the VHbb group
#LFN to PFN resolution is done with code in samples_base
#Cross-sections also defined in samples_base
from TTH.MEAnalysis.samples_base import *

sample_version = "V14"
path = "/home/joosep/joosep-mac/Documents/tth/data/ntp/v14/vhbb"
samples = cms.VPSet([
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttH'),
        xSec     = cms.double(0.5058),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([
            path + "/tth.root",
        ]),
        isMC     = cms.bool(True)
    ),
    # cms.PSet(
    #     skip     = cms.bool(False),
    #     name     = cms.string('ttjets'),
    #     xSec     = cms.double(0.5058),
    #     nGen     = cms.int64(-1),
    #     subFiles = cms.vstring([
    #         path + "/ttjets.root",
    #     ]),
    #     isMC     = cms.bool(True)
    # ),
    # cms.PSet(
    #     skip     = cms.bool(False),
    #     name     = cms.string('singlemu'),
    #     xSec     = cms.double(1),
    #     nGen     = cms.int64(-1),
    #     subFiles = cms.vstring([
    #         path + "/singlemu.root",
    #     ]),
    #     isMC     = cms.bool(False)
    # ),
])

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
