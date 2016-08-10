#!/bin/bash
source common.sh
cd $GC_SCRATCH
python ${CMSSW_BASE}/src/TTH/Plotting/python/joosep/sparsinator.py
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/counts.py count.root $FILE_NAMES
hadd out_count.root out.root count.root
