from TTH.MEAnalysis.samples_base import *
samples_dict = {
    "ttHTobb_M125_13TeV_powheg_pythia8": cms.PSet(
        name     = cms.string("ttHTobb_M125_13TeV_powheg_pythia8"),
        xSec     = cms.double(1),
        nGen     = cms.int64(1),
        isMC     = cms.bool(True),
        treeName = cms.string("vhbb/tree"),
        subFiles = cms.vstring(get_files(
            os.environ.get("CMSSW_BASE") + "/src/TTH/MEAnalysis/gc/datasets/vhbb_tth/ttHTobb_M125_13TeV_powheg_pythia8.txt"
            )[:5])
    )
}
