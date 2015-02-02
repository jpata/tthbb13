//#define _DEBUG

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
#include "TTH/TTHNtupleAnalyzer/interface/event_interpretation.hh"
#include "TTH/MEAnalysis/interface/btag_lr_tree.hh"
#include "TTH/MEAnalysis/interface/MECombination.h"
#include "TTH/Plotting/interface/joosep/histograms_step2.h"
#include "TTH/Plotting/interface/joosep/Sample.h"
#include "TTH/Plotting/interface/easylogging++.h"

using namespace std;

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
    LOG(ERROR) << "ERROR: could not interpret lepton type";
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
    LOG(ERROR) << "ERROR: could not interpret lepton type";
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

bool is_correct_perm(int perm, MECategory cat, Process prc) {
    if (cat==CAT1 || cat==CAT2 || cat==CAT3) {
        return ((perm == 111111) && prc==TTHBB) || ((perm == 111100) && prc==TTJETS); //
    }
    if (cat == CAT6ee || cat == CAT6emu || cat == CAT6mumu) {
        return ((perm == 100111) && prc==TTHBB) || ((perm == 100100) && prc==TTJETS);
    }
    return false;
}

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
    const edm::VParameterSet& samples_pars = in.getParameter<edm::VParameterSet>("samples");
    
    //limits with [first, last] events to process, indexed by full list of samples
	const std::vector<long long> ev_limits = in.getParameter<std::vector<long long>>("evLimits");
	const std::string outfn = in.getParameter<std::string>("outFile");
	const double elePt = in.getParameter<double>("elePt");
	const double muPt = in.getParameter<double>("muPt");


    TFile* outfile = new TFile(outfn.c_str(), "RECREATE");
	
	//const double lepton_pt_min = in.getParameter<double>("leptonPtMin");
	    
    TStopwatch sw;
    
    long long n_total_entries = 0;
    double tottime = 0.0;
    for(auto& sample_pars : samples_pars ) {


        Sample sample(sample_pars);
        TH1::SetDefaultSumw2(true);

        Histograms hs(sample.nickName + "_", sample.type);

        //attach branches with MH=125 (for ME branch names)
        sample.treeS2->set_branch_addresses(125.0);
		
        //count number of bytes read
        long long nbytes = 0;
        long long max_events = sample.getLastEvent();

		//if using less than full events, calculate weight modification to compensate
		const double wratio = sample.treeS2->tree->GetEntries() / max_events;
		LOG(INFO) << "wratio " << wratio;

        if (sample.skip) {
            LOG(INFO) << "Skipping sample " << sample.nickName;
            continue;
        }

        LOG(INFO) << "Looping over entries [" << sample.getFirstEvent() << " " << max_events << ")"
            << " Njob " << n_total_entries;
        for (long long entry = sample.getFirstEvent() ;entry < max_events; entry++) {
            n_total_entries += 1;
            
            if(n_total_entries % 10000 == 0) {
                sw.Stop();
                float t = sw.CpuTime();
                tottime += t;
                double time_per_event = tottime / n_total_entries;
                LOG(INFO) << n_total_entries << " " << t << " "
                    << tottime << " ETA " << (max_events - entry) * time_per_event << "s";
                sw.Start();
            }
            
            //check if we are within limits
            if ((n_total_entries < ev_limits[0]) ||
                (ev_limits[1] > ev_limits[0] && n_total_entries > ev_limits[1])
                ) {
                LOG(INFO) << "stopping loop with Njob " << n_total_entries << " "
                    << entry << " in " << sample.nickName;
                continue;
            }
            
            hs.h_proc->Fill(1);

            //zero all branch variables
            sample.treeS2->loop_initialize();
            long nb = sample.treeS2->tree->GetEntry(entry);
            nbytes += nb;

            METree t(*sample.treeS2);
            //assert(!is_undef(t.EVENT_.run));
            if (is_undef(t.EVENT_.run)) {
                LOG(ERROR) << "failed to read entry " << entry << " " << nb;
                continue;
            }
			if (sample.step1Enabled) {
				sample.treeS1->loop_initialize();

                long long idx = sample.getIndexS1(t.EVENT_.event, t.EVENT_.run, t.EVENT_.lumi);
                int nb = sample.treeS1->tree->GetEntry(
                    idx, 1
                );
				if (nb <= 0) {
					LOG(ERROR) << "failed to read entry " << entry;
					throw exception();
				}

				nbytes += nb;

                assert(!is_undef(sample.treeS1->event__run));
                
                if (t.EVENT_.run != sample.treeS1->event__run) {
                    LOG(ERROR) << "Mismatch " << t.EVENT_.run << " "
                        << sample.treeS1->event__run
                        << " i1 " << entry
                        << " i2 " << idx;
                    continue;
                }
				assert(t.EVENT_.run == sample.treeS1->event__run);
				assert(t.EVENT_.lumi == sample.treeS1->event__lumi);
				assert(t.EVENT_.event == sample.treeS1->event__id);
                assert(!is_undef(sample.treeS1->hypo1));
			}
			
			//keep only nominal events
			if (!(t.syst_ == 0)) {
				hs.h_cutreasons->Fill(SYST+1);
				continue;
			}
			
            const double w = t.weight_ * wratio;

			Event* event = 0;
			if (sample.step1Enabled) {
				event = sample.treeS1->as_event();
                assert(event != 0);
                assert(!is_undef(sample.treeS1->hypo1));
			}

            //reco vtype
            const TTH::EventHypothesis vt = static_cast<TTH::EventHypothesis>(t.Vtype_);
            
            //assign SL/DL hypothesis
            const bool is_sl = is_single_lepton(&t, sample.type);
            const bool is_dl = is_double_lepton(&t, sample.type);
            MECategory cat = assign_me_category(&t, sample.type);

            if (!((is_sl || is_dl))) {
                continue;
            }

            //keep only events for which Blr was calculated
            if (!(t.btag_LR_ >= 0)) {
                hs.h_cutreasons->Fill(BTAG_LR+1);
                continue;
            }

			//Single lepton cuts
            if (is_sl) {
				const float lep_pt1 = t.lepton_pt_[0];
				//const float lep_id = t.lepton_id_[0];
                hs.h_lep_pt_sl->Fill(lep_pt1, w);
				
                //Offline cut on lepton
				if (vt == TTH::EventHypothesis::en) {
					if (elePt>0 && lep_pt1 < elePt) {
						hs.h_cutreasons->Fill(LEPTON+1);
                        continue;
					}
				}
                else if (vt == TTH::EventHypothesis::mun) {
                    if (muPt > 0 && lep_pt1 < muPt) {
                        hs.h_cutreasons->Fill(LEPTON+1);
                        continue;
                    }
                }                
                
                hs.h_nt_sl->Fill(t.numBTagM_, w);
                if (t.numBTagM_ >= 3) {
                    hs.h_nj_sl->Fill(t.numJets_, w);
                }
                
                hs.h_lep_riso_sl->Fill(t.lepton_rIso_[0], w);
				hs.h_btag_lr_sl->Fill(t.btag_LR_, w);
				hs.h_btag_lr_sl2->Fill(t.btag_LR_, w);
            }
			
            //dilepton cuts
            if (is_dl) {
                const float lep_pt1 = t.lepton_pt_[0];
                const int lep_id1 = abs(t.lepton_type_[0]);
                hs.h_lep1_pt_dl->Fill(lep_pt1, w);

                const float lep_pt2 = t.lepton_pt_[1];
                const int lep_id2 = abs(t.lepton_type_[1]);
                hs.h_lep2_pt_dl->Fill(lep_pt2, w);
				
				if (vt == TTH::EventHypothesis::ee || vt == TTH::EventHypothesis::taue) {
					if (elePt>0 &&
                        ((lep_id1 == 11 && lep_pt1 < elePt) ||
                        (lep_id2 == 11 && lep_pt2 < elePt))
                    ) {
						hs.h_cutreasons->Fill(LEPTON+1);
                        continue;
					}
				}
                else if (vt == TTH::EventHypothesis::mumu || vt == TTH::EventHypothesis::taumu) {
                    if (muPt>0 &&
                        ((lep_id1 == 13 && lep_pt1 < muPt) ||
                        (lep_id2 == 13 && lep_pt2 < muPt))
                    ) {
                        hs.h_cutreasons->Fill(LEPTON+1);
                        continue;
                    }
                }
                else if (vt == TTH::EventHypothesis::emu) {
                    const float ele_pt = lep_id1 == 11 ? lep_pt1 : lep_pt2;
                    const float mu_pt = lep_id1 == 13 ? lep_pt1 : lep_pt2;
                    if (elePt > 0 && ele_pt < elePt) {
                        hs.h_cutreasons->Fill(LEPTON+1);
                    }
                    if (muPt > 0 && mu_pt < muPt) {
                        hs.h_cutreasons->Fill(LEPTON+1);
                    }
                }
				
                hs.h_nt_dl->Fill(t.numBTagM_, w);

                if (t.numBTagM_ >= 2) {
                    hs.h_nj_dl->Fill(t.numJets_, w);
                }
                
                hs.h_lep1_riso_dl->Fill(t.lepton_rIso_[0], w);
                hs.h_lep2_riso_dl->Fill(t.lepton_rIso_[1], w);
				hs.h_btag_lr_dl->Fill(t.btag_LR_, w);
				hs.h_btag_lr_dl2->Fill(t.btag_LR_, w);
            }


            map<int, int> max_perm;
            map<int, double> max_perm_prob;
            map<int, int> has_match_map;

            max_perm[0] = -1.0;
            max_perm[1] = -1.0;

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
			hs.h_triggers->Fill(0.0, w);
			bool trig_mu = trf[22]==1 || trf[23]==1 || trf[14]==1 || trf[21]==1;
			bool trig_ele = trf[44]==1;
			if (trig_mu) {
				hs.h_triggers->Fill(1.0, w);
			}
			if (trig_ele) {
				hs.h_triggers->Fill(2.0, w);
			}
			//std::cout << trig_mu << std::endl;
			
			//            if (i<10) {
			//                std::cout << "triggerflags ";
			//                for (int j=0;j<70;j++)
			//                    std::cout << trf[j];
			//                std::cout << endl;
			//            }
						
            hs.h_Vtype->Fill(t.Vtype_, w);
            hs.h_type->Fill(t.type_, w);
			//TTH::EventHypothesis vt2 = TTH::EventHypothesis::UNKNOWN_HYPO;

			// if (has_step1_tree) {
			// 	vt2 = assing_gen_vtype(t2);
			// 	hs.h_gvtype_vtype->Fill(vt2, t.Vtype_, w);
			// 	hs.h_gvtype_cat->Fill(vt2, cat, w);
			// }
			
            //h_gvtype_vtype->Fill(gen_hypo(std::abs(t.gen_))
			hs.h_cat_btag_lr->Fill(cat, t.btag_LR_, w);
			hs.h_vtype_btag_lr->Fill(t.Vtype_, t.btag_LR_, w);
			
            //passes btag LR cut
            int btag_lr_cat = is_btag_lr_high_low(&t, cat);
			
			
			//H
            if (btag_lr_cat == 1) {
                hs.h_catH->Fill(cat, w);
				//h_cat_rad_modeH->Fill(cat, rad_mode, w);
			//L
            } else if (btag_lr_cat == 0) {
                hs.h_catL->Fill(cat, w);
				//h_cat_rad_modeL->Fill(cat, rad_mode, w);
            }
			
			//H or L
			if (btag_lr_cat >= 0) {
				hs.h_cat->Fill(cat, w);
				hs.h_vtype_cat->Fill(t.Vtype_, cat, w);
				hs.h_cat_time->Fill(cat, t.time_, w);

				//h_cat_rad_mode->Fill(cat, rad_mode, w);
			}
			
            if (btag_lr_cat == 1 && (sample.type == ME_8TEV || sample.type == ME_13TEV)) {
                double me_discr = t.probAtSgn_ /
                (t.probAtSgn_ + 0.02 * t.probAtSgn_alt_);
                
                if (me_discr > 1.0)
                    me_discr = 1.0;
                if (me_discr < 0.0)
                    me_discr = 0.0;
                if (me_discr != me_discr)
                    me_discr = 0.0;
                
                if (btag_lr_cat == 1) {
                    hs.h_discr->Fill(me_discr, w);
                    hs.h_cat_discr->Fill(cat, me_discr, w);
                }
				
				// //number of events with correct permutation, signal and background hypo
                int n_correct_perm_s = 0;
                //int n_correct_perm_b = 0;
				
				// //keep track of the best permutation (most matches)
				int best_perm = 0;
				int n_best_perm = 0;
                //int idx_best_perm = -1;

                for (int np=0; np < t.nPermut_; np++) {
					const int perm = t.perm_to_gen_[np];
                    if (is_correct_perm(perm, cat, sample.process)) {
                        n_correct_perm_s += 1;
                    }

                    //number of particles matched out of 6
					int _n = perm_maps::count_matched(perm);
					if (_n > n_best_perm) {
						n_best_perm = _n;
						best_perm = perm;
                        //idx_best_perm = np;
					}
                }

                //if (cat == CAT1 || cat == CAT2 || cat == CAT3) {
                if (cat == CAT1) {

                    //Now we know the best matching permutation
                    //We can check if any of the W->qq quarks were not matched in the best case
                    bool q1_match = perm_maps::get_n(best_perm, 4);
                    bool q2_match = perm_maps::get_n(best_perm, 5);
                    //int best_perm_to_jet = t.perm_to_jet_[idx_best_perm];
                    //int q1_idx = perm_maps::get_n(best_perm_to_jet, 4);
                    //int q2_idx = perm_maps::get_n(best_perm_to_jet, 5);

                    int nmatched = q1_match + q2_match;

                    hs.h_nmatched_wqq->Fill(nmatched, w);

                    // LOG(DEBUG) << "match Wqq perm_to_gen[" << idx_best_perm << "]="
                    //     << best_perm
                    //     << " perm_to_jet[" << idx_best_perm << "]=" << best_perm_to_jet
                    //     << " qm " << q1_match << " " << q2_match
                    //     << " " << q1_idx << " " << q2_idx
                    //     << " nmatched " << nmatched;

                    // for (int i=2; i<t.nJet_; i++) {
                    //     std::cout << "j " << i << " " << t.jet_pt_[i]
                    //         << " " << t.jet_eta_[i]
                    //         << " " << t.jet_phi_[i]
                    //         << " " << t.jet_csv_[i]
                    //         << " " << endl;
                    // }

                    vector<Particle*> w_quarks;
                    if (sample.step1Enabled) {
                        for (int i=0; i<4; i++) {
                            int id = abs(event->top_decays[i]->id);
                            if (id<=6) {
                                w_quarks.push_back(event->top_decays[i]);
                            }
                        }
                    }
                    for (unsigned int nq=0; nq < w_quarks.size(); nq++) {
                        auto* q = w_quarks[nq];
                        bool match = false;
                        for (int i=0; i<t.nJet_; i++) {
                            TLorentzVector v(1.0, 0.0, 0.0, 1.0);
                            v.SetPtEtaPhiM(t.jet_pt_[i], t.jet_eta_[i], t.jet_phi_[i], t.jet_m_[i]); 
                            double dr = q->p4.DeltaR(v);
                            if (dr < 0.5) {
                                // cout << "matched pt " << q->p4.Pt() << " " << v.Pt()
                                //     << " eta " << q->p4.Eta() << " " << v.Eta()
                                //     << " phi " << q->p4.Phi() << " " << v.Phi()
                                //     << " " << nq << " " << i << endl;
                                match = true;
                            }
                        }
                        if (!match) {
                            // cout << "Could not match q " << q->p4.Pt()
                            // << " " << q->p4.Eta()
                            // << " " << q->p4.Phi()
                            // << " " << endl;

                            hs.h_unmatched_wqq_pt->Fill(q->p4.Pt(), w);
                            hs.h_unmatched_wqq_eta->Fill(q->p4.Eta(), w);
                        } else {
                            hs.h_matched_wqq_pt->Fill(q->p4.Pt(), w);
                            hs.h_matched_wqq_eta->Fill(q->p4.Eta(), w);
                        }
                    }
                }

				// h_max_perm_s_cat->Fill(perm_maps::map2[best_perm], cat, w);
				
				// for (int i=1;i<7;i++) {
				// 	if (perm_maps::has_n(best_perm, i)) {
				// 		h_matched_perm_s_cat->Fill(i - 1, cat, w);
				// 	} else {
				// 		h_unmatched_perm_s_cat->Fill(i - 1, cat, w);
				// 	}
				// }
				
                
// 				//H
//                 if (btag_lr_cat == 1) {
//                     //h_nperm_s_btaglr->Fill(n_correct_perm_s, t.btag_LR_, w);
//                     //h_nperm_b_btaglr->Fill(n_correct_perm_b, t.btag_LR_, w);
					
//                     //h_nperm_s_me->Fill(n_correct_perm_s, me_discr, w);
//                     //h_nperm_b_me->Fill(n_correct_perm_b, me_discr, w);
                    
//                     //h_nperm_s_cat->Fill(n_correct_perm_s, cat, w);
//                     //h_nperm_b_cat->Fill(n_correct_perm_b, cat, w);
					
// 					//find the spectra of the H->bb b quarks which are not matched to jets
// 					if (has_step1_tree && !is_undef(t2->gen_b__pt) && perm_maps::higgs_b_missed(best_perm)) {

//                         bool filled_fail = false; 
// 						for (auto* p : event->higgs_decays) {
// 							double min_dr = 100.0;
// 							Particle* nearest_match = 0;
// 							bool has_match = false;
// 							for (auto* j : orig_jets) {
// 								double dr = j->p4.DeltaR(p->p4);
// 								if (dr < min_dr) {
// 									min_dr = dr;
// 									nearest_match = j;
// 								}
// 								//cout << dr << endl;
// 								if (dr < 0.3) {
// 									has_match = true;
// 									break;
// 								}
// 							}
// 							if (!has_match) {
//                                 assert(nearest_match != 0);
// 								h_unmatchedHbb_pt->Fill(nearest_match->p4.Pt(), p->p4.Pt(), w);
// 								if (p->p4.Pt() > 30) {
//                                     if (!filled_fail) {
// 									   h_failreasons_cat->Fill(FailReason::NO_H_B, cat, w);
//                                        filled_fail = true;
//                                     }
// 									h_unmatchedHbb_eta->Fill(nearest_match->p4.Eta(), p->p4.Eta(), w);
// 									float csvval = nearest_match->idx >= 0 ? t2->jet__bd_csv[nearest_match->idx] : -1;
// 									if (csvval < 0) {
// 										csvval = 0;
// 									}
// 									h_unmatchedHbb_csv->Fill(csvval, w);
// 									h_unmatchedHbb_jetid->Fill(nearest_match->idx >= 0 ? t2->jet__jetId[nearest_match->idx] : -1, w);
// 									h_unmatchedHbb_dr->Fill(min_dr, w);
// 								}
// 							}
// 						}
// 					} //missed higgs b
					
// 					if (has_step1_tree && perm_maps::top_b_missed(best_perm)) {
						
// 						if (is_undef(t2->gen_t__b__pt) || is_undef(t2->gen_tbar__b__pt)) {
// 							cerr << "undefined top b pt" << endl;
// 							continue;
// 						}
// 						Particle p1(t2->gen_t__b__pt, t2->gen_t__b__eta, t2->gen_t__b__phi, t2->gen_t__b__mass, 5);
// 						Particle p2(t2->gen_tbar__b__pt, t2->gen_tbar__b__eta, t2->gen_tbar__b__phi, t2->gen_tbar__b__mass, -5);

//                         bool filled_fail = false;
						
// 						for (auto* p : {&p1, &p2}) {
							
// 							double min_dr = 100.0;
// 							Particle* nearest_match = 0;
// 							bool has_match = false;
							
// 							int ij = 0;
// 							for (auto* j : orig_jets) {
								
// 								//cout << t2->jet__pt[ij] << " " << t2->jet__eta[ij] << " " << t2->jet__phi[ij] << " " << t2->jet__mass[ij] << endl;
// 								ij++;
// 								double dr = j->p4.DeltaR(p->p4);
								
// 								if (dr < 0.3 && dr < min_dr) {
// 									has_match = true;
// 									break;
// 								}
								
// 								if (dr < min_dr) {
// 									min_dr = dr;
// 									nearest_match = j;
// 								}
// 							}
							
// 							if (!has_match) {
//                                 assert(nearest_match != 0);
// 								//cout << "tb " << t.EVENT_.run << " " << t.EVENT_.lumi << " " << t.EVENT_.event << endl;
//                                 if (!filled_fail) {
//                                    h_failreasons_cat->Fill(FailReason::NO_T_B, cat, w);
//                                    filled_fail = true;
//                                 }
// 								h_unmatched_tb_pt->Fill(nearest_match->p4.Pt(), p->p4.Pt(), w);
								
// 								if (p->p4.Pt() > 30 ) {
// 									h_unmatched_tb_eta->Fill(nearest_match->p4.Eta(), p->p4.Eta(), w);
// 									float csvval = nearest_match->idx >= 0 ? t2->jet__bd_csv[nearest_match->idx] : -1;
// 									if (csvval < 0) {
// 										csvval = 0;
// 									}
// 									h_unmatched_tb_csv->Fill(csvval, w);
// 									h_unmatched_tb_jetid->Fill(nearest_match->idx >= 0 ? t2->jet__jetId[nearest_match->idx] : -1, w);
// 									h_unmatched_tb_dr->Fill(min_dr, w);
// 								}
// 							}
// 						}
// 					} //missed top b
					
// 					if ((cat == CAT1 || cat == CAT2 || cat == CAT3 ) && has_step1_tree && perm_maps::w_q_missed(best_perm)) {
// 						int id1 = std::abs(t2->gen_t__w_d1__id);
// 						int id2 = std::abs(t2->gen_tbar__w_d1__id);

//                         bool filled_fail = false;
						
//                         if (is_undef(id1) || is_undef(id2)) {
//                             cerr << "top undefined" << endl;
//                             continue;
//                         }
// 						Particle* p1 = 0;
// 						Particle* p2 = 0;
// 						//t is hadronic
// 						if (id1>0 && id1 < 10) {
// 							p1 = new Particle(t2->gen_t__w_d1__pt, t2->gen_t__w_d1__eta, t2->gen_t__w_d1__phi, t2->gen_t__w_d1__mass, t2->gen_t__w_d1__id);
// 							p2 = new Particle(t2->gen_t__w_d2__pt, t2->gen_t__w_d2__eta, t2->gen_t__w_d2__phi, t2->gen_t__w_d2__mass, t2->gen_t__w_d2__id);
// 						}
// 						//tbar is hadronic
// 						else if (id2>0 && id2 < 10) {
// 							p1 = new Particle(t2->gen_tbar__w_d1__pt, t2->gen_tbar__w_d1__eta, t2->gen_tbar__w_d1__phi, t2->gen_tbar__w_d1__mass, t2->gen_tbar__w_d1__id);
// 							p2 = new Particle(t2->gen_tbar__w_d2__pt, t2->gen_tbar__w_d2__eta, t2->gen_tbar__w_d2__phi, t2->gen_tbar__w_d2__mass, t2->gen_tbar__w_d2__id);
// 						} else {
// //							LOG(ERROR) << "SL event but no hadronic W " << id1 << " " << id2;
//                             h_failreasons_cat->Fill(FailReason::DL_AS_SL, cat, w);

// 							continue;
// 						}
						
// 						for (auto* p : {p1, p2}) {
							
// 							double min_dr = 100.0;
// 							Particle* nearest_match = 0;
// 							bool has_match = false;
							
// 							int ij = 0;
// 							for (auto* j : orig_jets) {
								
// 								//cout << t2->jet__pt[ij] << " " << t2->jet__eta[ij] << " " << t2->jet__phi[ij] << " " << t2->jet__mass[ij] << endl;
// 								ij++;
// 								double dr = j->p4.DeltaR(p->p4);
								
// 								if (dr < 0.3 && dr < min_dr) {
// 									has_match = true;
// 									break;
// 								}
								
// 								if (dr < min_dr) {
// 									min_dr = dr;
// 									nearest_match = j;
// 								}
// 							}
							
// 							if (!has_match) {
//                                 assert(nearest_match != 0);
// 								//cout << "tb " << t.EVENT_.run << " " << t.EVENT_.lumi << " " << t.EVENT_.event << endl;
//                                 if (!filled_fail) {
//                                    h_failreasons_cat->Fill(FailReason::NO_W_Q, cat, w);
//                                    filled_fail = true;
//                                 }
// 								h_unmatched_Wqq_pt->Fill(nearest_match->p4.Pt(), p->p4.Pt(), w);
								
// 								if (p->p4.Pt() > 30) {
// 									h_unmatched_Wqq_eta->Fill(nearest_match->p4.Eta(), p->p4.Eta(), w);
// 									float csvval = nearest_match->idx >= 0 ? t2->jet__bd_csv[nearest_match->idx] : -1;
// 									if (csvval < 0) {
// 										csvval = 0;
// 									}
// 									h_unmatched_Wqq_csv->Fill(csvval, w);
// 									h_unmatched_Wqq_jetid->Fill(nearest_match->idx >= 0 ? t2->jet__jetId[nearest_match->idx] : -1, w);
// 									h_unmatched_Wqq_id->Fill(std::abs(p->id), w);
// 									h_unmatched_Wqq_dr->Fill(min_dr, w);
// 								}
// 							}
// 						}
// 						delete p1;
// 						delete p2;
// 					}
					
// 					// check if lepton correctly identified
// 					if (has_step1_tree) {
// 						int nlep = 0;
						
//                         bool filled_fail = false;
// 						int nele = 0, nmu = 0, ntau = 0;
// 						for (auto* p : event->top_decays) {
							
// 							double min_dr = 100.0;
// 							Particle* nearest_match = 0;
// 							bool has_match = false;
							
							
// 							int abs_id = std::abs(p->id);
							
// 							if (abs_id == 11) {
// 								nele += 1;
// 							}
// 							if (abs_id == 13) {
// 								nmu += 1;
// 							}
// 							if (abs_id == 15) {
// 								ntau += 1;
// 							}
							
// 							//leptons
// 							if (abs_id == 11 || abs_id == 13 || abs_id == 15) {
// 								nlep += 1;
								
// 								for (auto* l : orig_leptons) {
// 									double dr = l->p4.DeltaR(p->p4);
									
// 									if (dr < 0.3 && dr < min_dr) {
// 										has_match = true;
// 									}
									
// 									if (dr < min_dr) {
// 										min_dr = dr;
// 										nearest_match = l;
// 									}
// 								}
								
// 								if (!has_match) {
//                                     assert(nearest_match != 0);
// 									//cout << "lepton " << t.EVENT_.run << " " << t.EVENT_.lumi << " " << t.EVENT_.event << endl;
//                                     if (!filled_fail) {
//                                        h_failreasons_cat->Fill(FailReason::NO_LEPTON, cat, w);
//                                        filled_fail = true;
//                                     }

// 									h_unmatched_lepton_pt->Fill(nearest_match->p4.Pt(), p->p4.Pt(), w);
// 									h_unmatched_lepton_eta->Fill(nearest_match->p4.Eta(), p->p4.Eta(), w);
// 									h_unmatched_lepton_dr->Fill(min_dr, w);
// 									h_unmatched_lepton_id->Fill(abs_id, std::abs(nearest_match->id), w);
// 								}
// 							}
// 						} //top decays
						
// 						h_nlep_gen_reco->Fill(nlep, t.nLep_, w);
// 					}
//                 } //btag lr cat 1 (H)
				
                
                hs.h_proc->Fill(2);
            } //btag_lr_cat 1 (H) and has ME
		
			//delete event;
        } //entries
        
        LOG(INFO) << "read " << nbytes/1024/1024 << " Mb";
        LOG(INFO) << "processed " << n_total_entries << " in " << tottime << " seconds";
        //tf->Close();
        
        outfile->cd();
        
        for(auto& kv : hs.histmap) {
            const std::string& k = kv.first;
            TH1* h = kv.second;
            h->SetDirectory(outfile);
            LOG(INFO) << "saving " << k << " " << h->Integral();
        }

        
    } //samples
        
    outfile->Write();
    outfile->Close();
    
    
}