#include "TTH/Plotting/interface/joosep/histograms_step2.h"


Histograms::Histograms(const std::string pf, SampleType sample_type) {
    h_nj_sl = add_hist_1d<TH1D>(histmap, pf + "numJets_sl", 5, 12);
    h_nj_dl = add_hist_1d<TH1D>(histmap, pf + "numJets_dl", 4, 12);

    h_nt_sl = add_hist_1d<TH1D>(histmap, pf + "numBTagM_sl", 0, 8);
    h_nt_dl = add_hist_1d<TH1D>(histmap, pf + "numBTagM_dl", 0, 8);
	
	h_btag_lr_sl = add_hist_1d<TH1D>(histmap, pf + "btag_lr_sl", 0, 1, 20);
	h_btag_lr_dl = add_hist_1d<TH1D>(histmap, pf + "btag_lr_dl", 0, 1, 20);
	h_btag_lr_sl2 = add_hist_1d<TH1D>(histmap, pf + "btag_lr_sl2", 0.85, 1, 20);
	h_btag_lr_dl2 = add_hist_1d<TH1D>(histmap, pf + "btag_lr_dl2", 0.85, 1, 20);

    h_lep_pt_sl = add_hist_1d<TH1D>(histmap, pf + "lepton_pt_sl", 10, 400, 80);
    h_lep1_pt_dl = add_hist_1d<TH1D>(histmap, pf + "lepton1_pt_dl", 10, 400, 80);
    h_lep2_pt_dl = add_hist_1d<TH1D>(histmap, pf + "lepton2_pt_dl", 10, 400, 80);
    
    h_lep_riso_sl = add_hist_1d<TH1D>(histmap, pf + "lepton_riso_sl", 0, 0.2, 40);
    h_lep1_riso_dl = add_hist_1d<TH1D>(histmap, pf + "lepton1_riso_dl", 0, 0.2, 40);
    h_lep2_riso_dl = add_hist_1d<TH1D>(histmap, pf + "lepton2_riso_dl", 0, 0.2, 40);
    
    
    h_Vtype = add_hist_1d<TH1D>(histmap, pf + "Vtype", 0, 12);
	//TTH::label_axis(h_Vtype->GetXaxis());
    h_type = add_hist_1d<TH1D>(histmap, pf + "type", 0, 10);
    
    h_cat = add_hist_1d<TH1D>(histmap, pf + "category", 0, 8);
    h_catH = add_hist_1d<TH1D>(histmap, pf + "categoryH", 0, 8);
    h_catL = add_hist_1d<TH1D>(histmap, pf + "categoryL", 0, 8);
    
    h_cutreasons = add_hist_1d<TH1D>(histmap, pf + "cutreasons", 0, 20);
    h_triggers = add_hist_1d<TH1D>(histmap, pf + "triggers", 0, 10);
    h_proc = add_hist_1d<TH1D>(histmap, pf + "processed", 0, 2);
    
	h_cat_btag_lr = add_hist_2d<TH2D>(histmap, pf + "cat_btag_lr", 0, 8, 8, 0, 1, 20);
	h_cat_time = add_hist_2d<TH2D>(histmap, pf + "cat_time", 0, 8, 8, 0, 400, 20);

	h_vtype_btag_lr = add_hist_2d<TH2D>(histmap, pf + "vtype_btag_lr", 0, 12, 12, 0, 1, 20);
	//TTH::label_axis(h_vtype_btag_lr->GetXaxis());
	
    h_nperm_s_btaglr = add_hist_2d<TH2D>(histmap, pf + "nperm_s_btag_lr", 0, 3, 3, 0.9, 1, 10);
    h_nperm_s_me = add_hist_2d<TH2D>(histmap, pf + "nperm_s_me", 0, 3, 3, 0.0, 1.0, 6);
    h_nperm_s_cat = add_hist_2d<TH2D>(histmap, pf + "nperm_s_cat", 0, 3, 3, 0, 8, 8);

	// h_max_perm_s_cat = add_hist_2d<TH2D>(histmap, pf + "max_perm_s_cat", 0, 65, 65, 0, 8, 8);
	
	// for (int i=0; i < 64; i++) {
	// 	h_max_perm_s_cat->GetXaxis()->SetBinLabel(i+1, std::to_string(perm_maps::map1[i]).c_str());
	// 	//h_max_perm_b_cat->GetXaxis()->SetBinLabel(i+1, to_string(perm_maps::map1[i]).c_str());
	// }
	
	// TH2D* h_matched_perm_s_cat = add_hist_2d<TH2D>(histmap, pf + "matched_perm_s_cat", 0, 7, 7, 0, 8, 8);
	// TH2D* h_unmatched_perm_s_cat = add_hist_2d<TH2D>(histmap, pf + "unmatched_perm_s_cat", 0, 7, 7, 0, 8, 8);
	
	//TH2D* h_matched_perm_b_cat = add_hist_2d<TH2D>(histmap, pf + "matched_perm_b_cat", 0, 7, 7, 0, 8, 8);
	//TH2D* h_unmatched_perm_b_cat = add_hist_2d<TH2D>(histmap, pf + "unmatched_perm_b_cat", 0, 7, 7, 0, 8, 8);
	h_failreasons_cat = add_hist_2d<TH2D>(histmap, pf + "failreasons_cat", 0, 10, 10, 0, 8, 8);
	
	
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
	
	// h_unmatched_Hbb_pt = add_hist_2d<TH2D>(histmap, pf + "unmatchedHbb_pt", 0, 300, 60, 0, 300, 60);
	// h_unmatched_Hbb_eta = add_hist_2d<TH2D>(histmap, pf + "unmatchedHbb_eta",-5, 5, 60, -5, 5, 60);

	// h_unmatched_Hbb_csv = add_hist_1d<TH1D>(histmap, pf + "unmatchedHbb_csv", 0, 1, 60);
	// h_unmatched_Hbb_jetid = add_hist_1d<TH1D>(histmap, pf + "unmatchedHbb_jetid", -2, 2, 4);
	// h_unmatched_Hbb_dr = add_hist_1d<TH1D>(histmap, pf + "unmatchedHbb_dr", 0, 5, 20);
	
	// h_unmatched_tb_pt = add_hist_2d<TH2D>(histmap, pf + "unmatched_tb_pt", 0, 300, 60, 0, 300, 60);
	// h_unmatched_tb_eta = add_hist_2d<TH2D>(histmap, pf + "unmatched_tb_eta",-5, 5, 60, -5, 5, 60);

	// h_unmatched_tb_csv = add_hist_1d<TH1D>(histmap, pf + "unmatched_tb_csv", 0, 1, 60);
	// h_unmatched_tb_jetid = add_hist_1d<TH1D>(histmap, pf + "unmatched_tb_jetid", -2, 2, 4);
	// h_unmatched_tb_dr = add_hist_1d<TH1D>(histmap, pf + "unmatched_tb_dr", 0, 5, 20);
	
	// h_unmatched_Wqq_pt = add_hist_2d<TH2D>(histmap, pf + "unmatched_Wqq_pt", 0, 300, 60, 0, 300, 60);
	// h_unmatched_Wqq_eta = add_hist_2d<TH2D>(histmap, pf + "unmatched_Wqq_eta",-5, 5, 60, -5, 5, 60);

	// h_unmatched_Wqq_csv = add_hist_1d<TH1D>(histmap, pf + "unmatched_Wqq_csv", 0, 1, 60);
	// h_unmatched_Wqq_jetid = add_hist_1d<TH1D>(histmap, pf + "unmatched_Wqq_jetid", -2, 2, 4);
	// h_unmatched_Wqq_dr = add_hist_1d<TH1D>(histmap, pf + "unmatched_Wqq_dr", 0, 5, 20);
	// h_unmatched_Wqq_id = add_hist_1d<TH1D>(histmap, pf + "unmatched_Wqq_id", 0, 25, 25);
	
	// h_unmatched_lepton_pt = add_hist_2d<TH2D>(histmap, pf + "unmatched_lepton_pt", 0, 300, 60, 0, 300, 60);
	// h_unmatched_lepton_eta = add_hist_2d<TH2D>(histmap, pf + "unmatched_lepton_eta", -5, 5, 60, -5, 5, 60);

	// h_unmatched_lepton_dr = add_hist_1d<TH1D>(histmap, pf + "unmatched_lepton_dr", 0, 5, 20);
	// h_unmatched_lepton_id = add_hist_2d<TH2D>(histmap, pf + "unmatched_lepton_id", 0, 20, 20, 0, 20, 20);
	
	// h_nlep_gen_reco = add_hist_2d<TH2D>(histmap, pf + "nlep_gen_reco", 0, 3, 3, 0, 3, 3);

//		for (int i=1; i < 7; i++) {
//			for (auto* p : {h_matched_perm_s_cat, h_unmatched_perm_s_cat, h_matched_perm_b_cat, h_unmatched_perm_b_cat}) {
//				p->GetXaxis()->SetBinLabel(i, perm_maps::positions[i-1]);
//			}
//		}
	
    h_vtype_cat = add_hist_2d<TH2D>(histmap, pf + "vtype_cat", 0, 12, 12, 0, 8, 8);
	h_gvtype_cat = add_hist_2d<TH2D>(histmap, pf + "gen_vtype_cat", 0, 12, 12, 0, 8, 8);
	h_gvtype_vtype = add_hist_2d<TH2D>(histmap, pf + "gen_vtype_reco_vtype", 0, 12, 12, 0, 12, 12);
	h_unmatched_gvtype_vtype = add_hist_2d<TH2D>(histmap, pf + "unmatched_gen_vtype_reco_vtype", 0, 12, 12, 0, 12, 12);
	// TTH::label_axis(h_gvtype_cat->GetXaxis());
	// TTH::label_axis(h_gvtype_vtype->GetXaxis());
	// TTH::label_axis(h_gvtype_vtype->GetYaxis());
	// TTH::label_axis(h_unmatched_gvtype_vtype->GetXaxis());
	// TTH::label_axis(h_unmatched_gvtype_vtype->GetYaxis());

    h_btag_lr_nmatched_s = add_hist_2d<TH2D>(histmap, pf + "btag_lr_nmatched_s", 0.0, 1, 20, 0, 5, 5);
    h_btag_lr_nmatched_b = add_hist_2d<TH2D>(histmap, pf + "btag_lr_nmatched_b", 0.0, 1, 20, 0, 5, 5);
	
	h_nmatched_wqq = add_hist_1d<TH1D>(histmap, pf + "nmatched_wqq", 0, 3);
	h_nmatched_wqq_selected = add_hist_1d<TH1D>(histmap, pf + "nmatched_wqq_selected", 0, 3);
	h_unmatched_wqq_pt = add_hist_1d<TH1D>(histmap, pf + "unmatched_wqq_pt", 0, 300, 10);
	h_unmatched_wqq_eta = add_hist_1d<TH1D>(histmap, pf + "unmatched_wqq_eta", -2.5, 2.5, 10);
	h_matched_wqq_pt = add_hist_1d<TH1D>(histmap, pf + "matched_wqq_pt", 0, 300, 10);
	h_matched_wqq_eta = add_hist_1d<TH1D>(histmap, pf + "matched_wqq_eta", -2.5, 2.5, 10);

	h_nmatched_tagging_wqq = add_hist_2d<TH2D>(histmap, pf + "nmatched_tagging_wqq", 0, 3, 0, 3);

    h_cat_discr = 0;
    if (sample_type == ME_8TEV || sample_type == ME_13TEV) {
        h_cat_discr = add_hist_2d<TH2D>(histmap, pf + "cat_discr", 0, 8, 8, 0, 1, 6);
        h_discr = add_hist_1d<TH1D>(histmap, pf + "discr", 0, 1, 6);
    }

    h_btag_lr = add_hist_2d<TH2D>(histmap, pf + "btag_lr_rad", 0, 1, 2000, 0, 5, 5);
    h_btag_lr2 = add_hist_2d<TH2D>(histmap, pf + "btag_lr2_rad", 0, 1, 2000, 0, 5, 5);
    h_btag_lr3 = add_hist_2d<TH2D>(histmap, pf + "btag_lr3_rad", 0, 1, 2000, 0, 5, 5);
    h_btag_lr4 = add_hist_2d<TH2D>(histmap, pf + "btag_lr4_rad", 0, 1, 2000, 0, 5, 5);
    h_radmode = add_hist_1d<TH1D>(histmap, pf + "radmode", 0, 5);
}
