#!/bin/bash

source common.sh
#export DATASETPATH=ttHTobb_M125_13TeV_powheg_pythia8
#export FILE_NAMES=/store/user/jpata/VHBBHeppyV20/ttHTobb_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V20_ttHTobb_M125_13TeV_powheg_Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160209_170826/0000/tree_1.root

#go to work directory
cd $MY_SCRATCH

OUTDIR=$HOME/tth/gc/projectSkim/${TASK_ID}/${DATASETPATH}/
mkdir -p $OUTDIR
OFNAME=$OUTDIR/output_${MY_JOBID}.root
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/projectSkim.py out.root $FILE_NAMES
cp out.root $OFNAME
