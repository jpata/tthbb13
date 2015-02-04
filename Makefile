
STEP1_CFG=$(CMSSW_BASE)/python/TTH/TTHNtupleAnalyzer/Main_cfg.py

compile:
	cd $(CMSSW_BASE); scram b -j16

test:
	cd $(CMSSW_BASE); scram b TTH/TTHNtuplAnalyzer runtests

debug:
	cd $(CMSSW_BASE); scram b -j16 USER_CXXFLAGS="-DEDM_ML_DEBUG"

run_debug:
	cmsRun $(STEP1_CFG)

run_step1_tthbb:
	cmsRun $(STEP1_CFG) inputFiles=/store/mc/Spring14miniaod/TTbarH_HToBB_M-125_13TeV_pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/0E97DD3E-2209-E411-8A04-003048945312.root outputFile=tthbb_step1.root maxEvents=10000

run_step1_ttbar:
	cmsRun $(STEP1_CFG) inputFiles=/store/results/top/StoreResults/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/USER/Spring14dr_PU_S14_POSTLS170_V6AN1_miniAOD706p1_814812ec83fce2f620905d2bb30e9100-v2/00000/0012F41F-FA17-E411-A1FF-0025905A48B2.root outputFile=ttbar_step1.root maxEvents=10000

step1_test: run_step1_tthbb run_step1_ttbar

headers:
	python $(CMSSW_BASE)/src/TTH/TTHNtupleAnalyzer/python/headergen.py $(CMSSW_BASE)/src/TTH/MEAnalysis/interface/METree_template.hh $(CMSSW_BASE)/src/TTH/MEAnalysis/interface/METree.hh $(CMSSW_BASE)/src/TTH/MEAnalysis/python/branches.py


cutflow_step2:
	cutflow_step2 $(CMSSW_BASE)/src/TTH/Plotting/python/joosep/cutflow_step2_EE.py
