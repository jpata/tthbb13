#!/bin/bash

source common.sh

#go to work directory
cd $GC_SCRATCH

python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/projectSkim.py skim.root $FILE_NAMES
mv skim.root out.root
