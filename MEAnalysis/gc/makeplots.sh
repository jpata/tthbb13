#!/bin/bash

source common.sh
cd $GC_SCRATCH

# Run Plotting
echo "Running plotting"
python ${CMSSW_BASE}/src/TTH/Plotting/python/gregor/HiggsMasses.py 
echo "Done plotting"




