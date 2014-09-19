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
    pathToFile    = cms.string("/TEST/PATH/TO/NTUPLES"),

    # the samples
    #samples = samples_V3,
    samples  =   cms.VPSet(
        cms.PSet(
            skip     = cms.bool(False),
            name     = cms.string('TTH_HToBB_M-125_8TeV-pythia6'),
            nickName = cms.string('TTH125'),
            color    = cms.int32(2),
            xSec     = cms.double(0.1302*0.569)
        ),

        cms.PSet(
            skip     = cms.bool(True),
            name     = cms.string('TTJets_SemiLeptMGDecays_8TeV-madgraph'),
            nickName = cms.string('TTJetsSemiLept'),
            color    = cms.int32(41),
            xSec     = cms.double(107.66),
        ),

        cms.PSet(
            skip     = cms.bool(True),
            name     = cms.string('T_t-channel_TuneZ2star_8TeV-powheg-tauola'),
            nickName = cms.string('Tt'),
            color    = cms.int32(6),
            xSec     = cms.double(56.4)
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

