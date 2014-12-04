#!/bin/sh
set -e
echo "TTH/TTHNtupleAnalyzer runtests.sh " $LOCAL_TEST_DIR
cmsRun $LOCAL_TEST_DIR/ttbar_cfg.py 
cmsRun $LOCAL_TEST_DIR/tthbb_cfg.py 
#rm $CMSSW_BASE/ntuple.root
exit 0
