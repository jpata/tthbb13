#!/bin/bash

source common.sh
#export DATASETPATH=ttHTobb_M125_13TeV_powheg_pythia8

#go to work directory
cd $GC_SCRATCH

python ${CMSSW_BASE}/src/TTH/GenLevel/python/genLevelAnalysis_cms.py
mv Loop/tree.root tree.root
