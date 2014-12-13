from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'WD_TTbarH_HToBB'
config.General.workArea = 'WD_TTH'
config.General.transferLogs = True
config.General.requestName = "tth_tep1_nov24_TTbarH_HToBB"

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/home/joosep/Dropbox/tthbb13_72/CMSSW/src/TTH/TTHNtupleAnalyzer/python/Main_cfg.py'
#job runtime in minutes
config.JobType.maxJobRuntimeMin = 60*48

config.section_("Data")
config.Data.inputDataset = '/TTbarH_HToBB_M-125_13TeV_pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM'
config.Data.inputDBS = 'global'

config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2

config.Data.publication = False
#config.Data.publishDbsUrl = 'phys03'
#config.Data.publishDataName = 'tth_ntp_test1'

config.section_("Site")
config.Site.storageSite = "T2_CH_CSCS"
#config.Site.storageSite = "T2_EE_Estonia"
