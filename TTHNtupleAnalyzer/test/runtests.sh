#!/bin/sh
echo "TTH/TTHNtupleAnalyzer runtests.sh " $LOCAL_TEST_DIR
cmsRun $LOCAL_TEST_DIR/ttbar_cfg.py 
python $LOCAL_TEST_DIR/ttbar_test.py $CMSSW_BASE/ntuple.root
rm $CMSSW_BASE/ntuple.root
exit 0
