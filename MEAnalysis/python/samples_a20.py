from TTH.MEAnalysis.samples_base import *

samples_dict = {
    'ttHTobb_M125_13TeV_powheg_pythia8': cms.PSet(
    isMC = cms.bool(True),
    nGen = cms.int64(3933404),
    name = cms.string('ttHTobb_M125_13TeV_powheg_pythia8'),
    nickname = cms.string('ttHTobb_M125_13TeV_powheg_pythia8'),
    skip = cms.bool(False),
    subFiles = cms.vstring('file:///scratch/gregor/VHBBHeppyA20/tree_1.root'),
    xSec = cms.double(0.2934045))
}
