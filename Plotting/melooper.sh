#!/bin/bash
#HOSTNAME=`hostname`
#if [[ "$hnamestr" == *.hep.kbfi.ee ]]; then
#    source /home/joosep/root-6.05.02/bin/thisroot.sh
#elif [[ "$hnamestr" == t3ui* ]]; then
#    source /afs/cern.ch/sw/lcg/external/gcc/4.9/x86_64-slc6-gcc49-opt/setup.sh
#    source /afs/cern.ch/sw/lcg/app/releases/ROOT/6.05.02/x86_64-slc6-gcc49-opt/root/bin/thisroot.sh
#fi

export SCRAM_ARCH="slc6_amd64_gcc491"
source /cvmfs/cms.cern.ch/cmsset_default.sh
source ${CMSSW_BASE}/src/TTH/setenv_kbfi.sh

#go to work directory
cd $MY_SCRATCH

python ${CMSSW_BASE}/src/TTH/Plotting/python/makeJobfile.py
${CMSSW_BASE}/src/TTH/Plotting/melooper job.json

OUTDIR=$HOME/tth/gc/melooper/${TASK_ID}/
OFNAME=$OUTDIR/output_${MY_JOBID}.root
cp ControlPlotsSparse.root $OFNAME
mkdir -p $OUTDIR 
