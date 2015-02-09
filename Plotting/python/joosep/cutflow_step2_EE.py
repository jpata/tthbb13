import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms

process = cms.Process("MEAnalysisNew")

process.fwliteInput = cms.PSet(
    outFile = cms.string("outfile.root"),
    elePt=cms.double(-1),
    muPt=cms.double(-1),

    samples = cms.VPSet([
        cms.PSet(
            fileNamesS1=cms.vstring(["/hdfs/cms/store/user/jpata/tth/s1_eb733a1/TTHbb_s1_eb733a1_tth_hbb_13tev.root"]),
            fileNamesS2=cms.vstring(["/home/joosep/tth/gc/GC73609b5cb1c7/x/TTHBB125.root"]),
            nickName=cms.string("tthbb_13TeV"),
            fractionToProcess=cms.double(1.0),
            totalEvents=cms.int64(-1),
            type=cms.int32(3),
            process=cms.int32(0),
            skip=cms.bool(False),
        ),
        cms.PSet(
            fileNamesS1=cms.vstring(["/hdfs/cms/store/user/jpata/tth/s1_eb733a1/TTHbb_s1_eb733a1_tth_hbb_13tev_pu20bx25_phys14.root"]),
            fileNamesS2=cms.vstring(["/home/joosep/tth/gc/GC73609b5cb1c7/x/TTHBB125_PU20BX25_PHYS14.root"]),
            nickName=cms.string("tthbb_13TeV_pu20bx25_phys14"),
            fractionToProcess=cms.double(1.0),
            totalEvents=cms.int64(-1),
            type=cms.int32(3),
            process=cms.int32(0),
            skip=cms.bool(False),
        ),
        cms.PSet(
            fileNamesS1=cms.vstring(["/hdfs/cms/store/user/jpata/tth/s1_eb733a1/TTHbb_s1_eb733a1_tth_hbb_13tev_pu40bx50_phys14.root"]),
            fileNamesS2=cms.vstring(["/home/joosep/tth/gc/GC73609b5cb1c7/x/TTHBB125_PU40BX50_PHYS14.root"]),
            nickName=cms.string("tthbb_13TeV_pu40bx50_phys14"),
            fractionToProcess=cms.double(1.0),
            totalEvents=cms.int64(-1),
            type=cms.int32(3),
            process=cms.int32(0),
            skip=cms.bool(False),
        ),
        #cms.PSet(
        #   fileNamesS1=cms.vstring(["/hdfs/cms/store/user/jpata/tth/dec19_5b21f5f/TTHbb_s1_5b21f5f_ttjets_13tev.root"]),
        #   #fileNamesS1=cms.vstring([]),
        #   fileNamesS2=cms.vstring(["/home/joosep/tth/ttjets.root"]),
        #   nickName=cms.string("ttjets_13TeV"),
        #   fractionToProcess=cms.double(0.2),
        #   totalEvents=cms.int64(-1),
        #   type=cms.int32(3),
        #   process=cms.int32(1),
        #   skip=cms.bool(False),
        #),
        ]),
    evLimits=cms.vint64(0, -1)
)

def get_n(fn):
    fi = ROOT.TFile(fn)
    return fi.Get("tree").GetEntries()

if __name__ == "__main__":
    import sys, ROOT
    if hasattr(sys, "argv") and "--create-datasets" in sys.argv:
        of = open("step2.dat", "w")
        for samp in process.fwliteInput.samples:
            of.write("[{0}]".format(samp.nickName.value()) + "\n")
            for fi in samp.fileNamesS2:
                of.write("{0} = {1}".format(fi, get_n(fi)) + "\n")
        of.close()
    else:
        import os
        if "FILE_NAMES" in os.environ.keys():
            fns = os.environ["FILE_NAMES"].split()
            for sample in process.fwliteInput.samples:
                if sample.fileName.value() in fns:
                    sample.skip = False
                    print "Enabling", sample.nickName
                else:
                    print "Skipping", sample.nickName
                    sample.skip = True

            process.fwliteInput.evLimits = cms.vint64(
                int(os.environ["SKIP_EVENTS"]),
                int(os.environ["SKIP_EVENTS"] + os.environ["MAX_EVENTS"])
            )
            process.fwliteInput.outFile = cms.string("outfile_{0}.root".format(os.environ["MY_JOBID"]))
