void check_missed_hbb(Event* event, TTHTree* t2, int best_perm, MECategory cat, double w, std::vector<Particle*>& orig_jets, std::vector<Particle*>& orig_leptons) {
	using namespace Histograms;

	//find the spectra of the H->bb b quarks which are not matched to jets
	if (!is_undef(t2->gen_b__pt) && perm_maps::higgs_b_missed(best_perm)) {

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
}

void check_missed_tbb(Event* event, TTHTree* t2, int best_perm, MECategory cat, double w, std::vector<Particle*>& orig_jets, std::vector<Particle*>& orig_leptons) {

	using namespace Histograms;

	if (perm_maps::top_b_missed(best_perm)) {
		
		if (is_undef(t2->gen_t__b__pt) || is_undef(t2->gen_tbar__b__pt)) {
			cerr << "undefined top b pt" << endl;
			return;
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
				
				if (dr < min_dr) {
					min_dr = dr;
					nearest_match = j;

					if (dr < 0.3) {
						has_match = true;
						LOG(INFO) << "best permutation " << best_perm << " had no t->b match but dR " << dr << " j" << j->p4.Pt() << " b" << p->p4.Pt();
						break;
					}
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
}

void check_missed_lepton(Event* event, TTHTree* t2, METree* t, MECategory cat, double w, std::vector<Particle*>& orig_jets, std::vector<Particle*>& orig_leptons) {

	using namespace Histograms;

	//check if lepton correctly identified
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
	
	h_nlep_gen_reco->Fill(nlep, t->nLep_, w);
}

void check_missed_wqq(Event* event, TTHTree* t2, int best_perm, MECategory cat, double w, std::vector<Particle*>& orig_jets, std::vector<Particle*>& orig_leptons) {
	using namespace Histograms;

	if ((cat == CAT1 || cat == CAT2 || cat == CAT3 )&& perm_maps::w_q_missed(best_perm)) {
		int id1 = std::abs(t2->gen_t__w_d1__id);
		int id2 = std::abs(t2->gen_tbar__w_d1__id);

	    bool filled_fail = false;
		
	    if (is_undef(id1) || is_undef(id2)) {
	        cerr << "top undefined" << endl;
	        return;
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
	        h_failreasons_cat->Fill(FailReason::DL_AS_SL, cat, w);
			return;
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
}

int find_best_perm(METree* t, int* n_correct_perm_s, int* n_best_perm, Process process, MECategory cat, TTH::EventHypothesis vt2, double w, bool has_step1_tree) {
    using namespace Histograms;

    int best_perm = 0;
    
    for (int np=0; np < t->nPermut_; np++) {
        const int perm = t->perm_to_gen_[np];
        if (is_correct_perm(perm, cat, process)) {
            *n_correct_perm_s += 1;
            h_failreasons_cat->Fill(FailReason::MATCHED_ME, cat, w);
            
            if (has_step1_tree) {
                h_unmatched_gvtype_vtype->Fill(vt2, t->Vtype_, w);
            }
        }

        int _n = perm_maps::count_matched(perm);
        if (_n > *n_best_perm) {
            *n_best_perm = _n;
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

    return best_perm;
}

void find_match_perm(Event* ev, TTHTree* t2, std::vector<Particle*>& orig_jets, std::vector<Particle*>& orig_leptons) {

	using namespace std;

	for(auto* j : orig_jets) {
		for (auto* wd : ev->w_decays) {
			if (std::abs(wd->id) <= 6 && j->p4.DeltaR(wd->p4) < 0.3) {
				LOG(DEBUG) << "wd: " << *wd;
				j->parents.push_back(wd);
				wd->children.push_back(j);
			}
		}
	}
}