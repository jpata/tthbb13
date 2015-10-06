#This file knows about all the TTH samples as produced by the VHbb group
#LFN to PFN resolution is done with code in samples_base
#Cross-sections also defined in samples_base
from TTH.MEAnalysis.samples_base import *

sample_version = "V12"
path = "/home/joosep/joosep-mac/Documents/tth/data/ntp/v12/vhbb"
samples = cms.VPSet([

    #tt + jets
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('TT_TuneCUETP8M1_13TeV-powheg-pythia8'),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([
        path + "/ttjets_powheg.root",
        ]),
        isMC     = cms.bool(True)
    ),

    #tt + jets
    cms.PSet(
        skip     = cms.bool(True),
        name     = cms.string('TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([
        path + "/ttjets_amcatnlo.root",
        ]),
        isMC     = cms.bool(True)
    ),


    ##tt + H
    #tth_hbb_13tev_amcatnlo_pu20bx25_spring15 3933403.0 3933403.0 0.0
    cms.PSet(
        skip     = cms.bool(True),
        name     = cms.string('ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8'),
        xSec     = cms.double(0.5058),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([
        path + "/tth_amcatnlo.root",
        ]),
        isMC     = cms.bool(True)
    ),
    
    cms.PSet(
        skip     = cms.bool(True),
        name     = cms.string('ttHTobb_M125_13TeV_powheg_pythia8'),
        xSec     = cms.double(0.5058),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([
            path + "/tth_powheg.root",
        ]),
        isMC     = cms.bool(True)
    ),
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
