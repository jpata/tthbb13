from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'tthbb13_mem_test1'
config.General.workArea = 'crab_projects_mem_test1'
config.General.transferLogs=True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'heppy_crab_fake_pset.py'
config.JobType.scriptExe = 'heppy_crab_script.sh'
import os
#os.system("tar czf python.tar.gz --dereference --directory $CMSSW_BASE python")
config.JobType.inputFiles = [
    'heppy_crab_script.py',
    #'python.tar.gz',
    #'combined_cmssw.py',
    #'tthbb.py',
]
#config.JobType.outputFiles = ['tree.root']

config.section_("Data")
config.Data.primaryDataset = 'VHBBHeppyV12'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = 5
config.Data.outLFNDirBase = '/store/user/jpata/tthbb13/'
config.Data.publication = False
filelist = open("sig.dat").readlines()
filelist = map(lambda x: "root://cms-xrd-global.cern.ch/" + x, filelist)
filelist = map(lambda x: x.strip(), filelist)
print "filelist=", filelist
config.Data.userInputFiles = filelist
#config.Data.publishDataName = 'VHBB_HEPPY_V12'

config.section_("Site")
config.Site.storageSite = "T3_CH_PSI"

#config.Data.ignoreLocality = True
