#!/bin/bash

# Get private environment variables
echo "Reading env.sh:"
cat env.sh
source env.sh
echo "Done reading env.sh:"
source common.sh

#print out the environment
env
set -e

#go to work directory
cd $MY_SCRATCH

# Name of the local (ie under MYSCRATCH) place to put the datacard and the output
# Extract "out" from
# "$CMSSW_BASE/src/TTH/Plotting/python/Datacards/out"
export SCRATCH_DCARDDIR=$(basename ${datacarddir})

# get the datacards/root files we need as input
cp -r ${datacarddir} $SCRATCH_DCARDDIR

echo "Running MakeLimits"
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeLimits.py ${CMSSW_BASE}/${analysis_spec} $groups 
echo "Done MakeLimits"

#copy output
OUTDIR=$HOME/tth/makelimits/${TASK_ID}/${MY_JOBID}/
mkdir -p $OUTDIR 
echo "copying output"
cp $SCRATCH_DCARDDIR/higgsCombine*.root $OUTDIR 
cp $SCRATCH_DCARDDIR/out*.log $OUTDIR 



