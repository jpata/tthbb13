#!/bin/bash

#on PSI, CMSSW_BASE is not exported with the grid job, need to set manually
CMSSW_BASE=$HOME/TTH-72X-heppy/CMSSW/

env
set -e

pwd
ls -al

#set env
cd ${CMSSW_BASE}/src/TTH/MEAnalysis/
export SCRAM_ARCH="slc6_amd64_gcc481"
source /cvmfs/cms.cern.ch/cmsset_default.sh

#uncomment these to test the script
#these are all the input parameters that MEAnalysis_heppy_gc.py reads
#export SKIP_EVENTS=0
#export MAX_EVENTS=100
#export DATASETNICK=tth_13tev
#export DATASETPATH=tth_13tev
#export FILE_NAMES=/store/user/jpata/VHBBHeppyV10/TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola/VHBB_HEPPY_V10_TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola__Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/150302_164515/0000/tree_1.root
#export MY_SCRATCH=./

eval `scramv1 runtime -sh`

#make sure we have the correct custom python environment
source $CMSSW_BASE/src/TTH/setenv.sh
#export PYTHONPATH=$CMSSW_BASE/anaconda/lib/python2.7/site-packages:$PYTHONPATH
#export LD_LIBRARY_PATH=$CMSSW_BASE/anaconda/lib/:$LD_LIBRARY_PATH
#export PATH=$CMSSW_BASE/anaconda/bin/:$PATH

cd $MY_SCRATCH

$CMSSW_BASE/anaconda/bin/python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py
echo "MEAnalysis is done"

OUTDIR=$HOME/tth/gc/${TASK_ID}/${DATASETPATH}/
mkdir -p $OUTDIR 
echo "copying output"
OFNAME=$OUTDIR/output_${MY_JOBID}.root
cp $MY_SCRATCH/Loop/tree.root $OFNAME
echo $OFNAME > output.txt
