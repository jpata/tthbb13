#!/bin/bash
eval `scramv1 runtime -sh` 
source /cvmfs/cms.cern.ch/crab3/crab.sh
#voms-proxy-init -voms cms
while read i; do
  export DATASET=`echo $i | cut -f1 -d' '`
  export NLUMIS=`echo $i | cut -f2 -d' '`
  python heppy_crab_config_env.py > cfg_`echo $DATASET | cut -f2 -d'/'`.py
  #crab submit -c heppy_crab_config_env.py
done
