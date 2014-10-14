
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


#7_2 stuff
INFS=inputFiles=/store/relval/CMSSW_7_2_0_pre7/RelValTTbar_13/MINIAODSIM/PU25ns_PRE_LS172_V11-v1/00000/0EE5E9F5-344E-E411-BC87-003048FFD720.root,/store/relval/CMSSW_7_2_0_pre7/RelValTTbar_13/MINIAODSIM/PU25ns_PRE_LS172_V11-v1/00000/5ED3A519-354E-E411-900E-0025905A60A6.root

run_toptagger_1:
	cmsRun TTHNtupleAnalyzer/python/toptagger/default.py $(INFS) outputFile=toptagger_default.root

run_toptagger_2:
	cmsRun TTHNtupleAnalyzer/python/toptagger/loose.py $(INFS) outputFile=toptagger_loose.root
