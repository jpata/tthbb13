export SCRAM_ARCH=slc6_amd64_gcc481

#newest version existing on PSI
scram project -n CMSSW CMSSW CMSSW_7_2_2_patch1
cd CMSSW/src/
cmsenv
git cms-addpkg PhysicsTools/PatAlgos

#for top tagger
git cms-addpkg DataFormats/JetReco
git cms-addpkg RecoJets/JetAlgorithms
git cms-addpkg RecoJets/JetProducers

#get the TTH code
git clone https://github.com/jpata/tthbb13.git TTH
cp TTH/MEAnalysis/libs/*.so ../lib/$SCRAM_ARCH/

# to apply a the top tagger as a patch
git apply -3 --ignore-whitespace --ignore-space-change --exclude DataFormats/PatCandidates/src/classes_def_objects.xml TTH/0001-merged-HepTopTagger.patch

scram setup lhapdf

cp $CMSSW_BASE/external/$SCRAM_ARCH/lib/* $CMSSW_BASE/lib/$SCRAM_ARCH/
# And build:
# scram b -j 10
