#This file knows about all the TTH samples as produced by the VHbb group
#LFN to PFN resolution is done with code in samples_base
#Cross-sections also defined in samples_base
from TTH.MEAnalysis.samples_base import *

sample_version = "v11-722sync"

#nickName - string to identify the sample
#name - full name of the sample, currently same as nickName
#perJob - the number of events per job for the MEM code (unused) [events per job]
#xSec - the cross-section [pb]
#nGen - the number of true generated events in the MC sample, used for normalization [number of events]
#       if nGen == -1, then assumed to be unknown and taken from counter histogram in file (FIXME: implement)
#Subfiles - list of strings with PFN/LFN for the files.
#Skip - boolean which controls if the sample is processed or not by default
samples = cms.VPSet([

    #tt + jets
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        nickName = cms.string('ttjets_13tev_madgraph_pu20bx25_phys14'),
        perJob   = cms.uint32(2000),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_1.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_10.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_100.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_101.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_102.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_104.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_106.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_107.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_108.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_109.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_11.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_110.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_111.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_13.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_15.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_17.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_19.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_2.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_20.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_21.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_22.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_23.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_24.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_25.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_27.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_28.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_29.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_3.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_30.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_31.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_32.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_33.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_34.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_35.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_37.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_39.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_4.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_40.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_41.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_42.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_43.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_44.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_45.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_46.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_47.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_48.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_51.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_52.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_54.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_55.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_56.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_57.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_58.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_61.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_62.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_63.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_64.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_65.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_67.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_68.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_69.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_7.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_70.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_71.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_72.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_73.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_74.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_75.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_76.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_77.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_78.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_8.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_80.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_82.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_83.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_84.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_85.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_86.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_87.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_88.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_89.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_9.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_90.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_91.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_92.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_93.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_94.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_95.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_96.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_97.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_98.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170716/0000/tree_99.root",
        ]),
        isMC     = cms.bool(True)
    ),

    #tt + Z
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttz_13tev_madgraph_pu20bx25_phys14'),
        nickName = cms.string('ttz_13tev_madgraph_pu20bx25_phys14'),
        perJob   = cms.uint32(2000),
        xSec     = cms.double(2.232),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTZJets_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTZJets_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170818/0000/tree_1.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTZJets_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTZJets_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170818/0000/tree_2.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTZJets_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTZJets_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170818/0000/tree_3.root",
        ]),
        isMC     = cms.bool(True)
    ),

    #tt + W
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('ttw_13tev_madgraph_pu20bx25_phys14'),
        nickName = cms.string('ttw_13tev_madgraph_pu20bx25_phys14'),
        perJob   = cms.uint32(2000),
        xSec     = cms.double(1.152),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTWJets_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTWJets_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170751/0000/tree_1.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTWJets_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V11_TTWJets_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150609_170751/0000/tree_2.root",
        ]),
        isMC     = cms.bool(True)
    ),

    #tt + H
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_13tev_amcatnlo_pu20bx25'),
        nickName = cms.string('tth_13tev_amcatnlo_pu20bx25'),
        xSec     = cms.double(0.5058),
        nGen     = cms.int64(-1),
        perJob   = cms.uint32(2000),
        subFiles = cms.vstring([
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola/VHBB_HEPPY_V11_TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola__Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/150609_170651/0000/tree_1.root",
            "/store/user/jpata/VHBBHeppy722p2-tthsync-jun9-1/TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola/VHBB_HEPPY_V11_TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola__Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/150609_170651/0000/tree_2.root",
        ]),
        isMC     = cms.bool(True)
    ),
])


#ttz_13tev_madgraph_pu20bx25_phys14 249275.0
#ttjets_13tev_madgraph_pu20bx25_phys14 8346409.0
#ttw_13tev_madgraph_pu20bx25_phys14 246521.0
#tth_13tev_amcatnlo_pu20bx25 199699.0

def getSampleNGen(sample):
    import ROOT
    n = 0
    for f in sample.subFiles:
        tfn = lfn_to_pfn(f)
        tf = ROOT.TFile.Open(tfn)
        hc = tf.Get("Count")
        n += hc.GetBinContent(1)
        #print tfn, hc.GetBinContent(1)
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
