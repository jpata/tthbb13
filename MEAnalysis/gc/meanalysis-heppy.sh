#!/bin/bash

#uncomment these to test the script
#these are all the input parameters that MEAnalysis_heppy_gc.py reads
#export SKIP_EVENTS=0
#export MAX_EVENTS=200
#export DATASETPATH=ttHTobb_M125_13TeV_powheg_pythia8
#export FILE_NAMES=/store/user/jpata/VHBBHeppyV20/ttHTobb_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V20_ttHTobb_M125_13TeV_powheg_Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160209_170826/0000/tree_1.root
#export MY_SCRATCH=./

# Get private environment variables
echo "Reading env.sh:"
cat env.sh
source env.sh
echo "Done reading env.sh:"
source common.sh

#here we use @...@ to give grid-control the possibility to substitute the configuration file name
#comment this line when testing locally
#export ME_CONF=$CMSSW_BASE/src/TTH/MEAnalysis/python/cfg_withME.py
export ME_CONF=$CMSSW_BASE/src/TTH/MEAnalysis/python/@me_conf@

#go to work directory
cd $MY_SCRATCH

#print out the environment
env

# Make sure we process all evenats (as currently using file based splitting)
# Change back if we go to event bases
export MAX_EVENTS=9999999999

python ${CMSSW_BASE}/src/TTH/MEAnalysis/gc/MEAnalysis_heppy_gc.py
echo "MEAnalysis is done"

#copy output
ME_CONF_NAME=$(basename "$ME_CONF")
export SRMBASE=srm://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/
OUTDIR=/store/user/$USER/tth/${TASK_ID}/${ME_CONF_NAME%.*}/${DATASETPATH}/
gfal-mkdir -p $SRMBASE/$OUTDIR || true
echo "copying output"
OFNAME=$OUTDIR/output_${MY_JOBID}.root
gfal-copy file://$MY_SCRATCH/Loop/tree.root $SRMBASE/$OFNAME
echo $OFNAME > output.txt

