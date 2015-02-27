#!/bin/bash

#CMSSW_BASE=/shome/jpata/TTH/CMSSW
CMSSW_BASE=/home/joosep/TTH-73X/CMSSW

source config.sh

env
set -e

pwd
ls -al

#set env
cd ${CMSSW_BASE}/src/TTH/MEAnalysis/
export SCRAM_ARCH="slc6_amd64_gcc491"
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`

#make local cfg file in scratch
cd $MY_SCRATCH
python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_gc.py

#run MEAnalysis from main directory
cd ${CMSSW_BASE}/src/TTH/MEAnalysis/
time MEAnalysis $MY_SCRATCH/MEAnalysis_cfg.py
echo "MEAnalysis is done"

#back to scratch to copy output
cd $MY_SCRATCH
OFPATH=/home/$USER/tth/gc/${TASK_ID}/${DATACARD}/${DATASETPATH}/
mkdir -p $OFPATH
echo "copying output to $OFPATH/$OFNAME"
OFNAME=output_${MY_JOBID}.root
cp $MY_SCRATCH/output.root $OFPATH/$OFNAME
echo $OFPATH/$OFNAME > output.txt
