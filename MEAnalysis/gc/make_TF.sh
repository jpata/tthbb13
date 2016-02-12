#!/bin/bash

#on PSI, CMSSW_BASE is not exported with the grid job, need to set manually
#export CMSSW_BASE=$HOME/tth/sw/CMSSW/

#print out the environment
env
set -e

pwd
ls -al

cd ${CMSSW_BASE}/src/TTH/MEAnalysis/

# We want to use a CMSSW 7.2 Root 5
# Root 6 has a memleak kills the jobs
# Standalone Root 5 doesn't have dcap
#export SCRAM_ARCH=slc6_amd64_gcc481
#. /afs/cern.ch/sw/lcg/external/gcc/4.8.1/x86_64-slc6-gcc48-opt/setup.sh 
#. /cvmfs/cms.cern.ch/slc6_amd64_gcc481/cms/cmssw/CMSSW_7_2_5/external/slc6_amd64_gcc481/bin/thisroot.sh 
#
#echo "Current ROOT Version"
#which root

# Go to work directory
cd $MY_SCRATCH

# Get some extra stuff
cp ${CMSSW_BASE}/src/TTH/TTHNtupleAnalyzer/python/AccessHelpers.py .
cp ${CMSSW_BASE}/src/TTH/Plotting/python/TransferFunctions/runs/@runconf@/cfg_outputtree.dat .
export PYTHONPATH=.:$PYTHONPATH

# And run
echo "Preparing to run outputtree-strict.py"
python ${CMSSW_BASE}/src/TTH/Plotting/python/TransferFunctions/outputtree-strict.py
echo "outputtree-strict.py is Done"

# Copy output
OUTDIR=$HOME/tth/gc/${TASK_ID}/
mkdir -p $OUTDIR 
echo "copying output"
OFNAME=$OUTDIR/output_${MY_JOBID}.root
cp $MY_SCRATCH/out.root $OFNAME
echo $OFNAME > output.txt

