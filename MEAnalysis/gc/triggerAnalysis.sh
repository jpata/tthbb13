#!/bin/bash
source common.sh
cd $GC_SCRATCH
python ${CMSSW_BASE}/src/VHbbAnalysis/Heppy/test/triggerAnalysis/mc_emulation.py
