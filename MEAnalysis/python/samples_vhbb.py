#This file knows about all the TTH samples as produced by the VHbb group
#LFN to PFN resolution is done with code in samples_base
#Cross-sections also defined in samples_base
from TTH.MEAnalysis.samples_base import *

sample_version = "v10"

#nickName - string to identify the sample
#name - full name of the sample, currently same as nickName
#perJob - the number of events per job for the MEM code (unused) [events per job]
#xSec - the cross-section [pb]
#nGen - the number of true generated events in the MC sample, used for normalization [number of events]
#       if nGen == -1, then assumed to be unknown and taken from counter histogram in file (FIXME: implement)
#Subfiles - list of strings with PFN/LFN for the files.
#Skip - boolean which controls if the sample is processed or not by default
samples = cms.VPSet([

    #tt + jets
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        nickName = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        perJob   = cms.uint32(20000),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([
            "/store/user/gregor/store/user/gregor/VHBBHeppypreV12_G07/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_preV12_G07_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/150618_082915/0000/tree_181.root",
            "/store/user/gregor/store/user/gregor/VHBBHeppypreV12_G07/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_preV12_G07_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/150618_082915/0000/tree_37.root",
            "/store/user/gregor/store/user/gregor/VHBBHeppypreV12_G07/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_preV12_G07_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/150618_082915/0000/tree_214.root",
            "/store/user/gregor/store/user/gregor/VHBBHeppypreV12_G07/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_preV12_G07_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/150618_082915/0000/tree_210.root",

        ]),
        isMC     = cms.bool(True)
    ),
#tt + H
#    #Spring14
#    cms.PSet(
#        skip     = cms.bool(True),
#        name     = cms.string('tth_13tev'),
#        nickName = cms.string('tth_13tev'),
#        xSec     = cms.double(xsec[("tth", "13TeV")]),
#        nGen     = cms.int64(-1),
#        perJob   = cms.uint32(2000),
#        subFiles = cms.vstring([
#        ]),
#        isMC     = cms.bool(True)
#    ),
])

#This contains the samples, but accessible by nickName
samples_dict = {s.name.value(): s for s in samples}
