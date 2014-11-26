from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'WD_TTbarH_HToBB'
config.General.workArea = 'crab_TTH_Oct22'
config.General.saveLogs = True
config.General.requestName = "tth/step1/nov24/TTbarH_HToBB_"

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/home/joosep/Dropbox/tthbb13/CMSSW/src/TTH/TTHNtupleAnalyzer/python/Main_cfg.py'
#job runtime in minutes
config.JobType.maxjobruntime = 60*48

config.section_("Data")
config.Data.inputDataset = '/TTbarH_HToBB_M-125_13TeV_pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM'
config.Data.dbsUrl = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.publication = False
#config.Data.publishDbsUrl = 'phys03'
#config.Data.publishDataName = 'tth_ntp_test1'

config.section_("Site")
#config.Site.storageSite = "T2_CH_CSCS"
config.Site.storageSite = "T2_EE_Estonia"
