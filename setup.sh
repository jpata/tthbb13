export SCRAM_ARCH=slc6_amd64_gcc481
#cmsrel CMSSW_7_0_6_patch1
scram project -n CMSSW CMSSW CMSSW_7_0_6_patch1 
cd CMSSW_7_0_6_patch1/src/
cmsenv
git cms-addpkg PhysicsTools/PatAlgos
git cms-merge-topic 4330
scram b -j 20
