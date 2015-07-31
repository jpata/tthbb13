#This file knows about all the TTH samples as produced by the VHbb group
#LFN to PFN resolution is done with code in samples_base
#Cross-sections also defined in samples_base
from TTH.MEAnalysis.samples_base import *

sample_version = "v12-74X"

#nickName - string to identify the sample
#name - full name of the sample, currently same as nickName
#perJob - the number of events per job for the MEM code (unused) [events per job]
#xSec - the cross-section [pb]
#nGen - the number of true generated events in the MC sample, used for normalization [number of events]
#       if nGen == -1, then assumed to be unknown and taken from counter histogram in file (FIXME: implement)
#Subfiles - list of strings with PFN/LFN for the files.
#Skip - boolean which controls if the sample is processed or not by default
samples = cms.VPSet([

    #tt + H
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_13tev_amcatnlo'),
        nickName = cms.string('tth_13tev_amcatnlo'),
        xSec     = cms.double(0.5058),
        nGen     = cms.int64(199699), #FIXME: has to be replaced with the number of effective pos-neg weights
        perJob   = cms.uint32(200),
        subFiles = cms.vstring([
               
                    "/store/user/leac/Heppy_V12/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/arizzi-VHBB_HEPPY_U12_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1-0bb472e7ab42c930886da12708defce6/tree_3.root", 
                    "/store/user/leac/Heppy_V12/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/arizzi-VHBB_HEPPY_U12_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1-0bb472e7ab42c930886da12708defce6/tree_4.root",
                    "/store/user/leac/Heppy_V12/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/arizzi-VHBB_HEPPY_U12_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1-0bb472e7ab42c930886da12708defce6/tree_5.root",
                    "/store/user/leac/Heppy_V12/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/arizzi-VHBB_HEPPY_U12_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1-0bb472e7ab42c930886da12708defce6/tree_6.root",
                    "/store/user/leac/Heppy_V12/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/arizzi-VHBB_HEPPY_U12_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1-0bb472e7ab42c930886da12708defce6/tree_7.root",
                    "/store/user/leac/Heppy_V12/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/arizzi-VHBB_HEPPY_U12_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1-0bb472e7ab42c930886da12708defce6/tree_8.root",
                    "/store/user/leac/Heppy_V12/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/arizzi-VHBB_HEPPY_U12_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1-0bb472e7ab42c930886da12708defce6/tree_9.root",
                    "/store/user/leac/Heppy_V12/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/arizzi-VHBB_HEPPY_U12_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1-0bb472e7ab42c930886da12708defce6/tree_12.root",
                    "/store/user/leac/Heppy_V12/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/arizzi-VHBB_HEPPY_U12_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1-0bb472e7ab42c930886da12708defce6/tree_13.root",
                    "/store/user/leac/Heppy_V12/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/arizzi-VHBB_HEPPY_U12_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1-12e5c38111cc6fc8386050390e93038c/tree_3.root",
                    "/store/user/leac/Heppy_V12/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/arizzi-VHBB_HEPPY_U12_ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1-12e5c38111cc6fc8386050390e93038c/tree_9.root",
        ]),
        isMC     = cms.bool(True)
    ),
])



def getSampleNGen(sample):
    import ROOT
    n = 0
    ntot = 0
    for f in sample.subFiles:
        tfn = lfn_to_pfn(f)
        tf = ROOT.TFile.Open(tfn)
        hc = tf.Get("Count")
        hcpos = tf.Get("CountPosWeight")
        hcneg = tf.Get("CountNegWeight")
        n += hcpos.GetBinContent(1)
        n -= hcneg.GetBinContent(1)
        ntot += hcpos.GetBinContent(1) 
        ntot += hcneg.GetBinContent(1) 
        print tfn    
        tf.Close()
    print "number of gen events ",n, ntot
    return int(n)

#fill sample number of generated
for s in samples:
    if s.nGen.value() < 0:
        s.nGen = cms.int64(getSampleNGen(s))
        print s.name, "ngen", s.nGen
#This contains the samples, but accessible by nickName
samples_dict = {s.name.value(): s for s in samples}

if __name__ == "__main__":
    for sn, sample in samples_dict.items():
        print sample
