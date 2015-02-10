#!/bin/bash

env
set -e

pwd
ls -al

cd ${CMSSW_BASE}/src/TTH/MEAnalysis/
export SCRAM_ARCH="slc6_amd64_gcc481"
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
MEAnalysis gc/MEAnalysis_gc.py

mkdir -p ~/tth/gc/${TASK_ID}/${DATASETNICK}/${FILE_NAMES}/
cp $MY_SCRATCH/output.root ~/tth/gc/${TASK_ID}/${DATASETNICK}/${FILE_NAMES}/output_${MY_JOBID}.root