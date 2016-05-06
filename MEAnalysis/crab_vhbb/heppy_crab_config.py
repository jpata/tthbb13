from WMCore.Configuration import Configuration
config = Configuration()

submitname = "VHBBHeppyV21_tthbbV9_May4"

config.section_("General")
config.General.requestName = 'tth_' + submitname
config.General.workArea = 'crab_projects/' + submitname
config.General.transferLogs = True

config.section_("JobType")
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
#config.JobType.outputFiles = ['tree.root']

config.section_("Data")
config.Data.inputDataset = '/ttHTobb_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 10
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/jpata/tth/' + submitname
config.Data.publication = True
config.Data.outputDatasetTag = submitname
config.Data.ignoreLocality = False

config.section_("Site")
config.Site.storageSite = "T2_CH_CSCS"
