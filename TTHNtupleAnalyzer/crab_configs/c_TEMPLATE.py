from WMCore.Configuration import Configuration

global config

config = Configuration()

config.section_("General")
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxJobRuntimeMin = 60*24 #maximal job runtime in minute
config.JobType.scriptExe = 'myScript.sh'
config.JobType.inputFiles = ["../python/MakeTaggingNtuple.py", "../python/AccessHelpers.py"]
#config.JobType.outputFiles = ["output-tagging.root"]
config.JobType.outputFiles = ["output.root"]

config.section_("Data")
config.Data.inputDBS = 'global'
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
config.Data.publication = False

config.Data.allowNonValidInputDataset = True 

config.Data.unitsPerJob = 10
#config.Data.totalUnits = 5

config.section_("Site")



