#pragma once
#include <map>
#include "TTree.h"
#include "TLeaf.h"
#include "TFile.h"

#include <iostream>
#include <assert.h>

using namespace std;

template <class T>
class ScalarBranch {
public:
    
    //buffer for SetBranchAddress
    T val;
    
    ScalarBranch() {
        zero();
    }
    void zero() {
        val = (T)0;
    }
};

template <class T>
class VariableArrayBranch {
public:
    
    //buffer for SetBranchAddress
    T val[500];
    
    //Name of the branch that contains the length.
    const std::string length_name;
    
    //Clear buffers
    void zero() {
        for (int i=0; i<500; i++) {
            val[i] = (T)0;
        }
    }    
    
    VariableArrayBranch(const std::string _length_name) :
    length_name(_length_name) {
    }
};

class AutoTree {
public:
    
    //Double and double array buffers
    std::map<const std::string, ScalarBranch<double>*>          doubles_map;
    std::map<const std::string, VariableArrayBranch<double>*>   vdoubles_map;
    
    //Float and float array buffers
    std::map<const std::string, ScalarBranch<float>*>           floats_map;
    std::map<const std::string, VariableArrayBranch<float>*>    vfloats_map;
    
    //Int and int array buffers
    std::map<const std::string, ScalarBranch<int>*>             ints_map;
    std::map<const std::string, VariableArrayBranch<int>*>      vints_map;
    TTree* tree;
    
    AutoTree(TTree* tree);

    unsigned long getEntry(unsigned long i);
    
    template <class T>
    T getValue(const std::string name);
};
