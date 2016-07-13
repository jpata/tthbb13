export SCRAM_ARCH=slc6_amd64_gcc530

scram project -n CMSSW CMSSW CMSSW_8_0_11
cd CMSSW/src/
eval `scramv1 runtime -sh`

git cms-init
git cms-merge-topic jpata:meanalysis-80x

#get the TTH code
git clone https://github.com/jpata/tthbb13.git TTH --branch meanalysis-80x 
cd $CMSSW_BASE/src/TTH

git clone https://github.com/jpata/Code.git MEIntegratorStandalone --branch v0.3
git clone https://github.com/cms-ttH/CommonClassifier.git CommonClassifier --branch master
git clone https://github.com/grid-control/grid-control MEAnalysis/gc/grid-control --branch r1864
git clone https://github.com/jpata/ttH-bb-GenAnalysis.git GenLevel

cd $CMSSW_BASE/src

#FIXME: combine is not yet 80X?
#git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit --branch 74x-root6
#after scram b clean, these need to be copied again
cp -R TTH/MEIntegratorStandalone/libs/* ../lib/$SCRAM_ARCH/
scram setup lhapdf
