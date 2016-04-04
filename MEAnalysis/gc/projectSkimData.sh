#!/bin/bash

source common.sh

#go to work directory
cd $MY_SCRATCH

OUTDIR=$HOME/tth/gc/projectSkim/${TASK_ID}/${DATASETPATH}/
mkdir -p $OUTDIR
OFNAME=$OUTDIR/output_${MY_JOBID}.root
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/projectSkim.py skim.root $FILE_NAMES
cp skim.root $OFNAME
