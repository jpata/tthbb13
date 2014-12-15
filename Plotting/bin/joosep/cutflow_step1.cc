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
#include "TH2D.h"
#include "TH3D.h"
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

using namespace std;

template <class T>
T* add_hist_1d(std::map<std::string, TH1*>& histmap, string hname, int b1, int b2) {
    histmap[hname] = new T(hname.c_str(), hname.c_str(), b2-b1, b1, b2);
    histmap[hname]->Sumw2();
    return (T*)histmap[hname];
}

template <class T>
T* add_hist_1d(std::map<std::string, TH1*>& histmap, string hname, double b1, double b2, int nb) {
    histmap[hname] = new T(hname.c_str(), hname.c_str(), nb, b1, b2);
    histmap[hname]->Sumw2();
    return (T*)histmap[hname];
}

template <class T>
T* add_hist_2d(std::map<std::string, TH1*>& histmap, string hname, double b11, double b21, int nb1, double b12, double b22, int nb2) {
    histmap[hname] = new T(hname.c_str(), hname.c_str(), nb1, b11, b21, nb2, b12, b22);
    histmap[hname]->Sumw2();
    return (T*)histmap[hname];
}

template <class T>
T* add_hist_3d(std::map<std::string, TH1*>& histmap, string hname, double b11, double b21, int nb1, double b12, double b22, int nb2, double b13, double b23, int nb3) {
    histmap[hname] = new T(hname.c_str(), hname.c_str(), nb1, b11, b21, nb2, b12, b22, nb3, b13, b23);
    histmap[hname]->Sumw2();
    return (T*)histmap[hname];
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
    
    std::map<std::string, TH1*> histmap;
    
    TStopwatch sw;
    
    long n_total_entries = 0;
    double tottime = 0.0;
    
    
    TFile* outfile = new TFile("outfile_step1.root", "RECREATE");

    for(auto& sample : samples ) {
        
        //LFN of sample to read
        const string sample_fn = sample.getParameter<string>("fileName");
        
        //nickname of sample (must be unique)
        const string sample_nick = sample.getParameter<string>("nickName");
        const string tree_name = sample.getParameter<string>("treeName");
        
        //sample type, which may affect the meaning/contents of the TTrees
        //const SampleType sample_type = static_cast<SampleType>(sample.getParameter<int>("type"));
        
        std::cout << "opening file " << sample_fn.c_str() << std::endl;
        TFile* tf = new TFile(sample_fn.c_str());
        if (tf==0 || tf->IsZombie()) {
            std::cerr << "ERROR: could not open file " << sample_fn << " " << tf << std::endl;
            throw std::exception();
        }
        
        const std::string pf(sample_nick + "_");
        outfile->cd();
        
		TH1D* h_top1_mass = add_hist_1d<TH1D>(histmap, pf+"top1_mass", 100, 400, 60);
		TH1D* h_top2_mass = add_hist_1d<TH1D>(histmap, pf+"top2_mass", 100, 400, 60);
		TH1D* h_d_top_mass = add_hist_1d<TH1D>(histmap, pf+"d_top_mass", 100, 400, 60);
		TH1D* h_top1_pt = add_hist_1d<TH1D>(histmap, pf+"top1_pt", 0, 400, 60);
		TH1D* h_top2_pt = add_hist_1d<TH1D>(histmap, pf+"top2_pt", 0, 400, 60);
        TH1D* h_d_top_pt = add_hist_1d<TH1D>(histmap, pf+"d_top_pt", 0, 400, 60);

        TH1D* h_lep_puch_iso = add_hist_1d<TH1D>(histmap, pf+"lep_puch_iso", 0, 50, 20);
        TH1D* h_lep_p_iso = add_hist_1d<TH1D>(histmap, pf+"lep_p_iso", 0, 50, 20);
        TH1D* h_lep_ph_iso = add_hist_1d<TH1D>(histmap, pf+"lep_ph_iso", 0, 50, 20);
        TH1D* h_lep_hc_iso = add_hist_1d<TH1D>(histmap, pf+"lep_hc_iso", 0, 50, 20);
        TH1D* h_lep_ch_iso = add_hist_1d<TH1D>(histmap, pf+"lep_ch_iso", 0, 50, 20);
		TH1D* h_lep_ec_iso = add_hist_1d<TH1D>(histmap, pf+"lep_ec_iso", 0, 50, 20);
		
		TH1D* h_lep_rel_iso = add_hist_1d<TH1D>(histmap, pf+"lep_rel_iso", 0, 2, 20);
		
		TH2D* h_lep_pt_iso_mu = add_hist_2d<TH2D>(histmap, pf+"lep_pt_iso_mu", 0, 600, 60, 0, 5, 20);
        TH2D* h_lep_pt_iso_ele = add_hist_2d<TH2D>(histmap, pf+"lep_pt_iso_ele", 0, 600, 60, 0, 5, 20);
        
        TH3D* h_lep_pt_iso_npv_mu = add_hist_3d<TH3D>(histmap, pf+"lep_pt_iso_npv_mu", 0, 600, 60, 0, 5, 20, 0, 50, 50);
        TH3D* h_lep_pt_iso_npv_ele = add_hist_3d<TH3D>(histmap, pf+"lep_pt_iso_npv_ele", 0, 600, 60, 0, 5, 20, 0, 50, 50);
        
        TH3D* h_lep_pt_iso2_npv_mu = add_hist_3d<TH3D>(histmap, pf+"lep_pt_iso2_npv_mu", 0, 600, 60, 0, 0.2, 20, 0, 50, 50);
        TH3D* h_lep_pt_iso2_npv_ele = add_hist_3d<TH3D>(histmap, pf+"lep_pt_iso2_npv_ele", 0, 600, 60, 0, 0.2, 20, 0, 50, 50);
        
        //create ME TTree and branch variables
        TTHTree t((TTree*)(tf->Get(tree_name.c_str())));
        std::cout << sample_fn << " " << sample_nick << " entries " << t.tree->GetEntries() << std::endl;
       	 
        t.set_branch_addresses();
       	t.tree->SetBranchStatus("*", false); 
       	t.tree->SetBranchStatus("n__lep", true); 
       	t.tree->SetBranchStatus("lep__*", true);
       	t.tree->SetBranchStatus("n__pv", true);
       	t.tree->SetBranchStatus("gen_t*", true); 
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
            if ((n_total_entries<ev_limits[0]) ||
                (ev_limits[1]>ev_limits[0] && n_total_entries > ev_limits[1])
                ) {
                std::cout << "stopping loop with " << n_total_entries << " "
                << i << " in " << sample_nick << std::endl;
                break;
            }
            
            //zero all branch variables
            t.loop_initialize();
            nbytes += t.tree->GetEntry(i);
        	
			h_top1_mass->Fill(t.gen_t__mass);
			h_top1_mass->Fill(t.gen_tbar__mass);
			h_top2_mass->Fill(t.gen_t2__mass);
			h_top2_mass->Fill(t.gen_tbar2__mass);
			h_top1_pt->Fill(t.gen_t__pt);
			h_top1_pt->Fill(t.gen_tbar__pt);
			h_top2_pt->Fill(t.gen_t2__pt);
			h_top2_pt->Fill(t.gen_tbar2__pt);
			
			h_d_top_mass->Fill(t.gen_t__mass - t.gen_t2__mass);
			h_d_top_mass->Fill(t.gen_tbar__mass - t.gen_tbar2__mass);
			h_d_top_pt->Fill(t.gen_t__pt - t.gen_t2__pt);
			h_d_top_pt->Fill(t.gen_tbar__pt - t.gen_tbar2__pt);

            int nlep = t.n__lep;
            
            float npv = t.n__pv;
            
            for(int nl=0; nl < nlep; nl++) {
                
                float pt = t.lep__pt[nl];
                float eta = t.lep__eta[nl];
                
                float puch_iso = t.lep__puch_iso[nl];
                float p_iso = t.lep__p_iso[nl];
                float hc_iso = t.lep__hc_iso[nl];
                float ch_iso = t.lep__ch_iso[nl];
                float ec_iso = t.lep__ec_iso[nl];
                float ph_iso = t.lep__ph_iso[nl];
                
                int id = t.lep__id[nl];
                float iso = t.lep__rel_iso[nl];
                
                if (pt>20 && std::abs(eta)<2.1) {
                    continue;
                }
                
                h_lep_puch_iso->Fill(puch_iso);
                h_lep_p_iso->Fill(p_iso);
                h_lep_hc_iso->Fill(hc_iso);
                h_lep_ch_iso->Fill(ch_iso);
                h_lep_ec_iso->Fill(ec_iso);
                h_lep_ph_iso->Fill(ph_iso);
				
				h_lep_rel_iso->Fill(iso);
                
                if (std::abs(id) == 13) {
                    h_lep_pt_iso_mu->Fill(pt, iso, 1.0);
                    h_lep_pt_iso_npv_mu->Fill(pt, iso, npv, 1.0);
                    h_lep_pt_iso2_npv_mu->Fill(pt, iso, npv, 1.0);
                } else if (std::abs(id) == 11) {
                    h_lep_pt_iso_ele->Fill(pt, iso, 1.0);
                    h_lep_pt_iso_npv_ele->Fill(pt, iso, npv, 1.0);
                    h_lep_pt_iso2_npv_ele->Fill(pt, iso, npv, 1.0);
                }
            }
        }
        
        std::cout << "read " << nbytes/1024/1024 << " Mb" << std::endl;
        std::cout << "processed " << n_total_entries << " in "
        << tottime << " seconds" << std::endl ;
        tf->Close();
        
    }
    
    for(auto& kv : histmap) {
        const std::string& k = kv.first;
        TH1* h = kv.second;
        h->SetDirectory(outfile);
        cout << "saving " << k << " " << h->Integral() << endl;
    }
    
    outfile->Write();
    outfile->Close();
    
    
}
