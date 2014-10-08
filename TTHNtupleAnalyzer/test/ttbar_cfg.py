import FWCore.ParameterSet.Config as cms

from TTH.TTHNtupleAnalyzer.triggers_MC_cff import triggerPathNames
print '**** TRIGGER PATHS ****'
counter = 0
for trigger in triggerPathNames:
    print "[%s] = %s" % (counter, trigger)
    counter += 1


process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'/store/results/top/StoreResults/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/USER/Spring14dr_PU_S14_POSTLS170_V6AN1_miniAOD706p1_814812ec83fce2f620905d2bb30e9100-v2/00000/0012F41F-FA17-E411-A1FF-0025905A48B2.root',
        ## these are at PSI:
        '/store/mc/Spring14miniaod/TTbarH_HToBB_M-125_13TeV_pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/0E97DD3E-2209-E411-8A04-003048945312.root',
        '/store/mc/Spring14miniaod/TTbarH_HToBB_M-125_13TeV_pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/D0242854-2209-E411-B361-003048C559CE.root',
    )
)

process.tthNtupleAnalyzer = cms.EDAnalyzer(
    'TTHNtupleAnalyzer',
    isMC          = cms.bool(True),
    vertices      = cms.InputTag("offlineSlimmedPrimaryVertices"),
    muons         = cms.InputTag("slimmedMuons"),
    electrons     = cms.InputTag("slimmedElectrons"),
    taus          = cms.InputTag("slimmedTaus"),
    jets          = cms.InputTag("slimmedJets"),   
    topjets       = cms.InputTag("hepTopTagPFJetsCHS"),
    topjetsubjets = cms.InputTag("hepTopTagPFJetsCHS", "caTopSubJets"),
    topjetinfos   = cms.InputTag("hepTopTagInfos"),
    packed        = cms.InputTag("packedGenParticles"),
    pruned        = cms.InputTag("prunedGenParticles"),
    fatjets       = cms.InputTag("slimmedJetsAK8"),
    mets          = cms.InputTag("slimmedMETs"),
    #lhe          = cms.InputTag("externalLHEProducer"),
    lhe           = cms.InputTag(""),
    eleIdentifiers = cms.vstring([
            'eidLoose',
            'eidRobustHighEnergy',
            'eidRobustLoose',
            'eidRobustTight',
            'eidTight'
            ]),
    tauIdentifiers = cms.vstring([
            # 'againstElectronLoose',
            # 'againstElectronLooseMVA5',
            'againstElectronMVA5category',
            'againstElectronMVA5raw',
            # 'againstElectronMedium',
            'againstElectronMediumMVA5',
            'againstElectronTight',
            'againstElectronTightMVA5',
            'againstElectronVLooseMVA5',
            # 'againstElectronVTightMVA5',
            # 'againstMuonLoose',
            # 'againstMuonLoose2',
            # 'againstMuonLoose3',
            'againstMuonLooseMVA',
            # 'againstMuonMVAraw',
            # 'againstMuonMedium',
            # 'againstMuonMedium2',
            'againstMuonMediumMVA',
            # 'againstMuonTight',
            # 'againstMuonTight2',
            # 'againstMuonTight3',
            'againstMuonTightMVA',
            # 'byCombinedIsolationDeltaBetaCorrRaw3Hits',
            # 'byIsolationMVA3newDMwLTraw',
            # 'byIsolationMVA3newDMwoLTraw',
            # 'byIsolationMVA3oldDMwLTraw',
            # 'byIsolationMVA3oldDMwoLTraw',
            # 'byLooseCombinedIsolationDeltaBetaCorr3Hits',
            # 'byLooseIsolationMVA3newDMwLT',
            # 'byLooseIsolationMVA3newDMwoLT',
            # 'byLooseIsolationMVA3oldDMwLT',
            # 'byLooseIsolationMVA3oldDMwoLT',
            # 'byMediumCombinedIsolationDeltaBetaCorr3Hits',
            # 'byMediumIsolationMVA3newDMwLT',
            # 'byMediumIsolationMVA3newDMwoLT',
            # 'byMediumIsolationMVA3oldDMwLT',
            # 'byMediumIsolationMVA3oldDMwoLT',
            # 'byTightCombinedIsolationDeltaBetaCorr3Hits',
            # 'byTightIsolationMVA3newDMwLT',
            # 'byTightIsolationMVA3newDMwoLT',
            # 'byTightIsolationMVA3oldDMwLT',
            # 'byTightIsolationMVA3oldDMwoLT',
            # 'byVLooseIsolationMVA3newDMwLT',
            # 'byVLooseIsolationMVA3newDMwoLT',
            # 'byVLooseIsolationMVA3oldDMwLT',
            # 'byVLooseIsolationMVA3oldDMwoLT',
            # 'byVTightIsolationMVA3newDMwLT',
            # 'byVTightIsolationMVA3newDMwoLT',
            # 'byVTightIsolationMVA3oldDMwLT',
            # 'byVTightIsolationMVA3oldDMwoLT',
            # 'byVVTightIsolationMVA3newDMwLT',
            # 'byVVTightIsolationMVA3newDMwoLT',
            # 'byVVTightIsolationMVA3oldDMwLT',
            # 'byVVTightIsolationMVA3oldDMwoLT',
            'chargedIsoPtSum',
            'decayModeFinding',
            'decayModeFindingNewDMs',
            'neutralIsoPtSum',
            'puCorrPtSum'
            ]),

    bits      = cms.InputTag("TriggerResults","","HLT"),
    prescales = cms.InputTag("patTrigger"),
    objects   = cms.InputTag("selectedPatTrigger"),
    #triggerIdentifiers = cms.vstring(['DUMMY']),
    triggerIdentifiers = triggerPathNames, 

    jetMult_min   = cms.untracked.int32(-99),
    jetPt_min     = cms.untracked.double(20.),    
    muPt_min_     = cms.untracked.double(15.), 
    elePt_min_    = cms.untracked.double(15.), 
    tauPt_min_    = cms.untracked.double(15.), 

    )

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("ntuple.root"),
    #closeFileFast = cms.untracked.bool(True)
    )

process.load('RecoJets.JetProducers.caTopTaggers_cff')
process.hepTopTagPFJetsCHS.src = cms.InputTag("packedPFCandidates")

process.caTopTagInfos = cms.EDProducer("CATopJetTagger",
    src = cms.InputTag("cmsTopTagPFJetsCHS"),
    TopMass = cms.double(173),
    TopMassMin = cms.double(0.),
    TopMassMax = cms.double(250.),
    WMass = cms.double(80.4),
    WMassMin = cms.double(0.0),
    WMassMax = cms.double(200.0),
    MinMassMin = cms.double(0.0),
    MinMassMax = cms.double(200.0),
    verbose = cms.bool(False)
)

process.hepTopTagInfos = process.caTopTagInfos.clone(
    src = cms.InputTag("hepTopTagPFJetsCHS")
)

process.p = cms.Path(
    process.hepTopTagPFJetsCHS *
    process.hepTopTagInfos *
    process.tthNtupleAnalyzer
)

#process.out = cms.OutputModule(
#    "PoolOutputModule",
#    fileName = cms.untracked.string("edm.root"),
#    # Drop per-event meta data from dropped objects
#    dropMetaData = cms.untracked.string("ALL"),
#    SelectEvents = cms.untracked.PSet(
#        SelectEvents = cms.vstring("*")
#    ),
#    outputCommands = cms.untracked.vstring("keep *")
#)
#process.outpath = cms.EndPath(process.out)
