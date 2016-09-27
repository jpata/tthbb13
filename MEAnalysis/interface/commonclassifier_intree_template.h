#ifndef COMMONCLASSIFIER_INPUT_TREE
#define COMMONCLASSIFIER_INPUT_TREE

#include <TTree.h>
#include <cmath>
#include <iostream>
#include <string>

//HEADERGEN_DEFINES

//macros to initialize 1D and 2D (square) arrays
//x is the array, n is the size, y is the initialized value
#define SET_ZERO(x,n,y) for(int i=0;i<n;i++) {x[i]=y;}
#define SET_ZERO_2(x,n,m,y) for(int i=0;i<n;i++) { for(int j=0;j<m;j++) { x[i][j]=y; } }

/*
This is a simple wrapper class for the TTH-specific flat data format.
To use it, one should load the input file in the standard way using
TFile* f = new TFile("ntuple.root");
TTree* _ttree = (TTree*)f->Get("tthNtupleAnalyzer/events");
and then initialize the class using
CommonClassifierInputTree tree(_ttree);
CommonClassifierInputTree contains the C++ variables for all the branches and functions to conveniently set them.
To attach the branches in the read mode (call SetBranchAddress), call
tree.set_branch_addresses();
outside the event loop.
 You can loop over the events in the standard way
 for (unsigned int i=0; i < _ttree->GetEntries(); i++) {
     tree.loop_initialize(); // <-- this makes sure all the branch variables are cleared from the previous entry
     _ttree->GetEntry(i); // <--- loads the branch contents into the branch variables
     for (int njet=0; njet < tree.n__jet; njet++) {
         float x = tree.jet__pt[njet];
         //do something with the jet pt 
     }
*/
class CommonClassifierInputTree {
public:
    CommonClassifierInputTree(TTree* _tree) { tree = _tree; };
    TTree* tree;
   
        // Helper functions for accessing branches
    template <typename T> 
    T get_address(const std::string name) {
        auto* br = tree->GetBranch(name.c_str());
        if (br==0) {
            std::cerr << "ERROR: get_address CommonClassifierInputTree " << "branch " << name << " does not exist" << std::endl;
            throw std::exception();
        }
        auto* p = br->GetAddress();
        return reinterpret_cast<T>(p);
    }
    
    //HEADERGEN_BRANCH_VARIABLES
    //This comment is for automatic header generation, do not remove

    //initializes all branch variables
    void loop_initialize(void) {        
        //HEADERGEN_BRANCH_INITIALIZERS
    }

    //makes branches on a new TTree
    void make_branches(void) {
        //HEADERGEN_BRANCH_CREATOR
    }

    //connects the branches of an existing TTree to variables
    //used when loading the file
    void set_branch_addresses(void) {        
        //HEADERGEN_BRANCH_SETADDRESS
    }
};

#endif
