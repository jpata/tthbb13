from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'ttHTobb_M125_13TeV_powheg_pythia8'
config.General.workArea = 'crab_projects_mem'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'heppy_crab_fake_pset.py'
config.JobType.scriptExe = 'heppy_crab_script.sh'
config.JobType.maxJobRuntimeMin = 6 * 60

import os
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
#config.JobType.outputFiles = ['tree.root']

config.section_("Data")
config.Data.primaryDataset = 'ttHTobb_M125_13TeV_powheg_pythia8'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/jpata/tthbb13/VHBBHeppyV12/test2'
config.Data.publication = False
filelist = open("sig.dat").readlines()
#filelist = map(lambda x: "root://ganymede.hep.kbfi.ee:1094//" + x, filelist)
#filelist = map(lambda x: "root://xrootd-cms.infn.it//" + x, filelist)
#filelist = map(lambda x: x.strip(), filelist)
print "filelist=", filelist
config.Data.userInputFiles = filelist
#config.Data.publishDataName = 'VHBB_HEPPY_V12'

config.section_("Site")
config.Site.storageSite = "T2_CH_CSCS"
#config.Site.storageSite = "T2_EE_Estonia"

#config.Data.ignoreLocality = True
