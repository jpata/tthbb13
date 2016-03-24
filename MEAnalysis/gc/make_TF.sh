#!/bin/bash

source common.sh

# Go to work directory
cd $MY_SCRATCH

# Get some extra stuff
cp ${CMSSW_BASE}/src/TTH/TTHNtupleAnalyzer/python/AccessHelpers.py .
cp ${CMSSW_BASE}/src/TTH/Plotting/python/TransferFunctions/runs/$dsversion"_"$jettype/cfg_outputtree.dat .
export PYTHONPATH=.:$PYTHONPATH

echo "Preparing to run outputtree-strict.py"

python ${CMSSW_BASE}/src/TTH/Plotting/python/TransferFunctions/outputtree-strict.py
echo "outputtree-strict.py is Done"

# Copy output
export SRMBASE=srm://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/
OUTDIR=/store/user/$USER/tth/gc/makeTF/${TASK_ID}/@runconf@/
gfal-mkdir -p $SRMBASE/$OUTDIR || true
echo "copying output"
OFNAME=$OUTDIR/output_${MY_JOBID}.root
gfal-copy file://$MY_SCRATCH/out.root $SRMBASE/$OFNAME
echo $OFNAME > output.txt

