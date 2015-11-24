#!/usr/bin/env python

errmsg = None
retcode = 0
filename = ""
entries = 0

rootprefix = "root://eoscms.cern.ch//eos/cms/"
siteprefix = "/store/group/phys_higgs/hbb/ntuples/V16pre/"

def findSampleName(n):
    n = n.replace(rootprefix + siteprefix, "")
    spl = n.split("/")
    return spl[0]
try:
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
    filename, firstEvent, nEvents = firstInput.split("___")
    #rootfilename = "root://xrootd-cms.infn.it//" + filename
    #rootfilename = "root://148.187.64.51:1094//pnfs/lcg.cscs.ch/cms/trivcat/" + filename
    rootfilename = rootprefix + filename
    firstEvent = int(firstEvent)
    nEvents = int(nEvents)
    print "checking file",rootfilename
    tf = ROOT.TFile.Open(rootfilename)
    if not tf or tf.IsZombie():
        retcode = 8020 
        raise Exception("Could not open: {0}".format(rootfilename))
    tt = tf.Get("tree")
    nentries = tt.GetEntries()
    print "file entries", tt.GetEntries()
    if firstEvent > nentries:
        retcode = 8010 
        raise Exception("wrong entry number: {0}".format(firstEvent))
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
  
    config = None 
    try:  
        handle = None
        handle = open("MEAnalysis_heppy.py", 'r')
        cfo = imp.load_source("heppy_config", "MEAnalysis_heppy.py", handle)
        config = cfo.config
        handle.close()
    except AttributeError as e:
        retcode = 8001
        raise e

    from TTH.MEAnalysis.MEAnalysis_cfg_heppy import conf_to_str
    print "MEM config", conf_to_str(cfo.conf)
    
    #replace files with crab ones
    #Also get the correct sample (xsec) based on the file name
    #config.components[0].files=[rootfilename]
    sampleName = findSampleName(rootfilename)
    sample = cfo.samples_dict[sampleName]
    sample.subFiles = [rootfilename]
    print "Running over sample", sample
    config.components = [cfg.Component(
        sample.name.value(),
        files = [rootfilename],
        tree_name = "tree",
        n_gen = sample.nGen.value(),
        xs = sample.xSec.value(),
    )]
    #need to set isMC like this for heppy to find it
    config.components[0].isMC = sample.isMC.value()

    from PhysicsTools.HeppyCore.framework.looper import Looper
    print "processing",rootfilename, firstEvent, nEvents
    looper = Looper( 'Output', config, nPrint = 0, firstEvent=firstEvent, nEvents=nEvents)
    try:
        looper.loop()
    except Exception as e:
        retcode = 8021
        raise e
    looper.write()
    
    print "output file:", PSet.process.output.fileName
    os.rename("Output/tree.root", "tree.root")
    
    import ROOT
    f=ROOT.TFile.Open('tree.root')
    entries = f.Get('tree').GetEntries()
    #entries = 0
except Exception as e:
    import traceback
    errmsg = str(e) + "\n" + traceback.format_exc()
    if retcode == 0:
        retcode = 8003
    print "ERROR:", errmsg
finally:
    fwkerr = ""
    if retcode != 0:
        fwkerr = '''
<FrameworkError ExitStatus="{0}" Type="Fatal Exception" >
<![CDATA[{1}]]>
</FrameworkError>
'''.format(retcode, retcode)

    fwkreport='''<FrameworkJobReport>
    {2}
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
    <LFN>{0}</LFN>
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
    <TotalEvents>{1}</TotalEvents>
    <BranchHash>dc90308e392b2fa1e0eff46acbfa24bc</BranchHash>
    </File>
    </FrameworkJobReport>'''.format(filename, entries, fwkerr)
     
    f1=open('./FrameworkJobReport.xml', 'w+')
    f1.write(fwkreport)
    print "heppy crab script wrote FJR xml"
    print "heppy crab script is done!"
    print fwkreport
