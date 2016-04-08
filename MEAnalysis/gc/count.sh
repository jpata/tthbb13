#!/bin/bash
set -e
source common.sh

#go to work directory
cd $MY_SCRATCH

OUTDIR=$HOME/tth/gc/count/${TASK_ID}/${DATASETPATH}/
mkdir -p $OUTDIR
OFNAME=$OUTDIR/output_${MY_JOBID}.root
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/counts.py count.root $FILE_NAMES
cp count.root $OFNAME
