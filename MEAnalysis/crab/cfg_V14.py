from WMCore.Configuration import Configuration
config = Configuration()

#****************************DS CHANGE THIS && samples_v14.py (set to False) && inputfilename/script && COMPILE ****
# processing_name = "TTH_v3" #v1 done with QCD300 in samples_V14, v2 ok
# processing_name = "TTJets_v2" #v1 done with TTJets??
# processing_name = "QCD300_v2" #v1 done with QCD300 in samples
# processing_name = "QCD500_v1"
# processing_name = "QCD700_v3" #v2 done with QCD700 in samples
processing_name = "QCD1000_v1"
# processing_name = "QCD1500_v1"
# processing_name = "QCD2000_v5" #v3 done with QCD700 in samples_V14

sample = processing_name.split("_")[0]

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
#the output file is automatically configured by the fake PSet
#config.JobType.outputFiles = ['tree.root']

config.section_("Data")
#this name will be used for creating the output directory
config.Data.primaryDataset = "/" + sample + "/V14/MEM" #DS
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/dsalerno/tthbb745/VHBBHeppyV14/' #DS
config.Data.publication = False
config.Data.userInputFiles = open( sample+".txt").readlines() #DS

config.section_("Site")
#config.Site.storageSite = "T2_CH_CSCS"
config.Site.storageSite = "T3_CH_PSI" #DS

#config.Data.ignoreLocality = True
