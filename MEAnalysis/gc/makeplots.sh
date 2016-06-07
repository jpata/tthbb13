#!/bin/bash

source common.sh
cd $GC_SCRATCH

# Run Plotting
echo "Running plotting"
python ${CMSSW_BASE}/src/TTH/Plotting/python/gregor/BoostControlPlots.py 
python ${CMSSW_BASE}/src/TTH/Plotting/python/joosep/ObjectSync.py
echo "Done plotting"




