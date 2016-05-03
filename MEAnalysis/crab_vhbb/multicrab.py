dataset = {
    'ttH':'/ttHTobb_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
    'TTbar':'/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1/MINIAODSIM',
    'QCD300':'/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
    'QCD500':'/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
    'QCD700':'/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
    'QCD1000':'/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
    'QCD1500':'/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
    'QCD2000':'/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM',
}

nlumis = {
    'ttH':     -1,
    'TTbar':   99000,
    'QCD300':  -1,
    'QCD500':  -1,
    'QCD700':  -1,
    'QCD1000': -1,
    'QCD1500': -1,
    'QCD2000': -1,
}

lumisPerJob = {
    'ttH':     10,
    'TTbar':   200,
    'QCD300':  500,
    'QCD500':  500,
    'QCD700':  300,
    'QCD1000': 200,
    'QCD1500': 100,
    'QCD2000': 100,
}

version = '_v1'  #***************CHANGE HERE***************

fractionlumis=10 #>1 for testing

if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand

    def submit(config):
        res = crabCommand('submit', config = config)

    from CRABClient.UserUtilities import config
    config = config()
    name = 'VHBBHeppyV21_tthbbV9' + version
    config.General.workArea = 'crab_projects/'+name
    config.General.transferLogs = True

    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'heppy_crab_fake_pset.py'
    config.JobType.scriptExe = 'heppy_crab_script.sh'
    config.JobType.maxJobRuntimeMin = 40 * 60

    import os
    os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")
    os.system("tar czf data.tar.gz --dereference --directory $CMSSW_BASE/src/TTH/MEAnalysis root")
    
    vhbb_dir = os.environ.get("CMSSW_BASE") + "/src/VHbbAnalysis/Heppy/test"
    config.JobType.inputFiles = ['heppy_config.py',
                                 'heppy_crab_script.py',
                                 'python.tar.gz',
                                 'data.tar.gz',
                                 "MEAnalysis_heppy.py",
                                 'MVAJetTags_620SLHCX_Phase1And2Upgrade.db',
                                 'combined_cmssw.py',
                                 vhbb_dir + '/vhbb.py',
                                 vhbb_dir + '/vhbb_combined.py',
                                 'TMVAClassification_BDT.weights.xml',
                                 'puData.root',
                                 vhbb_dir + '/puDataMinus.root',
                                 vhbb_dir + '/puDataPlus.root',
                                 'puMC.root',
                                 'json.txt',
                                 vhbb_dir + "/Zll-spring15.weights.xml",
                                 vhbb_dir + "/Wln-spring15.weights.xml",
                                 vhbb_dir + "/Znn-spring15.weights.xml",
                                 vhbb_dir + "/VBF-spring15.weights.xml",
                                 vhbb_dir + "/ttbar-fall15_TargetGenOverPt_GenPtCut0.weights.xml",
                                 vhbb_dir + '/TMVA_blikelihood_vbf_cmssw76_h21trained.weights.xml'
]

    config.Data.inputDBS = 'global'
    config.Data.splitting = 'LumiBased'
    config.Data.publication = True
    config.Data.ignoreLocality = False

    config.Site.storageSite = "T2_CH_CSCS"

    listOfSamples = ['ttH','TTbar','QCD300','QCD500','QCD700','QCD1000','QCD1500','QCD2000'] #******CHOOSE HERE*********

    #loop over samples
    for sample in listOfSamples:
        print ''
        print 'submitting ' + sample
        config.General.requestName = sample + version
        config.Data.inputDataset = dataset[sample]
        config.Data.unitsPerJob = lumisPerJob[sample]/fractionlumis
        if fractionlumis>1:
            config.Data.totalUnits = lumisPerJob[sample]
        else:
            config.Data.totalUnits = nlumis[sample]
        config.Data.outputDatasetTag = name
        config.Data.outLFNDirBase = '/store/user/dsalerno/tth/' + name
	submit(config)
