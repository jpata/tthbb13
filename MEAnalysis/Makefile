PARCMD=~/parallel --gnu

.PHONY: clean

pick:
	edmCopyPickMerge inputFiles=file:///home/joosep/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/141B9915-1F08-E511-B9FF-001E675A6AB3.root outputFile=picked.root eventsToProcess=1:12701:2532028,1:8271:1648889,1:6588:1313413

download:
	mkdir -p ~/tth/spring15/sync/
	#/store/mc/RunIISpring15MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2_ext3-v1/10000/3231C86E-746E-E511-9978-0025905A60B8.root
	xrdcp root://xrootd.unl.edu//store/mc/RunIISpring15MiniAODv2/ttHTobb_M125_13TeV_powheg_pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/30000/DA1B6FD6-C46D-E511-9C7B-00A0D1EE29B8.root tth.root
	xrdcp root://xrootd.unl.edu//store/mc/RunIISpring15MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/0EE7E064-BE6F-E511-BB41-E4115BB4C4BC.root ttjets_1.root


split:
	mkdir -p ~/tth/spring15/sync/ttjets_1/
	edmLumisInFiles.py ~/tth/spring15/sync/ttjets_1.root > ~/tth/spring15/sync/ttjets_1/lumilist.json 
	python $(CMSSW_BASE)/src/TTH/MEAnalysis/python/splitLumi.py ~/tth/spring15/sync/ttjets_1/lumilist.json ~/tth/spring15/sync/ttjets_1/
	ls ~/tth/spring15/sync/ttjets_1/block*.json | $(PARCMD) -j40 cmsRun $(CMSSW_BASE)/src/TTH/TTHNtupleAnalyzer/python/pickEvents2_cfg.py inputFiles=file://$(HOME)/tth/spring15/sync/ttjets_1.root lumifile={} outputFile=~/tth/spring15/sync/ttjets_1/block_{#}.root 
	
	mkdir -p ~/tth/spring15/sync/tth/
	edmLumisInFiles.py ~/tth/spring15/sync/tth.root > ~/tth/spring15/sync/tth/lumilist.json 
	python $(CMSSW_BASE)/src/TTH/MEAnalysis/python/splitLumi.py ~/tth/spring15/sync/tth/lumilist.json ~/tth/spring15/sync/tth/
	ls ~/tth/spring15/sync/tth/block*.json | $(PARCMD) -j40 cmsRun $(CMSSW_BASE)/src/TTH/TTHNtupleAnalyzer/python/pickEvents2_cfg.py inputFiles=file://$(HOME)/tth/spring15/sync/tth.root lumifile={} outputFile=~/tth/spring15/sync/tth/block_{#}.root 

step2:
	cd $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test && ls  ~/tth/spring15/sync/tth/block_*.root | $(PARCMD) --result out_tth_step2 -j30 python ./vhbb_parallel.py {} tth_block_{#}
	cd $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test && ls  ~/tth/spring15/sync/ttjets_1/block*.root | $(PARCMD) --result out_ttjets_step2 -j30 python ./vhbb_parallel.py {} ttjets_block_{#}

step3:
	hadd -f ~/tth/spring15/sync/tthbb/ttjets.root ~/tth/gc/GC4635dcd58fdc/cfg_noME/ttjets/output_*.root
	hadd -f ~/tth/spring15/sync/tthbb/tth.root ~/tth/gc/GC4635dcd58fdc/cfg_noME/ttH/output_*.root

step4:
	python python/makeTable.py /home/joosep/tth/spring15/sync/tthbb/tth.root nominal > tth.csv
	python python/makeTable.py /home/joosep/tth/spring15/sync/tthbb/ttjets.root nominal > ttjets.csv

clean:
	rm -Rf $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/Loop_*
