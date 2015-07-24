#!/bin/bash

#on PSI, CMSSW_BASE is not exported with the grid job, need to set manually
#CMSSW_BASE=$HOME/TTH-72X-heppy/CMSSW/
CMSSW_BASE=/shome/tklijnsm/ME-heppy/TTH2/CMSSW/

env
set -e

pwd
ls -al


#export DATASETPATH="V11_tth_13tev"


#set env
cd ${CMSSW_BASE}/src/TTH/MEAnalysis/
export SCRAM_ARCH="slc6_amd64_gcc481"
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd $MY_SCRATCH


echo $DATASETPATH

python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py
echo "MEAnalysis is done"

OUTDIR=$HOME/tth/gc/${TASK_ID}/${DATASETPATH}/
mkdir -p $OUTDIR 
echo "copying output"
OFNAME=$OUTDIR/output_${MY_JOBID}.root
cp $MY_SCRATCH/Loop/tree.root $OFNAME
echo $OFNAME > output.txt
#echo "testtext" > test.txt
