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
#include "TTH/Plotting/interface/joosep/helpers_step2.hh"
#include "TTH/Plotting/interface/joosep/histograms_step2.hh"
#include "TTH/Plotting/interface/joosep/missed_particles.hh"

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

    using namespace Histograms;
	    
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
        make_histograms(sample_nick, sample_type);
        
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

            TTH::EventHypothesis vt2 = TTH::EventHypothesis::UNKNOWN_HYPO;

            if (has_step1_tree) {
                vt2 = assing_gen_vtype(t2);
                h_gvtype_vtype->Fill(vt2, t.Vtype_, w);
                h_gvtype_cat->Fill(vt2, cat, w);
            }
            
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
			

            //cat*H
            if (btag_lr_cat == 1 && (sample_type == ME_8TEV || sample_type == ME_13TEV)) {
                double me_discr = clip_value(
                    t.probAtSgn_ /
                    (t.probAtSgn_ + 0.02 * t.probAtSgn_alt_), 0.0, 1.0
                );
                
                h_cat_discr->Fill(cat, me_discr, w);
                				
				//number of events with correct permutation, signal and background hypo
                int n_correct_perm_s = 0;
                int n_best_perm = 0;                
				
				//keep track of the best permutation (most matches)
				int best_perm = find_best_perm(&t, &n_correct_perm_s, &n_best_perm, process, cat, vt2, w, has_step1_tree);
                LOG(DEBUG) << best_perm;

                h_nperm_s_btaglr->Fill(n_correct_perm_s, t.btag_LR_, w);
                //h_nperm_b_btaglr->Fill(n_correct_perm_b, t.btag_LR_, w);
				
                h_nperm_s_me->Fill(n_correct_perm_s, me_discr, w);
                //h_nperm_b_me->Fill(n_correct_perm_b, me_discr, w);
                
                h_nperm_s_cat->Fill(n_correct_perm_s, cat, w);
                //h_nperm_b_cat->Fill(n_correct_perm_b, cat, w);
				
                // check_missed_hbb(event, t2, best_perm, cat, w, orig_jets, orig_leptons);
                // check_missed_tbb(event, t2, best_perm, cat, w, orig_jets, orig_leptons);
                // check_missed_wqq(event, t2, best_perm, cat, w, orig_jets, orig_leptons);
		      
                find_match_perm(event, t2, orig_jets, orig_leptons);
                
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