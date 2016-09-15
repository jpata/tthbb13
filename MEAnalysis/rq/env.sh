source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
source ${CMSSW_BASE}/src/TTH/setenv_psi.sh
#to get the rq exe
export PATH=~jpata/anaconda/bin:$PATH
export PYTHONPATH=${CMSSW_BASE}/python:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/lcg/root/6.06.00-ikhhed4/lib
