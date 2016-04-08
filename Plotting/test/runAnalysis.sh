#!/bin/bash

set -e

DATACARD_DIR=./testhists
WD=$PWD
CODEDIR=$CMSSW_BASE/src/TTH

#make json job files for histogram projector
python python/makeJobfiles.py
##run histograms
ls job*.json | parallel --gnu --results res ./melooper {}

#merge and move to output dir
hadd -f ControlPlotsSparse.root ControlPlotsSparse_*.root
rm ControlPlotsSparse_*.root
rm job_*.json
#
#mkdir -p $DATACARD_DIR
#mv ControlPlots.root $DATACARD_DIR/
#
##project out datacards
#python python/Datacards/makeDatacard.py $DATACARD_DIR

#Run combine in parallel jobs
#cd $DATACARD_DIR
#python $CODEDIR/Plotting/python/combine.py shapes*.txt
#cd $WD
#
##Make limit plots
#python python/joosep/limits.py $DATACARD_DIR
