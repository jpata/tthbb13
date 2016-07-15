#!/bin/bash

source common.sh
#go to work directory
cd $GC_SCRATCH

#python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/MakeTaggingNtuple.py taggingNtuple.root $FILE_NAMES
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/dumpMEEvents.py > out.json
