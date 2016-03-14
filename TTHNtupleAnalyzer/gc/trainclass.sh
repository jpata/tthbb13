#!/bin/bash

#on PSI, CMSSW_BASE is not exported with the grid job, need to set manually
CMSSW_BASE=$HOME/TOP-763/CMSSW_7_6_3/

#print out the environment
env
set -e

pwd
ls -al

#set env
cd ${CMSSW_BASE}/src/TTH/TTHNtupleAnalyzer/
export SCRAM_ARCH="slc6_amd64_gcc491"
source /cvmfs/cms.cern.ch/cmsset_default.sh
source ${CMSSW_BASE}/src/TTH/setenv_psi.sh

#go to work directory
cd $MY_SCRATCH

# avoid lock-issues 
export THEANO_FLAGS="base_compiledir=."

# Only use one core
export OMP_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export MKL_NUM_THREADS=1

# Stage in the data
xrdcp root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/gregor/ntop_x1_qcd_800_1000-tagging-weighted.root ntop_x1_qcd_800_1000-tagging-weighted.root  
xrdcp root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/gregor/ntop_x1_zprime_m2000-tagging-weighted.root ntop_x1_zprime_m2000-tagging-weighted.root

# And the pickled results of two BDT trainings for comparison 
cp ${CMSSW_BASE}/src/TTH/TTHNtupleAnalyzer/python/BDT-nob.pickle .
cp ${CMSSW_BASE}/src/TTH/TTHNtupleAnalyzer/python/BDT.pickle .

echo "Run TrainClassifiers.py"
python ${CMSSW_BASE}/src/TTH/TTHNtupleAnalyzer/python/TrainClassifiers.py
echo "Done TrainClassifiers.py"

#copy output
ME_CONF_NAME=$(basename "$ME_CONF")
OUTDIR=$HOME/deeptop/${TASK_ID}/${MY_JOBID}/
mkdir -p $OUTDIR 
echo "copying output"

cp $MY_SCRATCH/*.png $OUTDIR 
cp $MY_SCRATCH/valacc.txt $OUTDIR 
cp $MY_SCRATCH/maxvalacc.txt $OUTDIR 
cp $MY_SCRATCH/deltaacc.txt $OUTDIR 
env > $OUTDIR/env.txt


