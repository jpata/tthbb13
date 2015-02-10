#ifndef HISTOGRAMS_STEP2_H
#define HISTOGRAMS_STEP2_H

#include <string>
#include "TH1D.h"
#include "TH2D.h"
#include <map>

#include "TTH/Plotting/interface/joosep/Sample.h"

//Skip to avoid multuple definition
//#include "TTH/TTHNtupleAnalyzer/interface/HypoEnums.hh"
//#include "TTH/MEAnalysis/interface/MECombination.h"

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
    LEPTON
};

enum FailReason {
	UNKNOWN_REASON,
	NO_H_B,
	NO_W_Q,
	NO_T_B,
	NO_LEPTON,
    DL_AS_SL,
	MATCHED_ME
};

//FIXME: manual fwd declaration instead of
//#include "TTH/TTHNtupleAnalyzer/interface/HypoEnums.hh"
//void TTH::label_axis(TAxis* ax);


class Histograms {

public:
	std::map<std::string, TH1*> histmap;

	TH1D *h_nj_sl, *h_nj_dl, *h_nt_sl, *h_nt_dl;
	TH1D *h_btag_lr_sl, *h_btag_lr_dl, *h_btag_lr_sl2, *h_btag_lr_dl2;
	TH1D *h_lep_pt_sl, *h_lep1_pt_dl, *h_lep2_pt_dl;

	TH1D *h_lep_riso_sl, *h_lep1_riso_dl, *h_lep2_riso_dl;

	TH1D *h_Vtype, *h_type, *h_cat, *h_catH, *h_catL;

	TH1D *h_cutreasons, *h_triggers, *h_proc;

	TH2D *h_cat_btag_lr, *h_cat_time, *h_vtype_btag_lr;

	TH2D *h_nperm_s_btaglr, *h_nperm_s_me, *h_nperm_s_cat;
	TH2D *h_max_perm_s_cat;

	TH2D *h_failreasons_cat;

	TH2D *h_unmatched_Hbb_pt, *h_unmatched_Hbb_eta;
	TH1D *h_unmatched_Hbb_csv, *h_unmatched_Hbb_jetid, *h_unmatched_Hbb_dr;
	TH2D *h_unmatched_tb_pt, *h_unmatched_tb_eta;

	TH1D *h_unmatched_tb_csv, *h_unmatched_tb_jetid, *h_unmatched_tb_dr;
	TH2D *h_unmatched_Wqq_pt, *h_unmatched_Wqq_eta;
	TH1D *h_unmatched_Wqq_csv, *h_unmatched_Wqq_jetid, *h_unmatched_Wqq_dr, *h_unmatched_Wqq_id;

	TH1D *h_unmatched_lepton_dr;
	TH2D *h_unmatched_lepton_pt, *h_unmatched_lepton_eta, *h_unmatched_lepton_id;

	TH2D *h_vtype_cat, *h_gvtype_cat, *h_gvtype_vtype, *h_unmatched_gvtype_vtype;

	TH2D *h_btag_lr_nmatched_s;
	TH2D *h_btag_lr_nmatched_b;

	TH1D* h_discr;
	TH2D* h_cat_discr;
	TH2D* h_nlep_gen_reco;

	TH1D *h_nmatched_wqq, *h_nmatched_wqq_selected; 
	TH1D *h_unmatched_wqq_pt, *h_unmatched_wqq_eta;
	TH1D *h_matched_wqq_pt, *h_matched_wqq_eta;
	TH2D *h_nmatched_tagging_wqq;

	TH2D *h_btag_lr, *h_btag_lr2, *h_btag_lr3, *h_btag_lr4;
	TH1D *h_radmode;
	TH2D *h_catH_radmode, *h_catL_radmode, *h_cat_radmode;

    TH2D *h_rad_lr_default;
    TH2D *h_rad_lr_cc;
    TH2D *h_rad_lr_cc_bj;
    TH2D *h_rad_lr_cc_bj_w;
    TH2D *h_rad_lr_wcq;


	Histograms(const std::string pf, SampleType sample_type);

	template <class T>
	T* add_hist_1d(std::map<std::string, TH1*>& histmap, std::string hname, int b1, int b2) {
	    histmap[hname] = new T(hname.c_str(), hname.c_str(), b2 - b1, b1, b2);
	    return (T*)histmap[hname];
	}

	template <class T>
	T* add_hist_1d(std::map<std::string, TH1*>& histmap, std::string hname, double b1, double b2, int nb) {
	    histmap[hname] = new T(hname.c_str(), hname.c_str(), nb, b1, b2);
	    return (T*)histmap[hname];
	}

	template <class T>
	T* add_hist_2d(std::map<std::string, TH1*>& histmap, std::string hname, double b11, double b21, int nb1, double b12, double b22, int nb2) {
	    histmap[hname] = new T(hname.c_str(), hname.c_str(), nb1, b11, b21, nb2, b12, b22);
	    return (T*)histmap[hname];
	}

	template <class T>
	T* add_hist_2d(std::map<std::string, TH1*>& histmap, std::string hname, int b11, int b12, int b21, int b22) {
	    histmap[hname] = new T(hname.c_str(), hname.c_str(), b12 - b11, b11, b12, b22 - b21, b21, b22);
	    return (T*)histmap[hname];
	}
};

#endif
