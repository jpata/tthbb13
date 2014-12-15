#include "FWCore/FWLite/interface/AutoLibraryLoader.h"

#include <cstdlib>
#include <iostream>
#include <fstream>
#include <map>
#include <string>
#include <algorithm>

#include "TSystem.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TH2F.h"
#include "THStack.h"
#include "TF1.h"
#include "TF2.h"
#include "TGraph.h"
#include "Math/GenVector/LorentzVector.h"
#include "TLorentzVector.h"
#include "TVectorD.h"
#include "TRandom3.h"
#include "TStopwatch.h"
#include "TMatrixT.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include "Math/GSLMCIntegrator.h"
#include "Math/IOptions.h"
#include "Math/IntegratorOptions.h"
#include "Math/AllIntegrationTypes.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TTH/TTHNtupleAnalyzer/interface/HypoEnums.hh"
#include "TTH/TTHNtupleAnalyzer/interface/tth_tree.hh"
#include "TTH/TTHNtupleAnalyzer/interface/event_interpretation.hh"
#include "TTH/MEAnalysis/interface/METree.hh"
#include "TTH/MEAnalysis/interface/btag_lr_tree.hh"
#include "TTH/MEAnalysis/interface/MECombination.h"

#include "TTH/Plotting/interface/easylogging++.h"

using namespace std;

enum SampleType {
    NOME_8TEV,
    ME_8TEV,
    NOME_13TEV,
    ME_13TEV
};

enum Process {
    TTHBB,
    TTJETS
};

enum MECategory {
    UNKNOWN_CAT,
    CAT1,
    CAT2,
    CAT3,
//    CAT6,
    CAT6ee,
    CAT6emu,
    CAT6mumu,
};

enum CutReasons {
    SYST,
    BTAG_LR,
};

MECategory assign_me_category(METree* t, SampleType st) {
    TTH::EventHypothesis vt = static_cast<TTH::EventHypothesis>(t->Vtype_);
    
    if (t->btag_LR_ >= 0.0 ) {
        if (t->type_ == 0 || (t->type_ == 3 && t->flag_type3_ > 0)) {
            return CAT1;
        }
        if (t->type_ == 1 || (t->type_ == 3 && t->flag_type3_ <= 0)) {
            return CAT2;
        }
        if (t->type_ == 2 && t->flag_type2_ <= 999) {
            return CAT3;
        }
        
        if (t->type_ == 6) {
            if (st == NOME_13TEV || ME_13TEV) {
                if (vt == TTH::EventHypothesis::mumu) {
                    return CAT6mumu;
                }
                if (vt == TTH::EventHypothesis::emu) {
                    return CAT6emu;
                }
                if (vt == TTH::EventHypothesis::ee) {
                    return CAT6ee;
                }
            }
            if (st == NOME_8TEV || ME_8TEV) {
                if (vt == TTH::EventHypothesis::mumu && t->nLep_ == 2) {
                    return CAT6mumu;
                }
                if (vt == 4 && t->nLep_ == 2) {
                    return CAT6emu;
                }
                if (vt == TTH::EventHypothesis::ee && t->nLep_ == 2) {
                    return CAT6ee;
                }
            }
            
            return UNKNOWN_CAT;
        }
    }
    
    //std::cerr << "ERROR: could not assign category type=" << t->type_ << std::endl;
    //throw std::exception();
    return UNKNOWN_CAT;
}

bool is_single_lepton(METree* t, SampleType sample_type) {
    //const int nl = t->nLep_;
    
    if( sample_type == ME_13TEV) {
        const TTH::EventHypothesis vt = static_cast<TTH::EventHypothesis>(t->Vtype_);
        return (vt==TTH::EventHypothesis::en) || (vt==TTH::EventHypothesis::mun);
    }
    else if( sample_type == NOME_8TEV || sample_type == ME_8TEV) {
        const int vt = t->Vtype_;
        return (vt == 3) || (vt == 2);
    }
    std::cerr << "ERROR: could not interpret lepton type" << std::endl;
    throw std::exception();
    return false;
}

bool is_double_lepton(METree* t, SampleType sample_type) {
    //const int nl = t->nLep_;
    
    if( sample_type == ME_13TEV) {
        const TTH::EventHypothesis vt = static_cast<TTH::EventHypothesis>(t->Vtype_);
        return (vt==TTH::EventHypothesis::emu) || (vt==TTH::EventHypothesis::mumu) || (vt==TTH::EventHypothesis::ee);
    }
    else if( sample_type == NOME_8TEV || sample_type == ME_8TEV) {
        const int vt = t->Vtype_;
        return (vt == 4) || (vt == 0) || (vt == 1);
    }
    std::cerr << "ERROR: could not interpret lepton type" << std::endl;
    throw std::exception();
    return false;
}

//1 -> H
//0 -> L
//-1 -> neither
int is_btag_lr_high_low(METree* t, MECategory cat) {
    if (cat == CAT1) {
        if (t->btag_LR_ >= 0.995) {
            return 1;
        } else if (t->btag_LR_ < 0.995 && t->btag_LR_ >= 0.96) {
            return 0;
        }
    }
    else if (cat == CAT2) {
        if (t->btag_LR_ >= 0.9925) {
            return 1;
        } else if (t->btag_LR_ < 0.9925 && t->btag_LR_ >= 0.96) {
            return 0;
        }
    }
    else if (cat == CAT3) {
        if (t->btag_LR_ >= 0.995) {
            return 1;
        } else if (t->btag_LR_ < 0.995 && t->btag_LR_ >= 0.97) {
            return 0;
        }
    }
    else if (cat == CAT6mumu || cat == CAT6ee || cat == CAT6emu) {
        if (t->btag_LR_ >= 0.925) {
            return 1;
        } else if (t->btag_LR_ < 0.925 && t->btag_LR_ >= 0.850) {
            return 0;
        }
    }
    return -1;
}

template <class T>
T* add_hist_1d(std::map<std::string, TH1*>& histmap, string hname, int b1, int b2) {
    histmap[hname] = new T(hname.c_str(), hname.c_str(), b2-b1, b1, b2);
    return (T*)histmap[hname];
}

template <class T>
T* add_hist_1d(std::map<std::string, TH1*>& histmap, string hname, double b1, double b2, int nb) {
    histmap[hname] = new T(hname.c_str(), hname.c_str(), nb, b1, b2);
    return (T*)histmap[hname];
}

template <class T>
T* add_hist_2d(std::map<std::string, TH1*>& histmap, string hname, double b11, double b21, int nb1, double b12, double b22, int nb2) {
    histmap[hname] = new T(hname.c_str(), hname.c_str(), nb1, b11, b21, nb2, b12, b22);
    return (T*)histmap[hname];
}

bool is_correct_perm(int perm, MECategory cat, Process prc) {
    if (cat==CAT1 || cat==CAT2 || cat==CAT3) {
        return ((perm == 111111) && prc==TTHBB) || ((perm == 111100) && prc==TTJETS); //
    }
    if (cat == CAT6ee || cat == CAT6emu || cat == CAT6mumu) {
        return ((perm == 100111) && prc==TTHBB) || ((perm == 100100) && prc==TTJETS);
    }
    return false;
}

enum FailReason {
	UNKNOWN_REASON,
	NO_H_B,
	NO_W_Q,
	NO_T_B,
	NO_LEPTON,
    DL_AS_SL,
	MATCHED_ME
};

TTH::EventHypothesis assing_gen_vtype(TTHTree* t) {
	std::vector<int> w_daus;
	w_daus.push_back(std::abs(t->gen_t__w_d1__id));
	w_daus.push_back(std::abs(t->gen_t__w_d2__id));
	w_daus.push_back(std::abs(t->gen_tbar__w_d1__id));
	w_daus.push_back(std::abs(t->gen_tbar__w_d2__id));
	
	int nele = std::count(w_daus.begin(), w_daus.end(), 11);
	int nmu = std::count(w_daus.begin(), w_daus.end(), 13);
	int ntau = std::count(w_daus.begin(), w_daus.end(), 15);
	
	if (nmu == 2)
		return TTH::EventHypothesis::mumu;
	if (nele == 2)
		return TTH::EventHypothesis::ee;
	if (ntau == 2)
		return TTH::EventHypothesis::tautau;
	
	if (nmu == 1 && nele == 1)
		return TTH::EventHypothesis::emu;
	
	if (nmu == 1 && ntau == 1)
		return TTH::EventHypothesis::taumu;
	
	if (nele == 1 && ntau == 1)
		return TTH::EventHypothesis::taue;
	
	if (nmu == 1)
		return TTH::EventHypothesis::mun;
	
	if (nele == 1)
		return TTH::EventHypothesis::en;

	if (ntau == 1)
		return TTH::EventHypothesis::taun;
	return TTH::EventHypothesis::nn;
}


_INITIALIZE_EASYLOGGINGPP

int main(int argc, const char* argv[])
{

    _START_EASYLOGGINGPP(argc, argv);

    gROOT->SetBatch(true);
    
    gSystem->Load("libFWCoreFWLite");
    gSystem->Load("libDataFormatsFWLite");
    
    AutoLibraryLoader::enable();
    
    PythonProcessDesc builder(argv[1]);
    const edm::ParameterSet& in = builder.processDesc()->getProcessPSet()->
    getParameter<edm::ParameterSet>("fwliteInput");
    
    //list of input samples
    const edm::VParameterSet& samples = in.getParameter<edm::VParameterSet>("samples");
    
    //limits with [first, last] events to process, indexed by full list of samples
	const std::vector<int> ev_limits = in.getParameter<std::vector<int>>("evLimits");
	const std::string outfn = in.getParameter<std::string>("outFile");

	
	const double elePt = in.getParameter<double>("elePt");
	//const double muPt = in.getParameter<double>("muPt");
	
	//const double lepton_pt_min = in.getParameter<double>("leptonPtMin");
	
    std::map<std::string, TH1*> histmap;
    
    TStopwatch sw;
    
    long n_total_entries = 0;
    double tottime = 0.0;
    for(auto& sample : samples ) {
        
        //LFN of sample to read
		const string sample_fn = sample.getParameter<string>("fileName");
		const string step1_sample_fn = sample.getUntrackedParameter<string>("step1FileName", "");
		cout << "step1 file name: " << step1_sample_fn << endl;
		
        //nickname of sample (must be unique)
		const string sample_nick = sample.getParameter<string>("nickName");
		int max_events = sample.getUntrackedParameter<int>("maxEvents", -1);
		
        //sample type, which may affect the meaning/contents of the TTrees
        const SampleType sample_type = static_cast<SampleType>(sample.getParameter<int>("type"));
        
        //sample type, which may affect the meaning/contents of the TTrees
        const Process process = static_cast<Process>(sample.getParameter<int>("process"));
        
        TH1::SetDefaultSumw2(true);
        
        //create output histograms
        const string pf = sample_nick + "_";
        TH1D* h_nj_sl = add_hist_1d<TH1D>(histmap, pf + "numJets_sl", 5, 12);
        TH1D* h_nj_dl = add_hist_1d<TH1D>(histmap, pf + "numJets_dl", 4, 12);

        TH1D* h_nt_sl = add_hist_1d<TH1D>(histmap, pf + "numBTagM_sl", 0, 8);
        TH1D* h_nt_dl = add_hist_1d<TH1D>(histmap, pf + "numBTagM_dl", 0, 8);
		
		TH1D* h_btag_lr_sl = add_hist_1d<TH1D>(histmap, pf + "btag_lr_sl", 0, 1, 20);
		TH1D* h_btag_lr_dl = add_hist_1d<TH1D>(histmap, pf + "btag_lr_dl", 0, 1, 20);
		TH1D* h_btag_lr_sl2 = add_hist_1d<TH1D>(histmap, pf + "btag_lr_sl2", 0.85, 1, 20);
		TH1D* h_btag_lr_dl2 = add_hist_1d<TH1D>(histmap, pf + "btag_lr_dl2", 0.85, 1, 20);

        TH1D* h_lep_pt_sl = add_hist_1d<TH1D>(histmap, pf + "lepton_pt_sl", 10, 400, 80);
        TH1D* h_lep1_pt_dl = add_hist_1d<TH1D>(histmap, pf + "lepton1_pt_dl", 10, 400, 80);
        TH1D* h_lep2_pt_dl = add_hist_1d<TH1D>(histmap, pf + "lepton2_pt_dl", 10, 400, 80);
        
        TH1D* h_lep_riso_sl = add_hist_1d<TH1D>(histmap, pf + "lepton_riso_sl", 0, 0.2, 40);
        TH1D* h_lep1_riso_dl = add_hist_1d<TH1D>(histmap, pf + "lepton1_riso_dl", 0, 0.2, 40);
        TH1D* h_lep2_riso_dl = add_hist_1d<TH1D>(histmap, pf + "lepton2_riso_dl", 0, 0.2, 40);
        
        
        TH1D* h_Vtype = add_hist_1d<TH1D>(histmap, pf + "Vtype", 0, 12);
		TTH::label_axis(h_Vtype->GetXaxis());
        TH1D* h_type = add_hist_1d<TH1D>(histmap, pf + "type", 0, 10);
        
        TH1D* h_cat = add_hist_1d<TH1D>(histmap, pf + "category", 0, 8);
        TH1D* h_catH = add_hist_1d<TH1D>(histmap, pf + "categoryH", 0, 8);
        TH1D* h_catL = add_hist_1d<TH1D>(histmap, pf + "categoryL", 0, 8);
        
        TH1D* h_cutreasons = add_hist_1d<TH1D>(histmap, pf + "cutreasons", 0, 20);
        TH1D* h_triggers = add_hist_1d<TH1D>(histmap, pf + "triggers", 0, 10);
        TH1D* h_proc = add_hist_1d<TH1D>(histmap, pf + "processed", 0, 2);
        
		TH2D* h_cat_btag_lr = add_hist_2d<TH2D>(histmap, pf + "cat_btag_lr", 0, 8, 8, 0, 1, 20);
		TH2D* h_cat_time = add_hist_2d<TH2D>(histmap, pf + "cat_time", 0, 8, 8, 0, 400, 20);
		//TH2D* h_cat_rad_mode = add_hist_2d<TH2D>(histmap, pf + "cat_rad_mode", 0, 8, 8, 0, 5, 5);
		//TH2D* h_cat_rad_modeH = add_hist_2d<TH2D>(histmap, pf + "catH_rad_mode", 0, 8, 8, 0, 5, 5);
		//TH2D* h_cat_rad_modeL = add_hist_2d<TH2D>(histmap, pf + "catL_rad_mode", 0, 8, 8, 0, 5, 5);
		
		TH2D* h_vtype_btag_lr = add_hist_2d<TH2D>(histmap, pf + "vtype_btag_lr", 0, 12, 12, 0, 1, 20);
		TTH::label_axis(h_vtype_btag_lr->GetXaxis());
		
        TH2D* h_nperm_s_btaglr = add_hist_2d<TH2D>(histmap, pf + "nperm_s_btag_lr", 0, 3, 3, 0.9, 1, 10);
        //TH2D* h_nperm_b_btaglr = add_hist_2d<TH2D>(histmap, pf + "nperm_b_btag_lr", 0, 3, 3, 0.9, 1, 10);
        
        TH2D* h_nperm_s_me = add_hist_2d<TH2D>(histmap, pf + "nperm_s_me", 0, 3, 3, 0.0, 1.0, 6);
        //TH2D* h_nperm_b_me = add_hist_2d<TH2D>(histmap, pf + "nperm_b_me", 0, 3, 3, 0.0, 1.0, 6);
        
        TH2D* h_nperm_s_cat = add_hist_2d<TH2D>(histmap, pf + "nperm_s_cat", 0, 3, 3, 0, 8, 8);
        //TH2D* h_nperm_b_cat = add_hist_2d<TH2D>(histmap, pf + "nperm_b_cat", 0, 3, 3, 0, 8, 8);

		TH2D* h_max_perm_s_cat = add_hist_2d<TH2D>(histmap, pf + "max_perm_s_cat", 0, 65, 65, 0, 8, 8);
		//TH2D* h_max_perm_b_cat = add_hist_2d<TH2D>(histmap, pf + "max_perm_b_cat", 0, 65, 65, 0, 8, 8);
		
		for (int i=0; i < 64; i++) {
			h_max_perm_s_cat->GetXaxis()->SetBinLabel(i+1, to_string(perm_maps::map1[i]).c_str());
			//h_max_perm_b_cat->GetXaxis()->SetBinLabel(i+1, to_string(perm_maps::map1[i]).c_str());
		}
		
		TH2D* h_matched_perm_s_cat = add_hist_2d<TH2D>(histmap, pf + "matched_perm_s_cat", 0, 7, 7, 0, 8, 8);
		TH2D* h_unmatched_perm_s_cat = add_hist_2d<TH2D>(histmap, pf + "unmatched_perm_s_cat", 0, 7, 7, 0, 8, 8);
		
		//TH2D* h_matched_perm_b_cat = add_hist_2d<TH2D>(histmap, pf + "matched_perm_b_cat", 0, 7, 7, 0, 8, 8);
		//TH2D* h_unmatched_perm_b_cat = add_hist_2d<TH2D>(histmap, pf + "unmatched_perm_b_cat", 0, 7, 7, 0, 8, 8);
		TH2D* h_failreasons_cat = add_hist_2d<TH2D>(histmap, pf + "failreasons_cat", 0, 10, 10, 0, 8, 8);
		
		
		int bidx = 1;
		for (const char* r : {
			"UNKNOWN_REASON",
			"NO_H_B",
			"NO_W_Q",
			"NO_T_B",
			"NO_LEPTON",
            "DL_AS_SL",
			"MATCHED_ME"}
		) {
			h_failreasons_cat->GetXaxis()->SetBinLabel(bidx, r);
			bidx += 1;
		}
		
		TH2D* h_unmatchedHbb_pt = add_hist_2d<TH2D>(histmap, pf + "unmatchedHbb_pt", 0, 300, 60, 0, 300, 60);
		TH2D* h_unmatchedHbb_eta = add_hist_2d<TH2D>(histmap, pf + "unmatchedHbb_eta",-5, 5, 60, -5, 5, 60);
		TH1D* h_unmatchedHbb_csv = add_hist_1d<TH1D>(histmap, pf + "unmatchedHbb_csv", 0, 1, 60);
		TH1D* h_unmatchedHbb_jetid = add_hist_1d<TH1D>(histmap, pf + "unmatchedHbb_jetid", -2, 2, 4);
		TH1D* h_unmatchedHbb_dr = add_hist_1d<TH1D>(histmap, pf + "unmatchedHbb_dr", 0, 5, 20);
		
		TH2D* h_unmatched_tb_pt = add_hist_2d<TH2D>(histmap, pf + "unmatched_tb_pt", 0, 300, 60, 0, 300, 60);
		TH2D* h_unmatched_tb_eta = add_hist_2d<TH2D>(histmap, pf + "unmatched_tb_eta",-5, 5, 60, -5, 5, 60);
		TH1D* h_unmatched_tb_csv = add_hist_1d<TH1D>(histmap, pf + "unmatched_tb_csv", 0, 1, 60);
		TH1D* h_unmatched_tb_jetid = add_hist_1d<TH1D>(histmap, pf + "unmatched_tb_jetid", -2, 2, 4);
		TH1D* h_unmatched_tb_dr = add_hist_1d<TH1D>(histmap, pf + "unmatched_tb_dr", 0, 5, 20);
		
		TH2D* h_unmatched_Wqq_pt = add_hist_2d<TH2D>(histmap, pf + "unmatched_Wqq_pt", 0, 300, 60, 0, 300, 60);
		TH2D* h_unmatched_Wqq_eta = add_hist_2d<TH2D>(histmap, pf + "unmatched_Wqq_eta",-5, 5, 60, -5, 5, 60);
		TH1D* h_unmatched_Wqq_csv = add_hist_1d<TH1D>(histmap, pf + "unmatched_Wqq_csv", 0, 1, 60);
		TH1D* h_unmatched_Wqq_jetid = add_hist_1d<TH1D>(histmap, pf + "unmatched_Wqq_jetid", -2, 2, 4);
		TH1D* h_unmatched_Wqq_dr = add_hist_1d<TH1D>(histmap, pf + "unmatched_Wqq_dr", 0, 5, 20);
		TH1D* h_unmatched_Wqq_id = add_hist_1d<TH1D>(histmap, pf + "unmatched_Wqq_id", 0, 25, 25);
		
		TH2D* h_unmatched_lepton_pt = add_hist_2d<TH2D>(histmap, pf + "unmatched_lepton_pt", 0, 300, 60, 0, 300, 60);
		TH2D* h_unmatched_lepton_eta = add_hist_2d<TH2D>(histmap, pf + "unmatched_lepton_eta", -5, 5, 60, -5, 5, 60);
		TH1D* h_unmatched_lepton_dr = add_hist_1d<TH1D>(histmap, pf + "unmatched_lepton_dr", 0, 5, 20);
		TH2D* h_unmatched_lepton_id = add_hist_2d<TH2D>(histmap, pf + "unmatched_lepton_id", 0, 20, 20, 0, 20, 20);
		
		TH2D* h_nlep_gen_reco = add_hist_2d<TH2D>(histmap, pf + "nlep_gen_reco", 0, 3, 3, 0, 3, 3);

//		for (int i=1; i < 7; i++) {
//			for (auto* p : {h_matched_perm_s_cat, h_unmatched_perm_s_cat, h_matched_perm_b_cat, h_unmatched_perm_b_cat}) {
//				p->GetXaxis()->SetBinLabel(i, perm_maps::positions[i-1]);
//			}
//		}
		
        TH2D* h_vtype_cat = add_hist_2d<TH2D>(histmap, pf + "vtype_cat", 0, 12, 12, 0, 8, 8);
		TH2D* h_gvtype_cat = add_hist_2d<TH2D>(histmap, pf + "gen_vtype_cat", 0, 12, 12, 0, 8, 8);
		TH2D* h_gvtype_vtype = add_hist_2d<TH2D>(histmap, pf + "gen_vtype_reco_vtype", 0, 12, 12, 0, 12, 12);
		TH2D* h_unmatched_gvtype_vtype = add_hist_2d<TH2D>(histmap, pf + "unmatched_gen_vtype_reco_vtype", 0, 12, 12, 0, 12, 12);
		TTH::label_axis(h_gvtype_cat->GetXaxis());
		TTH::label_axis(h_gvtype_vtype->GetXaxis());
		TTH::label_axis(h_gvtype_vtype->GetYaxis());
		TTH::label_axis(h_unmatched_gvtype_vtype->GetXaxis());
		TTH::label_axis(h_unmatched_gvtype_vtype->GetYaxis());

        TH2D* h_btag_lr_nmatched_s = add_hist_2d<TH2D>(histmap, pf + "btag_lr_nmatched_s", 0.0, 1, 20, 0, 5, 5);
        TH2D* h_btag_lr_nmatched_b = add_hist_2d<TH2D>(histmap, pf + "btag_lr_nmatched_b", 0.0, 1, 20, 0, 5, 5);
		
        TH2D* h_cat_discr = 0;
        if (sample_type == ME_8TEV || sample_type == ME_13TEV) {
            h_cat_discr = add_hist_2d<TH2D>(histmap, pf + "cat_discr", 0, 8, 8, 0, 1, 6);
        }
        
        //cout << "sample " << sample_fn << " type " << sample_type << endl;
        LOG(INFO) << "sample " << sample_fn << " type " << sample_type;
        TFile* tf = new TFile(sample_fn.c_str());
        if (tf==0 || tf->IsZombie()) {
            std::cerr << "ERROR: could not open file " << sample_fn << " " << tf << std::endl;
            throw std::exception();
        }
		TFile* tf2 = 0;
		bool has_step1_tree = false;
		if (step1_sample_fn.size() > 0) {
			tf2 = new TFile(step1_sample_fn.c_str());
			if (tf2==0 || tf->IsZombie()) {
				std::cerr << "ERROR: could not open file " << sample_fn << " " << tf << std::endl;
				throw std::exception();
			}
			has_step1_tree = true;
		}
		
        //create ME TTree and branch variables
        METree t((TTree*)(tf->Get("tree")));
        std::cout << "T1 entries " << t.tree->GetEntries() << std::endl;
		
		TTHTree* t2 = 0;

        BTagLRTree* btag_tree = new BTagLRTree((TTree*)(tf->Get("btag_lr")));
        btag_tree->set_branch_addresses();
		
		
        map<tuple<int,int, int>, int> event_map;
        map<tuple<int,int, int>, vector<int>> btag_lr_event_map;
		if (has_step1_tree) {
		//create ME TTree and branch variables
			t2 = new TTHTree((TTree*)tf2->Get("tthNtupleAnalyzer/events"));
			std::cout << "T2 entries " << t2->tree->GetEntries() << std::endl;
			t2->set_branch_addresses();
			
			//assert(t.tree->GetEntries() == t2->tree->GetEntries());
			has_step1_tree = true;
			
			t2->tree->SetBranchStatus("*", false);
			t2->tree->SetBranchStatus("event__*", true);

			for (int entry = 0; entry < t2->tree->GetEntries(); entry++) {
				t2->tree->GetEntry(entry);
                const auto k = make_tuple(t2->event__run, t2->event__lumi, t2->event__id);
				event_map[k] = entry;
			}
			t2->tree->SetBranchStatus("*", true);
		}

        for (int entry = 0; entry < btag_tree->tree->GetEntries(); entry++) {
            btag_tree->tree->GetEntry(entry);

            const auto k = make_tuple(btag_tree->event_run, btag_tree->event_lumi, btag_tree->event_id);
            if (btag_lr_event_map.find(k) == btag_lr_event_map.end()) {
                btag_lr_event_map[k] = vector<int>();
            }

            btag_lr_event_map[k].push_back(entry);
        }
        t2->tree->SetBranchStatus("*", true);
		
        //attach branches with MH=125 (for ME branch names)
        t.set_branch_addresses(125.0);
		
        //count number of bytes read
        long nbytes = 0;
		if (max_events<0) {
			max_events =t.tree->GetEntries();
		}
		
		//if using less than full events, calculate weight modification to compensate
		double wratio = t.tree->GetEntries() / max_events;
		
        for (int entry = 0 ;entry < max_events; entry++) {
            n_total_entries += 1;
            
            if(n_total_entries % 1000000 == 0) {
                sw.Stop();
                float t = sw.CpuTime();
                tottime += t;
                std::cout << n_total_entries << " " << t << " "
                << tottime << std::endl;
                sw.Start();
            }
            
            //check if we are within limits
            if ((n_total_entries < ev_limits[0]) ||
                (ev_limits[1]>ev_limits[0] && n_total_entries > ev_limits[1])
                ) {
                //std::cout << "stopping loop with " << n_total_entries << " "
                //<< i << " in " << sample_nick << std::endl;
                continue;
            }
            
            h_proc->Fill(1);
            //zero all branch variables
            t.loop_initialize();
            nbytes += t.tree->GetEntry(entry);

            assert(t.EVENT_.event != 0);

            const auto event_key = make_tuple(t.EVENT_.run, t.EVENT_.lumi, t.EVENT_.event);
            const int idx = event_map[event_key];
            assert(idx >= 0);

			if (has_step1_tree) {
				t2->loop_initialize();
                //cout << t.EVENT_.run << " " << t.EVENT_.lumi << " " << t.EVENT_.event << " " << idx << endl;
                int nb = t2->tree->GetEntry(idx);
				if (nb <= 0) {
					cerr << "failed to read entry " << entry << endl;
					throw exception();
				}
				nbytes += nb;
                //LOG(DEBUG) << "event " << " " << idx << " " << t.EVENT_.event << " " << t2->event__id;
				assert(t.EVENT_.run == t2->event__run);
				assert(t.EVENT_.lumi == t2->event__lumi);
				assert(t.EVENT_.event == t2->event__id);
			}
			
			//keep only nominal events
			if (!(t.syst_ == 0)) {
				h_cutreasons->Fill(SYST+1);
				continue;
			}
			
            const double w = t.weight_ * wratio;

			Event* event = 0;
			if (has_step1_tree) {
				event = t2->as_event();
                assert(event != 0);
			}
			
            //list of pointers to original particles in step1 TTree
			vector<Particle*> orig_jets;
			vector<Particle*> orig_leptons;

            //association between METree->TTHTree jet indices
            map<int, int> jet_map;


            //reco vtype
            const TTH::EventHypothesis vt = static_cast<TTH::EventHypothesis>(t.Vtype_);
            
            //assign SL/DL hypothesis
            const bool is_sl = is_single_lepton(&t, sample_type);
            const bool is_dl = is_double_lepton(&t, sample_type);
            MECategory cat = assign_me_category(&t, sample_type);

            if (!((is_sl || is_dl))) {
                continue;
            }

            //keep only events for which Blr was calculated
            if (!(t.btag_LR_ >= 0)) {
                h_cutreasons->Fill(BTAG_LR+1);
                continue;
            }
			
			if (has_step1_tree) {
				//find lepton from original collection
				for (int _i=0; _i < t.nLep_; _i++) {
					for (auto* p : event->leptons) {
						if (p->p4.Pt()>0 && std::abs(p->p4.Pt() - t.lepton_pt_[_i]) < 0.1) {
							orig_leptons.push_back(p);
							break;
						}
					}
				}
				assert(orig_leptons.size()==1 || orig_leptons.size()==2);
			}
			
			if (has_step1_tree) {
				//find jet from original collection
				//cout << "looping over " << t.nJet_ << " jets" << endl;
				for (int _i=0; _i < t.nJet_; _i++) {
					Particle* matched = 0;
                    int _j = 0;
					for (auto* p : event->jets) {
                        //cout << p->p4.Pt() << " " << t.jet_pt_[_i] << endl;
						if (p->p4.Pt()>0 && std::abs(p->p4.Pt() - t.jet_pt_[_i]) < 0.5) {
							//cout << "matched jet " << p << endl;
							matched = p;
							break;
						}
                        _j += 1;
					}
					if (matched) {
						//cout << "matched jet with idx " << matched->idx << endl;
						orig_jets.push_back(matched);
                        jet_map[_i] = _j;
					}
				}

                //cout << vt << " " << is_sl << " " << is_dl << " " << cat << endl;
                //LOG(DEBUG) << "event " << is_sl << " " << is_dl << " " << t.nJet_ << " " << t.numJets_ << " " << t.btag_LR_;

                assert(orig_jets.size()>0);

                //loop over btag LR permutations corresponding to event
                //LOG(DEBUG) << "perm 0 " << max_perm[0] << " " << max_perm_prob[0] << " " << has_match_map[0];
                //LOG(DEBUG) << "perm 1 " << max_perm[1] << " " << max_perm_prob[1] << " " << has_match_map[1];
			}



			//Single lepton cuts
            if (is_sl) {
				const float lep_pt1 = t.lepton_pt_[0];
				//const float lep_id = t.lepton_id_[0];
                h_lep_pt_sl->Fill(lep_pt1, w);
				
				if (vt == TTH::EventHypothesis::en) {
					if (elePt>0 && lep_pt1<elePt) {
						continue;
					}
				}
                
                h_nt_sl->Fill(t.numBTagM_, w);
                if (t.numBTagM_ >= 3) {
                    h_nj_sl->Fill(t.numJets_, w);
                }
                
                h_lep_riso_sl->Fill(t.lepton_rIso_[0], w);
				h_btag_lr_sl->Fill(t.btag_LR_, w);
				h_btag_lr_sl2->Fill(t.btag_LR_, w);
            }
			
            //dilepton cuts
            if (is_dl) {
                const float lep_pt1 = t.lepton_pt_[0];
                h_lep1_pt_dl->Fill(lep_pt1, w);
                const float lep_pt2 = t.lepton_pt_[1];
                h_lep2_pt_dl->Fill(lep_pt2, w);
				
				if (vt == TTH::EventHypothesis::emu || vt == TTH::EventHypothesis::ee || vt == TTH::EventHypothesis::taue) {
					if (elePt>0 && (lep_pt1<elePt)) {
						continue;
					}
				}
				
                h_nt_dl->Fill(t.numBTagM_, w);

                if (t.numBTagM_ >= 2) {
                    h_nj_dl->Fill(t.numJets_, w);
                }
                
                h_lep1_riso_dl->Fill(t.lepton_rIso_[0], w);
                h_lep2_riso_dl->Fill(t.lepton_rIso_[1], w);
				h_btag_lr_dl->Fill(t.btag_LR_, w);
				h_btag_lr_dl2->Fill(t.btag_LR_, w);
            }


            map<int, int> max_perm;
            map<int, double> max_perm_prob;
            map<int, int> has_match_map;

            max_perm[0] = -1.0;
            max_perm[1] = -1.0;
            for (auto _idx : btag_lr_event_map[event_key]) {
                btag_tree->loop_initialize();
                btag_tree->tree->GetEntry(_idx);

                int n_matched = 0;
                
                int id_b1 = btag_tree->id_b1;
                n_matched += abs(id_b1)==5 ? 1 : 0;
                
                int id_b2 = btag_tree->id_b2;
                n_matched += abs(id_b2)==5 ? 1 : 0;

                int id_bHad = btag_tree->id_bHad;
                n_matched += abs(id_bHad)==5 ? 1 : 0;

                int id_bLep = btag_tree->id_bLep;
                n_matched += abs(id_bLep)==5 ? 1 : 0;

                //LOG(DEBUG) << "perm " << btag_tree->permutation << " " << btag_tree->p_pos << " " << id_b1 << " " << id_b2 << " " << id_bHad << " " << id_bLep;

                if (max_perm_prob[btag_tree->hypo] < btag_tree->p_pos) {
                    max_perm_prob[btag_tree->hypo] = btag_tree->p_pos;
                    max_perm[btag_tree->hypo] = btag_tree->permutation;
                    has_match_map[btag_tree->hypo] = n_matched;
                }
            }

            h_btag_lr_nmatched_s->Fill(t.btag_LR_, has_match_map[0], w);
            h_btag_lr_nmatched_b->Fill(t.btag_LR_, has_match_map[1], w);
			
			//get trigger flags
			const bool* trf = t.triggerFlags_;
			
			//#    #// OR of four trigger paths:  "HLT_Mu40_eta2p1_v.*", "HLT_IsoMu24_eta2p1_v.*", "HLT_Mu40_v.*",  "HLT_IsoMu24_v.*"
			//#    #int trigVtype2 =  (Vtype==2 && ( triggerFlags[22]>0 || triggerFlags[23]>0 || triggerFlags[14]>0 ||triggerFlags[21]>0 ));
			//#    #// OR of two trigger paths:   "HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v.*", "HLT_Ele27_WP80_v.*"
			//#    #int trigVtype3 =  (Vtype==3 &&  triggerFlags[44]>0 );⇥␣
			//#    # // OR of four trigger paths:  "HLT_Mu40_eta2p1_v.*", "HLT_IsoMu24_eta2p1_v.*", "HLT_Mu40_v.*",  "HLT_IsoMu24_v.*"
			//#    #int trigVtype0 =  (Vtype==0 && ( triggerFlags[22]>0 || triggerFlags[23]>0 || triggerFlags[14]>0 ||triggerFlags[21]>0 ));
			//#    #// OR of two trigger paths:    "HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v.*",
			//
			h_triggers->Fill(0.0, w);
			bool trig_mu = trf[22]==1 || trf[23]==1 || trf[14]==1 || trf[21]==1;
			bool trig_ele = trf[44]==1;
			if (trig_mu) {
				h_triggers->Fill(1.0, w);
			}
			if (trig_ele) {
				h_triggers->Fill(2.0, w);
			}
			//std::cout << trig_mu << std::endl;
			
			//            if (i<10) {
			//                std::cout << "triggerflags ";
			//                for (int j=0;j<70;j++)
			//                    std::cout << trf[j];
			//                std::cout << endl;
			//            }
						
            h_Vtype->Fill(t.Vtype_, w);
            h_type->Fill(t.type_, w);
			TTH::EventHypothesis vt2 = TTH::EventHypothesis::UNKNOWN_HYPO;

			if (has_step1_tree) {
				vt2 = assing_gen_vtype(t2);
				h_gvtype_vtype->Fill(vt2, t.Vtype_, w);
				h_gvtype_cat->Fill(vt2, cat, w);
			}
			
            //h_gvtype_vtype->Fill(gen_hypo(std::abs(t.gen_))
			h_cat_btag_lr->Fill(cat, t.btag_LR_, w);
			h_vtype_btag_lr->Fill(t.Vtype_, t.btag_LR_, w);
			
            //passes btag LR cut
            int btag_lr_cat = is_btag_lr_high_low(&t, cat);
			
			
			//H
            if (btag_lr_cat == 1) {
                h_catH->Fill(cat, w);
				//h_cat_rad_modeH->Fill(cat, rad_mode, w);
			//L
            } else if (btag_lr_cat == 0) {
                h_catL->Fill(cat, w);
				//h_cat_rad_modeL->Fill(cat, rad_mode, w);
            }
			
			//H or L
			if (btag_lr_cat >= 0) {
				h_cat->Fill(cat, w);
				h_vtype_cat->Fill(t.Vtype_, cat, w);
				h_cat_time->Fill(cat, t.time_, w);

				//h_cat_rad_mode->Fill(cat, rad_mode, w);
			}
			
            if (btag_lr_cat == 1 && (sample_type == ME_8TEV || sample_type == ME_13TEV)) {
                double me_discr = t.probAtSgn_ /
                (t.probAtSgn_ + 0.02 * t.probAtSgn_alt_);
                
                if (me_discr > 1.0)
                    me_discr = 1.0;
                if (me_discr < 0.0)
                    me_discr = 0.0;
                if (me_discr != me_discr)
                    me_discr = 0.0;
                
                if (btag_lr_cat == 1) {
                    h_cat_discr->Fill(cat, me_discr, w);
                }
				
				//number of events with correct permutation, signal and background hypo
                int n_correct_perm_s = 0;
                //int n_correct_perm_b = 0;
				
				//keep track of the best permutation (most matches)
				int best_perm = 0;
				int n_best_perm = 0;

                for (int np=0; np<t.nPermut_; np++) {
					const int perm = t.perm_to_gen_[np];
                    if (is_correct_perm(perm, cat, process)) {
                        n_correct_perm_s += 1;
						h_failreasons_cat->Fill(FailReason::MATCHED_ME, cat, w);
						
						if (has_step1_tree) {
							h_unmatched_gvtype_vtype->Fill(vt2, t.Vtype_, w);
						}
                    }
					
					int _n = perm_maps::count_matched(perm);
					if (_n > n_best_perm) {
						n_best_perm = _n;
						best_perm = perm;
					}
                }
				h_max_perm_s_cat->Fill(perm_maps::map2[best_perm], cat, w);
				
				for (int i=1;i<7;i++) {
					if (perm_maps::has_n(best_perm, i)) {
						h_matched_perm_s_cat->Fill(i - 1, cat, w);
					} else {
						h_unmatched_perm_s_cat->Fill(i - 1, cat, w);
					}
				}
				
                
				//H
                if (btag_lr_cat == 1) {
                    h_nperm_s_btaglr->Fill(n_correct_perm_s, t.btag_LR_, w);
                    //h_nperm_b_btaglr->Fill(n_correct_perm_b, t.btag_LR_, w);
					
                    h_nperm_s_me->Fill(n_correct_perm_s, me_discr, w);
                    //h_nperm_b_me->Fill(n_correct_perm_b, me_discr, w);
                    
                    h_nperm_s_cat->Fill(n_correct_perm_s, cat, w);
                    //h_nperm_b_cat->Fill(n_correct_perm_b, cat, w);
					
					//find the spectra of the H->bb b quarks which are not matched to jets
					if (has_step1_tree && !is_undef(t2->gen_b__pt) && perm_maps::higgs_b_missed(best_perm)) {

                        bool filled_fail = false; 
						for (auto* p : event->higgs_decays) {
							double min_dr = 100.0;
							Particle* nearest_match = 0;
							bool has_match = false;
							for (auto* j : orig_jets) {
								double dr = j->p4.DeltaR(p->p4);
								if (dr < min_dr) {
									min_dr = dr;
									nearest_match = j;
								}
								//cout << dr << endl;
								if (dr < 0.3) {
									has_match = true;
									break;
								}
							}
							if (!has_match) {
                                assert(nearest_match != 0);
								h_unmatchedHbb_pt->Fill(nearest_match->p4.Pt(), p->p4.Pt(), w);
								if (p->p4.Pt() > 30) {
                                    if (!filled_fail) {
									   h_failreasons_cat->Fill(FailReason::NO_H_B, cat, w);
                                       filled_fail = true;
                                    }
									h_unmatchedHbb_eta->Fill(nearest_match->p4.Eta(), p->p4.Eta(), w);
									float csvval = nearest_match->idx >= 0 ? t2->jet__bd_csv[nearest_match->idx] : -1;
									if (csvval < 0) {
										csvval = 0;
									}
									h_unmatchedHbb_csv->Fill(csvval, w);
									h_unmatchedHbb_jetid->Fill(nearest_match->idx >= 0 ? t2->jet__jetId[nearest_match->idx] : -1, w);
									h_unmatchedHbb_dr->Fill(min_dr, w);
								}
							}
						}
					}
					
					if (has_step1_tree && perm_maps::top_b_missed(best_perm)) {
						
						if (is_undef(t2->gen_t__b__pt) || is_undef(t2->gen_tbar__b__pt)) {
							cerr << "undefined top b pt" << endl;
							continue;
						}
						Particle p1(t2->gen_t__b__pt, t2->gen_t__b__eta, t2->gen_t__b__phi, t2->gen_t__b__mass, 5);
						Particle p2(t2->gen_tbar__b__pt, t2->gen_tbar__b__eta, t2->gen_tbar__b__phi, t2->gen_tbar__b__mass, -5);

                        bool filled_fail = false;
						
						for (auto* p : {&p1, &p2}) {
							
							double min_dr = 100.0;
							Particle* nearest_match = 0;
							bool has_match = false;
							
							int ij = 0;
							for (auto* j : orig_jets) {
								
								//cout << t2->jet__pt[ij] << " " << t2->jet__eta[ij] << " " << t2->jet__phi[ij] << " " << t2->jet__mass[ij] << endl;
								ij++;
								double dr = j->p4.DeltaR(p->p4);
								
								if (dr < 0.3 && dr < min_dr) {
									has_match = true;
									break;
								}
								
								if (dr < min_dr) {
									min_dr = dr;
									nearest_match = j;
								}
							}
							
							if (!has_match) {
                                assert(nearest_match != 0);
								//cout << "tb " << t.EVENT_.run << " " << t.EVENT_.lumi << " " << t.EVENT_.event << endl;
                                if (!filled_fail) {
                                   h_failreasons_cat->Fill(FailReason::NO_T_B, cat, w);
                                   filled_fail = true;
                                }
								h_unmatched_tb_pt->Fill(nearest_match->p4.Pt(), p->p4.Pt(), w);
								
								if (p->p4.Pt() > 30 ) {
									h_unmatched_tb_eta->Fill(nearest_match->p4.Eta(), p->p4.Eta(), w);
									float csvval = nearest_match->idx >= 0 ? t2->jet__bd_csv[nearest_match->idx] : -1;
									if (csvval < 0) {
										csvval = 0;
									}
									h_unmatched_tb_csv->Fill(csvval, w);
									h_unmatched_tb_jetid->Fill(nearest_match->idx >= 0 ? t2->jet__jetId[nearest_match->idx] : -1, w);
									h_unmatched_tb_dr->Fill(min_dr, w);
								}
							}
						}
					}
					
					if ((cat == CAT1 || cat == CAT2 || cat == CAT3 ) && has_step1_tree && perm_maps::w_q_missed(best_perm)) {
						int id1 = std::abs(t2->gen_t__w_d1__id);
						int id2 = std::abs(t2->gen_tbar__w_d1__id);

                        bool filled_fail = false;
						
                        if (is_undef(id1) || is_undef(id2)) {
                            cerr << "top undefined" << endl;
                            continue;
                        }
						Particle* p1 = 0;
						Particle* p2 = 0;
						//t is hadronic
						if (id1>0 && id1 < 10) {
							p1 = new Particle(t2->gen_t__w_d1__pt, t2->gen_t__w_d1__eta, t2->gen_t__w_d1__phi, t2->gen_t__w_d1__mass, t2->gen_t__w_d1__id);
							p2 = new Particle(t2->gen_t__w_d2__pt, t2->gen_t__w_d2__eta, t2->gen_t__w_d2__phi, t2->gen_t__w_d2__mass, t2->gen_t__w_d2__id);
						}
						//tbar is hadronic
						else if (id2>0 && id2 < 10) {
							p1 = new Particle(t2->gen_tbar__w_d1__pt, t2->gen_tbar__w_d1__eta, t2->gen_tbar__w_d1__phi, t2->gen_tbar__w_d1__mass, t2->gen_tbar__w_d1__id);
							p2 = new Particle(t2->gen_tbar__w_d2__pt, t2->gen_tbar__w_d2__eta, t2->gen_tbar__w_d2__phi, t2->gen_tbar__w_d2__mass, t2->gen_tbar__w_d2__id);
						} else {
//							LOG(ERROR) << "SL event but no hadronic W " << id1 << " " << id2;
                            h_failreasons_cat->Fill(FailReason::DL_AS_SL, cat, w);

							continue;
						}
						
						for (auto* p : {p1, p2}) {
							
							double min_dr = 100.0;
							Particle* nearest_match = 0;
							bool has_match = false;
							
							int ij = 0;
							for (auto* j : orig_jets) {
								
								//cout << t2->jet__pt[ij] << " " << t2->jet__eta[ij] << " " << t2->jet__phi[ij] << " " << t2->jet__mass[ij] << endl;
								ij++;
								double dr = j->p4.DeltaR(p->p4);
								
								if (dr < 0.3 && dr < min_dr) {
									has_match = true;
									break;
								}
								
								if (dr < min_dr) {
									min_dr = dr;
									nearest_match = j;
								}
							}
							
							if (!has_match) {
                                assert(nearest_match != 0);
								//cout << "tb " << t.EVENT_.run << " " << t.EVENT_.lumi << " " << t.EVENT_.event << endl;
                                if (!filled_fail) {
                                   h_failreasons_cat->Fill(FailReason::NO_W_Q, cat, w);
                                   filled_fail = true;
                                }
								h_unmatched_Wqq_pt->Fill(nearest_match->p4.Pt(), p->p4.Pt(), w);
								
								if (p->p4.Pt() > 30) {
									h_unmatched_Wqq_eta->Fill(nearest_match->p4.Eta(), p->p4.Eta(), w);
									float csvval = nearest_match->idx >= 0 ? t2->jet__bd_csv[nearest_match->idx] : -1;
									if (csvval < 0) {
										csvval = 0;
									}
									h_unmatched_Wqq_csv->Fill(csvval, w);
									h_unmatched_Wqq_jetid->Fill(nearest_match->idx >= 0 ? t2->jet__jetId[nearest_match->idx] : -1, w);
									h_unmatched_Wqq_id->Fill(std::abs(p->id), w);
									h_unmatched_Wqq_dr->Fill(min_dr, w);
								}
							}
						}
						delete p1;
						delete p2;
					}
					
					//check if lepton correctly identified
					if (has_step1_tree) {
						int nlep = 0;
						
                        bool filled_fail = false;
						int nele = 0, nmu = 0, ntau = 0;
						for (auto* p : event->top_decays) {
							
							double min_dr = 100.0;
							Particle* nearest_match = 0;
							bool has_match = false;
							
							
							int abs_id = std::abs(p->id);
							
							if (abs_id == 11) {
								nele += 1;
							}
							if (abs_id == 13) {
								nmu += 1;
							}
							if (abs_id == 15) {
								ntau += 1;
							}
							
							//leptons
							if (abs_id == 11 || abs_id == 13 || abs_id == 15) {
								nlep += 1;
								
								for (auto* l : orig_leptons) {
									double dr = l->p4.DeltaR(p->p4);
									
									if (dr < 0.3 && dr < min_dr) {
										has_match = true;
									}
									
									if (dr < min_dr) {
										min_dr = dr;
										nearest_match = l;
									}
								}
								
								if (!has_match) {
                                    assert(nearest_match != 0);
									//cout << "lepton " << t.EVENT_.run << " " << t.EVENT_.lumi << " " << t.EVENT_.event << endl;
                                    if (!filled_fail) {
                                       h_failreasons_cat->Fill(FailReason::NO_LEPTON, cat, w);
                                       filled_fail = true;
                                    }

									h_unmatched_lepton_pt->Fill(nearest_match->p4.Pt(), p->p4.Pt(), w);
									h_unmatched_lepton_eta->Fill(nearest_match->p4.Eta(), p->p4.Eta(), w);
									h_unmatched_lepton_dr->Fill(min_dr, w);
									h_unmatched_lepton_id->Fill(abs_id, std::abs(nearest_match->id), w);
								}
							}
						}
						
						h_nlep_gen_reco->Fill(nlep, t.nLep_, w);
					}
                }
				
                
                h_proc->Fill(2);
            }
		
			delete event;
        } //entries
        
        std::cout << "read " << nbytes/1024/1024 << " Mb" << std::endl;
        std::cout << "processed " << n_total_entries << " in "
        << tottime << " seconds" << std::endl ;
        tf->Close();
        
    } //samples
    
    TFile* outfile = new TFile(outfn.c_str(), "RECREATE");
    outfile->cd();
    
    for(auto& kv : histmap) {
        const std::string& k = kv.first;
        TH1* h = kv.second;
        h->SetDirectory(outfile);
        cout << "saving " << k << " " << h->Integral() << endl;
    }
    
    outfile->Write();
    outfile->Close();
    
    
}