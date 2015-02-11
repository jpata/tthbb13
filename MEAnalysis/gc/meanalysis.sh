#!/bin/bash

CMSSW_BASE=/shome/jpata/TTH/CMSSW

env
set -e

pwd
ls -al

cd ${CMSSW_BASE}/src/TTH/MEAnalysis/
export SCRAM_ARCH="slc6_amd64_gcc491"
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
time MEAnalysis gc/MEAnalysis_gc.py
echo "MEAnalysis is done"

mkdir -p ~/tth/gc/${TASK_ID}/${DATASETNICK}/
echo "copying output"
cp $MY_SCRATCH/output.root ~/tth/gc/${TASK_ID}/${DATASETNICK}/output_${MY_JOBID}.root
