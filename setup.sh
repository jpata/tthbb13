export SCRAM_ARCH=slc6_amd64_gcc493

scram project -n CMSSW CMSSW CMSSW_7_6_3_patch2
cd CMSSW/src/
cmsenv
git cms-init

git cms-merge-topic jpata:V21_v1

#get the TTH code
git clone https://github.com/jpata/tthbb13.git TTH
cd TTH
git checkout meanalysis-76x
git clone https://github.com/bianchini/Code.git MEIntegratorStandalone
cd MEIntegratorStandalone
cd ../..

cd TTH
git clone https://github.com/jpata/CommonClassifier.git --branch mem_npoints
cd ..

#git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
#cd HiggsAnalysis/CombinedLimit
#git checkout 74x-root6
#cd ../..

#after scram b clean, these need to be copied again
cp -R TTH/MEIntegratorStandalone/libs/* ../lib/$SCRAM_ARCH/

scram setup lhapdf

cd TTH/MEAnalysis/gc
git clone https://github.com/grid-control/grid-control
cd grid-control
git checkout from-svn
cd ../../..
# And build:
# scram b -j 10
