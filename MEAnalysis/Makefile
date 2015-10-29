PARCMD=~/parallel --gnu

.PHONY: clean

pick:
	edmCopyPickMerge inputFiles=file:///home/joosep/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/141B9915-1F08-E511-B9FF-001E675A6AB3.root outputFile=picked.root eventsToProcess=1:12701:2532028,1:8271:1648889,1:6588:1313413

download:
	mkdir -p ~/tth/spring15/sync/ttjets/
	xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIISpring15MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/40000/00087FEB-236E-E511-9ACB-003048FF86CA.root ~/tth/spring15/sync/ttjets.root
	#mkdir -p ~/tth/spring15/sync/ttH/
	#xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIISpring15DR74/ttHTobb_M125_13TeV_powheg_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/141B9915-1F08-E511-B9FF-001E675A6AB3.root ~/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/141B9915-1F08-E511-B9FF-001E675A6AB3.root


split:
	edmLumisInFiles.py ~/tth/spring15/sync/ttjets.root > ~/tth/spring15/sync/ttjets/lumilist.json 
	python $(CMSSW_BASE)/src/TTH/MEAnalysis/python/splitLumi.py ~/tth/spring15/sync/ttjets/lumilist.json ~/tth/spring15/sync/ttjets/
	ls ~/tth/spring15/sync/ttjets/block*.json | $(PARCMD) -j24 cmsRun $(CMSSW_BASE)/src/TTH/TTHNtupleAnalyzer/python/pickEvents2_cfg.py inputFiles=file://$(HOME)/tth/spring15/sync/ttjets.root lumifile={} outputFile=~/tth/spring15/sync/ttjets/block_{#}.root 
	
	#edmLumisInFiles.py ~/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/141B9915-1F08-E511-B9FF-001E675A6AB3.root > ~/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/lumilist.json
	#python $(CMSSW_BASE)/src/TTH/MEAnalysis/python/splitLumi.py ~/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/lumilist.json ~/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/
	#ls ~/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/block*.json | $(PARCMD) -j24 cmsRun $(CMSSW_BASE)/src/TTH/TTHNtupleAnalyzer/python/pickEvents2_cfg.py inputFiles=file://$(HOME)/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/141B9915-1F08-E511-B9FF-001E675A6AB3.root lumifile={} outputFile=~/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/block_{#}.root 

step2:
	#cd $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test && ls  ~/tth/spring15/sync/ttHTobb_M125_13TeV_powheg_pythia8__Asympt25ns_MCRUN2_74_V9-v1/block*.root | $(PARCMD) --result out_step2 -j30 python ./vhbb_parallel.py {} tth_{#}
	cd $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test && ls  ~/tth/spring15/sync/ttjets/block*.root | $(PARCMD) --result out_ttjets_step2 -j30 python ./vhbb_parallel.py {} ttjets_block{#}

step3:
	seq 0 75 | $(PARCMD) -j30 ./python/MEAnalysis_heppy_parallel.py {}

step4:
	python python/makeTable.py tth.root nominal > tth.csv
	python python/makeTable.py ttjets.root nominal > ttjets.csv
	#python python/makeTable.py tth.root raw > tth_raw.csv
	#python python/makeTable.py tth.root JESUp > tth_JESUp.csv
	#python python/makeTable.py tth.root JESDown > tth_JESDown.csv
	#python python/makeTable.py ttjets.root JESUp > ttjets_JESUp.csv
	#python python/makeTable.py ttjets.root JESDown > ttjets_JESDown.csv

clean:
	rm -Rf $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/Loop_*
