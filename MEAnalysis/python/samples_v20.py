from TTH.MEAnalysis.samples_base import *
samples_dict = {
    
        "DoubleEG": cms.PSet(
            name     = cms.string("DoubleEG"),
            nickname = cms.string("DoubleEG"),
            xSec     = cms.double(xsec_sample.get("DoubleEG", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(True),
            isMC     = cms.bool(False),
            subFiles = cms.vstring(get_files("DoubleEG.dat")),
        ),
        
        "DoubleMuon": cms.PSet(
            name     = cms.string("DoubleMuon"),
            nickname = cms.string("DoubleMuon"),
            xSec     = cms.double(xsec_sample.get("DoubleMuon", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(True),
            isMC     = cms.bool(False),
            subFiles = cms.vstring(get_files("DoubleMuon.dat")),
        ),
        
        "MuonEG": cms.PSet(
            name     = cms.string("MuonEG"),
            nickname = cms.string("MuonEG"),
            xSec     = cms.double(xsec_sample.get("MuonEG", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(True),
            isMC     = cms.bool(False),
            subFiles = cms.vstring(get_files("MuonEG.dat")),
        ),
        
        "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_s"),
            xSec     = cms.double(xsec_sample.get("ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(621946),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.dat")),
        ),
        
        "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_t"),
            xSec     = cms.double(xsec_sample.get("ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(4228832),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.dat")),
        ),
        
        "ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_tbar"),
            xSec     = cms.double(xsec_sample.get("ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(1630900),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat")),
        ),
        
        "ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_t"),
            xSec     = cms.double(xsec_sample.get("ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(3131600),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat")),
        ),
        
        "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_tbarW"),
            xSec     = cms.double(xsec_sample.get("ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(923800),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat")),
        ),
        
        "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_tW"),
            xSec     = cms.double(xsec_sample.get("ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(1000000),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat")),
        ),
        
        "SingleElectron": cms.PSet(
            name     = cms.string("SingleElectron"),
            nickname = cms.string("SingleElectron"),
            xSec     = cms.double(xsec_sample.get("SingleElectron", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(True),
            isMC     = cms.bool(False),
            subFiles = cms.vstring(get_files("SingleElectron.dat")),
        ),
        
        "SingleMuon": cms.PSet(
            name     = cms.string("SingleMuon"),
            nickname = cms.string("SingleMuon"),
            xSec     = cms.double(xsec_sample.get("SingleMuon", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(True),
            isMC     = cms.bool(False),
            subFiles = cms.vstring(get_files("SingleMuon.dat")),
        ),
        
        "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("tt_dl"),
            xSec     = cms.double(xsec_sample.get("TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(6102376),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_ht_1200_2500"),
            xSec     = cms.double(xsec_sample.get("TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(907931),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_ht_2500_inf"),
            xSec     = cms.double(xsec_sample.get("TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(434877),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_ht_600_800"),
            xSec     = cms.double(xsec_sample.get("TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(4593625),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_ht_800_1200"),
            xSec     = cms.double(xsec_sample.get("TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(3003217),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_sl_t"),
            xSec     = cms.double(xsec_sample.get("TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(11870675),
            skip     = cms.bool(True),
            isMC     = cms.bool(False),
            subFiles = cms.vstring(get_files("TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_sl_tbar"),
            xSec     = cms.double(xsec_sample.get("TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(11620354),
            skip     = cms.bool(True),
            isMC     = cms.bool(False),
            subFiles = cms.vstring(get_files("TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets"),
            xSec     = cms.double(xsec_sample.get("TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(10079121),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8": cms.PSet(
            name     = cms.string("TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8"),
            nickname = cms.string("ttW_Wlnu"),
            xSec     = cms.double(xsec_sample.get("TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8", 1)),
            nGen     = cms.int64(129001),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.dat")),
        ),
        
        "TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8": cms.PSet(
            name     = cms.string("TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8"),
            nickname = cms.string("ttW_Wqq"),
            xSec     = cms.double(xsec_sample.get("TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8", 1)),
            nGen     = cms.int64(429599),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.dat")),
        ),
        
        "TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8": cms.PSet(
            name     = cms.string("TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8"),
            nickname = cms.string("ttZ_Zqq"),
            xSec     = cms.double(xsec_sample.get("TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8", 1)),
            nGen     = cms.int64(350106),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8.dat")),
        ),
        
        "TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8": cms.PSet(
            name     = cms.string("TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8"),
            nickname = cms.string("ttjets"),
            xSec     = cms.double(xsec_sample.get("TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8", 1)),
            nGen     = cms.int64(9250446),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8.dat")),
        ),
        
        "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("wjets_Wlnu_ht_100_200"),
            xSec     = cms.double(xsec_sample.get("WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(10205377),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("wjets_Wlnu_ht_100_200"),
            xSec     = cms.double(xsec_sample.get("WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(1858826),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("wjets_Wlnu_ht_600_inf"),
            xSec     = cms.double(xsec_sample.get("WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(1041358),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("wjets_Wqq_ht_600_inf"),
            xSec     = cms.double(xsec_sample.get("WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(1025100),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat")),
        ),
        
        "WW_TuneCUETP8M1_13TeV-pythia8": cms.PSet(
            name     = cms.string("WW_TuneCUETP8M1_13TeV-pythia8"),
            nickname = cms.string("ww"),
            xSec     = cms.double(xsec_sample.get("WW_TuneCUETP8M1_13TeV-pythia8", 1)),
            nGen     = cms.int64(906782),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WW_TuneCUETP8M1_13TeV-pythia8.dat")),
        ),
        
        "WZ_TuneCUETP8M1_13TeV-pythia8": cms.PSet(
            name     = cms.string("WZ_TuneCUETP8M1_13TeV-pythia8"),
            nickname = cms.string("wz"),
            xSec     = cms.double(xsec_sample.get("WZ_TuneCUETP8M1_13TeV-pythia8", 1)),
            nGen     = cms.int64(1000000),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WZ_TuneCUETP8M1_13TeV-pythia8.dat")),
        ),
        
        "ZZ_TuneCUETP8M1_13TeV-pythia8": cms.PSet(
            name     = cms.string("ZZ_TuneCUETP8M1_13TeV-pythia8"),
            nickname = cms.string("zz"),
            xSec     = cms.double(xsec_sample.get("ZZ_TuneCUETP8M1_13TeV-pythia8", 1)),
            nGen     = cms.int64(985600),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ZZ_TuneCUETP8M1_13TeV-pythia8.dat")),
        ),
        
        "ttHToNonbb_M125_13TeV_powheg_pythia8": cms.PSet(
            name     = cms.string("ttHToNonbb_M125_13TeV_powheg_pythia8"),
            nickname = cms.string("ttH_Hnonbb"),
            xSec     = cms.double(xsec_sample.get("ttHToNonbb_M125_13TeV_powheg_pythia8", 1)),
            nGen     = cms.int64(3945824),
            skip     = cms.bool(True),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ttHToNonbb_M125_13TeV_powheg_pythia8.dat")),
        ),
        
        "ttHTobb_M125_13TeV_powheg_pythia8": cms.PSet(
            name     = cms.string("ttHTobb_M125_13TeV_powheg_pythia8"),
            nickname = cms.string("ttH_Hbb"),
            xSec     = cms.double(xsec_sample.get("ttHTobb_M125_13TeV_powheg_pythia8", 1)),
            nGen     = cms.int64(1980218),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ttHTobb_M125_13TeV_powheg_pythia8.dat")),
        ),
    }
