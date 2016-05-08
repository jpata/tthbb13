#!/bin/bash
set -e
source common.sh

#go to work directory
cd $GC_SCRATCH

#OUTDIR=$HOME/tth/gc/count/${GC_TASK_ID}/${DATASETPATH}/
OUTDIR=$HOME/TTH_2016/TTH_76X_v1/count/${GC_TASK_ID}/${DATASETPATH}/
mkdir -p $OUTDIR
OFNAME=$OUTDIR/output_${MY_JOBID}.root
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/counts.py count.root $FILE_NAMES
cp count.root $OFNAME
