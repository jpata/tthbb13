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

#define PRINT 1

TCut dl = "is_dl";
TCut sl = "is_sl";

//TString path = "/shome/bianchi/tth/gc/";
//TString path = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/Jun17_sync722_98a561/";
TString path     = "/scratch/bianchi/new";
TString save_dir = "./root/new/";

const int NBIN = 1000;

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
		  int color=2 , TLegend* leg=0, TString leg_name="", TString var = "1./(1. + 0.02*mem_ttbb_p[0]/mem_tth_p[0])", TH1F* histo=0){

  if(PRINT) cout << "roc():" << endl;

  TFile* f = TFile::Open( fname , "READ" );
  if(f==0 || f->IsZombie()) return 0;

  TTree* t = (TTree*)f->Get("tree");
  if(t==0) return 0;

  TH1F h("h", "", NBIN, xMin, xMax);
  //t->Draw(var+">>h", cut*"TMath::Abs(genWeight)/genWeight");
  t->Draw(var+">>h", cut);

  if(histo){
    histo->Add(&h);
    histo->Rebin(100);
    histo->Scale(1./histo->Integral());
  }

  float OF = h.GetBinContent( h.GetNbinsX() ) +  h.GetBinContent( h.GetNbinsX()+1) ;
  float UF = h.GetBinContent( 1 ) +  h.GetBinContent( 0 ) ;
  h.SetBinContent( h.GetNbinsX(), OF);
  h.SetBinContent( 1, UF );

  int total = h.Integral();
  if(PRINT) cout << "\tTot:  " << total << " entries" << endl;
  const int steps = (xMax-xMin)/step;
  double x[steps];
  double y[steps];
  double ex[steps];
  double ey[steps];

  if(total==0) return 0;
  if(PRINT) cout << "\tPath: " << string(fname.Data()) << endl;
  if(PRINT) cout << "\tCut:  " << string(cut.GetTitle()) <<  endl; 
  if(PRINT) cout << "\tFill eff. vs cut....";
  for(int i = 0 ; i < steps ; i++){
    x[i]  = xMin + i*step;
    ex[i] = 0.;
    y[i]  = h.Integral( h.FindBin(x[i]+step/2.), h.GetNbinsX()  )/total;
    ey[i] = sqrt(y[i]*(1-y[i])/total);
  }
  if(PRINT) cout << "done!" << endl;

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

  TH1F* hROC = new TH1F("hROC", "CMS Simulation $sqrt{s}=13 TeV; #epsilon ttH; #epsilon tt+jets ", 100, doLog ? xLow : 0., 1.0);
  hROC->SetMinimum(doLog ? yLow : 0.);
  hROC->SetMaximum(1.0);

  if(PRINT) cout << "Doing ROC 1...." << endl;
  TH1F* hROC1 = new TH1F("hROC1", "", NBIN, xMin1, xMax1); hROC1->Sumw2(); hROC1->SetLineWidth(3); hROC1->SetLineColor(kRed);
  TH1F* hROC2 = new TH1F("hROC2", "", NBIN, xMin1, xMax1); hROC2->Sumw2(); hROC2->SetLineWidth(3); hROC2->SetLineColor(kBlue);
  TGraphErrors* gROC1 = roc(fname1, step1, xMin1, xMax1, cut1, 2, leg, leg1, var1, hROC1);
  TGraphErrors* gROC2 = roc(fname2, step1, xMin1, xMax1, cut1, 2, 0,   leg1, var1, hROC2);

  if(PRINT) cout << "Doing ROC 2...." << endl;
  TH1F* hROC1cut = new TH1F("hROC1cut", "", NBIN, xMin1, xMax1); hROC1cut->Sumw2(); hROC1cut->SetLineWidth(3); hROC1cut->SetLineColor(kRed);
  TH1F* hROC2cut = new TH1F("hROC2cut", "", NBIN, xMin1, xMax1); hROC2cut->Sumw2(); hROC2cut->SetLineWidth(3); hROC2cut->SetLineColor(kBlue);
  TGraphErrors* gROC1cut = roc(fname3, step2, xMin2, xMax2, cut2, 3, leg, leg2, var2, hROC1cut);
  TGraphErrors* gROC2cut = roc(fname4, step2, xMin2, xMax2, cut2, 3, 0,   leg2, var2, hROC2cut);

  if(gROC1==0 || gROC2==0){
    if(PRINT) cout << "!!!! roc_comp_ROC returned unexpectedly !!!!" << endl;
    return;
  }

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

  leg->SetHeader(title);
  leg->Draw();

  //return;
  c1->SetName(save_name);
  c1->SaveAs( save_dir+"/"+save_name+".png" );

  TFile* out = TFile::Open(save_dir+"/"+save_name+".root", "RECREATE");
  out->cd();
  c1->Write();
  gROC1->Write("cut_vs_eff_S_0");
  gROC2->Write("cut_vs_eff_B_0");
  gROC1cut->Write("cut_vs_eff_S_1");
  gROC2cut->Write("cut_vs_eff_B_1");
  hROC1->Write("S_0");
  hROC2->Write("B_0");
  hROC1cut->Write("S_1");
  hROC2cut->Write("B_1");
  out->Write();
  out->Close();

  delete c1; delete leg; delete diag;
  delete hROC1; delete hROC2;
  delete hROC1cut; delete hROC2cut;
}

void roc_comp3_ROC(TString fname1 = "", TString fname2 = "", TString fname3 = "", TString fname4 = "", TString fname5 = "", TString fname6 = "", 
		   TString var1 = "mem_tth_p[17] /(mem_tth_p[17]  + 0.1*mem_ttbb_p[17])",
		   TString var2 = "mem_tth_p[18] /(mem_tth_p[18]  + 0.1*mem_ttbb_p[18])",
		   TString var3 = "mem_tth_p[18] /(mem_tth_p[18]  + 0.1*mem_ttbb_p[18])",
		   TCut cut1="((nMatch_wq_btag==2 && nMatch_tb_btag==2 && ((nMatch_hb_btag==2 && nGenBHiggs==2) || nGenBHiggs<2)) && is_sl && nBCSVM==4 && njets==6 && mem_tth_nperm[17]>0)",
		   TCut cut2="((nMatch_wq_btag==2 && nMatch_tb_btag==2 && ((nMatch_hb_btag==2 && nGenBHiggs==2) || nGenBHiggs<2)) && is_sl && nBCSVM==4 && njets==6 && mem_tth_nperm[18]>0)",
		   TCut cut3="((nMatch_wq_btag==2 && nMatch_tb_btag==2 && ((nMatch_hb_btag==2 && nGenBHiggs==2) || nGenBHiggs<2)) && is_sl && nBCSVM==4 && njets==6 && mem_tth_nperm[18]>0)",
		   TString title = "6 jets",		   
		   TString leg1 = "",  
		   TString leg2 = "",  
		   TString leg3 = "",  
		   TString save_name = "tmp.png",
		   int toplot = 2,
		   float step1=0.05, float xMin1=-0.01, float xMax1=1.01, 
		   float step2=0.05, float xMin2=-0.01, float xMax2=1.01, 
		   float step3=0.05, float xMin3=-0.01, float xMax3=1.01, 
		   float xLow = 0., float yLow = 1, int doLog=0
                   ){

  TCanvas *c1   = new TCanvas("c1","",5,30,650,600);
  TCanvas *c2   = new TCanvas("c2","",5,30,650,600);
  TLegend* leg  = new TLegend(0.12,0.72,0.47,0.89,NULL,"brNDC");
  TLegend* legC = new TLegend(0.12,0.72,0.47,0.89,NULL,"brNDC");
  CanvasAndLegend(c1, leg,  doLog);
  CanvasAndLegend(c2, legC, doLog);

  c1->cd();
  TH1F* hROC = new TH1F("hROC", "CMS Simulation #sqrt{s}=13 TeV; #epsilon ttH; #epsilon tt+jets ", 100, doLog ? xLow : 0., 1.0);
  hROC->SetMinimum(doLog ? yLow : 0.);
  hROC->SetMaximum(1.0);

  if(PRINT) cout << "Doing ROC 1...." << endl;
  TH1F* hROC1 = new TH1F("hROC1", "", NBIN, xMin1, xMax1); hROC1->Sumw2(); hROC1->SetLineWidth(3); hROC1->SetLineColor(kRed);
  TH1F* hROC2 = new TH1F("hROC2", "", NBIN, xMin1, xMax1); hROC2->Sumw2(); hROC2->SetLineWidth(3); hROC2->SetLineColor(kBlue);
  TGraphErrors* gROC1 = roc(fname1, step1, xMin1, xMax1, cut1, 2, leg, leg1, var1, hROC1);
  TGraphErrors* gROC2 = roc(fname2, step1, xMin1, xMax1, cut1, 2, 0,   leg1, var1, hROC2);

  if(PRINT) cout << "Doing ROC 2...." << endl;
  TH1F* hROC1cut = new TH1F("hROC1cut", "", NBIN, xMin1, xMax1); hROC1cut->Sumw2(); hROC1cut->SetLineWidth(3); hROC1cut->SetLineColor(kRed);
  TH1F* hROC2cut = new TH1F("hROC2cut", "", NBIN, xMin1, xMax1); hROC2cut->Sumw2(); hROC2cut->SetLineWidth(3); hROC2cut->SetLineColor(kBlue);
  TGraphErrors* gROC1cut = roc(fname3, step2, xMin2, xMax2, cut2, 3, leg, leg2, var2, hROC1cut);
  TGraphErrors* gROC2cut = roc(fname4, step2, xMin2, xMax2, cut2, 3, 0,   leg2, var2, hROC2cut);

  if(PRINT) cout << "Doing ROC 3...." << endl;
  TH1F* hROC1cut2 = new TH1F("hROC1cut2", "", NBIN, xMin1, xMax1); hROC1cut2->Sumw2(); hROC1cut2->SetLineWidth(3); hROC1cut2->SetLineColor(kRed);
  TH1F* hROC2cut2 = new TH1F("hROC2cut2", "", NBIN, xMin1, xMax1); hROC2cut2->Sumw2(); hROC2cut2->SetLineWidth(3); hROC2cut2->SetLineColor(kBlue);
  TGraphErrors* gROC1cut2 = roc(fname5, step3, xMin3, xMax3, cut3, 4, leg, leg3, var3, hROC1cut2);
  TGraphErrors* gROC2cut2 = roc(fname6, step3, xMin3, xMax3, cut3, 4, 0,   leg3, var3, hROC2cut2);

  if(gROC1==0 || gROC2==0 || gROC1cut==0 || gROC1cut==0 || gROC1cut2==0 || gROC2cut2==0){
    if(PRINT) cout << "!!!! roc_comp_ROC returned unexpectedly !!!!" << endl;
    return;
  }

  TGraphErrors* gROC = new TGraphErrors( gROC1->GetN() , gROC1->GetY(), gROC2->GetY(), gROC1->GetEY(), gROC2->GetEY());
  gROC->SetLineWidth(3);
  gROC->SetLineColor(2);

  TGraphErrors* gROCcut = new TGraphErrors( gROC1cut->GetN() , gROC1cut->GetY(), gROC2cut->GetY(), gROC1cut->GetEY(), gROC2cut->GetEY());
  gROCcut->SetLineWidth(3);
  gROCcut->SetLineColor(3);

  TGraphErrors* gROCcut2 = new TGraphErrors( gROC1cut2->GetN() , gROC1cut2->GetY(), gROC2cut2->GetY(), gROC1cut2->GetEY(), gROC2cut2->GetEY());
  gROCcut2->SetLineWidth(3);
  gROCcut2->SetLineColor(4);

  hROC->Draw();
  gROC->Draw("LSAME");
  gROCcut->Draw("LSAME");
  gROCcut2->Draw("LSAME");

  cout << "<" << string(leg1.Data()) << ">: bkg eff. at (0.5, 0.2, 0.1) = " << endl; 
  cout << "\t(" << gROC->Eval(0.5) << ", " << gROC->Eval(0.2) << "," << gROC->Eval(0.1) << ")" 
       << endl; 
  cout << "<" << string(leg2.Data()) << ">: bkg eff. at (0.5, 0.2, 0.1) = " << endl; 
  cout << "\t(" << gROCcut->Eval(0.5) << ", " << gROCcut->Eval(0.2) << "," << gROCcut->Eval(0.1) << ")" 
       << endl; 
  cout << "<" << string(leg3.Data()) << ">: bkg eff. at (0.5, 0.2, 0.1) = " << endl;
  cout << "\t(" << gROCcut2->Eval(0.5) << ", " << gROCcut2->Eval(0.2) << "," << gROCcut2->Eval(0.1) << ")" 
       << endl; 

  TF1* diag = new TF1("diag", "x", 0.,1.);
  diag->SetLineColor(kBlack);
  diag->SetLineStyle(kDashed);
  diag->Draw("SAME");

  leg->Draw();
  leg->SetHeader(title);

  //return;
  c1->SetName(save_name+"_roc");
  c1->SaveAs( save_dir+"/"+save_name+"_roc.png" );

  c2->cd();
  TH1F* h_sgn = 0;
  TH1F* h_bkg = 0;
  TString discrname = "";
  if(toplot==0){
    h_sgn = hROC1;
    h_bkg = hROC2;
    discrname = leg1;
  }
  else if(toplot==1){
    h_sgn = hROC1cut;
    h_bkg = hROC2cut;
    discrname = leg2;
  }
  else{
    h_sgn = hROC1cut2;
    h_bkg = hROC2cut2;
    discrname = leg3;
  }

  h_sgn->SetTitle("CMS Simulation #sqrt{s}=13 TeV");
  h_sgn->SetXTitle(discrname);
  h_sgn->SetYTitle("normalised to one");
  h_sgn->SetMaximum(0.6);
  h_sgn->SetMinimum(0.0);
  h_sgn->Draw("HISTE");
  h_bkg->Draw("HISTESAME");
  legC->AddEntry(h_sgn,"t#bar{t}H",    "L");
  legC->AddEntry(h_bkg,"t#bar{t}+jets","L");
  legC->SetHeader(title);
  legC->Draw();
  c2->SetName(save_name+"_discr");
  c2->SaveAs( save_dir+"/"+save_name+"_discr.png" );


  TFile* out = TFile::Open(save_dir+"/"+save_name+".root", "RECREATE");
  out->cd();
  c1->Write();
  c2->Write();
  gROC1->Write("cut_vs_eff_S_0");
  gROC2->Write("cut_vs_eff_B_0");
  gROC1cut->Write("cut_vs_eff_S_1");
  gROC2cut->Write("cut_vs_eff_B_1");
  gROC1cut2->Write("cut_vs_eff_S_2");
  gROC2cut2->Write("cut_vs_eff_B_2");
  hROC1->Write("S_0");
  hROC2->Write("B_0");
  hROC1cut->Write("S_1");
  hROC2cut->Write("B_1");
  hROC1cut2->Write("S_2");
  hROC2cut2->Write("B_2");
  out->Write();
  out->Close();

  delete c1; delete leg; delete diag;
  delete hROC1; delete hROC2;
  delete hROC1cut; delete hROC2cut;
  delete hROC1cut2; delete hROC2cut2;
}


void roc_opt_ROC(TString fname1 = "", TString fname2 = "", 
		 int pos = 0,
		 TCut cut="is_sl && nBCSVM>=4 && njets>=6",
		 TString title = "6 jets",		   
		 TString save_name = "tmp.png",
		 int fom = 0,
		 float step=0.01, float xMin=-0.01, float xMax=2.01
		 ){

  TCanvas *c1  = new TCanvas("c1","",5,30,650,600);
  TLegend* leg = new TLegend(0.12,0.72,0.47,0.89,NULL,"brNDC");
  CanvasAndLegend(c1, leg, 0);


  const unsigned int n_k = 1; 
  const float step_k     = 0.05;

  /*
  const unsigned int n_a = 15;
  const float step_a     = 150;
  */
  const unsigned int n_a = 12;
  const float step_a     = 10;

  float k_factor[n_k];
  float a_factor[n_a];
  for( unsigned int k = 0 ; k < n_k; ++k ){
    k_factor[k] = 0.15 + step_k*k;
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

      if(PRINT) cout << "Processing k=" << K << ", a=" << A << "..." << endl;
      /*
      TString var1(Form("%f*(mem_tth_p[%d] /(mem_tth_p[%d]  + %f*mem_ttbb_p[%d]))",A,pos,pos,K,pos));
      TString var2(Form("(1-%f)*btag_LR_4b_2b",A));
      */        
      TString var1("");
      /*
      if( a<(n_a - 1) ) 
	var1 = TString(Form("(mem_tth_p[%d] /(mem_tth_p[%d]  + %f*mem_ttbb_p[%d]*(1+%f*btag_lr_2b_alt/btag_lr_4b_alt)))",pos,pos,K,pos,A));
      else{ 
	TString log("(-log(1./(btag_lr_4b_alt/(btag_lr_4b_alt+btag_lr_2b_alt))-1))");
	var1 = "("+log+")/15.";
      }
      */
      if( a<(n_a - 1) ) 
	var1 = TString(Form("(mem_tth_p[%d] /(mem_tth_p[%d]  + %f*mem_ttbb_p[%d]*(1+%f*mem_tth_btag_weight_jj[%d]/mem_tth_btag_weight_bb[%d])))",pos,pos,K,pos,A,pos,pos));
      else{ 
	TString log(Form("-log(1./(mem_tth_btag_weight_bb[%d]/(mem_tth_btag_weight_bb[%d]+mem_tth_btag_weight_jj[%d]))-1)",pos,pos,pos));
	//var1 = TString(Form("mem_tth_btag_weight_bb[%d]/(mem_tth_btag_weight_bb[%d]+mem_tth_btag_weight_jj[%d])",pos,pos,pos));
	var1 =  "("+log+")/15.";
      }

      TString var2("0");
      TString var = var1+"+"+var2;

      if(PRINT) cout << "Doing ROC for variable " << string(var.Data()) << endl;
      TGraphErrors* gROC1 = roc(fname1, step, xMin, xMax, cut, 2, 0,   Form("k=%f,a=%f",K,A), var);
      TGraphErrors* gROC2 = roc(fname2, step, xMin, xMax, cut, 2, 0,   Form("k=%f,a=%f",K,A), var);
      if(gROC1==0 || gROC2==0) return;
      
      TGraphErrors* gROCtmp = new TGraphErrors( gROC1->GetN() , gROC1->GetY(), gROC2->GetY(), gROC1->GetEY(), gROC2->GetEY());
      gROCtmp->SetLineWidth(3);
      gROCtmp->SetLineColor(2);
      double inttmp = 0.;      
      if(fom==0){
	double max_x = (gROCtmp->GetX())[0];
	double max_y = (gROCtmp->GetY())[0];
	double min_x = (gROCtmp->GetX())[gROCtmp->GetN()-1];
	double min_y = (gROCtmp->GetY())[gROCtmp->GetN()-1];
	inttmp = (max_x-min_x)*(max_y-min_y)/2. - gROCtmp->Integral(); 
      }
      if(fom==1) inttmp = gROCtmp->Eval(0.5); 
      if(fom==2) inttmp = gROCtmp->Eval(0.2); 
      if(fom==3) inttmp = gROCtmp->Eval(0.1); 
      if(PRINT) cout << "Integral = " << inttmp << " (fom: " << fom << ") filled in bin " << hROC->FindBin(K,A) << endl;      
      hROC->SetBinContent(hROC->FindBin(K,A), inttmp);
      //delete gROC1;
      //delete gROC2;
      //delete gROCtmp;
      if(PRINT) cout << "Done..." << endl;
    }
  }

  if(PRINT) cout << "Print 2D histo..." << endl;
  hROC->Draw("COLZ");
  leg->Draw();

  if(1) cout << "Save png..." << endl;
  c1->SaveAs( save_dir+"/"+save_name+".png" );

  if(PRINT) cout << "Open ROOT file..." << endl;
  TFile* out = TFile::Open(save_dir+"/"+save_name+".root", "RECREATE");
  out->cd();
  c1->Write();
  hROC->Write();
  if(PRINT) cout << "Write ROOT file..." << endl;
  out->Write();
  if(PRINT) cout << "Close ROOT file..." << endl;
  out->Close();

  if(PRINT) cout << "Delete and return..." << endl;
  delete c1; delete leg;
}

////////////////////////////////////////////////////////////////////
void run_DL_opt( TString gcS1 = "", TString gcB1 = ""
		 ){
  
  //TString fS1 = path+gcS1+"/tth_13tev_amcatnlo_pu20bx25.root";
  //TString fB1 = path+gcB1+"/ttjets_13tev_madgraph_pu20bx25_phys14.root";
  
  TString fS1 = "/shome/bianchi/tth/gc/GCf0e72192040b/MEAnalysis_cfg_heppy/tth_13tev_amcatnlo_pu20bx25/output-DL.root";
  TString fB1 = "/shome/bianchi/tth/gc/GC56e39869b161/MEAnalysis_cfg_heppy/ttjets_13tev_madgraph_pu20bx25_phys14/output-bkg_tmp.root";

  string name = "";
  for( int f = 1 ; f < 2; ++f){  
    
    if(f==0) name = "AUC";
    if(f==1) name = "#epsilon_{B} at #epsilon_{S}=0.5";
    if(f==2) name = "#epsilon_{B} at #epsilon_{S}=0.2";
    
    roc_opt_ROC( fS1, fB1,
		 1,
		 dl && TCut("njets>=4 && nBCSVM==3"),
		 Form("DL, N_{b}==3, N_{j}#geq4, %s", name.c_str()),
		 Form("OPT_DL_g4_3_FOM%d",f), f                                               
		 );

    roc_opt_ROC( fS1, fB1,
		 1,
		 dl && TCut("njets>=4 && nBCSVM>=4"),
		 Form("DL, N_{b}#geq4, N_{j}#geq4, %s",name.c_str()),
		 Form("OPT_DL_g4_g4_FOM%d",f), f                                               
		 );
  }

}



////////////////////////////////////////////////////////////////////

void run_SL_opt( //TString gcS1 = "GCdd371ba1cc90", TString gcB1 = "GC399bef150c46"
		TString gcS1 = "", TString gcB1 = ""
		 ){

  TString fS1 = path+gcS1+"/tth_13tev_amcatnlo_pu20bx25.root";
  TString fB1 = path+gcB1+"/ttjets_13tev_madgraph_pu20bx25_phys14.root";


  if(PRINT) cout << "################## >=4 tags" << endl;

  string name = "";
  for( int f = 3 ; f < 2; ++f){  
    
    if(f==0) name = "AUC";
    if(f==1) name = "#epsilon_{B} at #epsilon_{S}=0.5";
    if(f==2) name = "#epsilon_{B} at #epsilon_{S}=0.2";

    roc_opt_ROC( fS1, fB1,
		 0,
		 sl && TCut("njets>=7 && nBCSVM>=4"),
		 Form("SL, N_{b}#geq4, N_{j}#geq7, %s", name.c_str()),
		 Form("OPT_SL_g7_g4_FOM%d",f), f
		 );

    roc_opt_ROC( fS1, fB1,
		 0,
		 sl && TCut("njets==6 && nBCSVM>=4"),
		 Form("SL, N_{b}#geq4, N_{j}=6, %s", name.c_str()),
		 Form("OPT_SL_6_g4_FOM%d",f), f
		 );
    
    roc_opt_ROC( fS1, fB1,
		 0,
		 sl && TCut("njets==6 && nBCSVM>=4 && (Wmass>60 && Wmass<100)"),
		 Form("SL, N_{b}#geq4, N_{j}=6, W-tag, %s", name.c_str()),
		 Form("OPT_SL_6_g4_wtag_FOM%d",f), f    
		 );
    
    roc_opt_ROC( fS1, fB1,
		 0,
		 sl && TCut("njets==5 && nBCSVM>=4"),
		 Form("SL, N_{b}#geq4, N_{j}=5, %s", name.c_str()),
		 Form("OPT_SL_5_g4_FOM%d",f), f
		 );

    roc_opt_ROC( fS1, fB1,
		 0,
		 sl && TCut("njets==4 && nBCSVM>=4"),
		 Form("SL, N_{b}#geq4, N_{j}=4, %s", name.c_str()),
		 Form("OPT_SL_4_g4_FOM%d",f), f
		 );
    
  }
  
  if(PRINT) cout << "################## =3 tags" << endl;

  for( int f = 2 ; f < 3; ++f){  
    
    if(f==0) name = "AUC";
    if(f==1) name = "#epsilon_{B} at #epsilon_{S}=0.5";
    if(f==2) name = "#epsilon_{B} at #epsilon_{S}=0.2";
        
    roc_opt_ROC( fS1, fB1,
		 0,
		 sl && TCut("njets==5 && nBCSVM==3"),
		 Form("SL, N_{b}=3, N_{j}=5, %s",  name.c_str()),
		 Form("OPT_SL_5_3_FOM%d",f), f                                               
		 );
    
    roc_opt_ROC( fS1, fB1,
		 0,
		 sl && TCut("njets>=6 && nBCSVM==3"),
		 Form("SL, N_{b}=3, N_{j}#geq6, %s", name.c_str()),
		 Form("OPT_SL_g6_3_FOM%d",f), f
		 );
  }
  
  return;
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
		"TEST"                                                         // png name
		);
  return;
}
////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////
void run_ROC_SL( TString gcS1 = "", TString gcB1 = "", 
		 TString gcS2 = "", TString gcB2 = ""
		 ){
  
  TString fS1 = path+gcS1+"/tth_13tev_amcatnlo_pu20bx25.root";
  TString fB1 = path+gcB1+"/ttjets_13tev_madgraph_pu20bx25_phys14.root";

  bool do6jets = false;
  bool do5jets = true;
  bool do4jets = true;
  bool do3tags = false;
  bool do2tags = false;

  if( do6jets ){
  roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		 "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		 "-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)/15.",
		 "(mem_tth_p[0] /(mem_tth_p[0]  + 0.03*mem_ttbb_p[0]*(1+60.*mem_tth_btag_weight_jj[0]/mem_tth_btag_weight_bb[0])))",
		 sl && TCut("njets>=7 && nBCSVM>=4"),
		 sl && TCut("njets>=7 && nBCSVM>=4"),
		 sl && TCut("njets>=7 && nBCSVM>=4"),
		 "SL channel,  N_{b}#geq4, N_{j}#geq7", 		
		 "ME discr.",
		 "B-tag discr.",
		 "Combined discr.",
		 "SL_g7_g4"
		 );

  roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		 "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		 "-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)/15.",
		 "(mem_tth_p[0] /(mem_tth_p[0]  + 0.03*mem_ttbb_p[0]*(1+30.*mem_tth_btag_weight_jj[0]/mem_tth_btag_weight_bb[0])))",
		 sl && TCut("njets==6 && nBCSVM>=4 && !(Wmass>60 && Wmass<100)"),
		 sl && TCut("njets==6 && nBCSVM>=4 && !(Wmass>60 && Wmass<100)"),
		 sl && TCut("njets==6 && nBCSVM>=4 && !(Wmass>60 && Wmass<100)"),
		 "SL channel,  N_{b}#geq4, N_{j}=6, !W-tag", 		
		 "ME discr.",
		 "B-tag discr.",
		 "Combined discr.",
		 "SL_6_g4_nWtag"
		 );

  roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		 "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		 "-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)/15.",
		 "(mem_tth_p[0] /(mem_tth_p[0]  + 0.03*mem_ttbb_p[0]*(1+10.*mem_tth_btag_weight_jj[0]/mem_tth_btag_weight_bb[0])))",
		 sl && TCut("njets==6 && nBCSVM>=4 && (Wmass>60 && Wmass<100)"),
		 sl && TCut("njets==6 && nBCSVM>=4 && (Wmass>60 && Wmass<100)"),
		 sl && TCut("njets==6 && nBCSVM>=4 && (Wmass>60 && Wmass<100)"),
		 "SL channel,  N_{b}#geq4, N_{j}=6, W-tag", 		
		 "ME discr.",
		 "B-tag discr.",
		 "Combined discr.",
		 "SL_6_g4_Wtag"
		 );
  }

  if( do5jets ){
  roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		 "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		 "-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)/15.",
		 "(mem_tth_p[0] /(mem_tth_p[0]  + 0.03*mem_ttbb_p[0]*(1+60.*mem_tth_btag_weight_jj[0]/mem_tth_btag_weight_bb[0])))",
		 sl && TCut("njets==5 && nBCSVM>=4"),
		 sl && TCut("njets==5 && nBCSVM>=4"),
		 sl && TCut("njets==5 && nBCSVM>=4"),
		 "SL channel,  N_{b}#geq4, N_{j}=5", 		
		 "ME discr.",
		 "B-tag discr.",
		 "Combined discr.",
		 "SL_5_g4"
		 );
  }

  if( do4jets ){
  roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		 "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		 "-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)/15.",
		 "(mem_tth_p[0] /(mem_tth_p[0]  + 0.03*mem_ttbb_p[0]*(1+40.*mem_tth_btag_weight_jj[0]/mem_tth_btag_weight_bb[0])))",
		 sl && TCut("njets==4 && nBCSVM>=4"),
		 sl && TCut("njets==4 && nBCSVM>=4"),
		 sl && TCut("njets==4 && nBCSVM>=4"),
		 "SL channel,  N_{b}#geq4, N_{j}=4", 		
		 "ME discr.",
		 "B-tag discr.",
		 "Combined discr.",
		 "SL_4_g4"
		 );

  }


  if(do3tags){
    roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		   "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		   "(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.",
		   "(mem_tth_p[0] /(mem_tth_p[0]  + 0.03*mem_ttbb_p[0]*(1+80.*mem_tth_btag_weight_jj[0]/mem_tth_btag_weight_bb[0])))",
		   sl && TCut("njets==4 && nBCSVM==3"),
		   sl && TCut("njets==4 && nBCSVM==3"),
		   sl && TCut("njets==4 && nBCSVM==3"),
		   "SL channel,  N_{b}=3, N_{j}=4", 		
		   "ME discr.",
		   "B-tag discr.",
		   "Combined discr.",
		   "SL_4_3",
		   1
		   );


    roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		   "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		   "(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.",
		   "-log(1./btag_LR_4b_2b_alt-1)/10.",
		   sl && TCut("njets==4 && nBCSVM==3"),
		   sl && TCut("njets==4 && nBCSVM==3"),
		   sl && TCut("njets==4 && nBCSVM==3"),
		   "SL channel,  N_{b}=3, N_{j}=4", 		
		   "ME discr.",
		   "B-tag discr.",
		   "B-tag event discr.",
		   "SL_4_3_v2"
		 );

    roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		   "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		   "(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.",
		   "(mem_tth_p[0] /(mem_tth_p[0]  + 0.03*mem_ttbb_p[0]*(1+80.*mem_tth_btag_weight_jj[0]/mem_tth_btag_weight_bb[0])))",
		   sl && TCut("njets==4 && nBCSVM==3") && TCut("(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.>0.6"),
		   sl && TCut("njets==4 && nBCSVM==3") && TCut("(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.>0.6"),
		   sl && TCut("njets==4 && nBCSVM==3") && TCut("(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.>0.6"),
		   "SL channel,  N_{b}=3, N_{j}=4, B-tag discr.>0.6", 		
		   "ME discr.",
		   "B-tag discr.",
		   "Combined discr.",
		   "SL_4_3_cut06",
		   0
		   );

    roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		   "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		   "(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.",
		   "(mem_tth_p[0] /(mem_tth_p[0]  + 0.004*mem_ttbb_p[0]*(1+80.*mem_tth_btag_weight_jj[0]/mem_tth_btag_weight_bb[0])))",
		   sl && TCut("njets==5 && nBCSVM==3"),
		   sl && TCut("njets==5 && nBCSVM==3"),
		   sl && TCut("njets==5 && nBCSVM==3"),
		   "SL channel,  N_{b}=3, N_{j}=5", 		
		   "ME discr.",
		   "B-tag discr.",
		   "Combined discr.",
		   "SL_5_3",
		   2
		   );

    roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		   "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		   "(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.",
		   "(mem_tth_p[0] /(mem_tth_p[0]  + 0.03*mem_ttbb_p[0]*(1+80.*mem_tth_btag_weight_jj[0]/mem_tth_btag_weight_bb[0])))",
		   sl && TCut("njets==5 && nBCSVM==3") && TCut("(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.>0.6"),
		   sl && TCut("njets==5 && nBCSVM==3") && TCut("(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.>0.6"),
		   sl && TCut("njets==5 && nBCSVM==3") && TCut("(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.>0.6"),
		   "SL channel,  N_{b}=3, N_{j}=5, B-tag discr.>0.6", 		
		   "ME discr.",
		   "B-tag discr.",
		   "Combined discr.",
		   "SL_5_3_cut06",
		   0
		   );

    roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		   "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		   "(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.",
		   "(mem_tth_p[0] /(mem_tth_p[0]  + 0.004*mem_ttbb_p[0]*(1+80.*mem_tth_btag_weight_jj[0]/mem_tth_btag_weight_bb[0])))",
		   sl && TCut("njets>=6 && nBCSVM==3"),
		   sl && TCut("njets>=6 && nBCSVM==3"),
		   sl && TCut("njets>=6 && nBCSVM==3"),
		   "SL channel,  N_{b}=3, N_{j}#geq6", 		
		   "ME discr.",
		   "B-tag discr.",
		   "Combined discr.",
		   "SL_g6_3",
		   2
		   );

    roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		   "mem_tth_p[0] /(mem_tth_p[0]  + 0.15*mem_ttbb_p[0])",
		   "(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.",
		   "(mem_tth_p[0] /(mem_tth_p[0]  + 0.03*mem_ttbb_p[0]*(1+80.*mem_tth_btag_weight_jj[0]/mem_tth_btag_weight_bb[0])))",
		   sl && TCut("njets>=6 && nBCSVM==3") && TCut("(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.>0.6"),
		   sl && TCut("njets>=6 && nBCSVM==3") && TCut("(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.>0.6"),
		   sl && TCut("njets>=6 && nBCSVM==3") && TCut("(-log(1./(mem_tth_btag_weight_bb[0]/(mem_tth_btag_weight_bb[0]+mem_tth_btag_weight_jj[0]))-1)+2)/8.>0.6"),
		   "SL channel,  N_{b}=3, N_{j}#geq6, B-tag discr.>0.6", 		
		   "ME discr.",
		   "B-tag discr.",
		   "Combined discr.",
		   "SL_g6_3_cut06",
		   0
		   );

  }
  if(do2tags){
    roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		   "btag_LR_4b_2b_alt",
		   "btag_LR_4b_2b_alt",
		   "btag_LR_4b_2b_alt",
		   sl && TCut("njets>=4 && nBCSVM==2"),
		   sl && TCut("njets>=4 && nBCSVM==2"),
		   sl && TCut("njets>=4 && nBCSVM==2"),
		   "SL channel,  N_{b}=2, N_{j}#geq4", 		
		   "B-tag discr.",
		   "B-tag discr.",
		   "B-tag discr.",
		   "SL_g4_2",
		   1
		   );
    roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		   "btag_LR_4b_2b_alt",
		   "btag_LR_4b_2b_alt",
		   "btag_LR_4b_2b_alt",
		   sl && TCut("njets>=6 && nBCSVM==2"),
		   sl && TCut("njets>=6 && nBCSVM==2"),
		   sl && TCut("njets>=6 && nBCSVM==2"),
		   "SL channel,  N_{b}=2, N_{j}#geq6", 		
		   "B-tag discr.",
		   "B-tag discr.",
		   "B-tag discr.",
		   "SL_g6_2",
		   1
		   );

    roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		   "btag_LR_4b_2b_alt",
		   "btag_LR_4b_2b_alt",
		   "btag_LR_4b_2b_alt",
		   sl && TCut("njets==5 && nBCSVM==2"),
		   sl && TCut("njets==5 && nBCSVM==2"),
		   sl && TCut("njets==5 && nBCSVM==2"),
		   "SL channel,  N_{b}=2, N_{j}=5", 		
		   "B-tag discr.",
		   "B-tag discr.",
		   "B-tag discr.",
		   "SL_5_2",
		   1
		   );

    roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		   "btag_LR_4b_2b_alt",
		   "btag_LR_4b_2b_alt",
		   "btag_LR_4b_2b_alt",
		   sl && TCut("njets==4 && nBCSVM==2"),
		   sl && TCut("njets==4 && nBCSVM==2"),
		   sl && TCut("njets==4 && nBCSVM==2"),
		   "SL channel,  N_{b}=2, N_{j}=4", 		
		   "B-tag discr.",
		   "B-tag discr.",
		   "B-tag discr.",
		   "SL_4_2",
		   1
		   );
  }

  return;
}
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
void run_ROC_DL( TString gcS1 = "", TString gcB1 = "", 
		 TString gcS2 = "", TString gcB2 = ""
		 ){
  
  //TString fS1 = path+gcS1+"/tth_13tev_amcatnlo_pu20bx25.root";
  //TString fB1 = path+gcB1+"/ttjets_13tev_madgraph_pu20bx25_phys14.root";
  
  TString fS1 = "/shome/bianchi/tth/gc/GC242bebe6c5b3/MEAnalysis_cfg_heppy/tth_13tev_amcatnlo_pu20bx25/output-sig.root";
  TString fB1 = "/shome/bianchi/tth/gc/GC499521aa4b0f/MEAnalysis_cfg_heppy/ttjets_13tev_madgraph_pu20bx25_phys14/output-bkg.root";


  roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		 "mem_tth_p[1] /(mem_tth_p[1]  + 0.15*mem_ttbb_p[1])",
		 "(-log(1./(mem_tth_btag_weight_bb[1]/(mem_tth_btag_weight_bb[1]+mem_tth_btag_weight_jj[1]))-1)+2)/10.",
		 "(mem_tth_p[1] /(mem_tth_p[1]  + 0.03*mem_ttbb_p[1]*(1+30.*mem_tth_btag_weight_jj[1]/mem_tth_btag_weight_bb[1])))",
		 dl && TCut("njets>=4 && nBCSVM>=4"),
		 dl && TCut("njets>=4 && nBCSVM>=4"),
		 dl && TCut("njets>=4 && nBCSVM>=4"),
		 "DL channel,  N_{b}#geq4, N_{j}#geq4", 		
		 "ME discr.",
		 "B-tag discr.",
		 "Combined discr.",
		 "DL_g4_g4",
		 2
		 );


  roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		 "mem_tth_p[1] /(mem_tth_p[1]  + 0.15*mem_ttbb_p[1])",
		 "(-log(1./(mem_tth_btag_weight_bb[1]/(mem_tth_btag_weight_bb[1]+mem_tth_btag_weight_jj[1]))-1)+2)/10.",
		 "(mem_tth_p[1] /(mem_tth_p[1]  + 0.005*mem_ttbb_p[1]*(1+30.*mem_tth_btag_weight_jj[1]/mem_tth_btag_weight_bb[1])))",
		 dl && TCut("njets>=4 && nBCSVM==3"),
		 dl && TCut("njets>=4 && nBCSVM==3"),
		 dl && TCut("njets>=4 && nBCSVM==3"),
		 "DL channel,  N_{b}=3, N_{j}#geq4", 		
		 "ME discr.",
		 "B-tag discr.",
		 "Combined discr.",
		 "DL_g4_3",
		 2
		 );

  roc_comp3_ROC( fS1, fB1, fS1, fB1, fS1, fB1,
		 "btag_LR_4b_2b_alt",
		 "btag_LR_4b_2b_alt",
		 "btag_LR_4b_2b_alt",
		 dl && TCut("njets>=4 && nBCSVM==2"),
		 dl && TCut("njets>=4 && nBCSVM==2"),
		 dl && TCut("njets>=4 && nBCSVM==2"),
		 "DL channel,  N_{b}=2, N_{j}#geq4", 		
		 "Combined discr.",
		 "Combined discr.",
		 "Combined discr.",
		 "DL_g4_2",
		 2
		 );


  return;
}
////////////////////////////////////////////////////////////////////


void run_all(){

  //run_test();
  //run_DL();
  run_SL_opt();  

}
