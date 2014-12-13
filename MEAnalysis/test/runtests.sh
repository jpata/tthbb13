#!/bin/sh
set -e
echo "TTH/MEAnalysis runtests.sh " $LOCAL_TEST_DIR
cd $CMSSW_BASE/src/TTH/MEAnalysis
$CMSSW_BASE/bin/$SCRAM_ARCH/MEAnalysis test/me_tthbb.py
$CMSSW_BASE/bin/$SCRAM_ARCH/MEAnalysis test/me_ttbar.py
exit 0
