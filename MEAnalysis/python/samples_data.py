#This file knows about all the TTH samples as produced by the VHbb group
#LFN to PFN resolution is done with code in samples_base
#Cross-sections also defined in samples_base
from TTH.MEAnalysis.samples_base import *

sample_version = "v12-Data"

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
        name     = cms.string('Data_50ns_run251'),
        nickName = cms.string('Data_50ns_run251'),
        xSec     = cms.double(1),
        nGen     = cms.int64(1), 
        perJob   = cms.uint32(200),
        subFiles = cms.vstring([
               
                    "/store/user/dsalerno/50ns_run251_v4/tree_run244.root",
                    "/store/user/dsalerno/50ns_run251_v4/tree_run251.root",
                    "/store/user/dsalerno/50ns_run251_v4/tree_run252.root",
                    "/store/user/dsalerno/50ns_run251_v4/tree_run561.root",
                    "/store/user/dsalerno/50ns_run251_v4/tree_run562.root",
                    "/store/user/dsalerno/50ns_run251_v4/tree_run721.root",
        ]),
        isMC     = cms.bool(False)
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
