#!/bin/sh
echo "TTH/TTHNtupleAnalyzer runtests.sh " $LOCAL_TEST_DIR
cmsRun $LOCAL_TEST_DIR/ttbar_cfg.py 
exit 0
