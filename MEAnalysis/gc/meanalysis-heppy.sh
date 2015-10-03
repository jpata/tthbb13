#!/bin/bash

#uncomment these to test the script
#these are all the input parameters that MEAnalysis_heppy_gc.py reads
export SKIP_EVENTS=0
export MAX_EVENTS=100
export DATASETPATH=TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2
export FILE_NAMES=/store/t3groups/ethz-higgs/run2/VHBBHeppyV13/TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBB_HEPPY_V13_TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/151002_060618/0000/tree_172.root
export MY_SCRATCH=./


#on PSI, CMSSW_BASE is not exported with the grid job, need to set manually
CMSSW_BASE=$HOME/tth/sw/CMSSW/

#here we use @...@ to give grid-control the possibility to substitute the configuration file name
export ME_CONF=$CMSSW_BASE/src/TTH/MEAnalysis/python/MEAnalysis_cfg_heppy.py
#export ME_CONF=$CMSSW_BASE/src/TTH/MEAnalysis/python/@me_conf@

#print out the environment
env
set -e

pwd
ls -al

#set env
cd ${CMSSW_BASE}/src/TTH/MEAnalysis/
export SCRAM_ARCH="slc6_amd64_gcc491"
source /cvmfs/cms.cern.ch/cmsset_default.sh

#call cmsenv
eval `scramv1 runtime -sh`

#make sure we have the correct custom python environment
export PYTHONPATH=~joosep/anaconda/lib/python2.7/site-packages:$PYTHONPATH
export LD_LIBRARY_PATH=~joosep/anaconda/lib/:$LD_LIBRARY_PATH
export PATH=~joosep/anaconda/bin/:$PATH

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
