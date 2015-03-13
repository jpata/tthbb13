from TTH.MEAnalysis.samples_v1 import *

#if subfiles are empty, they must be filled either by
#calling MEAnalysis.samples_v1.initialize_from_cfgfile
#or by hand form arguments

sample_version = "v10"
#skip is a boolean which controls if the sample is processed or not by default

samples = cms.VPSet([
#tt + jets
    cms.PSet(
        skip     = cms.bool(True),
        name     = cms.string('ttjets_13tev_phys14'),
        nickName = cms.string('ttjets_13tev_phys14'),
        perJob   = cms.uint32(100000),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([]),
        isMC     = cms.bool(True)
    ),
    cms.PSet(
        skip     = cms.bool(True),
        name     = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        nickName = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        perJob   = cms.uint32(100000),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([]),
        isMC     = cms.bool(True)
    ),
#tt + H
    #Spring14
    cms.PSet(
        skip     = cms.bool(True),
        name     = cms.string('tth_hbb_13tev'),
        nickName = cms.string('tth_hbb_13tev'),
        xSec     = cms.double(xsec[("tthbb", "13TeV")]),
        nGen     = cms.int64(-1),
        perJob   = cms.uint32(1000),
        subFiles = cms.vstring([]),
        isMC     = cms.bool(True)
    ),
])

samples_dict = {s.name.value(): s for s in samples}
