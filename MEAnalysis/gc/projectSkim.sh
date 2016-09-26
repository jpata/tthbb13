#!/bin/bash

source common.sh
#export DATASETPATH=ttHTobb_M125_13TeV_powheg_pythia8
#export FILE_NAMES=/store/user/jpata/tth/Jun17_leptonic_nome/TT_TuneEE5C_13TeV-powheg-herwigpp/Jun17_leptonic_nome/160617_165529/0000/tree_1.root
#export GC_SCRATCH=/scratch/jpata

#go to work directory
cd $GC_SCRATCH

#python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/MakeTaggingNtuple.py taggingNtuple.root $FILE_NAMES
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/projectSkim.py skim.root $FILE_NAMES
python ${CMSSW_BASE}/src/TTH/Plotting/python/joosep/btag/hists.py btag.root $FILE_NAMES
python ${CMSSW_BASE}/src/TTH/MEAnalysis/python/counts.py count.root $FILE_NAMES
hadd out.root skim.root btag.root count.root
