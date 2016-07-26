#!/bin/bash

source common.sh
cd $GC_SCRATCH
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/memonly.py
