#include "TFile.h"
#include "TTree.h"
#include "TTH/Plotting/interface/metree.h"
#include <iostream>

int main(int argc, const char** argv) {
    TFile* tf = new TFile("/Users/joosep/Documents/tth/data/ntp/v12/Sep14/ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root");
    TTree* tree = (TTree*)(tf->Get("tree"));
    
    TreeData data;
    data.loadTree(tree);

    int njtot = 0;
    for (int i=0; i<100; i++) {
        tree->GetEntry(i);
        njtot += data.numJets;
        std::cout << "nj " << data.numJets << std::endl;
    }
    return 0;
}
