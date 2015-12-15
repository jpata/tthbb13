PARCMD=~/parallel --gnu

.PHONY: clean

SYNCPATH=~/tth/spring15/sync/

pick:
	edmCopyPickMerge inputFiles=file:///home/joosep/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/141B9915-1F08-E511-B9FF-001E675A6AB3.root outputFile=picked.root eventsToProcess=1:12701:2532028,1:8271:1648889,1:6588:1313413

download:
	#mkdir -p $(SYNCPATH) 
	#xrdcp root://xrootd.unl.edu//store/mc/RunIISpring15MiniAODv2/ttHTobb_M125_13TeV_powheg_pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/DA1B6FD6-C46D-E511-9C7B-00A0D1EE29B8.root $(SYNCPATH)/tth.root
	#xrdcp root://xrootd.unl.edu//store/mc/RunIISpring15MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/0EE7E064-BE6F-E511-BB41-E4115BB4C4BC.root $(SYNCPATH)/ttjets_1.root
	#xrdcp root://xrootd.unl.edu//store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/10000/021FD3F0-876F-E511-99D2-0025905A6060.root $(SYNCPATH)/singlemu.root
	#xrdcp root://xrootd.unl.edu//store/data/Run2015D/MuonEG/MINIAOD/05Oct2015-v2/60000/00D43A12-C573-E511-8F4C-0025905A60E0.root $(SYNCPATH)/muoneg.root
	xrdcp root://cmsxrootd.fnal.gov///store/user/hmildner/el_skim_3loosejets.root $(SYNCPATH)/el_skim_3loosejets.root
	xrdcp root://cmsxrootd.fnal.gov///store/user/hmildner/mu_skim_3loosejets.root $(SYNCPATH)/mu_skim_3loosejets.root
	xrdcp root://cmsxrootd.fnal.gov///store/user/hmildner/muel_skim_2loosejets.root $(SYNCPATH)/muel_skim_2loosejets.root

split:
	mkdir -p ~/tth/spring15/sync/ttjets_1/
	edmLumisInFiles.py ~/tth/spring15/sync/ttjets_1.root > ~/tth/spring15/sync/ttjets_1/lumilist.json 
	python $(CMSSW_BASE)/src/TTH/MEAnalysis/python/splitLumi.py ~/tth/spring15/sync/ttjets_1/lumilist.json ~/tth/spring15/sync/ttjets_1/
	ls ~/tth/spring15/sync/ttjets_1/block*.json | $(PARCMD) -j40 cmsRun $(CMSSW_BASE)/src/TTH/TTHNtupleAnalyzer/python/pickEvents2_cfg.py inputFiles=file://$(HOME)/tth/spring15/sync/ttjets_1.root lumifile={} outputFile=~/tth/spring15/sync/ttjets_1/block_{#}.root 
	
	mkdir -p ~/tth/spring15/sync/tth/
	edmLumisInFiles.py ~/tth/spring15/sync/tth.root > ~/tth/spring15/sync/tth/lumilist.json 
	python $(CMSSW_BASE)/src/TTH/MEAnalysis/python/splitLumi.py ~/tth/spring15/sync/tth/lumilist.json ~/tth/spring15/sync/tth/
	ls ~/tth/spring15/sync/tth/block*.json | $(PARCMD) -j40 cmsRun $(CMSSW_BASE)/src/TTH/TTHNtupleAnalyzer/python/pickEvents2_cfg.py inputFiles=file://$(HOME)/tth/spring15/sync/tth.root lumifile={} outputFile=~/tth/spring15/sync/tth/block_{#}.root 
	
	mkdir -p ~/tth/spring15/sync/el_skim/
	edmLumisInFiles.py ~/tth/spring15/sync/el_skim_3loosejets.root > ~/tth/spring15/sync/el_skim/lumilist.json
	python $(CMSSW_BASE)/src/TTH/MEAnalysis/python/splitLumi.py ~/tth/spring15/sync/el_skim/lumilist.json ~/tth/spring15/sync/el_skim/
	ls ~/tth/spring15/sync/el_skim/block*.json | $(PARCMD) -j40 cmsRun $(CMSSW_BASE)/src/TTH/TTHNtupleAnalyzer/python/pickEvents2_cfg.py inputFiles=file://$(HOME)/tth/spring15/sync/el_skim_3loosejets.root lumifile={} outputFile=~/tth/spring15/sync/el_skim/block_{#}.root
	
	mkdir -p ~/tth/spring15/sync/mu_skim/
	edmLumisInFiles.py ~/tth/spring15/sync/mu_skim_3loosejets.root > ~/tth/spring15/sync/mu_skim/lumilist.json
	python $(CMSSW_BASE)/src/TTH/MEAnalysis/python/splitLumi.py ~/tth/spring15/sync/mu_skim/lumilist.json ~/tth/spring15/sync/mu_skim/
	ls ~/tth/spring15/sync/mu_skim/block*.json | $(PARCMD) -j40 cmsRun $(CMSSW_BASE)/src/TTH/TTHNtupleAnalyzer/python/pickEvents2_cfg.py inputFiles=file://$(HOME)/tth/spring15/sync/mu_skim_3loosejets.root lumifile={} outputFile=~/tth/spring15/sync/mu_skim/block_{#}.root
	
	mkdir -p ~/tth/spring15/sync/muel_skim/
	edmLumisInFiles.py ~/tth/spring15/sync/muel_skim_2loosejets.root > ~/tth/spring15/sync/muel_skim/lumilist.json
	python $(CMSSW_BASE)/src/TTH/MEAnalysis/python/splitLumi.py ~/tth/spring15/sync/muel_skim/lumilist.json ~/tth/spring15/sync/muel_skim/
	ls ~/tth/spring15/sync/muel_skim/block*.json | $(PARCMD) -j40 cmsRun $(CMSSW_BASE)/src/TTH/TTHNtupleAnalyzer/python/pickEvents2_cfg.py inputFiles=file://$(HOME)/tth/spring15/sync/muel_skim_2loosejets.root lumifile={} outputFile=~/tth/spring15/sync/muel_skim/block_{#}.root

step2:
	#mkdir -p ~/tth/spring15/sync/vhbb/v10/
	hadd -f ~/tth/spring15/sync/vhbb/v10/ttjets.root ~/tth/sw/CMSSW_7_4_15/src/VHbbAnalysis/Heppy/test/Loop_task_ttjets_*_1/tree.root
	hadd -f ~/tth/spring15/sync/vhbb/v10/tth.root ~/tth/sw/CMSSW_7_4_15/src/VHbbAnalysis/Heppy/test/Loop_task_tth_*_1/tree.root
	hadd -f ~/tth/spring15/sync/vhbb/v10/mu_skim.root ~/tth/sw/CMSSW_7_4_15/src/VHbbAnalysis/Heppy/test/Loop_task_mu_skim_*/tree.root
	hadd -f ~/tth/spring15/sync/vhbb/v10/el_skim.root ~/tth/sw/CMSSW_7_4_15/src/VHbbAnalysis/Heppy/test/Loop_task_el_skim_*/tree.root
	hadd -f ~/tth/spring15/sync/vhbb/v10/muel_skim.root ~/tth/sw/CMSSW_7_4_15/src/VHbbAnalysis/Heppy/test/Loop_task_muel_skim_*/tree.root

step3:
	hadd -f ~/tth/spring15/sync/tthbb/ttjets.root ~/tth/gc/GCb043a9d6bed0/cfg_sync/ttjets/output_*.root
	hadd -f ~/tth/spring15/sync/tthbb/tth.root ~/tth/gc/GCb043a9d6bed0/cfg_sync/ttH/output_*.root

step4:
	python python/makeTable.py /home/joosep/tth/spring15/sync/tthbb/tth.root nominal > tth.csv
	python python/makeTable.py /home/joosep/tth/spring15/sync/tthbb/ttjets.root nominal > ttjets.csv

clean:
	rm -Rf $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/Loop_*
