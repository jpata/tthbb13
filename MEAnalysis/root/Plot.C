#include <cstdlib>
#include <iostream> 
#include <map>
#include <string>
#include <vector>

#include "TMath.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"

#include "TH1F.h"
#include "TH2F.h"
#include "TF1.h"
#include "TF2.h"

#include "TPaveText.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TPad.h"
#include "TList.h"
#include "TCollection.h"
#include "TObject.h"
#include "TLegend.h"
#include "THStack.h"
#include "TCut.h"

#include "TVector3.h"
#include "TLorentzVector.h"

#define SAVEPLOTS 0


void plot_BestMass(TString fname  = "gen_default",
		   TString header = "Signal (parton-level)",
		   TString hname  = "hBestMass",
		   int color = 2
		   ){

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


  TCanvas *c1 = new TCanvas("c1","",5,30,650,600);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);

  TFile *f = TFile::Open("TestMENew_"+fname+".root","READ");


  TH1F* hBestMass = (TH1F*)f->Get(hname);
  if( !hBestMass ){
    cout << "No such histogram" << endl;
    return;
  }

  //hBestMass->Rebin(3);

  hBestMass->SetFillStyle(3004);
  hBestMass->SetFillColor(color);
  hBestMass->SetLineWidth(2);
  hBestMass->SetLineColor(color);
  hBestMass->SetTitle("");
  hBestMass->SetXTitle("#bar{M} (GeV)");
  hBestMass->SetYTitle("P(M)");
  
  TLegend* leg = new TLegend(0.48,0.65,0.78,0.85,NULL,"brNDC");
  leg->SetHeader( header );
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04); 

  string str_header(hname.Data());
  if( str_header.find("Prob")!=string::npos)
    leg->AddEntry(hBestMass, Form("#splitline{All permutations}{#mu=%.1f, RMS=%.1f}",  
				  hBestMass->GetMean(), hBestMass->GetRMS() ),"F");
  else
    leg->AddEntry(hBestMass, Form("#splitline{Good permutation}{#mu=%.1f, RMS=%.1f}",  
				  hBestMass->GetMean(), hBestMass->GetRMS() ),"F");


  hBestMass->DrawNormalized("HIST");
  leg->Draw();

  if(SAVEPLOTS){
    c1->SaveAs("plots/Plot_"+hname+"_"+fname+".png");
    c1->SaveAs("plots/Plot_"+hname+"_"+fname+".pdf");
  }

  return;
}




void plot_TF1d(TString fname  = "gen_default",
	       TString header = "Light jet TF",
	       TString unitsX = "jet E (GeV)",
	       TString unitsY = "TF(E|#hat{E})",
	       TString hname  = "tfWjet1",
	       int event = 1,
	       TString extraLabel = ""){

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


  TCanvas *c1 = new TCanvas("c1","",5,30,650,600);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);

  TFile *f = TFile::Open("TestMENew_"+fname+".root","READ");
  TH1F* hBestMass = (TH1F*)f->Get(TString(Form("Event_%d/",event))+hname);


  if( !hBestMass ){
    cout << "No such histogram" << endl;
    return;
  }

  hBestMass->SetLineWidth(2);
  hBestMass->SetLineColor(kRed);
  hBestMass->SetTitle("");
  hBestMass->SetXTitle( unitsX );
  hBestMass->SetYTitle( "units" );
  hBestMass->SetTitleSize(0.04,"X");
  hBestMass->SetTitleSize(0.04,"Y");

  TLegend* leg = new TLegend(0.65,0.65,0.80,0.85,NULL,"brNDC");
  leg->SetHeader( header );
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.06); 
  leg->AddEntry(hBestMass, unitsY);

  hBestMass->Draw("HIST");
  leg->Draw();

  if(SAVEPLOTS){
    c1->SaveAs("plots/Plot_"+hname+"_"+fname+extraLabel+".png");
    c1->SaveAs("plots/Plot_"+hname+"_"+fname+extraLabel+".pdf");
  }


  return;
}



void plot_TF2d(TString fname  = "gen_default",
	       TString header = "MEt TF",
	       TString unitsX = "p_{T} (GeV)",
	       TString unitsY = "#phi",
	       TString unitsZ = "TF(#phi|#hat{#phi},p_{T})",
	       TString hname  = "tfMetPhi",
	       int event = 1
	       ){

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


  TCanvas *c1 = new TCanvas("c1","",5,30,650,600);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);

  TFile *f = TFile::Open("TestMENew_"+fname+".root","READ");
  TH2F* hBestMass = (TH2F*)f->Get(TString(Form("Event_%d/",event))+hname);

  if( !hBestMass ){
    cout << "No such histogram" << endl;
    return;
  }

  hBestMass->SetLineWidth(2);
  hBestMass->SetLineColor(kRed);
  hBestMass->SetTitle("");
  hBestMass->SetXTitle( unitsX );
  hBestMass->SetYTitle( unitsY );

  TLegend* leg = new TLegend(0.65,0.65,0.80,0.85,NULL,"brNDC");
  leg->SetHeader( header );
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04); 
  leg->AddEntry(hBestMass, unitsZ);

  hBestMass->Draw("LEGO");
  leg->Draw();

  if(SAVEPLOTS){
    c1->SaveAs("plots/Plot_"+hname+"_"+fname+".png");
    c1->SaveAs("plots/Plot_"+hname+"_"+fname+".pdf");
  }


  return;
}



void plot_param(TString header = "Light jet TF",	      
		TString unitsX = "jet E (GeV)",
		TString unitsY = "Acceptance",
		TString hname  = "accLightBin0",
		float xLow  = 20,
		float xHigh = 100,
		float yLow  = -999,
		float yHigh = -999,
		TString extraLabel = ""
		){

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


  TCanvas *c1 = new TCanvas("c1","",5,30,650,600);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);

  TFile *f = TFile::Open("ControlPlots.root","READ");
  TH1F* hBestMass = (TH1F*)f->Get(hname);


  if( !hBestMass ){
    cout << "No such histogram" << endl;
    return;
  }


  TString fname;
  TIter iter( hBestMass->GetListOfFunctions() );
  TObject* obj = iter();
  while ( obj!=0 ){
    TF1* func = dynamic_cast<TF1*>(obj);
    //cout << func->GetName() << endl;
    fname = func->GetName();
    obj = iter();
  }
  TF1 *func = hBestMass->GetFunction(fname);
  cout << "Param 0: " << func->GetParameter(0) << endl;
  cout << "Param 1: " << func->GetParameter(1) << endl;

  hBestMass->SetMarkerStyle(kFullCircle);
  hBestMass->SetMarkerColor(kBlue);
  hBestMass->SetTitle("");
  hBestMass->SetXTitle( unitsX );
  hBestMass->SetYTitle( unitsY );
  hBestMass->SetTitleSize(0.05,"X");
  hBestMass->SetTitleSize(0.05,"Y");

  hBestMass->SetTitleOffset(0.90,"X");
  hBestMass->SetTitleOffset(0.83,"Y");

  hBestMass->GetXaxis()->SetRangeUser(xLow,xHigh);
  if(yLow!=-999 && yHigh!=-999)
    hBestMass->GetYaxis()->SetRangeUser(yLow,yHigh);

  TLegend* leg = new TLegend(0.15,0.65,0.55,0.85,NULL,"brNDC");
  leg->SetHeader( header );
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.06); 
  leg->AddEntry(func, "Fit", "L");

  hBestMass->Draw("PE");
  leg->Draw();

  if(SAVEPLOTS){
    c1->SaveAs("plots/Plot_"+hname+"_tf_"+extraLabel+".png");
    c1->SaveAs("plots/Plot_"+hname+"_tf_"+extraLabel+".pdf");
  }


  return;
}


void plot_P_plot(string mode = "SL2wj", string norm = "acc",
		 string level = "gen",
		 string mass = "bestInt",
		 string cat  = "SL(4,2)",
		 int event = 1){
		 
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


  TFile *f = TFile::Open(("MEValidator_"+mode+"_"+level+"_"+norm+".root").c_str(),"READ");
  TCanvas* c_gen = (TCanvas*)f->Get(Form("Event_%d/c_%s",event, level.c_str()));
  if(!c_gen) return;
  else cout << "Found!" << endl;
  c_gen->Draw();
  THStack* srec = (THStack*)(c_gen->FindObject(("stack_m_all_"+level).c_str()));
  if( srec!=0 ) cout << "Found!" << endl;

  string what = "dummy";
  if(level.find("rec")!=string::npos) what = "smeared";
  if(level.find("gen")!=string::npos) what = "partons";

  srec->SetTitle(("t#bar{t}h(125) "+cat+", "+what).c_str());
  srec->GetXaxis()->SetTitle("M (GeV)");
  srec->GetXaxis()->SetTitleSize(0.05);
  srec->GetXaxis()->SetTitleOffset(0.92);
  srec->GetYaxis()->SetTitle("P(M|Y_{p})");
  srec->GetYaxis()->SetTitleSize(0.05);
  srec->GetYaxis()->SetTitleOffset(0.85);

  //srec->Draw("");
  //TH1F* hStack = (TH1F*)srec->GetHistogram();
  //if( hStack!=0 )  cout << "Found!" << endl;
  //hStack->SetXTitle("#bar{M} (GeV)");
  //TLegend* leg = (TLegend*)(c_gen->FindObject("leg"));
  //if( leg!=0 ) cout << "Found!" << endl;

  //c_gen->Draw("");

  /*
  TH1F* hStack = 0;
  hStack = (TH1F*)srec->GetHistogram();
  if(!hStack) return;
  hStack->SetXTitle("#bar{M} (GeV)");
  hStack->SetYTitle("units");
  hStack->SetTitleSize(0.05,"Y");
  hStack->SetTitleSize(0.05,"X");
  hStack->SetTitleOffset(0.92,"X");
  hStack->SetTitleOffset(0.98,"Y");
  hStack->SetTitle("");
  hStack->SetMaximum( hStack->GetMaximum()*1.2);
  hStack->Draw();
  */

  string num(Form("%d",event));

  if(SAVEPLOTS){
    c_gen->SaveAs(("plots/Plot_"+mode+"_"+level+"_"+norm+"_"+mass+"_"+num+".png").c_str());
    c_gen->SaveAs(("plots/Plot_"+mode+"_"+level+"_"+norm+"_"+mass+"_"+num+".pdf").c_str());
  }

  return;


  
  

}

void plot_xsection(string cat  = ""){
		 
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


  TCanvas *c1 = new TCanvas("c1","",5,30,650,600);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);
  c1->SetLogy(1);


  TLegend* leg = new TLegend(0.52,0.60,0.82,0.88,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04); 

  TPaveText *pt = new TPaveText(.52,.22,.82,.35,"brNDC");
  pt->SetFillStyle(0);
  pt->SetBorderSize(0);
  pt->SetFillColor(10);
  pt->SetTextSize(0.04); 


  TFile *fxsec = TFile::Open("root_TestMENew/TestMENew_rec_XSec_v2.root","READ");
  TFile *facc  = TFile::Open("root_TestMENew/TestMENew_rec_Acc_v3.root", "READ");

  TH1F* hxsec = (TH1F*)fxsec->Get("hInt");
  hxsec->SetXTitle("#bar{M} (GeV)");
  hxsec->SetYTitle("#sigma (a.u.)");
  hxsec->SetTitleSize(0.05,"Y");
  hxsec->SetTitleSize(0.05,"X");
  hxsec->SetTitleOffset(0.92,"X");
  hxsec->SetTitleOffset(0.98,"Y");

  TH1F* hacc  = (TH1F*)facc->Get("hInt");

  hxsec->SetLineColor(kRed);
  hxsec->SetLineStyle(kSolid);
  hxsec->SetLineWidth(3);
  hxsec->SetFillStyle(3002);
  hxsec->SetFillColor(kRed);
  hxsec->SetMaximum( hxsec->GetMaximum()*1.2 );
  hxsec->SetMinimum( 8e15);

  hacc->SetLineColor(kBlue);
  hacc->SetLineStyle(kSolid);
  hacc->SetLineWidth(3);
  hacc->SetFillStyle(3002);
  hacc->SetFillColor(kBlue);
  hacc->SetMaximum( hacc->GetMaximum()*1.2 );


  hxsec->Draw("HIST");
  hacc->Draw("HISTSAME");

  leg->SetHeader(("t#bar{t}H(125)"+cat).c_str());
  leg->AddEntry(hxsec, "#sigma(M) from [4]", "F");
  leg->AddEntry(hacc,  "#sigma(M)#timesA from [4]", "F");

  TF1* fxxsec = new TF1("fxxsec", "9.06355e+18*TMath::Landau(x,5.47665e+01,1.05552e+01)", 50, 300);
  fxxsec->SetLineColor(kRed);
  TF1* fxacc  = new TF1("fxacc", "7.84e+17*TMath::Landau(x,6.17e+01,1.61e+01)", 50, 300);
  fxacc->SetLineColor(kBlue);

  fxxsec->Draw("SAME");
  fxacc->Draw("SAME");


  TH1F* htrue = (TH1F*)hxsec->Clone("htrue");
  htrue->Reset();
  htrue->Fill(80, 0.4277);
  htrue->Fill(100,0.2433);
  htrue->Fill(120,0.1459 );
  htrue->Fill(140,0.09150 );
  htrue->Fill(160,0.05978 );
  htrue->Fill(180,0.04061 );
  htrue->Fill(200,0.02858 );

  htrue->SetMarkerStyle(34);
  htrue->SetMarkerSize(2.0);
  htrue->SetMarkerColor(38);
  htrue->Scale(hxsec->GetBinContent(hxsec->FindBin(80))/htrue->GetBinContent(htrue->FindBin(80)));
  htrue->Draw("PSAME");

  leg->AddEntry(htrue, "#sigma(M) from Ref. [?]", "P");
  leg->Draw();

  if(SAVEPLOTS){
    c1->SaveAs("plots/Plot_xsection.pdf");
    c1->SaveAs("plots/Plot_xsection.png");
  }
}

void plot_genreco(string mode = "SL2wj", string norm = "acc",
		  string mass = "bestInt",
		  string cat  = "SL(4,2)",
		  int  nBins  = 20, 
		  float xLow  = 50,
		  float xHigh = 250){

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


  TCanvas *c1 = new TCanvas("c1","",5,30,650,600);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);


  TLegend* leg = new TLegend(0.52,0.60,0.82,0.88,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04); 

  TPaveText *pt = new TPaveText(.52,.22,.82,.35,"brNDC");
  pt->SetFillStyle(0);
  pt->SetBorderSize(0);
  pt->SetFillColor(10);
  pt->SetTextSize(0.04); 


  TFile *fgen = TFile::Open(("MEValidator_"+mode+"_gen_"+norm+".root").c_str(),"READ");
  TFile *frec = TFile::Open(("MEValidator_"+mode+"_rec_"+norm+".root").c_str(),"READ");

  TTree* tgen = (TTree*)fgen->Get("tree");
  TTree* trec = (TTree*)frec->Get("tree");

  TH1F* hgen_good = new TH1F("hgen_good","; #bar{M} (GeV); units", nBins, xLow, xHigh);
  hgen_good->SetLineColor(kRed);
  hgen_good->SetLineStyle(kSolid);
  hgen_good->SetLineWidth(3);
  hgen_good->SetFillStyle(3002);
  hgen_good->SetFillColor(kRed);
  hgen_good->SetMaximum( hgen_good->GetMaximum()*1.2 );
  TH1F* hgen_bad  = new TH1F("hgen_bad", "; #bar{M} (GeV); units", nBins, xLow, xHigh);
  hgen_bad->SetLineColor(kRed+2);
  hgen_bad->SetLineStyle(kDashed);
  hgen_bad->SetLineWidth(2);
  hgen_bad->SetFillStyle(3002);
  hgen_bad->SetFillColor(kRed+2);

  tgen->Draw( ("m_"+mass+"_all_gen>>hgen_good").c_str(),  ("match_"+mass+"_all_gen==1").c_str());
  tgen->Draw( ("m_"+mass+"_all_gen>>hgen_bad" ).c_str(),  ("match_"+mass+"_all_gen==0").c_str());
  float normgen = hgen_good->Integral() + hgen_bad->Integral();
  hgen_good->Scale(1./normgen);
  hgen_bad ->Scale(1./normgen);

  THStack*  sgen =  new THStack("gen","");
  sgen->Add(hgen_bad);
  sgen->Add(hgen_good);

  TH1F* hrec_good = new TH1F("hrec_good","; #bar{M} (GeV); units", nBins, xLow, xHigh);
  hrec_good->SetLineColor(kBlue);
  hrec_good->SetLineStyle(kSolid);
  hrec_good->SetLineWidth(3);
  hrec_good->SetFillStyle(3354);
  hrec_good->SetFillColor(kBlue);
  hrec_good->Sumw2();
  TH1F* hrec_bad  = new TH1F("hrec_bad", "; #bar{M} (GeV); units", nBins, xLow, xHigh);
  hrec_bad->SetLineColor(kBlue+2);
  hrec_bad->SetLineStyle(kDashed);
  hrec_bad->SetLineWidth(2);
  hrec_bad->SetFillStyle(3354);
  hrec_bad->SetFillColor(kBlue+2);
  hrec_bad->Sumw2();

  trec->Draw( ("m_"+mass+"_all_rec>>hrec_good").c_str(),  ("match_"+mass+"_all_rec==1").c_str());
  trec->Draw( ("m_"+mass+"_all_rec>>hrec_bad" ).c_str(),  ("match_"+mass+"_all_rec==0").c_str());
  float normrec = hrec_good->Integral() + hrec_bad->Integral();
  hrec_good->Scale(1./normrec);
  hrec_bad ->Scale(1./normrec);


  THStack*  srec =  new THStack("rec","");
  srec->Add(hrec_bad);
  srec->Add(hrec_good);

  sgen->Draw("HIST");
  srec->Draw("HISTESAME");
  hgen_bad->Draw("HISTSAME");
  
  TH1F* hStack = (TH1F*)sgen->GetHistogram();
  hStack->SetXTitle("#bar{M} (GeV)");
  hStack->SetYTitle("units");
  hStack->SetTitleSize(0.05,"Y");
  hStack->SetTitleSize(0.05,"X");
  hStack->SetTitleOffset(0.92,"X");
  hStack->SetTitleOffset(0.98,"Y");
  hStack->SetTitle(Form("Match efficiency: %.0f%% (partons), %.0f%% (smeared)", hgen_good->Integral()*100, hrec_good->Integral()*100  ));
  hStack->SetMaximum( hStack->GetMaximum()*1.2);

  leg->SetHeader(("t#bar{t}H(125), "+cat).c_str());
  leg->AddEntry(hgen_good, "partons, good" ,  "F");
  leg->AddEntry(hgen_bad,  "partons, wrong",  "F");
  leg->AddEntry(hrec_good, "smeared, good",   "F");
  leg->AddEntry(hrec_bad,  "smeared, wrong",  "F");

  leg->Draw();
  //sgen->Draw("HISTSAME");

  pt->AddText("Good matching:");
  pt->AddText(Form("partons: %.0f%%",hgen_good->Integral()*100 ))->SetTextColor(kRed);
  pt->AddText(Form("smeared: %.0f%%",hrec_good->Integral()*100 ))->SetTextColor(kBlue);
  pt->SetTextAlign(31);

  pt->Draw();

  if(SAVEPLOTS){
    c1->SaveAs(("plots/Plot_"+mode+"_"+norm+"_"+mass+".png").c_str());
    c1->SaveAs(("plots/Plot_"+mode+"_"+norm+"_"+mass+".pdf").c_str());
  }


  return;
}


void plot_genreco_prob(int gen = 1, 
		       string mode = "SL2wj", string norm = "acc",
		       string mass = "bestInt",
		       string cat  = "SL(4,2)",
		       int  nBins  = 20, 
		       float xLow  = 50,
		       float xHigh = 250){

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


  TCanvas *c1 = new TCanvas("c1","",5,30,650,600);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);


  TLegend* leg = new TLegend(0.52,0.60,0.82,0.88,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04); 

  TPaveText *pt = new TPaveText(.52,.22,.82,.35,"brNDC");
  pt->SetFillStyle(0);
  pt->SetBorderSize(0);
  pt->SetFillColor(10);
  pt->SetTextSize(0.04); 


  TFile *fgen = TFile::Open(("MEValidator_"+mode+"_gen_"+norm+".root").c_str(),"READ");
  TFile *frec = TFile::Open(("MEValidator_"+mode+"_rec_"+norm+".root").c_str(),"READ");

  TTree* tgen = (TTree*)fgen->Get("tree");
  TTree* trec = (TTree*)frec->Get("tree");

  TH1F* hgen_good = new TH1F("hgen_good","; -2Log(P(#bar{M}|Y); units", nBins, xLow, xHigh);
  hgen_good->SetLineColor(kRed);
  hgen_good->SetLineStyle(kSolid);
  hgen_good->SetLineWidth(3);
  hgen_good->SetFillStyle(3002);
  hgen_good->SetFillColor(kRed);
  hgen_good->SetMaximum( hgen_good->GetMaximum()*1.2 );
  TH1F* hgen_bad  = new TH1F("hgen_bad", "; -2Log(P(#bar{M}|Y); units", nBins, xLow, xHigh);
  hgen_bad->SetLineColor(kRed+2);
  hgen_bad->SetLineStyle(kDashed);
  hgen_bad->SetLineWidth(2);
  hgen_bad->SetFillStyle(3002);
  hgen_bad->SetFillColor(kRed+2);

  tgen->Draw( ("-2*TMath::Log(p_"+mass+"_all_gen)>>hgen_good").c_str(),  ("p_"+mass+"_all_gen>0 && match_"+mass+"_all_gen==1").c_str());
  tgen->Draw( ("-2*TMath::Log(p_"+mass+"_all_gen)>>hgen_bad" ).c_str(),  ("p_"+mass+"_all_gen>0 && match_"+mass+"_all_gen==0").c_str());
  float normgen = hgen_good->Integral() + hgen_bad->Integral();
  hgen_good->Scale(1./normgen);
  hgen_bad ->Scale(1./normgen);

  THStack*  sgen =  new THStack("gen","");
  sgen->Add(hgen_bad);
  sgen->Add(hgen_good);

  TH1F* hrec_good = new TH1F("hrec_good","; -2Log(P(#bar{M}|Y); units", nBins, xLow, xHigh);
  hrec_good->SetLineColor(kBlue);
  hrec_good->SetLineStyle(kSolid);
  hrec_good->SetLineWidth(3);
  hrec_good->SetFillStyle(3354);
  hrec_good->SetFillColor(kBlue);
  hrec_good->Sumw2();
  TH1F* hrec_bad  = new TH1F("hrec_bad", "; -2Log(P(#bar{M}|Y); units", nBins, xLow, xHigh);
  hrec_bad->SetLineColor(kBlue+2);
  hrec_bad->SetLineStyle(kDashed);
  hrec_bad->SetLineWidth(2);
  hrec_bad->SetFillStyle(3354);
  hrec_bad->SetFillColor(kBlue+2);
  hrec_bad->Sumw2();

  trec->Draw( ("-2*TMath::Log(p_"+mass+"_all_rec)>>hrec_good").c_str(),  ("p_"+mass+"_all_rec>0 && match_"+mass+"_all_rec==1").c_str());
  trec->Draw( ("-2*TMath::Log(p_"+mass+"_all_rec)>>hrec_bad" ).c_str(),  ("p_"+mass+"_all_rec>0 && match_"+mass+"_all_rec==0").c_str());
  float normrec = hrec_good->Integral() + hrec_bad->Integral();
  hrec_good->Scale(1./normrec);
  hrec_bad ->Scale(1./normrec);


  THStack*  srec =  new THStack("rec","");
  srec->Add(hrec_bad);
  srec->Add(hrec_good);

  if(gen){
    sgen->Draw("HIST");
    hgen_bad->Draw("HISTSAME");
  }
  else
    srec->Draw("HISTE");
  
  TH1F* hStack = 0;
  if(gen) 
    hStack = (TH1F*)sgen->GetHistogram();
  else
    hStack = (TH1F*)srec->GetHistogram();

  hStack->SetXTitle("-2Log(P(#bar{M}|Y))");
  hStack->SetYTitle("units");
  hStack->SetTitleSize(0.05,"Y");
  hStack->SetTitleSize(0.05,"X");
  hStack->SetTitleOffset(0.92,"X");
  hStack->SetTitleOffset(0.98,"Y");
  hStack->SetTitle(Form("Match efficiency: %.0f%% (partons), %.0f%% (smeared)", hgen_good->Integral()*100, hrec_good->Integral()*100  ));
  hStack->SetMaximum( hStack->GetMaximum()*1.2);

  leg->SetHeader(("t#bar{t}H(125), "+cat).c_str());
  if(gen){
    leg->AddEntry(hgen_good, "partons, good" ,  "F");
    leg->AddEntry(hgen_bad,  "partons, wrong",  "F");
  }
  else{
    leg->AddEntry(hrec_good, "smeared, good",   "F");
    leg->AddEntry(hrec_bad,  "smeared, wrong",  "F");
  }

  leg->Draw();
  //sgen->Draw("HISTSAME");

  pt->AddText("Good matching:");
  if(gen) 
    pt->AddText(Form("partons: %.0f%%",hgen_good->Integral()*100 ))->SetTextColor(kRed);
  else
    pt->AddText(Form("smeared: %.0f%%",hrec_good->Integral()*100 ))->SetTextColor(kBlue);
  pt->SetTextAlign(31);

  //pt->Draw();

  string level = gen==1 ? "gen" : "rec" ;

  if(SAVEPLOTS){
    c1->SaveAs(("plots/Plot_"+mode+"_"+norm+"_"+mass+"_prob_"+level+".png").c_str());
    c1->SaveAs(("plots/Plot_"+mode+"_"+norm+"_"+mass+"_prob_"+level+".pdf").c_str());
  }


  return;
}





void plot_genreco_good(string mode = "SL2wj", string norm = "acc",
		       string cat  = "SL(4,2)",
		       int  nBins  = 30, 
		       float xLow  = 50,
		       float xHigh = 250){

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


  TCanvas *c1 = new TCanvas("c1","",5,30,650,600);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);


  TLegend* leg = new TLegend(0.52,0.60,0.82,0.88,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04); 

  TPaveText *pt = new TPaveText(.52,.22,.82,.35,"brNDC");
  pt->SetFillStyle(0);
  pt->SetBorderSize(0);
  pt->SetFillColor(10);
  pt->SetTextSize(0.04); 


  TFile *fgen = TFile::Open(("MEValidator_"+mode+"_gen_"+norm+".root").c_str(),"READ");
  TFile *frec = TFile::Open(("MEValidator_"+mode+"_rec_"+norm+".root").c_str(),"READ");

  TTree* tgen = (TTree*)fgen->Get("tree");
  TTree* trec = (TTree*)frec->Get("tree");

  TH1F* hgen_good = new TH1F("hgen_good","; #bar{M} (GeV); units", nBins, xLow, xHigh);
  hgen_good->SetLineColor(kRed);
  hgen_good->SetLineStyle(kSolid);
  hgen_good->SetLineWidth(3);
  hgen_good->SetFillStyle(3002);
  hgen_good->SetFillColor(kRed);

  tgen->Draw( "m_best_good_gen>>hgen_good" );
  float normgen = hgen_good->Integral() ;
  hgen_good->Scale(1./normgen);
  TF1* gaus_gen = new TF1("gaus_gen","gaus",50,250);
  gaus_gen->SetNpx(1000);
  gaus_gen->SetLineColor(kRed);
  gaus_gen->SetParameter(1,hgen_good->GetMean() );
  hgen_good->Fit(gaus_gen, "", "", hgen_good->GetMean()-30, hgen_good->GetMean()+30 );
  hgen_good->SetMaximum( hgen_good->GetMaximum()*1.2);

  THStack*  sgen =  new THStack("gen","");
  sgen->Add(hgen_good);

  TH1F* hrec_good = new TH1F("hrec_good","; #bar{M} (GeV); units", nBins, xLow, xHigh);
  hrec_good->SetLineColor(kBlue);
  hrec_good->SetLineStyle(kSolid);
  hrec_good->SetLineWidth(3);
  hrec_good->SetFillStyle(3354);
  hrec_good->SetFillColor(kBlue);

  hrec_good->Sumw2();
  trec->Draw( "m_best_good_rec>>hrec_good" );
  float normrec = hrec_good->Integral();
  hrec_good->Scale(1./normrec);
  TF1* gaus_rec = new TF1("gaus_rec","gaus",50,250);
  gaus_rec->SetLineColor(kBlue);
  gaus_rec->SetParameter(1,hrec_good->GetMean() );
  hrec_good->Fit(gaus_rec, "", "", hrec_good->GetMean()-30, hrec_good->GetMean()+30 );


  THStack*  srec =  new THStack("rec","");
  srec->Add(hrec_good);

  sgen->Draw("HIST");
  srec->Draw("HISTESAME");
  gaus_gen->Draw("SAME");
  gaus_rec->Draw("SAME");
  
  TH1F* hStack = (TH1F*)sgen->GetHistogram();
  hStack->SetXTitle("#bar{M} (GeV)");
  hStack->SetYTitle("units");
  hStack->SetTitleSize(0.05,"Y");
  hStack->SetTitleSize(0.05,"X");
  hStack->SetTitleOffset(0.92,"X");
  hStack->SetTitleOffset(0.98,"Y");

  leg->SetHeader(("t#bar{t}H(125), "+cat).c_str());
  leg->AddEntry(hgen_good, "partons" ,  "F");
  leg->AddEntry(hrec_good, "smeared",   "F");

  leg->Draw();
  //sgen->Draw("HISTSAME");

  pt->AddText("Gaussian fit:");
  pt->AddText(Form("#mu=%.0f, #sigma =  %.1f GeV", gaus_gen->GetParameter(1),gaus_gen->GetParameter(2)  ))->SetTextColor(kRed);
  pt->AddText(Form("#mu=%.0f, #sigma = %.1f GeV",  gaus_rec->GetParameter(1),gaus_rec->GetParameter(2)))->SetTextColor(kBlue);
  pt->SetTextAlign(11);
  pt->Draw();

  if(SAVEPLOTS){
    c1->SaveAs(("plots/Plot_"+mode+"_"+norm+"_good_gen_vs_reco.png").c_str());
    c1->SaveAs(("plots/Plot_"+mode+"_"+norm+"_good_gen_vs_reco.pdf").c_str());
  }


  return;
}




void plot_masses(string mode = "SL2wj", 
		 string norm = "acc",
		 string level = "gen",
		 string mass1 = "bestInt",  string mass2 = "bestMax",
		 string cat  = "SL(4,2)",
		 int  nBins  = 20, 
		 float xLow  = 50,
		 float xHigh = 250){

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


  TCanvas *c1 = new TCanvas("c1","",5,30,650,600);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);


  TLegend* leg = new TLegend(0.50,0.60,0.80,0.88,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04); 

  TPaveText *pt = new TPaveText(.52,.22,.82,.35,"brNDC");
  pt->SetFillStyle(0);
  pt->SetBorderSize(0);
  pt->SetFillColor(10);
  pt->SetTextSize(0.04); 


  string what = "dummy";
  if(level.find("rec")!=string::npos) what = "smeared";
  if(level.find("gen")!=string::npos) what = "partons";

  string mass_1 = "dummy";
  int old_1 = 0;
  if(mass1.find("Int")!=string::npos) 
    mass_1 = "max_{p}#left{#intP(M|Y_{p})dM#right}";
  else if(mass1.find("Max")!=string::npos) 
    mass_1 = "max_{p,M}#left{P(M|Y_{p})#right}";
  else{
    mass_1 = "max_{M}#left{#sum_{P}P(M|Y_{p})#right}";
    old_1  = 1;
  }

 
  string mass_2 = "dummy";
  int old_2 = 0;
  if(mass2.find("Int")!=string::npos) 
    mass_2 = "max_{p}#left{#intP(M|Y_{p})dM#right}";
  else if(mass2.find("Max")!=string::npos) 
    mass_2 = "max_{p,M}#left{P(M|Y_{p})#right}";
  else{
    mass_2 = "max_{M}#left{#sumP(M|Y_{p})#right}";
    old_2  = 1;
  }


  TFile *fgen = TFile::Open(("MEValidator_"+mode+"_"+level+"_"+norm+".root").c_str(),"READ");
  TFile *frec = TFile::Open(("MEValidator_"+mode+"_"+level+"_"+norm+".root").c_str(),"READ");

  TTree* tgen = (TTree*)fgen->Get("tree");
  TTree* trec = (TTree*)frec->Get("tree");

  TH1F* hgen_good = new TH1F("hgen_good","; #bar{M} (GeV); units", nBins, xLow, xHigh);
  hgen_good->SetLineColor(kRed);
  hgen_good->SetLineStyle(kSolid);
  hgen_good->SetLineWidth(3);
  hgen_good->SetFillStyle(3002);
  hgen_good->SetFillColor(kRed);
 
  hgen_good->Sumw2();
  if(old_1<0.5) tgen->Draw( ("m_"+mass1+"_all_"+level+">>hgen_good").c_str(),  ("m_"+mass1+"_all_"+level+">0 && match_"+mass1+"_all_"+level+">0").c_str());
  float match1 = hgen_good->Integral() ; hgen_good->Reset();
  tgen->Draw( ("m_"+mass1+"_all_"+level+">>hgen_good").c_str(),  ("m_"+mass1+"_all_"+level+">0").c_str());

  float normgen = hgen_good->Integral() ;
  hgen_good->Scale(1./normgen);

  THStack*  sgen =  new THStack("gen","");
  sgen->Add(hgen_good);

  TH1F* hrec_good = new TH1F("hrec_good","; #bar{M} (GeV); units", nBins, xLow, xHigh);
  hrec_good->SetLineColor(kBlue);
  hrec_good->SetLineStyle(kSolid);
  hrec_good->SetLineWidth(3);
  hrec_good->SetFillStyle(3354);
  hrec_good->SetFillColor(kBlue);

  hrec_good->Sumw2();
  if(old_2<0.5) trec->Draw( ("m_"+mass2+"_all_"+level+">>hrec_good").c_str(),  ("m_"+mass2+"_all_"+level+">0 && match_"+mass2+"_all_"+level+">0").c_str());
  float match2 = hrec_good->Integral() ; hrec_good->Reset();
  trec->Draw( ("m_"+mass2+"_all_"+level+">>hrec_good").c_str(),  ("m_"+mass2+"_all_"+level+">0").c_str());
  float normrec = hrec_good->Integral() ;
  hrec_good->Scale(1./normrec);


  THStack*  srec =  new THStack("rec","");
  srec->Add(hrec_good);

  sgen->Draw("HISTE");
  srec->Draw("HISTESAME");
   
  TH1F* hStack = (TH1F*)sgen->GetHistogram();
  hStack->SetXTitle("#bar{M} (GeV)");
  hStack->SetYTitle("units");
  hStack->SetTitleSize(0.05,"Y");
  hStack->SetTitleSize(0.05,"X");
  hStack->SetTitleOffset(0.92,"X");
  hStack->SetTitleOffset(0.98,"Y");
  hStack->SetTitle(Form("Match efficiency: %.0f%% (partons), %.0f%% (smeared)", hgen_good->Integral()*100, hrec_good->Integral()*100  ));



  leg->SetHeader(("t#bar{t}H(125), "+cat).c_str());
  leg->AddEntry(hgen_good, (mass_1).c_str() ,  "F");
  leg->AddEntry(hrec_good, (mass_2).c_str(),   "F");

  leg->Draw();
  //sgen->Draw("HISTSAME");

  pt->AddText("Good matching:");
  if(old_1<0.5) pt->AddText(Form("%.0f%%",match1/normgen*100 ))->SetTextColor(kRed);
  if(old_2<0.5) pt->AddText(Form("%.0f%%",match2/normrec*100 ))->SetTextColor(kBlue);
  pt->SetTextAlign(31);

  pt->Draw();

  if(SAVEPLOTS){
    c1->SaveAs(("plots/Plot_"+mode+"_"+norm+"_"+mass1+"_vs_"+mass2+".png").c_str());
    c1->SaveAs(("plots/Plot_"+mode+"_"+norm+"_"+mass1+"_vs_"+mass2+".pdf").c_str());
  }


  return;
}


void plot_norm(string mode = "SL2wj", 
	       string norm1 = "acc",
	       string norm2 = "unnorm",
	       string level = "gen",
	       string mass = "bestInt",
	       string cat  = "SL(4,2)",
	       int  nBins  = 20, 
	       float xLow  = 50,
	       float xHigh = 250,
	       int match = 1
	       ){

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


  TCanvas *c1 = new TCanvas("c1","",5,30,650,600);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);


  TLegend* leg = new TLegend(0.50,0.60,0.80,0.88,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04); 

  TPaveText *pt = new TPaveText(.52,.22,.82,.35,"brNDC");
  pt->SetFillStyle(0);
  pt->SetBorderSize(0);
  pt->SetFillColor(10);
  pt->SetTextSize(0.04); 

  int old = 1;
  if(mass.find("Int")!=string::npos || mass.find("Max")!=string::npos) old = 0;

  string what = "dummy";
  if(level.find("rec")!=string::npos) what = "smeared";
  if(level.find("gen")!=string::npos) what = "partons";

  string norm_1 = "dummy";
  if(norm1.find("acc")!=string::npos) 
    norm_1 = "N= #sigma(M)#times A";
  else if(norm1.find("unnorm")!=string::npos) 
    norm_1 = "N=1";
  else{
  }

 
  string norm_2 = "dummy";
  if(norm2.find("acc")!=string::npos) 
    norm_2 = "N= #sigma(M)#timesAcc";
  else if(norm2.find("unnorm")!=string::npos) 
    norm_2 = "N=1";
  else{
  }

  string sign = match>0.5 ? ">" : "<" ;
 

  TFile *fgen = TFile::Open(("MEValidator_"+mode+"_"+level+"_"+norm1+".root").c_str(),"READ");
  TFile *frec = TFile::Open(("MEValidator_"+mode+"_"+level+"_"+norm2+".root").c_str(),"READ");

  TTree* tgen = (TTree*)fgen->Get("tree");
  TTree* trec = (TTree*)frec->Get("tree");

  TH1F* hgen_good = new TH1F("hgen_good","; #bar{M} (GeV); units", nBins, xLow, xHigh);
  hgen_good->SetLineColor(kRed);
  hgen_good->SetLineStyle(kSolid);
  hgen_good->SetLineWidth(3);
  hgen_good->SetFillStyle(3002);
  hgen_good->SetFillColor(kRed);
 
  hgen_good->Sumw2();
  if(old<0.5) tgen->Draw( ("m_"+mass+"_all_"+level+">>hgen_good").c_str(),  ("m_"+mass+"_all_"+level+">0 && match_"+mass+"_all_"+level+">-0.5").c_str());
  float match1 = hgen_good->Integral() ; hgen_good->Reset();
  tgen->Draw( ("m_"+mass+"_all_"+level+">>hgen_good").c_str(),  ("m_"+mass+"_all_"+level+">0 && match_"+mass+"_all_"+level+sign+"0.5").c_str());

  float normgen = hgen_good->Integral() ;
  hgen_good->Scale(1./normgen);

  THStack*  sgen =  new THStack("gen","");
  sgen->Add(hgen_good);

  TH1F* hrec_good = new TH1F("hrec_good","; #bar{M} (GeV); units", nBins, xLow, xHigh);
  hrec_good->SetLineColor(kBlue);
  hrec_good->SetLineStyle(kSolid);
  hrec_good->SetLineWidth(3);
  hrec_good->SetFillStyle(3354);
  hrec_good->SetFillColor(kBlue);

  hrec_good->Sumw2();
  if(old<0.5) trec->Draw( ("m_"+mass+"_all_"+level+">>hrec_good").c_str(),  ("m_"+mass+"_all_"+level+">0 && match_"+mass+"_all_"+level+">-0.5").c_str());
  float match2 = hrec_good->Integral() ; hrec_good->Reset();
  trec->Draw( ("m_"+mass+"_all_"+level+">>hrec_good").c_str(),  ("m_"+mass+"_all_"+level+">0 && match_"+mass+"_all_"+level+sign+"0.5").c_str());
  float normrec = hrec_good->Integral() ;
  hrec_good->Scale(1./normrec);


  THStack*  srec =  new THStack("rec","");
  srec->Add(hrec_good);

  if(hgen_good->GetMaximum() > hrec_good->GetMaximum()){
    sgen->Draw("HISTE");
    srec->Draw("HISTESAME");
  }
  else{
    srec->Draw("HISTE");
    sgen->Draw("HISTESAME");
  }
   
  TH1F* hStack = (TH1F*)sgen->GetHistogram();
  hStack->SetXTitle("#bar{M} (GeV)");
  hStack->SetYTitle("units");
  hStack->SetTitleSize(0.05,"Y");
  hStack->SetTitleSize(0.05,"X");
  hStack->SetTitleOffset(0.92,"X");
  hStack->SetTitleOffset(0.98,"Y");
  hStack->SetTitle(Form("Match efficiency: %.0f%% (partons), %.0f%% (smeared)" ,hgen_good->Integral()*100, hrec_good->Integral()*100  ));
  hStack->SetMaximum( hStack->GetMaximum()*1.2);


  leg->SetHeader(("t#bar{t}H(125), "+cat).c_str());
  leg->AddEntry(hgen_good, (norm_1).c_str() ,  "F");
  leg->AddEntry(hrec_good, (norm_2).c_str(),   "F");

  leg->Draw();
  //sgen->Draw("HISTSAME");

  pt->AddText("Good matching:");
  if(old<0.5) pt->AddText(Form("%.0f%%",match>0.5 ? (1/match1*normgen*100) : (1-1/match1*normgen)*100 ))->SetTextColor(kRed);
  if(old<0.5) pt->AddText(Form("%.0f%%",match>0.5 ? (1/match2*normrec*100) : (1-1/match2*normrec)*100 ))->SetTextColor(kBlue);
  pt->SetTextAlign(31);

  if(old<0.5) pt->Draw();

  string isMatch = match>0.5 ? "match" : "unmatch" ;
  if(SAVEPLOTS){
    c1->SaveAs(("plots/Plot_"+mode+"_"+mass+"_"+norm1+"_vs_"+norm2+"_"+isMatch+".png").c_str());
    c1->SaveAs(("plots/Plot_"+mode+"_"+mass+"_"+norm1+"_vs_"+norm2+"_"+isMatch+".pdf").c_str());
  }


  return;
}





void plot_systematics(int syst = 0, string mode = "SL2wj", string norm = "acc",
		      string mass = "bestInt",
		      string cat  = "SL(4,2)",
		      int  nBins  = 20, 
		      float xLow  = 50,
		      float xHigh = 250){

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


  TCanvas *c1 = new TCanvas("c1","",5,30,650,600);
  c1->SetGrid(0,0);
  c1->SetFillStyle(4000);
  c1->SetFillColor(10);
  c1->SetTicky();
  c1->SetObjectStat(0);


  TLegend* leg = new TLegend(0.50,0.60,0.80,0.88,NULL,"brNDC");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetFillColor(10);
  leg->SetTextSize(0.04);
  leg->SetHeader(("t#bar{t}H(125), "+cat).c_str());

  TFile *fgen_nominal = syst<6 ? TFile::Open(("MEValidator_"+mode+"_gen_"+norm+".root").c_str(),"READ") : TFile::Open(("MEValidator_"+mode+"_rec_"+norm+".root").c_str(),"READ");
  TFile *fgen_noME    = TFile::Open(("MEValidator_"+mode+"_gen_"+norm+"_noME.root").c_str(),"READ");
  TFile *fgen_noMET   = TFile::Open(("MEValidator_"+mode+"_gen_"+norm+"_noMET.root").c_str(),"READ");
  TFile *fgen_noJac   = TFile::Open(("MEValidator_"+mode+"_gen_"+norm+"_noJac.root").c_str(),"READ");
  TFile *fgen_noTF    = TFile::Open(("MEValidator_"+mode+"_gen_"+norm+"_noTF.root").c_str(),"READ");
  TFile *fgen_noPDF   = TFile::Open(("MEValidator_"+mode+"_gen_"+norm+"_noPDF.root").c_str(),"READ");
  TFile *fgen_jUp     = TFile::Open(("MEValidator_"+mode+"_rec_"+norm+"_jUp.root").c_str(),"READ");
  TFile *fgen_bUp     = TFile::Open(("MEValidator_"+mode+"_rec_"+norm+"_bUp.root").c_str(),"READ");
  TFile *fgen_METUp   = TFile::Open(("MEValidator_"+mode+"_rec_"+norm+"_METUp.root").c_str(),"READ");

  vector<TFile*> files;
  files.push_back(fgen_nominal);
  files.push_back(fgen_noME);
  files.push_back(fgen_noMET);
  files.push_back(fgen_noJac);
  files.push_back(fgen_noTF);
  files.push_back(fgen_noPDF);
  files.push_back(fgen_jUp);
  files.push_back(fgen_bUp);
  files.push_back(fgen_METUp);
  
  vector<TH1F*> histos;

  TH1F* h = new TH1F("h","; #bar{M} (GeV); units", nBins, xLow, xHigh);
  h->SetTitleSize(0.05,"Y");
  h->SetTitleSize(0.05,"X");
  h->SetTitleOffset(0.92,"X");
  h->SetTitleOffset(0.98,"Y");

  for(unsigned int k = 0; k < files.size(); k++){
    TH1F*  h2 = (TH1F*)h->Clone(Form("h_%d",k));

    if(!files[k]){
      histos.push_back( 0 );
      continue;
    }

    TTree* t = (TTree*)files[k]->Get("tree");
    h2->Sumw2();
    if(k<6 && syst<6)
      t->Draw( Form("m_%s_all_gen>>h_%d", mass.c_str(), k) ,  ("m_"+mass+"_all_gen>0").c_str());
    else if( k<6 && syst>5)
      t->Draw( Form("m_%s_all_rec>>h_%d", mass.c_str(), k) ,  ("m_"+mass+"_all_rec>0").c_str());
    else if(k>5 && syst>5)
      t->Draw( Form("m_%s_all_rec>>h_%d", mass.c_str(), k) ,  ("m_"+mass+"_all_rec>0").c_str());
    else{}

    h2->Scale(1./h2->Integral());
    if(k==0){
      h2->SetLineColor(kRed);
      h2->SetLineStyle(kSolid);
      h2->SetLineWidth(3);
      h2->SetFillStyle(3354);
      h2->SetFillColor(kRed);
    }
    else{
      h2->SetLineColor(kBlue);
      h2->SetLineStyle(kDashed);
      h2->SetLineWidth(3);
      h2->SetFillStyle(0);
      h2->SetFillColor(0);
    }
    histos.push_back( h2 );
  }

  float max = 0;
  for( unsigned int k = 0; k < histos.size(); k++ ){
    if( !histos[k] ) continue;
    if( histos[k]->GetMaximum()>max) max =  histos[k]->GetMaximum();
  }

  string name = "dummy";

  for(unsigned int k = 0; k < histos.size(); k++){

    if( !histos[k] ) continue;

    histos[k]->GetYaxis()->SetRangeUser(0, max*1.2);

    if(k==0) 
      histos[k]->Draw("HIST");
    else if(k>0 && k==syst)
      histos[k]->Draw("HISTESAME");
    else{};

    if( (string(files[k]->GetName())).find("noME.")!=string::npos )
      name = "w/o ME";
    else if( (string(files[k]->GetName())).find("noMET.")!=string::npos )
      name = "w/o E_{T}^{miss} TF";
    else if( (string(files[k]->GetName())).find("noTF.")!=string::npos )
      name = "w/o jet TF";
    else if( (string(files[k]->GetName())).find("noJac.")!=string::npos )
      name = "w/o Jacobians";
    else if( (string(files[k]->GetName())).find("noPDF.")!=string::npos )
      name = "w/o PDF";
    else if( (string(files[k]->GetName())).find("jUp.")!=string::npos )
      name = "1.25 #times #sigma_{j}";
    else if( (string(files[k]->GetName())).find("bUp.")!=string::npos )
      name = "1.25 #times #sigma_{b}";
    else if( (string(files[k]->GetName())).find("METUp.")!=string::npos )
      name = "1.25 #times #sigma_{MET}";
    else
      name = "Nominal";

    if(k==0 || (k>0 && k==syst)) leg->AddEntry( histos[k], name.c_str(), "F" );
  }
 
  leg->Draw();

  if(SAVEPLOTS){
    c1->SaveAs(("plots/Plot_"+mode+"_"+norm+"_"+mass+"_"+string(Form("%d",syst))+".png").c_str());
    c1->SaveAs(("plots/Plot_"+mode+"_"+norm+"_"+mass+"_"+string(Form("%d",syst))+".pdf").c_str());
  }


  return;

}


void makeAll(){

  plot_P_plot("SL2wj","acc","gen","bestInt","SL(4,2)",1);
  plot_P_plot("SL2wj","acc","gen","bestInt","SL(4,2)",2);
  plot_P_plot("SL2wj","acc","gen","bestInt","SL(4,2)",6);
  plot_P_plot("SL2wj","acc","gen","bestInt","SL(4,2)",7);
  plot_P_plot("SL2wj","acc","gen","bestInt","SL(4,2)",8);
  plot_P_plot("SL1wj","acc","gen","bestInt","SL(4,1)",1);
  plot_P_plot("SL1wj","acc","gen","bestInt","SL(4,1)",4);
  plot_P_plot("SL1wj","acc","gen","bestInt","SL(4,1)",5);
  plot_P_plot("SLNoBHad","acc","gen","bestInt","SL(3,2) no b_{h}",1);
  plot_P_plot("SLNoBHad","acc","gen","bestInt","SL(3,2) no b_{h}",4);
  plot_P_plot("SLNoBHad","acc","gen","bestInt","SL(3,2) no b_{h}",5);
  plot_P_plot("SLNoBLep","acc","gen","bestInt","SL(3,2) no b_{l}",4);
  plot_P_plot("DL",      "acc","gen","bestInt","DL(4,N)",1);
  plot_P_plot("DL",      "acc","gen","bestInt","DL(4,N)",2);
  plot_P_plot("DL",      "acc","gen","bestInt","DL(4,N)",4);
  plot_P_plot("DL",      "acc","gen","bestInt","DL(4,N)",5);
  plot_P_plot("DL",      "acc","gen","bestInt","DL(4,N)",6);
  plot_P_plot("DL",      "acc","gen","bestInt","DL(4,N)",7);

  plot_genreco("SL2wj",   "acc","bestInt","SL(4,2)",           25,50,250);
  plot_genreco("SL1wj",   "acc","bestInt","SL(4,2)",           25,50,250);
  plot_genreco("SLNoBHad","acc","bestInt","SL(3,2) no b_{q}",  25,50,250);
  plot_genreco("SLNoBLep","acc","bestInt","SL(3,2) no b_{l}",  25,50,250);
  plot_genreco("DL",      "acc","bestInt","DL(4,N)",           25,50,250);
  
  plot_genreco("SL2wj",   "unnorm","bestInt","SL(4,2)",           25,50,250);
  plot_genreco("SL1wj",   "unnorm","bestInt","SL(4,2)",           25,50,250);
  plot_genreco("SLNoBHad","unnorm","bestInt","SL(3,2) no b_{q}",  25,50,250);
  plot_genreco("SLNoBLep","unnorm","bestInt","SL(3,2) no b_{l}",  25,50,250);
  plot_genreco("DL",      "unnorm","bestInt","DL(4,N)",           25,50,250);

  plot_systematics(1, "SL2wj",  "acc", "bestInt", "SL(4,2) partons", 50, 50, 250);
  plot_systematics(2, "SL2wj",  "acc", "bestInt", "SL(4,2) partons", 50, 50, 250);
  plot_systematics(3, "SL2wj",  "acc", "bestInt", "SL(4,2) partons", 50, 50, 250);
  plot_systematics(4, "SL2wj",  "acc", "bestInt", "SL(4,2) partons", 50, 50, 250);
  plot_systematics(5, "SL2wj",  "acc", "bestInt", "SL(4,2) partons", 50, 50, 250);
  plot_systematics(6, "SL2wj",  "acc", "bestInt", "SL(4,2) smeared", 15, 50, 250);
  plot_systematics(7, "SL2wj",  "acc", "bestInt", "SL(4,2) smeared", 15, 50, 250);
  plot_systematics(8, "SL2wj",  "acc", "bestInt", "SL(4,2) smeared", 15, 50, 250);

  plot_systematics(6, "SL1wj",  "acc", "bestInt", "SL(4,1) smeared", 15, 50, 250);
  plot_systematics(7, "SL1wj",  "acc", "bestInt", "SL(4,1) smeared", 15, 50, 250);
  plot_systematics(8, "SL1wj",  "acc", "bestInt", "SL(4,1) smeared", 15, 50, 250);

  plot_masses("SL2wj","acc","gen","bestInt","best","SL(4,2) partons",20,50,250);
  plot_masses("SL1wj","acc","gen","bestInt","best","SL(4,1) partons",20,50,250);
  plot_masses("SLNoBHad","acc","gen","bestInt","best","SL(3,2) partons",20,50,250);
  plot_masses("SLNoBLep","acc","gen","bestInt","best","SL(3,2) partons",20,50,250);
  plot_masses("DL","acc","gen","bestInt","best","DL(4,N) partons",20,50,250);

  plot_masses("SL2wj","unnorm","gen","bestInt","best","SL(4,2) partons",20,50,250);
  plot_masses("SL1wj","unnorm","gen","bestInt","best","SL(4,1) partons",20,50,250);
  plot_masses("SLNoBHad","unnorm","gen","bestInt","best","SL(3,2) partons",20,50,250);
  plot_masses("SLNoBLep","unnorm","gen","bestInt","best","SL(3,2) partons",20,50,250);
  plot_masses("DL","unnorm","gen","bestInt","best","DL(4,N) partons",20,50,250);

  //plot_masses("SL2wj","acc","rec","bestInt","best","SL(4,2) partons",15,50,250);
  //plot_masses("SL1wj","acc","rec","bestInt","best","SL(4,1) partons",15,50,250);
  //plot_masses("SLNoBHad","acc","rec","bestInt","best","SL(3,2) partons",15,50,250);
  //plot_masses("SLNoBLep","acc","rec","bestInt","best","SL(3,2) partons",15,50,250);
  //plot_masses("DL","acc","rec","bestInt","best","DL(4,N) partons",15,50,250);

  //plot_masses("SL2wj","unnorm","rec","bestInt","best","SL(4,2) partons",15,50,250);
  //plot_masses("SL1wj","unnorm","rec","bestInt","best","SL(4,1) partons",15,50,250);
  //plot_masses("SLNoBHad","unnorm","rec","bestInt","best","SL(3,2) partons",15,50,250);
  //plot_masses("SLNoBLep","unnorm","rec","bestInt","best","SL(3,2) partons",15,50,250);
  //plot_masses("DL","unnorm","rec","bestInt","best","DL(4,N) partons",15,50,250);


  plot_masses("SL2wj","acc","gen","bestInt","bestMax","SL(4,2) partons",20,50,250);
  plot_masses("SL1wj","acc","gen","bestInt","bestMax","SL(4,1) partons",20,50,250);
  plot_masses("SLNoBHad","acc","gen","bestInt","bestMax","SL(3,2) partons",20,50,250);
  plot_masses("SLNoBLep","acc","gen","bestInt","bestMax","SL(3,2) partons",20,50,250);
  plot_masses("DL","acc","gen","bestInt","bestMax","DL(4,N) partons",20,50,250);

  plot_masses("SL2wj","unnorm","gen","bestInt","bestMax","SL(4,2) partons",20,50,250);
  plot_masses("SL1wj","unnorm","gen","bestInt","bestMax","SL(4,1) partons",20,50,250);
  plot_masses("SLNoBHad","unnorm","gen","bestInt","bestMax","SL(3,2) partons",20,50,250);
  plot_masses("SLNoBLep","unnorm","gen","bestInt","bestMax","SL(3,2) partons",20,50,250);
  plot_masses("DL","unnorm","gen","bestInt","bestMax","DL(4,N) partons",20,50,250);

  //plot_masses("SL2wj","acc","rec","bestInt","bestMax","SL(4,2) partons",15,50,250);
  //plot_masses("SL1wj","acc","rec","bestInt","bestMax","SL(4,1) partons",15,50,250);
  //plot_masses("SLNoBHad","acc","rec","bestInt","bestMax","SL(3,2) partons",15,50,250);
  //plot_masses("SLNoBLep","acc","rec","bestInt","bestMax","SL(3,2) partons",15,50,250);
  //plot_masses("DL","acc","rec","bestInt","bestMax","DL(4,N) partons",15,50,250);

  //plot_masses("SL2wj","unnorm","rec","bestInt","bestMax","SL(4,2) partons",15,50,250);
  //plot_masses("SL1wj","unnorm","rec","bestInt","bestMax","SL(4,1) partons",15,50,250);
  //plot_masses("SLNoBHad","unnorm","rec","bestInt","bestMax","SL(3,2) partons",15,50,250);
  //plot_masses("SLNoBLep","unnorm","rec","bestInt","bestMax","SL(3,2) partons",15,50,250);
  //plot_masses("DL","unnorm","rec","bestInt","bestMax","DL(4,N) partons",15,50,250);

  plot_norm("SL2wj",   "acc","unnorm", "gen", "bestInt", "SL(4,2) partons",30,50,250,1);
  plot_norm("SL1wj",   "acc","unnorm", "gen", "bestInt", "SL(4,1) partons",30,50,250,1);
  plot_norm("SLNoBHad","acc","unnorm", "gen", "bestInt", "SL(3,1) partons",30,50,250,1);
  plot_norm("SLNoBLep","acc","unnorm", "gen", "bestInt", "SL(3,1) partons",30,50,250,1);
  plot_norm("DL",      "unnorm","acc", "gen", "bestInt", "DL(4,N) partons",30,50,250,1);
  plot_norm("SL2wj",   "acc","unnorm", "gen", "bestInt", "SL(4,2) partons",15,50,250,0);
  plot_norm("SL1wj",   "acc","unnorm", "gen", "bestInt", "SL(4,1) partons",15,50,250,0);
  plot_norm("SLNoBHad","acc","unnorm", "gen", "bestInt", "SL(3,1) partons",15,50,250,0);
  plot_norm("SLNoBLep","acc","unnorm", "gen", "bestInt", "SL(3,1) partons",15,50,250,0);
  plot_norm("DL",      "unnorm","acc", "gen", "bestInt", "DL(4,N) partons",15,50,250,0);
  plot_norm("SL2wj",   "acc","unnorm", "rec", "bestInt", "SL(4,2) partons",30,50,250,1);
  plot_norm("SL1wj",   "acc","unnorm", "rec", "bestInt", "SL(4,1) partons",30,50,250,1);
  plot_norm("SLNoBHad","acc","unnorm", "rec", "bestInt", "SL(3,1) partons",30,50,250,1);
  plot_norm("SLNoBLep","acc","unnorm", "rec", "bestInt", "SL(3,1) partons",30,50,250,1);
  plot_norm("DL",      "unnorm","acc", "rec", "bestInt", "DL(4,N) partons",30,50,250,1);
  plot_norm("SL2wj",   "acc","unnorm", "rec", "bestInt", "SL(4,2) partons",15,50,250,0);
  plot_norm("SL1wj",   "acc","unnorm", "rec", "bestInt", "SL(4,1) partons",15,50,250,0);
  plot_norm("SLNoBHad","acc","unnorm", "rec", "bestInt", "SL(3,1) partons",15,50,250,0);
  plot_norm("SLNoBLep","acc","unnorm", "rec", "bestInt", "SL(3,1) partons",15,50,250,0);
  plot_norm("DL",      "unnorm","acc", "rec", "bestInt", "DL(4,N) partons",15,50,250,0);


  plot_genreco_good("SL2wj","acc","SL(4,2)",     30,  60, 250);
  plot_genreco_good("SL1wj","acc","SL(4,1)",     30,  60, 250);
  plot_genreco_good("SLNoBLep","acc","SL(3,2)",  30,  60, 250);
  plot_genreco_good("SLNoBHad","acc","SL(3,2)",  30,  60, 250);
  plot_genreco_good("DL","acc","DL(4,N)",        30,  60, 250);

  plot_genreco_good("SL2wj","unnorm","SL(4,2)",     30,  60, 250);
  plot_genreco_good("SL1wj","unnorm","SL(4,1)",     30,  60, 250);
  plot_genreco_good("SLNoBLep","unnorm","SL(3,2)",  30,  60, 250);
  plot_genreco_good("SLNoBHad","unnorm","SL(3,2)",  30,  60, 250);
  plot_genreco_good("DL","unnorm","DL(4,N)",        30,  60, 250);


  plot_genreco_prob(0, "SL2wj",  "acc",   "bestInt",  "SL(4,2)", 20, 80, 160);
  plot_genreco_prob(1, "SL2wj",  "acc",   "bestInt",  "SL(4,2)", 20, 80, 160);
  plot_genreco_prob(0, "SL2wj",  "unnorm","bestInt",  "SL(4,2)", 25,  0, 100);
  plot_genreco_prob(1, "SL2wj",  "unnorm","bestInt",  "SL(4,2)", 25,  0, 100);

  plot_genreco_prob(0, "SL1wj",  "acc",   "bestInt",  "SL(4,1)", 20, 80, 160);
  plot_genreco_prob(1, "SL1wj",  "acc",   "bestInt",  "SL(4,1)", 20, 80, 160);
  plot_genreco_prob(0, "SL1wj",  "unnorm","bestInt",  "SL(4,1)", 25,  0, 100);
  plot_genreco_prob(1, "SL1wj",  "unnorm","bestInt",  "SL(4,1)", 25,  0, 100);

  plot_genreco_prob(0, "SLNoBHad",  "acc",   "bestInt",  "SL(3,2)", 20, 80, 160);
  plot_genreco_prob(1, "SLNoBHad",  "acc",   "bestInt",  "SL(3,2)", 20, 80, 160);
  plot_genreco_prob(0, "SLNoBHad",  "unnorm","bestInt",  "SL(3,2)", 25,  0, 100);
  plot_genreco_prob(1, "SLNoBHad",  "unnorm","bestInt",  "SL(3,2)", 25,  0, 100);

  plot_genreco_prob(0, "SLNoBLep",  "acc",   "bestInt",  "SL(3,2)", 20, 80, 160);
  plot_genreco_prob(1, "SLNoBLep",  "acc",   "bestInt",  "SL(3,2)", 20, 80, 160);
  plot_genreco_prob(0, "SLNoBLep",  "unnorm","bestInt",  "SL(3,2)", 25,  0, 100);
  plot_genreco_prob(1, "SLNoBLep",  "unnorm","bestInt",  "SL(3,2)", 25,  0, 100);

  plot_genreco_prob(0, "DL",  "acc",   "bestInt",  "DL(4,N)", 20, 80, 160);
  plot_genreco_prob(1, "DL",  "acc",   "bestInt",  "DL(4,N)", 20, 80, 160);
  plot_genreco_prob(0, "DL",  "unnorm","bestInt",  "DL(4,N)", 25,  0, 100);
  plot_genreco_prob(1, "DL",  "unnorm","bestInt",  "DL(4,N)", 25,  0, 100);

  //plot_param("udcsg 0<|#eta|<1.5", "parton E (GeV)",   "#sigma^{j}(E)", "resolLightBin0", 30,  180, 0, 30, "");
  //plot_param("udcsg 1.5<|#eta|<2.5", "parton E (GeV)", "#sigma^{j}(E)", "resolLightBin1", 30,  180, 0, 30, "");
  //plot_param("b-quarks 0<|#eta|<1.5", "parton E (GeV)",   "#sigma^{j}(E)", "resolHeavyBin0", 30,  180, 0, 30, "");
  //plot_param("b-quarks 1.5<|#eta|<2.5", "parton E (GeV)", "#sigma^{j}(E)", "resolHeavyBin1", 30,  180, 0, 30, "");

  //plot_param("udcsg 0<|#eta|<1.5",   "parton E (GeV)", "#mu^{j}(E)", "respLightBin0", 30,  200, 30, 200, "");
  //plot_param("udcsg 1.5<|#eta|<2.5", "parton E (GeV)", "#mu^{j}(E)", "respLightBin1", 30,  200, 30, 180, "");
  //plot_param("b-quarks 0<|#eta|<1.5",   "parton E (GeV)", "#mu^{j}(E)", "respHeavyBin0", 30,  200, 30, 200, "");
  //plot_param("b-quarks 1.5<|#eta|<2.5", "parton E (GeV)", "#mu^{j}(E)", "respHeavyBin1", 30,  200, 30, 200, "");

  //plot_param("E^{miss}_{x,y}", "#sumE_{T} (GeV)",   "#sigma^{MET}_{x,y}", "hWidthsPxResol", 0,  8000, 0, 50, "");

  //plot_param("MET, #sum E_T<1200 (GeV)", "#nu p_{T} (GeV)", "#mu^{#nu_{T}}", "hMeanEt_0", 10,  299, -20, 30, "");
  //plot_param("MET, 1200<#sum E_T<1800 (GeV)", "#nu p_{T} (GeV)", "#mu^{#nu_{T}}", "hMeanEt_1", 10,  299, -20, 30, "");
  //plot_param("MET, 1800<#sum E_T (GeV)", "#nu p_{T} (GeV)", "#mu^{#nu_{T}}", "hMeanEt_2", 10,  299, -20, 30, "");

  //plot_param("MET, #sum E_T<1200 (GeV)", "#nu p_{T} (GeV)", "#sigma^{#nu_{T}}", "hWidthEt_0", 10,  299, 0, 60, "");
  //plot_param("MET, 1200<#sum E_T<1800 (GeV)", "#nu p_{T} (GeV)", "#sigma^{#nu_{T}}", "hWidthEt_1", 10,  299, 0, 60, "");
  //plot_param("MET, 1800<#sum E_T (GeV)", "#nu p_{T} (GeV)", "#sigma^{#nu_{T}}", "hWidthEt_2", 10,  299, 0, 60, "");

  return;

  /*

  plot_BestMass("rec_default_ttjets_largerLR_range", "t#bar{t}+jets", "hBestMassProb", 4);
  */

  //plot_TF1d("gen_default","Light jet TF", "parton E (GeV)","TF(E|#hat{E})","tfWjet1");
  //plot_TF1d("gen_default","Heavy jet TF", "parton E (GeV)","TF(E|#hat{E})","tfbHad");
  //plot_TF1d("gen_default","MET TF", "#nu p_{T} (GeV)","TF(E|#hat{E})","tfMetPt");
  //plot_TF2d("gen_default","MET TF", "#nu p_{T} (GeV)","#phi", "TF(#phi|#hat{#phi},p_{T})","tfMetPhi");

  /*
  plot_TF1d("rec_default","P(M|Y_{good})", "#bar{M} (GeV)","signal","hMass", 1);
  plot_TF1d("rec_default","P(M|Y)", "#bar{M} (GeV)","signal","hMassProb", 1, "_2peak_BAD");
  plot_TF1d("rec_default","P(M|Y)", "#bar{M} (GeV)","signal","hMassProb", 3, "_2peak_GOOD");
  plot_TF1d("rec_default","P(M|Y)", "#bar{M} (GeV)","signal","hMassProb", 4, "_1peak_GOOD");
  plot_TF1d("rec_default","P(M|Y)", "#bar{M} (GeV)","signal","hMassProb", 34,"_3peak_BAD");

  return;

  plot_BestMass("gen_default", "Signal (parton)", "hBestMass");
  plot_BestMass("gen_default", "Signal (parton)", "hBestMassProb");

  plot_BestMass("rec_default", "Signal (nominal res.)", "hBestMass");
  plot_BestMass("rec_default", "Signal (nominal res.)", "hBestMassProb");
  plot_BestMass("rec_METup", "Signal (+50% MET)",      "hBestMassProb");
  plot_BestMass("rec_ScaleLup", "Signal (+50% udcsg)", "hBestMassProb");
  plot_BestMass("rec_ScaleBup", "Signal (+50% b)",     "hBestMassProb");

  plot_BestMass("gen_noJac", "Signal (parton) no Jac.", "hBestMassProb");
  plot_BestMass("gen_noPDF", "Signal (parton) no PDF", "hBestMassProb");
  plot_BestMass("gen_noMET", "Signal (parton) no E_{T}^{miss} TF", "hBestMassProb");
  plot_BestMass("gen_noME",  "Signal (parton) no PS", "hBestMassProb");
  plot_BestMass("gen_noTF",  "Signal (parton) no jet TF", "hBestMassProb");

  plot_BestMass("gen_default_largerLR_range", "Signal (parton) [60,210]", "hBestMassProb");
  plot_BestMass("rec_default_largerLR_range", "Signal (res.) [60,210]", "hBestMassProb");
  */
}
