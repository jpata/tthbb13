#!/bin/bash

#uncomment these to test the script
#these are all the input parameters that MEAnalysis_heppy_gc.py reads
#export SKIP_EVENTS=0
#export MAX_EVENTS=10000
#export DATASETPATH=ttHTobb_M125_13TeV_powheg_pythia8
#export FILE_NAMES=/store/user/jpata/VHBBHeppyV16pre/ttHTobb_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V16pre_ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151117_175129/0000/tree_1.root
#export MY_SCRATCH=./

#on PSI, CMSSW_BASE is not exported with the grid job, need to set manually
CMSSW_BASE=$HOME/VHBB-763/CMSSW_7_6_3/

#here we use @...@ to give grid-control the possibility to substitute the configuration file name
#export ME_CONF=$CMSSW_BASE/src/TTH/MEAnalysis/python/cfg_withME.py
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
source ${CMSSW_BASE}/src/TTH/setenv_psi.sh
#source ${CMSSW_BASE}/src/TTH/setenv_kbfi.sh

# Only use one core
export OMP_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export MKL_NUM_THREADS=1

#go to work directory
cd $MY_SCRATCH

# avoid lock-issues 
export THEANO_FLAGS="base_compiledir=."

xrdcp  root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/gregor/ttHTobb_M125_13TeV_powheg_pythia8.root ttHTobb_M125_13TeV_powheg_pythia8.root

echo "Run TrainClassifiers"
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/TrainClassifiers_topevent.py
echo "Done TrainClassifiers"

#copy output
ME_CONF_NAME=$(basename "$ME_CONF")
OUTDIR=$HOME/tth/gc/${TASK_ID}/${MY_JOBID}/
mkdir -p $OUTDIR 
echo "copying output"

cp $MY_SCRATCH/*.png $OUTDIR 
cp $MY_SCRATCH/valacc.txt $OUTDIR 
cp $MY_SCRATCH/maxvalacc.txt $OUTDIR 
cp $MY_SCRATCH/deltaacc.txt $OUTDIR 
cp $MY_SCRATCH/*.yaml $OUTDIR 
cp $MY_SCRATCH/*.h5 $OUTDIR 
env > $OUTDIR/env.txt


