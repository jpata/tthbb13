#!/bin/bash
echo "Running"
set -e

cd $GC_SCRATCH
tar xf job_*.tar.gz
cd CMSSW*/work/
./run.sh
cp log $GC_SCRATCH/
cp Output/cmsRun.log $GC_SCRATCH/
cp Output/tree.root $GC_SCRATCH/tree_cmssw.root
cp tree.root $GC_SCRATCH/
