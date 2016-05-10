#!/bin/bash

source common.sh
cd $GC_SCRATCH

# get the datacards/root files we need as input
cp ${datacardbase}/${analysis}/*.root .
cp ${datacardbase}/${analysis}/*.txt .

# Run MakeLimits
echo "Running MakeLimits"
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeLimits.py $specfile . $analysis $group
echo "Done MakeLimits"

ls -l .
