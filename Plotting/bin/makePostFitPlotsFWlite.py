import FWCore.ParameterSet.Config as cms

process = cms.Process("makePostFitPlotsFWlite")

process.fwliteInput = cms.PSet(

    path2Workspace  = cms.string("NONE"),
    path2Datacard   = cms.string("/mnt/t3nfs01/data01/shome/jpata/tth/datacards/v13/ttH_hbb_13TeV_sl_jge6_tge4_high.txt"),
    path2FitResults = cms.string("/mnt/t3nfs01/data01/shome/jpata/tth/datacards/v13/common/ttH_hbb_13TeV_sl.root"),
    outputName      = cms.string("PostFit_bj.root"),
    dirName         = cms.string("bla"),

)
