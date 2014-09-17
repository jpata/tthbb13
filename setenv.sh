#source this file to set up the environment

#remember current dir
CURRENT_DIR=`pwd`

#get the directory of this file
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#save a global environment variable where this code is located
export TTH_DIR=$SCRIPT_DIR

#set the correct scram arch
export SCRAM_ARCH=slc6_amd64_gcc481

#do cmsenv
cd $SCRIPT_DIR
eval `scram runtime -sh`

#set up CRAB
source /cvmfs/cms.cern.ch/crab3/crab.sh

#create the grid proxy for 7 days
voms-proxy-init --voms cms --valid 168:00
voms-proxy-info --all

#go back to where we were
cd $CURRENT_DIR

echo "TTH environment setup complete"
echo $CMSSW_BASE
