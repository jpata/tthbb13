export SCRAM_ARCH=slc6_amd64_gcc493

scram project -n CMSSW CMSSW CMSSW_7_6_3_patch2
cd CMSSW/src/
cmsenv
git cms-init

git cms-merge-topic jpata:V21_v1

#get the TTH code
git clone https://github.com/jpata/tthbb13.git TTH
cd TTH
git checkout meanalysis-76x_V9
git clone https://github.com/bianchini/Code.git TTH/MEIntegratorStandalone

git clone https://github.com/jpata/CommonClassifier.git TTH/CommonClassifier --branch mem_npoints

git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit --branch 74x-root6 

#after scram b clean, these need to be copied again
cp -R TTH/MEIntegratorStandalone/libs/* ../lib/$SCRAM_ARCH/

scram setup lhapdf

cd TTH/MEAnalysis/gc
git clone https://github.com/grid-control/grid-control
cd $CMSSW_BASE
