from WMCore.Configuration import Configuration

global config

config = Configuration()

config.section_("General")
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.allowNonProductionCMSSW = True
config.JobType.maxJobRuntimeMin = 60*48 #maximal job runtime in minutes

config.section_("Data")
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.publication = False

config.section_("Site")



