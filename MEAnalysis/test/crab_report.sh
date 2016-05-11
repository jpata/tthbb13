#!/bin/bash
eval `scramv1 runtime -sh`
source /cvmfs/cms.cern.ch/crab3/crab.sh
fn=`mktemp`
echo $1
crab status --json $1 | grep "{" > $fn
python $CMSSW_BASE/src/TTH/MEAnalysis/python/crab_report.py $fn
rm $fn
