#!/bin/bash

source common.sh
cd $GC_SCRATCH
python ${CMSSW_BASE}/src/TTH/MEIntegratorStandalone/test/test_json.py > out.txt
