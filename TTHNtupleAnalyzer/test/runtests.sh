#!/bin/sh
echo "TTH/TTHNtupleAnalyzer runtests.sh " $LOCAL_TEST_DIR
cmsRun $LOCAL_TEST_DIR/ttbar_cfg.py 
python $LOCAL_TEST_DIR/../python/produce_dqm.py $CMSSW_BASE/output.root $LOCAL_TEST_DIR/dqm.root
compare_using_files.py $LOCAL_TEST_DIR/../root/dqm/785da0.root $LOCAL_TEST_DIR/dqm.root -C -R --meta "v1 @@@ v2" -o $LOCAL_TEST_DIR/dqmreport
python $LOCAL_TEST_DIR/ttbar_test.py $CMSSW_BASE/output.root
#rm $CMSSW_BASE/ntuple.root
exit 0
