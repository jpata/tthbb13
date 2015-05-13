export SCRAM_ARCH=slc6_amd64_gcc491

scram project -n CMSSW CMSSW CMSSW_7_4_1_patch1
cd CMSSW/src/
cmsenv
git cms-addpkg PhysicsTools/PatAlgos

#for top tagger
git cms-addpkg DataFormats/JetReco
git cms-addpkg RecoJets/JetAlgorithms
git cms-addpkg RecoJets/JetProducers

# get the TTH code
git clone https://github.com/jpata/tthbb13.git TTH
cd TTH
git checkout dev-74X
cd ..

# Add HEPTopTagger
git cms-merge-topic gkasieczka:htt-v2-74X

cp $CMSSW_BASE/external/$SCRAM_ARCH/lib/* $CMSSW_BASE/lib/$SCRAM_ARCH/

# And build:
scram b -j 10
