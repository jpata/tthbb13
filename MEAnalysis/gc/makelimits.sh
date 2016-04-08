#!/bin/bash

# Setup
echo "Reading env.sh:"
cat env.sh
source env.sh
echo "Done reading env.sh:"
source common.sh
cd $MY_SCRATCH

# get the datacards/root files we need as input
cp ${datacardbase}/${analysis}/*.root .
cp ${datacardbase}/${analysis}/*.txt .

# Run MakeLimits
echo "Running MakeLimits"
echo ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeLimits.py $specfile . $analysis $group
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeLimits.py $specfile . $analysis $group
echo "Done MakeLimits"

#copy output
OUTDIR=$HOME/tth/gc/makelimits/${TASK_ID}/${analysis}/
mkdir -p $OUTDIR 
echo "copying output"
cp higgsCombine*.root $OUTDIR 
cp out*.log $OUTDIR 



