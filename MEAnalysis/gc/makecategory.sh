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

# Create output directory
mkdir out

# get the sparse histograms
cp  $sparse_histo_file sparse.root

echo "Running MakeCategory"
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeCategory.py sparse.root ${CMSSW_BASE}/${analysis_spec} $category
echo "Done MakeCategory"

#copy output
OUTDIR=$HOME/tth/gc/${TASK_ID}/out/
mkdir -p $OUTDIR 
echo "copying output"
cp out/* $OUTDIR 




