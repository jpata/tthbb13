#This file knows about all the TTH samples as produced by the VHbb group
#LFN to PFN resolution is done with code in samples_base
#Cross-sections also defined in samples_base
from TTH.MEAnalysis.samples_base import *

sample_version = "v10"

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
        perJob   = cms.uint32(10000),
        xSec     = cms.double(xsec[("ttjets", "13TeV")]),
        nGen     = cms.int64(-1),
        subFiles = cms.vstring([
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_1.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_10.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_11.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_12.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_13.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_14.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_15.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_16.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_17.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_18.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_19.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_2.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_20.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_21.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_22.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_23.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_24.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_25.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_26.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_27.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_28.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_29.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_3.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_30.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_31.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_32.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_33.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_34.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_35.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_36.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_38.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_39.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_4.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_40.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_41.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_42.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_43.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_44.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_45.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_46.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_47.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_48.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_49.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_5.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_50.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_51.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_52.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_53.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_54.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_55.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_56.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_57.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_58.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_59.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_6.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_60.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_61.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_62.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_63.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_64.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_65.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_66.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_67.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_68.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_69.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_7.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_8.root",
            "/store/user/jpata/VHBBHeppyV10/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/VHBB_HEPPY_V10_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1/150302_165139/0000/tree_9.root",
        ]),
        isMC     = cms.bool(True)
    ),
#tt + H
    #Spring14
    cms.PSet(
        skip     = cms.bool(False),
        name     = cms.string('tth_13tev'),
        nickName = cms.string('tth_13tev'),
        xSec     = cms.double(xsec[("tth", "13TeV")]),
        nGen     = cms.int64(-1),
        perJob   = cms.uint32(10000),
        subFiles = cms.vstring([
            "/store/user/jpata/VHBBHeppyV10/TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola/VHBB_HEPPY_V10_TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola__Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/150302_164515/0000/tree_1.root"
        ]),
        isMC     = cms.bool(True)
    ),
])

#This contains the samples, but accessible by nickName
samples_dict = {s.name.value(): s for s in samples}
