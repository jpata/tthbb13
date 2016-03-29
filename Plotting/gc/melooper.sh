#!/bin/bash

source env.sh 
source common.sh

#go to work directory
cd $MY_SCRATCH

python ${CMSSW_BASE}/src/TTH/Plotting/python/makeJobfile.py
${CMSSW_BASE}/src/TTH/Plotting/melooper job.json

OUTDIR=$HOME/tth/gc/melooper/${TASK_ID}/${DATASETPATH}/
mkdir -p $OUTDIR 
OFNAME=$OUTDIR/output_${MY_JOBID}.root
cp ControlPlotsSparse.root $OFNAME
