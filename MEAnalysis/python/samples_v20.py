from TTH.MEAnalysis.samples_base import *
samples_dict = {
    "ttHTobb_M125_13TeV_powheg_pythia8": cms.PSet(
        name     = cms.string("ttHTobb_M125_13TeV_powheg_pythia8"),
        xSec     = cms.double(1),
        nGen     = cms.int64(1),
        isMC     = cms.bool(True),
        treeName = cms.string("vhbb/tree"),
        subFiles = cms.vstring([
            "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/tth/VHBBHeppyV20_tthbbV3_withme_finer/ttHTobb_M125_13TeV_powheg_pythia8/VHBBHeppyV20_tthbbV3_withme_finer_ttHTobb_M125_13TeV_powheg_Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160302_131859/0000/tree_885.root"
        ])
    )
}
