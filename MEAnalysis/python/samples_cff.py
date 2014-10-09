import FWCore.ParameterSet.Types  as CfgTypes
import FWCore.ParameterSet.Config as cms

#-----NLO-------
xsecTT_SL = 103.0
xsecTT_FL = 24.8
xsecTT_FH = 106

#----NNLO------
xsecTT_SL = 107.66
xsecTT_FL = 25.81
xsecTT_FH = 112.33

# the input samples 
samples_V2       = cms.VPSet(
    
    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph'),
    nickName = cms.string('DYJets10to50'),
    color    = cms.int32(18),
    xSec     = cms.double(12765.)
    ),
    
    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball'),
    nickName = cms.string('DYJets50'),
    color    = cms.int32(19),
    xSec     = cms.double(3503.71)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball'),
    nickName = cms.string('WJets'),
    color    = cms.int32(29),
    xSec     = cms.double(37509.0),
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('TtW'),
    color    = cms.int32(6),
    xSec     = cms.double(11.1)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('T_t-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Tt'),
    color    = cms.int32(6),
    xSec     = cms.double(56.4)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('T_s-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Ts'),
    color    = cms.int32(6),
    xSec     = cms.double(3.79)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('TbartW'),
    color    = cms.int32(6),
    xSec     = cms.double(11.1)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Tbart'),
    color    = cms.int32(6),
    xSec     = cms.double(30.7)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Tbars'),
    color    = cms.int32(6),
    xSec     = cms.double(1.76)
    ),


    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('WW_TuneZ2star_8TeV_pythia6_tauola'),
    nickName = cms.string('WW'),
    color    = cms.int32(4),
    xSec     = cms.double(56.75)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('WZ_TuneZ2star_8TeV_pythia6_tauola'),
    nickName = cms.string('WZ'),
    color    = cms.int32(4),
    xSec     = cms.double(33.85)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('ZZ_TuneZ2star_8TeV_pythia6_tauola'),
    nickName = cms.string('ZZ'),
    color    = cms.int32(4),
    xSec     = cms.double(8.297)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTH_HToBB_M-110_8TeV-pythia6'),
    nickName = cms.string('TTH110'),
    color    = cms.int32(2),
    xSec     = cms.double(0.1887*0.744)
    ),

    
    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTH_HToBB_M-115_8TeV-pythia6'),
    nickName = cms.string('TTH115'),
    color    = cms.int32(2),
    xSec     = cms.double(0.1663*0.703)
    ),


    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTH_HToBB_M-120_8TeV-pythia6'),
    nickName = cms.string('TTH120'),
    color    = cms.int32(2),
    xSec     = cms.double(0.1470*0.648)
    ),


    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTH_HToBB_M-125_8TeV-pythia6_v2'),
    nickName = cms.string('TTH125'),
    color    = cms.int32(2),
    xSec     = cms.double(0.1302*0.569)
    ),


    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTH_HToBB_M-130_8TeV-pythia6'),
    nickName = cms.string('TTH130'),
    color    = cms.int32(2),
    xSec     = cms.double(0.1157*0.494)
    ),

    
    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTH_HToBB_M-135_8TeV-pythia6'),
    nickName = cms.string('TTH135'),
    color    = cms.int32(2),
    xSec     = cms.double(0.1031*0.404)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTWJets_8TeV-madgraph'),
    nickName = cms.string('TTW'),
    color    = cms.int32(18),
    xSec     = cms.double(0.232),
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTZJets_8TeV-madgraph_v2'),
    nickName = cms.string('TTZ'),
    color    = cms.int32(18),
    xSec     = cms.double(0.2057),
    ),


    cms.PSet(
    skip     = cms.bool(False),  
    name     = cms.string('TTJets_SemiLeptMGDecays_8TeV-madgraph'),
    nickName = cms.string('TTJetsSemiLept'),
    color    = cms.int32(41),
    xSec     = cms.double(xsecTT_SL),
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTJets_FullLeptMGDecays_8TeV-madgraph'),
    nickName = cms.string('TTJetsFullLept'),
    color    = cms.int32(41),
    xSec     = cms.double(xsecTT_FL),
    ),

    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    nickName = cms.string('Run2012_DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectronRun2012CAug24RerecoEdmV42'),
    nickName = cms.string('Run2012_DoubleElectronRun2012CAug24RerecoEdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectronRun2012D'),
    nickName = cms.string('Run2012_DoubleElectronRun2012D'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012A-13Jul2012-v1_ProcFIXED'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012A-13Jul2012-v1_ProcFIXED'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012A-recover-06Aug2012-v1_ProcV2'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012A-recover-06Aug2012-v1_ProcV2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012B-13Jul2012-v1_ProcFIXED'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012B-13Jul2012-v1_ProcFIXED'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV1'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV1'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV2'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),



    cms.PSet(
    skip     = cms.bool(True),  # 148139
    name     = cms.string('SingleElectronRun2012AAug06EdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012AAug06EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 1551019
    name     = cms.string('SingleElectronRun2012AJul13EdmV42b'),
    nickName = cms.string('Run2012_SingleElectronRun2012AJul13EdmV42b'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 9351330
    name     = cms.string('SingleElectronRun2012BJul13EdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012BJul13EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 263593
    name     = cms.string('SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    nickName = cms.string('Run2012_SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 1064158
    name     = cms.string('SingleElectronRun2012CAug24RerecoEdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012CAug24RerecoEdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 9768094
    name     = cms.string('SingleElectronRun2012CPromptv2EdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012CPromptv2EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 3491407
    name     = cms.string('SingleElectronRun2012CPromptV2TopUpEdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012CPromptV2TopUpEdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 16178887
    name     = cms.string('SingleElectronRun2012D-PromptReco-v1_v3'),
    nickName = cms.string('Run2012_SingleElectronRun2012D-PromptReco-v1_v3'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),

    # THESE ARE FOR V2
    cms.PSet(
    skip     = cms.bool(True), # 90889
    name     = cms.string('SingleMuRun2012AAug06EdmV42'),
    nickName = cms.string('Run2012_SingleMuRun2012AAug06EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 916855
    name     = cms.string('SingleMuRun2012AJul13EdmV42'),
    nickName = cms.string('Run2012_SingleMuRun2012AJul13EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 6121904
    name     = cms.string('SingleMuRun2012BJul13EdmV42'),
    nickName = cms.string('Run2012_SingleMuRun2012BJul13EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2'),
    nickName = cms.string('Run2012_SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012CAug24RerecoEdmV42'),
    nickName = cms.string('Run2012_SingleMuRun2012CAug24RerecoEdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012CPromptV2TopUpEdmV42'),
    nickName = cms.string('Run2012_SingleMuRun2012CPromptV2TopUpEdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012CPromptv2EdmV42'),
    nickName = cms.string('Run2012_SingleMuRun2012CPromptv2EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 11860310
    name     = cms.string('SingleMuRun2012D-PromptReco-v1'),
    nickName = cms.string('Run2012_SingleMuRun2012D-PromptReco-v1'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),

    )


# GEN LEVEL STUDIES
samples_GEN      = cms.VPSet(

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTH125_sherpa_LOPSUEHAD_unweighted'),
    nickName = cms.string('sherpa_tth'),
    color    = cms.int32(2),
    xSec     = cms.double(0.1302*0.569)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTbb_sherpa_unweighted'),
    nickName = cms.string('sherpa_ttbb'),
    color    = cms.int32(41),
    xSec     = cms.double(6.76)
    ),
    
    )



samples_V3       = cms.VPSet(


    ###################################################################################
    #################  MC
    ###################################################################################

    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph'),
    nickName = cms.string('DYJets10to50'),
    color    = cms.int32(18),
    xSec     = cms.double(12765.)
    ),
    
    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph'),
    nickName = cms.string('DYJets50'),
    color    = cms.int32(19),
    xSec     = cms.double(3503.71)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball'),
    nickName = cms.string('WJets'),
    color    = cms.int32(29),
    xSec     = cms.double(37509.0),
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('TtW'),
    color    = cms.int32(6),
    xSec     = cms.double(11.1)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('T_t-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Tt'),
    color    = cms.int32(6),
    xSec     = cms.double(56.4)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('T_s-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Ts'),
    color    = cms.int32(6),
    xSec     = cms.double(3.79)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('TbartW'),
    color    = cms.int32(6),
    xSec     = cms.double(11.1)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Tbart'),
    color    = cms.int32(6),
    xSec     = cms.double(30.7)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Tbars'),
    color    = cms.int32(6),
    xSec     = cms.double(1.76)
    ),


    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('WW_TuneZ2star_8TeV_pythia6_tauola'),
    nickName = cms.string('WW'),
    color    = cms.int32(4),
    xSec     = cms.double(56.75)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('WZ_TuneZ2star_8TeV_pythia6_tauola'),
    nickName = cms.string('WZ'),
    color    = cms.int32(4),
    xSec     = cms.double(33.85)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('ZZ_TuneZ2star_8TeV_pythia6_tauola'),
    nickName = cms.string('ZZ'),
    color    = cms.int32(4),
    xSec     = cms.double(8.297)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTH_HToBB_M-125_8TeV-pythia6'),
    nickName = cms.string('TTH125'),
    color    = cms.int32(2),
    xSec     = cms.double(0.1302*0.569)
    ),


    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTWJets_8TeV-madgraph'),
    nickName = cms.string('TTW'),
    color    = cms.int32(18),
    xSec     = cms.double(0.232),
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTZJets_8TeV-madgraph'),
    nickName = cms.string('TTZ'),
    color    = cms.int32(18),
    xSec     = cms.double(0.2057),
    ),


    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTJets_SemiLeptMGDecays_8TeV-madgraph'),
    nickName = cms.string('TTJetsSemiLept'),
    color    = cms.int32(41),
    xSec     = cms.double(xsecTT_SL),
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTJets_FullLeptMGDecays_8TeV-madgraph'),
    nickName = cms.string('TTJetsFullLept'),
    color    = cms.int32(41),
    xSec     = cms.double(xsecTT_FL),
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTJets_HadronicMGDecays_8TeV-madgraph'),
    nickName = cms.string('TTJetsFullHad'),
    color    = cms.int32(41),
    xSec     = cms.double(xsecTT_FH),
    ),


    ###################################################################################
    #################  DATA
    ###################################################################################

    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    nickName = cms.string('Run2012_DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectronRun2012CAug24RerecoEdmV42'),
    nickName = cms.string('Run2012_DoubleElectronRun2012CAug24RerecoEdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectronRun2012D'),
    nickName = cms.string('Run2012_DoubleElectronRun2012D'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012A-13Jul2012-v1_ProcFIXED'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012A-13Jul2012-v1_ProcFIXED'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012A-recover-06Aug2012-v1_ProcV2'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012A-recover-06Aug2012-v1_ProcV2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012B-13Jul2012-v1_ProcFIXED'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012B-13Jul2012-v1_ProcFIXED'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV1'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV1'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV2'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),



    cms.PSet(
    skip     = cms.bool(True),  # 148139
    name     = cms.string('SingleElectronRun2012AAug06EdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012AAug06EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 1551019
    name     = cms.string('SingleElectronRun2012AJul13EdmV42b'),
    nickName = cms.string('Run2012_SingleElectronRun2012AJul13EdmV42b'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 9351330
    name     = cms.string('SingleElectronRun2012BJul13EdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012BJul13EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 263593
    name     = cms.string('SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    nickName = cms.string('Run2012_SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 1064158
    name     = cms.string('SingleElectronRun2012CAug24RerecoEdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012CAug24RerecoEdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 9768094
    name     = cms.string('SingleElectronRun2012CPromptv2EdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012CPromptv2EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 3491407
    name     = cms.string('SingleElectronRun2012CPromptV2TopUpEdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012CPromptV2TopUpEdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 16178887
    name     = cms.string('SingleElectronRun2012D-PromptReco-v1_v3'),
    nickName = cms.string('Run2012_SingleElectronRun2012D-PromptReco-v1_v3'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),



    cms.PSet(
    skip     = cms.bool(True), # 90889
    name     = cms.string('SingleMuRun2012AAug06'),
    nickName = cms.string('Run2012_SingleMuRun2012AAug06'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 916855
    name     = cms.string('SingleMuRun2012AJul13'),
    nickName = cms.string('Run2012_SingleMuRun2012AJul13'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 6121904
    name     = cms.string('SingleMuRun2012BJul13'),
    nickName = cms.string('Run2012_SingleMuRun2012BJul13'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2'),
    nickName = cms.string('Run2012_SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012CAug24Rereco'),
    nickName = cms.string('Run2012_SingleMuRun2012CAug24Rereco'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012CPromptv2'),
    nickName = cms.string('Run2012_SingleMuRun2012CPromptv2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012CPromptV2TopUp'),
    nickName = cms.string('Run2012_SingleMuRun2012CPromptV2TopUp'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(False),
    name     = cms.string('SingleMuRun2012D-PromptReco-v1'),
    nickName = cms.string('Run2012_SingleMuRun2012D-PromptReco-v1'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),

    )


samples_V4       = cms.VPSet(


    ###################################################################################
    #################  MC
    ###################################################################################

    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph'),
    nickName = cms.string('DYJets10to50'),
    color    = cms.int32(18),
    xSec     = cms.double(14702.)
    ),
    
    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph'),
    nickName = cms.string('DYJets50'),
    color    = cms.int32(19),
    xSec     = cms.double(3503.71)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball'),
    nickName = cms.string('WJets'),
    color    = cms.int32(29),
    xSec     = cms.double(37509.0),
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('TtW'),
    color    = cms.int32(6),
    xSec     = cms.double(11.1)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('T_t-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Tt'),
    color    = cms.int32(6),
    xSec     = cms.double(56.4)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('T_s-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Ts'),
    color    = cms.int32(6),
    xSec     = cms.double(3.79)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('TbartW'),
    color    = cms.int32(6),
    xSec     = cms.double(11.1)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Tbart'),
    color    = cms.int32(6),
    xSec     = cms.double(30.7)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola'),
    nickName = cms.string('Tbars'),
    color    = cms.int32(6),
    xSec     = cms.double(1.76)
    ),


    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('WW_TuneZ2star_8TeV_pythia6_tauola'),
    nickName = cms.string('WW'),
    color    = cms.int32(4),
    xSec     = cms.double(56.75)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('WZ_TuneZ2star_8TeV_pythia6_tauola'),
    nickName = cms.string('WZ'),
    color    = cms.int32(4),
    xSec     = cms.double(33.85)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('ZZ_TuneZ2star_8TeV_pythia6_tauola'),
    nickName = cms.string('ZZ'),
    color    = cms.int32(4),
    xSec     = cms.double(8.297)
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTH_HToBB_M-125_8TeV-pythia6'),
    nickName = cms.string('TTH125'),
    color    = cms.int32(2),
    xSec     = cms.double(0.1293*0.577)
    ),


    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTWJets_8TeV-madgraph'),
    nickName = cms.string('TTW'),
    color    = cms.int32(18),
    xSec     = cms.double(0.232),
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTZJets_8TeV-madgraph'),
    nickName = cms.string('TTZ'),
    color    = cms.int32(18),
    xSec     = cms.double(0.2057),
    ),


    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTJets_SemiLeptMGDecays_8TeV-madgraph'),
    nickName = cms.string('TTJetsSemiLept'),
    color    = cms.int32(41),
    xSec     = cms.double(xsecTT_SL),
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTJets_FullLeptMGDecays_8TeV-madgraph'),
    nickName = cms.string('TTJetsFullLept'),
    color    = cms.int32(41),
    xSec     = cms.double(xsecTT_FL),
    ),

    cms.PSet(
    skip     = cms.bool(True),  
    name     = cms.string('TTJets_HadronicMGDecays_8TeV-madgraph'),
    nickName = cms.string('TTJetsFullHad'),
    color    = cms.int32(41),
    xSec     = cms.double(xsecTT_FH),
    ),

    #QCD x-sections from: http://cms.cern.ch/iCMS/prep/requestmanagement?dsn=QCD_Pt_*_*_BCtoE_TuneZ2star_8TeV_pythia6*
    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('QCD_Pt_80_170_BCtoE_TuneZ2star_8TeV_pythia6'),
    nickName = cms.string('QCD_Pt_80_170_BCtoE'),
    color    = cms.int32(100),
    xSec     = cms.double(1191000.0*0.0109),
    ),
    
    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('QCD_Pt_170_250_BCtoE_TuneZ2star_8TeV_pythia6'),
    nickName = cms.string('QCD_Pt_170_250_BCtoE'),
    color    = cms.int32(100),
    xSec     = cms.double(30980.0*0.0204),
    ),

    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('QCD_Pt_250_350_BCtoE_TuneZ2star_8TeV_pythia6'),
    nickName = cms.string('QCD_Pt_250_350_BCtoE'),
    color    = cms.int32(100),
    xSec     = cms.double(4250.0*0.0243),
    ),

    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('QCD_Pt_350_BCtoE_TuneZ2star_8TeV_pythia6'),
    nickName = cms.string('QCD_Pt_350_BCtoE'),
    color    = cms.int32(100),
    xSec     = cms.double(811.0*0.0295),
    ),

#    http://cms.cern.ch/iCMS/prep/requestmanagement?dsn=QCD_Pt-*_bEnriched_TuneZ2star_8TeV-pythia6-evtgen

    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('QCD_Pt-30To50_bEnriched_TuneZ2star_8TeV-pythia6'),
    nickName = cms.string('QCD_Pt-30To50_bEnriched'),
    color    = cms.int32(100),
    xSec     = cms.double(6.677E7*0.0812),
    ),

    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('QCD_Pt-50To150_bEnriched_TuneZ2star_8TeV-pythia6'),
    nickName = cms.string('QCD_Pt-50To150_bEnriched'),
    color    = cms.int32(100),
    xSec     = cms.double(9355000.0*0.0956),
    ),

    cms.PSet(
    skip     = cms.bool(True),
    name     = cms.string('QCD_Pt-150_bEnriched_TuneZ2star_8TeV-pythia6'),
    nickName = cms.string('QCD_Pt-150_bEnriched'),
    color    = cms.int32(100),
    xSec     = cms.double(67340.0*0.1259),
    ),

    ###################################################################################
    #################  DATA
    ###################################################################################

    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    nickName = cms.string('Run2012_DoubleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectronRun2012CAug24RerecoEdmV42'),
    nickName = cms.string('Run2012_DoubleElectronRun2012CAug24RerecoEdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectronRun2012D'),
    nickName = cms.string('Run2012_DoubleElectronRun2012D'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012A-13Jul2012-v1_ProcFIXED'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012A-13Jul2012-v1_ProcFIXED'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012A-recover-06Aug2012-v1_ProcV2'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012A-recover-06Aug2012-v1_ProcV2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012B-13Jul2012-v1_ProcFIXED'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012B-13Jul2012-v1_ProcFIXED'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV1'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV1'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV2'),
    nickName = cms.string('Run2012_DoubleElectron_Run2012C-PromptReco-v2_HBB_EDMNtupleV42_ProcV2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),



    cms.PSet(
    skip     = cms.bool(True),  # 148139
    name     = cms.string('SingleElectronRun2012AAug06EdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012AAug06EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 1551019
    name     = cms.string('SingleElectronRun2012AJul13EdmV42b'),
    nickName = cms.string('Run2012_SingleElectronRun2012AJul13EdmV42b'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 9351330
    name     = cms.string('SingleElectronRun2012BJul13EdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012BJul13EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 263593
    name     = cms.string('SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    nickName = cms.string('Run2012_SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 1064158
    name     = cms.string('SingleElectronRun2012CAug24RerecoEdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012CAug24RerecoEdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 9768094
    name     = cms.string('SingleElectronRun2012CPromptv2EdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012CPromptv2EdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 3491407
    name     = cms.string('SingleElectronRun2012CPromptV2TopUpEdmV42'),
    nickName = cms.string('Run2012_SingleElectronRun2012CPromptV2TopUpEdmV42'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 16178887
    name     = cms.string('SingleElectronRun2012D-PromptReco-v1_v3'),
    nickName = cms.string('Run2012_SingleElectronRun2012D-PromptReco-v1_v3'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),



    cms.PSet(
    skip     = cms.bool(True), # 90889
    name     = cms.string('SingleMuRun2012AAug06'),
    nickName = cms.string('Run2012_SingleMuRun2012AAug06'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 916855
    name     = cms.string('SingleMuRun2012AJul13'),
    nickName = cms.string('Run2012_SingleMuRun2012AJul13'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), # 6121904
    name     = cms.string('SingleMuRun2012BJul13'),
    nickName = cms.string('Run2012_SingleMuRun2012BJul13'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2'),
    nickName = cms.string('Run2012_SingleMuRun2012C-EcalRecover_11Dec2012-v1_v2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012CAug24Rereco'),
    nickName = cms.string('Run2012_SingleMuRun2012CAug24Rereco'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012CPromptv2'),
    nickName = cms.string('Run2012_SingleMuRun2012CPromptv2'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(True), 
    name     = cms.string('SingleMuRun2012CPromptV2TopUp'),
    nickName = cms.string('Run2012_SingleMuRun2012CPromptV2TopUp'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),
    cms.PSet(
    skip     = cms.bool(False),
    name     = cms.string('SingleMuRun2012D-PromptReco-v1'),
    nickName = cms.string('Run2012_SingleMuRun2012D-PromptReco-v1'),
    color    = cms.int32(1),
    xSec     = cms.double(-1),
    ),

    )
