#!/bin/bash

source env.sh 
source common.sh

#go to work directory
cd $GC_SCRATCH

python ${CMSSW_BASE}/src/TTH/Plotting/python/makeJobfile.py
${CMSSW_BASE}/src/TTH/Plotting/melooper job.json
