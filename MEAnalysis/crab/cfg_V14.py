from WMCore.Configuration import Configuration
config = Configuration()

#****************************DS CHANGE THIS && samples_v14.py (set to False) && userInputFiles/script && COMPILE ****
# processing_name = "TTH_v1"
# processing_name = "TTJets_v1"
# processing_name = "QCD300_v1"
# processing_name = "QCD500_v1"
# processing_name = "QCD700_v1"
# processing_name = "QCD1000_v" #forgot the v1
# processing_name = "QCD1500_v1"
processing_name = "QCD2000_v1"

sample = processing_name.split("_")[0]

config.section_("General")
#this will be used for the crab directory name
config.General.requestName = processing_name #DS
config.General.workArea = 'crab_projects_mem_V14_all/' #DS
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'heppy_crab_fake_pset.py'
config.JobType.scriptExe = 'heppy_crab_script.sh'
#job maximum runtime in minutes
config.JobType.maxJobRuntimeMin = 2750 # 46 * 60

import os
#we need to specially ship the python and data directories

os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")
os.system("tar czf data.tar.gz --dereference --directory $CMSSW_BASE/src/TTH/MEAnalysis root")
config.JobType.inputFiles = [
    'heppy_crab_script.py',
    'python.tar.gz',
    'data.tar.gz',
    #'combined_cmssw.py',
    #'tthbb.py',
    "../python/MEAnalysis_heppy.py" #DS
]
#the output file is automatically configured by the fake PSet
#config.JobType.outputFiles = ['tree.root']

config.section_("Data")
#this name will be used for creating the output directory
config.Data.outputPrimaryDataset = sample #"/" + sample + "/V14/MEM" #DS
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/dsalerno/tthbb745/VHBBHeppyV14_all/' #DS
config.Data.publication = False
#config.Data.userInputFiles = open( sample+".txt").readlines() #DS
config.Data.userInputFiles = open( sample+".jobs").readlines() #DS change in heppy_crab_script.py

config.section_("Site")
#config.Site.storageSite = "T2_CH_CSCS"
config.Site.storageSite = "T3_CH_PSI" #DS
config.Site.blacklist = ["T3_US_FIT*"]
config.Site.whitelist = ["T2_IT*","T2_CH*","T2_FR*", "T2_DE*"]

#config.Data.ignoreLocality = True
