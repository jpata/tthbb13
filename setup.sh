export SCRAM_ARCH=slc6_amd64_gcc481
#cmsrel CMSSW_7_0_6_patch1
scram project -n CMSSW CMSSW CMSSW_7_2_0_pre5 
cd CMSSW/src/
cmsenv
git cms-addpkg PhysicsTools/PatAlgos
#git cms-merge-topic 4330
git clone https://github.com/jpata/tthbb13.git TTH
cp TTH/MEAnalysis/libs/*.so ../lib/$SCRAM_ARCH/
scram b -j 20
