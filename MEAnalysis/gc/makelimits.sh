#!/bin/bash

source common.sh

#go to work directory
cd $MY_SCRATCH

# Name of the local (ie under MYSCRATCH) place to put the datacard and the output
# Extract "out" from
# "$CMSSW_BASE/src/TTH/Plotting/python/Datacards/out"
export SCRATCH_DCARDDIR=$(basename ${datacarddir})

echo "MY_SCRATCH=$MY_SCRATCH"

echo `pwd`
echo "SCRATCH_DCARDDIR="$SCRATCH_DCARDDIR
# get the datacards/root files we need as input
cp -r ${datacarddir} $SCRATCH_DCARDDIR
cd $SCRATCH_DCARDDIR

echo "Running MakeLimits"
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeLimits.py ${CMSSW_BASE}/${analysis_spec} $groups 
echo "Done MakeLimits"
cd ../

xbase=${analysis_spec##*/}
anspec_base=${xbase%.*}

#copy output
OUTDIR=$HOME/tth/gc/makelimits/${TASK_ID}/${anspec_base}/${MY_JOBID}/
mkdir -p $OUTDIR 
echo "copying output"
cp $SCRATCH_DCARDDIR/higgsCombine*.root $OUTDIR 
cp $SCRATCH_DCARDDIR/out*.log $OUTDIR 



