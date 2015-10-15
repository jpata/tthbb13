
#ifndef METREE_H
#define METREE_H
#include "TTree.h"
class TreeData {
public:
  int nmem_ttbb;
  double mem_ttbb_btag_weight_jj[11]; //
  int mem_ttbb_nperm[11]; //
  double mem_ttbb_chi2[11]; //
  double mem_ttbb_p_err[11]; //
  double mem_ttbb_time[11]; //
  double mem_ttbb_btag_weight_cc[11]; //
  double mem_ttbb_p[11]; //
  double mem_ttbb_efficiency[11]; //
  double mem_ttbb_btag_weight_bb[11]; //
  double mem_ttbb_prefit_code[11]; //
  int mem_ttbb_error_code[11]; //
  int nmem_tth_raw;
  double mem_tth_raw_btag_weight_jj[11]; //
  int mem_tth_raw_nperm[11]; //
  double mem_tth_raw_chi2[11]; //
  double mem_tth_raw_p_err[11]; //
  double mem_tth_raw_time[11]; //
  double mem_tth_raw_btag_weight_cc[11]; //
  double mem_tth_raw_p[11]; //
  double mem_tth_raw_efficiency[11]; //
  double mem_tth_raw_btag_weight_bb[11]; //
  double mem_tth_raw_prefit_code[11]; //
  int mem_tth_raw_error_code[11]; //
  int nfw_aj_JESDown;
  double fw_aj_JESDown_fw_h_alljets_JESDown[8]; //
  int nmem_ttbb_JESUp;
  double mem_ttbb_JESUp_btag_weight_jj[11]; //
  int mem_ttbb_JESUp_nperm[11]; //
  double mem_ttbb_JESUp_chi2[11]; //
  double mem_ttbb_JESUp_p_err[11]; //
  double mem_ttbb_JESUp_time[11]; //
  double mem_ttbb_JESUp_btag_weight_cc[11]; //
  double mem_ttbb_JESUp_p[11]; //
  double mem_ttbb_JESUp_efficiency[11]; //
  double mem_ttbb_JESUp_btag_weight_bb[11]; //
  double mem_ttbb_JESUp_prefit_code[11]; //
  int mem_ttbb_JESUp_error_code[11]; //
  int nfw_uj_JESDown;
  double fw_uj_JESDown_fw_h_untagjets_JESDown[8]; //
  int nfw_aj;
  double fw_aj_fw_h_alljets_nominal[8]; //
  int nmem_ttbb_JESDown;
  double mem_ttbb_JESDown_btag_weight_jj[11]; //
  int mem_ttbb_JESDown_nperm[11]; //
  double mem_ttbb_JESDown_chi2[11]; //
  double mem_ttbb_JESDown_p_err[11]; //
  double mem_ttbb_JESDown_time[11]; //
  double mem_ttbb_JESDown_btag_weight_cc[11]; //
  double mem_ttbb_JESDown_p[11]; //
  double mem_ttbb_JESDown_efficiency[11]; //
  double mem_ttbb_JESDown_btag_weight_bb[11]; //
  double mem_ttbb_JESDown_prefit_code[11]; //
  int mem_ttbb_JESDown_error_code[11]; //
  int nfw_uj;
  double fw_uj_fw_h_untagjets_nominal[8]; //
  int nfw_bj_JESUp;
  double fw_bj_JESUp_fw_h_btagjets_JESUp[8]; //
  int nfw_uj_raw;
  double fw_uj_raw_fw_h_untagjets_raw[8]; //
  int nmem_ttbb_raw;
  double mem_ttbb_raw_btag_weight_jj[11]; //
  int mem_ttbb_raw_nperm[11]; //
  double mem_ttbb_raw_chi2[11]; //
  double mem_ttbb_raw_p_err[11]; //
  double mem_ttbb_raw_time[11]; //
  double mem_ttbb_raw_btag_weight_cc[11]; //
  double mem_ttbb_raw_p[11]; //
  double mem_ttbb_raw_efficiency[11]; //
  double mem_ttbb_raw_btag_weight_bb[11]; //
  double mem_ttbb_raw_prefit_code[11]; //
  int mem_ttbb_raw_error_code[11]; //
  int nmem_tth_JESUp;
  double mem_tth_JESUp_btag_weight_jj[11]; //
  int mem_tth_JESUp_nperm[11]; //
  double mem_tth_JESUp_chi2[11]; //
  double mem_tth_JESUp_p_err[11]; //
  double mem_tth_JESUp_time[11]; //
  double mem_tth_JESUp_btag_weight_cc[11]; //
  double mem_tth_JESUp_p[11]; //
  double mem_tth_JESUp_efficiency[11]; //
  double mem_tth_JESUp_btag_weight_bb[11]; //
  double mem_tth_JESUp_prefit_code[11]; //
  int mem_tth_JESUp_error_code[11]; //
  int nmem_tth_JESDown;
  double mem_tth_JESDown_btag_weight_jj[11]; //
  int mem_tth_JESDown_nperm[11]; //
  double mem_tth_JESDown_chi2[11]; //
  double mem_tth_JESDown_p_err[11]; //
  double mem_tth_JESDown_time[11]; //
  double mem_tth_JESDown_btag_weight_cc[11]; //
  double mem_tth_JESDown_p[11]; //
  double mem_tth_JESDown_efficiency[11]; //
  double mem_tth_JESDown_btag_weight_bb[11]; //
  double mem_tth_JESDown_prefit_code[11]; //
  int mem_tth_JESDown_error_code[11]; //
  int nothertopCandidate;
  double othertopCandidate_tau1[28]; //
  double othertopCandidate_phi[28]; //
  double othertopCandidate_sjW2btag[28]; //
  double othertopCandidate_sjW2pt[28]; //
  double othertopCandidate_sjW1btag[28]; //
  double othertopCandidate_sjW1mass[28]; //
  double othertopCandidate_sjNonWmass[28]; //
  double othertopCandidate_sjNonWeta[28]; //
  double othertopCandidate_pt[28]; //
  double othertopCandidate_ptForRoptCalc[28]; //
  double othertopCandidate_tau2[28]; //
  double othertopCandidate_sjW2mass[28]; //
  double othertopCandidate_tau3[28]; //
  double othertopCandidate_sjNonWpt[28]; //
  double othertopCandidate_mass[28]; //
  double othertopCandidate_sjNonWbtag[28]; //
  double othertopCandidate_Ropt[28]; //
  double othertopCandidate_RoptCalc[28]; //
  double othertopCandidate_sjW1phi[28]; //
  double othertopCandidate_sjW1pt[28]; //
  double othertopCandidate_sjNonWphi[28]; //
  double othertopCandidate_delRopt[28]; //
  double othertopCandidate_sjW1eta[28]; //
  double othertopCandidate_fRec[28]; //
  double othertopCandidate_sjW2phi[28]; //
  double othertopCandidate_eta[28]; //
  double othertopCandidate_n_subjettiness[28]; //
  double othertopCandidate_bbtag[28]; //
  double othertopCandidate_sjW2eta[28]; //
  int nfw_aj_JESUp;
  double fw_aj_JESUp_fw_h_alljets_JESUp[8]; //
  int nleps;
  double leps_phi[2]; //
  double leps_pt[2]; //
  double leps_pdgId[2]; //
  double leps_relIso04[2]; //
  double leps_eta[2]; //
  double leps_mass[2]; //
  double leps_relIso03[2]; //
  int njets;
  double jets_mcPt[9]; //
  double jets_mcEta[9]; //
  double jets_mcPhi[9]; //
  double jets_btagCSVInp2t[9]; //
  double jets_qgl[9]; //
  double jets_btagCSVRnd3t[9]; //
  double jets_id[9]; //
  double jets_bTagWeightLFUp[9]; //
  double jets_mcNumBHadronsFromTop[9]; //
  double jets_mcNumCHadronsFromTop[9]; //
  double jets_pt[9]; //
  double jets_mcNumBHadrons[9]; //
  double jets_mcNumCHadronsAfterTop[9]; //
  double jets_bTagWeightStats2Up[9]; //
  double jets_eta[9]; //
  double jets_btagProb[9]; //
  double jets_btagCSVRndge4t[9]; //
  double jets_bTagWeightStats1Up[9]; //
  double jets_bTagWeightStats1Down[9]; //
  double jets_mcNumCHadrons[9]; //
  int jets_matchFlag[9]; //
  double jets_phi[9]; //
  double jets_bTagWeightStats2Down[9]; //
  double jets_bTagWeightLFDown[9]; //
  int jets_hadronFlavour[9]; //
  double jets_corr_JESUp[9]; //
  double jets_bTagWeightJESDown[9]; //
  double jets_btagCSVInp3t[9]; //
  double jets_bTagWeightHFDown[9]; //
  double jets_btagSoftMu[9]; //
  double jets_btagCSVRnd2t[9]; //
  double jets_corr[9]; //
  double jets_btagCMVAV2[9]; //
  double jets_corr_JESDown[9]; //
  double jets_btagCSV[9]; //
  double jets_mcM[9]; //
  double jets_bTagWeightHFUp[9]; //
  int jets_mcMatchId[9]; //
  double jets_mcNumBHadronsAfterTop[9]; //
  double jets_bTagWeight[9]; //
  double jets_btagSoftEl[9]; //
  double jets_mass[9]; //
  double jets_bTagWeightJESUp[9]; //
  int jets_mcFlavour[9]; //
  double jets_btagCSVInpge4t[9]; //
  int nfw_bj;
  double fw_bj_fw_h_btagjets_nominal[8]; //
  int nfw_aj_raw;
  double fw_aj_raw_fw_h_alljets_raw[8]; //
  int nfatjets;
  double fatjets_phi[4]; //
  double fatjets_pt[4]; //
  double fatjets_tau1[4]; //
  double fatjets_tau2[4]; //
  double fatjets_tau3[4]; //
  double fatjets_eta[4]; //
  double fatjets_mass[4]; //
  double fatjets_bbtag[4]; //
  int nhiggsCandidate;
  double higgsCandidate_phi[9]; //
  double higgsCandidate_pt[9]; //
  double higgsCandidate_tau1[9]; //
  double higgsCandidate_tau2[9]; //
  double higgsCandidate_tau3[9]; //
  double higgsCandidate_eta[9]; //
  double higgsCandidate_n_subjettiness[9]; //
  double higgsCandidate_bbtag[9]; //
  double higgsCandidate_mass[9]; //
  int nfw_uj_JESUp;
  double fw_uj_JESUp_fw_h_untagjets_JESUp[8]; //
  int nmem_tth;
  double mem_tth_btag_weight_jj[11]; //
  int mem_tth_nperm[11]; //
  double mem_tth_chi2[11]; //
  double mem_tth_p_err[11]; //
  double mem_tth_time[11]; //
  double mem_tth_btag_weight_cc[11]; //
  double mem_tth_p[11]; //
  double mem_tth_efficiency[11]; //
  double mem_tth_btag_weight_bb[11]; //
  double mem_tth_prefit_code[11]; //
  int mem_tth_error_code[11]; //
  int nfw_bj_raw;
  double fw_bj_raw_fw_h_btagjets_raw[8]; //
  int ntopCandidate;
  double topCandidate_tau1[28]; //
  double topCandidate_phi[28]; //
  double topCandidate_sjW2btag[28]; //
  double topCandidate_sjW2pt[28]; //
  double topCandidate_sjW1btag[28]; //
  double topCandidate_sjW1mass[28]; //
  double topCandidate_sjNonWmass[28]; //
  double topCandidate_sjNonWeta[28]; //
  double topCandidate_pt[28]; //
  double topCandidate_ptForRoptCalc[28]; //
  double topCandidate_tau2[28]; //
  double topCandidate_sjW2mass[28]; //
  double topCandidate_tau3[28]; //
  double topCandidate_sjNonWpt[28]; //
  double topCandidate_mass[28]; //
  double topCandidate_sjNonWbtag[28]; //
  double topCandidate_Ropt[28]; //
  double topCandidate_RoptCalc[28]; //
  double topCandidate_sjW1phi[28]; //
  double topCandidate_sjW1pt[28]; //
  double topCandidate_sjNonWphi[28]; //
  double topCandidate_delRopt[28]; //
  double topCandidate_sjW1eta[28]; //
  double topCandidate_fRec[28]; //
  double topCandidate_sjW2phi[28]; //
  double topCandidate_eta[28]; //
  double topCandidate_n_subjettiness[28]; //
  double topCandidate_bbtag[28]; //
  double topCandidate_sjW2eta[28]; //
  int nfw_bj_JESDown;
  double fw_bj_JESDown_fw_h_btagjets_JESDown[8]; //
  int nbRnd_inp_3t_JESDown;
  double bRnd_inp_3t_JESDown_p[1]; //
  int bRnd_inp_3t_JESDown_ntoys[1]; //
  int bRnd_inp_3t_JESDown_tag_id[1]; //
  int bRnd_inp_3t_JESDown_pass[1]; //
  int nbRnd_rnd_3t_JESUp;
  double bRnd_rnd_3t_JESUp_p[1]; //
  int bRnd_rnd_3t_JESUp_ntoys[1]; //
  int bRnd_rnd_3t_JESUp_tag_id[1]; //
  int bRnd_rnd_3t_JESUp_pass[1]; //
  int nbRnd_inp_3t_JESUp;
  double bRnd_inp_3t_JESUp_p[1]; //
  int bRnd_inp_3t_JESUp_ntoys[1]; //
  int bRnd_inp_3t_JESUp_tag_id[1]; //
  int bRnd_inp_3t_JESUp_pass[1]; //
  int nbRnd_inp_3t_raw;
  double bRnd_inp_3t_raw_p[1]; //
  int bRnd_inp_3t_raw_ntoys[1]; //
  int bRnd_inp_3t_raw_tag_id[1]; //
  int bRnd_inp_3t_raw_pass[1]; //
  int nmet_jetcorr;
  double met_jetcorr_phi[1]; //
  double met_jetcorr_sumEt[1]; //
  double met_jetcorr_pt[1]; //
  double met_jetcorr_px[1]; //
  double met_jetcorr_py[1]; //
  double met_jetcorr_genPhi[1]; //
  double met_jetcorr_genPt[1]; //
  int npv;
  double pv_z[1]; //
  double pv_isFake[1]; //
  double pv_rho[1]; //
  double pv_ndof[1]; //
  int nbRnd_inp_ge4t_JESUp;
  double bRnd_inp_ge4t_JESUp_p[1]; //
  int bRnd_inp_ge4t_JESUp_ntoys[1]; //
  int bRnd_inp_ge4t_JESUp_tag_id[1]; //
  int bRnd_inp_ge4t_JESUp_pass[1]; //
  int nll;
  double ll_phi[1]; //
  double ll_eta[1]; //
  double ll_mass[1]; //
  double ll_pt[1]; //
  int nbRnd_rnd_ge4t;
  double bRnd_rnd_ge4t_p[1]; //
  int bRnd_rnd_ge4t_ntoys[1]; //
  int bRnd_rnd_ge4t_tag_id[1]; //
  int bRnd_rnd_ge4t_pass[1]; //
  int nbRnd_rnd_ge4t_JESUp;
  double bRnd_rnd_ge4t_JESUp_p[1]; //
  int bRnd_rnd_ge4t_JESUp_ntoys[1]; //
  int bRnd_rnd_ge4t_JESUp_tag_id[1]; //
  int bRnd_rnd_ge4t_JESUp_pass[1]; //
  int nbRnd_inp_ge4t_JESDown;
  double bRnd_inp_ge4t_JESDown_p[1]; //
  int bRnd_inp_ge4t_JESDown_ntoys[1]; //
  int bRnd_inp_ge4t_JESDown_tag_id[1]; //
  int bRnd_inp_ge4t_JESDown_pass[1]; //
  int nbRnd_rnd_ge4t_JESDown;
  double bRnd_rnd_ge4t_JESDown_p[1]; //
  int bRnd_rnd_ge4t_JESDown_ntoys[1]; //
  int bRnd_rnd_ge4t_JESDown_tag_id[1]; //
  int bRnd_rnd_ge4t_JESDown_pass[1]; //
  int nmet;
  double met_phi[1]; //
  double met_sumEt[1]; //
  double met_pt[1]; //
  double met_px[1]; //
  double met_py[1]; //
  double met_genPhi[1]; //
  double met_genPt[1]; //
  int nbRnd_inp_ge4t;
  double bRnd_inp_ge4t_p[1]; //
  int bRnd_inp_ge4t_ntoys[1]; //
  int bRnd_inp_ge4t_tag_id[1]; //
  int bRnd_inp_ge4t_pass[1]; //
  int nbRnd_rnd_ge4t_raw;
  double bRnd_rnd_ge4t_raw_p[1]; //
  int bRnd_rnd_ge4t_raw_ntoys[1]; //
  int bRnd_rnd_ge4t_raw_tag_id[1]; //
  int bRnd_rnd_ge4t_raw_pass[1]; //
  int nbRnd_inp_3t;
  double bRnd_inp_3t_p[1]; //
  int bRnd_inp_3t_ntoys[1]; //
  int bRnd_inp_3t_tag_id[1]; //
  int bRnd_inp_3t_pass[1]; //
  int nmet_ttbar_gen;
  double met_ttbar_gen_phi[1]; //
  double met_ttbar_gen_sumEt[1]; //
  double met_ttbar_gen_pt[1]; //
  double met_ttbar_gen_px[1]; //
  double met_ttbar_gen_py[1]; //
  double met_ttbar_gen_genPhi[1]; //
  double met_ttbar_gen_genPt[1]; //
  int nbRnd_rnd_3t_raw;
  double bRnd_rnd_3t_raw_p[1]; //
  int bRnd_rnd_3t_raw_ntoys[1]; //
  int bRnd_rnd_3t_raw_tag_id[1]; //
  int bRnd_rnd_3t_raw_pass[1]; //
  int nbRnd_rnd_3t;
  double bRnd_rnd_3t_p[1]; //
  int bRnd_rnd_3t_ntoys[1]; //
  int bRnd_rnd_3t_tag_id[1]; //
  int bRnd_rnd_3t_pass[1]; //
  int nbRnd_inp_ge4t_raw;
  double bRnd_inp_ge4t_raw_p[1]; //
  int bRnd_inp_ge4t_raw_ntoys[1]; //
  int bRnd_inp_ge4t_raw_tag_id[1]; //
  int bRnd_inp_ge4t_raw_pass[1]; //
  int nbRnd_rnd_3t_JESDown;
  double bRnd_rnd_3t_JESDown_p[1]; //
  int bRnd_rnd_3t_JESDown_ntoys[1]; //
  int bRnd_rnd_3t_JESDown_tag_id[1]; //
  int bRnd_rnd_3t_JESDown_pass[1]; //
  int nmet_gen;
  double met_gen_phi[1]; //
  double met_gen_sumEt[1]; //
  double met_gen_pt[1]; //
  double met_gen_px[1]; //
  double met_gen_py[1]; //
  double met_gen_genPhi[1]; //
  double met_gen_genPt[1]; //
  double std_bdisc_btag_JESDown;
  double qg_LR_flavour_4q_1q_raw;
  double mean_bdisc_btag;
  int HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v;
  double bTagWeight_Stats2Down;
  double min_dr_btag_JESDown;
  double qg_LR_flavour_4q_1q_2q_3q_JESUp;
  double ht_raw;
  double qg_LR_flavour_4q_0q_1q_2q_3q;
  double C_JESDown;
  double btag_lr_4b_Rndge4t_JESDown;
  int passes_jet_JESUp;
  double momentum_eig2_JESDown;
  double mean_dr_btag_JESDown;
  double pt_drpair_btag_JESDown;
  int is_dl_JESUp;
  double weight_xs;
  int nMatch_hb_raw;
  double btag_lr_4b_Inpge4t;
  double qg_LR_flavour_4q_0q_1q_2q_JESUp;
  double pt_drpair_btag;
  int nBCSVT_raw;
  double ht_JESDown;
  double bTagWeight_Stats2Up;
  double btag_lr_2b_Rnd3t_JESDown;
  int nMatch_hb_btag_raw;
  double qg_LR_flavour_4q_0q_1q_2q_3q_JESDown;
  double std_bdisc_btag;
  double sphericity;
  int nMatchSimB_JESUp;
  double btag_LR_4b_2b_Inp3t_JESUp;
  int HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v;
  int passes_btag_JESDown;
  double btag_lr_4b;
  double qg_LR_flavour_4q_0q_1q_2q;
  double qg_LR_flavour_4q_1q_2q;
  double qg_LR_flavour_4q_1q_JESUp;
  int nBCSVM_raw;
  double btag_lr_4b_Inpge4t_JESDown;
  int nBCSVL_JESUp;
  double Wmass_raw;
  double std_dr_btag_raw;
  double isotropy_JESDown;
  double qg_LR_flavour_4q_1q;
  double mean_bdisc_btag_JESUp;
  double qg_LR_flavour_4q_0q_JESDown;
  double qg_LR_flavour_4q_3q_JESUp;
  double momentum_eig2;
  double momentum_eig1;
  double momentum_eig0;
  double momentum_eig0_JESDown;
  double qg_LR_flavour_4q_1q_2q_3q_raw;
  double std_bdisc_JESUp;
  double bTagWeight_JESUp;
  int nMatch_tb_raw;
  int cat_btag;
  double btag_lr_2b_Rndge4t_JESDown;
  double btag_lr_2b_JESDown;
  double bTagWeight_HFDown;
  double btag_lr_2b_Inpge4t;
  double btag_lr_2b_Inp3t;
  int is_dl_raw;
  double bTagWeight_Stats1Down;
  int cat_btag_JESUp;
  double isotropy;
  double eta_drpair_btag_raw;
  double btag_LR_4b_2b_Rnd3t_raw;
  double bTagWeight;
  int nMatchSimC_raw;
  double aplanarity_raw;
  double btag_LR_4b_2b_Inpge4t_raw;
  int is_fh;
  double n_boosted_bjets;
  double mass_drpair_btag_raw;
  double btag_lr_4b_Inp3t_raw;
  double eta_drpair_btag;
  int is_sl_raw;
  double btag_LR_4b_2b_raw;
  double btag_LR_4b_2b_Rnd3t_JESUp;
  int passes_jet_raw;
  double eta_drpair_btag_JESUp;
  int nBCSVL_JESDown;
  double n_bjets;
  double qg_LR_flavour_4q_0q_raw;
  int numJets;
  double btag_lr_2b;
  double btag_LR_4b_2b_Inpge4t_JESDown;
  int nMatch_wq_btag_JESUp;
  double btag_lr_2b_Rndge4t_raw;
  double n_ljets;
  int nBCSVL_raw;
  double n_excluded_ljets;
  double min_dr_btag;
  double qg_LR_flavour_4q_0q_1q_JESDown;
  double btag_lr_2b_Inp3t_JESUp;
  double Wmass;
  int nMatchSimB_raw;
  int cat_JESDown;
  int nMatchSimC_JESUp;
  double btag_lr_2b_Rnd3t;
  double qg_LR_flavour_4q_1q_2q_JESDown;
  int nMatch_wq_JESDown;
  double qg_LR_flavour_4q_0q_1q_JESUp;
  double momentum_eig2_JESUp;
  int nMatch_wq_btag_JESDown;
  double qg_LR_flavour_4q_2q_JESDown;
  double std_bdisc_btag_JESUp;
  int cat_btag_JESDown;
  int is_fh_JESDown;
  double btag_lr_2b_Inp3t_JESDown;
  double btag_lr_4b_Rndge4t_raw;
  double C;
  double pt_drpair_btag_raw;
  int nBCSVT_JESDown;
  double aplanarity;
  double btag_LR_4b_2b_Inp3t_JESDown;
  int is_sl_JESDown;
  double std_dr_btag;
  double momentum_eig1_raw;
  double qg_LR_flavour_4q_1q_JESDown;
  double btag_LR_4b_2b_Inp3t;
  int numJets_JESUp;
  int passes_btag_raw;
  int is_sl;
  double tth_mva;
  double mean_bdisc_btag_raw;
  double qg_LR_flavour_4q_1q_2q_3q_JESDown;
  double std_bdisc;
  double btag_lr_4b_Rnd3t_JESDown;
  double btag_LR_4b_2b_JESUp;
  double mass_drpair_btag_JESDown;
  double mean_bdisc_JESUp;
  double btag_lr_4b_Inp3t_JESUp;
  double btag_lr_4b_Rnd3t_JESUp;
  double qg_LR_flavour_4q_2q_3q_JESDown;
  int cat_raw;
  double qg_LR_flavour_4q_2q_3q_JESUp;
  int passPV;
  int triggerBitmask;
  double btag_lr_2b_Rndge4t;
  double D_raw;
  double bTagWeight_LFUp;
  int cat_btag_raw;
  double btag_LR_4b_2b_Rnd3t_JESDown;
  int nMatchSimC_JESDown;
  int nBCSVM_JESUp;
  double mean_bdisc_raw;
  int ttCls;
  int triggerDecision;
  int nMatch_tb_JESDown;
  double btag_lr_4b_JESDown;
  int HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v;
  double min_dr_btag_JESUp;
  double std_bdisc_btag_raw;
  double pt_drpair_btag_JESUp;
  double mean_bdisc_btag_JESDown;
  double qg_LR_flavour_4q_3q;
  double btag_lr_2b_Inp3t_raw;
  double qg_LR_flavour_4q_2q_3q;
  double btag_lr_2b_JESUp;
  double qg_LR_flavour_4q_2q_3q_raw;
  double C_raw;
  int nBCSVT;
  int nMatch_hb_btag_JESUp;
  double btag_LR_4b_2b_Inp3t_raw;
  double std_bdisc_raw;
  int cat_gen_raw;
  int nGenQW;
  int nMatch_wq_JESUp;
  double momentum_eig1_JESUp;
  int HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v;
  double qg_LR_flavour_4q_2q_raw;
  double aplanarity_JESUp;
  int nMatch_tb_btag;
  double qg_LR_flavour_4q_0q_JESUp;
  int nMatch_hb;
  double btag_lr_2b_Inpge4t_JESUp;
  int nBCSVL;
  int nBCSVM;
  int cat_gen;
  int HLT_BIT_HLT_Ele27_eta2p1_WP85_Gsf_HT200_v;
  int passes_btag_JESUp;
  double sphericity_JESUp;
  int numJets_raw;
  int is_fh_JESUp;
  double sphericity_raw;
  double qg_LR_flavour_4q_1q_2q_3q;
  double ht;
  double btag_LR_4b_2b_Rndge4t_JESDown;
  double btag_lr_4b_Rnd3t_raw;
  double btag_lr_4b_Rnd3t;
  int passes_jet_JESDown;
  int nMatch_wq_btag;
  double btag_lr_4b_JESUp;
  double qg_LR_flavour_4q_0q_1q_raw;
  double qg_LR_flavour_4q_2q;
  int nMatch_tb_JESUp;
  double sphericity_JESDown;
  int cat_gen_JESDown;
  double mean_bdisc;
  double mass_drpair_btag;
  double momentum_eig1_JESDown;
  double mass_drpair_btag_JESUp;
  int is_dl_JESDown;
  double bTagWeight_LFDown;
  double btag_lr_4b_Inp3t;
  double qg_LR_flavour_4q_2q_JESUp;
  int is_sl_JESUp;
  double momentum_eig2_raw;
  int cat;
  int nMatchSimB_JESDown;
  double btag_LR_4b_2b_Rnd3t;
  int nMatch_tb_btag_raw;
  double btag_LR_4b_2b;
  double qg_LR_flavour_4q_3q_raw;
  double btag_LR_4b_2b_Rndge4t_raw;
  int nMatch_wq;
  double qg_LR_flavour_4q_0q_1q_2q_raw;
  int numJets_JESDown;
  int nMatchSimB;
  int nMatchSimC;
  int nMatch_wq_btag_raw;
  double qg_LR_flavour_4q_3q_JESDown;
  int nMatch_tb_btag_JESDown;
  double btag_LR_4b_2b_Inpge4t;
  int nMatch_hb_JESUp;
  double btag_LR_4b_2b_Inpge4t_JESUp;
  double btag_lr_4b_Rndge4t;
  int nMatch_wq_raw;
  double bTagWeight_JESDown;
  double ht_JESUp;
  double btag_lr_4b_raw;
  double std_dr_btag_JESUp;
  double btag_lr_2b_Rndge4t_JESUp;
  double isotropy_raw;
  double n_boosted_ljets;
  int nBCSVT_JESUp;
  double qg_LR_flavour_4q_0q_1q;
  double D;
  int nMatch_hb_btag;
  double mean_bdisc_JESDown;
  int HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v;
  double btag_lr_2b_Rnd3t_JESUp;
  double btag_lr_2b_Rnd3t_raw;
  double mean_dr_btag;
  double aplanarity_JESDown;
  double qg_LR_flavour_4q_1q_2q_raw;
  int nGenBHiggs;
  double isotropy_JESUp;
  double std_dr_btag_JESDown;
  double bTagWeight_Stats1Up;
  double Wmass_JESDown;
  int cat_gen_JESUp;
  double momentum_eig0_JESUp;
  double btag_LR_4b_2b_Rndge4t_JESUp;
  double btag_LR_4b_2b_JESDown;
  double btag_lr_4b_Inpge4t_JESUp;
  double qg_LR_flavour_4q_0q_1q_2q_3q_JESUp;
  double btag_lr_4b_Inp3t_JESDown;
  double btag_lr_4b_Inpge4t_raw;
  double btag_lr_2b_Inpge4t_JESDown;
  double D_JESDown;
  double bTagWeight_HFUp;
  double btag_lr_2b_Inpge4t_raw;
  double min_dr_btag_raw;
  int is_fh_raw;
  double Wmass_JESUp;
  double qg_LR_flavour_4q_1q_2q_JESUp;
  int HLT_BIT_HLT_IsoMu24_eta2p1_v;
  double qg_LR_flavour_4q_0q;
  double btag_lr_4b_Rndge4t_JESUp;
  double btag_LR_4b_2b_Rndge4t;
  double n_excluded_bjets;
  int nMatch_hb_btag_JESDown;
  double btag_lr_2b_raw;
  double momentum_eig0_raw;
  int nBCSVM_JESDown;
  int nMatch_tb_btag_JESUp;
  double qg_LR_flavour_4q_0q_1q_2q_3q_raw;
  double std_bdisc_JESDown;
  double eta_drpair_btag_JESDown;
  int passes_btag;
  int nMatch_hb_JESDown;
  int cat_JESUp;
  double qg_LR_flavour_4q_0q_1q_2q_JESDown;
  int nMatch_tb;
  int passes_jet;
  double D_JESUp;
  int is_dl;
  int nGenBTop;
  double C_JESUp;
  double mean_dr_btag_raw;
  double mean_dr_btag_JESUp;
  void loadTree(TTree* tree) {
    tree->SetBranchAddress("nmem_ttbb", &(this->nmem_ttbb));
    tree->SetBranchAddress("mem_ttbb_btag_weight_jj", this->mem_ttbb_btag_weight_jj);
    tree->SetBranchAddress("mem_ttbb_nperm", this->mem_ttbb_nperm);
    tree->SetBranchAddress("mem_ttbb_chi2", this->mem_ttbb_chi2);
    tree->SetBranchAddress("mem_ttbb_p_err", this->mem_ttbb_p_err);
    tree->SetBranchAddress("mem_ttbb_time", this->mem_ttbb_time);
    tree->SetBranchAddress("mem_ttbb_btag_weight_cc", this->mem_ttbb_btag_weight_cc);
    tree->SetBranchAddress("mem_ttbb_p", this->mem_ttbb_p);
    tree->SetBranchAddress("mem_ttbb_efficiency", this->mem_ttbb_efficiency);
    tree->SetBranchAddress("mem_ttbb_btag_weight_bb", this->mem_ttbb_btag_weight_bb);
    tree->SetBranchAddress("mem_ttbb_prefit_code", this->mem_ttbb_prefit_code);
    tree->SetBranchAddress("mem_ttbb_error_code", this->mem_ttbb_error_code);
    tree->SetBranchAddress("nmem_tth_raw", &(this->nmem_tth_raw));
    tree->SetBranchAddress("mem_tth_raw_btag_weight_jj", this->mem_tth_raw_btag_weight_jj);
    tree->SetBranchAddress("mem_tth_raw_nperm", this->mem_tth_raw_nperm);
    tree->SetBranchAddress("mem_tth_raw_chi2", this->mem_tth_raw_chi2);
    tree->SetBranchAddress("mem_tth_raw_p_err", this->mem_tth_raw_p_err);
    tree->SetBranchAddress("mem_tth_raw_time", this->mem_tth_raw_time);
    tree->SetBranchAddress("mem_tth_raw_btag_weight_cc", this->mem_tth_raw_btag_weight_cc);
    tree->SetBranchAddress("mem_tth_raw_p", this->mem_tth_raw_p);
    tree->SetBranchAddress("mem_tth_raw_efficiency", this->mem_tth_raw_efficiency);
    tree->SetBranchAddress("mem_tth_raw_btag_weight_bb", this->mem_tth_raw_btag_weight_bb);
    tree->SetBranchAddress("mem_tth_raw_prefit_code", this->mem_tth_raw_prefit_code);
    tree->SetBranchAddress("mem_tth_raw_error_code", this->mem_tth_raw_error_code);
    tree->SetBranchAddress("nfw_aj_JESDown", &(this->nfw_aj_JESDown));
    tree->SetBranchAddress("fw_aj_JESDown_fw_h_alljets_JESDown", this->fw_aj_JESDown_fw_h_alljets_JESDown);
    tree->SetBranchAddress("nmem_ttbb_JESUp", &(this->nmem_ttbb_JESUp));
    tree->SetBranchAddress("mem_ttbb_JESUp_btag_weight_jj", this->mem_ttbb_JESUp_btag_weight_jj);
    tree->SetBranchAddress("mem_ttbb_JESUp_nperm", this->mem_ttbb_JESUp_nperm);
    tree->SetBranchAddress("mem_ttbb_JESUp_chi2", this->mem_ttbb_JESUp_chi2);
    tree->SetBranchAddress("mem_ttbb_JESUp_p_err", this->mem_ttbb_JESUp_p_err);
    tree->SetBranchAddress("mem_ttbb_JESUp_time", this->mem_ttbb_JESUp_time);
    tree->SetBranchAddress("mem_ttbb_JESUp_btag_weight_cc", this->mem_ttbb_JESUp_btag_weight_cc);
    tree->SetBranchAddress("mem_ttbb_JESUp_p", this->mem_ttbb_JESUp_p);
    tree->SetBranchAddress("mem_ttbb_JESUp_efficiency", this->mem_ttbb_JESUp_efficiency);
    tree->SetBranchAddress("mem_ttbb_JESUp_btag_weight_bb", this->mem_ttbb_JESUp_btag_weight_bb);
    tree->SetBranchAddress("mem_ttbb_JESUp_prefit_code", this->mem_ttbb_JESUp_prefit_code);
    tree->SetBranchAddress("mem_ttbb_JESUp_error_code", this->mem_ttbb_JESUp_error_code);
    tree->SetBranchAddress("nfw_uj_JESDown", &(this->nfw_uj_JESDown));
    tree->SetBranchAddress("fw_uj_JESDown_fw_h_untagjets_JESDown", this->fw_uj_JESDown_fw_h_untagjets_JESDown);
    tree->SetBranchAddress("nfw_aj", &(this->nfw_aj));
    tree->SetBranchAddress("fw_aj_fw_h_alljets_nominal", this->fw_aj_fw_h_alljets_nominal);
    tree->SetBranchAddress("nmem_ttbb_JESDown", &(this->nmem_ttbb_JESDown));
    tree->SetBranchAddress("mem_ttbb_JESDown_btag_weight_jj", this->mem_ttbb_JESDown_btag_weight_jj);
    tree->SetBranchAddress("mem_ttbb_JESDown_nperm", this->mem_ttbb_JESDown_nperm);
    tree->SetBranchAddress("mem_ttbb_JESDown_chi2", this->mem_ttbb_JESDown_chi2);
    tree->SetBranchAddress("mem_ttbb_JESDown_p_err", this->mem_ttbb_JESDown_p_err);
    tree->SetBranchAddress("mem_ttbb_JESDown_time", this->mem_ttbb_JESDown_time);
    tree->SetBranchAddress("mem_ttbb_JESDown_btag_weight_cc", this->mem_ttbb_JESDown_btag_weight_cc);
    tree->SetBranchAddress("mem_ttbb_JESDown_p", this->mem_ttbb_JESDown_p);
    tree->SetBranchAddress("mem_ttbb_JESDown_efficiency", this->mem_ttbb_JESDown_efficiency);
    tree->SetBranchAddress("mem_ttbb_JESDown_btag_weight_bb", this->mem_ttbb_JESDown_btag_weight_bb);
    tree->SetBranchAddress("mem_ttbb_JESDown_prefit_code", this->mem_ttbb_JESDown_prefit_code);
    tree->SetBranchAddress("mem_ttbb_JESDown_error_code", this->mem_ttbb_JESDown_error_code);
    tree->SetBranchAddress("nfw_uj", &(this->nfw_uj));
    tree->SetBranchAddress("fw_uj_fw_h_untagjets_nominal", this->fw_uj_fw_h_untagjets_nominal);
    tree->SetBranchAddress("nfw_bj_JESUp", &(this->nfw_bj_JESUp));
    tree->SetBranchAddress("fw_bj_JESUp_fw_h_btagjets_JESUp", this->fw_bj_JESUp_fw_h_btagjets_JESUp);
    tree->SetBranchAddress("nfw_uj_raw", &(this->nfw_uj_raw));
    tree->SetBranchAddress("fw_uj_raw_fw_h_untagjets_raw", this->fw_uj_raw_fw_h_untagjets_raw);
    tree->SetBranchAddress("nmem_ttbb_raw", &(this->nmem_ttbb_raw));
    tree->SetBranchAddress("mem_ttbb_raw_btag_weight_jj", this->mem_ttbb_raw_btag_weight_jj);
    tree->SetBranchAddress("mem_ttbb_raw_nperm", this->mem_ttbb_raw_nperm);
    tree->SetBranchAddress("mem_ttbb_raw_chi2", this->mem_ttbb_raw_chi2);
    tree->SetBranchAddress("mem_ttbb_raw_p_err", this->mem_ttbb_raw_p_err);
    tree->SetBranchAddress("mem_ttbb_raw_time", this->mem_ttbb_raw_time);
    tree->SetBranchAddress("mem_ttbb_raw_btag_weight_cc", this->mem_ttbb_raw_btag_weight_cc);
    tree->SetBranchAddress("mem_ttbb_raw_p", this->mem_ttbb_raw_p);
    tree->SetBranchAddress("mem_ttbb_raw_efficiency", this->mem_ttbb_raw_efficiency);
    tree->SetBranchAddress("mem_ttbb_raw_btag_weight_bb", this->mem_ttbb_raw_btag_weight_bb);
    tree->SetBranchAddress("mem_ttbb_raw_prefit_code", this->mem_ttbb_raw_prefit_code);
    tree->SetBranchAddress("mem_ttbb_raw_error_code", this->mem_ttbb_raw_error_code);
    tree->SetBranchAddress("nmem_tth_JESUp", &(this->nmem_tth_JESUp));
    tree->SetBranchAddress("mem_tth_JESUp_btag_weight_jj", this->mem_tth_JESUp_btag_weight_jj);
    tree->SetBranchAddress("mem_tth_JESUp_nperm", this->mem_tth_JESUp_nperm);
    tree->SetBranchAddress("mem_tth_JESUp_chi2", this->mem_tth_JESUp_chi2);
    tree->SetBranchAddress("mem_tth_JESUp_p_err", this->mem_tth_JESUp_p_err);
    tree->SetBranchAddress("mem_tth_JESUp_time", this->mem_tth_JESUp_time);
    tree->SetBranchAddress("mem_tth_JESUp_btag_weight_cc", this->mem_tth_JESUp_btag_weight_cc);
    tree->SetBranchAddress("mem_tth_JESUp_p", this->mem_tth_JESUp_p);
    tree->SetBranchAddress("mem_tth_JESUp_efficiency", this->mem_tth_JESUp_efficiency);
    tree->SetBranchAddress("mem_tth_JESUp_btag_weight_bb", this->mem_tth_JESUp_btag_weight_bb);
    tree->SetBranchAddress("mem_tth_JESUp_prefit_code", this->mem_tth_JESUp_prefit_code);
    tree->SetBranchAddress("mem_tth_JESUp_error_code", this->mem_tth_JESUp_error_code);
    tree->SetBranchAddress("nmem_tth_JESDown", &(this->nmem_tth_JESDown));
    tree->SetBranchAddress("mem_tth_JESDown_btag_weight_jj", this->mem_tth_JESDown_btag_weight_jj);
    tree->SetBranchAddress("mem_tth_JESDown_nperm", this->mem_tth_JESDown_nperm);
    tree->SetBranchAddress("mem_tth_JESDown_chi2", this->mem_tth_JESDown_chi2);
    tree->SetBranchAddress("mem_tth_JESDown_p_err", this->mem_tth_JESDown_p_err);
    tree->SetBranchAddress("mem_tth_JESDown_time", this->mem_tth_JESDown_time);
    tree->SetBranchAddress("mem_tth_JESDown_btag_weight_cc", this->mem_tth_JESDown_btag_weight_cc);
    tree->SetBranchAddress("mem_tth_JESDown_p", this->mem_tth_JESDown_p);
    tree->SetBranchAddress("mem_tth_JESDown_efficiency", this->mem_tth_JESDown_efficiency);
    tree->SetBranchAddress("mem_tth_JESDown_btag_weight_bb", this->mem_tth_JESDown_btag_weight_bb);
    tree->SetBranchAddress("mem_tth_JESDown_prefit_code", this->mem_tth_JESDown_prefit_code);
    tree->SetBranchAddress("mem_tth_JESDown_error_code", this->mem_tth_JESDown_error_code);
    tree->SetBranchAddress("nothertopCandidate", &(this->nothertopCandidate));
    tree->SetBranchAddress("othertopCandidate_tau1", this->othertopCandidate_tau1);
    tree->SetBranchAddress("othertopCandidate_phi", this->othertopCandidate_phi);
    tree->SetBranchAddress("othertopCandidate_sjW2btag", this->othertopCandidate_sjW2btag);
    tree->SetBranchAddress("othertopCandidate_sjW2pt", this->othertopCandidate_sjW2pt);
    tree->SetBranchAddress("othertopCandidate_sjW1btag", this->othertopCandidate_sjW1btag);
    tree->SetBranchAddress("othertopCandidate_sjW1mass", this->othertopCandidate_sjW1mass);
    tree->SetBranchAddress("othertopCandidate_sjNonWmass", this->othertopCandidate_sjNonWmass);
    tree->SetBranchAddress("othertopCandidate_sjNonWeta", this->othertopCandidate_sjNonWeta);
    tree->SetBranchAddress("othertopCandidate_pt", this->othertopCandidate_pt);
    tree->SetBranchAddress("othertopCandidate_ptForRoptCalc", this->othertopCandidate_ptForRoptCalc);
    tree->SetBranchAddress("othertopCandidate_tau2", this->othertopCandidate_tau2);
    tree->SetBranchAddress("othertopCandidate_sjW2mass", this->othertopCandidate_sjW2mass);
    tree->SetBranchAddress("othertopCandidate_tau3", this->othertopCandidate_tau3);
    tree->SetBranchAddress("othertopCandidate_sjNonWpt", this->othertopCandidate_sjNonWpt);
    tree->SetBranchAddress("othertopCandidate_mass", this->othertopCandidate_mass);
    tree->SetBranchAddress("othertopCandidate_sjNonWbtag", this->othertopCandidate_sjNonWbtag);
    tree->SetBranchAddress("othertopCandidate_Ropt", this->othertopCandidate_Ropt);
    tree->SetBranchAddress("othertopCandidate_RoptCalc", this->othertopCandidate_RoptCalc);
    tree->SetBranchAddress("othertopCandidate_sjW1phi", this->othertopCandidate_sjW1phi);
    tree->SetBranchAddress("othertopCandidate_sjW1pt", this->othertopCandidate_sjW1pt);
    tree->SetBranchAddress("othertopCandidate_sjNonWphi", this->othertopCandidate_sjNonWphi);
    tree->SetBranchAddress("othertopCandidate_delRopt", this->othertopCandidate_delRopt);
    tree->SetBranchAddress("othertopCandidate_sjW1eta", this->othertopCandidate_sjW1eta);
    tree->SetBranchAddress("othertopCandidate_fRec", this->othertopCandidate_fRec);
    tree->SetBranchAddress("othertopCandidate_sjW2phi", this->othertopCandidate_sjW2phi);
    tree->SetBranchAddress("othertopCandidate_eta", this->othertopCandidate_eta);
    tree->SetBranchAddress("othertopCandidate_n_subjettiness", this->othertopCandidate_n_subjettiness);
    tree->SetBranchAddress("othertopCandidate_bbtag", this->othertopCandidate_bbtag);
    tree->SetBranchAddress("othertopCandidate_sjW2eta", this->othertopCandidate_sjW2eta);
    tree->SetBranchAddress("nfw_aj_JESUp", &(this->nfw_aj_JESUp));
    tree->SetBranchAddress("fw_aj_JESUp_fw_h_alljets_JESUp", this->fw_aj_JESUp_fw_h_alljets_JESUp);
    tree->SetBranchAddress("nleps", &(this->nleps));
    tree->SetBranchAddress("leps_phi", this->leps_phi);
    tree->SetBranchAddress("leps_pt", this->leps_pt);
    tree->SetBranchAddress("leps_pdgId", this->leps_pdgId);
    tree->SetBranchAddress("leps_relIso04", this->leps_relIso04);
    tree->SetBranchAddress("leps_eta", this->leps_eta);
    tree->SetBranchAddress("leps_mass", this->leps_mass);
    tree->SetBranchAddress("leps_relIso03", this->leps_relIso03);
    tree->SetBranchAddress("njets", &(this->njets));
    tree->SetBranchAddress("jets_mcPt", this->jets_mcPt);
    tree->SetBranchAddress("jets_mcEta", this->jets_mcEta);
    tree->SetBranchAddress("jets_mcPhi", this->jets_mcPhi);
    tree->SetBranchAddress("jets_btagCSVInp2t", this->jets_btagCSVInp2t);
    tree->SetBranchAddress("jets_qgl", this->jets_qgl);
    tree->SetBranchAddress("jets_btagCSVRnd3t", this->jets_btagCSVRnd3t);
    tree->SetBranchAddress("jets_id", this->jets_id);
    tree->SetBranchAddress("jets_bTagWeightLFUp", this->jets_bTagWeightLFUp);
    tree->SetBranchAddress("jets_mcNumBHadronsFromTop", this->jets_mcNumBHadronsFromTop);
    tree->SetBranchAddress("jets_mcNumCHadronsFromTop", this->jets_mcNumCHadronsFromTop);
    tree->SetBranchAddress("jets_pt", this->jets_pt);
    tree->SetBranchAddress("jets_mcNumBHadrons", this->jets_mcNumBHadrons);
    tree->SetBranchAddress("jets_mcNumCHadronsAfterTop", this->jets_mcNumCHadronsAfterTop);
    tree->SetBranchAddress("jets_bTagWeightStats2Up", this->jets_bTagWeightStats2Up);
    tree->SetBranchAddress("jets_eta", this->jets_eta);
    tree->SetBranchAddress("jets_btagProb", this->jets_btagProb);
    tree->SetBranchAddress("jets_btagCSVRndge4t", this->jets_btagCSVRndge4t);
    tree->SetBranchAddress("jets_bTagWeightStats1Up", this->jets_bTagWeightStats1Up);
    tree->SetBranchAddress("jets_bTagWeightStats1Down", this->jets_bTagWeightStats1Down);
    tree->SetBranchAddress("jets_mcNumCHadrons", this->jets_mcNumCHadrons);
    tree->SetBranchAddress("jets_matchFlag", this->jets_matchFlag);
    tree->SetBranchAddress("jets_phi", this->jets_phi);
    tree->SetBranchAddress("jets_bTagWeightStats2Down", this->jets_bTagWeightStats2Down);
    tree->SetBranchAddress("jets_bTagWeightLFDown", this->jets_bTagWeightLFDown);
    tree->SetBranchAddress("jets_hadronFlavour", this->jets_hadronFlavour);
    tree->SetBranchAddress("jets_corr_JESUp", this->jets_corr_JESUp);
    tree->SetBranchAddress("jets_bTagWeightJESDown", this->jets_bTagWeightJESDown);
    tree->SetBranchAddress("jets_btagCSVInp3t", this->jets_btagCSVInp3t);
    tree->SetBranchAddress("jets_bTagWeightHFDown", this->jets_bTagWeightHFDown);
    tree->SetBranchAddress("jets_btagSoftMu", this->jets_btagSoftMu);
    tree->SetBranchAddress("jets_btagCSVRnd2t", this->jets_btagCSVRnd2t);
    tree->SetBranchAddress("jets_corr", this->jets_corr);
    tree->SetBranchAddress("jets_btagCMVAV2", this->jets_btagCMVAV2);
    tree->SetBranchAddress("jets_corr_JESDown", this->jets_corr_JESDown);
    tree->SetBranchAddress("jets_btagCSV", this->jets_btagCSV);
    tree->SetBranchAddress("jets_mcM", this->jets_mcM);
    tree->SetBranchAddress("jets_bTagWeightHFUp", this->jets_bTagWeightHFUp);
    tree->SetBranchAddress("jets_mcMatchId", this->jets_mcMatchId);
    tree->SetBranchAddress("jets_mcNumBHadronsAfterTop", this->jets_mcNumBHadronsAfterTop);
    tree->SetBranchAddress("jets_bTagWeight", this->jets_bTagWeight);
    tree->SetBranchAddress("jets_btagSoftEl", this->jets_btagSoftEl);
    tree->SetBranchAddress("jets_mass", this->jets_mass);
    tree->SetBranchAddress("jets_bTagWeightJESUp", this->jets_bTagWeightJESUp);
    tree->SetBranchAddress("jets_mcFlavour", this->jets_mcFlavour);
    tree->SetBranchAddress("jets_btagCSVInpge4t", this->jets_btagCSVInpge4t);
    tree->SetBranchAddress("nfw_bj", &(this->nfw_bj));
    tree->SetBranchAddress("fw_bj_fw_h_btagjets_nominal", this->fw_bj_fw_h_btagjets_nominal);
    tree->SetBranchAddress("nfw_aj_raw", &(this->nfw_aj_raw));
    tree->SetBranchAddress("fw_aj_raw_fw_h_alljets_raw", this->fw_aj_raw_fw_h_alljets_raw);
    tree->SetBranchAddress("nfatjets", &(this->nfatjets));
    tree->SetBranchAddress("fatjets_phi", this->fatjets_phi);
    tree->SetBranchAddress("fatjets_pt", this->fatjets_pt);
    tree->SetBranchAddress("fatjets_tau1", this->fatjets_tau1);
    tree->SetBranchAddress("fatjets_tau2", this->fatjets_tau2);
    tree->SetBranchAddress("fatjets_tau3", this->fatjets_tau3);
    tree->SetBranchAddress("fatjets_eta", this->fatjets_eta);
    tree->SetBranchAddress("fatjets_mass", this->fatjets_mass);
    tree->SetBranchAddress("fatjets_bbtag", this->fatjets_bbtag);
    tree->SetBranchAddress("nhiggsCandidate", &(this->nhiggsCandidate));
    tree->SetBranchAddress("higgsCandidate_phi", this->higgsCandidate_phi);
    tree->SetBranchAddress("higgsCandidate_pt", this->higgsCandidate_pt);
    tree->SetBranchAddress("higgsCandidate_tau1", this->higgsCandidate_tau1);
    tree->SetBranchAddress("higgsCandidate_tau2", this->higgsCandidate_tau2);
    tree->SetBranchAddress("higgsCandidate_tau3", this->higgsCandidate_tau3);
    tree->SetBranchAddress("higgsCandidate_eta", this->higgsCandidate_eta);
    tree->SetBranchAddress("higgsCandidate_n_subjettiness", this->higgsCandidate_n_subjettiness);
    tree->SetBranchAddress("higgsCandidate_bbtag", this->higgsCandidate_bbtag);
    tree->SetBranchAddress("higgsCandidate_mass", this->higgsCandidate_mass);
    tree->SetBranchAddress("nfw_uj_JESUp", &(this->nfw_uj_JESUp));
    tree->SetBranchAddress("fw_uj_JESUp_fw_h_untagjets_JESUp", this->fw_uj_JESUp_fw_h_untagjets_JESUp);
    tree->SetBranchAddress("nmem_tth", &(this->nmem_tth));
    tree->SetBranchAddress("mem_tth_btag_weight_jj", this->mem_tth_btag_weight_jj);
    tree->SetBranchAddress("mem_tth_nperm", this->mem_tth_nperm);
    tree->SetBranchAddress("mem_tth_chi2", this->mem_tth_chi2);
    tree->SetBranchAddress("mem_tth_p_err", this->mem_tth_p_err);
    tree->SetBranchAddress("mem_tth_time", this->mem_tth_time);
    tree->SetBranchAddress("mem_tth_btag_weight_cc", this->mem_tth_btag_weight_cc);
    tree->SetBranchAddress("mem_tth_p", this->mem_tth_p);
    tree->SetBranchAddress("mem_tth_efficiency", this->mem_tth_efficiency);
    tree->SetBranchAddress("mem_tth_btag_weight_bb", this->mem_tth_btag_weight_bb);
    tree->SetBranchAddress("mem_tth_prefit_code", this->mem_tth_prefit_code);
    tree->SetBranchAddress("mem_tth_error_code", this->mem_tth_error_code);
    tree->SetBranchAddress("nfw_bj_raw", &(this->nfw_bj_raw));
    tree->SetBranchAddress("fw_bj_raw_fw_h_btagjets_raw", this->fw_bj_raw_fw_h_btagjets_raw);
    tree->SetBranchAddress("ntopCandidate", &(this->ntopCandidate));
    tree->SetBranchAddress("topCandidate_tau1", this->topCandidate_tau1);
    tree->SetBranchAddress("topCandidate_phi", this->topCandidate_phi);
    tree->SetBranchAddress("topCandidate_sjW2btag", this->topCandidate_sjW2btag);
    tree->SetBranchAddress("topCandidate_sjW2pt", this->topCandidate_sjW2pt);
    tree->SetBranchAddress("topCandidate_sjW1btag", this->topCandidate_sjW1btag);
    tree->SetBranchAddress("topCandidate_sjW1mass", this->topCandidate_sjW1mass);
    tree->SetBranchAddress("topCandidate_sjNonWmass", this->topCandidate_sjNonWmass);
    tree->SetBranchAddress("topCandidate_sjNonWeta", this->topCandidate_sjNonWeta);
    tree->SetBranchAddress("topCandidate_pt", this->topCandidate_pt);
    tree->SetBranchAddress("topCandidate_ptForRoptCalc", this->topCandidate_ptForRoptCalc);
    tree->SetBranchAddress("topCandidate_tau2", this->topCandidate_tau2);
    tree->SetBranchAddress("topCandidate_sjW2mass", this->topCandidate_sjW2mass);
    tree->SetBranchAddress("topCandidate_tau3", this->topCandidate_tau3);
    tree->SetBranchAddress("topCandidate_sjNonWpt", this->topCandidate_sjNonWpt);
    tree->SetBranchAddress("topCandidate_mass", this->topCandidate_mass);
    tree->SetBranchAddress("topCandidate_sjNonWbtag", this->topCandidate_sjNonWbtag);
    tree->SetBranchAddress("topCandidate_Ropt", this->topCandidate_Ropt);
    tree->SetBranchAddress("topCandidate_RoptCalc", this->topCandidate_RoptCalc);
    tree->SetBranchAddress("topCandidate_sjW1phi", this->topCandidate_sjW1phi);
    tree->SetBranchAddress("topCandidate_sjW1pt", this->topCandidate_sjW1pt);
    tree->SetBranchAddress("topCandidate_sjNonWphi", this->topCandidate_sjNonWphi);
    tree->SetBranchAddress("topCandidate_delRopt", this->topCandidate_delRopt);
    tree->SetBranchAddress("topCandidate_sjW1eta", this->topCandidate_sjW1eta);
    tree->SetBranchAddress("topCandidate_fRec", this->topCandidate_fRec);
    tree->SetBranchAddress("topCandidate_sjW2phi", this->topCandidate_sjW2phi);
    tree->SetBranchAddress("topCandidate_eta", this->topCandidate_eta);
    tree->SetBranchAddress("topCandidate_n_subjettiness", this->topCandidate_n_subjettiness);
    tree->SetBranchAddress("topCandidate_bbtag", this->topCandidate_bbtag);
    tree->SetBranchAddress("topCandidate_sjW2eta", this->topCandidate_sjW2eta);
    tree->SetBranchAddress("nfw_bj_JESDown", &(this->nfw_bj_JESDown));
    tree->SetBranchAddress("fw_bj_JESDown_fw_h_btagjets_JESDown", this->fw_bj_JESDown_fw_h_btagjets_JESDown);
    tree->SetBranchAddress("nbRnd_inp_3t_JESDown", &(this->nbRnd_inp_3t_JESDown));
    tree->SetBranchAddress("bRnd_inp_3t_JESDown_p", this->bRnd_inp_3t_JESDown_p);
    tree->SetBranchAddress("bRnd_inp_3t_JESDown_ntoys", this->bRnd_inp_3t_JESDown_ntoys);
    tree->SetBranchAddress("bRnd_inp_3t_JESDown_tag_id", this->bRnd_inp_3t_JESDown_tag_id);
    tree->SetBranchAddress("bRnd_inp_3t_JESDown_pass", this->bRnd_inp_3t_JESDown_pass);
    tree->SetBranchAddress("nbRnd_rnd_3t_JESUp", &(this->nbRnd_rnd_3t_JESUp));
    tree->SetBranchAddress("bRnd_rnd_3t_JESUp_p", this->bRnd_rnd_3t_JESUp_p);
    tree->SetBranchAddress("bRnd_rnd_3t_JESUp_ntoys", this->bRnd_rnd_3t_JESUp_ntoys);
    tree->SetBranchAddress("bRnd_rnd_3t_JESUp_tag_id", this->bRnd_rnd_3t_JESUp_tag_id);
    tree->SetBranchAddress("bRnd_rnd_3t_JESUp_pass", this->bRnd_rnd_3t_JESUp_pass);
    tree->SetBranchAddress("nbRnd_inp_3t_JESUp", &(this->nbRnd_inp_3t_JESUp));
    tree->SetBranchAddress("bRnd_inp_3t_JESUp_p", this->bRnd_inp_3t_JESUp_p);
    tree->SetBranchAddress("bRnd_inp_3t_JESUp_ntoys", this->bRnd_inp_3t_JESUp_ntoys);
    tree->SetBranchAddress("bRnd_inp_3t_JESUp_tag_id", this->bRnd_inp_3t_JESUp_tag_id);
    tree->SetBranchAddress("bRnd_inp_3t_JESUp_pass", this->bRnd_inp_3t_JESUp_pass);
    tree->SetBranchAddress("nbRnd_inp_3t_raw", &(this->nbRnd_inp_3t_raw));
    tree->SetBranchAddress("bRnd_inp_3t_raw_p", this->bRnd_inp_3t_raw_p);
    tree->SetBranchAddress("bRnd_inp_3t_raw_ntoys", this->bRnd_inp_3t_raw_ntoys);
    tree->SetBranchAddress("bRnd_inp_3t_raw_tag_id", this->bRnd_inp_3t_raw_tag_id);
    tree->SetBranchAddress("bRnd_inp_3t_raw_pass", this->bRnd_inp_3t_raw_pass);
    tree->SetBranchAddress("nmet_jetcorr", &(this->nmet_jetcorr));
    tree->SetBranchAddress("met_jetcorr_phi", this->met_jetcorr_phi);
    tree->SetBranchAddress("met_jetcorr_sumEt", this->met_jetcorr_sumEt);
    tree->SetBranchAddress("met_jetcorr_pt", this->met_jetcorr_pt);
    tree->SetBranchAddress("met_jetcorr_px", this->met_jetcorr_px);
    tree->SetBranchAddress("met_jetcorr_py", this->met_jetcorr_py);
    tree->SetBranchAddress("met_jetcorr_genPhi", this->met_jetcorr_genPhi);
    tree->SetBranchAddress("met_jetcorr_genPt", this->met_jetcorr_genPt);
    tree->SetBranchAddress("npv", &(this->npv));
    tree->SetBranchAddress("pv_z", this->pv_z);
    tree->SetBranchAddress("pv_isFake", this->pv_isFake);
    tree->SetBranchAddress("pv_rho", this->pv_rho);
    tree->SetBranchAddress("pv_ndof", this->pv_ndof);
    tree->SetBranchAddress("nbRnd_inp_ge4t_JESUp", &(this->nbRnd_inp_ge4t_JESUp));
    tree->SetBranchAddress("bRnd_inp_ge4t_JESUp_p", this->bRnd_inp_ge4t_JESUp_p);
    tree->SetBranchAddress("bRnd_inp_ge4t_JESUp_ntoys", this->bRnd_inp_ge4t_JESUp_ntoys);
    tree->SetBranchAddress("bRnd_inp_ge4t_JESUp_tag_id", this->bRnd_inp_ge4t_JESUp_tag_id);
    tree->SetBranchAddress("bRnd_inp_ge4t_JESUp_pass", this->bRnd_inp_ge4t_JESUp_pass);
    tree->SetBranchAddress("nll", &(this->nll));
    tree->SetBranchAddress("ll_phi", this->ll_phi);
    tree->SetBranchAddress("ll_eta", this->ll_eta);
    tree->SetBranchAddress("ll_mass", this->ll_mass);
    tree->SetBranchAddress("ll_pt", this->ll_pt);
    tree->SetBranchAddress("nbRnd_rnd_ge4t", &(this->nbRnd_rnd_ge4t));
    tree->SetBranchAddress("bRnd_rnd_ge4t_p", this->bRnd_rnd_ge4t_p);
    tree->SetBranchAddress("bRnd_rnd_ge4t_ntoys", this->bRnd_rnd_ge4t_ntoys);
    tree->SetBranchAddress("bRnd_rnd_ge4t_tag_id", this->bRnd_rnd_ge4t_tag_id);
    tree->SetBranchAddress("bRnd_rnd_ge4t_pass", this->bRnd_rnd_ge4t_pass);
    tree->SetBranchAddress("nbRnd_rnd_ge4t_JESUp", &(this->nbRnd_rnd_ge4t_JESUp));
    tree->SetBranchAddress("bRnd_rnd_ge4t_JESUp_p", this->bRnd_rnd_ge4t_JESUp_p);
    tree->SetBranchAddress("bRnd_rnd_ge4t_JESUp_ntoys", this->bRnd_rnd_ge4t_JESUp_ntoys);
    tree->SetBranchAddress("bRnd_rnd_ge4t_JESUp_tag_id", this->bRnd_rnd_ge4t_JESUp_tag_id);
    tree->SetBranchAddress("bRnd_rnd_ge4t_JESUp_pass", this->bRnd_rnd_ge4t_JESUp_pass);
    tree->SetBranchAddress("nbRnd_inp_ge4t_JESDown", &(this->nbRnd_inp_ge4t_JESDown));
    tree->SetBranchAddress("bRnd_inp_ge4t_JESDown_p", this->bRnd_inp_ge4t_JESDown_p);
    tree->SetBranchAddress("bRnd_inp_ge4t_JESDown_ntoys", this->bRnd_inp_ge4t_JESDown_ntoys);
    tree->SetBranchAddress("bRnd_inp_ge4t_JESDown_tag_id", this->bRnd_inp_ge4t_JESDown_tag_id);
    tree->SetBranchAddress("bRnd_inp_ge4t_JESDown_pass", this->bRnd_inp_ge4t_JESDown_pass);
    tree->SetBranchAddress("nbRnd_rnd_ge4t_JESDown", &(this->nbRnd_rnd_ge4t_JESDown));
    tree->SetBranchAddress("bRnd_rnd_ge4t_JESDown_p", this->bRnd_rnd_ge4t_JESDown_p);
    tree->SetBranchAddress("bRnd_rnd_ge4t_JESDown_ntoys", this->bRnd_rnd_ge4t_JESDown_ntoys);
    tree->SetBranchAddress("bRnd_rnd_ge4t_JESDown_tag_id", this->bRnd_rnd_ge4t_JESDown_tag_id);
    tree->SetBranchAddress("bRnd_rnd_ge4t_JESDown_pass", this->bRnd_rnd_ge4t_JESDown_pass);
    tree->SetBranchAddress("nmet", &(this->nmet));
    tree->SetBranchAddress("met_phi", this->met_phi);
    tree->SetBranchAddress("met_sumEt", this->met_sumEt);
    tree->SetBranchAddress("met_pt", this->met_pt);
    tree->SetBranchAddress("met_px", this->met_px);
    tree->SetBranchAddress("met_py", this->met_py);
    tree->SetBranchAddress("met_genPhi", this->met_genPhi);
    tree->SetBranchAddress("met_genPt", this->met_genPt);
    tree->SetBranchAddress("nbRnd_inp_ge4t", &(this->nbRnd_inp_ge4t));
    tree->SetBranchAddress("bRnd_inp_ge4t_p", this->bRnd_inp_ge4t_p);
    tree->SetBranchAddress("bRnd_inp_ge4t_ntoys", this->bRnd_inp_ge4t_ntoys);
    tree->SetBranchAddress("bRnd_inp_ge4t_tag_id", this->bRnd_inp_ge4t_tag_id);
    tree->SetBranchAddress("bRnd_inp_ge4t_pass", this->bRnd_inp_ge4t_pass);
    tree->SetBranchAddress("nbRnd_rnd_ge4t_raw", &(this->nbRnd_rnd_ge4t_raw));
    tree->SetBranchAddress("bRnd_rnd_ge4t_raw_p", this->bRnd_rnd_ge4t_raw_p);
    tree->SetBranchAddress("bRnd_rnd_ge4t_raw_ntoys", this->bRnd_rnd_ge4t_raw_ntoys);
    tree->SetBranchAddress("bRnd_rnd_ge4t_raw_tag_id", this->bRnd_rnd_ge4t_raw_tag_id);
    tree->SetBranchAddress("bRnd_rnd_ge4t_raw_pass", this->bRnd_rnd_ge4t_raw_pass);
    tree->SetBranchAddress("nbRnd_inp_3t", &(this->nbRnd_inp_3t));
    tree->SetBranchAddress("bRnd_inp_3t_p", this->bRnd_inp_3t_p);
    tree->SetBranchAddress("bRnd_inp_3t_ntoys", this->bRnd_inp_3t_ntoys);
    tree->SetBranchAddress("bRnd_inp_3t_tag_id", this->bRnd_inp_3t_tag_id);
    tree->SetBranchAddress("bRnd_inp_3t_pass", this->bRnd_inp_3t_pass);
    tree->SetBranchAddress("nmet_ttbar_gen", &(this->nmet_ttbar_gen));
    tree->SetBranchAddress("met_ttbar_gen_phi", this->met_ttbar_gen_phi);
    tree->SetBranchAddress("met_ttbar_gen_sumEt", this->met_ttbar_gen_sumEt);
    tree->SetBranchAddress("met_ttbar_gen_pt", this->met_ttbar_gen_pt);
    tree->SetBranchAddress("met_ttbar_gen_px", this->met_ttbar_gen_px);
    tree->SetBranchAddress("met_ttbar_gen_py", this->met_ttbar_gen_py);
    tree->SetBranchAddress("met_ttbar_gen_genPhi", this->met_ttbar_gen_genPhi);
    tree->SetBranchAddress("met_ttbar_gen_genPt", this->met_ttbar_gen_genPt);
    tree->SetBranchAddress("nbRnd_rnd_3t_raw", &(this->nbRnd_rnd_3t_raw));
    tree->SetBranchAddress("bRnd_rnd_3t_raw_p", this->bRnd_rnd_3t_raw_p);
    tree->SetBranchAddress("bRnd_rnd_3t_raw_ntoys", this->bRnd_rnd_3t_raw_ntoys);
    tree->SetBranchAddress("bRnd_rnd_3t_raw_tag_id", this->bRnd_rnd_3t_raw_tag_id);
    tree->SetBranchAddress("bRnd_rnd_3t_raw_pass", this->bRnd_rnd_3t_raw_pass);
    tree->SetBranchAddress("nbRnd_rnd_3t", &(this->nbRnd_rnd_3t));
    tree->SetBranchAddress("bRnd_rnd_3t_p", this->bRnd_rnd_3t_p);
    tree->SetBranchAddress("bRnd_rnd_3t_ntoys", this->bRnd_rnd_3t_ntoys);
    tree->SetBranchAddress("bRnd_rnd_3t_tag_id", this->bRnd_rnd_3t_tag_id);
    tree->SetBranchAddress("bRnd_rnd_3t_pass", this->bRnd_rnd_3t_pass);
    tree->SetBranchAddress("nbRnd_inp_ge4t_raw", &(this->nbRnd_inp_ge4t_raw));
    tree->SetBranchAddress("bRnd_inp_ge4t_raw_p", this->bRnd_inp_ge4t_raw_p);
    tree->SetBranchAddress("bRnd_inp_ge4t_raw_ntoys", this->bRnd_inp_ge4t_raw_ntoys);
    tree->SetBranchAddress("bRnd_inp_ge4t_raw_tag_id", this->bRnd_inp_ge4t_raw_tag_id);
    tree->SetBranchAddress("bRnd_inp_ge4t_raw_pass", this->bRnd_inp_ge4t_raw_pass);
    tree->SetBranchAddress("nbRnd_rnd_3t_JESDown", &(this->nbRnd_rnd_3t_JESDown));
    tree->SetBranchAddress("bRnd_rnd_3t_JESDown_p", this->bRnd_rnd_3t_JESDown_p);
    tree->SetBranchAddress("bRnd_rnd_3t_JESDown_ntoys", this->bRnd_rnd_3t_JESDown_ntoys);
    tree->SetBranchAddress("bRnd_rnd_3t_JESDown_tag_id", this->bRnd_rnd_3t_JESDown_tag_id);
    tree->SetBranchAddress("bRnd_rnd_3t_JESDown_pass", this->bRnd_rnd_3t_JESDown_pass);
    tree->SetBranchAddress("nmet_gen", &(this->nmet_gen));
    tree->SetBranchAddress("met_gen_phi", this->met_gen_phi);
    tree->SetBranchAddress("met_gen_sumEt", this->met_gen_sumEt);
    tree->SetBranchAddress("met_gen_pt", this->met_gen_pt);
    tree->SetBranchAddress("met_gen_px", this->met_gen_px);
    tree->SetBranchAddress("met_gen_py", this->met_gen_py);
    tree->SetBranchAddress("met_gen_genPhi", this->met_gen_genPhi);
    tree->SetBranchAddress("met_gen_genPt", this->met_gen_genPt);
    tree->SetBranchAddress("std_bdisc_btag_JESDown", &(this->std_bdisc_btag_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_raw", &(this->qg_LR_flavour_4q_1q_raw));
    tree->SetBranchAddress("mean_bdisc_btag", &(this->mean_bdisc_btag));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v", &(this->HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v));
    tree->SetBranchAddress("bTagWeight_Stats2Down", &(this->bTagWeight_Stats2Down));
    tree->SetBranchAddress("min_dr_btag_JESDown", &(this->min_dr_btag_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_3q_JESUp", &(this->qg_LR_flavour_4q_1q_2q_3q_JESUp));
    tree->SetBranchAddress("ht_raw", &(this->ht_raw));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_3q", &(this->qg_LR_flavour_4q_0q_1q_2q_3q));
    tree->SetBranchAddress("C_JESDown", &(this->C_JESDown));
    tree->SetBranchAddress("btag_lr_4b_Rndge4t_JESDown", &(this->btag_lr_4b_Rndge4t_JESDown));
    tree->SetBranchAddress("passes_jet_JESUp", &(this->passes_jet_JESUp));
    tree->SetBranchAddress("momentum_eig2_JESDown", &(this->momentum_eig2_JESDown));
    tree->SetBranchAddress("mean_dr_btag_JESDown", &(this->mean_dr_btag_JESDown));
    tree->SetBranchAddress("pt_drpair_btag_JESDown", &(this->pt_drpair_btag_JESDown));
    tree->SetBranchAddress("is_dl_JESUp", &(this->is_dl_JESUp));
    tree->SetBranchAddress("weight_xs", &(this->weight_xs));
    tree->SetBranchAddress("nMatch_hb_raw", &(this->nMatch_hb_raw));
    tree->SetBranchAddress("btag_lr_4b_Inpge4t", &(this->btag_lr_4b_Inpge4t));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_JESUp", &(this->qg_LR_flavour_4q_0q_1q_2q_JESUp));
    tree->SetBranchAddress("pt_drpair_btag", &(this->pt_drpair_btag));
    tree->SetBranchAddress("nBCSVT_raw", &(this->nBCSVT_raw));
    tree->SetBranchAddress("ht_JESDown", &(this->ht_JESDown));
    tree->SetBranchAddress("bTagWeight_Stats2Up", &(this->bTagWeight_Stats2Up));
    tree->SetBranchAddress("btag_lr_2b_Rnd3t_JESDown", &(this->btag_lr_2b_Rnd3t_JESDown));
    tree->SetBranchAddress("nMatch_hb_btag_raw", &(this->nMatch_hb_btag_raw));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_3q_JESDown", &(this->qg_LR_flavour_4q_0q_1q_2q_3q_JESDown));
    tree->SetBranchAddress("std_bdisc_btag", &(this->std_bdisc_btag));
    tree->SetBranchAddress("sphericity", &(this->sphericity));
    tree->SetBranchAddress("nMatchSimB_JESUp", &(this->nMatchSimB_JESUp));
    tree->SetBranchAddress("btag_LR_4b_2b_Inp3t_JESUp", &(this->btag_LR_4b_2b_Inp3t_JESUp));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v", &(this->HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v));
    tree->SetBranchAddress("passes_btag_JESDown", &(this->passes_btag_JESDown));
    tree->SetBranchAddress("btag_lr_4b", &(this->btag_lr_4b));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q", &(this->qg_LR_flavour_4q_0q_1q_2q));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q", &(this->qg_LR_flavour_4q_1q_2q));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_JESUp", &(this->qg_LR_flavour_4q_1q_JESUp));
    tree->SetBranchAddress("nBCSVM_raw", &(this->nBCSVM_raw));
    tree->SetBranchAddress("btag_lr_4b_Inpge4t_JESDown", &(this->btag_lr_4b_Inpge4t_JESDown));
    tree->SetBranchAddress("nBCSVL_JESUp", &(this->nBCSVL_JESUp));
    tree->SetBranchAddress("Wmass_raw", &(this->Wmass_raw));
    tree->SetBranchAddress("std_dr_btag_raw", &(this->std_dr_btag_raw));
    tree->SetBranchAddress("isotropy_JESDown", &(this->isotropy_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q", &(this->qg_LR_flavour_4q_1q));
    tree->SetBranchAddress("mean_bdisc_btag_JESUp", &(this->mean_bdisc_btag_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_JESDown", &(this->qg_LR_flavour_4q_0q_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_3q_JESUp", &(this->qg_LR_flavour_4q_3q_JESUp));
    tree->SetBranchAddress("momentum_eig2", &(this->momentum_eig2));
    tree->SetBranchAddress("momentum_eig1", &(this->momentum_eig1));
    tree->SetBranchAddress("momentum_eig0", &(this->momentum_eig0));
    tree->SetBranchAddress("momentum_eig0_JESDown", &(this->momentum_eig0_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_3q_raw", &(this->qg_LR_flavour_4q_1q_2q_3q_raw));
    tree->SetBranchAddress("std_bdisc_JESUp", &(this->std_bdisc_JESUp));
    tree->SetBranchAddress("bTagWeight_JESUp", &(this->bTagWeight_JESUp));
    tree->SetBranchAddress("nMatch_tb_raw", &(this->nMatch_tb_raw));
    tree->SetBranchAddress("cat_btag", &(this->cat_btag));
    tree->SetBranchAddress("btag_lr_2b_Rndge4t_JESDown", &(this->btag_lr_2b_Rndge4t_JESDown));
    tree->SetBranchAddress("btag_lr_2b_JESDown", &(this->btag_lr_2b_JESDown));
    tree->SetBranchAddress("bTagWeight_HFDown", &(this->bTagWeight_HFDown));
    tree->SetBranchAddress("btag_lr_2b_Inpge4t", &(this->btag_lr_2b_Inpge4t));
    tree->SetBranchAddress("btag_lr_2b_Inp3t", &(this->btag_lr_2b_Inp3t));
    tree->SetBranchAddress("is_dl_raw", &(this->is_dl_raw));
    tree->SetBranchAddress("bTagWeight_Stats1Down", &(this->bTagWeight_Stats1Down));
    tree->SetBranchAddress("cat_btag_JESUp", &(this->cat_btag_JESUp));
    tree->SetBranchAddress("isotropy", &(this->isotropy));
    tree->SetBranchAddress("eta_drpair_btag_raw", &(this->eta_drpair_btag_raw));
    tree->SetBranchAddress("btag_LR_4b_2b_Rnd3t_raw", &(this->btag_LR_4b_2b_Rnd3t_raw));
    tree->SetBranchAddress("bTagWeight", &(this->bTagWeight));
    tree->SetBranchAddress("nMatchSimC_raw", &(this->nMatchSimC_raw));
    tree->SetBranchAddress("aplanarity_raw", &(this->aplanarity_raw));
    tree->SetBranchAddress("btag_LR_4b_2b_Inpge4t_raw", &(this->btag_LR_4b_2b_Inpge4t_raw));
    tree->SetBranchAddress("is_fh", &(this->is_fh));
    tree->SetBranchAddress("n_boosted_bjets", &(this->n_boosted_bjets));
    tree->SetBranchAddress("mass_drpair_btag_raw", &(this->mass_drpair_btag_raw));
    tree->SetBranchAddress("btag_lr_4b_Inp3t_raw", &(this->btag_lr_4b_Inp3t_raw));
    tree->SetBranchAddress("eta_drpair_btag", &(this->eta_drpair_btag));
    tree->SetBranchAddress("is_sl_raw", &(this->is_sl_raw));
    tree->SetBranchAddress("btag_LR_4b_2b_raw", &(this->btag_LR_4b_2b_raw));
    tree->SetBranchAddress("btag_LR_4b_2b_Rnd3t_JESUp", &(this->btag_LR_4b_2b_Rnd3t_JESUp));
    tree->SetBranchAddress("passes_jet_raw", &(this->passes_jet_raw));
    tree->SetBranchAddress("eta_drpair_btag_JESUp", &(this->eta_drpair_btag_JESUp));
    tree->SetBranchAddress("nBCSVL_JESDown", &(this->nBCSVL_JESDown));
    tree->SetBranchAddress("n_bjets", &(this->n_bjets));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_raw", &(this->qg_LR_flavour_4q_0q_raw));
    tree->SetBranchAddress("numJets", &(this->numJets));
    tree->SetBranchAddress("btag_lr_2b", &(this->btag_lr_2b));
    tree->SetBranchAddress("btag_LR_4b_2b_Inpge4t_JESDown", &(this->btag_LR_4b_2b_Inpge4t_JESDown));
    tree->SetBranchAddress("nMatch_wq_btag_JESUp", &(this->nMatch_wq_btag_JESUp));
    tree->SetBranchAddress("btag_lr_2b_Rndge4t_raw", &(this->btag_lr_2b_Rndge4t_raw));
    tree->SetBranchAddress("n_ljets", &(this->n_ljets));
    tree->SetBranchAddress("nBCSVL_raw", &(this->nBCSVL_raw));
    tree->SetBranchAddress("n_excluded_ljets", &(this->n_excluded_ljets));
    tree->SetBranchAddress("min_dr_btag", &(this->min_dr_btag));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_JESDown", &(this->qg_LR_flavour_4q_0q_1q_JESDown));
    tree->SetBranchAddress("btag_lr_2b_Inp3t_JESUp", &(this->btag_lr_2b_Inp3t_JESUp));
    tree->SetBranchAddress("Wmass", &(this->Wmass));
    tree->SetBranchAddress("nMatchSimB_raw", &(this->nMatchSimB_raw));
    tree->SetBranchAddress("cat_JESDown", &(this->cat_JESDown));
    tree->SetBranchAddress("nMatchSimC_JESUp", &(this->nMatchSimC_JESUp));
    tree->SetBranchAddress("btag_lr_2b_Rnd3t", &(this->btag_lr_2b_Rnd3t));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_JESDown", &(this->qg_LR_flavour_4q_1q_2q_JESDown));
    tree->SetBranchAddress("nMatch_wq_JESDown", &(this->nMatch_wq_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_JESUp", &(this->qg_LR_flavour_4q_0q_1q_JESUp));
    tree->SetBranchAddress("momentum_eig2_JESUp", &(this->momentum_eig2_JESUp));
    tree->SetBranchAddress("nMatch_wq_btag_JESDown", &(this->nMatch_wq_btag_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_JESDown", &(this->qg_LR_flavour_4q_2q_JESDown));
    tree->SetBranchAddress("std_bdisc_btag_JESUp", &(this->std_bdisc_btag_JESUp));
    tree->SetBranchAddress("cat_btag_JESDown", &(this->cat_btag_JESDown));
    tree->SetBranchAddress("is_fh_JESDown", &(this->is_fh_JESDown));
    tree->SetBranchAddress("btag_lr_2b_Inp3t_JESDown", &(this->btag_lr_2b_Inp3t_JESDown));
    tree->SetBranchAddress("btag_lr_4b_Rndge4t_raw", &(this->btag_lr_4b_Rndge4t_raw));
    tree->SetBranchAddress("C", &(this->C));
    tree->SetBranchAddress("pt_drpair_btag_raw", &(this->pt_drpair_btag_raw));
    tree->SetBranchAddress("nBCSVT_JESDown", &(this->nBCSVT_JESDown));
    tree->SetBranchAddress("aplanarity", &(this->aplanarity));
    tree->SetBranchAddress("btag_LR_4b_2b_Inp3t_JESDown", &(this->btag_LR_4b_2b_Inp3t_JESDown));
    tree->SetBranchAddress("is_sl_JESDown", &(this->is_sl_JESDown));
    tree->SetBranchAddress("std_dr_btag", &(this->std_dr_btag));
    tree->SetBranchAddress("momentum_eig1_raw", &(this->momentum_eig1_raw));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_JESDown", &(this->qg_LR_flavour_4q_1q_JESDown));
    tree->SetBranchAddress("btag_LR_4b_2b_Inp3t", &(this->btag_LR_4b_2b_Inp3t));
    tree->SetBranchAddress("numJets_JESUp", &(this->numJets_JESUp));
    tree->SetBranchAddress("passes_btag_raw", &(this->passes_btag_raw));
    tree->SetBranchAddress("is_sl", &(this->is_sl));
    tree->SetBranchAddress("tth_mva", &(this->tth_mva));    
    tree->SetBranchAddress("mean_bdisc_btag_raw", &(this->mean_bdisc_btag_raw));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_3q_JESDown", &(this->qg_LR_flavour_4q_1q_2q_3q_JESDown));
    tree->SetBranchAddress("std_bdisc", &(this->std_bdisc));
    tree->SetBranchAddress("btag_lr_4b_Rnd3t_JESDown", &(this->btag_lr_4b_Rnd3t_JESDown));
    tree->SetBranchAddress("btag_LR_4b_2b_JESUp", &(this->btag_LR_4b_2b_JESUp));
    tree->SetBranchAddress("mass_drpair_btag_JESDown", &(this->mass_drpair_btag_JESDown));
    tree->SetBranchAddress("mean_bdisc_JESUp", &(this->mean_bdisc_JESUp));
    tree->SetBranchAddress("btag_lr_4b_Inp3t_JESUp", &(this->btag_lr_4b_Inp3t_JESUp));
    tree->SetBranchAddress("btag_lr_4b_Rnd3t_JESUp", &(this->btag_lr_4b_Rnd3t_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_3q_JESDown", &(this->qg_LR_flavour_4q_2q_3q_JESDown));
    tree->SetBranchAddress("cat_raw", &(this->cat_raw));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_3q_JESUp", &(this->qg_LR_flavour_4q_2q_3q_JESUp));
    tree->SetBranchAddress("passPV", &(this->passPV));
    tree->SetBranchAddress("triggerBitmask", &(this->triggerBitmask));
    tree->SetBranchAddress("btag_lr_2b_Rndge4t", &(this->btag_lr_2b_Rndge4t));
    tree->SetBranchAddress("D_raw", &(this->D_raw));
    tree->SetBranchAddress("bTagWeight_LFUp", &(this->bTagWeight_LFUp));
    tree->SetBranchAddress("cat_btag_raw", &(this->cat_btag_raw));
    tree->SetBranchAddress("btag_LR_4b_2b_Rnd3t_JESDown", &(this->btag_LR_4b_2b_Rnd3t_JESDown));
    tree->SetBranchAddress("nMatchSimC_JESDown", &(this->nMatchSimC_JESDown));
    tree->SetBranchAddress("nBCSVM_JESUp", &(this->nBCSVM_JESUp));
    tree->SetBranchAddress("mean_bdisc_raw", &(this->mean_bdisc_raw));
    tree->SetBranchAddress("ttCls", &(this->ttCls));
    tree->SetBranchAddress("triggerDecision", &(this->triggerDecision));
    tree->SetBranchAddress("nMatch_tb_JESDown", &(this->nMatch_tb_JESDown));
    tree->SetBranchAddress("btag_lr_4b_JESDown", &(this->btag_lr_4b_JESDown));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v", &(this->HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v));
    tree->SetBranchAddress("min_dr_btag_JESUp", &(this->min_dr_btag_JESUp));
    tree->SetBranchAddress("std_bdisc_btag_raw", &(this->std_bdisc_btag_raw));
    tree->SetBranchAddress("pt_drpair_btag_JESUp", &(this->pt_drpair_btag_JESUp));
    tree->SetBranchAddress("mean_bdisc_btag_JESDown", &(this->mean_bdisc_btag_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_3q", &(this->qg_LR_flavour_4q_3q));
    tree->SetBranchAddress("btag_lr_2b_Inp3t_raw", &(this->btag_lr_2b_Inp3t_raw));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_3q", &(this->qg_LR_flavour_4q_2q_3q));
    tree->SetBranchAddress("btag_lr_2b_JESUp", &(this->btag_lr_2b_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_3q_raw", &(this->qg_LR_flavour_4q_2q_3q_raw));
    tree->SetBranchAddress("C_raw", &(this->C_raw));
    tree->SetBranchAddress("nBCSVT", &(this->nBCSVT));
    tree->SetBranchAddress("nMatch_hb_btag_JESUp", &(this->nMatch_hb_btag_JESUp));
    tree->SetBranchAddress("btag_LR_4b_2b_Inp3t_raw", &(this->btag_LR_4b_2b_Inp3t_raw));
    tree->SetBranchAddress("std_bdisc_raw", &(this->std_bdisc_raw));
    tree->SetBranchAddress("cat_gen_raw", &(this->cat_gen_raw));
    tree->SetBranchAddress("nGenQW", &(this->nGenQW));
    tree->SetBranchAddress("nMatch_wq_JESUp", &(this->nMatch_wq_JESUp));
    tree->SetBranchAddress("momentum_eig1_JESUp", &(this->momentum_eig1_JESUp));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v", &(this->HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_raw", &(this->qg_LR_flavour_4q_2q_raw));
    tree->SetBranchAddress("aplanarity_JESUp", &(this->aplanarity_JESUp));
    tree->SetBranchAddress("nMatch_tb_btag", &(this->nMatch_tb_btag));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_JESUp", &(this->qg_LR_flavour_4q_0q_JESUp));
    tree->SetBranchAddress("nMatch_hb", &(this->nMatch_hb));
    tree->SetBranchAddress("btag_lr_2b_Inpge4t_JESUp", &(this->btag_lr_2b_Inpge4t_JESUp));
    tree->SetBranchAddress("nBCSVL", &(this->nBCSVL));
    tree->SetBranchAddress("nBCSVM", &(this->nBCSVM));
    tree->SetBranchAddress("cat_gen", &(this->cat_gen));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele27_eta2p1_WP85_Gsf_HT200_v", &(this->HLT_BIT_HLT_Ele27_eta2p1_WP85_Gsf_HT200_v));
    tree->SetBranchAddress("passes_btag_JESUp", &(this->passes_btag_JESUp));
    tree->SetBranchAddress("sphericity_JESUp", &(this->sphericity_JESUp));
    tree->SetBranchAddress("numJets_raw", &(this->numJets_raw));
    tree->SetBranchAddress("is_fh_JESUp", &(this->is_fh_JESUp));
    tree->SetBranchAddress("sphericity_raw", &(this->sphericity_raw));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_3q", &(this->qg_LR_flavour_4q_1q_2q_3q));
    tree->SetBranchAddress("ht", &(this->ht));
    tree->SetBranchAddress("btag_LR_4b_2b_Rndge4t_JESDown", &(this->btag_LR_4b_2b_Rndge4t_JESDown));
    tree->SetBranchAddress("btag_lr_4b_Rnd3t_raw", &(this->btag_lr_4b_Rnd3t_raw));
    tree->SetBranchAddress("btag_lr_4b_Rnd3t", &(this->btag_lr_4b_Rnd3t));
    tree->SetBranchAddress("passes_jet_JESDown", &(this->passes_jet_JESDown));
    tree->SetBranchAddress("nMatch_wq_btag", &(this->nMatch_wq_btag));
    tree->SetBranchAddress("btag_lr_4b_JESUp", &(this->btag_lr_4b_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_raw", &(this->qg_LR_flavour_4q_0q_1q_raw));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q", &(this->qg_LR_flavour_4q_2q));
    tree->SetBranchAddress("nMatch_tb_JESUp", &(this->nMatch_tb_JESUp));
    tree->SetBranchAddress("sphericity_JESDown", &(this->sphericity_JESDown));
    tree->SetBranchAddress("cat_gen_JESDown", &(this->cat_gen_JESDown));
    tree->SetBranchAddress("mean_bdisc", &(this->mean_bdisc));
    tree->SetBranchAddress("mass_drpair_btag", &(this->mass_drpair_btag));
    tree->SetBranchAddress("momentum_eig1_JESDown", &(this->momentum_eig1_JESDown));
    tree->SetBranchAddress("mass_drpair_btag_JESUp", &(this->mass_drpair_btag_JESUp));
    tree->SetBranchAddress("is_dl_JESDown", &(this->is_dl_JESDown));
    tree->SetBranchAddress("bTagWeight_LFDown", &(this->bTagWeight_LFDown));
    tree->SetBranchAddress("btag_lr_4b_Inp3t", &(this->btag_lr_4b_Inp3t));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_JESUp", &(this->qg_LR_flavour_4q_2q_JESUp));
    tree->SetBranchAddress("is_sl_JESUp", &(this->is_sl_JESUp));
    tree->SetBranchAddress("momentum_eig2_raw", &(this->momentum_eig2_raw));
    tree->SetBranchAddress("cat", &(this->cat));
    tree->SetBranchAddress("nMatchSimB_JESDown", &(this->nMatchSimB_JESDown));
    tree->SetBranchAddress("btag_LR_4b_2b_Rnd3t", &(this->btag_LR_4b_2b_Rnd3t));
    tree->SetBranchAddress("nMatch_tb_btag_raw", &(this->nMatch_tb_btag_raw));
    tree->SetBranchAddress("btag_LR_4b_2b", &(this->btag_LR_4b_2b));
    tree->SetBranchAddress("qg_LR_flavour_4q_3q_raw", &(this->qg_LR_flavour_4q_3q_raw));
    tree->SetBranchAddress("btag_LR_4b_2b_Rndge4t_raw", &(this->btag_LR_4b_2b_Rndge4t_raw));
    tree->SetBranchAddress("nMatch_wq", &(this->nMatch_wq));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_raw", &(this->qg_LR_flavour_4q_0q_1q_2q_raw));
    tree->SetBranchAddress("numJets_JESDown", &(this->numJets_JESDown));
    tree->SetBranchAddress("nMatchSimB", &(this->nMatchSimB));
    tree->SetBranchAddress("nMatchSimC", &(this->nMatchSimC));
    tree->SetBranchAddress("nMatch_wq_btag_raw", &(this->nMatch_wq_btag_raw));
    tree->SetBranchAddress("qg_LR_flavour_4q_3q_JESDown", &(this->qg_LR_flavour_4q_3q_JESDown));
    tree->SetBranchAddress("nMatch_tb_btag_JESDown", &(this->nMatch_tb_btag_JESDown));
    tree->SetBranchAddress("btag_LR_4b_2b_Inpge4t", &(this->btag_LR_4b_2b_Inpge4t));
    tree->SetBranchAddress("nMatch_hb_JESUp", &(this->nMatch_hb_JESUp));
    tree->SetBranchAddress("btag_LR_4b_2b_Inpge4t_JESUp", &(this->btag_LR_4b_2b_Inpge4t_JESUp));
    tree->SetBranchAddress("btag_lr_4b_Rndge4t", &(this->btag_lr_4b_Rndge4t));
    tree->SetBranchAddress("nMatch_wq_raw", &(this->nMatch_wq_raw));
    tree->SetBranchAddress("bTagWeight_JESDown", &(this->bTagWeight_JESDown));
    tree->SetBranchAddress("ht_JESUp", &(this->ht_JESUp));
    tree->SetBranchAddress("btag_lr_4b_raw", &(this->btag_lr_4b_raw));
    tree->SetBranchAddress("std_dr_btag_JESUp", &(this->std_dr_btag_JESUp));
    tree->SetBranchAddress("btag_lr_2b_Rndge4t_JESUp", &(this->btag_lr_2b_Rndge4t_JESUp));
    tree->SetBranchAddress("isotropy_raw", &(this->isotropy_raw));
    tree->SetBranchAddress("n_boosted_ljets", &(this->n_boosted_ljets));
    tree->SetBranchAddress("nBCSVT_JESUp", &(this->nBCSVT_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q", &(this->qg_LR_flavour_4q_0q_1q));
    tree->SetBranchAddress("D", &(this->D));
    tree->SetBranchAddress("nMatch_hb_btag", &(this->nMatch_hb_btag));
    tree->SetBranchAddress("mean_bdisc_JESDown", &(this->mean_bdisc_JESDown));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v", &(this->HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v));
    tree->SetBranchAddress("btag_lr_2b_Rnd3t_JESUp", &(this->btag_lr_2b_Rnd3t_JESUp));
    tree->SetBranchAddress("btag_lr_2b_Rnd3t_raw", &(this->btag_lr_2b_Rnd3t_raw));
    tree->SetBranchAddress("mean_dr_btag", &(this->mean_dr_btag));
    tree->SetBranchAddress("aplanarity_JESDown", &(this->aplanarity_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_raw", &(this->qg_LR_flavour_4q_1q_2q_raw));
    tree->SetBranchAddress("nGenBHiggs", &(this->nGenBHiggs));
    tree->SetBranchAddress("isotropy_JESUp", &(this->isotropy_JESUp));
    tree->SetBranchAddress("std_dr_btag_JESDown", &(this->std_dr_btag_JESDown));
    tree->SetBranchAddress("bTagWeight_Stats1Up", &(this->bTagWeight_Stats1Up));
    tree->SetBranchAddress("Wmass_JESDown", &(this->Wmass_JESDown));
    tree->SetBranchAddress("cat_gen_JESUp", &(this->cat_gen_JESUp));
    tree->SetBranchAddress("momentum_eig0_JESUp", &(this->momentum_eig0_JESUp));
    tree->SetBranchAddress("btag_LR_4b_2b_Rndge4t_JESUp", &(this->btag_LR_4b_2b_Rndge4t_JESUp));
    tree->SetBranchAddress("btag_LR_4b_2b_JESDown", &(this->btag_LR_4b_2b_JESDown));
    tree->SetBranchAddress("btag_lr_4b_Inpge4t_JESUp", &(this->btag_lr_4b_Inpge4t_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_3q_JESUp", &(this->qg_LR_flavour_4q_0q_1q_2q_3q_JESUp));
    tree->SetBranchAddress("btag_lr_4b_Inp3t_JESDown", &(this->btag_lr_4b_Inp3t_JESDown));
    tree->SetBranchAddress("btag_lr_4b_Inpge4t_raw", &(this->btag_lr_4b_Inpge4t_raw));
    tree->SetBranchAddress("btag_lr_2b_Inpge4t_JESDown", &(this->btag_lr_2b_Inpge4t_JESDown));
    tree->SetBranchAddress("D_JESDown", &(this->D_JESDown));
    tree->SetBranchAddress("bTagWeight_HFUp", &(this->bTagWeight_HFUp));
    tree->SetBranchAddress("btag_lr_2b_Inpge4t_raw", &(this->btag_lr_2b_Inpge4t_raw));
    tree->SetBranchAddress("min_dr_btag_raw", &(this->min_dr_btag_raw));
    tree->SetBranchAddress("is_fh_raw", &(this->is_fh_raw));
    tree->SetBranchAddress("Wmass_JESUp", &(this->Wmass_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_JESUp", &(this->qg_LR_flavour_4q_1q_2q_JESUp));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoMu24_eta2p1_v", &(this->HLT_BIT_HLT_IsoMu24_eta2p1_v));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q", &(this->qg_LR_flavour_4q_0q));
    tree->SetBranchAddress("btag_lr_4b_Rndge4t_JESUp", &(this->btag_lr_4b_Rndge4t_JESUp));
    tree->SetBranchAddress("btag_LR_4b_2b_Rndge4t", &(this->btag_LR_4b_2b_Rndge4t));
    tree->SetBranchAddress("n_excluded_bjets", &(this->n_excluded_bjets));
    tree->SetBranchAddress("nMatch_hb_btag_JESDown", &(this->nMatch_hb_btag_JESDown));
    tree->SetBranchAddress("btag_lr_2b_raw", &(this->btag_lr_2b_raw));
    tree->SetBranchAddress("momentum_eig0_raw", &(this->momentum_eig0_raw));
    tree->SetBranchAddress("nBCSVM_JESDown", &(this->nBCSVM_JESDown));
    tree->SetBranchAddress("nMatch_tb_btag_JESUp", &(this->nMatch_tb_btag_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_3q_raw", &(this->qg_LR_flavour_4q_0q_1q_2q_3q_raw));
    tree->SetBranchAddress("std_bdisc_JESDown", &(this->std_bdisc_JESDown));
    tree->SetBranchAddress("eta_drpair_btag_JESDown", &(this->eta_drpair_btag_JESDown));
    tree->SetBranchAddress("passes_btag", &(this->passes_btag));
    tree->SetBranchAddress("nMatch_hb_JESDown", &(this->nMatch_hb_JESDown));
    tree->SetBranchAddress("cat_JESUp", &(this->cat_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_JESDown", &(this->qg_LR_flavour_4q_0q_1q_2q_JESDown));
    tree->SetBranchAddress("nMatch_tb", &(this->nMatch_tb));
    tree->SetBranchAddress("passes_jet", &(this->passes_jet));
    tree->SetBranchAddress("D_JESUp", &(this->D_JESUp));
    tree->SetBranchAddress("is_dl", &(this->is_dl));
    tree->SetBranchAddress("nGenBTop", &(this->nGenBTop));
    tree->SetBranchAddress("C_JESUp", &(this->C_JESUp));
    tree->SetBranchAddress("mean_dr_btag_raw", &(this->mean_dr_btag_raw));
    tree->SetBranchAddress("mean_dr_btag_JESUp", &(this->mean_dr_btag_JESUp));
  } //loadTree
}; //class

#endif
