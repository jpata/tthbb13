#This file knows about all the TTH samples as produced by the VHbb group
#LFN to PFN resolution is done with code in samples_base
#Cross-sections also defined in samples_base
from TTH.MEAnalysis.samples_base import *
import FWCore.ParameterSet.Config as cms
import os

samples_dict = {
    "sample": cms.PSet(
        name     = cms.string("sample"),
        nickname = cms.string("sample"),
        xSec     = cms.double("1"),
        nGen     = cms.int64(0),
        skip     = cms.bool(False),
        isMC     = cms.bool(True),
        treeName = cms.string("tree"),
        subFiles = cms.vstring(os.environ["INPUT_FILE"]),
    )
}
