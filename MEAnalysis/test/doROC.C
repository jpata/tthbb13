#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TF1.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TString.h"
#include "TLegend.h"
#include "TStyle.h"
#include "TPad.h"
#include "TCut.h"
#include "TLorentzVector.h"

TCut dl = "is_dl";
TCut sl = "is_sl";

TString path = "/shome/bianchi/tth/gc/";

void CanvasAndLegend(TCanvas* c1, TLegend* leg, int logy=0){
  c1->SetGrid(1,1);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);
  c1->SetLogy(logy);
  c1->SetLogx(logy);
  gStyle->SetOptStat(0);
  gStyle->SetTitleFillColor(0);
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetCanvasColor(0);
  gStyle->SetPadBorderMode(0);
  gStyle->SetPadColor(0);
  gStyle->SetTitleFillColor(0);
  gStyle->SetTitleBorderSize(0);
  gStyle->SetTitleH(0.07);
  gStyle->SetTitleFontSize(0.1);
  gStyle->SetTitleStyle(0);
  gStyle->SetTitleOffset(1.3,"y");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.03);
}

TGraphErrors* roc(TString fname="output_sgn.root", float step=0.01, float xMin=0., float xMax=1., TCut cut = "", 
		  int color=2 , TLegend* leg=0, TString leg_name="", TString var = "1./(1. + 0.02*mem_ttbb_p[0]/mem_tth_p[0])"){

  cout << "roc():" << endl;

  TFile* f = TFile::Open( fname , "READ" );
  if(f==0 || f->IsZombie()) return 0;

  TTree* t = (TTree*)f->Get("tree");
  if(t==0) return 0;

  TH1F h("h", "", 100, xMin, xMax);
  t->Draw(var+">>h", cut);

  float OF = h.GetBinContent( h.GetNbinsX() ) +  h.GetBinContent( h.GetNbinsX()+1) ;
  float UF = h.GetBinContent( 1 ) +  h.GetBinContent( 0 ) ;
  h.SetBinContent( h.GetNbinsX(), OF);
  h.SetBinContent( 1, UF );

  int total = h.Integral();
  cout << "\tTot:  " << total << " entries" << endl;
  const int steps = (xMax-xMin)/step;
  double x[steps];
  double y[steps];
  double ex[steps];
  double ey[steps];

  if(total==0) return 0;
  cout << "\tPath: " << string(fname.Data()) << endl;
  cout << "\tCut:  " << string(cut.GetTitle()) <<  endl; 
  cout << "\tFill eff. vs cut....";
  for(int i = 0 ; i < steps ; i++){
    x[i]  = xMin + i*step;
    ex[i] = 0.;
    y[i]  = h.Integral( h.FindBin(x[i]+step/2.), h.GetNbinsX()  )/total;
    ey[i] = sqrt(y[i]*(1-y[i])/total);
  }
  cout << "done!" << endl;

  TGraphErrors* gROC = new TGraphErrors(steps, x, y, ex, ey);

  if(leg!=0){
    gROC->SetLineWidth(3);
    gROC->SetLineColor(color);
    leg->AddEntry(gROC, leg_name, "L" );
  }

  f->Close();

  return gROC;
}


void roc_comp_ROC(TString fname1 = "", TString fname2 = "", TString fname3 = "", TString fname4 = "", 
		  TString var1 = "mem_tth_p[17] /(mem_tth_p[17]  + 0.1*mem_ttbb_p[17])",
		  TString var2 = "mem_tth_p[18] /(mem_tth_p[18]  + 0.1*mem_ttbb_p[18])",
		  TCut cut1="((nMatch_wq_btag==2 && nMatch_tb_btag==2 && ((nMatch_hb_btag==2 && nGenBHiggs==2) || nGenBHiggs<2)) && is_sl && nBCSVM==4 && njets==6 && mem_tth_nperm[17]>0)",
		  TCut cut2="((nMatch_wq_btag==2 && nMatch_tb_btag==2 && ((nMatch_hb_btag==2 && nGenBHiggs==2) || nGenBHiggs<2)) && is_sl && nBCSVM==4 && njets==6 && mem_tth_nperm[18]>0)",
		  TString title = "6 jets",		   
		  TString leg1 = "",  
		  TString leg2 = "",  
		  TString save_name = "tmp.png",
		  float step1=0.05, float xMin1=-0.01, float xMax1=1.01, 
		  float step2=0.05, float xMin2=-0.01, float xMax2=1.01, 
		  float xLow = 0., float yLow = 1, int doLog=0
                   ){

  TCanvas *c1  = new TCanvas("c1","",5,30,650,600);
  TLegend* leg = new TLegend(0.12,0.72,0.47,0.89,NULL,"brNDC");
  CanvasAndLegend(c1, leg, doLog);

  TH1F* hROC = new TH1F("hROC", title+"; #epsilon ttH; #epsilon tt+jets ", 100, doLog ? xLow : 0., 1.0);
  hROC->SetMinimum(doLog ? yLow : 0.);
  hROC->SetMaximum(1.0);

  cout << "Doing ROC 1...." << endl;
  TGraphErrors* gROC1 = roc(fname1, step1, xMin1, xMax1, cut1, 2, leg, leg1, var1);
  TGraphErrors* gROC2 = roc(fname2, step1, xMin1, xMax1, cut1, 2, 0,   leg1, var1);

  cout << "Doing ROC 2...." << endl;
  TGraphErrors* gROC1cut = roc(fname3, step2, xMin2, xMax2, cut2, 3, leg, leg2, var2);
  TGraphErrors* gROC2cut = roc(fname4, step2, xMin2, xMax2, cut2, 3, 0,   leg2, var2);

  if(gROC1==0 || gROC2==0) return;

  TGraphErrors* gROC = new TGraphErrors( gROC1->GetN() , gROC1->GetY(), gROC2->GetY(), gROC1->GetEY(), gROC2->GetEY());
  gROC->SetLineWidth(3);
  gROC->SetLineColor(2);

  TGraphErrors* gROCcut = new TGraphErrors( gROC1cut->GetN() , gROC1cut->GetY(), gROC2cut->GetY(), gROC1cut->GetEY(), gROC2cut->GetEY());
  gROCcut->SetLineWidth(3);
  gROCcut->SetLineColor(3);

  hROC->Draw();
  gROC->Draw("LSAME");
  gROCcut->Draw("LSAME");

  TF1* diag = new TF1("diag", "x", 0.,1.);
  diag->SetLineColor(kBlack);
  diag->SetLineStyle(kDashed);
  diag->Draw("SAME");

  leg->Draw();

  //return;
  c1->SaveAs( save_name );

  TFile* out = TFile::Open(save_name+".root", "RECREATE");
  out->cd();
  c1->Write();
  gROC1->Write("cut_vs_eff_S_0");
  gROC2->Write("cut_vs_eff_B_0");
  gROC1cut->Write("cut_vs_eff_S_1");
  gROC2cut->Write("cut_vs_eff_B_1");
  out->Write();
  out->Close();

  delete c1; delete leg; delete diag;
}

void roc_opt_ROC(TString fname1 = "", TString fname2 = "", 
		 int pos = 0,
		 TCut cut="is_sl && nBCSVM>=4 && njets>=6",
		 TString title = "6 jets",		   
		 TString save_name = "tmp.png",
		 float step=0.05, float xMin=-0.01, float xMax=2.01
		 ){

  TCanvas *c1  = new TCanvas("c1","",5,30,650,600);
  TLegend* leg = new TLegend(0.12,0.72,0.47,0.89,NULL,"brNDC");
  CanvasAndLegend(c1, leg, 0);


  const unsigned int n_k = 4; 
  const unsigned int n_a = 6; 
  const float step_k = 0.1;
  const float step_a = 0.2;

  float k_factor[n_k];
  float a_factor[n_a];
  for( unsigned int k = 0 ; k < n_k; ++k ){
    k_factor[k] = 0.05 + step_k*k;
  }
  for( unsigned int a = 0 ; a < n_a; ++a ){
    a_factor[a] = 0.0 + step_a*a;
  }

  //TGraphErrors* gROC = 0;

  TH2F* hROC = new TH2F("hROC", title+"; K; A", n_k, k_factor[0]-step_k/2., k_factor[n_k-1]+step_k/2., n_a, a_factor[0]-step_a/2., a_factor[n_a-1]+step_a/2.);

  for(unsigned int k = 0 ; k < n_k; ++k){
    float K = k_factor[k];
    for(unsigned int a = 0 ; a < n_a; ++a){
      float A = a_factor[a];

      cout << "Processing k=" << K << ", a=" << A << endl;
      TString var1(Form("%f*(mem_tth_p[%d] /(mem_tth_p[%d]  + %f*mem_ttbb_p[%d]))",A,pos,pos,K,pos));
      TString var2(Form("(1-%f)*btag_LR_4b_2b",A));
      TString var = var1+"+"+var2;

      cout << "Doing ROC for variable " << string(var.Data()) << endl;
      TGraphErrors* gROC1 = roc(fname1, step, xMin, xMax, cut, 2, 0,   Form("k=%f,a=%f",K,A), var);
      TGraphErrors* gROC2 = roc(fname2, step, xMin, xMax, cut, 2, 0,   Form("k=%f,a=%f",K,A), var);
      if(gROC1==0 || gROC2==0) return;
      
      TGraphErrors* gROCtmp = new TGraphErrors( gROC1->GetN() , gROC1->GetY(), gROC2->GetY(), gROC1->GetEY(), gROC2->GetEY());
      gROCtmp->SetLineWidth(3);
      gROCtmp->SetLineColor(2);
      double inttmp = gROCtmp->Integral(); 
      cout << "Integral = " << inttmp << " filled in bin " << hROC->FindBin(K,A) << endl;
      hROC->SetBinContent(hROC->FindBin(K,A), 0.5-inttmp);
      //delete gROC1;
      //delete gROC2;
      //delete gROCtmp;
      cout << "...Done" << endl;
    }
  }

  cout << "Print 2D histo..." << endl;
  hROC->Draw("COLZ");
  leg->Draw();

  cout << "Save png..." << endl;
  c1->SaveAs( save_name );

  cout << "Open ROOT file..." << endl;
  TFile* out = TFile::Open(save_name+".root", "RECREATE");
  out->cd();
  c1->Write();
  hROC->Write();
  cout << "Write ROOT file..." << endl;
  out->Write();
  cout << "Close ROOT file..." << endl;
  out->Close();

  cout << "Delete and return..." << endl;
  delete c1; delete leg;
}

////////////////////////////////////////////////////////////////////
void run_DL_opt( TString gcS1 = "GC3de9cd7caec1", TString gcB1 = "GCa5f687e57337"
		 ){

  TString fS1 = path+gcS1+"/tth_13tev/output-sig.root";
  TString fB1 = path+gcB1+"/ttjets_13tev_madgraph_pu20bx25_phys14/output-bkg.root";
  
  roc_opt_ROC( fS1, fB1,
	       0,
	       dl && TCut("njets>=4 && nBCSVM==2"),
	       "DL, N_{b}==2, N_{j}#geq4",
	       "OPT_DL_g4_2.png"                                               
	       );
  
  roc_opt_ROC( fS1, fB1,
	       0,
	       dl && TCut("njets>=4 && nBCSVM==3"),
	       "DL, N_{b}==3, N_{j}#geq4",
	       "OPT_DL_g4_3.png"                                               
	       );

}

////////////////////////////////////////////////////////////////////
void run_test( TString gcS1 = "", TString gcB1 = "", 
	       TString gcS2 = "", TString gcB2 = ""
	       ){

  TString fS1 = path+gcS1+"/tth_13tev/output-sig.root";
  TString fB1 = path+gcB1+"/ttjets_13tev_madgraph_pu20bx25_phys14/output-bkg.root";
  TString fS2 = path+gcS2+"/tth_13tev/output-sig.root";
  TString fB2 = path+gcB2+"/ttjets_13tev_madgraph_pu20bx25_phys14/output-bkg.root";

  roc_comp_ROC( fS1, fB1, fS2, fB2,                                                // fS*/fB* for *th ROC  
		"mem_tth_p[0] / (mem_tth_p[0]  + 0.1*mem_ttbb_p[0])",              // Var for 1st ROC
		"mem_tth_p[1] / (mem_tth_p[1]  + 0.1*mem_ttbb_p[1])",              // Var for 2nd ROC
		sl && TCut("njets>=6 && nBCSVM>=4") && TCut("mem_tth_nperm[0]>0"), // Cut for 1st ROC
		sl && TCut("njets>=6 && nBCSVM>=4") && TCut("mem_tth_nperm[0]>0"), // Cur for 2nd ROC
		"",                                                                // Title
		"0w",                                                              // Legend for 1st ROC
		"0w",                                                              // Legend for 2nd ROC
		"TEST.png"                                                         // png name
		);
  return;
}
////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////
void run_DL( TString gcS1 = "GC3de9cd7caec1", TString gcB1 = "GCa5f687e57337", 
	     TString gcS2 = "GC3de9cd7caec1", TString gcB2 = "GCa5f687e57337"
	     ){

  TString fS1 = path+gcS1+"/tth_13tev/output-sig.root";
  TString fB1 = path+gcB1+"/ttjets_13tev_madgraph_pu20bx25_phys14/output-bkg.root";
  TString fS2 = path+gcS2+"/tth_13tev/output-sig.root";
  TString fB2 = path+gcB2+"/ttjets_13tev_madgraph_pu20bx25_phys14/output-bkg.root";

  roc_comp_ROC( fS1, fB1, fS2, fB2,                                        
		"mem_tth_p[0] / (mem_tth_p[0]  + 0.1*mem_ttbb_p[0])",      
		"btag_LR_4b_2b",
		dl && TCut("njets>=4 && nBCSVM==2"),
		dl && TCut("njets>=4 && nBCSVM==2"),
		"DL, N_{b}==2, N_{j}#geq4",
		"DL, MEM",                                                 
		"DL, LR",                                                  
		"ROC_DL_g4_2_btag-mem.png"                                               
		);

  roc_comp_ROC( fS1, fB1, fS2, fB2,                                        
		"mem_tth_p[0] / (mem_tth_p[0]  + 0.1*mem_ttbb_p[0])",      
		"btag_LR_4b_2b",
		dl && TCut("njets>=4 && nBCSVM==3"),
		dl && TCut("njets>=4 && nBCSVM==3"),
		"DL, N_{b}==3, N_{j}#geq4",
		"DL, MEM",                                                 
		"DL, LR",                                                  
		"ROC_DL_g4_3_btag-mem.png"                                               
		);

  roc_comp_ROC( fS1, fB1, fS2, fB2,                                        
		"mem_tth_p[0] / (mem_tth_p[0]  + 0.1*mem_ttbb_p[0])",      
		"btag_LR_4b_2b",
		dl && TCut("njets>=4 && nBCSVM>=4"),
		dl && TCut("njets>=4 && nBCSVM>=4"),
		"DL, N_{b}#geq4, N_{j}#geq4",
		"DL, MEM",                                                 
		"DL, LR",                                                  
		"ROC_DL_g4_g4_btag-mem.png"                                               
		);

  roc_comp_ROC( fS1, fB1, fS2, fB2,                                        
		"mem_tth_p[0] / (mem_tth_p[0]  + 0.1*mem_ttbb_p[0])",      
		"btag_LR_4b_2b",
		dl && TCut("njets>=4 && nBCSVM>=2"),
		dl && TCut("njets>=4 && nBCSVM>=2"),
		"DL, N_{b}#geq2, N_{j}#geq4",
		"DL, MEM",                                                 
		"DL, LR",                                                  
		"ROC_DL_g4_g2_btag-mem.png"                                               
		);
  return;
}
////////////////////////////////////////////////////////////////////


void run_all(){

  //run_test();
  run_DL();

}
