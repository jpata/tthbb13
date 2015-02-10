#!/bin/sh
set -e
echo "running TTH/TTHNtupleAnalyzer runtests.sh " $LOCAL_TEST_DIR

echo "ttbar_cfg.py"
cmsRun $LOCAL_TEST_DIR/ttbar_cfg.py &

echo "tthbb.py"
cmsRun $LOCAL_TEST_DIR/tthbb_cfg.py &

echo "tthtautau.py"
cmsRun $LOCAL_TEST_DIR/tthtautau_cfg.py &

wait
#rm $CMSSW_BASE/ntuple.root
exit 0
