#This file knows about all the TTH samples as produced by the VHbb group
#LFN to PFN resolution is done with code in samples_base
#Cross-sections also defined in samples_base
from TTH.MEAnalysis.samples_base import *
import FWCore.ParameterSet.Config as cms
import os

samples_dict = {
    "sample": cms.PSet(
        name     = cms.string(os.environ.get("TTH_SAMPLE", "sample")),
        nickname = cms.string("sample"),
        xSec     = cms.double("1"),
        nGen     = cms.int64(0),
        skip     = cms.bool(False),
        isMC     = cms.bool(bool(int(os.environ.get("IS_MC", 1)))),
        treeName = cms.string(os.environ.get("INPUT_TREE", "vhbb/tree")),
        subFiles = cms.vstring(os.environ["INPUT_FILE"]),
    )
}
