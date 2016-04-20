export SCRAM_ARCH=slc6_amd64_gcc530

scram project -n CMSSW CMSSW CMSSW_8_0_4
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
git checkout tagging-80X
cd ..

# Add HEPTopTagger
git cms-merge-topic gkasieczka:htt-v2-76X

cp $CMSSW_BASE/external/$SCRAM_ARCH/lib/* $CMSSW_BASE/lib/$SCRAM_ARCH/

# And build:
scram b -j 10
