#!/bin/bash
set -e
source common.sh

#go to work directory
cd $GC_SCRATCH

python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/counts.py count.root $FILE_NAMES
