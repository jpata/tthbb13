#!/bin/bash

source common.sh
#go to work directory
cd $GC_SCRATCH

ANALYSIS_CONFIG=${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/config_sldl.cfg python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/dumpCommonClassifier.py
