#!/bin/sh
set -e
echo "TTH/MEAnalysis runtests.sh " $LOCAL_TEST_DIR
cd $CMSSW_BASE/src/TTH/MEAnalysis
$CMSSW_BASE/bin/$SCRAM_ARCH/MEAnalysis test/me_test_cfg.py
exit 0
