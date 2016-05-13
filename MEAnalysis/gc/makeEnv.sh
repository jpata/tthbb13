#!/bin/bash
# Prepares user specific environment variables.
# Run once when you setup
# env.sh should NOT GO under version control
echo export CMSSW_BASE=$CMSSW_BASE > env.sh
echo export SCRAM_ARCH=$SCRAM_ARCH >> env.sh
echo export USER=$USER >> env.sh
echo export TTH_STAGEOUT_PATH=/home/$USER/tth/gc >> env.sh
