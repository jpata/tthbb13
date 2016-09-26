#!/bin/bash

source common.sh

# Go to work directory
cd $GC_SCRATCH

# Get some extra stuff
cp ${CMSSW_BASE}/src/TTH/MEAnalysis/python/AccessHelpers.py .
cp ${CMSSW_BASE}/src/TTH/Plotting/python/TransferFunctions/runs/$dsversion"_"$jettype/cfg_outputtree.dat .
export PYTHONPATH=.:$PYTHONPATH

echo "Preparing to run outputtree-strict.py"

python ${CMSSW_BASE}/src/TTH/Plotting/python/TransferFunctions/outputtree-strict.py

