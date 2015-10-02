#This file knows about all the TTH samples as produced by the VHbb group
#LFN to PFN resolution is done with code in samples_base
#Cross-sections also defined in samples_base
from TTH.MEAnalysis.samples_base import *

sample_version = "V13_pre"

#nickname - string to identify the sample
#name - full name of the sample, currently same as nickName
#perJob - the number of events per job for the MEM code (unused) [events per job]
#xSec - the cross-section [pb]
#nGen - the number of true generated events in the MC sample, used for normalization [number of events]
#       if nGen == -1, then assumed to be unknown and taken from counter histogram in file
#Subfiles - list of strings with PFN/LFN for the files.
#Skip - boolean which controls if the sample is processed or not by default


samples = cms.VPSet([

    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttHToNonbb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2'),
        nickname = cms.string("ttH_nohbb"),
        xSec     = cms.double(0.5058 * (1.0 - 0.569)),
        nGen     = cms.int64(3800595),
        subFiles = cms.vstring([
        ]),
        isMC     = cms.bool(True)
    ),
    
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1'),
        nickname = cms.string("ttH_hbb"),
        xSec     = cms.double(0.5058 * 0.569),
        nGen     = cms.int64(3933403),
        subFiles = cms.vstring([
            ]),
        isMC     = cms.bool(True)
    ),

    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1'),
        nickname = cms.string("ttw_wlnu"),
        xSec     = cms.double(1.152 * (1.0 - 0.676)),
        nGen     = cms.int64(129850),
        subFiles = cms.vstring([
        ]),
        isMC     = cms.bool(True)
    ),

    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1'),
        nickname = cms.string("ttw_wqq"),
        xSec     = cms.double(1.152 * 0.676),
        nGen     = cms.int64(430330),
        subFiles = cms.vstring([
                    ]),
                    isMC     = cms.bool(True)
                ),
            
            
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1'),
        nickname = cms.string("ttz_zllnunu"),
        xSec     = cms.double(2.232 * (3 * 0.03365 + 0.2)),
        nGen     = cms.int64(184989),
        subFiles = cms.vstring([
        ]),
        isMC     = cms.bool(True)
    ),

    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1'),
        nickname = cms.string("ttz_zqq"),
        xSec     = cms.double(2.232 * 0.699),
        nGen     = cms.int64(351398),
        subFiles = cms.vstring([
        ]),
        isMC     = cms.bool(True)
    ),

    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2'),
        nickname = cms.string("ttjets"),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(19899492),
        subFiles = cms.vstring([
        ]),
        isMC     = cms.bool(True)
    ),
    
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9_ext3-v1'),
        nickname = cms.string("ttjets"),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(49455924),
        subFiles = cms.vstring([
            "/store/user/jpata/VHBBHeppyV13/TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/VHBB_HEPPY_V13_TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/151002_060600/0000/tree_108.root"
        ]),
        isMC     = cms.bool(True)
    ),
    
])

#fill sample number of generated
for s in samples:
    if s.nGen.value() < 0:
        s.nGen = cms.int64(getSampleNGen(s))
samples_dict = {s.name.value(): s for s in samples}

if __name__ == "__main__":
    for sn, sample in samples_dict.items():
        print sample.name, sample.nickname, sample.nGen
