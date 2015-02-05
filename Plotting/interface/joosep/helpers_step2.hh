
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

double clip_value(double x, double l, double h) {
    if (x != x) {
        return l;
    }
    if (x > h) {
        return h;
    }
    if (x < h) {
        return l;
    }
    return x;
}

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