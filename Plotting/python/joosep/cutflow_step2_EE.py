import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms

process = cms.Process("MEAnalysisNew")

process.fwliteInput = cms.PSet(
	outFile = cms.string("outfile.root"),
	elePt=cms.double(-1),
	muPt=cms.double(-1),

    samples = cms.VPSet([
        cms.PSet(
            fileNamesS1=cms.vstring(["/hdfs/cms/store/user/jpata/tth/dec19_5b21f5f/TTHbb_s1_5b21f5f_tth_hbb_13tev.root"]),
            fileNamesS2=cms.vstring(["/home/joosep/tth/tthbb.root"]),
            nickName=cms.string("tthbb_13TeV"),
            fractionToProcess=cms.double(1.0),
            totalEvents=cms.int64(-1),
            type=cms.int32(3),
            process=cms.int32(0),
            skip=cms.bool(False),
        ),
        cms.PSet(
           # fileNamesS1=cms.vstring(["/hdfs/cms/store/user/jpata/tth/dec19_5b21f5f/TTHbb_s1_5b21f5f_ttjets_13tev.root"]),
           fileNamesS1=cms.vstring([]),
           fileNamesS2=cms.vstring(["/home/joosep/tth/ttjets.root"]),
           nickName=cms.string("ttjets_13TeV"),
           fractionToProcess=cms.double(0.1),
           totalEvents=cms.int64(-1),
           type=cms.int32(3),
           process=cms.int32(1),
           skip=cms.bool(False),
        ),
        ]),
    evLimits=cms.vint64(0, -1)
)

# import os
# if "FILE_NAMES" in os.environ.keys():
#     fns = os.environ["FILE_NAMES"].split()
#     for sample in process.fwliteInput.samples:
#         if sample.fileName.value() in fns:
#             sample.skip = False
#             print "Enabling", sample.nickName
#         else:
#             print "Skipping", sample.nickName
#             sample.skip = True

#     process.fwliteInput.evLimits = cms.vint64(
#         int(os.environ["SKIP_EVENTS"]),
#         int(os.environ["SKIP_EVENTS"] + os.environ["MAX_EVENTS"])
#     )
#     process.fwliteInput.outFile = cms.string("outfile_{0}.root".format(os.environ["MY_JOBID"]))
