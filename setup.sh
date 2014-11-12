export SCRAM_ARCH=slc6_amd64_gcc481
#cmsrel CMSSW_7_0_6_patch1

#newest version existing on PSI
scram project -n CMSSW CMSSW CMSSW_7_0_7_patch1
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

# Apply the jet toolbox patch
git apply  --ignore-whitespace --ignore-space-change --exclude DataFormats/PatCandidates/src/classes_def_objects.xml TTH/jet_toolbox.patch

# Bring fastjet contrib up to speed (necessary as long as we not on 7_2)
cp TTH/fastjet-xmls/* ../config/toolbox/$SCRAM_ARCH/tools/selected/
scram setup fastjet-contrib
scram setup fastjet-contrib-archive

# to apply a the top tagger as a patch
git apply -3 --ignore-whitespace --ignore-space-change --exclude DataFormats/PatCandidates/src/classes_def_objects.xml TTH/0001-merged-HepTopTagger.patch

scram setup lhapdf

# And build:
# scram b -j 10