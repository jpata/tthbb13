#!/bin/bash

source common.sh
cd $GC_SCRATCH

# Run Plotting
echo "Running plotting"
#python ${CMSSW_BASE}/src/TTH/Plotting/python/gregor/HiggsMasses.py 
python ${CMSSW_BASE}/src/TTH/Plotting/python/joosep/ObjectSync.py --samples ${CMSSW_BASE}/src/TTH/MEAnalysis/test/samples.cfg
echo "Done plotting"




