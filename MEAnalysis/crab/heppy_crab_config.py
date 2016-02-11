from WMCore.Configuration import Configuration
config = Configuration()
import os

processing_name = "Feb9_GITHASH" 
config.section_("General")
#this will be used for the crab directory name
config.General.requestName = DNAME
config.General.workArea = 'crab_projects_mem/' + processing_name
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'heppy_crab_fake_pset.py'
config.JobType.scriptExe = 'heppy_crab_script.sh'
#job maximum runtime in minutes
config.JobType.maxJobRuntimeMin = 47 * 60

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
    "MEAnalysis_heppy.py"
]
#the output file is automaticalluy configured by the fake PSet
#config.JobType.outputFiles = ['tree.root']

config.section_("Data")
#this name will be used for creating the output directory
config.Data.outputPrimaryDataset = FULLDAS
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/jpata/tthbb13/VHBBHeppyV16pre/' + processing_name
config.Data.publication = False
filelist = open(DATASET).readlines()
config.Data.userInputFiles = filelist

config.section_("Site")
#config.Site.storageSite = "T3_CH_PSI"
#config.Site.storageSite = "T2_CH_CSCS"
config.Site.storageSite = "T2_EE_Estonia"
config.Site.blacklist = ["T2_UA_KIPT", "T3_US_FIT"]
#config.Data.ignoreLocality = True
