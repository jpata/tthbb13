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

#to get original 7_2 top-tagger code
#git remote add gkasieczka https://github.com/gkasieczka/cmssw.git
#git fetch -a gkasieczka
#git merge 8cb31b5587b7e73780d58976a8d174c01330cf44
#toptagger merged from branch CMSSW_7_2_X / htt-dev

#get the TTH code
git clone https://github.com/jpata/tthbb13.git TTH
cp TTH/MEAnalysis/libs/*.so ../lib/$SCRAM_ARCH/

#apply the top tagger as a commit
#git remote add jpata https://github.com/jpata/cmssw.git
#git fetch -a jpata
#git merge jpata/patched_toptagger

#to apply a the top tagger as a patch
#git apply --check TTH/0001-merged-HepTopTagger.patch && git apply TTH/0001-merged-HepTopTagger.patch  
#git apply -v --ignore-whitespace TTH/0001-merged-HepTopTagger.patch
git apply -3 --ignore-whitespace --ignore-space-change TTH/0001-merged-HepTopTagger.patch

scram setup lhapdf
