#!/usr/bin/env python
import os, time, sys, re, imp
import ROOT

import PhysicsTools.HeppyCore.framework.config as cfg
cfg.Analyzer.nosubdir=True
import PSet

t0 = time.time()
print "ARGV:",sys.argv

me_conf_name = "MEAnalysis_cfg_heppy.py"
for arg in sys.argv:
    if arg.startswith("ME_CONF="):
        me_conf_name = arg.split("=")[1]


JobNumber=sys.argv[1]
print "JobNumber", JobNumber
print PSet.process.dumpPython()

crabFiles=PSet.process.source.fileNames
print "crabFiles", crabFiles

firstInput = crabFiles[0]

###
### Convert LFN to PFN
###
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
print "timeto_convertPFN ",(time.time()-t0) #DS 

###
### VHBB code
###
handle = open("heppy_config.py", 'r')
cfo = imp.load_source("heppy_config", "heppy_config.py", handle)
config = cfo.config
config.preprocessor.options["lumisToProcess"] = PSet.process.source.lumisToProcess
handle.close()
print "timeto_setLumis ",(time.time()-t0) #DS 

#replace files with crab ones
config.components[0].files=crabFiles

print "heppy_config", config
from PhysicsTools.HeppyCore.framework.looper import Looper
looper = Looper( 'Output', config, nPrint=0)
looper.loop()
looper.write()
print "timeto_doVHbb ",(time.time()-t0) #DS

###
### tthbb13 code
###
print "Running tth code"
import cPickle as pickle
import TTH.MEAnalysis.TFClasses as TFClasses
sys.modules["TFClasses"] = TFClasses
os.environ["ME_CONF"] = os.environ["CMSSW_BASE"] + "/python/TTH/MEAnalysis/" + me_conf_name
handle = open("MEAnalysis_heppy.py", 'r')
cfo2 = imp.load_source("heppy_config", "MEAnalysis_heppy.py", handle)
config = cfo2.config
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import conf_to_str
print "MEM config", conf_to_str(cfo2.conf)
config.components = [cfg.Component(
    "dummy",
    files = ["Output/tree.root"],
    tree_name = "tree",
    n_gen = 1,
    xs = 1,
)]
config.components[0].isMC = cfo.sample.isMC
looper = Looper('Output_tth', config, nPrint=0)
looper.loop()
looper.write()
print "timeto_doMEM ",(time.time()-t0) #DS

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
tof.Close()

f=ROOT.TFile.Open('tree.root')
entries=f.Get('tree').GetEntries()

#Now write the FWKJobReport
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
print "timeto_totalJob ",(time.time()-t0) #DS
