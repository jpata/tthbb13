//python $CMSSW_BASE/src/TTH/TTHNtupleAnalyzer/python/headergen.py $CMSSW_BASE/src/TTH/MEAnalysis/interface/btag_lr_tree_template.hh $CMSSW_BASE/src/TTH/MEAnalysis/interface/bteag_lr_tree.hh $CMSSW_BASE/src/TTH/MEAnalysis/python/btag_lr_tree_branches.py
#include "TTH/TTHNtupleAnalyzer/interface/tth_tree.hh"

class BTagLRTree {
	public:
	TTree* tree;
	float permutation_pos;
	float bLep_pos;
	float w1_pos;
	float w2_pos;
	float bHad_pos;
	float b1_pos;
	float jets_bLep_pos;
	float jets_w1_pos;
	float jets_w2_pos;
	float jets_bHad_pos;
	float jets_b1_pos;
	float p_b_bLep;
	float p_b_bHad;
	float p_b_b1;
	float p_j_b1;
	float p_b_b2;
	float p_j_b2;
	float p_j_w1;
	float p_j_w2;
	float hypo;
	float p_pos;
	float p_bb;
	float p_jj;
	int event;
	int syst;
	int nS;
	int nB;
	int id_bLep;
	int id_bHad;
	int id_b1;
	int id_b2;
	int id_w1;
	int id_w2;
	int permutation;
	int event_run;
	int event_lumi;
	int event_id;
    //HEADERGEN_BRANCH_VARIABLES


	BTagLRTree(TTree* _tree) {
        tree = _tree;
    };

	void make_branches() {
		tree->Branch("permutation_pos", &permutation_pos, "permutation_pos/F");
		tree->Branch("bLep_pos", &bLep_pos, "bLep_pos/F");
		tree->Branch("w1_pos", &w1_pos, "w1_pos/F");
		tree->Branch("w2_pos", &w2_pos, "w2_pos/F");
		tree->Branch("bHad_pos", &bHad_pos, "bHad_pos/F");
		tree->Branch("b1_pos", &b1_pos, "b1_pos/F");
		tree->Branch("jets_bLep_pos", &jets_bLep_pos, "jets_bLep_pos/F");
		tree->Branch("jets_w1_pos", &jets_w1_pos, "jets_w1_pos/F");
		tree->Branch("jets_w2_pos", &jets_w2_pos, "jets_w2_pos/F");
		tree->Branch("jets_bHad_pos", &jets_bHad_pos, "jets_bHad_pos/F");
		tree->Branch("jets_b1_pos", &jets_b1_pos, "jets_b1_pos/F");
		tree->Branch("p_b_bLep", &p_b_bLep, "p_b_bLep/F");
		tree->Branch("p_b_bHad", &p_b_bHad, "p_b_bHad/F");
		tree->Branch("p_b_b1", &p_b_b1, "p_b_b1/F");
		tree->Branch("p_j_b1", &p_j_b1, "p_j_b1/F");
		tree->Branch("p_b_b2", &p_b_b2, "p_b_b2/F");
		tree->Branch("p_j_b2", &p_j_b2, "p_j_b2/F");
		tree->Branch("p_j_w1", &p_j_w1, "p_j_w1/F");
		tree->Branch("p_j_w2", &p_j_w2, "p_j_w2/F");
		tree->Branch("hypo", &hypo, "hypo/F");
		tree->Branch("p_pos", &p_pos, "p_pos/F");
		tree->Branch("p_bb", &p_bb, "p_bb/F");
		tree->Branch("p_jj", &p_jj, "p_jj/F");
		tree->Branch("event", &event, "event/I");
		tree->Branch("syst", &syst, "syst/I");
		tree->Branch("nS", &nS, "nS/I");
		tree->Branch("nB", &nB, "nB/I");
		tree->Branch("id_bLep", &id_bLep, "id_bLep/I");
		tree->Branch("id_bHad", &id_bHad, "id_bHad/I");
		tree->Branch("id_b1", &id_b1, "id_b1/I");
		tree->Branch("id_b2", &id_b2, "id_b2/I");
		tree->Branch("id_w1", &id_w1, "id_w1/I");
		tree->Branch("id_w2", &id_w2, "id_w2/I");
		tree->Branch("permutation", &permutation, "permutation/I");
		tree->Branch("event_run", &event_run, "event_run/I");
		tree->Branch("event_lumi", &event_lumi, "event_lumi/I");
		tree->Branch("event_id", &event_id, "event_id/I");
		//HEADERGEN_BRANCH_CREATOR
	}
        
	void set_branch_addresses() {
		tree->SetBranchAddress("permutation_pos", &permutation_pos);
		tree->SetBranchAddress("bLep_pos", &bLep_pos);
		tree->SetBranchAddress("w1_pos", &w1_pos);
		tree->SetBranchAddress("w2_pos", &w2_pos);
		tree->SetBranchAddress("bHad_pos", &bHad_pos);
		tree->SetBranchAddress("b1_pos", &b1_pos);
		tree->SetBranchAddress("jets_bLep_pos", &jets_bLep_pos);
		tree->SetBranchAddress("jets_w1_pos", &jets_w1_pos);
		tree->SetBranchAddress("jets_w2_pos", &jets_w2_pos);
		tree->SetBranchAddress("jets_bHad_pos", &jets_bHad_pos);
		tree->SetBranchAddress("jets_b1_pos", &jets_b1_pos);
		tree->SetBranchAddress("p_b_bLep", &p_b_bLep);
		tree->SetBranchAddress("p_b_bHad", &p_b_bHad);
		tree->SetBranchAddress("p_b_b1", &p_b_b1);
		tree->SetBranchAddress("p_j_b1", &p_j_b1);
		tree->SetBranchAddress("p_b_b2", &p_b_b2);
		tree->SetBranchAddress("p_j_b2", &p_j_b2);
		tree->SetBranchAddress("p_j_w1", &p_j_w1);
		tree->SetBranchAddress("p_j_w2", &p_j_w2);
		tree->SetBranchAddress("hypo", &hypo);
		tree->SetBranchAddress("p_pos", &p_pos);
		tree->SetBranchAddress("p_bb", &p_bb);
		tree->SetBranchAddress("p_jj", &p_jj);
		tree->SetBranchAddress("event", &event);
		tree->SetBranchAddress("syst", &syst);
		tree->SetBranchAddress("nS", &nS);
		tree->SetBranchAddress("nB", &nB);
		tree->SetBranchAddress("id_bLep", &id_bLep);
		tree->SetBranchAddress("id_bHad", &id_bHad);
		tree->SetBranchAddress("id_b1", &id_b1);
		tree->SetBranchAddress("id_b2", &id_b2);
		tree->SetBranchAddress("id_w1", &id_w1);
		tree->SetBranchAddress("id_w2", &id_w2);
		tree->SetBranchAddress("permutation", &permutation);
		tree->SetBranchAddress("event_run", &event_run);
		tree->SetBranchAddress("event_lumi", &event_lumi);
		tree->SetBranchAddress("event_id", &event_id);
		//HEADERGEN_BRANCH_SETADDRESS
	}

	void loop_initialize() {
		permutation_pos = DEF_VAL_FLOAT;
		bLep_pos = DEF_VAL_FLOAT;
		w1_pos = DEF_VAL_FLOAT;
		w2_pos = DEF_VAL_FLOAT;
		bHad_pos = DEF_VAL_FLOAT;
		b1_pos = DEF_VAL_FLOAT;
		jets_bLep_pos = DEF_VAL_FLOAT;
		jets_w1_pos = DEF_VAL_FLOAT;
		jets_w2_pos = DEF_VAL_FLOAT;
		jets_bHad_pos = DEF_VAL_FLOAT;
		jets_b1_pos = DEF_VAL_FLOAT;
		p_b_bLep = DEF_VAL_FLOAT;
		p_b_bHad = DEF_VAL_FLOAT;
		p_b_b1 = DEF_VAL_FLOAT;
		p_j_b1 = DEF_VAL_FLOAT;
		p_b_b2 = DEF_VAL_FLOAT;
		p_j_b2 = DEF_VAL_FLOAT;
		p_j_w1 = DEF_VAL_FLOAT;
		p_j_w2 = DEF_VAL_FLOAT;
		hypo = DEF_VAL_FLOAT;
		p_pos = DEF_VAL_FLOAT;
		p_bb = DEF_VAL_FLOAT;
		p_jj = DEF_VAL_FLOAT;
		event = DEF_VAL_INT;
		syst = DEF_VAL_INT;
		nS = DEF_VAL_INT;
		nB = DEF_VAL_INT;
		id_bLep = DEF_VAL_INT;
		id_bHad = DEF_VAL_INT;
		id_b1 = DEF_VAL_INT;
		id_b2 = DEF_VAL_INT;
		id_w1 = DEF_VAL_INT;
		id_w2 = DEF_VAL_INT;
		permutation = DEF_VAL_INT;
		event_run = DEF_VAL_INT;
		event_lumi = DEF_VAL_INT;
		event_id = DEF_VAL_INT;
		//HEADERGEN_BRANCH_INITIALIZERS
	}

};
