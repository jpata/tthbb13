import FWCore.ParameterSet.Types as CfgTypes
import FWCore.ParameterSet.Config as cms

import TTH.MEAnalysis.samples_v1 as samples_v1
import TTH.MEAnalysis.mem_parameters_cff as memp

process = cms.Process("TreeProducer")

process.fwliteInput = cms.PSet(
    outFileName   = cms.string("jet_trees.root"),
    pathToFile    = cms.string(memp.pathToFile),
    ordering      = cms.string(memp.ordering),
    lumi          = cms.double(1.0),
    verbose       = cms.bool(True),
    evalReg       = cms.bool(False),
    maxnum        = cms.int32(100000),

    samples       = samples_v1.samples
)
