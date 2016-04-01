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

echo "Running MakeCategory"
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeCategory.py $sparse_histo_file ${CMSSW_BASE}/${analysis_spec} $category
echo "Done MakeCategory"

xbase=${analysis_spec##*/}
anspec_base=${xbase%.*}
echo "anspec_base", $anspec_base
#copy output
OUTDIR=$HOME/tth/gc/makecategory/${TASK_ID}/${anspec_base}/
mkdir -p $OUTDIR 
echo "copying output"
cp out/* $OUTDIR 




