//python $CMSSW_BASE/src/TTH/TTHNtupleAnalyzer/python/headergen.py $CMSSW_BASE/src/TTH/MEAnalysis/interface/btag_lr_tree_template.hh $CMSSW_BASE/src/TTH/MEAnalysis/interface/bteag_lr_tree.hh $CMSSW_BASE/src/TTH/MEAnalysis/python/btag_lr_tree_branches.py
#include "TTH/TTHNtupleAnalyzer/interface/tth_tree.hh"

class BTagLRTree {
	public:
	TTree* tree;
    //HEADERGEN_BRANCH_VARIABLES


	BTagLRTree(TTree* _tree) {
        tree = _tree;
    };

	void make_branches() {
		//HEADERGEN_BRANCH_CREATOR
	}
        
	void set_branch_addresses() {
		//HEADERGEN_BRANCH_SETADDRESS
	}

	void loop_initialize() {
		//HEADERGEN_BRANCH_INITIALIZERS
	}

};
