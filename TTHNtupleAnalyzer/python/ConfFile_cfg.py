import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger = cms.Service("MessageLogger",
        destinations=cms.untracked.vstring('cerr', 'debug', 'cout'),
        debugModules=cms.untracked.vstring('*'),
        cerr=cms.untracked.PSet(
            threshold=cms.untracked.string('ERROR'),
        #    FwkReport = cms.untracked.PSet(
        #        reportEvery = cms.untracked.int32(100),
        #    ),
        ),
        cout=cms.untracked.PSet(
            threshold=cms.untracked.string('INFO'),
            #FwkReport = cms.untracked.PSet(
            #    reportEvery = cms.untracked.int32(100),
            #),
        ),
        debug=cms.untracked.PSet(threshold=cms.untracked.string('DEBUG')),
)
#process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        'file:/hdfs/local/joosep/ttbar_miniaod.root'
    )
)

process.tthNtupleAnalyzer = cms.EDAnalyzer('TTHNtupleAnalyzer',
    isMC = cms.bool(True),
    vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    muons = cms.InputTag("slimmedMuons"),
    electrons = cms.InputTag("slimmedElectrons"),
    taus = cms.InputTag("slimmedTaus"),
    jets = cms.InputTag("slimmedJets"),
    packed = cms.InputTag("packedGenParticles"),
    pruned = cms.InputTag("prunedGenParticles"),
    fatjets = cms.InputTag("slimmedJetsAK8"),
    mets = cms.InputTag("slimmedMETs"),
    lhe = cms.InputTag("externalLHEProducer"),
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
        ])
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("ntuple.root"),
    #closeFileFast = cms.untracked.bool(True)
)


process.p = cms.Path(process.tthNtupleAnalyzer)
