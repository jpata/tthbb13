#!/bin/bash

source common.sh

# Go to work directory
cd $MY_SCRATCH

# Get some extra stuff
cp ${CMSSW_BASE}/src/TTH/TTHNtupleAnalyzer/python/AccessHelpers.py .
cp ${CMSSW_BASE}/src/TTH/Plotting/python/TransferFunctions/runs/@runconf@/cfg_outputtree.dat .
export PYTHONPATH=.:$PYTHONPATH

# And run
echo "Preparing to run outputtree-strict.py"
python ${CMSSW_BASE}/src/TTH/Plotting/python/TransferFunctions/outputtree-strict.py
echo "outputtree-strict.py is Done"

# Copy output
OUTDIR=$HOME/tth/gc/makeTF/${TASK_ID}/@runconf@/
mkdir -p $OUTDIR 
echo "copying output"
OFNAME=$OUTDIR/output_${MY_JOBID}.root
cp $MY_SCRATCH/out.root $OFNAME
echo $OFNAME > output.txt

