#!/bin/bash
STEP1_CFG=$CMSSW_BASE/python/TTH/TTHNtupleAnalyzer/Main_cfg.py
HASH=`git rev-parse --short HEAD`
DQM_OUT_DIR=$CMSSW_BASE/src/TTH/TTHNtupleAnalyzer/dqm/$HASH

REFERENCE=044c911

mkdir -p $DQM_OUT_DIR
cmsRun $STEP1_CFG inputFiles=/store/mc/Spring14miniaod/TTbarH_HToBB_M-125_13TeV_pythia6/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/0E97DD3E-2209-E411-8A04-003048945312.root outputFile=$DQM_OUT_DIR/tthbb_step1.root maxEvents=1000
$CMSSW_BASE/src/TTH/TTHNtupleAnalyzer/python/produce_dqm.py $DQM_OUT_DIR/tthbb_step1_numEvent1000.root $DQM_OUT_DIR/tthbb.root

cmsRun $STEP1_CFG inputFiles=/store/mc/Spring14miniaod/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_POSTLS170_V5-v2/00000/004C6DA7-FB03-E411-96BD-0025905A497A.root outputFile=$DQM_OUT_DIR/ttjets_step1.root maxEvents=1000
$CMSSW_BASE/src/TTH/TTHNtupleAnalyzer/python/produce_dqm.py $DQM_OUT_DIR/ttjets_step1_numEvent1000.root $DQM_OUT_DIR/ttjets.root

cd $DQM_OUT_DIR
mkdir -p reports/tthbb
mkdir -p reports/ttjets

compare_using_files.py $DQM_OUT_DIR/../$REFERENCE/tthbb.root $DQM_OUT_DIR/tthbb.root --meta "ref_$REFERENCE @@@ $HASH" -R -C -o $DQM_OUT_DIR/reports/tthbb
compare_using_files.py $DQM_OUT_DIR/../$REFERENCE/ttjets.root $DQM_OUT_DIR/ttjets.root --meta "ref_$REFERENCE @@@ $HASH" -R -C -o $DQM_OUT_DIR/reports/ttjets
