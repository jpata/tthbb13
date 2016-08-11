#!/bin/bash

source common.sh

#go to work directory
cd $GC_SCRATCH

# Create output directory
mkdir out

echo "Running MakeCategory" $sparsefile $specfile $analysis $category
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeCategory.py --anspec=$specfile --analysis=$analysis --category=$category --outdir="."
echo "Done MakeCategory"
