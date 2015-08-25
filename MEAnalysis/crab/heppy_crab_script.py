#!/usr/bin/env python
print "heppy_crab_script.py started"
import ROOT
import os
import PhysicsTools.HeppyCore.framework.config as cfg
cfg.Analyzer.nosubdir=True

import PSet
import sys
import re
print "ARGV:",sys.argv
JobNumber = sys.argv[1]
crabFiles = PSet.process.source.fileNames
print "crabFiles=", crabFiles
firstInput = crabFiles[0]
tf = ROOT.TFile.Open(firstInput)
tt = tf.Get("tree")
print "file entries", tt.GetEntries()
tf.Close()
#print "--------------- using edmFileUtil to convert PFN to LFN -------------------------"
#for i in xrange(0,len(crabFiles)) :
#     if os.getenv("GLIDECLIENT_Group","") != "overflow" :
#       print "Data is local"
#       pfn=os.popen("edmFileUtil -d %s"%(crabFiles[i])).read() 
#       pfn=re.sub("\n","",pfn)
#       print crabFiles[i],"->",pfn
#       crabFiles[i]=pfn
#     else:
#       print "Data is not local, using AAA/xrootd"
#       crabFiles[i]="root://cms-xrd-global.cern.ch/"+crabFiles[i]

import imp
import cPickle as pickle
import TTH.MEAnalysis.TFClasses as TFClasses
import sys
sys.modules["TFClasses"] = TFClasses

handle = open("MEAnalysis_heppy.py", 'r')
cfo = imp.load_source("heppy_config", "MEAnalysis_heppy.py", handle)
config = cfo.config
handle.close()

#replace files with crab ones
config.components[0].files=crabFiles

from PhysicsTools.HeppyCore.framework.looper import Looper
looper = Looper( 'Output', config, nPrint = 1)
looper.loop()
looper.write()

print PSet.process.output.fileName
os.rename("Output/tree.root", "tree.root")

import ROOT
f=ROOT.TFile.Open('tree.root')
entries=f.Get('tree').GetEntries()
#entries = 0

fwkreport='''<FrameworkJobReport>
<ReadBranches>
</ReadBranches>
<PerformanceReport>
  <PerformanceSummary Metric="StorageStatistics">
    <Metric Name="Parameter-untracked-bool-enabled" Value="true"/>
    <Metric Name="Parameter-untracked-bool-stats" Value="true"/>
    <Metric Name="Parameter-untracked-string-cacheHint" Value="application-only"/>
    <Metric Name="Parameter-untracked-string-readHint" Value="auto-detect"/>
    <Metric Name="ROOT-tfile-read-totalMegabytes" Value="0"/>
    <Metric Name="ROOT-tfile-write-totalMegabytes" Value="0"/>
  </PerformanceSummary>
</PerformanceReport>

<GeneratorInfo>
</GeneratorInfo>

<InputFile>
<LFN>%s</LFN>
<PFN></PFN>
<Catalog></Catalog>
<InputType>primaryFiles</InputType>
<ModuleLabel>source</ModuleLabel>
<GUID></GUID>
<InputSourceClass>PoolSource</InputSourceClass>
<EventsRead>1</EventsRead>

</InputFile>

<File>
<LFN></LFN>
<PFN>tree.root</PFN>
<Catalog></Catalog>
<ModuleLabel>HEPPY</ModuleLabel>
<GUID></GUID>
<OutputModuleClass>PoolOutputModule</OutputModuleClass>
<TotalEvents>%s</TotalEvents>
<BranchHash>dc90308e392b2fa1e0eff46acbfa24bc</BranchHash>
</File>

</FrameworkJobReport>''' % (firstInput,entries)

f1=open('./FrameworkJobReport.xml', 'w+')
f1.write(fwkreport)
print "heppy crab script wrote FJR xml"
print "heppy crab script is done!"
