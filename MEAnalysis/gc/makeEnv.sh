#!/bin/bash
# Prepares user specific environment variables.
# Run once when you setup
# env.sh should NOT GO under version control
echo export CMSSW_BASE=$CMSSW_BASE > env.sh
echo export SCRAM_ARCH=$SCRAM_ARCH >> env.sh
