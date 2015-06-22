#!/bin/bash

#Download the anaconda package
set -e
wget http://phys.hep.kbfi.ee/~joosep/Anaconda-2.2.0-Linux-x86_64.sh
chmod +x Anaconda-2.2.0-Linux-x86_64.sh
#
##Install anaconda to the cmssw directory
./Anaconda-2.2.0-Linux-x86_64.sh -p $CMSSW_BASE/anaconda -b

#point the PYTHONPATH variable to the anaconda dir
source setenv.sh

#Install library for tables
pip install tabulate

pip install --upgrade numpy

#upgrade machine learning
pip install --upgrade scikit-learn

#upgrade data table library
pip install --upgrade pandas

pip install --upgrade rootpy
pip install --upgrade root_numpy
