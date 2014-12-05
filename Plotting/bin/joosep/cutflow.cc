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
#include "TTH/MEAnalysis/interface/METree.hh"

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
    CAT6,
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
            
            return CAT6;
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
    else if (cat == CAT6 || cat == CAT6mumu || cat == CAT6ee || cat == CAT6emu) {
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

int main(int argc, const char* argv[])
{
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
	
    std::map<std::string, TH1*> histmap;
    
    TStopwatch sw;
    
    long n_total_entries = 0;
    double tottime = 0.0;
    for(auto& sample : samples ) {
        
        //LFN of sample to read
        const string sample_fn = sample.getParameter<string>("fileName");
        
        //nickname of sample (must be unique)
        const string sample_nick = sample.getParameter<string>("nickName");
        
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
        
        
        TH1D* h_Vtype = add_hist_1d<TH1D>(histmap, pf + "Vtype", 0, 10);
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
		
		TH2D* h_vtype_btag_lr = add_hist_2d<TH2D>(histmap, pf + "vtype_btag_lr", 0, 10, 10, 0, 1, 20);
		
		
        TH2D* h_nperm_s_btaglr = add_hist_2d<TH2D>(histmap, pf + "nperm_s_btag_lr", 0, 3, 3, 0.9, 1, 10);
        TH2D* h_nperm_b_btaglr = add_hist_2d<TH2D>(histmap, pf + "nperm_b_btag_lr", 0, 3, 3, 0.9, 1, 10);
        
        TH2D* h_nperm_s_me = add_hist_2d<TH2D>(histmap, pf + "nperm_s_me", 0, 3, 3, 0.0, 1.0, 6);
        TH2D* h_nperm_b_me = add_hist_2d<TH2D>(histmap, pf + "nperm_b_me", 0, 3, 3, 0.0, 1.0, 6);
        
        TH2D* h_nperm_s_cat = add_hist_2d<TH2D>(histmap, pf + "nperm_s_cat", 0, 3, 3, 0, 8, 8);
        TH2D* h_nperm_b_cat = add_hist_2d<TH2D>(histmap, pf + "nperm_b_cat", 0, 3, 3, 0, 8, 8);
        
        TH2D* h_vtype_cat = add_hist_2d<TH2D>(histmap, pf + "vtype_cat", 0, 10, 10, 0, 8, 8);
        //TH2D* h_gvtype_cat = add_hist_2d<TH2D>(histmap, pf + "gen_vtype_cat", 0, 10, 10, 0, 8, 8);
        
        
        TH2D* h_cat_discr = 0;
        if (sample_type == ME_8TEV || sample_type == ME_13TEV) {
            h_cat_discr = add_hist_2d<TH2D>(histmap, pf + "cat_discr", 0, 8, 8, 0, 1, 6);
        }
        
        cout << "sample " << sample_fn << " type " << sample_type << endl;
        TFile* tf = new TFile(sample_fn.c_str());
        if (tf==0 || tf->IsZombie()) {
            std::cerr << "ERROR: could not open file " << sample_fn << " " << tf << std::endl;
            throw std::exception();
        }
        
        //create ME TTree and branch variables
        METree t((TTree*)(tf->Get("tree")));
        std::cout << "entries " << t.tree->GetEntries() << std::endl;
        
        //attach branches with MH=125 (for ME branch names)
        t.set_branch_addresses(125.0);
        
        //count number of bytes read
        long nbytes = 0;
        for (int i = 0 ;i < t.tree->GetEntries(); i++) {
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
            nbytes += t.tree->GetEntry(i);
            
            const float w = t.weight_;
            
            //keep only nominal events
            if (!(t.syst_ == 0)) {
                h_cutreasons->Fill(SYST+1);
                continue;
            }
            
            //keep only events for which Blr was calculated
            if (!(t.btag_LR_ > 0)) {
                h_cutreasons->Fill(BTAG_LR+1);
                continue;
            }
            
            //assign SL/DL hypothesis
            const bool is_sl = is_single_lepton(&t, sample_type);
            const bool is_dl = is_double_lepton(&t, sample_type);
            
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
            
            //Single lepton cuts
            if (is_sl) {
                const float lep_pt1 = t.lepton_pt_[0];
                h_lep_pt_sl->Fill(lep_pt1, w);
                
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
                
                h_nt_dl->Fill(t.numBTagM_, w);

                if (t.numBTagM_ >= 2) {
                    h_nj_dl->Fill(t.numJets_, w);
                }
                
                h_lep1_riso_dl->Fill(t.lepton_rIso_[0], w);
                h_lep2_riso_dl->Fill(t.lepton_rIso_[1], w);
				h_btag_lr_dl->Fill(t.btag_LR_, w);
				h_btag_lr_dl2->Fill(t.btag_LR_, w);
            }
            
            MECategory cat = assign_me_category(&t, sample_type);
            
            h_Vtype->Fill(t.Vtype_, w);
            h_type->Fill(t.type_, w);
			
            //h_gvtype_vtype->Fill(gen_hypo(std::abs(t.gen_))
			h_cat_btag_lr->Fill(cat, t.btag_LR_, w);
			h_vtype_btag_lr->Fill(t.Vtype_, t.btag_LR_, w);
//			
//			TTH::TTJetsRadiationMode rad_mode = TTH::assign_radiation_mode(
//				t.nMatchSimBs_, t.nMatchSimCs_
//			);
			
            //passes btag LR cut
            int btag_lr_cat = is_btag_lr_high_low(&t, cat);
            
            if (btag_lr_cat == 1) {
                h_catH->Fill(cat, w);
				//h_cat_rad_modeH->Fill(cat, rad_mode, w);
            } else if (btag_lr_cat == 0) {
                h_catL->Fill(cat, w);
				//h_cat_rad_modeL->Fill(cat, rad_mode, w);
            }
			
			//if (t.btag_LR_ >= 0) {
			if (btag_lr_cat >= 0) {
				h_cat->Fill(cat, w);
				h_vtype_cat->Fill(t.Vtype_, cat, w);
				h_cat_time->Fill(cat, t.time_, w);
				//h_cat_rad_mode->Fill(cat, rad_mode, w);
			}
			
            if (sample_type == ME_8TEV || sample_type == ME_13TEV) {
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
                
                int n_correct_perm_s = 0;
                int n_correct_perm_b = 0;
                
                for (int np=0; np<t.nPermut_; np++) {
                    if (is_correct_perm(t.perm_to_gen_[np], cat, process)) {
                        n_correct_perm_s += 1;
                    }
                    
                }
                for (int np=0; np<t.nPermut_alt_; np++) {
                    if (is_correct_perm(t.perm_to_gen_alt_[np], cat, process)) {
                        n_correct_perm_b += 1;
                    }
                }

                if (btag_lr_cat == 1) {
                    h_nperm_s_btaglr->Fill(n_correct_perm_s, t.btag_LR_, w);
                    h_nperm_b_btaglr->Fill(n_correct_perm_b, t.btag_LR_, w);
                    h_nperm_s_me->Fill(n_correct_perm_s, me_discr, w);
                    h_nperm_b_me->Fill(n_correct_perm_b, me_discr, w);
                    
                    h_nperm_s_cat->Fill(n_correct_perm_s, cat, w);
                    h_nperm_b_cat->Fill(n_correct_perm_b, cat, w);
                }
                
                h_proc->Fill(2);
            }
        }
        
        std::cout << "read " << nbytes/1024/1024 << " Mb" << std::endl;
        std::cout << "processed " << n_total_entries << " in "
        << tottime << " seconds" << std::endl ;
        tf->Close();
        
    }
    
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