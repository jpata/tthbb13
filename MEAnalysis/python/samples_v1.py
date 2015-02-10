import FWCore.ParameterSet.Config as cms

# $t \bar{t} + \mathrm{jets}$ - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO, $M_{top} = 172.5$ GeV
# ttH - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV, $M_H = 125.0$ GeV
samples = cms.VPSet(
    # cms.PSet(
    #     skip     = cms.bool(False),
    #     name     = cms.string('ttjets_13tev'),
    #     nickName = cms.string('TTJets'),
    #     color    = cms.int32(1),
    #     xSec     = cms.double(508.5)
    # ),
    # cms.PSet(
    #     skip     = cms.bool(False),
    #     name     = cms.string('ttjets_13tev_phys14'),
    #     nickName = cms.string('TTJets_PHYS14'),
    #     color    = cms.int32(1),
    #     xSec     = cms.double(508.5)
    # ),
    # cms.PSet(
    #     skip     = cms.bool(False),
    #     name     = cms.string('ttjets_13tev_pu40bx50'),
    #     nickName = cms.string('TTJets_PU40BX50'),
    #     color    = cms.int32(1),
    #     xSec     = cms.double(508.5)
    # ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev'),
        nickName = cms.string('TTHBB125'),
        color    = cms.int32(2),
        xSec     = cms.double(0.1302*0.569),
        nEvents  = cms.uint64(97520),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(1), #1 - bd_csv, 0 - bd_cisvv2
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev_pu20bx25_phys14'),
        nickName = cms.string('TTHBB125_PU20BX25_PHYS14'),
        color    = cms.int32(2),
        xSec     = cms.double(0.1302*0.569),
        nEvents  = cms.uint64(190700),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(0), #1 - bd_csv, 0 - bd_cisvv2
    ),
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_hbb_13tev_pu40bx50_phys14'),
        nickName = cms.string('TTHBB125_PU40BX50_PHYS14'),
        color    = cms.int32(2),
        xSec     = cms.double(0.1302*0.569),
        nEvents  = cms.uint64(172500),
        perJob   = cms.uint32(1000),
        bdisc    = cms.int32(0), #1 - bd_csv, 0 - bd_cisvv2
    ),
)

if __name__=="__main__":
	for s in samples:
		print s.name.value() + ".root"

# now defined in TTH/TTHNtupleAnalyzer/python/Samples.py
# nickname_map = {
# 	"ttjets": "/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM",
# 	"tthbb": "/TTbarH_HToBB_M-125_13TeV_pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
# 	"ttjets_pu40bx50": "/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-141029_PU40bx50_PLS170_V6AN2-v1/MINIAODSIM",
# 	"tthbb_pu40bx50": "/TTbarH_HToBB_M-125_13TeV_pythia6/Spring14miniaod-141029_PU40bx50_PLS170_V6AN2-v1/MINIAODSIM"
# }
