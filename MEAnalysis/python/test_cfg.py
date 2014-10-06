import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms

process = cms.Process("MEAnalysis")

process.fwliteInput = cms.PSet(
    # the target luminosity (used to calculate the 'weight' variable)
    isMC          = cms.bool(True),

    # output file name
    outFileName   = cms.string("./root/MEAnalysisNewTEST.root"),
    #outFileName   = cms.string("/scratch/bianchi/Trees/MEM/MEAnalysisNewTEST_Sherpa_Had.root"),

    # input file directory
    pathToFile    = cms.string("$CMSSW_BASE/../data"),
    pathToTF      = cms.string("./root/transferFunctionsTEST.root"),

    # the samples
    samples  =   cms.VPSet(
        cms.PSet(
            skip     = cms.bool(False),
            name     = cms.string('ttjets_1'),
            nickName = cms.string('ttjets'),
            color    = cms.int32(2),
            xSec     = cms.double(0.1)
        ),
    ),

    # the target luminosity (used to calculate the 'weight' variable)
    lumi          = cms.untracked.double(19.04),

    # various degrees of verbosity
    debug        = cms.untracked.int32(0),

    # extremely verbose
    verbose      = cms.bool(False),

    # the 'nominal' Higgs, top, and W masses
    MH           = cms.untracked.double(125.00),
    MT           = cms.untracked.double(174.30),
    MW           = cms.untracked.double( 80.19),

    # event limits
    evLimits       = cms.vint32(0, -1),

    # if 1, save into the tree all events
    # if 0, save only events passing the analysis cuts
    ntuplizeAll         = cms.untracked.int32(1),

)

