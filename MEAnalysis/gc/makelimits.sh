#!/bin/bash

source common.sh
cd $GC_SCRATCH

# get the datacards/root files we need as input
cp ${datacardbase}/${analysis}/*.root .
cp ${datacardbase}/${analysis}/*.txt .

# Run MakeLimits
echo "Running MakeLimits"
echo ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeLimits.py $specfile . $analysis $group
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeLimits.py $specfile . $analysis $group
echo "Done MakeLimits"

ls -l .
cp higgsCombine*.root $OUTDIR 
cp out*.log $OUTDIR 



