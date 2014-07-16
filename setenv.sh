CURRENT_DIR=`pwd`
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export TTH_DIR=$SCRIPT_DIR
cd $SCRIPT_DIR/CMSSW*
eval `scram runtime -sh`
cd $CURRENT_DIR
