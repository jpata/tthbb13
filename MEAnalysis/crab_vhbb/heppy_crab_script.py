#!/usr/bin/env python
import os
import PhysicsTools.HeppyCore.framework.config as cfg
import ROOT

cfg.Analyzer.nosubdir=True

import PSet
import sys
import re
print "ARGV:",sys.argv
JobNumber=sys.argv[1]
print PSet.process.dumpPython()
crabFiles=PSet.process.source.fileNames
print crabFiles
firstInput = crabFiles[0]
print "--------------- using edmFileUtil to convert PFN to LFN -------------------------"
for i in xrange(0,len(crabFiles)) :
     if ((os.getenv("GLIDECLIENT_Group","") != "overflow" and
        os.getenv("GLIDECLIENT_Group","") != "overflow_conservative") or "file:/" in crabFiles[i]):
       print "Data is local"
       pfn=os.popen("edmFileUtil -d %s"%(crabFiles[i])).read() 
       pfn=re.sub("\n","",pfn)
       print crabFiles[i],"->",pfn
       crabFiles[i]=pfn
     else:
       print "Data is not local, using AAA/xrootd"
       crabFiles[i]="root://cms-xrd-global.cern.ch/"+crabFiles[i]

import imp
handle = open("heppy_config.py", 'r')
cfo = imp.load_source("heppy_config", "heppy_config.py", handle)
config = cfo.config
config.preprocessor.options["lumisToProcess"] = PSet.process.source.lumisToProcess
handle.close()

#replace files with crab ones
config.components[0].files=crabFiles

print config
from PhysicsTools.HeppyCore.framework.looper import Looper
looper = Looper( 'Output', config, nPrint=0)
looper.loop()
looper.write()

print "Running tth code"
import imp
import cPickle as pickle
import TTH.MEAnalysis.TFClasses as TFClasses
import sys
sys.modules["TFClasses"] = TFClasses
        
handle = None
handle = open("MEAnalysis_heppy.py", 'r')
cfo = imp.load_source("heppy_config", "MEAnalysis_heppy.py", handle)
config = cfo.config
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import conf_to_str
print "MEM config", conf_to_str(cfo.conf)
config.components = [cfg.Component(
    "dummy",
    files = ["Output/tree.root"],
    tree_name = "tree",
    n_gen = 1,
    xs = 1,
)]
config.components[0].isMC = True
looper = Looper('Output_tth', config, nPrint=0)
looper.loop()
looper.write()

#Now we need to copy both the vhbb and tth outputs to the same file
inf1 = ROOT.TFile("Output/tree.root")
inf2 = ROOT.TFile("Output_tth/tree.root")
tof = ROOT.TFile("tree.root", "RECREATE")

vhbb_dir = tof.mkdir("vhbb")
def copyTo(src, dst):
    #copy ttjets output
    dst.cd()
    for k in src.GetListOfKeys():
        o = k.ReadObj()
        if o.ClassName() == "TTree":
            o = o.CloneTree()
        else:
            o = o.Clone()
        print k, o 
        dst.Add(o) 
        o.Write("", ROOT.TObject.kOverwrite)

copyTo(inf1, vhbb_dir)
copyTo(inf2, tof)

#print PSet.process.output.fileName
#os.system("./addTreeFiles.py tree.root Output/tree.root Output_tth/tree.root")

f=ROOT.TFile.Open('tree.root')
entries=f.Get('tree').GetEntries()

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
