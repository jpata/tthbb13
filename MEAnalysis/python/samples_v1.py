import FWCore.ParameterSet.Config as cms

# $t \bar{t} + \mathrm{jets}$ - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, $M_{top} = 172.5$ GeV
# ttH - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV, $M_H = 125.0$ GeV
samples = cms.VPSet(
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets'),
        nickName = cms.string('TTJets'),
        color    = cms.int32(1),
        xSec     = cms.double(508.5)
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tthbb'),
        nickName = cms.string('TTHBB125'),
        color    = cms.int32(2),
        xSec     = cms.double(831.76)
    ),
)
