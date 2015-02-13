//#define _DEBUG
#define NDEBUG

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

#include "TTH/MEAnalysis/interface/btag_lr_tree.hh"
#include "TTH/Plotting/interface/joosep/histograms_step2.h"
#include "TTH/Plotting/interface/joosep/Sample.h"
#include "TTH/Plotting/interface/easylogging++.h"
#include "TTH/Plotting/interface/joosep/helpers_step2.hh"
#include "TTH/MEAnalysis/interface/MECombination.h"

using namespace std;

const double lambda_bb = 0.1;
const double lambda_bj = 0.2;
const double lambda_cc = 0.1;
const double lambda_jj = 0.6;

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
    
    TTree* outtree_s1 = 0;
    TTree* outtree_s2 = 0;
    //const double lepton_pt_min = in.getParameter<double>("leptonPtMin");
        
    TStopwatch sw;
    
    long long n_total_entries = 0;
    double tottime = 0.0;
    for(auto& sample_pars : samples_pars ) {


        Sample sample(sample_pars);
        if (sample.treeS1 != 0) {
            outtree_s1 = sample.treeS1->tree->CloneTree(0);
            outtree_s1->SetName("tree_s1");
        }
        if (sample.treeS2 != 0) {
            outtree_s2 = sample.treeS2->tree->CloneTree(0);
            outtree_s2->SetName("tree_s2");
        }

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
            LOG(DEBUG) << "processing entry " << entry;
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
            
            //keep only nominal events
            if (!(t.syst_ == 0)) {
                hs.h_cutreasons->Fill(SYST+1);
                continue;
            }
            
            const double w = t.weight_ * wratio;

            Event* event = 0;

            //reco vtype
            const TTH::EventHypothesis vt = static_cast<TTH::EventHypothesis>(t.Vtype_);
            
            //assign SL/DL hypothesis
            const bool is_sl = is_single_lepton(&t, sample.type);
            const bool is_dl = is_double_lepton(&t, sample.type);
            MECategory cat = assign_me_category(&t, sample.type);
            RadiationMode rad = classify_radiation(&t, sample.process);
            if (!((is_sl || is_dl))) {
                continue;
            }

            hs.h_radmode->Fill(rad, w);

            //keep only events for which Blr was calculated
            if (!(t.btag_LR >= 0)) {
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
                hs.h_btag_lr_sl->Fill(t.btag_LR, w);
                hs.h_btag_lr_sl2->Fill(t.btag_LR, w);
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
                hs.h_btag_lr_dl->Fill(t.btag_LR, w);
                hs.h_btag_lr_dl2->Fill(t.btag_LR, w);
            }


            map<int, int> max_perm;
            map<int, double> max_perm_prob;
            map<int, int> has_match_map;

            max_perm[0] = -1.0;
            max_perm[1] = -1.0;

            //get trigger flags
            const bool* trf = t.triggerFlags_;
            
            hs.h_triggers->Fill(0.0, w);
            bool trig_mu = trf[22]==1 || trf[23]==1 || trf[14]==1 || trf[21]==1;
            bool trig_ele = trf[44]==1;
            if (trig_mu) {
                hs.h_triggers->Fill(1.0, w);
            }
            if (trig_ele) {
                hs.h_triggers->Fill(2.0, w);
            }
                        
            hs.h_Vtype->Fill(t.Vtype_, w);
            hs.h_type->Fill(t.type_, w);

            hs.h_btag_lr->Fill(t.btag_LR, rad, w);
            hs.h_btag_lr2->Fill(t.btag_LR2, rad, w);
            hs.h_btag_lr3->Fill(t.btag_LR3, rad, w);
            hs.h_btag_lr4->Fill(t.btag_LR4, rad, w);

            hs.h_cat_btag_lr->Fill(cat, t.btag_LR, w);
            hs.h_vtype_btag_lr->Fill(t.Vtype_, t.btag_LR, w);
            
            //passes btag LR cut
            int btag_lr_cat = is_btag_lr_high_low(&t, cat);
            
            hs.h_cat_radmode->Fill(cat, rad, w);

            const double lr_default = t.btag_lr_l_bbbb / (t.btag_lr_l_bbbb + t.btag_lr_l_bbjj);
            const double lr_cc = lambda_bb * t.btag_lr_l_bbbb / (lambda_bb * t.btag_lr_l_bbbb + (1.0 - lambda_bb - lambda_cc) * t.btag_lr_l_bbjj + lambda_cc * t.btag_lr_l_bbcc);
            const double lr_cc_bj = t.btag_lr_l_bbbb / (t.btag_lr_l_bbbb + t.btag_lr_l_bbbj + t.btag_lr_l_bbjj + t.btag_lr_l_bbcc);
            const double lr_cc_bj_w = lambda_bb * t.btag_lr_l_bbbb / (lambda_bb * t.btag_lr_l_bbbb + lambda_bj * t.btag_lr_l_bbbj + lambda_jj * t.btag_lr_l_bbjj + lambda_cc * t.btag_lr_l_bbcc);
            const double lr_wcq = (t.btag_lr_l_bbbb + t.btag_lr_l_bbbbcq) / (t.btag_lr_l_bbbb + t.btag_lr_l_bbbbcq + t.btag_lr_l_bbjj + t.btag_lr_l_bbjjcq);
           
            if (t.numJets_ >= 6) {
                hs.h_radmode->Fill(rad, w);
                hs.h_rad_lr_default  -> Fill(rad, lr_default, w);
                hs.h_rad_lr_cc       -> Fill(rad, lr_cc, w);
                hs.h_rad_lr_cc_bj    -> Fill(rad, lr_cc_bj, w);
                hs.h_rad_lr_cc_bj_w  -> Fill(rad, lr_cc_bj_w, w);
                hs.h_rad_lr_wcq      -> Fill(rad, lr_wcq, w);
            }
             
            //H
            if (btag_lr_cat == 1) {
                hs.h_catH->Fill(cat, w);
                hs.h_catH_radmode->Fill(cat, rad, w);
                //h_cat_rad_modeH->Fill(cat, rad_mode, w);
            //L
            } else if (btag_lr_cat == 0) {
                hs.h_catL->Fill(cat, w);
                hs.h_catL_radmode->Fill(cat, rad, w);
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

                    event = sample.treeS1->as_event();
                    assert(event != 0);
                    assert(!is_undef(sample.treeS1->hypo1));
                }
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

                    int selcomb = t.perm_to_gen_[t.selected_comb];
                    bool q1_match_selcomb = perm_maps::get_n(selcomb, 4);
                    bool q2_match_selcomb = perm_maps::get_n(selcomb, 5);

                    hs.h_nmatched_wqq_selected->Fill(q1_match_selcomb + q2_match_selcomb, w);

                    if (sample.step1Enabled) {
                        LOG(DEBUG) << "Wqq loop";
                        vector<Particle*> w_quarks;
                        for (unsigned int i=0; i < event->w_decays.size(); i++) {
                            LOG(DEBUG) << "Wqq loop " << i << " " << event->w_decays.size() << " " << event->w_decays[i];
                            int id = abs(event->w_decays[i]->id);
                            if (id<=6) {
                                w_quarks.push_back(event->w_decays[i]);
                                //cout << "q " << event->top_decays[i]->p4.Pt()
                                //    << " " << event->top_decays[i]->p4.Eta()
                                //    << " " << event->top_decays[i]->p4.Phi()
                                //    << " " << event->top_decays[i]->id
                                //    << endl;
                            }
                        }
                    }
                }
                
                hs.h_proc->Fill(2);

                if (outtree_s1 != 0) {
                    outtree_s1->Fill();
                }
                if (outtree_s2 != 0) {
                    outtree_s2->Fill();
                }
            } //btag_lr_cat 1 (H) and has ME
        } //entries
        
        LOG(INFO) << "read " << nbytes/1024/1024 << " Mb";
        LOG(INFO) << "processed " << n_total_entries << " in " << tottime << " seconds";
        //tf->Close();
        
        outfile->cd();
        
        if (outtree_s1 != 0) {
            outtree_s1->SetDirectory(outfile);
        }
        if (outtree_s2 != 0) {
            outtree_s2->SetDirectory(outfile);
        }

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
