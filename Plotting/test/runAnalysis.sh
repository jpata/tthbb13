#!/bin/bash

DATACARD_DIR=~/Dropbox/tth/datacards/ref2_spring15/Oct1/

#project out datacards
python python/Datacards/makeDatacard.py $DATACARD_DIR

#Run combine in parallel jobs
#python python/combine.py $DATACARD_DIR/shapes*.txt

#Make limit plots
python python/joosep/limits.py $DATACARD_DIR
