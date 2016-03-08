
#ifndef METREE_H
#define METREE_H
#include "TTree.h"
class TreeData {
public:
  int ncommon_mem;
  double common_mem_p_bkg[1]; //
  double common_mem_p[1]; //
  double common_mem_blr_4b[1]; //
  double common_mem_blr_2b[1]; //
  double common_mem_p_sig[1]; //
  int ncommon_mem_JESDown;
  double common_mem_JESDown_p_bkg[1]; //
  double common_mem_JESDown_p[1]; //
  double common_mem_JESDown_blr_4b[1]; //
  double common_mem_JESDown_blr_2b[1]; //
  double common_mem_JESDown_p_sig[1]; //
  int ncommon_mem_JESUp;
  double common_mem_JESUp_p_bkg[1]; //
  double common_mem_JESUp_p[1]; //
  double common_mem_JESUp_blr_4b[1]; //
  double common_mem_JESUp_blr_2b[1]; //
  double common_mem_JESUp_p_sig[1]; //
  int nfatjets;
  double fatjets_phi[4]; //
  double fatjets_pt[4]; //
  double fatjets_tau1[4]; //
  double fatjets_tau2[4]; //
  double fatjets_tau3[4]; //
  double fatjets_eta[4]; //
  double fatjets_mass[4]; //
  double fatjets_bbtag[4]; //
  int nfw_aj;
  double fw_aj_fw_h_alljets_nominal[8]; //
  int nfw_aj_JESDown;
  double fw_aj_JESDown_fw_h_alljets_JESDown[8]; //
  int nfw_aj_JESUp;
  double fw_aj_JESUp_fw_h_alljets_JESUp[8]; //
  int nfw_bj;
  double fw_bj_fw_h_btagjets_nominal[8]; //
  int nfw_bj_JESDown;
  double fw_bj_JESDown_fw_h_btagjets_JESDown[8]; //
  int nfw_bj_JESUp;
  double fw_bj_JESUp_fw_h_btagjets_JESUp[8]; //
  int nfw_uj;
  double fw_uj_fw_h_untagjets_nominal[8]; //
  int nfw_uj_JESDown;
  double fw_uj_JESDown_fw_h_untagjets_JESDown[8]; //
  int nfw_uj_JESUp;
  double fw_uj_JESUp_fw_h_untagjets_JESUp[8]; //
  int ngenHiggs;
  double genHiggs_phi[2]; //
  double genHiggs_eta[2]; //
  double genHiggs_mass[2]; //
  double genHiggs_id[2]; //
  double genHiggs_pt[2]; //
  int ngenTopHad;
  double genTopHad_phi[2]; //
  double genTopHad_eta[2]; //
  double genTopHad_mass[2]; //
  double genTopHad_pt[2]; //
  double genTopHad_decayMode[2]; //
  int ngenTopLep;
  double genTopLep_phi[2]; //
  double genTopLep_eta[2]; //
  double genTopLep_mass[2]; //
  double genTopLep_pt[2]; //
  double genTopLep_decayMode[2]; //
  int nhiggsCandidate;
  double higgsCandidate_mass_pruned[4]; //mass of the matched pruned jet
  double higgsCandidate_n_subjettiness[4]; //
  double higgsCandidate_phi[4]; //
  double higgsCandidate_pt[4]; //
  double higgsCandidate_tau3[4]; //
  double higgsCandidate_tau1[4]; //
  double higgsCandidate_dr_top[4]; //deltaR to the best HTT candidate
  double higgsCandidate_dr_genHiggs[4]; //deltaR to gen higgs
  double higgsCandidate_tau2[4]; //
  double higgsCandidate_mass_softdrop[4]; //mass of the matched softdrop jet
  double higgsCandidate_eta[4]; //
  double higgsCandidate_mass[4]; //
  double higgsCandidate_bbtag[4]; //
  double higgsCandidate_mass_softdropz2b1[4]; //mass of the matched softdropz2b1 jet
  int njets;
  double jets_mcPt[16]; //
  double jets_mcEta[16]; //
  int jets_matchBfromHadT[16]; //
  double jets_id[16]; //
  double jets_bTagWeightLFUp[16]; //b-tag CSV weight, variating LF Up
  double jets_pt[16]; //
  double jets_mcNumBHadrons[16]; //
  double jets_corr_JERDown[16]; //
  double jets_bTagWeightStats2Up[16]; //b-tag CSV weight, variating Stats2 Up
  double jets_qgl[16]; //
  double jets_bTagWeightcErr2Up[16]; //b-tag CSV weight, variating cErr2 Up
  double jets_mcPhi[16]; //
  double jets_bTagWeightStats1Up[16]; //b-tag CSV weight, variating Stats1 Up
  double jets_bTagWeightStats1Down[16]; //b-tag CSV weight, variating Stats1 Down
  double jets_bTagWeightcErr2Down[16]; //b-tag CSV weight, variating cErr2 Down
  int jets_matchFlag[16]; //0 - matched to light quark from W, 1 - matched to b form top, 2 - matched to b from higgs
  double jets_phi[16]; //
  double jets_bTagWeightStats2Down[16]; //b-tag CSV weight, variating Stats2 Down
  double jets_bTagWeightLFDown[16]; //b-tag CSV weight, variating LF Down
  int jets_hadronFlavour[16]; //
  double jets_corr_JESUp[16]; //
  double jets_bTagWeightJESDown[16]; //b-tag CSV weight, variating JES Down
  double jets_bTagWeightHFDown[16]; //b-tag CSV weight, variating HF Down
  double jets_corr_JERUp[16]; //
  double jets_corr[16]; //
  double jets_corr_JER[16]; //
  double jets_corr_JESDown[16]; //
  double jets_btagCSV[16]; //
  double jets_mcM[16]; //
  double jets_bTagWeightHFUp[16]; //b-tag CSV weight, variating HF Up
  double jets_bTagWeightcErr1Down[16]; //b-tag CSV weight, variating cErr1 Down
  int jets_mcMatchId[16]; //
  double jets_btagBDT[16]; //
  double jets_bTagWeightcErr1Up[16]; //b-tag CSV weight, variating cErr1 Up
  double jets_bTagWeight[16]; //b-tag CSV weight, nominal
  double jets_eta[16]; //
  double jets_mass[16]; //
  double jets_bTagWeightJESUp[16]; //b-tag CSV weight, variating JES Up
  double jets_mcNumCHadrons[16]; //
  int jets_mcFlavour[16]; //
  int nleps;
  double leps_phi[2]; //
  double leps_pt[2]; //
  double leps_pdgId[2]; //
  double leps_relIso04[2]; //
  double leps_eta[2]; //
  double leps_mass[2]; //
  double leps_relIso03[2]; //
  double leps_mvaId[2]; //
  int nloose_jets;
  double loose_jets_mcPt[6]; //
  double loose_jets_mcEta[6]; //
  int loose_jets_matchBfromHadT[6]; //
  double loose_jets_id[6]; //
  double loose_jets_bTagWeightLFUp[6]; //b-tag CSV weight, variating LF Up
  double loose_jets_pt[6]; //
  double loose_jets_mcNumBHadrons[6]; //
  double loose_jets_corr_JERDown[6]; //
  double loose_jets_bTagWeightStats2Up[6]; //b-tag CSV weight, variating Stats2 Up
  double loose_jets_qgl[6]; //
  double loose_jets_bTagWeightcErr2Up[6]; //b-tag CSV weight, variating cErr2 Up
  double loose_jets_mcPhi[6]; //
  double loose_jets_bTagWeightStats1Up[6]; //b-tag CSV weight, variating Stats1 Up
  double loose_jets_bTagWeightStats1Down[6]; //b-tag CSV weight, variating Stats1 Down
  double loose_jets_bTagWeightcErr2Down[6]; //b-tag CSV weight, variating cErr2 Down
  int loose_jets_matchFlag[6]; //0 - matched to light quark from W, 1 - matched to b form top, 2 - matched to b from higgs
  double loose_jets_phi[6]; //
  double loose_jets_bTagWeightStats2Down[6]; //b-tag CSV weight, variating Stats2 Down
  double loose_jets_bTagWeightLFDown[6]; //b-tag CSV weight, variating LF Down
  int loose_jets_hadronFlavour[6]; //
  double loose_jets_corr_JESUp[6]; //
  double loose_jets_bTagWeightJESDown[6]; //b-tag CSV weight, variating JES Down
  double loose_jets_bTagWeightHFDown[6]; //b-tag CSV weight, variating HF Down
  double loose_jets_corr_JERUp[6]; //
  double loose_jets_corr[6]; //
  double loose_jets_corr_JER[6]; //
  double loose_jets_corr_JESDown[6]; //
  double loose_jets_btagCSV[6]; //
  double loose_jets_mcM[6]; //
  double loose_jets_bTagWeightHFUp[6]; //b-tag CSV weight, variating HF Up
  double loose_jets_bTagWeightcErr1Down[6]; //b-tag CSV weight, variating cErr1 Down
  int loose_jets_mcMatchId[6]; //
  double loose_jets_btagBDT[6]; //
  double loose_jets_bTagWeightcErr1Up[6]; //b-tag CSV weight, variating cErr1 Up
  double loose_jets_bTagWeight[6]; //b-tag CSV weight, nominal
  double loose_jets_eta[6]; //
  double loose_jets_mass[6]; //
  double loose_jets_bTagWeightJESUp[6]; //b-tag CSV weight, variating JES Up
  double loose_jets_mcNumCHadrons[6]; //
  int loose_jets_mcFlavour[6]; //
  int nmem_ttbb;
  double mem_ttbb_p[12]; //
  double mem_ttbb_chi2[12]; //
  double mem_ttbb_p_err[12]; //
  double mem_ttbb_efficiency[12]; //
  int mem_ttbb_nperm[12]; //
  double mem_ttbb_time[12]; //
  int mem_ttbb_error_code[12]; //
  int nmem_ttbb_JESDown;
  double mem_ttbb_JESDown_p[12]; //
  double mem_ttbb_JESDown_chi2[12]; //
  double mem_ttbb_JESDown_p_err[12]; //
  double mem_ttbb_JESDown_efficiency[12]; //
  int mem_ttbb_JESDown_nperm[12]; //
  double mem_ttbb_JESDown_time[12]; //
  int mem_ttbb_JESDown_error_code[12]; //
  int nmem_ttbb_JESUp;
  double mem_ttbb_JESUp_p[12]; //
  double mem_ttbb_JESUp_chi2[12]; //
  double mem_ttbb_JESUp_p_err[12]; //
  double mem_ttbb_JESUp_efficiency[12]; //
  int mem_ttbb_JESUp_nperm[12]; //
  double mem_ttbb_JESUp_time[12]; //
  int mem_ttbb_JESUp_error_code[12]; //
  int nmem_tth;
  double mem_tth_p[12]; //
  double mem_tth_chi2[12]; //
  double mem_tth_p_err[12]; //
  double mem_tth_efficiency[12]; //
  int mem_tth_nperm[12]; //
  double mem_tth_time[12]; //
  int mem_tth_error_code[12]; //
  int nmem_tth_JESDown;
  double mem_tth_JESDown_p[12]; //
  double mem_tth_JESDown_chi2[12]; //
  double mem_tth_JESDown_p_err[12]; //
  double mem_tth_JESDown_efficiency[12]; //
  int mem_tth_JESDown_nperm[12]; //
  double mem_tth_JESDown_time[12]; //
  int mem_tth_JESDown_error_code[12]; //
  int nmem_tth_JESUp;
  double mem_tth_JESUp_p[12]; //
  double mem_tth_JESUp_chi2[12]; //
  double mem_tth_JESUp_p_err[12]; //
  double mem_tth_JESUp_efficiency[12]; //
  int mem_tth_JESUp_nperm[12]; //
  double mem_tth_JESUp_time[12]; //
  int mem_tth_JESUp_error_code[12]; //
  int nothertopCandidate;
  double othertopCandidate_tau1[4]; //
  double othertopCandidate_etacal[4]; //
  double othertopCandidate_sjW2btag[4]; //
  double othertopCandidate_n_subjettiness_groomed[4]; //
  double othertopCandidate_sjW2pt[4]; //
  double othertopCandidate_sjW1btag[4]; //
  double othertopCandidate_sjW1mass[4]; //
  double othertopCandidate_sjNonWmass[4]; //
  double othertopCandidate_sjNonWeta[4]; //
  double othertopCandidate_pt[4]; //
  double othertopCandidate_ptForRoptCalc[4]; //
  double othertopCandidate_tau2[4]; //
  double othertopCandidate_phi[4]; //
  double othertopCandidate_tau3[4]; //
  double othertopCandidate_sjNonWpt[4]; //
  double othertopCandidate_sjW2mass[4]; //
  double othertopCandidate_mass[4]; //
  double othertopCandidate_sjNonWbtag[4]; //
  double othertopCandidate_Ropt[4]; //
  double othertopCandidate_RoptCalc[4]; //
  double othertopCandidate_masscal[4]; //
  double othertopCandidate_ptcal[4]; //
  double othertopCandidate_sjW1phi[4]; //
  double othertopCandidate_sjW1pt[4]; //
  double othertopCandidate_sjNonWphi[4]; //
  double othertopCandidate_delRopt[4]; //
  double othertopCandidate_sjW1eta[4]; //
  double othertopCandidate_fRec[4]; //
  double othertopCandidate_phical[4]; //
  double othertopCandidate_sjW2phi[4]; //
  double othertopCandidate_eta[4]; //
  double othertopCandidate_n_subjettiness[4]; //
  double othertopCandidate_bbtag[4]; //
  double othertopCandidate_sjW2eta[4]; //
  double othertopCandidate_genTopHad_dr[4]; //DeltaR to the closest hadronic gen top
  int ntopCandidate;
  double topCandidate_tau1[1]; //
  double topCandidate_etacal[1]; //
  double topCandidate_sjW2btag[1]; //
  double topCandidate_n_subjettiness_groomed[1]; //
  double topCandidate_sjW2pt[1]; //
  double topCandidate_sjW1btag[1]; //
  double topCandidate_sjW1mass[1]; //
  double topCandidate_sjNonWmass[1]; //
  double topCandidate_sjNonWeta[1]; //
  double topCandidate_pt[1]; //
  double topCandidate_ptForRoptCalc[1]; //
  double topCandidate_tau2[1]; //
  double topCandidate_phi[1]; //
  double topCandidate_tau3[1]; //
  double topCandidate_sjNonWpt[1]; //
  double topCandidate_sjW2mass[1]; //
  double topCandidate_mass[1]; //
  double topCandidate_sjNonWbtag[1]; //
  double topCandidate_Ropt[1]; //
  double topCandidate_RoptCalc[1]; //
  double topCandidate_masscal[1]; //
  double topCandidate_ptcal[1]; //
  double topCandidate_sjW1phi[1]; //
  double topCandidate_sjW1pt[1]; //
  double topCandidate_sjNonWphi[1]; //
  double topCandidate_delRopt[1]; //
  double topCandidate_sjW1eta[1]; //
  double topCandidate_fRec[1]; //
  double topCandidate_phical[1]; //
  double topCandidate_sjW2phi[1]; //
  double topCandidate_eta[1]; //
  double topCandidate_n_subjettiness[1]; //
  double topCandidate_bbtag[1]; //
  double topCandidate_sjW2eta[1]; //
  double topCandidate_genTopHad_dr[1]; //DeltaR to the closest hadronic gen top
  int nll;
  double ll_phi[1]; //
  double ll_eta[1]; //
  double ll_mass[1]; //
  double ll_pt[1]; //
  int nmet;
  double met_phi[1]; //
  double met_sumEt[1]; //
  double met_pt[1]; //
  double met_px[1]; //
  double met_py[1]; //
  double met_genPhi[1]; //
  double met_genPt[1]; //
  int nmet_gen;
  double met_gen_phi[1]; //
  double met_gen_sumEt[1]; //
  double met_gen_pt[1]; //
  double met_gen_px[1]; //
  double met_gen_py[1]; //
  double met_gen_genPhi[1]; //
  double met_gen_genPt[1]; //
  int nmet_jetcorr;
  double met_jetcorr_phi[1]; //
  double met_jetcorr_sumEt[1]; //
  double met_jetcorr_pt[1]; //
  double met_jetcorr_px[1]; //
  double met_jetcorr_py[1]; //
  double met_jetcorr_genPhi[1]; //
  double met_jetcorr_genPt[1]; //
  int nmet_ttbar_gen;
  double met_ttbar_gen_phi[1]; //
  double met_ttbar_gen_sumEt[1]; //
  double met_ttbar_gen_pt[1]; //
  double met_ttbar_gen_px[1]; //
  double met_ttbar_gen_py[1]; //
  double met_ttbar_gen_genPhi[1]; //
  double met_ttbar_gen_genPt[1]; //
  int npv;
  double pv_z[1]; //
  double pv_isFake[1]; //
  double pv_rho[1]; //
  double pv_ndof[1]; //
  double C;
  double C_JESDown;
  double C_JESUp;
  double D;
  double D_JESDown;
  double D_JESUp;
  int HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v;
  int HLT_BIT_HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV0p45_v;
  int HLT_BIT_HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV0p45_v;
  int HLT_BIT_HLT_AK8PFHT650_TrimR0p1PT0p03Mass50_v;
  int HLT_BIT_HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v;
  int HLT_BIT_HLT_AK8PFJet360_TrimMass30_v;
  int HLT_BIT_HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_BTagCSV0p72_v;
  int HLT_BIT_HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_v;
  int HLT_BIT_HLT_DiCentralPFJet55_PFMET110_NoiseCleaned_v;
  int HLT_BIT_HLT_DiPFJetAve140_v;
  int HLT_BIT_HLT_DiPFJetAve200_v;
  int HLT_BIT_HLT_DiPFJetAve260_v;
  int HLT_BIT_HLT_DiPFJetAve320_v;
  int HLT_BIT_HLT_DiPFJetAve40_v;
  int HLT_BIT_HLT_DiPFJetAve60_v;
  int HLT_BIT_HLT_DiPFJetAve80_v;
  int HLT_BIT_HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf_v;
  int HLT_BIT_HLT_DoubleIsoMu17_eta2p1_v;
  int HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v;
  int HLT_BIT_HLT_DoubleJet90_Double30_TripleBTagCSV0p67_v;
  int HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v;
  int HLT_BIT_HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v;
  int HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v;
  int HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_v;
  int HLT_BIT_HLT_Ele22_eta2p1_WPLoose_Gsf_v;
  int HLT_BIT_HLT_Ele22_eta2p1_WPTight_Gsf_v;
  int HLT_BIT_HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v;
  int HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v;
  int HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v;
  int HLT_BIT_HLT_Ele23_WPLoose_Gsf_WHbbBoost_v;
  int HLT_BIT_HLT_Ele23_WPLoose_Gsf_v;
  int HLT_BIT_HLT_Ele27_WPLoose_Gsf_WHbbBoost_v;
  int HLT_BIT_HLT_Ele27_WPLoose_Gsf_v;
  int HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_CentralPFJet30_BTagCSV07_v;
  int HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v;
  int HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_v;
  int HLT_BIT_HLT_Ele27_eta2p1_WPTight_Gsf_v;
  int HLT_BIT_HLT_Ele30WP60_Ele8_Mass55_v;
  int HLT_BIT_HLT_Ele32_eta2p1_WPLoose_Gsf_CentralPFJet30_BTagCSV07_v;
  int HLT_BIT_HLT_Ele32_eta2p1_WPLoose_Gsf_v;
  int HLT_BIT_HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v;
  int HLT_BIT_HLT_IsoMu16_eta2p1_CaloMET30_v;
  int HLT_BIT_HLT_IsoMu18_v;
  int HLT_BIT_HLT_IsoMu20_eta2p1_CentralPFJet30_BTagCSV07_v;
  int HLT_BIT_HLT_IsoMu20_eta2p1_v;
  int HLT_BIT_HLT_IsoMu20_v;
  int HLT_BIT_HLT_IsoMu24_eta2p1_CentralPFJet30_BTagCSV07_v;
  int HLT_BIT_HLT_IsoMu24_eta2p1_v;
  int HLT_BIT_HLT_IsoMu27_v;
  int HLT_BIT_HLT_IsoTkMu18_v;
  int HLT_BIT_HLT_IsoTkMu20_v;
  int HLT_BIT_HLT_IsoTkMu27_v;
  int HLT_BIT_HLT_L1_TripleJet_VBF_v;
  int HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_v;
  int HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_v;
  int HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_v;
  int HLT_BIT_HLT_MonoCentralPFJet80_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v;
  int HLT_BIT_HLT_MonoCentralPFJet80_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v;
  int HLT_BIT_HLT_Mu16_eta2p1_CaloMET30_v;
  int HLT_BIT_HLT_Mu17_TkMu8_DZ_v;
  int HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v;
  int HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v;
  int HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v;
  int HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v;
  int HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v;
  int HLT_BIT_HLT_Mu20_v;
  int HLT_BIT_HLT_Mu24_eta2p1_v;
  int HLT_BIT_HLT_Mu24_v;
  int HLT_BIT_HLT_Mu27_v;
  int HLT_BIT_HLT_Mu40_eta2p1_PFJet200_PFJet50_v;
  int HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v;
  int HLT_BIT_HLT_OldIsoMu18_v;
  int HLT_BIT_HLT_OldIsoTkMu18_v;
  int HLT_BIT_HLT_PFHT350_PFMET100_NoiseCleaned_v;
  int HLT_BIT_HLT_PFHT350_v;
  int HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v;
  int HLT_BIT_HLT_PFHT400_SixJet30_v;
  int HLT_BIT_HLT_PFHT450_SixJet40_PFBTagCSV0p72_v;
  int HLT_BIT_HLT_PFHT450_SixJet40_v;
  int HLT_BIT_HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v;
  int HLT_BIT_HLT_PFHT650_WideJetMJJ950DEtaJJ1p5_v;
  int HLT_BIT_HLT_PFHT750_4JetPt50_v;
  int HLT_BIT_HLT_PFHT800_v;
  int HLT_BIT_HLT_PFJet140_v;
  int HLT_BIT_HLT_PFJet200_v;
  int HLT_BIT_HLT_PFJet260_v;
  int HLT_BIT_HLT_PFJet320_v;
  int HLT_BIT_HLT_PFJet400_v;
  int HLT_BIT_HLT_PFJet40_v;
  int HLT_BIT_HLT_PFJet450_v;
  int HLT_BIT_HLT_PFJet60_v;
  int HLT_BIT_HLT_PFJet80_v;
  int HLT_BIT_HLT_PFMET100_PFMHT100_IDTight_v;
  int HLT_BIT_HLT_PFMET110_PFMHT110_IDTight_v;
  int HLT_BIT_HLT_PFMET120_NoiseCleaned_Mu5_v;
  int HLT_BIT_HLT_PFMET120_PFMHT120_IDTight_v;
  int HLT_BIT_HLT_PFMET170_NoiseCleaned_v;
  int HLT_BIT_HLT_PFMET90_PFMHT90_IDTight_v;
  int HLT_BIT_HLT_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v;
  int HLT_BIT_HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v;
  int HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v;
  int HLT_BIT_HLT_QuadJet45_TripleBTagCSV0p67_v;
  int HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v;
  int HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq240_v;
  int HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v;
  int HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq500_v;
  int HLT_BIT_HLT_QuadPFJet_VBF_v;
  int HLT_BIT_HLT_TkMu20_v;
  int HLT_BIT_HLT_TkMu24_eta2p1_v;
  int HLT_BIT_HLT_TkMu27_v;
  int HLT_HH4bAll;
  int HLT_HH4bHighLumi;
  int HLT_HH4bLowLumi;
  int HLT_VBFHbbAll;
  int HLT_VBFHbbHighLumi;
  int HLT_VBFHbbLowLumi;
  int HLT_WenHbbAll;
  int HLT_WenHbbHighLumi;
  int HLT_WenHbbLowLumi;
  int HLT_WmnHbbAll;
  int HLT_WmnHbbHighLumi;
  int HLT_WmnHbbLowLumi;
  int HLT_WtaunHbbAll;
  int HLT_WtaunHbbHighLumi;
  int HLT_WtaunHbbLowLumi;
  int HLT_ZeeHbbAll;
  int HLT_ZeeHbbHighLumi;
  int HLT_ZeeHbbLowLumi;
  int HLT_ZmmHbbAll;
  int HLT_ZmmHbbHighLumi;
  int HLT_ZmmHbbLowLumi;
  int HLT_ZnnHbb;
  int HLT_ZnnHbbAll;
  int HLT_hadronic;
  int HLT_ttHhardonicAll;
  int HLT_ttHhardonicHighLumi;
  int HLT_ttHhardonicLowLumi;
  int HLT_ttHleptonic;
  double Wmass;
  double Wmass_JESDown;
  double Wmass_JESUp;
  double aplanarity;
  double aplanarity_JESDown;
  double aplanarity_JESUp;
  double bTagWeight;
  double bTagWeight_HFDown;
  double bTagWeight_HFUp;
  double bTagWeight_JESDown;
  double bTagWeight_JESUp;
  double bTagWeight_LFDown;
  double bTagWeight_LFUp;
  double bTagWeight_Stats1Down;
  double bTagWeight_Stats1Up;
  double bTagWeight_Stats2Down;
  double bTagWeight_Stats2Up;
  double bTagWeight_cErr1Down;
  double bTagWeight_cErr1Up;
  double bTagWeight_cErr2Down;
  double bTagWeight_cErr2Up;
  double btag_LR_4b_2b;
  double btag_LR_4b_2b_JESDown;
  double btag_LR_4b_2b_JESUp;
  double btag_lr_2b;
  double btag_lr_2b_JESDown;
  double btag_lr_2b_JESUp;
  double btag_lr_4b;
  double btag_lr_4b_JESDown;
  double btag_lr_4b_JESUp;
  int cat;
  int cat_JESDown;
  int cat_JESUp;
  int cat_btag;
  int cat_btag_JESDown;
  int cat_btag_JESUp;
  int cat_gen;
  int cat_gen_JESDown;
  int cat_gen_JESUp;
  double common_bdt;
  double common_bdt_JESDown;
  double common_bdt_JESUp;
  double common_bdt_withmem1;
  double common_bdt_withmem1_JESDown;
  double common_bdt_withmem1_JESUp;
  double common_bdt_withmem2;
  double common_bdt_withmem2_JESDown;
  double common_bdt_withmem2_JESUp;
  double eta_drpair_btag;
  double eta_drpair_btag_JESDown;
  double eta_drpair_btag_JESUp;
  long evt;
  int genHiggsDecayMode;
  double genWeight;
  double ht;
  double ht_JESDown;
  double ht_JESUp;
  int is_dl;
  int is_dl_JESDown;
  int is_dl_JESUp;
  int is_fh;
  int is_fh_JESDown;
  int is_fh_JESUp;
  int is_sl;
  int is_sl_JESDown;
  int is_sl_JESUp;
  double isotropy;
  double isotropy_JESDown;
  double isotropy_JESUp;
  double json;
  long lumi;
  double mass_drpair_btag;
  double mass_drpair_btag_JESDown;
  double mass_drpair_btag_JESUp;
  double mean_bdisc;
  double mean_bdisc_JESDown;
  double mean_bdisc_JESUp;
  double mean_bdisc_btag;
  double mean_bdisc_btag_JESDown;
  double mean_bdisc_btag_JESUp;
  double mean_dr_btag;
  double mean_dr_btag_JESDown;
  double mean_dr_btag_JESUp;
  double min_dr_btag;
  double min_dr_btag_JESDown;
  double min_dr_btag_JESUp;
  double momentum_eig0;
  double momentum_eig0_JESDown;
  double momentum_eig0_JESUp;
  double momentum_eig1;
  double momentum_eig1_JESDown;
  double momentum_eig1_JESUp;
  double momentum_eig2;
  double momentum_eig2_JESDown;
  double momentum_eig2_JESUp;
  int nBCSVL;
  int nBCSVL_JESDown;
  int nBCSVL_JESUp;
  int nBCSVM;
  int nBCSVM_JESDown;
  int nBCSVM_JESUp;
  int nBCSVT;
  int nBCSVT_JESDown;
  int nBCSVT_JESUp;
  int nGenBHiggs;
  int nGenBTop;
  int nGenQW;
  int nMatchSimB;
  int nMatchSimB_JESDown;
  int nMatchSimB_JESUp;
  int nMatchSimC;
  int nMatchSimC_JESDown;
  int nMatchSimC_JESUp;
  int nMatch_hb;
  int nMatch_hb_JESDown;
  int nMatch_hb_JESUp;
  int nMatch_hb_btag;
  int nMatch_hb_btag_JESDown;
  int nMatch_hb_btag_JESUp;
  int nMatch_tb;
  int nMatch_tb_JESDown;
  int nMatch_tb_JESUp;
  int nMatch_tb_btag;
  int nMatch_tb_btag_JESDown;
  int nMatch_tb_btag_JESUp;
  int nMatch_wq;
  int nMatch_wq_JESDown;
  int nMatch_wq_JESUp;
  int nMatch_wq_btag;
  int nMatch_wq_btag_JESDown;
  int nMatch_wq_btag_JESUp;
  double nPU0;
  double nPVs;
  double nTrueInt;
  double n_bjets;
  double n_boosted_bjets;
  double n_boosted_ljets;
  double n_excluded_bjets;
  double n_excluded_ljets;
  double n_ljets;
  int numJets;
  int numJets_JESDown;
  int numJets_JESUp;
  int passPV;
  int passes_btag;
  int passes_btag_JESDown;
  int passes_btag_JESUp;
  int passes_jet;
  int passes_jet_JESDown;
  int passes_jet_JESUp;
  int passes_mem;
  int passes_mem_JESDown;
  int passes_mem_JESUp;
  double pt_drpair_btag;
  double pt_drpair_btag_JESDown;
  double pt_drpair_btag_JESUp;
  double puWeight;
  double qg_LR_flavour_4q_0q;
  double qg_LR_flavour_4q_0q_1q;
  double qg_LR_flavour_4q_0q_1q_2q;
  double qg_LR_flavour_4q_0q_1q_2q_3q;
  double qg_LR_flavour_4q_0q_1q_2q_3q_JESDown;
  double qg_LR_flavour_4q_0q_1q_2q_3q_JESUp;
  double qg_LR_flavour_4q_0q_1q_2q_JESDown;
  double qg_LR_flavour_4q_0q_1q_2q_JESUp;
  double qg_LR_flavour_4q_0q_1q_JESDown;
  double qg_LR_flavour_4q_0q_1q_JESUp;
  double qg_LR_flavour_4q_0q_JESDown;
  double qg_LR_flavour_4q_0q_JESUp;
  double qg_LR_flavour_4q_1q;
  double qg_LR_flavour_4q_1q_2q;
  double qg_LR_flavour_4q_1q_2q_3q;
  double qg_LR_flavour_4q_1q_2q_3q_JESDown;
  double qg_LR_flavour_4q_1q_2q_3q_JESUp;
  double qg_LR_flavour_4q_1q_2q_JESDown;
  double qg_LR_flavour_4q_1q_2q_JESUp;
  double qg_LR_flavour_4q_1q_JESDown;
  double qg_LR_flavour_4q_1q_JESUp;
  double qg_LR_flavour_4q_2q;
  double qg_LR_flavour_4q_2q_3q;
  double qg_LR_flavour_4q_2q_3q_JESDown;
  double qg_LR_flavour_4q_2q_3q_JESUp;
  double qg_LR_flavour_4q_2q_JESDown;
  double qg_LR_flavour_4q_2q_JESUp;
  double qg_LR_flavour_4q_3q;
  double qg_LR_flavour_4q_3q_JESDown;
  double qg_LR_flavour_4q_3q_JESUp;
  double rho;
  long run;
  double sphericity;
  double sphericity_JESDown;
  double sphericity_JESUp;
  double std_bdisc;
  double std_bdisc_JESDown;
  double std_bdisc_JESUp;
  double std_bdisc_btag;
  double std_bdisc_btag_JESDown;
  double std_bdisc_btag_JESUp;
  double std_dr_btag;
  double std_dr_btag_JESDown;
  double std_dr_btag_JESUp;
  int triggerBitmask;
  int triggerDecision;
  int ttCls;
  double tth_mva;
  double tth_mva_JESDown;
  double tth_mva_JESUp;
  double weight_xs;
  double xsec;
  void loadTree(TTree* tree) {
    tree->SetBranchAddress("ncommon_mem", &(this->ncommon_mem));
    tree->SetBranchAddress("common_mem_p_bkg", this->common_mem_p_bkg);
    tree->SetBranchAddress("common_mem_p", this->common_mem_p);
    tree->SetBranchAddress("common_mem_blr_4b", this->common_mem_blr_4b);
    tree->SetBranchAddress("common_mem_blr_2b", this->common_mem_blr_2b);
    tree->SetBranchAddress("common_mem_p_sig", this->common_mem_p_sig);
    tree->SetBranchAddress("ncommon_mem_JESDown", &(this->ncommon_mem_JESDown));
    tree->SetBranchAddress("common_mem_JESDown_p_bkg", this->common_mem_JESDown_p_bkg);
    tree->SetBranchAddress("common_mem_JESDown_p", this->common_mem_JESDown_p);
    tree->SetBranchAddress("common_mem_JESDown_blr_4b", this->common_mem_JESDown_blr_4b);
    tree->SetBranchAddress("common_mem_JESDown_blr_2b", this->common_mem_JESDown_blr_2b);
    tree->SetBranchAddress("common_mem_JESDown_p_sig", this->common_mem_JESDown_p_sig);
    tree->SetBranchAddress("ncommon_mem_JESUp", &(this->ncommon_mem_JESUp));
    tree->SetBranchAddress("common_mem_JESUp_p_bkg", this->common_mem_JESUp_p_bkg);
    tree->SetBranchAddress("common_mem_JESUp_p", this->common_mem_JESUp_p);
    tree->SetBranchAddress("common_mem_JESUp_blr_4b", this->common_mem_JESUp_blr_4b);
    tree->SetBranchAddress("common_mem_JESUp_blr_2b", this->common_mem_JESUp_blr_2b);
    tree->SetBranchAddress("common_mem_JESUp_p_sig", this->common_mem_JESUp_p_sig);
    tree->SetBranchAddress("nfatjets", &(this->nfatjets));
    tree->SetBranchAddress("fatjets_phi", this->fatjets_phi);
    tree->SetBranchAddress("fatjets_pt", this->fatjets_pt);
    tree->SetBranchAddress("fatjets_tau1", this->fatjets_tau1);
    tree->SetBranchAddress("fatjets_tau2", this->fatjets_tau2);
    tree->SetBranchAddress("fatjets_tau3", this->fatjets_tau3);
    tree->SetBranchAddress("fatjets_eta", this->fatjets_eta);
    tree->SetBranchAddress("fatjets_mass", this->fatjets_mass);
    tree->SetBranchAddress("fatjets_bbtag", this->fatjets_bbtag);
    tree->SetBranchAddress("nfw_aj", &(this->nfw_aj));
    tree->SetBranchAddress("fw_aj_fw_h_alljets_nominal", this->fw_aj_fw_h_alljets_nominal);
    tree->SetBranchAddress("nfw_aj_JESDown", &(this->nfw_aj_JESDown));
    tree->SetBranchAddress("fw_aj_JESDown_fw_h_alljets_JESDown", this->fw_aj_JESDown_fw_h_alljets_JESDown);
    tree->SetBranchAddress("nfw_aj_JESUp", &(this->nfw_aj_JESUp));
    tree->SetBranchAddress("fw_aj_JESUp_fw_h_alljets_JESUp", this->fw_aj_JESUp_fw_h_alljets_JESUp);
    tree->SetBranchAddress("nfw_bj", &(this->nfw_bj));
    tree->SetBranchAddress("fw_bj_fw_h_btagjets_nominal", this->fw_bj_fw_h_btagjets_nominal);
    tree->SetBranchAddress("nfw_bj_JESDown", &(this->nfw_bj_JESDown));
    tree->SetBranchAddress("fw_bj_JESDown_fw_h_btagjets_JESDown", this->fw_bj_JESDown_fw_h_btagjets_JESDown);
    tree->SetBranchAddress("nfw_bj_JESUp", &(this->nfw_bj_JESUp));
    tree->SetBranchAddress("fw_bj_JESUp_fw_h_btagjets_JESUp", this->fw_bj_JESUp_fw_h_btagjets_JESUp);
    tree->SetBranchAddress("nfw_uj", &(this->nfw_uj));
    tree->SetBranchAddress("fw_uj_fw_h_untagjets_nominal", this->fw_uj_fw_h_untagjets_nominal);
    tree->SetBranchAddress("nfw_uj_JESDown", &(this->nfw_uj_JESDown));
    tree->SetBranchAddress("fw_uj_JESDown_fw_h_untagjets_JESDown", this->fw_uj_JESDown_fw_h_untagjets_JESDown);
    tree->SetBranchAddress("nfw_uj_JESUp", &(this->nfw_uj_JESUp));
    tree->SetBranchAddress("fw_uj_JESUp_fw_h_untagjets_JESUp", this->fw_uj_JESUp_fw_h_untagjets_JESUp);
    tree->SetBranchAddress("ngenHiggs", &(this->ngenHiggs));
    tree->SetBranchAddress("genHiggs_phi", this->genHiggs_phi);
    tree->SetBranchAddress("genHiggs_eta", this->genHiggs_eta);
    tree->SetBranchAddress("genHiggs_mass", this->genHiggs_mass);
    tree->SetBranchAddress("genHiggs_id", this->genHiggs_id);
    tree->SetBranchAddress("genHiggs_pt", this->genHiggs_pt);
    tree->SetBranchAddress("ngenTopHad", &(this->ngenTopHad));
    tree->SetBranchAddress("genTopHad_phi", this->genTopHad_phi);
    tree->SetBranchAddress("genTopHad_eta", this->genTopHad_eta);
    tree->SetBranchAddress("genTopHad_mass", this->genTopHad_mass);
    tree->SetBranchAddress("genTopHad_pt", this->genTopHad_pt);
    tree->SetBranchAddress("genTopHad_decayMode", this->genTopHad_decayMode);
    tree->SetBranchAddress("ngenTopLep", &(this->ngenTopLep));
    tree->SetBranchAddress("genTopLep_phi", this->genTopLep_phi);
    tree->SetBranchAddress("genTopLep_eta", this->genTopLep_eta);
    tree->SetBranchAddress("genTopLep_mass", this->genTopLep_mass);
    tree->SetBranchAddress("genTopLep_pt", this->genTopLep_pt);
    tree->SetBranchAddress("genTopLep_decayMode", this->genTopLep_decayMode);
    tree->SetBranchAddress("nhiggsCandidate", &(this->nhiggsCandidate));
    tree->SetBranchAddress("higgsCandidate_mass_pruned", this->higgsCandidate_mass_pruned);
    tree->SetBranchAddress("higgsCandidate_n_subjettiness", this->higgsCandidate_n_subjettiness);
    tree->SetBranchAddress("higgsCandidate_phi", this->higgsCandidate_phi);
    tree->SetBranchAddress("higgsCandidate_pt", this->higgsCandidate_pt);
    tree->SetBranchAddress("higgsCandidate_tau3", this->higgsCandidate_tau3);
    tree->SetBranchAddress("higgsCandidate_tau1", this->higgsCandidate_tau1);
    tree->SetBranchAddress("higgsCandidate_dr_top", this->higgsCandidate_dr_top);
    tree->SetBranchAddress("higgsCandidate_dr_genHiggs", this->higgsCandidate_dr_genHiggs);
    tree->SetBranchAddress("higgsCandidate_tau2", this->higgsCandidate_tau2);
    tree->SetBranchAddress("higgsCandidate_mass_softdrop", this->higgsCandidate_mass_softdrop);
    tree->SetBranchAddress("higgsCandidate_eta", this->higgsCandidate_eta);
    tree->SetBranchAddress("higgsCandidate_mass", this->higgsCandidate_mass);
    tree->SetBranchAddress("higgsCandidate_bbtag", this->higgsCandidate_bbtag);
    tree->SetBranchAddress("higgsCandidate_mass_softdropz2b1", this->higgsCandidate_mass_softdropz2b1);
    tree->SetBranchAddress("njets", &(this->njets));
    tree->SetBranchAddress("jets_mcPt", this->jets_mcPt);
    tree->SetBranchAddress("jets_mcEta", this->jets_mcEta);
    tree->SetBranchAddress("jets_matchBfromHadT", this->jets_matchBfromHadT);
    tree->SetBranchAddress("jets_id", this->jets_id);
    tree->SetBranchAddress("jets_bTagWeightLFUp", this->jets_bTagWeightLFUp);
    tree->SetBranchAddress("jets_pt", this->jets_pt);
    tree->SetBranchAddress("jets_mcNumBHadrons", this->jets_mcNumBHadrons);
    tree->SetBranchAddress("jets_corr_JERDown", this->jets_corr_JERDown);
    tree->SetBranchAddress("jets_bTagWeightStats2Up", this->jets_bTagWeightStats2Up);
    tree->SetBranchAddress("jets_qgl", this->jets_qgl);
    tree->SetBranchAddress("jets_bTagWeightcErr2Up", this->jets_bTagWeightcErr2Up);
    tree->SetBranchAddress("jets_mcPhi", this->jets_mcPhi);
    tree->SetBranchAddress("jets_bTagWeightStats1Up", this->jets_bTagWeightStats1Up);
    tree->SetBranchAddress("jets_bTagWeightStats1Down", this->jets_bTagWeightStats1Down);
    tree->SetBranchAddress("jets_bTagWeightcErr2Down", this->jets_bTagWeightcErr2Down);
    tree->SetBranchAddress("jets_matchFlag", this->jets_matchFlag);
    tree->SetBranchAddress("jets_phi", this->jets_phi);
    tree->SetBranchAddress("jets_bTagWeightStats2Down", this->jets_bTagWeightStats2Down);
    tree->SetBranchAddress("jets_bTagWeightLFDown", this->jets_bTagWeightLFDown);
    tree->SetBranchAddress("jets_hadronFlavour", this->jets_hadronFlavour);
    tree->SetBranchAddress("jets_corr_JESUp", this->jets_corr_JESUp);
    tree->SetBranchAddress("jets_bTagWeightJESDown", this->jets_bTagWeightJESDown);
    tree->SetBranchAddress("jets_bTagWeightHFDown", this->jets_bTagWeightHFDown);
    tree->SetBranchAddress("jets_corr_JERUp", this->jets_corr_JERUp);
    tree->SetBranchAddress("jets_corr", this->jets_corr);
    tree->SetBranchAddress("jets_corr_JER", this->jets_corr_JER);
    tree->SetBranchAddress("jets_corr_JESDown", this->jets_corr_JESDown);
    tree->SetBranchAddress("jets_btagCSV", this->jets_btagCSV);
    tree->SetBranchAddress("jets_mcM", this->jets_mcM);
    tree->SetBranchAddress("jets_bTagWeightHFUp", this->jets_bTagWeightHFUp);
    tree->SetBranchAddress("jets_bTagWeightcErr1Down", this->jets_bTagWeightcErr1Down);
    tree->SetBranchAddress("jets_mcMatchId", this->jets_mcMatchId);
    tree->SetBranchAddress("jets_btagBDT", this->jets_btagBDT);
    tree->SetBranchAddress("jets_bTagWeightcErr1Up", this->jets_bTagWeightcErr1Up);
    tree->SetBranchAddress("jets_bTagWeight", this->jets_bTagWeight);
    tree->SetBranchAddress("jets_eta", this->jets_eta);
    tree->SetBranchAddress("jets_mass", this->jets_mass);
    tree->SetBranchAddress("jets_bTagWeightJESUp", this->jets_bTagWeightJESUp);
    tree->SetBranchAddress("jets_mcNumCHadrons", this->jets_mcNumCHadrons);
    tree->SetBranchAddress("jets_mcFlavour", this->jets_mcFlavour);
    tree->SetBranchAddress("nleps", &(this->nleps));
    tree->SetBranchAddress("leps_phi", this->leps_phi);
    tree->SetBranchAddress("leps_pt", this->leps_pt);
    tree->SetBranchAddress("leps_pdgId", this->leps_pdgId);
    tree->SetBranchAddress("leps_relIso04", this->leps_relIso04);
    tree->SetBranchAddress("leps_eta", this->leps_eta);
    tree->SetBranchAddress("leps_mass", this->leps_mass);
    tree->SetBranchAddress("leps_relIso03", this->leps_relIso03);
    tree->SetBranchAddress("leps_mvaId", this->leps_mvaId);
    tree->SetBranchAddress("nloose_jets", &(this->nloose_jets));
    tree->SetBranchAddress("loose_jets_mcPt", this->loose_jets_mcPt);
    tree->SetBranchAddress("loose_jets_mcEta", this->loose_jets_mcEta);
    tree->SetBranchAddress("loose_jets_matchBfromHadT", this->loose_jets_matchBfromHadT);
    tree->SetBranchAddress("loose_jets_id", this->loose_jets_id);
    tree->SetBranchAddress("loose_jets_bTagWeightLFUp", this->loose_jets_bTagWeightLFUp);
    tree->SetBranchAddress("loose_jets_pt", this->loose_jets_pt);
    tree->SetBranchAddress("loose_jets_mcNumBHadrons", this->loose_jets_mcNumBHadrons);
    tree->SetBranchAddress("loose_jets_corr_JERDown", this->loose_jets_corr_JERDown);
    tree->SetBranchAddress("loose_jets_bTagWeightStats2Up", this->loose_jets_bTagWeightStats2Up);
    tree->SetBranchAddress("loose_jets_qgl", this->loose_jets_qgl);
    tree->SetBranchAddress("loose_jets_bTagWeightcErr2Up", this->loose_jets_bTagWeightcErr2Up);
    tree->SetBranchAddress("loose_jets_mcPhi", this->loose_jets_mcPhi);
    tree->SetBranchAddress("loose_jets_bTagWeightStats1Up", this->loose_jets_bTagWeightStats1Up);
    tree->SetBranchAddress("loose_jets_bTagWeightStats1Down", this->loose_jets_bTagWeightStats1Down);
    tree->SetBranchAddress("loose_jets_bTagWeightcErr2Down", this->loose_jets_bTagWeightcErr2Down);
    tree->SetBranchAddress("loose_jets_matchFlag", this->loose_jets_matchFlag);
    tree->SetBranchAddress("loose_jets_phi", this->loose_jets_phi);
    tree->SetBranchAddress("loose_jets_bTagWeightStats2Down", this->loose_jets_bTagWeightStats2Down);
    tree->SetBranchAddress("loose_jets_bTagWeightLFDown", this->loose_jets_bTagWeightLFDown);
    tree->SetBranchAddress("loose_jets_hadronFlavour", this->loose_jets_hadronFlavour);
    tree->SetBranchAddress("loose_jets_corr_JESUp", this->loose_jets_corr_JESUp);
    tree->SetBranchAddress("loose_jets_bTagWeightJESDown", this->loose_jets_bTagWeightJESDown);
    tree->SetBranchAddress("loose_jets_bTagWeightHFDown", this->loose_jets_bTagWeightHFDown);
    tree->SetBranchAddress("loose_jets_corr_JERUp", this->loose_jets_corr_JERUp);
    tree->SetBranchAddress("loose_jets_corr", this->loose_jets_corr);
    tree->SetBranchAddress("loose_jets_corr_JER", this->loose_jets_corr_JER);
    tree->SetBranchAddress("loose_jets_corr_JESDown", this->loose_jets_corr_JESDown);
    tree->SetBranchAddress("loose_jets_btagCSV", this->loose_jets_btagCSV);
    tree->SetBranchAddress("loose_jets_mcM", this->loose_jets_mcM);
    tree->SetBranchAddress("loose_jets_bTagWeightHFUp", this->loose_jets_bTagWeightHFUp);
    tree->SetBranchAddress("loose_jets_bTagWeightcErr1Down", this->loose_jets_bTagWeightcErr1Down);
    tree->SetBranchAddress("loose_jets_mcMatchId", this->loose_jets_mcMatchId);
    tree->SetBranchAddress("loose_jets_btagBDT", this->loose_jets_btagBDT);
    tree->SetBranchAddress("loose_jets_bTagWeightcErr1Up", this->loose_jets_bTagWeightcErr1Up);
    tree->SetBranchAddress("loose_jets_bTagWeight", this->loose_jets_bTagWeight);
    tree->SetBranchAddress("loose_jets_eta", this->loose_jets_eta);
    tree->SetBranchAddress("loose_jets_mass", this->loose_jets_mass);
    tree->SetBranchAddress("loose_jets_bTagWeightJESUp", this->loose_jets_bTagWeightJESUp);
    tree->SetBranchAddress("loose_jets_mcNumCHadrons", this->loose_jets_mcNumCHadrons);
    tree->SetBranchAddress("loose_jets_mcFlavour", this->loose_jets_mcFlavour);
    tree->SetBranchAddress("nmem_ttbb", &(this->nmem_ttbb));
    tree->SetBranchAddress("mem_ttbb_p", this->mem_ttbb_p);
    tree->SetBranchAddress("mem_ttbb_chi2", this->mem_ttbb_chi2);
    tree->SetBranchAddress("mem_ttbb_p_err", this->mem_ttbb_p_err);
    tree->SetBranchAddress("mem_ttbb_efficiency", this->mem_ttbb_efficiency);
    tree->SetBranchAddress("mem_ttbb_nperm", this->mem_ttbb_nperm);
    tree->SetBranchAddress("mem_ttbb_time", this->mem_ttbb_time);
    tree->SetBranchAddress("mem_ttbb_error_code", this->mem_ttbb_error_code);
    tree->SetBranchAddress("nmem_ttbb_JESDown", &(this->nmem_ttbb_JESDown));
    tree->SetBranchAddress("mem_ttbb_JESDown_p", this->mem_ttbb_JESDown_p);
    tree->SetBranchAddress("mem_ttbb_JESDown_chi2", this->mem_ttbb_JESDown_chi2);
    tree->SetBranchAddress("mem_ttbb_JESDown_p_err", this->mem_ttbb_JESDown_p_err);
    tree->SetBranchAddress("mem_ttbb_JESDown_efficiency", this->mem_ttbb_JESDown_efficiency);
    tree->SetBranchAddress("mem_ttbb_JESDown_nperm", this->mem_ttbb_JESDown_nperm);
    tree->SetBranchAddress("mem_ttbb_JESDown_time", this->mem_ttbb_JESDown_time);
    tree->SetBranchAddress("mem_ttbb_JESDown_error_code", this->mem_ttbb_JESDown_error_code);
    tree->SetBranchAddress("nmem_ttbb_JESUp", &(this->nmem_ttbb_JESUp));
    tree->SetBranchAddress("mem_ttbb_JESUp_p", this->mem_ttbb_JESUp_p);
    tree->SetBranchAddress("mem_ttbb_JESUp_chi2", this->mem_ttbb_JESUp_chi2);
    tree->SetBranchAddress("mem_ttbb_JESUp_p_err", this->mem_ttbb_JESUp_p_err);
    tree->SetBranchAddress("mem_ttbb_JESUp_efficiency", this->mem_ttbb_JESUp_efficiency);
    tree->SetBranchAddress("mem_ttbb_JESUp_nperm", this->mem_ttbb_JESUp_nperm);
    tree->SetBranchAddress("mem_ttbb_JESUp_time", this->mem_ttbb_JESUp_time);
    tree->SetBranchAddress("mem_ttbb_JESUp_error_code", this->mem_ttbb_JESUp_error_code);
    tree->SetBranchAddress("nmem_tth", &(this->nmem_tth));
    tree->SetBranchAddress("mem_tth_p", this->mem_tth_p);
    tree->SetBranchAddress("mem_tth_chi2", this->mem_tth_chi2);
    tree->SetBranchAddress("mem_tth_p_err", this->mem_tth_p_err);
    tree->SetBranchAddress("mem_tth_efficiency", this->mem_tth_efficiency);
    tree->SetBranchAddress("mem_tth_nperm", this->mem_tth_nperm);
    tree->SetBranchAddress("mem_tth_time", this->mem_tth_time);
    tree->SetBranchAddress("mem_tth_error_code", this->mem_tth_error_code);
    tree->SetBranchAddress("nmem_tth_JESDown", &(this->nmem_tth_JESDown));
    tree->SetBranchAddress("mem_tth_JESDown_p", this->mem_tth_JESDown_p);
    tree->SetBranchAddress("mem_tth_JESDown_chi2", this->mem_tth_JESDown_chi2);
    tree->SetBranchAddress("mem_tth_JESDown_p_err", this->mem_tth_JESDown_p_err);
    tree->SetBranchAddress("mem_tth_JESDown_efficiency", this->mem_tth_JESDown_efficiency);
    tree->SetBranchAddress("mem_tth_JESDown_nperm", this->mem_tth_JESDown_nperm);
    tree->SetBranchAddress("mem_tth_JESDown_time", this->mem_tth_JESDown_time);
    tree->SetBranchAddress("mem_tth_JESDown_error_code", this->mem_tth_JESDown_error_code);
    tree->SetBranchAddress("nmem_tth_JESUp", &(this->nmem_tth_JESUp));
    tree->SetBranchAddress("mem_tth_JESUp_p", this->mem_tth_JESUp_p);
    tree->SetBranchAddress("mem_tth_JESUp_chi2", this->mem_tth_JESUp_chi2);
    tree->SetBranchAddress("mem_tth_JESUp_p_err", this->mem_tth_JESUp_p_err);
    tree->SetBranchAddress("mem_tth_JESUp_efficiency", this->mem_tth_JESUp_efficiency);
    tree->SetBranchAddress("mem_tth_JESUp_nperm", this->mem_tth_JESUp_nperm);
    tree->SetBranchAddress("mem_tth_JESUp_time", this->mem_tth_JESUp_time);
    tree->SetBranchAddress("mem_tth_JESUp_error_code", this->mem_tth_JESUp_error_code);
    tree->SetBranchAddress("nothertopCandidate", &(this->nothertopCandidate));
    tree->SetBranchAddress("othertopCandidate_tau1", this->othertopCandidate_tau1);
    tree->SetBranchAddress("othertopCandidate_etacal", this->othertopCandidate_etacal);
    tree->SetBranchAddress("othertopCandidate_sjW2btag", this->othertopCandidate_sjW2btag);
    tree->SetBranchAddress("othertopCandidate_n_subjettiness_groomed", this->othertopCandidate_n_subjettiness_groomed);
    tree->SetBranchAddress("othertopCandidate_sjW2pt", this->othertopCandidate_sjW2pt);
    tree->SetBranchAddress("othertopCandidate_sjW1btag", this->othertopCandidate_sjW1btag);
    tree->SetBranchAddress("othertopCandidate_sjW1mass", this->othertopCandidate_sjW1mass);
    tree->SetBranchAddress("othertopCandidate_sjNonWmass", this->othertopCandidate_sjNonWmass);
    tree->SetBranchAddress("othertopCandidate_sjNonWeta", this->othertopCandidate_sjNonWeta);
    tree->SetBranchAddress("othertopCandidate_pt", this->othertopCandidate_pt);
    tree->SetBranchAddress("othertopCandidate_ptForRoptCalc", this->othertopCandidate_ptForRoptCalc);
    tree->SetBranchAddress("othertopCandidate_tau2", this->othertopCandidate_tau2);
    tree->SetBranchAddress("othertopCandidate_phi", this->othertopCandidate_phi);
    tree->SetBranchAddress("othertopCandidate_tau3", this->othertopCandidate_tau3);
    tree->SetBranchAddress("othertopCandidate_sjNonWpt", this->othertopCandidate_sjNonWpt);
    tree->SetBranchAddress("othertopCandidate_sjW2mass", this->othertopCandidate_sjW2mass);
    tree->SetBranchAddress("othertopCandidate_mass", this->othertopCandidate_mass);
    tree->SetBranchAddress("othertopCandidate_sjNonWbtag", this->othertopCandidate_sjNonWbtag);
    tree->SetBranchAddress("othertopCandidate_Ropt", this->othertopCandidate_Ropt);
    tree->SetBranchAddress("othertopCandidate_RoptCalc", this->othertopCandidate_RoptCalc);
    tree->SetBranchAddress("othertopCandidate_masscal", this->othertopCandidate_masscal);
    tree->SetBranchAddress("othertopCandidate_ptcal", this->othertopCandidate_ptcal);
    tree->SetBranchAddress("othertopCandidate_sjW1phi", this->othertopCandidate_sjW1phi);
    tree->SetBranchAddress("othertopCandidate_sjW1pt", this->othertopCandidate_sjW1pt);
    tree->SetBranchAddress("othertopCandidate_sjNonWphi", this->othertopCandidate_sjNonWphi);
    tree->SetBranchAddress("othertopCandidate_delRopt", this->othertopCandidate_delRopt);
    tree->SetBranchAddress("othertopCandidate_sjW1eta", this->othertopCandidate_sjW1eta);
    tree->SetBranchAddress("othertopCandidate_fRec", this->othertopCandidate_fRec);
    tree->SetBranchAddress("othertopCandidate_phical", this->othertopCandidate_phical);
    tree->SetBranchAddress("othertopCandidate_sjW2phi", this->othertopCandidate_sjW2phi);
    tree->SetBranchAddress("othertopCandidate_eta", this->othertopCandidate_eta);
    tree->SetBranchAddress("othertopCandidate_n_subjettiness", this->othertopCandidate_n_subjettiness);
    tree->SetBranchAddress("othertopCandidate_bbtag", this->othertopCandidate_bbtag);
    tree->SetBranchAddress("othertopCandidate_sjW2eta", this->othertopCandidate_sjW2eta);
    tree->SetBranchAddress("othertopCandidate_genTopHad_dr", this->othertopCandidate_genTopHad_dr);
    tree->SetBranchAddress("ntopCandidate", &(this->ntopCandidate));
    tree->SetBranchAddress("topCandidate_tau1", this->topCandidate_tau1);
    tree->SetBranchAddress("topCandidate_etacal", this->topCandidate_etacal);
    tree->SetBranchAddress("topCandidate_sjW2btag", this->topCandidate_sjW2btag);
    tree->SetBranchAddress("topCandidate_n_subjettiness_groomed", this->topCandidate_n_subjettiness_groomed);
    tree->SetBranchAddress("topCandidate_sjW2pt", this->topCandidate_sjW2pt);
    tree->SetBranchAddress("topCandidate_sjW1btag", this->topCandidate_sjW1btag);
    tree->SetBranchAddress("topCandidate_sjW1mass", this->topCandidate_sjW1mass);
    tree->SetBranchAddress("topCandidate_sjNonWmass", this->topCandidate_sjNonWmass);
    tree->SetBranchAddress("topCandidate_sjNonWeta", this->topCandidate_sjNonWeta);
    tree->SetBranchAddress("topCandidate_pt", this->topCandidate_pt);
    tree->SetBranchAddress("topCandidate_ptForRoptCalc", this->topCandidate_ptForRoptCalc);
    tree->SetBranchAddress("topCandidate_tau2", this->topCandidate_tau2);
    tree->SetBranchAddress("topCandidate_phi", this->topCandidate_phi);
    tree->SetBranchAddress("topCandidate_tau3", this->topCandidate_tau3);
    tree->SetBranchAddress("topCandidate_sjNonWpt", this->topCandidate_sjNonWpt);
    tree->SetBranchAddress("topCandidate_sjW2mass", this->topCandidate_sjW2mass);
    tree->SetBranchAddress("topCandidate_mass", this->topCandidate_mass);
    tree->SetBranchAddress("topCandidate_sjNonWbtag", this->topCandidate_sjNonWbtag);
    tree->SetBranchAddress("topCandidate_Ropt", this->topCandidate_Ropt);
    tree->SetBranchAddress("topCandidate_RoptCalc", this->topCandidate_RoptCalc);
    tree->SetBranchAddress("topCandidate_masscal", this->topCandidate_masscal);
    tree->SetBranchAddress("topCandidate_ptcal", this->topCandidate_ptcal);
    tree->SetBranchAddress("topCandidate_sjW1phi", this->topCandidate_sjW1phi);
    tree->SetBranchAddress("topCandidate_sjW1pt", this->topCandidate_sjW1pt);
    tree->SetBranchAddress("topCandidate_sjNonWphi", this->topCandidate_sjNonWphi);
    tree->SetBranchAddress("topCandidate_delRopt", this->topCandidate_delRopt);
    tree->SetBranchAddress("topCandidate_sjW1eta", this->topCandidate_sjW1eta);
    tree->SetBranchAddress("topCandidate_fRec", this->topCandidate_fRec);
    tree->SetBranchAddress("topCandidate_phical", this->topCandidate_phical);
    tree->SetBranchAddress("topCandidate_sjW2phi", this->topCandidate_sjW2phi);
    tree->SetBranchAddress("topCandidate_eta", this->topCandidate_eta);
    tree->SetBranchAddress("topCandidate_n_subjettiness", this->topCandidate_n_subjettiness);
    tree->SetBranchAddress("topCandidate_bbtag", this->topCandidate_bbtag);
    tree->SetBranchAddress("topCandidate_sjW2eta", this->topCandidate_sjW2eta);
    tree->SetBranchAddress("topCandidate_genTopHad_dr", this->topCandidate_genTopHad_dr);
    tree->SetBranchAddress("nll", &(this->nll));
    tree->SetBranchAddress("ll_phi", this->ll_phi);
    tree->SetBranchAddress("ll_eta", this->ll_eta);
    tree->SetBranchAddress("ll_mass", this->ll_mass);
    tree->SetBranchAddress("ll_pt", this->ll_pt);
    tree->SetBranchAddress("nmet", &(this->nmet));
    tree->SetBranchAddress("met_phi", this->met_phi);
    tree->SetBranchAddress("met_sumEt", this->met_sumEt);
    tree->SetBranchAddress("met_pt", this->met_pt);
    tree->SetBranchAddress("met_px", this->met_px);
    tree->SetBranchAddress("met_py", this->met_py);
    tree->SetBranchAddress("met_genPhi", this->met_genPhi);
    tree->SetBranchAddress("met_genPt", this->met_genPt);
    tree->SetBranchAddress("nmet_gen", &(this->nmet_gen));
    tree->SetBranchAddress("met_gen_phi", this->met_gen_phi);
    tree->SetBranchAddress("met_gen_sumEt", this->met_gen_sumEt);
    tree->SetBranchAddress("met_gen_pt", this->met_gen_pt);
    tree->SetBranchAddress("met_gen_px", this->met_gen_px);
    tree->SetBranchAddress("met_gen_py", this->met_gen_py);
    tree->SetBranchAddress("met_gen_genPhi", this->met_gen_genPhi);
    tree->SetBranchAddress("met_gen_genPt", this->met_gen_genPt);
    tree->SetBranchAddress("nmet_jetcorr", &(this->nmet_jetcorr));
    tree->SetBranchAddress("met_jetcorr_phi", this->met_jetcorr_phi);
    tree->SetBranchAddress("met_jetcorr_sumEt", this->met_jetcorr_sumEt);
    tree->SetBranchAddress("met_jetcorr_pt", this->met_jetcorr_pt);
    tree->SetBranchAddress("met_jetcorr_px", this->met_jetcorr_px);
    tree->SetBranchAddress("met_jetcorr_py", this->met_jetcorr_py);
    tree->SetBranchAddress("met_jetcorr_genPhi", this->met_jetcorr_genPhi);
    tree->SetBranchAddress("met_jetcorr_genPt", this->met_jetcorr_genPt);
    tree->SetBranchAddress("nmet_ttbar_gen", &(this->nmet_ttbar_gen));
    tree->SetBranchAddress("met_ttbar_gen_phi", this->met_ttbar_gen_phi);
    tree->SetBranchAddress("met_ttbar_gen_sumEt", this->met_ttbar_gen_sumEt);
    tree->SetBranchAddress("met_ttbar_gen_pt", this->met_ttbar_gen_pt);
    tree->SetBranchAddress("met_ttbar_gen_px", this->met_ttbar_gen_px);
    tree->SetBranchAddress("met_ttbar_gen_py", this->met_ttbar_gen_py);
    tree->SetBranchAddress("met_ttbar_gen_genPhi", this->met_ttbar_gen_genPhi);
    tree->SetBranchAddress("met_ttbar_gen_genPt", this->met_ttbar_gen_genPt);
    tree->SetBranchAddress("npv", &(this->npv));
    tree->SetBranchAddress("pv_z", this->pv_z);
    tree->SetBranchAddress("pv_isFake", this->pv_isFake);
    tree->SetBranchAddress("pv_rho", this->pv_rho);
    tree->SetBranchAddress("pv_ndof", this->pv_ndof);
    tree->SetBranchAddress("C", &(this->C));
    tree->SetBranchAddress("C_JESDown", &(this->C_JESDown));
    tree->SetBranchAddress("C_JESUp", &(this->C_JESUp));
    tree->SetBranchAddress("D", &(this->D));
    tree->SetBranchAddress("D_JESDown", &(this->D_JESDown));
    tree->SetBranchAddress("D_JESUp", &(this->D_JESUp));
    tree->SetBranchAddress("HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v", &(this->HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v));
    tree->SetBranchAddress("HLT_BIT_HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV0p45_v", &(this->HLT_BIT_HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV0p45_v));
    tree->SetBranchAddress("HLT_BIT_HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV0p45_v", &(this->HLT_BIT_HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV0p45_v));
    tree->SetBranchAddress("HLT_BIT_HLT_AK8PFHT650_TrimR0p1PT0p03Mass50_v", &(this->HLT_BIT_HLT_AK8PFHT650_TrimR0p1PT0p03Mass50_v));
    tree->SetBranchAddress("HLT_BIT_HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v", &(this->HLT_BIT_HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v));
    tree->SetBranchAddress("HLT_BIT_HLT_AK8PFJet360_TrimMass30_v", &(this->HLT_BIT_HLT_AK8PFJet360_TrimMass30_v));
    tree->SetBranchAddress("HLT_BIT_HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_BTagCSV0p72_v", &(this->HLT_BIT_HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_BTagCSV0p72_v));
    tree->SetBranchAddress("HLT_BIT_HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_v", &(this->HLT_BIT_HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DiCentralPFJet55_PFMET110_NoiseCleaned_v", &(this->HLT_BIT_HLT_DiCentralPFJet55_PFMET110_NoiseCleaned_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DiPFJetAve140_v", &(this->HLT_BIT_HLT_DiPFJetAve140_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DiPFJetAve200_v", &(this->HLT_BIT_HLT_DiPFJetAve200_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DiPFJetAve260_v", &(this->HLT_BIT_HLT_DiPFJetAve260_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DiPFJetAve320_v", &(this->HLT_BIT_HLT_DiPFJetAve320_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DiPFJetAve40_v", &(this->HLT_BIT_HLT_DiPFJetAve40_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DiPFJetAve60_v", &(this->HLT_BIT_HLT_DiPFJetAve60_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DiPFJetAve80_v", &(this->HLT_BIT_HLT_DiPFJetAve80_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf_v", &(this->HLT_BIT_HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DoubleIsoMu17_eta2p1_v", &(this->HLT_BIT_HLT_DoubleIsoMu17_eta2p1_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v", &(this->HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v));
    tree->SetBranchAddress("HLT_BIT_HLT_DoubleJet90_Double30_TripleBTagCSV0p67_v", &(this->HLT_BIT_HLT_DoubleJet90_Double30_TripleBTagCSV0p67_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v", &(this->HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v", &(this->HLT_BIT_HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v", &(this->HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_v", &(this->HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele22_eta2p1_WPLoose_Gsf_v", &(this->HLT_BIT_HLT_Ele22_eta2p1_WPLoose_Gsf_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele22_eta2p1_WPTight_Gsf_v", &(this->HLT_BIT_HLT_Ele22_eta2p1_WPTight_Gsf_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v", &(this->HLT_BIT_HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v", &(this->HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v", &(this->HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele23_WPLoose_Gsf_WHbbBoost_v", &(this->HLT_BIT_HLT_Ele23_WPLoose_Gsf_WHbbBoost_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele23_WPLoose_Gsf_v", &(this->HLT_BIT_HLT_Ele23_WPLoose_Gsf_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele27_WPLoose_Gsf_WHbbBoost_v", &(this->HLT_BIT_HLT_Ele27_WPLoose_Gsf_WHbbBoost_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele27_WPLoose_Gsf_v", &(this->HLT_BIT_HLT_Ele27_WPLoose_Gsf_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_CentralPFJet30_BTagCSV07_v", &(this->HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_CentralPFJet30_BTagCSV07_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v", &(this->HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_v", &(this->HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele27_eta2p1_WPTight_Gsf_v", &(this->HLT_BIT_HLT_Ele27_eta2p1_WPTight_Gsf_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele30WP60_Ele8_Mass55_v", &(this->HLT_BIT_HLT_Ele30WP60_Ele8_Mass55_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele32_eta2p1_WPLoose_Gsf_CentralPFJet30_BTagCSV07_v", &(this->HLT_BIT_HLT_Ele32_eta2p1_WPLoose_Gsf_CentralPFJet30_BTagCSV07_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele32_eta2p1_WPLoose_Gsf_v", &(this->HLT_BIT_HLT_Ele32_eta2p1_WPLoose_Gsf_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v", &(this->HLT_BIT_HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoMu16_eta2p1_CaloMET30_v", &(this->HLT_BIT_HLT_IsoMu16_eta2p1_CaloMET30_v));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoMu18_v", &(this->HLT_BIT_HLT_IsoMu18_v));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoMu20_eta2p1_CentralPFJet30_BTagCSV07_v", &(this->HLT_BIT_HLT_IsoMu20_eta2p1_CentralPFJet30_BTagCSV07_v));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoMu20_eta2p1_v", &(this->HLT_BIT_HLT_IsoMu20_eta2p1_v));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoMu20_v", &(this->HLT_BIT_HLT_IsoMu20_v));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoMu24_eta2p1_CentralPFJet30_BTagCSV07_v", &(this->HLT_BIT_HLT_IsoMu24_eta2p1_CentralPFJet30_BTagCSV07_v));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoMu24_eta2p1_v", &(this->HLT_BIT_HLT_IsoMu24_eta2p1_v));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoMu27_v", &(this->HLT_BIT_HLT_IsoMu27_v));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoTkMu18_v", &(this->HLT_BIT_HLT_IsoTkMu18_v));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoTkMu20_v", &(this->HLT_BIT_HLT_IsoTkMu20_v));
    tree->SetBranchAddress("HLT_BIT_HLT_IsoTkMu27_v", &(this->HLT_BIT_HLT_IsoTkMu27_v));
    tree->SetBranchAddress("HLT_BIT_HLT_L1_TripleJet_VBF_v", &(this->HLT_BIT_HLT_L1_TripleJet_VBF_v));
    tree->SetBranchAddress("HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_v", &(this->HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_v));
    tree->SetBranchAddress("HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_v", &(this->HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_v));
    tree->SetBranchAddress("HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_v", &(this->HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_v));
    tree->SetBranchAddress("HLT_BIT_HLT_MonoCentralPFJet80_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v", &(this->HLT_BIT_HLT_MonoCentralPFJet80_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v));
    tree->SetBranchAddress("HLT_BIT_HLT_MonoCentralPFJet80_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v", &(this->HLT_BIT_HLT_MonoCentralPFJet80_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu16_eta2p1_CaloMET30_v", &(this->HLT_BIT_HLT_Mu16_eta2p1_CaloMET30_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu17_TkMu8_DZ_v", &(this->HLT_BIT_HLT_Mu17_TkMu8_DZ_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v", &(this->HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v", &(this->HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v", &(this->HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v", &(this->HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v", &(this->HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu20_v", &(this->HLT_BIT_HLT_Mu20_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu24_eta2p1_v", &(this->HLT_BIT_HLT_Mu24_eta2p1_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu24_v", &(this->HLT_BIT_HLT_Mu24_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu27_v", &(this->HLT_BIT_HLT_Mu27_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu40_eta2p1_PFJet200_PFJet50_v", &(this->HLT_BIT_HLT_Mu40_eta2p1_PFJet200_PFJet50_v));
    tree->SetBranchAddress("HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v", &(this->HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v));
    tree->SetBranchAddress("HLT_BIT_HLT_OldIsoMu18_v", &(this->HLT_BIT_HLT_OldIsoMu18_v));
    tree->SetBranchAddress("HLT_BIT_HLT_OldIsoTkMu18_v", &(this->HLT_BIT_HLT_OldIsoTkMu18_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFHT350_PFMET100_NoiseCleaned_v", &(this->HLT_BIT_HLT_PFHT350_PFMET100_NoiseCleaned_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFHT350_v", &(this->HLT_BIT_HLT_PFHT350_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v", &(this->HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFHT400_SixJet30_v", &(this->HLT_BIT_HLT_PFHT400_SixJet30_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFHT450_SixJet40_PFBTagCSV0p72_v", &(this->HLT_BIT_HLT_PFHT450_SixJet40_PFBTagCSV0p72_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFHT450_SixJet40_v", &(this->HLT_BIT_HLT_PFHT450_SixJet40_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v", &(this->HLT_BIT_HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFHT650_WideJetMJJ950DEtaJJ1p5_v", &(this->HLT_BIT_HLT_PFHT650_WideJetMJJ950DEtaJJ1p5_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFHT750_4JetPt50_v", &(this->HLT_BIT_HLT_PFHT750_4JetPt50_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFHT800_v", &(this->HLT_BIT_HLT_PFHT800_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFJet140_v", &(this->HLT_BIT_HLT_PFJet140_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFJet200_v", &(this->HLT_BIT_HLT_PFJet200_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFJet260_v", &(this->HLT_BIT_HLT_PFJet260_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFJet320_v", &(this->HLT_BIT_HLT_PFJet320_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFJet400_v", &(this->HLT_BIT_HLT_PFJet400_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFJet40_v", &(this->HLT_BIT_HLT_PFJet40_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFJet450_v", &(this->HLT_BIT_HLT_PFJet450_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFJet60_v", &(this->HLT_BIT_HLT_PFJet60_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFJet80_v", &(this->HLT_BIT_HLT_PFJet80_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFMET100_PFMHT100_IDTight_v", &(this->HLT_BIT_HLT_PFMET100_PFMHT100_IDTight_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFMET110_PFMHT110_IDTight_v", &(this->HLT_BIT_HLT_PFMET110_PFMHT110_IDTight_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFMET120_NoiseCleaned_Mu5_v", &(this->HLT_BIT_HLT_PFMET120_NoiseCleaned_Mu5_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFMET120_PFMHT120_IDTight_v", &(this->HLT_BIT_HLT_PFMET120_PFMHT120_IDTight_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFMET170_NoiseCleaned_v", &(this->HLT_BIT_HLT_PFMET170_NoiseCleaned_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFMET90_PFMHT90_IDTight_v", &(this->HLT_BIT_HLT_PFMET90_PFMHT90_IDTight_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v", &(this->HLT_BIT_HLT_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v));
    tree->SetBranchAddress("HLT_BIT_HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v", &(this->HLT_BIT_HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v));
    tree->SetBranchAddress("HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v", &(this->HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v));
    tree->SetBranchAddress("HLT_BIT_HLT_QuadJet45_TripleBTagCSV0p67_v", &(this->HLT_BIT_HLT_QuadJet45_TripleBTagCSV0p67_v));
    tree->SetBranchAddress("HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v", &(this->HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v));
    tree->SetBranchAddress("HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq240_v", &(this->HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq240_v));
    tree->SetBranchAddress("HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v", &(this->HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v));
    tree->SetBranchAddress("HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq500_v", &(this->HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq500_v));
    tree->SetBranchAddress("HLT_BIT_HLT_QuadPFJet_VBF_v", &(this->HLT_BIT_HLT_QuadPFJet_VBF_v));
    tree->SetBranchAddress("HLT_BIT_HLT_TkMu20_v", &(this->HLT_BIT_HLT_TkMu20_v));
    tree->SetBranchAddress("HLT_BIT_HLT_TkMu24_eta2p1_v", &(this->HLT_BIT_HLT_TkMu24_eta2p1_v));
    tree->SetBranchAddress("HLT_BIT_HLT_TkMu27_v", &(this->HLT_BIT_HLT_TkMu27_v));
    tree->SetBranchAddress("HLT_HH4bAll", &(this->HLT_HH4bAll));
    tree->SetBranchAddress("HLT_HH4bHighLumi", &(this->HLT_HH4bHighLumi));
    tree->SetBranchAddress("HLT_HH4bLowLumi", &(this->HLT_HH4bLowLumi));
    tree->SetBranchAddress("HLT_VBFHbbAll", &(this->HLT_VBFHbbAll));
    tree->SetBranchAddress("HLT_VBFHbbHighLumi", &(this->HLT_VBFHbbHighLumi));
    tree->SetBranchAddress("HLT_VBFHbbLowLumi", &(this->HLT_VBFHbbLowLumi));
    tree->SetBranchAddress("HLT_WenHbbAll", &(this->HLT_WenHbbAll));
    tree->SetBranchAddress("HLT_WenHbbHighLumi", &(this->HLT_WenHbbHighLumi));
    tree->SetBranchAddress("HLT_WenHbbLowLumi", &(this->HLT_WenHbbLowLumi));
    tree->SetBranchAddress("HLT_WmnHbbAll", &(this->HLT_WmnHbbAll));
    tree->SetBranchAddress("HLT_WmnHbbHighLumi", &(this->HLT_WmnHbbHighLumi));
    tree->SetBranchAddress("HLT_WmnHbbLowLumi", &(this->HLT_WmnHbbLowLumi));
    tree->SetBranchAddress("HLT_WtaunHbbAll", &(this->HLT_WtaunHbbAll));
    tree->SetBranchAddress("HLT_WtaunHbbHighLumi", &(this->HLT_WtaunHbbHighLumi));
    tree->SetBranchAddress("HLT_WtaunHbbLowLumi", &(this->HLT_WtaunHbbLowLumi));
    tree->SetBranchAddress("HLT_ZeeHbbAll", &(this->HLT_ZeeHbbAll));
    tree->SetBranchAddress("HLT_ZeeHbbHighLumi", &(this->HLT_ZeeHbbHighLumi));
    tree->SetBranchAddress("HLT_ZeeHbbLowLumi", &(this->HLT_ZeeHbbLowLumi));
    tree->SetBranchAddress("HLT_ZmmHbbAll", &(this->HLT_ZmmHbbAll));
    tree->SetBranchAddress("HLT_ZmmHbbHighLumi", &(this->HLT_ZmmHbbHighLumi));
    tree->SetBranchAddress("HLT_ZmmHbbLowLumi", &(this->HLT_ZmmHbbLowLumi));
    tree->SetBranchAddress("HLT_ZnnHbb", &(this->HLT_ZnnHbb));
    tree->SetBranchAddress("HLT_ZnnHbbAll", &(this->HLT_ZnnHbbAll));
    tree->SetBranchAddress("HLT_hadronic", &(this->HLT_hadronic));
    tree->SetBranchAddress("HLT_ttHhardonicAll", &(this->HLT_ttHhardonicAll));
    tree->SetBranchAddress("HLT_ttHhardonicHighLumi", &(this->HLT_ttHhardonicHighLumi));
    tree->SetBranchAddress("HLT_ttHhardonicLowLumi", &(this->HLT_ttHhardonicLowLumi));
    tree->SetBranchAddress("HLT_ttHleptonic", &(this->HLT_ttHleptonic));
    tree->SetBranchAddress("Wmass", &(this->Wmass));
    tree->SetBranchAddress("Wmass_JESDown", &(this->Wmass_JESDown));
    tree->SetBranchAddress("Wmass_JESUp", &(this->Wmass_JESUp));
    tree->SetBranchAddress("aplanarity", &(this->aplanarity));
    tree->SetBranchAddress("aplanarity_JESDown", &(this->aplanarity_JESDown));
    tree->SetBranchAddress("aplanarity_JESUp", &(this->aplanarity_JESUp));
    tree->SetBranchAddress("bTagWeight", &(this->bTagWeight));
    tree->SetBranchAddress("bTagWeight_HFDown", &(this->bTagWeight_HFDown));
    tree->SetBranchAddress("bTagWeight_HFUp", &(this->bTagWeight_HFUp));
    tree->SetBranchAddress("bTagWeight_JESDown", &(this->bTagWeight_JESDown));
    tree->SetBranchAddress("bTagWeight_JESUp", &(this->bTagWeight_JESUp));
    tree->SetBranchAddress("bTagWeight_LFDown", &(this->bTagWeight_LFDown));
    tree->SetBranchAddress("bTagWeight_LFUp", &(this->bTagWeight_LFUp));
    tree->SetBranchAddress("bTagWeight_Stats1Down", &(this->bTagWeight_Stats1Down));
    tree->SetBranchAddress("bTagWeight_Stats1Up", &(this->bTagWeight_Stats1Up));
    tree->SetBranchAddress("bTagWeight_Stats2Down", &(this->bTagWeight_Stats2Down));
    tree->SetBranchAddress("bTagWeight_Stats2Up", &(this->bTagWeight_Stats2Up));
    tree->SetBranchAddress("bTagWeight_cErr1Down", &(this->bTagWeight_cErr1Down));
    tree->SetBranchAddress("bTagWeight_cErr1Up", &(this->bTagWeight_cErr1Up));
    tree->SetBranchAddress("bTagWeight_cErr2Down", &(this->bTagWeight_cErr2Down));
    tree->SetBranchAddress("bTagWeight_cErr2Up", &(this->bTagWeight_cErr2Up));
    tree->SetBranchAddress("btag_LR_4b_2b", &(this->btag_LR_4b_2b));
    tree->SetBranchAddress("btag_LR_4b_2b_JESDown", &(this->btag_LR_4b_2b_JESDown));
    tree->SetBranchAddress("btag_LR_4b_2b_JESUp", &(this->btag_LR_4b_2b_JESUp));
    tree->SetBranchAddress("btag_lr_2b", &(this->btag_lr_2b));
    tree->SetBranchAddress("btag_lr_2b_JESDown", &(this->btag_lr_2b_JESDown));
    tree->SetBranchAddress("btag_lr_2b_JESUp", &(this->btag_lr_2b_JESUp));
    tree->SetBranchAddress("btag_lr_4b", &(this->btag_lr_4b));
    tree->SetBranchAddress("btag_lr_4b_JESDown", &(this->btag_lr_4b_JESDown));
    tree->SetBranchAddress("btag_lr_4b_JESUp", &(this->btag_lr_4b_JESUp));
    tree->SetBranchAddress("cat", &(this->cat));
    tree->SetBranchAddress("cat_JESDown", &(this->cat_JESDown));
    tree->SetBranchAddress("cat_JESUp", &(this->cat_JESUp));
    tree->SetBranchAddress("cat_btag", &(this->cat_btag));
    tree->SetBranchAddress("cat_btag_JESDown", &(this->cat_btag_JESDown));
    tree->SetBranchAddress("cat_btag_JESUp", &(this->cat_btag_JESUp));
    tree->SetBranchAddress("cat_gen", &(this->cat_gen));
    tree->SetBranchAddress("cat_gen_JESDown", &(this->cat_gen_JESDown));
    tree->SetBranchAddress("cat_gen_JESUp", &(this->cat_gen_JESUp));
    tree->SetBranchAddress("common_bdt", &(this->common_bdt));
    tree->SetBranchAddress("common_bdt_JESDown", &(this->common_bdt_JESDown));
    tree->SetBranchAddress("common_bdt_JESUp", &(this->common_bdt_JESUp));
    tree->SetBranchAddress("common_bdt_withmem1", &(this->common_bdt_withmem1));
    tree->SetBranchAddress("common_bdt_withmem1_JESDown", &(this->common_bdt_withmem1_JESDown));
    tree->SetBranchAddress("common_bdt_withmem1_JESUp", &(this->common_bdt_withmem1_JESUp));
    tree->SetBranchAddress("common_bdt_withmem2", &(this->common_bdt_withmem2));
    tree->SetBranchAddress("common_bdt_withmem2_JESDown", &(this->common_bdt_withmem2_JESDown));
    tree->SetBranchAddress("common_bdt_withmem2_JESUp", &(this->common_bdt_withmem2_JESUp));
    tree->SetBranchAddress("eta_drpair_btag", &(this->eta_drpair_btag));
    tree->SetBranchAddress("eta_drpair_btag_JESDown", &(this->eta_drpair_btag_JESDown));
    tree->SetBranchAddress("eta_drpair_btag_JESUp", &(this->eta_drpair_btag_JESUp));
    tree->SetBranchAddress("evt", &(this->evt));
    tree->SetBranchAddress("genHiggsDecayMode", &(this->genHiggsDecayMode));
    tree->SetBranchAddress("genWeight", &(this->genWeight));
    tree->SetBranchAddress("ht", &(this->ht));
    tree->SetBranchAddress("ht_JESDown", &(this->ht_JESDown));
    tree->SetBranchAddress("ht_JESUp", &(this->ht_JESUp));
    tree->SetBranchAddress("is_dl", &(this->is_dl));
    tree->SetBranchAddress("is_dl_JESDown", &(this->is_dl_JESDown));
    tree->SetBranchAddress("is_dl_JESUp", &(this->is_dl_JESUp));
    tree->SetBranchAddress("is_fh", &(this->is_fh));
    tree->SetBranchAddress("is_fh_JESDown", &(this->is_fh_JESDown));
    tree->SetBranchAddress("is_fh_JESUp", &(this->is_fh_JESUp));
    tree->SetBranchAddress("is_sl", &(this->is_sl));
    tree->SetBranchAddress("is_sl_JESDown", &(this->is_sl_JESDown));
    tree->SetBranchAddress("is_sl_JESUp", &(this->is_sl_JESUp));
    tree->SetBranchAddress("isotropy", &(this->isotropy));
    tree->SetBranchAddress("isotropy_JESDown", &(this->isotropy_JESDown));
    tree->SetBranchAddress("isotropy_JESUp", &(this->isotropy_JESUp));
    tree->SetBranchAddress("json", &(this->json));
    tree->SetBranchAddress("lumi", &(this->lumi));
    tree->SetBranchAddress("mass_drpair_btag", &(this->mass_drpair_btag));
    tree->SetBranchAddress("mass_drpair_btag_JESDown", &(this->mass_drpair_btag_JESDown));
    tree->SetBranchAddress("mass_drpair_btag_JESUp", &(this->mass_drpair_btag_JESUp));
    tree->SetBranchAddress("mean_bdisc", &(this->mean_bdisc));
    tree->SetBranchAddress("mean_bdisc_JESDown", &(this->mean_bdisc_JESDown));
    tree->SetBranchAddress("mean_bdisc_JESUp", &(this->mean_bdisc_JESUp));
    tree->SetBranchAddress("mean_bdisc_btag", &(this->mean_bdisc_btag));
    tree->SetBranchAddress("mean_bdisc_btag_JESDown", &(this->mean_bdisc_btag_JESDown));
    tree->SetBranchAddress("mean_bdisc_btag_JESUp", &(this->mean_bdisc_btag_JESUp));
    tree->SetBranchAddress("mean_dr_btag", &(this->mean_dr_btag));
    tree->SetBranchAddress("mean_dr_btag_JESDown", &(this->mean_dr_btag_JESDown));
    tree->SetBranchAddress("mean_dr_btag_JESUp", &(this->mean_dr_btag_JESUp));
    tree->SetBranchAddress("min_dr_btag", &(this->min_dr_btag));
    tree->SetBranchAddress("min_dr_btag_JESDown", &(this->min_dr_btag_JESDown));
    tree->SetBranchAddress("min_dr_btag_JESUp", &(this->min_dr_btag_JESUp));
    tree->SetBranchAddress("momentum_eig0", &(this->momentum_eig0));
    tree->SetBranchAddress("momentum_eig0_JESDown", &(this->momentum_eig0_JESDown));
    tree->SetBranchAddress("momentum_eig0_JESUp", &(this->momentum_eig0_JESUp));
    tree->SetBranchAddress("momentum_eig1", &(this->momentum_eig1));
    tree->SetBranchAddress("momentum_eig1_JESDown", &(this->momentum_eig1_JESDown));
    tree->SetBranchAddress("momentum_eig1_JESUp", &(this->momentum_eig1_JESUp));
    tree->SetBranchAddress("momentum_eig2", &(this->momentum_eig2));
    tree->SetBranchAddress("momentum_eig2_JESDown", &(this->momentum_eig2_JESDown));
    tree->SetBranchAddress("momentum_eig2_JESUp", &(this->momentum_eig2_JESUp));
    tree->SetBranchAddress("nBCSVL", &(this->nBCSVL));
    tree->SetBranchAddress("nBCSVL_JESDown", &(this->nBCSVL_JESDown));
    tree->SetBranchAddress("nBCSVL_JESUp", &(this->nBCSVL_JESUp));
    tree->SetBranchAddress("nBCSVM", &(this->nBCSVM));
    tree->SetBranchAddress("nBCSVM_JESDown", &(this->nBCSVM_JESDown));
    tree->SetBranchAddress("nBCSVM_JESUp", &(this->nBCSVM_JESUp));
    tree->SetBranchAddress("nBCSVT", &(this->nBCSVT));
    tree->SetBranchAddress("nBCSVT_JESDown", &(this->nBCSVT_JESDown));
    tree->SetBranchAddress("nBCSVT_JESUp", &(this->nBCSVT_JESUp));
    tree->SetBranchAddress("nGenBHiggs", &(this->nGenBHiggs));
    tree->SetBranchAddress("nGenBTop", &(this->nGenBTop));
    tree->SetBranchAddress("nGenQW", &(this->nGenQW));
    tree->SetBranchAddress("nMatchSimB", &(this->nMatchSimB));
    tree->SetBranchAddress("nMatchSimB_JESDown", &(this->nMatchSimB_JESDown));
    tree->SetBranchAddress("nMatchSimB_JESUp", &(this->nMatchSimB_JESUp));
    tree->SetBranchAddress("nMatchSimC", &(this->nMatchSimC));
    tree->SetBranchAddress("nMatchSimC_JESDown", &(this->nMatchSimC_JESDown));
    tree->SetBranchAddress("nMatchSimC_JESUp", &(this->nMatchSimC_JESUp));
    tree->SetBranchAddress("nMatch_hb", &(this->nMatch_hb));
    tree->SetBranchAddress("nMatch_hb_JESDown", &(this->nMatch_hb_JESDown));
    tree->SetBranchAddress("nMatch_hb_JESUp", &(this->nMatch_hb_JESUp));
    tree->SetBranchAddress("nMatch_hb_btag", &(this->nMatch_hb_btag));
    tree->SetBranchAddress("nMatch_hb_btag_JESDown", &(this->nMatch_hb_btag_JESDown));
    tree->SetBranchAddress("nMatch_hb_btag_JESUp", &(this->nMatch_hb_btag_JESUp));
    tree->SetBranchAddress("nMatch_tb", &(this->nMatch_tb));
    tree->SetBranchAddress("nMatch_tb_JESDown", &(this->nMatch_tb_JESDown));
    tree->SetBranchAddress("nMatch_tb_JESUp", &(this->nMatch_tb_JESUp));
    tree->SetBranchAddress("nMatch_tb_btag", &(this->nMatch_tb_btag));
    tree->SetBranchAddress("nMatch_tb_btag_JESDown", &(this->nMatch_tb_btag_JESDown));
    tree->SetBranchAddress("nMatch_tb_btag_JESUp", &(this->nMatch_tb_btag_JESUp));
    tree->SetBranchAddress("nMatch_wq", &(this->nMatch_wq));
    tree->SetBranchAddress("nMatch_wq_JESDown", &(this->nMatch_wq_JESDown));
    tree->SetBranchAddress("nMatch_wq_JESUp", &(this->nMatch_wq_JESUp));
    tree->SetBranchAddress("nMatch_wq_btag", &(this->nMatch_wq_btag));
    tree->SetBranchAddress("nMatch_wq_btag_JESDown", &(this->nMatch_wq_btag_JESDown));
    tree->SetBranchAddress("nMatch_wq_btag_JESUp", &(this->nMatch_wq_btag_JESUp));
    tree->SetBranchAddress("nPU0", &(this->nPU0));
    tree->SetBranchAddress("nPVs", &(this->nPVs));
    tree->SetBranchAddress("nTrueInt", &(this->nTrueInt));
    tree->SetBranchAddress("n_bjets", &(this->n_bjets));
    tree->SetBranchAddress("n_boosted_bjets", &(this->n_boosted_bjets));
    tree->SetBranchAddress("n_boosted_ljets", &(this->n_boosted_ljets));
    tree->SetBranchAddress("n_excluded_bjets", &(this->n_excluded_bjets));
    tree->SetBranchAddress("n_excluded_ljets", &(this->n_excluded_ljets));
    tree->SetBranchAddress("n_ljets", &(this->n_ljets));
    tree->SetBranchAddress("numJets", &(this->numJets));
    tree->SetBranchAddress("numJets_JESDown", &(this->numJets_JESDown));
    tree->SetBranchAddress("numJets_JESUp", &(this->numJets_JESUp));
    tree->SetBranchAddress("passPV", &(this->passPV));
    tree->SetBranchAddress("passes_btag", &(this->passes_btag));
    tree->SetBranchAddress("passes_btag_JESDown", &(this->passes_btag_JESDown));
    tree->SetBranchAddress("passes_btag_JESUp", &(this->passes_btag_JESUp));
    tree->SetBranchAddress("passes_jet", &(this->passes_jet));
    tree->SetBranchAddress("passes_jet_JESDown", &(this->passes_jet_JESDown));
    tree->SetBranchAddress("passes_jet_JESUp", &(this->passes_jet_JESUp));
    tree->SetBranchAddress("passes_mem", &(this->passes_mem));
    tree->SetBranchAddress("passes_mem_JESDown", &(this->passes_mem_JESDown));
    tree->SetBranchAddress("passes_mem_JESUp", &(this->passes_mem_JESUp));
    tree->SetBranchAddress("pt_drpair_btag", &(this->pt_drpair_btag));
    tree->SetBranchAddress("pt_drpair_btag_JESDown", &(this->pt_drpair_btag_JESDown));
    tree->SetBranchAddress("pt_drpair_btag_JESUp", &(this->pt_drpair_btag_JESUp));
    tree->SetBranchAddress("puWeight", &(this->puWeight));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q", &(this->qg_LR_flavour_4q_0q));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q", &(this->qg_LR_flavour_4q_0q_1q));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q", &(this->qg_LR_flavour_4q_0q_1q_2q));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_3q", &(this->qg_LR_flavour_4q_0q_1q_2q_3q));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_3q_JESDown", &(this->qg_LR_flavour_4q_0q_1q_2q_3q_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_3q_JESUp", &(this->qg_LR_flavour_4q_0q_1q_2q_3q_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_JESDown", &(this->qg_LR_flavour_4q_0q_1q_2q_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_2q_JESUp", &(this->qg_LR_flavour_4q_0q_1q_2q_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_JESDown", &(this->qg_LR_flavour_4q_0q_1q_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_1q_JESUp", &(this->qg_LR_flavour_4q_0q_1q_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_JESDown", &(this->qg_LR_flavour_4q_0q_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_0q_JESUp", &(this->qg_LR_flavour_4q_0q_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q", &(this->qg_LR_flavour_4q_1q));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q", &(this->qg_LR_flavour_4q_1q_2q));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_3q", &(this->qg_LR_flavour_4q_1q_2q_3q));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_3q_JESDown", &(this->qg_LR_flavour_4q_1q_2q_3q_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_3q_JESUp", &(this->qg_LR_flavour_4q_1q_2q_3q_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_JESDown", &(this->qg_LR_flavour_4q_1q_2q_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_2q_JESUp", &(this->qg_LR_flavour_4q_1q_2q_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_JESDown", &(this->qg_LR_flavour_4q_1q_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_1q_JESUp", &(this->qg_LR_flavour_4q_1q_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q", &(this->qg_LR_flavour_4q_2q));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_3q", &(this->qg_LR_flavour_4q_2q_3q));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_3q_JESDown", &(this->qg_LR_flavour_4q_2q_3q_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_3q_JESUp", &(this->qg_LR_flavour_4q_2q_3q_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_JESDown", &(this->qg_LR_flavour_4q_2q_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_2q_JESUp", &(this->qg_LR_flavour_4q_2q_JESUp));
    tree->SetBranchAddress("qg_LR_flavour_4q_3q", &(this->qg_LR_flavour_4q_3q));
    tree->SetBranchAddress("qg_LR_flavour_4q_3q_JESDown", &(this->qg_LR_flavour_4q_3q_JESDown));
    tree->SetBranchAddress("qg_LR_flavour_4q_3q_JESUp", &(this->qg_LR_flavour_4q_3q_JESUp));
    tree->SetBranchAddress("rho", &(this->rho));
    tree->SetBranchAddress("run", &(this->run));
    tree->SetBranchAddress("sphericity", &(this->sphericity));
    tree->SetBranchAddress("sphericity_JESDown", &(this->sphericity_JESDown));
    tree->SetBranchAddress("sphericity_JESUp", &(this->sphericity_JESUp));
    tree->SetBranchAddress("std_bdisc", &(this->std_bdisc));
    tree->SetBranchAddress("std_bdisc_JESDown", &(this->std_bdisc_JESDown));
    tree->SetBranchAddress("std_bdisc_JESUp", &(this->std_bdisc_JESUp));
    tree->SetBranchAddress("std_bdisc_btag", &(this->std_bdisc_btag));
    tree->SetBranchAddress("std_bdisc_btag_JESDown", &(this->std_bdisc_btag_JESDown));
    tree->SetBranchAddress("std_bdisc_btag_JESUp", &(this->std_bdisc_btag_JESUp));
    tree->SetBranchAddress("std_dr_btag", &(this->std_dr_btag));
    tree->SetBranchAddress("std_dr_btag_JESDown", &(this->std_dr_btag_JESDown));
    tree->SetBranchAddress("std_dr_btag_JESUp", &(this->std_dr_btag_JESUp));
    tree->SetBranchAddress("triggerBitmask", &(this->triggerBitmask));
    tree->SetBranchAddress("triggerDecision", &(this->triggerDecision));
    tree->SetBranchAddress("ttCls", &(this->ttCls));
    tree->SetBranchAddress("tth_mva", &(this->tth_mva));
    tree->SetBranchAddress("tth_mva_JESDown", &(this->tth_mva_JESDown));
    tree->SetBranchAddress("tth_mva_JESUp", &(this->tth_mva_JESUp));
    tree->SetBranchAddress("weight_xs", &(this->weight_xs));
    tree->SetBranchAddress("xsec", &(this->xsec));
  } //loadTree
  void init() {
    this->ncommon_mem = 0;
    for (int i=0; i < 1; i++) { this->common_mem_p_bkg[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_p[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_blr_4b[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_blr_2b[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_p_sig[i] = 0; }
    this->ncommon_mem_JESDown = 0;
    for (int i=0; i < 1; i++) { this->common_mem_JESDown_p_bkg[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_JESDown_p[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_JESDown_blr_4b[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_JESDown_blr_2b[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_JESDown_p_sig[i] = 0; }
    this->ncommon_mem_JESUp = 0;
    for (int i=0; i < 1; i++) { this->common_mem_JESUp_p_bkg[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_JESUp_p[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_JESUp_blr_4b[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_JESUp_blr_2b[i] = 0; }
    for (int i=0; i < 1; i++) { this->common_mem_JESUp_p_sig[i] = 0; }
    this->nfatjets = 0;
    for (int i=0; i < 4; i++) { this->fatjets_phi[i] = 0; }
    for (int i=0; i < 4; i++) { this->fatjets_pt[i] = 0; }
    for (int i=0; i < 4; i++) { this->fatjets_tau1[i] = 0; }
    for (int i=0; i < 4; i++) { this->fatjets_tau2[i] = 0; }
    for (int i=0; i < 4; i++) { this->fatjets_tau3[i] = 0; }
    for (int i=0; i < 4; i++) { this->fatjets_eta[i] = 0; }
    for (int i=0; i < 4; i++) { this->fatjets_mass[i] = 0; }
    for (int i=0; i < 4; i++) { this->fatjets_bbtag[i] = 0; }
    this->nfw_aj = 0;
    for (int i=0; i < 8; i++) { this->fw_aj_fw_h_alljets_nominal[i] = 0; }
    this->nfw_aj_JESDown = 0;
    for (int i=0; i < 8; i++) { this->fw_aj_JESDown_fw_h_alljets_JESDown[i] = 0; }
    this->nfw_aj_JESUp = 0;
    for (int i=0; i < 8; i++) { this->fw_aj_JESUp_fw_h_alljets_JESUp[i] = 0; }
    this->nfw_bj = 0;
    for (int i=0; i < 8; i++) { this->fw_bj_fw_h_btagjets_nominal[i] = 0; }
    this->nfw_bj_JESDown = 0;
    for (int i=0; i < 8; i++) { this->fw_bj_JESDown_fw_h_btagjets_JESDown[i] = 0; }
    this->nfw_bj_JESUp = 0;
    for (int i=0; i < 8; i++) { this->fw_bj_JESUp_fw_h_btagjets_JESUp[i] = 0; }
    this->nfw_uj = 0;
    for (int i=0; i < 8; i++) { this->fw_uj_fw_h_untagjets_nominal[i] = 0; }
    this->nfw_uj_JESDown = 0;
    for (int i=0; i < 8; i++) { this->fw_uj_JESDown_fw_h_untagjets_JESDown[i] = 0; }
    this->nfw_uj_JESUp = 0;
    for (int i=0; i < 8; i++) { this->fw_uj_JESUp_fw_h_untagjets_JESUp[i] = 0; }
    this->ngenHiggs = 0;
    for (int i=0; i < 2; i++) { this->genHiggs_phi[i] = 0; }
    for (int i=0; i < 2; i++) { this->genHiggs_eta[i] = 0; }
    for (int i=0; i < 2; i++) { this->genHiggs_mass[i] = 0; }
    for (int i=0; i < 2; i++) { this->genHiggs_id[i] = 0; }
    for (int i=0; i < 2; i++) { this->genHiggs_pt[i] = 0; }
    this->ngenTopHad = 0;
    for (int i=0; i < 2; i++) { this->genTopHad_phi[i] = 0; }
    for (int i=0; i < 2; i++) { this->genTopHad_eta[i] = 0; }
    for (int i=0; i < 2; i++) { this->genTopHad_mass[i] = 0; }
    for (int i=0; i < 2; i++) { this->genTopHad_pt[i] = 0; }
    for (int i=0; i < 2; i++) { this->genTopHad_decayMode[i] = 0; }
    this->ngenTopLep = 0;
    for (int i=0; i < 2; i++) { this->genTopLep_phi[i] = 0; }
    for (int i=0; i < 2; i++) { this->genTopLep_eta[i] = 0; }
    for (int i=0; i < 2; i++) { this->genTopLep_mass[i] = 0; }
    for (int i=0; i < 2; i++) { this->genTopLep_pt[i] = 0; }
    for (int i=0; i < 2; i++) { this->genTopLep_decayMode[i] = 0; }
    this->nhiggsCandidate = 0;
    for (int i=0; i < 4; i++) { this->higgsCandidate_mass_pruned[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_n_subjettiness[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_phi[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_pt[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_tau3[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_tau1[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_dr_top[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_dr_genHiggs[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_tau2[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_mass_softdrop[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_eta[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_mass[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_bbtag[i] = 0; }
    for (int i=0; i < 4; i++) { this->higgsCandidate_mass_softdropz2b1[i] = 0; }
    this->njets = 0;
    for (int i=0; i < 16; i++) { this->jets_mcPt[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_mcEta[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_matchBfromHadT[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_id[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightLFUp[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_pt[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_mcNumBHadrons[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_corr_JERDown[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightStats2Up[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_qgl[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightcErr2Up[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_mcPhi[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightStats1Up[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightStats1Down[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightcErr2Down[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_matchFlag[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_phi[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightStats2Down[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightLFDown[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_hadronFlavour[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_corr_JESUp[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightJESDown[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightHFDown[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_corr_JERUp[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_corr[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_corr_JER[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_corr_JESDown[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_btagCSV[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_mcM[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightHFUp[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightcErr1Down[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_mcMatchId[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_btagBDT[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightcErr1Up[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeight[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_eta[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_mass[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_bTagWeightJESUp[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_mcNumCHadrons[i] = 0; }
    for (int i=0; i < 16; i++) { this->jets_mcFlavour[i] = 0; }
    this->nleps = 0;
    for (int i=0; i < 2; i++) { this->leps_phi[i] = 0; }
    for (int i=0; i < 2; i++) { this->leps_pt[i] = 0; }
    for (int i=0; i < 2; i++) { this->leps_pdgId[i] = 0; }
    for (int i=0; i < 2; i++) { this->leps_relIso04[i] = 0; }
    for (int i=0; i < 2; i++) { this->leps_eta[i] = 0; }
    for (int i=0; i < 2; i++) { this->leps_mass[i] = 0; }
    for (int i=0; i < 2; i++) { this->leps_relIso03[i] = 0; }
    for (int i=0; i < 2; i++) { this->leps_mvaId[i] = 0; }
    this->nloose_jets = 0;
    for (int i=0; i < 6; i++) { this->loose_jets_mcPt[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_mcEta[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_matchBfromHadT[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_id[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightLFUp[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_pt[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_mcNumBHadrons[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_corr_JERDown[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightStats2Up[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_qgl[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightcErr2Up[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_mcPhi[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightStats1Up[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightStats1Down[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightcErr2Down[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_matchFlag[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_phi[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightStats2Down[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightLFDown[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_hadronFlavour[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_corr_JESUp[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightJESDown[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightHFDown[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_corr_JERUp[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_corr[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_corr_JER[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_corr_JESDown[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_btagCSV[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_mcM[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightHFUp[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightcErr1Down[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_mcMatchId[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_btagBDT[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightcErr1Up[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeight[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_eta[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_mass[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_bTagWeightJESUp[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_mcNumCHadrons[i] = 0; }
    for (int i=0; i < 6; i++) { this->loose_jets_mcFlavour[i] = 0; }
    this->nmem_ttbb = 0;
    for (int i=0; i < 12; i++) { this->mem_ttbb_p[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_chi2[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_p_err[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_efficiency[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_nperm[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_time[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_error_code[i] = 0; }
    this->nmem_ttbb_JESDown = 0;
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESDown_p[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESDown_chi2[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESDown_p_err[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESDown_efficiency[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESDown_nperm[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESDown_time[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESDown_error_code[i] = 0; }
    this->nmem_ttbb_JESUp = 0;
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESUp_p[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESUp_chi2[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESUp_p_err[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESUp_efficiency[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESUp_nperm[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESUp_time[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_ttbb_JESUp_error_code[i] = 0; }
    this->nmem_tth = 0;
    for (int i=0; i < 12; i++) { this->mem_tth_p[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_chi2[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_p_err[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_efficiency[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_nperm[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_time[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_error_code[i] = 0; }
    this->nmem_tth_JESDown = 0;
    for (int i=0; i < 12; i++) { this->mem_tth_JESDown_p[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESDown_chi2[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESDown_p_err[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESDown_efficiency[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESDown_nperm[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESDown_time[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESDown_error_code[i] = 0; }
    this->nmem_tth_JESUp = 0;
    for (int i=0; i < 12; i++) { this->mem_tth_JESUp_p[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESUp_chi2[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESUp_p_err[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESUp_efficiency[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESUp_nperm[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESUp_time[i] = 0; }
    for (int i=0; i < 12; i++) { this->mem_tth_JESUp_error_code[i] = 0; }
    this->nothertopCandidate = 0;
    for (int i=0; i < 4; i++) { this->othertopCandidate_tau1[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_etacal[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjW2btag[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_n_subjettiness_groomed[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjW2pt[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjW1btag[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjW1mass[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjNonWmass[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjNonWeta[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_pt[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_ptForRoptCalc[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_tau2[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_phi[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_tau3[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjNonWpt[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjW2mass[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_mass[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjNonWbtag[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_Ropt[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_RoptCalc[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_masscal[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_ptcal[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjW1phi[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjW1pt[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjNonWphi[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_delRopt[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjW1eta[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_fRec[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_phical[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjW2phi[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_eta[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_n_subjettiness[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_bbtag[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_sjW2eta[i] = 0; }
    for (int i=0; i < 4; i++) { this->othertopCandidate_genTopHad_dr[i] = 0; }
    this->ntopCandidate = 0;
    for (int i=0; i < 1; i++) { this->topCandidate_tau1[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_etacal[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjW2btag[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_n_subjettiness_groomed[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjW2pt[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjW1btag[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjW1mass[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjNonWmass[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjNonWeta[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_pt[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_ptForRoptCalc[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_tau2[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_phi[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_tau3[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjNonWpt[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjW2mass[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_mass[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjNonWbtag[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_Ropt[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_RoptCalc[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_masscal[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_ptcal[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjW1phi[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjW1pt[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjNonWphi[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_delRopt[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjW1eta[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_fRec[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_phical[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjW2phi[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_eta[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_n_subjettiness[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_bbtag[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_sjW2eta[i] = 0; }
    for (int i=0; i < 1; i++) { this->topCandidate_genTopHad_dr[i] = 0; }
    this->nll = 0;
    for (int i=0; i < 1; i++) { this->ll_phi[i] = 0; }
    for (int i=0; i < 1; i++) { this->ll_eta[i] = 0; }
    for (int i=0; i < 1; i++) { this->ll_mass[i] = 0; }
    for (int i=0; i < 1; i++) { this->ll_pt[i] = 0; }
    this->nmet = 0;
    for (int i=0; i < 1; i++) { this->met_phi[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_sumEt[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_pt[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_px[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_py[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_genPhi[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_genPt[i] = 0; }
    this->nmet_gen = 0;
    for (int i=0; i < 1; i++) { this->met_gen_phi[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_gen_sumEt[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_gen_pt[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_gen_px[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_gen_py[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_gen_genPhi[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_gen_genPt[i] = 0; }
    this->nmet_jetcorr = 0;
    for (int i=0; i < 1; i++) { this->met_jetcorr_phi[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_jetcorr_sumEt[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_jetcorr_pt[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_jetcorr_px[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_jetcorr_py[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_jetcorr_genPhi[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_jetcorr_genPt[i] = 0; }
    this->nmet_ttbar_gen = 0;
    for (int i=0; i < 1; i++) { this->met_ttbar_gen_phi[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_ttbar_gen_sumEt[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_ttbar_gen_pt[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_ttbar_gen_px[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_ttbar_gen_py[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_ttbar_gen_genPhi[i] = 0; }
    for (int i=0; i < 1; i++) { this->met_ttbar_gen_genPt[i] = 0; }
    this->npv = 0;
    for (int i=0; i < 1; i++) { this->pv_z[i] = 0; }
    for (int i=0; i < 1; i++) { this->pv_isFake[i] = 0; }
    for (int i=0; i < 1; i++) { this->pv_rho[i] = 0; }
    for (int i=0; i < 1; i++) { this->pv_ndof[i] = 0; }
    this->C = 0;
    this->C_JESDown = 0;
    this->C_JESUp = 0;
    this->D = 0;
    this->D_JESDown = 0;
    this->D_JESUp = 0;
    this->HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v = 0;
    this->HLT_BIT_HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV0p45_v = 0;
    this->HLT_BIT_HLT_AK8PFHT600_TrimR0p1PT0p03Mass50_BTagCSV0p45_v = 0;
    this->HLT_BIT_HLT_AK8PFHT650_TrimR0p1PT0p03Mass50_v = 0;
    this->HLT_BIT_HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v = 0;
    this->HLT_BIT_HLT_AK8PFJet360_TrimMass30_v = 0;
    this->HLT_BIT_HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_BTagCSV0p72_v = 0;
    this->HLT_BIT_HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDTight_v = 0;
    this->HLT_BIT_HLT_DiCentralPFJet55_PFMET110_NoiseCleaned_v = 0;
    this->HLT_BIT_HLT_DiPFJetAve140_v = 0;
    this->HLT_BIT_HLT_DiPFJetAve200_v = 0;
    this->HLT_BIT_HLT_DiPFJetAve260_v = 0;
    this->HLT_BIT_HLT_DiPFJetAve320_v = 0;
    this->HLT_BIT_HLT_DiPFJetAve40_v = 0;
    this->HLT_BIT_HLT_DiPFJetAve60_v = 0;
    this->HLT_BIT_HLT_DiPFJetAve80_v = 0;
    this->HLT_BIT_HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf_v = 0;
    this->HLT_BIT_HLT_DoubleIsoMu17_eta2p1_v = 0;
    this->HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v = 0;
    this->HLT_BIT_HLT_DoubleJet90_Double30_TripleBTagCSV0p67_v = 0;
    this->HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v = 0;
    this->HLT_BIT_HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v = 0;
    this->HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v = 0;
    this->HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_v = 0;
    this->HLT_BIT_HLT_Ele22_eta2p1_WPLoose_Gsf_v = 0;
    this->HLT_BIT_HLT_Ele22_eta2p1_WPTight_Gsf_v = 0;
    this->HLT_BIT_HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v = 0;
    this->HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v = 0;
    this->HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v = 0;
    this->HLT_BIT_HLT_Ele23_WPLoose_Gsf_WHbbBoost_v = 0;
    this->HLT_BIT_HLT_Ele23_WPLoose_Gsf_v = 0;
    this->HLT_BIT_HLT_Ele27_WPLoose_Gsf_WHbbBoost_v = 0;
    this->HLT_BIT_HLT_Ele27_WPLoose_Gsf_v = 0;
    this->HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_CentralPFJet30_BTagCSV07_v = 0;
    this->HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v = 0;
    this->HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_v = 0;
    this->HLT_BIT_HLT_Ele27_eta2p1_WPTight_Gsf_v = 0;
    this->HLT_BIT_HLT_Ele30WP60_Ele8_Mass55_v = 0;
    this->HLT_BIT_HLT_Ele32_eta2p1_WPLoose_Gsf_CentralPFJet30_BTagCSV07_v = 0;
    this->HLT_BIT_HLT_Ele32_eta2p1_WPLoose_Gsf_v = 0;
    this->HLT_BIT_HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v = 0;
    this->HLT_BIT_HLT_IsoMu16_eta2p1_CaloMET30_v = 0;
    this->HLT_BIT_HLT_IsoMu18_v = 0;
    this->HLT_BIT_HLT_IsoMu20_eta2p1_CentralPFJet30_BTagCSV07_v = 0;
    this->HLT_BIT_HLT_IsoMu20_eta2p1_v = 0;
    this->HLT_BIT_HLT_IsoMu20_v = 0;
    this->HLT_BIT_HLT_IsoMu24_eta2p1_CentralPFJet30_BTagCSV07_v = 0;
    this->HLT_BIT_HLT_IsoMu24_eta2p1_v = 0;
    this->HLT_BIT_HLT_IsoMu27_v = 0;
    this->HLT_BIT_HLT_IsoTkMu18_v = 0;
    this->HLT_BIT_HLT_IsoTkMu20_v = 0;
    this->HLT_BIT_HLT_IsoTkMu27_v = 0;
    this->HLT_BIT_HLT_L1_TripleJet_VBF_v = 0;
    this->HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_v = 0;
    this->HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_v = 0;
    this->HLT_BIT_HLT_LooseIsoPFTau50_Trk30_eta2p1_v = 0;
    this->HLT_BIT_HLT_MonoCentralPFJet80_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v = 0;
    this->HLT_BIT_HLT_MonoCentralPFJet80_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v = 0;
    this->HLT_BIT_HLT_Mu16_eta2p1_CaloMET30_v = 0;
    this->HLT_BIT_HLT_Mu17_TkMu8_DZ_v = 0;
    this->HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v = 0;
    this->HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v = 0;
    this->HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v = 0;
    this->HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v = 0;
    this->HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v = 0;
    this->HLT_BIT_HLT_Mu20_v = 0;
    this->HLT_BIT_HLT_Mu24_eta2p1_v = 0;
    this->HLT_BIT_HLT_Mu24_v = 0;
    this->HLT_BIT_HLT_Mu27_v = 0;
    this->HLT_BIT_HLT_Mu40_eta2p1_PFJet200_PFJet50_v = 0;
    this->HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v = 0;
    this->HLT_BIT_HLT_OldIsoMu18_v = 0;
    this->HLT_BIT_HLT_OldIsoTkMu18_v = 0;
    this->HLT_BIT_HLT_PFHT350_PFMET100_NoiseCleaned_v = 0;
    this->HLT_BIT_HLT_PFHT350_v = 0;
    this->HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v = 0;
    this->HLT_BIT_HLT_PFHT400_SixJet30_v = 0;
    this->HLT_BIT_HLT_PFHT450_SixJet40_PFBTagCSV0p72_v = 0;
    this->HLT_BIT_HLT_PFHT450_SixJet40_v = 0;
    this->HLT_BIT_HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v = 0;
    this->HLT_BIT_HLT_PFHT650_WideJetMJJ950DEtaJJ1p5_v = 0;
    this->HLT_BIT_HLT_PFHT750_4JetPt50_v = 0;
    this->HLT_BIT_HLT_PFHT800_v = 0;
    this->HLT_BIT_HLT_PFJet140_v = 0;
    this->HLT_BIT_HLT_PFJet200_v = 0;
    this->HLT_BIT_HLT_PFJet260_v = 0;
    this->HLT_BIT_HLT_PFJet320_v = 0;
    this->HLT_BIT_HLT_PFJet400_v = 0;
    this->HLT_BIT_HLT_PFJet40_v = 0;
    this->HLT_BIT_HLT_PFJet450_v = 0;
    this->HLT_BIT_HLT_PFJet60_v = 0;
    this->HLT_BIT_HLT_PFJet80_v = 0;
    this->HLT_BIT_HLT_PFMET100_PFMHT100_IDTight_v = 0;
    this->HLT_BIT_HLT_PFMET110_PFMHT110_IDTight_v = 0;
    this->HLT_BIT_HLT_PFMET120_NoiseCleaned_Mu5_v = 0;
    this->HLT_BIT_HLT_PFMET120_PFMHT120_IDTight_v = 0;
    this->HLT_BIT_HLT_PFMET170_NoiseCleaned_v = 0;
    this->HLT_BIT_HLT_PFMET90_PFMHT90_IDTight_v = 0;
    this->HLT_BIT_HLT_PFMETNoMu120_NoiseCleaned_PFMHTNoMu120_IDTight_v = 0;
    this->HLT_BIT_HLT_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v = 0;
    this->HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v = 0;
    this->HLT_BIT_HLT_QuadJet45_TripleBTagCSV0p67_v = 0;
    this->HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v = 0;
    this->HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq240_v = 0;
    this->HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v = 0;
    this->HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq500_v = 0;
    this->HLT_BIT_HLT_QuadPFJet_VBF_v = 0;
    this->HLT_BIT_HLT_TkMu20_v = 0;
    this->HLT_BIT_HLT_TkMu24_eta2p1_v = 0;
    this->HLT_BIT_HLT_TkMu27_v = 0;
    this->HLT_HH4bAll = 0;
    this->HLT_HH4bHighLumi = 0;
    this->HLT_HH4bLowLumi = 0;
    this->HLT_VBFHbbAll = 0;
    this->HLT_VBFHbbHighLumi = 0;
    this->HLT_VBFHbbLowLumi = 0;
    this->HLT_WenHbbAll = 0;
    this->HLT_WenHbbHighLumi = 0;
    this->HLT_WenHbbLowLumi = 0;
    this->HLT_WmnHbbAll = 0;
    this->HLT_WmnHbbHighLumi = 0;
    this->HLT_WmnHbbLowLumi = 0;
    this->HLT_WtaunHbbAll = 0;
    this->HLT_WtaunHbbHighLumi = 0;
    this->HLT_WtaunHbbLowLumi = 0;
    this->HLT_ZeeHbbAll = 0;
    this->HLT_ZeeHbbHighLumi = 0;
    this->HLT_ZeeHbbLowLumi = 0;
    this->HLT_ZmmHbbAll = 0;
    this->HLT_ZmmHbbHighLumi = 0;
    this->HLT_ZmmHbbLowLumi = 0;
    this->HLT_ZnnHbb = 0;
    this->HLT_ZnnHbbAll = 0;
    this->HLT_hadronic = 0;
    this->HLT_ttHhardonicAll = 0;
    this->HLT_ttHhardonicHighLumi = 0;
    this->HLT_ttHhardonicLowLumi = 0;
    this->HLT_ttHleptonic = 0;
    this->Wmass = 0;
    this->Wmass_JESDown = 0;
    this->Wmass_JESUp = 0;
    this->aplanarity = 0;
    this->aplanarity_JESDown = 0;
    this->aplanarity_JESUp = 0;
    this->bTagWeight = 0;
    this->bTagWeight_HFDown = 0;
    this->bTagWeight_HFUp = 0;
    this->bTagWeight_JESDown = 0;
    this->bTagWeight_JESUp = 0;
    this->bTagWeight_LFDown = 0;
    this->bTagWeight_LFUp = 0;
    this->bTagWeight_Stats1Down = 0;
    this->bTagWeight_Stats1Up = 0;
    this->bTagWeight_Stats2Down = 0;
    this->bTagWeight_Stats2Up = 0;
    this->bTagWeight_cErr1Down = 0;
    this->bTagWeight_cErr1Up = 0;
    this->bTagWeight_cErr2Down = 0;
    this->bTagWeight_cErr2Up = 0;
    this->btag_LR_4b_2b = 0;
    this->btag_LR_4b_2b_JESDown = 0;
    this->btag_LR_4b_2b_JESUp = 0;
    this->btag_lr_2b = 0;
    this->btag_lr_2b_JESDown = 0;
    this->btag_lr_2b_JESUp = 0;
    this->btag_lr_4b = 0;
    this->btag_lr_4b_JESDown = 0;
    this->btag_lr_4b_JESUp = 0;
    this->cat = 0;
    this->cat_JESDown = 0;
    this->cat_JESUp = 0;
    this->cat_btag = 0;
    this->cat_btag_JESDown = 0;
    this->cat_btag_JESUp = 0;
    this->cat_gen = 0;
    this->cat_gen_JESDown = 0;
    this->cat_gen_JESUp = 0;
    this->common_bdt = 0;
    this->common_bdt_JESDown = 0;
    this->common_bdt_JESUp = 0;
    this->common_bdt_withmem1 = 0;
    this->common_bdt_withmem1_JESDown = 0;
    this->common_bdt_withmem1_JESUp = 0;
    this->common_bdt_withmem2 = 0;
    this->common_bdt_withmem2_JESDown = 0;
    this->common_bdt_withmem2_JESUp = 0;
    this->eta_drpair_btag = 0;
    this->eta_drpair_btag_JESDown = 0;
    this->eta_drpair_btag_JESUp = 0;
    this->evt = 0;
    this->genHiggsDecayMode = 0;
    this->genWeight = 0;
    this->ht = 0;
    this->ht_JESDown = 0;
    this->ht_JESUp = 0;
    this->is_dl = 0;
    this->is_dl_JESDown = 0;
    this->is_dl_JESUp = 0;
    this->is_fh = 0;
    this->is_fh_JESDown = 0;
    this->is_fh_JESUp = 0;
    this->is_sl = 0;
    this->is_sl_JESDown = 0;
    this->is_sl_JESUp = 0;
    this->isotropy = 0;
    this->isotropy_JESDown = 0;
    this->isotropy_JESUp = 0;
    this->json = 0;
    this->lumi = 0;
    this->mass_drpair_btag = 0;
    this->mass_drpair_btag_JESDown = 0;
    this->mass_drpair_btag_JESUp = 0;
    this->mean_bdisc = 0;
    this->mean_bdisc_JESDown = 0;
    this->mean_bdisc_JESUp = 0;
    this->mean_bdisc_btag = 0;
    this->mean_bdisc_btag_JESDown = 0;
    this->mean_bdisc_btag_JESUp = 0;
    this->mean_dr_btag = 0;
    this->mean_dr_btag_JESDown = 0;
    this->mean_dr_btag_JESUp = 0;
    this->min_dr_btag = 0;
    this->min_dr_btag_JESDown = 0;
    this->min_dr_btag_JESUp = 0;
    this->momentum_eig0 = 0;
    this->momentum_eig0_JESDown = 0;
    this->momentum_eig0_JESUp = 0;
    this->momentum_eig1 = 0;
    this->momentum_eig1_JESDown = 0;
    this->momentum_eig1_JESUp = 0;
    this->momentum_eig2 = 0;
    this->momentum_eig2_JESDown = 0;
    this->momentum_eig2_JESUp = 0;
    this->nBCSVL = 0;
    this->nBCSVL_JESDown = 0;
    this->nBCSVL_JESUp = 0;
    this->nBCSVM = 0;
    this->nBCSVM_JESDown = 0;
    this->nBCSVM_JESUp = 0;
    this->nBCSVT = 0;
    this->nBCSVT_JESDown = 0;
    this->nBCSVT_JESUp = 0;
    this->nGenBHiggs = 0;
    this->nGenBTop = 0;
    this->nGenQW = 0;
    this->nMatchSimB = 0;
    this->nMatchSimB_JESDown = 0;
    this->nMatchSimB_JESUp = 0;
    this->nMatchSimC = 0;
    this->nMatchSimC_JESDown = 0;
    this->nMatchSimC_JESUp = 0;
    this->nMatch_hb = 0;
    this->nMatch_hb_JESDown = 0;
    this->nMatch_hb_JESUp = 0;
    this->nMatch_hb_btag = 0;
    this->nMatch_hb_btag_JESDown = 0;
    this->nMatch_hb_btag_JESUp = 0;
    this->nMatch_tb = 0;
    this->nMatch_tb_JESDown = 0;
    this->nMatch_tb_JESUp = 0;
    this->nMatch_tb_btag = 0;
    this->nMatch_tb_btag_JESDown = 0;
    this->nMatch_tb_btag_JESUp = 0;
    this->nMatch_wq = 0;
    this->nMatch_wq_JESDown = 0;
    this->nMatch_wq_JESUp = 0;
    this->nMatch_wq_btag = 0;
    this->nMatch_wq_btag_JESDown = 0;
    this->nMatch_wq_btag_JESUp = 0;
    this->nPU0 = 0;
    this->nPVs = 0;
    this->nTrueInt = 0;
    this->n_bjets = 0;
    this->n_boosted_bjets = 0;
    this->n_boosted_ljets = 0;
    this->n_excluded_bjets = 0;
    this->n_excluded_ljets = 0;
    this->n_ljets = 0;
    this->numJets = 0;
    this->numJets_JESDown = 0;
    this->numJets_JESUp = 0;
    this->passPV = 0;
    this->passes_btag = 0;
    this->passes_btag_JESDown = 0;
    this->passes_btag_JESUp = 0;
    this->passes_jet = 0;
    this->passes_jet_JESDown = 0;
    this->passes_jet_JESUp = 0;
    this->passes_mem = 0;
    this->passes_mem_JESDown = 0;
    this->passes_mem_JESUp = 0;
    this->pt_drpair_btag = 0;
    this->pt_drpair_btag_JESDown = 0;
    this->pt_drpair_btag_JESUp = 0;
    this->puWeight = 0;
    this->qg_LR_flavour_4q_0q = 0;
    this->qg_LR_flavour_4q_0q_1q = 0;
    this->qg_LR_flavour_4q_0q_1q_2q = 0;
    this->qg_LR_flavour_4q_0q_1q_2q_3q = 0;
    this->qg_LR_flavour_4q_0q_1q_2q_3q_JESDown = 0;
    this->qg_LR_flavour_4q_0q_1q_2q_3q_JESUp = 0;
    this->qg_LR_flavour_4q_0q_1q_2q_JESDown = 0;
    this->qg_LR_flavour_4q_0q_1q_2q_JESUp = 0;
    this->qg_LR_flavour_4q_0q_1q_JESDown = 0;
    this->qg_LR_flavour_4q_0q_1q_JESUp = 0;
    this->qg_LR_flavour_4q_0q_JESDown = 0;
    this->qg_LR_flavour_4q_0q_JESUp = 0;
    this->qg_LR_flavour_4q_1q = 0;
    this->qg_LR_flavour_4q_1q_2q = 0;
    this->qg_LR_flavour_4q_1q_2q_3q = 0;
    this->qg_LR_flavour_4q_1q_2q_3q_JESDown = 0;
    this->qg_LR_flavour_4q_1q_2q_3q_JESUp = 0;
    this->qg_LR_flavour_4q_1q_2q_JESDown = 0;
    this->qg_LR_flavour_4q_1q_2q_JESUp = 0;
    this->qg_LR_flavour_4q_1q_JESDown = 0;
    this->qg_LR_flavour_4q_1q_JESUp = 0;
    this->qg_LR_flavour_4q_2q = 0;
    this->qg_LR_flavour_4q_2q_3q = 0;
    this->qg_LR_flavour_4q_2q_3q_JESDown = 0;
    this->qg_LR_flavour_4q_2q_3q_JESUp = 0;
    this->qg_LR_flavour_4q_2q_JESDown = 0;
    this->qg_LR_flavour_4q_2q_JESUp = 0;
    this->qg_LR_flavour_4q_3q = 0;
    this->qg_LR_flavour_4q_3q_JESDown = 0;
    this->qg_LR_flavour_4q_3q_JESUp = 0;
    this->rho = 0;
    this->run = 0;
    this->sphericity = 0;
    this->sphericity_JESDown = 0;
    this->sphericity_JESUp = 0;
    this->std_bdisc = 0;
    this->std_bdisc_JESDown = 0;
    this->std_bdisc_JESUp = 0;
    this->std_bdisc_btag = 0;
    this->std_bdisc_btag_JESDown = 0;
    this->std_bdisc_btag_JESUp = 0;
    this->std_dr_btag = 0;
    this->std_dr_btag_JESDown = 0;
    this->std_dr_btag_JESUp = 0;
    this->triggerBitmask = 0;
    this->triggerDecision = 0;
    this->ttCls = 0;
    this->tth_mva = 0;
    this->tth_mva_JESDown = 0;
    this->tth_mva_JESUp = 0;
    this->weight_xs = 0;
    this->xsec = 0;
  } //init
}; //class

#endif
