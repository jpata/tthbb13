export SCRAM_ARCH=slc6_amd64_gcc491

scram project -n CMSSW CMSSW CMSSW_7_4_7_patch1
cd CMSSW/src/
cmsenv
git cms-init

git checkout -b merge
#Get the vhbb-heppy code

git cms-merge-topic vhbb:vhbbHeppy74X

#get the TTH code
git clone https://github.com/jpata/tthbb13.git TTH
cd TTH
git checkout meanalysis-74x
git clone https://github.com/bianchini/Code.git MEIntegratorStandalone
cd MEIntegratorStandalone

cd ../..
#after scram b clean, these need to be copied again
cp TTH/MEAnalysis/libs/*.so ../lib/$SCRAM_ARCH/
scram setup lhapdf

# And build:
# scram b -j 10
