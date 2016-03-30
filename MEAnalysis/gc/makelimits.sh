#!/bin/bash

# Get private environment variables
echo "Reading env.sh:"
cat env.sh
source env.sh
echo "Done reading env.sh:"
source common.sh

#on PSI, CMSSW_BASE is not exported with the grid job, need to set manually
CMSSW_BASE=$HOME/VHBB-763/CMSSW_7_6_3/

#print out the environment
env
set -e

#go to work directory
cd $MY_SCRATCH

# Name of the local (ie under MYSCRATCH) place to put the datacard and the output
# Extract "out" from
# "$CMSSW_BASE/src/TTH/Plotting/python/Datacards/out"
export SCRATCH_DCARDDIR=$(basename ${CMSSW_BASE}/${datacarddir})

# get the datacards/root files we need as input
cp -r ${CMSSW_BASE}/${datacarddir} $SCRATCH_DCARDDIR

echo "Running MakeLimits"
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeLimits.py ${CMSSW_BASE}/${analysis_spec} $groups 
echo "Done MakeLimits"

#copy output
OUTDIR=$HOME/tth/gc/${TASK_ID}/${MY_JOBID}/
mkdir -p $OUTDIR 
echo "copying output"
cp $SCRATCH_DCARDDIR/higgsCombine*.root $OUTDIR 
cp $SCRATCH_DCARDDIR/out*.log $OUTDIR 



