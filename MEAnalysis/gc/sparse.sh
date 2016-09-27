#!/bin/bash
source common.sh
cd $GC_SCRATCH
#in case of FileBasedSplitter, need to override MAX_EVENTS
export MAX_EVENTS=999999999999
export SKIP_EVENTS=0
ANALYSIS_CONFIG=${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/config_sldl.cfg python ${CMSSW_BASE}/src/TTH/Plotting/python/joosep/sparsinator.py
