#!/bin/bash

set -e

JULIA=rjulia

#Produce skimmed jet trees
$JULIA ../MEAnalysis/test/jetskim.jl jets.root

#make b-tagger PDF histograms
python python/joosep/btag/hists.py jets.root ControlPlots.root

#make roc curve comparison plots
python python/joosep/btag/plots.py ControlPlots.root
