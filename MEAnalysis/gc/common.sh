#Try to find out on which site we are running
SITE="UNKNOWN"
hnamestr=`hostname`
if [[ "$hnamestr" == t3* ]]; then
    export SITE="PSI"
elif [[ "$hnamestr" == comp* ]]; then
    export SITE="TALLINN"
fi

# Get private environment variables
source env.sh

env
set -e

pwd
ls -al

#set env
cd ${CMSSW_BASE}/src/TTH/MEAnalysis/
export SCRAM_ARCH="slc6_amd64_gcc491"
source /cvmfs/cms.cern.ch/cmsset_default.sh
#eval `scramv1 runtime -sh`
if [[ "$SITE" == "PSI" ]]; then
    source ${CMSSW_BASE}/src/TTH/setenv_psi.sh
elif [[ "$SITE" == "TALLINN" ]]; then
    source ${CMSSW_BASE}/src/TTH/setenv_kbfi.sh
fi
