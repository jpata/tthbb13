#!/bin/bash

#uncomment these to test the script
#these are all the input parameters that MEAnalysis_heppy_gc.py reads
#export SKIP_EVENTS=0
#export MAX_EVENTS=200
#export DATASETPATH=ttHTobb_M125_13TeV_powheg_pythia8
#export FILE_NAMES=/store/user/jpata/VHBBHeppyV20/ttHTobb_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V20_ttHTobb_M125_13TeV_powheg_Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160209_170826/0000/tree_1.root
#export MY_SCRATCH=./

SITE="UNKNOWN"
hnamestr=`hostname`
if [[ "$hnamestr" == t3* ]]; then
    export SITE="PSI"
elif [[ "$hnamestr" == comp* ]]; then
    export SITE="TALLINN"
fi

#on PSI, CMSSW_BASE is not exported with the grid job, need to set manually
if [[ "$SITE" == "PSI" ]]; then
    export CMSSW_BASE=$HOME/tth/sw-76/CMSSW/
fi;

#here we use @...@ to give grid-control the possibility to substitute the configuration file name
#comment this line when testing locally
#export ME_CONF=$CMSSW_BASE/src/TTH/MEAnalysis/python/cfg_withME.py
export ME_CONF=$CMSSW_BASE/src/TTH/MEAnalysis/python/@me_conf@

#print out the environment
env
set -e

pwd
ls -al

#set env
cd ${CMSSW_BASE}/src/TTH/MEAnalysis/
export SCRAM_ARCH="slc6_amd64_gcc491"
source /cvmfs/cms.cern.ch/cmsset_default.sh
#eval `scramv1 runtime -sh`
if [[ "$SITE" == "PSI" ]]; then
    source ${CMSSW_BASE}/src/TTH/setenv_psi.sh
elif [[ "$SITE" == "TALLINN" ]]; then
    source ${CMSSW_BASE}/src/TTH/setenv_kbfi.sh
fi

#go to work directory
cd $MY_SCRATCH

python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py
echo "MEAnalysis is done"

#copy output
ME_CONF_NAME=$(basename "$ME_CONF")
OUTDIR=$HOME/tth/gc/${TASK_ID}/${ME_CONF_NAME%.*}/${DATASETPATH}/
mkdir -p $OUTDIR 
echo "copying output"
OFNAME=$OUTDIR/output_${MY_JOBID}.root
cp $MY_SCRATCH/Loop/tree.root $OFNAME
echo $OFNAME > output.txt
