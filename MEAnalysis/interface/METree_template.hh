#ifndef METREE_H
#define METREE_H
//Generate METree.hh with
//python $CMSSW_BASE/src/TTH/TTHNtupleAnalyzer/python/headergen.py $CMSSW_BASE/src/TTH/MEAnalysis/interface/METree_template.hh $CMSSW_BASE/src/TTH/MEAnalysis/interface/METree.hh $CMSSW_BASE/src/TTH/MEAnalysis/python/branches.py
#include "TTH/MEAnalysis/interface/HelperFunctions.h"
#include "TTH/TTHNtupleAnalyzer/interface/tth_tree.hh"

// maximum number of permutations per event
#define NMAXPERMUT 60

// maximum number of mass points for likelihood scan
#define NMAXMASS   20

// maximum number of four-vectors per event saved in output
#define NMAXJETS   10

#define NMAXLEPTONS 2
class METree {
public:
	METree(TTree* _tree) {
        tree = _tree;
    };
	
	template <typename T> 
	T get_address(const std::string name) {
		auto* br = tree->GetBranch(name.c_str());
		if (br==0) {
			std::cerr << "ERROR: get_address METree " << "branch " << name << " does not exist" << std::endl;
			throw std::exception();
		}
		auto* p = br->GetAddress();
		return reinterpret_cast<T>(p);
	}

	TTree* tree;
    
    // counts how many events have been analyzed (to have fixed-size jobs)
    int counter_;
    
	//Index of the processed sample
    int sample;
    
	// number of jet-quark permutations (for signal and bkg hypotheses)
    int nPermut_, nPermut_alt_;
    // number of (Higgs/Top) mass points
    int nMassPoints_;
    // total number integration per event (nPermut*nMassPoints)
    int nTotInteg_,nTotInteg_alt_;
    
    // number of matches to higgs quarks among tagged jets
    int matchesH_;
    // number of matches to W quarks among un-tagged jets
    int matchesW_;
    // number of matches to top quarks among tagged jets
    int matchesT_;
    // number of matches to higgs quarks among all jets
    int matchesHAll_;
    // number of matches to W quarks among all jets
    int matchesWAll_;
    // number of matches to top quarks among all jets
    int matchesTAll_;
    // count how many quarks from W decay overlap by dR<0.5
    int overlapLight_;
    // count how many b-quarks overlap by dR<0.5
    int overlapHeavy_;
    
    // integration type
    int type_;
    
    // sytematics
    int syst_;
    
    // number of systematic loops per event
    int iterations_;
    
    // num. of b-hadrons and c-quarks
    int nSimBs_; //, nC_, nCTop_;
    int nSimCs_;
    
    // num of b-hadrons inside jets (backward compatibility)
    int nMatchSimBsOld_;
    // num of b-hadrons inside jets
    // gen_eta < 5, gen_pt > 20
    int nMatchSimBs_v1_;
    // gen_eta <2.5, gen_pt > 20
    int nMatchSimBs_v2_;
    // gen_eta < 2.5, gen_pt > 20, reco_pt > 30
    int nMatchSimBs_;
    // num of c-hadrons inside jets
    int nMatchSimCs_v1_;
    int nMatchSimCs_v2_;
    int nMatchSimCs_;
    
    // gen top/higgs informations
    float p4H_   [4];
    float p4T_   [4];
    float p4Tbar_[4];
    
    // a structure with tth gen system infos
    tthInfo ttH_;
    
    // type-dependent flags
    int flag_type0_;
    int flag_type1_;
    int flag_type2_;
    int flag_type3_;
    int flag_type4_;
    int flag_type6_;
    
    // event-wise **ME** probability (summed over permutations)
    // ...for ttH...
    float probAtSgn_ ;
    
    // ...for ttbb...
    float probAtSgn_alt_ ;
    
    // event-wise **ME X btag** probability (summed over permutations)
    // ...for ttH...
    float probAtSgn_ttbb_;
    // ...for tt(bb,jj,bj,cc)...
    float probAtSgn_alt_ttbb_;
    float probAtSgn_alt_ttjj_;
    float probAtSgn_alt_ttbj_;
    float probAtSgn_alt_ttcc_;
    
    // per-permutation and mass value **ME** probability
    float probAtSgn_permut_       [NMAXPERMUT*NMAXMASS];
    float probAtSgn_alt_permut_   [NMAXPERMUT*NMAXMASS];
    float probAtSgnErr_permut_    [NMAXPERMUT*NMAXMASS];
    float probAtSgnErr_alt_permut_[NMAXPERMUT*NMAXMASS];
    int   callsAtSgn_permut_      [NMAXPERMUT*NMAXMASS];
    int   callsAtSgn_alt_permut_  [NMAXPERMUT*NMAXMASS];
    float chi2AtSgn_permut_       [NMAXPERMUT*NMAXMASS];
    float chi2AtSgn_alt_permut_   [NMAXPERMUT*NMAXMASS];
    
    // per-permutation **btag** probability
    float probAtSgn_bb_permut_[NMAXPERMUT];
    float probAtSgn_bj_permut_[NMAXPERMUT];
    float probAtSgn_cc_permut_[NMAXPERMUT];
    float probAtSgn_jj_permut_[NMAXPERMUT];
    
    // masses to be scanned
    float mH_scan_[NMAXMASS];
    float mT_scan_[NMAXMASS];
    
    // a flag for the event type
    int Vtype_;
    // event-dependent weight (for normalization)
    float weight_;
    
    // event-dependent CSV weight (for normalization)
    float weightCSV_[19];
    
    // for theory systematics (tt+jets only)
    float SCALEsyst_[3];
    
    // additional gen top PT scale factor
    float weightTopPt_;
    // cpu time
    float time_;
    // event information
    EventInfo EVENT_;
    // num of PVs
    int nPVs_;
    // pu reweighting
    float PUweight_, PUweightP_, PUweightM_;
    // trigger turn-on
    float trigger_;
    float triggerErr_;
    // trigger bits (data)
    bool triggerFlags_[70];
    // number of gen jets
    float lheNj_;
    
    // number of b's, c's, l's, and gluons in the multi-leg ME
    int n_b_, n_c_, n_l_, n_g_;
    
    // lepton kinematic (at most two leptons)
    int   nLep_;
    float lepton_pt_    [NMAXLEPTONS];
    float lepton_eta_   [NMAXLEPTONS];
    float lepton_phi_   [NMAXLEPTONS];
    float lepton_m_     [NMAXLEPTONS];
    float lepton_charge_[NMAXLEPTONS];
    float lepton_rIso_  [NMAXLEPTONS];
    int   lepton_type_  [NMAXLEPTONS];
    float lepton_dxy_   [NMAXLEPTONS];
    float lepton_dz_    [NMAXLEPTONS];
    float lepton_wp80_  [NMAXLEPTONS];
    float lepton_wp95_  [NMAXLEPTONS];
    float lepton_wp70_  [NMAXLEPTONS];
    float lepton_MVAtrig_ [NMAXLEPTONS];
    
    float Mll_, MTln_;
    
    // additional SF for electrons;
    float sf_ele_;
    
    // met kinematic
    float MET_pt_;
    float MET_phi_;
    float MET_sumEt_;
    
    // invisible particles kinematic
    float Nus_pt_;
    float Nus_phi_;
    
    // control variables
    float mH_matched_;
    float mTop_matched_;
    float mW_matched_;
    
    // jet kinematics (as passed via **jets** collection)
    int nJet_;
    float jet_pt_    [NMAXJETS];
    float jet_pt_alt_[NMAXJETS];
    float jet_eta_   [NMAXJETS];
    float jet_phi_   [NMAXJETS];
    float jet_m_     [NMAXJETS];
    float jet_csv_   [NMAXJETS];
    int jet_id_    [NMAXJETS];
    
    // number of selected hJets
    int hJetAmong_;
    int jetsAboveCut_;
    
    // number of trials
    int num_of_trials_;
    
    // number of selected jets passing CSV L,M,T
    int numBTagL_, numBTagM_, numBTagT_;
    // nummber of selected jets
    int numJets_;
    // btag likelihood ratio
    //float btag_LR_;
    
    // permutation -> jets association
    int   perm_to_jet_    [NMAXPERMUT];
    int   perm_to_jet_alt_[NMAXPERMUT];

    // permutation -> gen association
    // bLep W1 W2 bHad bH1 bH2
    // If a particular index is set, then for this permutation
    // the jet was matched to the corresponding gen-level object.
    // E.g. 110011 means that the b from the leptonic top, one of
    // the quarks from W->qq and both of the bs from H->bb were matched
    // correctly to gen-level objects for this permutation
    int   perm_to_gen_     [NMAXPERMUT];
    int   perm_to_gen_alt_ [NMAXPERMUT];

    //HEADERGEN_BRANCH_VARIABLES
    
	void make_branches(const float MH) {
        tree->Branch("counter",      &counter_,       "counter/I");
        tree->Branch("sample",       &sample,        "sample/I");
        tree->Branch("nPermut_s",    &nPermut_,       "nPermut_s/I");
        tree->Branch("nPermut_b",    &nPermut_alt_,   "nPermut_b/I");
        tree->Branch("nMassPoints",  &nMassPoints_,   "nMassPoints/I");
        tree->Branch("nTotInteg_s",  &nTotInteg_,     "nTotInteg_s/I");
        tree->Branch("nTotInteg_b",  &nTotInteg_alt_, "nTotInteg_b/I");
        tree->Branch("matchesH",     &matchesH_,      "matchesH/I");
        tree->Branch("matchesW",     &matchesW_,      "matchesW/I");
        tree->Branch("matchesT",     &matchesT_,      "matchesT/I");
        tree->Branch("matchesHAll",  &matchesHAll_,   "matchesHAll/I");
        tree->Branch("matchesWAll",  &matchesWAll_,   "matchesWAll/I");
        tree->Branch("matchesTAll",  &matchesTAll_,   "matchesTAll/I");
        tree->Branch("overlapLight", &overlapLight_,  "overlapLight/I");
        tree->Branch("overlapHeavy", &overlapHeavy_,  "overlapHeavy/I");
        tree->Branch("type",         &type_,          "type/I");
        tree->Branch("syst",         &syst_,          "syst/I");
        tree->Branch("iterations",   &iterations_,    "iterations/I");
        
        tree->Branch("nSimBs",       &nSimBs_,        "nSimBs/I");
        tree->Branch("nSimCs",       &nSimCs_,        "nSimCs/I");
        tree->Branch("nMatchSimBsOld",&nMatchSimBsOld_,"nMatchSimBsOld/I");
        tree->Branch("nMatchSimBs_v1",&nMatchSimBs_v1_,"nMatchSimBs_v1/I");
        tree->Branch("nMatchSimBs_v2",&nMatchSimBs_v2_,"nMatchSimBs_v2/I");
        tree->Branch("nMatchSimBs",  &nMatchSimBs_,    "nMatchSimBs/I");
        tree->Branch("nMatchSimCs_v1",  &nMatchSimCs_v1_,    "nMatchSimCs_v1/I");
        tree->Branch("nMatchSimCs_v2",  &nMatchSimCs_v2_,    "nMatchSimCs_v2/I");
        tree->Branch("nMatchSimCs",  &nMatchSimCs_,    "nMatchSimCs/I");
        
        tree->Branch("weight",       &weight_,        "weight/F");
        tree->Branch("weightCSV",    weightCSV_,      "weightCSV[19]/F");
        tree->Branch("SCALEsyst",    SCALEsyst_,      "SCALEsyst[3]/F");
        
        tree->Branch("weightTopPt",  &weightTopPt_,   "weightTopPt/F");
        tree->Branch("time",         &time_,          "time/F");
        tree->Branch("flag_type0",   &flag_type0_,    "flag_type0/I");
        tree->Branch("flag_type1",   &flag_type1_,    "flag_type1/I");
        tree->Branch("flag_type2",   &flag_type2_,    "flag_type2/I");
        tree->Branch("flag_type3",   &flag_type3_,    "flag_type3/I");
        tree->Branch("flag_type4",   &flag_type4_,    "flag_type4/I");
        tree->Branch("flag_type6",   &flag_type6_,    "flag_type6/I");
        tree->Branch("Vtype",        &Vtype_,         "Vtype/I");
        tree->Branch("EVENT",        &EVENT_,         "run/I:lumi/I:event/I:json/I");
        tree->Branch("nPVs",         &nPVs_,          "nPVs/I");
        tree->Branch("PUweight",     &PUweight_,      "PUweight/F");
        tree->Branch("PUweightP",    &PUweightP_,     "PUweightP/F");
        tree->Branch("PUweightM",    &PUweightM_,     "PUweightM/F");
        tree->Branch("lheNj",        &lheNj_,         "lheNj/F");
        tree->Branch("n_b",          &n_b_,           "n_b/I");
        tree->Branch("n_c",          &n_c_,           "n_c/I");
        tree->Branch("n_l",          &n_l_,           "n_l/I");
        tree->Branch("n_g",          &n_g_,           "n_g/I");
        tree->Branch("trigger",      &trigger_,       "trigger/F");
        tree->Branch("triggerErr",   &triggerErr_,    "triggerErr/F");
        tree->Branch("triggerFlags", triggerFlags_,   "triggerFlags[70]/b");
        tree->Branch("p4H",          p4H_,            "p4H[4]/F");
        tree->Branch("p4T",          p4T_,            "p4T[4]/F");
        tree->Branch("p4Tbar",       p4Tbar_,         "p4Tbar[4]/F");
        tree->Branch("ttH",          &ttH_,           "x1/F:x2/F:pdf/F:pt/F:eta/F:phi/F:m/F:me2_ttH/F:me2_ttbb/F");
        
        // marginalized over permutations (all <=> Sum_{p=0}^{nTotPermut}( mH=MH, mT=MT ) )
        tree->Branch(Form("p_%d_all_s",     int(MH)),   &probAtSgn_,           Form("p_%d_all_s/F",              int(MH)) );
        tree->Branch(Form("p_%d_all_b",     int(MH)),   &probAtSgn_alt_,       Form("p_%d_all_b/F",              int(MH)) );
        tree->Branch(Form("p_%d_all_s_ttbb",int(MH)),   &probAtSgn_ttbb_,      Form("p_%d_all_s_ttbb/F",         int(MH)) );
        tree->Branch(Form("p_%d_all_b_ttbb",int(MH)),   &probAtSgn_alt_ttbb_,  Form("p_%d_all_b_ttbb/F",         int(MH)) );
        tree->Branch(Form("p_%d_all_b_ttjj",int(MH)),   &probAtSgn_alt_ttjj_,  Form("p_%d_all_b_ttjj/F",         int(MH)) );
        tree->Branch(Form("p_%d_all_b_ttbj",int(MH)),   &probAtSgn_alt_ttbj_,  Form("p_%d_all_b_ttbj/F",         int(MH)) );
        tree->Branch(Form("p_%d_all_b_ttcc",int(MH)),   &probAtSgn_alt_ttcc_,  Form("p_%d_all_b_ttcc/F",         int(MH)) );
        
        // differential in permutations and mass value. E.g.:
        //  p_vsMH_s[0],          ..., p_vsMH_s[  nPermut-1] => prob. per-permutation and for mH = masses[0]
        //  p_vsMH_s[nPermut], ...,    p_vsMH_s[2*nPermut-1] => prob. per-permutation and for mH = masses[1]
        //  ....
        tree->Branch("p_vsMH_s",     probAtSgn_permut_,       "p_vsMH_s[nTotInteg_s]/F" );
        tree->Branch("p_vsMT_b",     probAtSgn_alt_permut_,   "p_vsMT_b[nTotInteg_b]/F");
        tree->Branch("p_vsMH_Err_s", probAtSgnErr_permut_,    "p_vsMH_Err_s[nTotInteg_s]/F" );
        tree->Branch("p_msMT_Err_b", probAtSgnErr_alt_permut_,"p_vsMT_Err_b[nTotInteg_b]/F" );
        tree->Branch("n_vsMH_s",     callsAtSgn_permut_,      "n_vsMH_s[nTotInteg_s]/I" );
        tree->Branch("n_vsMT_b",     callsAtSgn_alt_permut_,  "n_vsMT_b[nTotInteg_b]/I");
        tree->Branch("x_vsMH_s",     chi2AtSgn_permut_,       "x_vsMH_s[nTotInteg_s]/F" );
        tree->Branch("x_vsMT_b",     chi2AtSgn_alt_permut_,   "x_vsMT_b[nTotInteg_b]/F");
        
        // differential in permutation
        tree->Branch("p_tt_bb",      probAtSgn_bb_permut_,    "p_tt_bb[nPermut_s]/F");
        tree->Branch("p_tt_bj",      probAtSgn_bj_permut_,    "p_tt_bj[nPermut_b]/F");
        tree->Branch("p_tt_cc",      probAtSgn_cc_permut_,    "p_tt_cc[nPermut_b]/F");
        tree->Branch("p_tt_jj",      probAtSgn_jj_permut_,    "p_tt_jj[nPermut_b]/F");
        
        // # of mass points scanned
        tree->Branch("mH_scan",       mH_scan_,          "mH_scan[nMassPoints]/F");
        tree->Branch("mT_scan",       mT_scan_,          "mT_scan[nMassPoints]/F");
        
        // lepton kinematics
        tree->Branch("nLep",                    &nLep_,        "nLep/I");
        tree->Branch("lepton_pt",               lepton_pt_,    "lepton_pt[nLep]/F");
        tree->Branch("lepton_eta",              lepton_eta_,   "lepton_eta[nLep]/F");
        tree->Branch("lepton_phi",              lepton_phi_,   "lepton_phi[nLep]/F");
        tree->Branch("lepton_m",                lepton_m_,     "lepton_m[nLep]/F");
        tree->Branch("lepton_charge",           lepton_charge_,"lepton_charge[nLep]/F");
        tree->Branch("lepton_rIso",             lepton_rIso_,  "lepton_rIso[nLep]/F");
        tree->Branch("lepton_type",             lepton_type_,  "lepton_type[nLep]/I");
        tree->Branch("lepton_dxy",              lepton_dxy_,   "lepton_dxy[nLep]/F");
        tree->Branch("lepton_dz",               lepton_dz_,    "lepton_dz[nLep]/F");
        tree->Branch("lepton_wp80",             lepton_wp80_,  "lepton_wp80[nLep]/F");
        tree->Branch("lepton_wp95",             lepton_wp95_,  "lepton_wp95[nLep]/F");
        tree->Branch("lepton_wp70",             lepton_wp70_,  "lepton_wp70[nLep]/F");
        tree->Branch("lepton_MVAtrig",          lepton_MVAtrig_, "lepton_MVAtrig[nLep]/F");
        
        tree->Branch("Mll",                     &Mll_,         "Mll/F");
        tree->Branch("MTln",                    &MTln_,        "MTln/F");
        
        // additional electron SF
        tree->Branch("weightEle",               &sf_ele_,      "weightEle/F");
        
        // MET kinematics
        tree->Branch("MET_pt",                  &MET_pt_,    "MET_pt/F");
        tree->Branch("MET_phi",                 &MET_phi_,   "MET_phi/F");
        tree->Branch("MET_sumEt",               &MET_sumEt_, "MET_sumEt/F");
        
        // Invisible particles kinematics
        tree->Branch("Nus_pt",                  &Nus_pt_,    "Nus_pt/F");
        tree->Branch("Nus_phi",                 &Nus_phi_,   "Nus_phi/F");
        
        // jet kinematics
        tree->Branch("nJet",                    &nJet_,        "nJet/I");
        tree->Branch("jet_pt",                  jet_pt_,       "jet_pt[nJet]/F");
        tree->Branch("jet_pt_alt",              jet_pt_alt_,   "jet_pt_alt[nJet]/F");
        tree->Branch("jet_eta",                 jet_eta_,      "jet_eta[nJet]/F");
        tree->Branch("jet_phi",                 jet_phi_,      "jet_phi[nJet]/F");
        tree->Branch("jet_m",                   jet_m_,        "jet_m[nJet]/F");
        tree->Branch("jet_csv",                 jet_csv_,      "jet_csv[nJet]/F");
        tree->Branch("jet_id",                  jet_id_,       "jet_id[nJet]/I");
        tree->Branch("hJetAmong",               &hJetAmong_,   "hJetAmong/I");
        tree->Branch("jetsAboveCut",            &jetsAboveCut_,"jetsAboveCut/I");
        tree->Branch("num_of_trials",           &num_of_trials_,"num_of_trials/I");
        
        
        // Jet multiplicity
        tree->Branch("numBTagL",                &numBTagL_,    "numBTagL/I");
        tree->Branch("numBTagM",                &numBTagM_,    "numBTagM/I");
        tree->Branch("numBTagT",                &numBTagT_,    "numBTagT/I");
        tree->Branch("numJets",                 &numJets_,     "numJets/I");
        //tree->Branch("btag_LR",                 &btag_LR_,     "btag_LR/F");
        
        // Control variables
        tree->Branch("mH_matched",              &mH_matched_,   "mH_matched/F");
        tree->Branch("mTop_matched",            &mTop_matched_, "mTop_matched/F");
        tree->Branch("mW_matched",              &mW_matched_,   "mW_matched/F");
        
        // a map that associates to each permutation [p=0...nTotPermut] to the corresponding jet,
        // indexed according to the order in the jet_* collection
        //  E.g.: perm_to_jets[0] = 234567 <==> the first permutation (element '0' of p_vsMH_s/p_vsMT_b )
        //        associates element '2' of jets_* to the bLep, element '3' to W1Had, '4' to 'W2Had', '5' to bHad, and '6','7'
        //        to non-top radiation
        tree->Branch("perm_to_jet_s",             perm_to_jet_,    "perm_to_jet[nPermut_s]/I");
        tree->Branch("perm_to_gen_s" ,            perm_to_gen_,    "perm_to_gen[nPermut_s]/I");
        tree->Branch("perm_to_jet_b",             perm_to_jet_alt_,"perm_to_jet[nPermut_b]/I");
        tree->Branch("perm_to_gen_b" ,            perm_to_gen_alt_,"perm_to_gen[nPermut_b]/I");
        
		//HEADERGEN_BRANCH_CREATOR
        
    }

	void set_branch_addresses(const float MH) {
        tree->SetBranchAddress("weight", &weight_);
        tree->SetBranchAddress("time", &time_);
		
		tree->SetBranchAddress("EVENT", &EVENT_);
		tree->SetBranchAddress("jet_pt", &jet_pt_);
		tree->SetBranchAddress("jet_eta", &jet_eta_);
		tree->SetBranchAddress("jet_phi", &jet_phi_);
		tree->SetBranchAddress("jet_m", &jet_m_);
		tree->SetBranchAddress("jet_id", &jet_id_);
		tree->SetBranchAddress("lepton_pt", &lepton_pt_);
		
        tree->SetBranchAddress("lepton_rIso", &lepton_rIso_);
        tree->SetBranchAddress("numBTagL", &numBTagL_);
        tree->SetBranchAddress("numBTagM", &numBTagM_);
        tree->SetBranchAddress("numBTagT", &numBTagT_);
        tree->SetBranchAddress("numJets", &numJets_);
        //tree->SetBranchAddress("btag_LR", &btag_LR_);
		tree->SetBranchAddress("nLep", &nLep_);
		tree->SetBranchAddress("nJet", &nJet_);

		tree->SetBranchAddress(Form("p_%d_all_s",     int(MH)), &probAtSgn_);
        tree->SetBranchAddress(Form("p_%d_all_b",     int(MH)), &probAtSgn_alt_);
        tree->SetBranchAddress(Form("p_%d_all_s_ttbb",int(MH)), &probAtSgn_ttbb_);
        tree->SetBranchAddress(Form("p_%d_all_b_ttbb",int(MH)), &probAtSgn_alt_ttbb_);
        tree->SetBranchAddress(Form("p_%d_all_b_ttjj",int(MH)), &probAtSgn_alt_ttjj_);
        tree->SetBranchAddress(Form("p_%d_all_b_ttbj",int(MH)), &probAtSgn_alt_ttbj_);
        tree->SetBranchAddress(Form("p_%d_all_b_ttcc",int(MH)), &probAtSgn_alt_ttcc_);
        tree->SetBranchAddress("Vtype", &Vtype_);
        tree->SetBranchAddress("type", &type_);
        tree->SetBranchAddress("flag_type0", &flag_type0_);
        tree->SetBranchAddress("flag_type1", &flag_type1_);
        tree->SetBranchAddress("flag_type2", &flag_type2_);
        tree->SetBranchAddress("flag_type3", &flag_type3_);
        tree->SetBranchAddress("flag_type4", &flag_type4_);
        tree->SetBranchAddress("flag_type6", &flag_type6_);
        tree->SetBranchAddress("syst", &syst_);
        tree->SetBranchAddress("triggerFlags", &triggerFlags_);
        tree->SetBranchAddress("nMatchSimBs", &nMatchSimBs_);
        tree->SetBranchAddress("nMatchSimCs", &nMatchSimCs_);
        
        tree->SetBranchAddress("nPermut_s", &nPermut_);
        tree->SetBranchAddress("nPermut_b", &nPermut_alt_);
        
        tree->SetBranchAddress("perm_to_gen_s", perm_to_gen_);
        tree->SetBranchAddress("perm_to_gen_b", perm_to_gen_alt_);
        //HEADERGEN_BRANCH_SETADDRESS
	}

    void loop_initialize(void) {
        nLep_ = 0;
        nJet_ = 0;
		Vtype_ = DEF_VAL_INT;
		type_ = DEF_VAL_INT;
        SET_ZERO(lepton_pt_, NMAXLEPTONS, DEF_VAL_FLOAT);
        SET_ZERO(lepton_rIso_, NMAXLEPTONS, DEF_VAL_FLOAT);
        SET_ZERO(triggerFlags_, 70, 0);
        
        SET_ZERO(perm_to_gen_, NMAXPERMUT, 0.0);
        SET_ZERO(perm_to_gen_alt_, NMAXPERMUT, 0.0);

		numBTagL_ = DEF_VAL_INT;
		numBTagM_ = DEF_VAL_INT;
		numBTagT_ = DEF_VAL_INT;
		numJets_ = DEF_VAL_INT;
        
        nMatchSimBs_ = DEF_VAL_INT;
        nMatchSimCs_ = DEF_VAL_INT;
        
		//btag_LR_ = DEF_VAL_FLOAT;

		probAtSgn_ = DEF_VAL_FLOAT;
		probAtSgn_alt_ = DEF_VAL_FLOAT;
		probAtSgn_ttbb_ = DEF_VAL_FLOAT;
		probAtSgn_alt_ttbb_ = DEF_VAL_FLOAT;
		probAtSgn_alt_ttjj_ = DEF_VAL_FLOAT;
		probAtSgn_alt_ttbj_ = DEF_VAL_FLOAT;
		probAtSgn_alt_ttcc_ = DEF_VAL_FLOAT;
		
		flag_type0_ = DEF_VAL_INT;
		flag_type1_ = DEF_VAL_INT;
		flag_type2_ = DEF_VAL_INT;
		flag_type3_ = DEF_VAL_INT;
		flag_type4_ = DEF_VAL_INT;
		flag_type6_ = DEF_VAL_INT;
        
		nPermut_            = 0;
        nPermut_alt_        = 0;
        nTotInteg_          = 0;
        nTotInteg_alt_      = 0;
        matchesH_           = -99;
        matchesT_           = -99;
        matchesHAll_        = -99;
        matchesWAll_        = -99;
        matchesTAll_        = -99;
        overlapLight_       = -99;
        overlapHeavy_       = -99;
        type_               = -99;
        syst_               = -99;
        iterations_         = -1;

        mH_matched_         = -99.;
        mW_matched_         = -99.;
        mTop_matched_       = -99.;
        triggerErr_  = 0.;
        sf_ele_      = -99;
		
		//HEADERGEN_BRANCH_INITIALIZERS
    }

	void copy_branches(TTHTree* itree) {
        //HEADERGEN_COPY_BRANCHES
	}
};
#endif

