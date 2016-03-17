samples_dict = {
    
        "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_tW"),
            xSec     = cms.double(xsec_sample.get("ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1")),
        ),
        
        "ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_tbar"),
            xSec     = cms.double(xsec_sample.get("ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1")),
        ),
        
        "ttHTobb_M125_13TeV_powheg_pythia8": cms.PSet(
            name     = cms.string("ttHTobb_M125_13TeV_powheg_pythia8"),
            nickname = cms.string("ttH_Hbb"),
            xSec     = cms.double(xsec_sample.get("ttHTobb_M125_13TeV_powheg_pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ttHTobb_M125_13TeV_powheg_pythia8")),
        ),
        
        "TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_ht_600_800"),
            xSec     = cms.double(xsec_sample.get("TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
        
        "TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_sl_tbar"),
            xSec     = cms.double(xsec_sample.get("TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(False),
            subFiles = cms.vstring(get_files("TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
        
        "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_t"),
            xSec     = cms.double(xsec_sample.get("ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1")),
        ),
        
        "TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_ht_800_1200"),
            xSec     = cms.double(xsec_sample.get("TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
        
        "TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_sl_t"),
            xSec     = cms.double(xsec_sample.get("TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(False),
            subFiles = cms.vstring(get_files("TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
        
        "TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_ht_1200_2500"),
            xSec     = cms.double(xsec_sample.get("TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
        
        "WZ_TuneCUETP8M1_13TeV-pythia8": cms.PSet(
            name     = cms.string("WZ_TuneCUETP8M1_13TeV-pythia8"),
            nickname = cms.string("wz"),
            xSec     = cms.double(xsec_sample.get("WZ_TuneCUETP8M1_13TeV-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WZ_TuneCUETP8M1_13TeV-pythia8")),
        ),
        
        "ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_t"),
            xSec     = cms.double(xsec_sample.get("ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1")),
        ),
        
        "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_tbarW"),
            xSec     = cms.double(xsec_sample.get("ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1")),
        ),
        
        "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1": cms.PSet(
            name     = cms.string("ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1"),
            nickname = cms.string("stop_s"),
            xSec     = cms.double(xsec_sample.get("ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1")),
        ),
        
        "WW_TuneCUETP8M1_13TeV-pythia8": cms.PSet(
            name     = cms.string("WW_TuneCUETP8M1_13TeV-pythia8"),
            nickname = cms.string("ww"),
            xSec     = cms.double(xsec_sample.get("WW_TuneCUETP8M1_13TeV-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WW_TuneCUETP8M1_13TeV-pythia8")),
        ),
        
        "WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("wjets_Wlnu_ht_100_200"),
            xSec     = cms.double(xsec_sample.get("WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
        
        "WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("wjets_Wqq_ht_600_inf"),
            xSec     = cms.double(xsec_sample.get("WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
        
        "WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("wjets_Wlnu_ht_100_200"),
            xSec     = cms.double(xsec_sample.get("WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
        
        "ZZ_TuneCUETP8M1_13TeV-pythia8": cms.PSet(
            name     = cms.string("ZZ_TuneCUETP8M1_13TeV-pythia8"),
            nickname = cms.string("zz"),
            xSec     = cms.double(xsec_sample.get("ZZ_TuneCUETP8M1_13TeV-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ZZ_TuneCUETP8M1_13TeV-pythia8")),
        ),
        
        "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets"),
            xSec     = cms.double(xsec_sample.get("TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
        
        "WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("wjets_Wlnu_ht_600_inf"),
            xSec     = cms.double(xsec_sample.get("WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
        
        "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("tt_dl"),
            xSec     = cms.double(xsec_sample.get("TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
        
        "ttHToNonbb_M125_13TeV_powheg_pythia8": cms.PSet(
            name     = cms.string("ttHToNonbb_M125_13TeV_powheg_pythia8"),
            nickname = cms.string("ttH_Hnonbb"),
            xSec     = cms.double(xsec_sample.get("ttHToNonbb_M125_13TeV_powheg_pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("ttHToNonbb_M125_13TeV_powheg_pythia8")),
        ),
        
        "TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": cms.PSet(
            name     = cms.string("TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"),
            nickname = cms.string("ttjets_ht_2500_inf"),
            xSec     = cms.double(xsec_sample.get("TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1)),
            nGen     = cms.int64(0),
            skip     = cms.bool(False),
            isMC     = cms.bool(True),
            subFiles = cms.vstring(get_files("TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8")),
        ),
    }
