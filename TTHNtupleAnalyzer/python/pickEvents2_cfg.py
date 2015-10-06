import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

import FWCore.PythonUtilities.LumiList as LumiList
options = VarParsing ('analysis')
options.register ('lumifile',
    "",
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "lumifile"
)
options.parseArguments()

process = cms.Process("PickEvent")
process.source = cms.Source ("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
)
process.source.lumisToProcess = LumiList.LumiList(filename = options.lumifile).getVLuminosityBlockRange()

process.Out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string (options.outputFile)
)

process.end = cms.EndPath(process.Out)
