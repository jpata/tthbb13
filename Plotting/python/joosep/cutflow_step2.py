import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms

process = cms.Process("MEAnalysisNew")

process.fwliteInput = cms.PSet(
	outFile = cms.string("outfile.root"),
	elePt=cms.double(-1),
	muPt=cms.double(-1),

    samples = cms.VPSet([
        cms.PSet(
            fileNamesS1=cms.vstring(["/home/joosep/mac-docs/tth/data/s1_eb733a1/s1/TTHbb_s1_eb733a1_tth_hbb_13tev_amcatnlo_pu20bx25_phys14.root"]),
            fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/s1_eb733a1/s2/tth_hbb_13tev_amcatnlo_pu20bx25_phys14.root"]),
            nickName=cms.string("tthbb_13TeV_phys14"),
            fractionToProcess=cms.double(1.0),
            totalEvents=cms.int64(-1),
            type=cms.int32(3),
            process=cms.int32(0),
            skip=cms.bool(False),
        ),
        # cms.PSet(
        #     fileNamesS1=cms.vstring([]),
        #     fileNamesS2=cms.vstring(["/home/joosep/mac-docs/tth/data/ttjets.root"]),
        #     nickName=cms.string("ttjets_13TeV"),
        #     fractionToProcess=cms.double(1.0),
        #     totalEvents=cms.int64(-1),
        #     type=cms.int32(3),
        #     process=cms.int32(1),
        #     skip=cms.bool(False),
        # ),
        ]),
    evLimits=cms.vint64(0, -1)
)
