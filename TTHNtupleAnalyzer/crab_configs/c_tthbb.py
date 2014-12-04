from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'WD_TTbarH_HToBB'
config.General.workArea = 'crab_TTH_2014_12_05'
config.General.transferLogs = True
config.General.requestName = "tth_step1_2014_12_05_TTbarH_HToBB_"


config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/shome/gregor/TTH-72X/CMSSW/src/TTH/TTHNtupleAnalyzer/python/Main_cfg.py'
config.JobType.allowNonProductionCMSSW = True
#job runtime in minutes
config.JobType.maxJobRuntimeMin =60*48


config.section_("Data")
config.Data.inputDataset = '/TTbarH_HToBB_M-125_13TeV_pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 10
config.Data.publication = False
#config.Data.publishDbsUrl = 'phys03'
#config.Data.publishDataName = 'tth_ntp_test1'

config.section_("Site")
config.Site.storageSite = "T2_CH_CSCS"
#config.Site.storageSite = "T2_EE_Estonia"
