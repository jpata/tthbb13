from WMCore.Configuration import Configuration
config = Configuration()

processing_name = "TTH_v7" #DS
config.section_("General")
#this will be used for the crab directory name
config.General.requestName = processing_name #DS
config.General.workArea = 'crab_projects_mem/' #DS
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'heppy_crab_fake_pset.py'
config.JobType.scriptExe = 'heppy_crab_script.sh'
#job maximum runtime in minutes
config.JobType.maxJobRuntimeMin = 46 * 60

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
#the output file is automaticalluy configured by the fake PSet
#config.JobType.outputFiles = ['tree.root']

config.section_("Data")
#this name will be used for creating the output directory
config.Data.primaryDataset = "/ttHTobb_M125_13TeV_powheg_pythia8/V12/MEM" #'/ttHpowheg' #DS - same as request name
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/dsalerno/tthbb745/VHBBHeppyV12/' + processing_name #DS
config.Data.publication = False
config.Data.userInputFiles = open("ttHTobb_M125_13TeV_powheg_pythia8.txt").readlines() #DS

config.section_("Site")
#config.Site.storageSite = "T2_CH_CSCS"
config.Site.storageSite = "T3_CH_PSI" #DS

#config.Data.ignoreLocality = True
