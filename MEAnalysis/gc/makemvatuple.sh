#!/bin/bash

source common.sh
cd $GC_SCRATCH

# Run MakeTaggingNtuple
echo "Running MakeTaggingNtuple"
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/MakeTaggingNtuple.py out.root
echo "Done MakeTaggingNtuple"




