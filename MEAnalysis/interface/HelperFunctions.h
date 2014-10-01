#ifndef HELPERFUNCTIONS_H // header guards
#define HELPERFUNCTIONS_H

using namespace std;

#include <cassert>
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "TMath.h"
#include "TLorentzVector.h"
#include "TTree.h"
#include "TString.h"

#if not defined(__CINT__) || defined(__MAKECINT__)
#include "TMVA/Reader.h"
#include "TMVA/Tools.h"
#endif

typedef struct 
{
  float et; 
  float sumet;
  float sig;
  float phi;
} metInfo;

typedef struct 
{
  float x1; 
  float x2;
  float pdf;
  float pt;
  float eta;
  float phi;
  float m;
  float me2_ttH;
  float me2_ttbb;

  void reset(){
     x1       = -99.; 
     x2       = -99.;
     pdf      = -99.;
     pt       = -99.;
     eta      = -99.;
     phi      = -99.;
     m        = -99.;
     me2_ttH  = -99.;
     me2_ttbb = -99.;
  };

} tthInfo;


typedef struct 
{
  int run;
  int lumi;
  int event;
  int json;
} EventInfo;
 

typedef struct
{
  TLorentzVector p4;
  float csv;
  int index;
  int flavour;
  float shift;
} JetObservable;

typedef struct
{
 
  TLorentzVector p4[8];

  void fill( vector<TLorentzVector> p4v ){
    for(unsigned int k = 0 ; k < p4v.size() ; k++){
      if(k<8) p4[k] = p4v[k];
    }
  };

  void print( string name ){
    cout << "Phase-space point " << name << ":" << endl;
    for(unsigned int k = 0 ; k < 8 ; k++){
      cout << "(" << p4[k].E() << ", " <<  p4[k].Eta() << ", " <<  p4[k].Phi() << ") " << endl;
    }
  };
  
} PhaseSpacePoint;


bool isSamePSP( PhaseSpacePoint P, PhaseSpacePoint Q, float resolE, float resolDR){

  for(unsigned int k = 0 ; k < 8 ; k++){
    if(  (Q.p4)[k].E()<=0 ){
      //cout << "Negative energy..." << endl;
      return false;    
    }
    
    float dEoE = TMath::Abs( (P.p4)[k].E()- (Q.p4)[k].E() )/ (Q.p4)[k].E();
    float dR   = ( (P.p4)[k] ).DeltaR( (Q.p4)[k] );
    if( dEoE>resolE  || dR > resolDR ){
      //cout << "dE/E(" << k << ") = " << dEoE << ", dR = " << dR << endl;
      return false;
    }
  }
  
  //cout << "It the same PSP!!!" << endl; 
  return true;   
}

struct JetObservableListerByPt
{
  bool operator()( const JetObservable &lx, const JetObservable& rx ) const {
    return (lx.p4).Pt() > (rx.p4).Pt();
  }
};

struct JetObservableListerByCSV
{
  bool operator()( const JetObservable &lx, const JetObservable& rx ) const {
    return (lx.csv) > (rx.csv);
  }
};

struct SorterByPt
{
  bool operator()( const TLorentzVector &lx, const TLorentzVector & rx ) const {
    return lx.Pt() > rx.Pt();
  }
};

typedef struct
{
  float bmass;
  float bpt;
  float beta;
  float bphi;
  float bstatus;
  float wdau1mass;
  float wdau1pt;
  float wdau1eta;
  float wdau1phi;
  float wdau1id;
  float wdau2mass;
  float wdau2pt;
  float wdau2eta;
  float wdau2phi;
  float wdau2id;
} genTopInfo;

typedef struct 
{
  float mass; 
  float pt;
  float eta;
  float phi;
  float status;
  float charge;
  float momid;
} genParticleInfo;


//https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution
float resolutionBias(float eta, int shift, int alreadyCorrect = 0)
{
  if(eta < 0.5){
    if(shift ==  0) 
      return alreadyCorrect ?  0. : 0.052 ;
    if(shift == +1) 
      return 0.115 - resolutionBias(eta, 0 , !alreadyCorrect);  
    if(shift == -1) 
      return 0.010 - resolutionBias(eta, 0 , !alreadyCorrect);  
  }

  if(eta < 1.1){
    if(shift ==  0) 
      return alreadyCorrect ?  0. : 0.057 ;
    if(shift == +1) 
      return 0.114 - resolutionBias(eta, 0 , !alreadyCorrect);  
    if(shift == -1) 
      return 0.001 - resolutionBias(eta, 0 , !alreadyCorrect);  
  }

  if(eta < 1.7){
    if(shift ==  0) 
      return alreadyCorrect ?  0. : 0.096 ;
    if(shift == +1) 
      return 0.161 - resolutionBias(eta, 0 , !alreadyCorrect);  
    if(shift == -1) 
      return 0.032 - resolutionBias(eta, 0 , !alreadyCorrect);  
  }

  if(eta < 2.3){
    if(shift ==  0) 
      return alreadyCorrect ?  0. : 0.134 ;
    if(shift == +1) 
      return 0.228 - resolutionBias(eta, 0 , !alreadyCorrect);  
    if(shift == -1) 
      return 0.042 - resolutionBias(eta, 0 , !alreadyCorrect);  
  }

  if(eta < 5.0){
    if(shift ==  0) 
      return alreadyCorrect ?  0. : 0.288 ;
    if(shift == +1) 
      return 0.488 - resolutionBias(eta, 0 , !alreadyCorrect);  
    if(shift == -1) 
      return 0.089 - resolutionBias(eta, 0 , !alreadyCorrect);  
  }

  return 0.;
}


//SetUp CSV reweighting

void SetUpCSVreweighting( TString path , TFile* f_CSVwgt_HF , TFile* f_CSVwgt_LF,
			  TH1D* h_csv_wgt_hf[9][5],
			  TH1D* c_csv_wgt_hf[5][5],
			  TH1D* h_csv_wgt_lf[9][3][3]){

  // Do not set it up if we're running on collision data

  f_CSVwgt_HF =  TFile::Open( path+"/csv_rwt_hf.root" );
  f_CSVwgt_LF =  TFile::Open( path+"/csv_rwt_lf.root" );

  if( !f_CSVwgt_HF || f_CSVwgt_HF->IsZombie() ) return;
  if( !f_CSVwgt_LF || f_CSVwgt_LF->IsZombie() ) return;

  // CSV reweighting
  for( int iSys=0; iSys<9; iSys++ ){

    TString syst_csv_suffix_hf = "final";
    TString syst_csv_suffix_c  = "final";
    TString syst_csv_suffix_lf = "final";
    
    switch( iSys ){
    case 0:
      // this is the nominal case
      break;
    case 1:
      // JESUp
      syst_csv_suffix_hf = "final_JESUp"; syst_csv_suffix_lf = "final_JESUp";
      syst_csv_suffix_c  = "final_cErr1Up";
      break;
    case 2:
      // JESDown
      syst_csv_suffix_hf = "final_JESDown"; syst_csv_suffix_lf = "final_JESDown";
      syst_csv_suffix_c  = "final_cErr1Down";
      break;
    case 3:
      // purity up
      syst_csv_suffix_hf = "final_LFUp"; syst_csv_suffix_lf = "final_HFUp";
      syst_csv_suffix_c  = "final_cErr2Up";
      break;
    case 4:
      // purity down
      syst_csv_suffix_hf = "final_LFDown"; syst_csv_suffix_lf = "final_HFDown";
      syst_csv_suffix_c  = "final_cErr2Down";
      break;
    case 5:
      // stats1 up
      syst_csv_suffix_hf = "final_Stats1Up"; syst_csv_suffix_lf = "final_Stats1Up";
      break;
    case 6:
      // stats1 down
      syst_csv_suffix_hf = "final_Stats1Down"; syst_csv_suffix_lf = "final_Stats1Down";
      break;
    case 7:
      // stats2 up
      syst_csv_suffix_hf = "final_Stats2Up"; syst_csv_suffix_lf = "final_Stats2Up";
      break;
    case 8:
      // stats2 down
      syst_csv_suffix_hf = "final_Stats2Down"; syst_csv_suffix_lf = "final_Stats2Down";
      break;
    }

    for( int iPt=0; iPt<5; iPt++ ) 
      h_csv_wgt_hf[iSys][iPt] = (TH1D*)f_CSVwgt_HF->Get( Form("csv_ratio_Pt%i_Eta0_%s",iPt,syst_csv_suffix_hf.Data()) );

    if( iSys<5 ){
      for( int iPt=0; iPt<5; iPt++ ) 
	c_csv_wgt_hf[iSys][iPt] = (TH1D*)f_CSVwgt_HF->Get( Form("c_csv_ratio_Pt%i_Eta0_%s",iPt,syst_csv_suffix_c.Data()) );
    }
    
    for( int iPt=0; iPt<3; iPt++ ){
      for( int iEta=0; iEta<3; iEta++ )
	h_csv_wgt_lf[iSys][iPt][iEta] = (TH1D*)f_CSVwgt_LF->Get( Form("csv_ratio_Pt%i_Eta%i_%s",iPt,iEta,syst_csv_suffix_lf.Data()) );
    }
  }

}



enum sysType {
   Nominal = 0,
   JESup,
   JESdown,
   CSVLFup,
   CSVLFdown,
   CSVHFStats1up,
   CSVHFStats1down,
   CSVHFStats2up,
   CSVHFStats2down,
   CSVCErr1up,
   CSVCErr1down,
   CSVCErr2up,
   CSVCErr2down,
   CSVHFup,
   CSVHFdown,
   CSVLFStats1up, 
   CSVLFStats1down,
   CSVLFStats2up,  
   CSVLFStats2down
 };


double GetCSVweight(const std::vector<JetObservable>& iJets, 
		    const sysType iSysType,
		    TH1D* h_csv_wgt_hf[9][5],
		    TH1D* c_csv_wgt_hf[5][5],
		    TH1D* h_csv_wgt_lf[9][3][3]){

  int failure = 0;
  for( int iSys=0; iSys<9; iSys++ ){
    for( int iPt=0; iPt<5; iPt++ ) 
      if( h_csv_wgt_hf[iSys][iPt]==0 ) failure++;
    if( iSys<5 ){
      for( int iPt=0; iPt<5; iPt++ ) 
	if( c_csv_wgt_hf[iSys][iPt] == 0 ) failure++;
    }
    for( int iPt=0; iPt<3; iPt++ ){
      for( int iEta=0; iEta<3; iEta++ )
	if( h_csv_wgt_lf[iSys][iPt][iEta] == 0) failure++;
    }    
  }

  if( failure>0 ) return 1.0;

  int iSysHF = 0;
  switch(iSysType){
  case sysType::JESup:            iSysHF=1; break;
  case sysType::JESdown:         iSysHF=2; break;
  case sysType::CSVLFup:         iSysHF=3; break;
  case sysType::CSVLFdown:       iSysHF=4; break;
  case sysType::CSVHFStats1up:    iSysHF=5; break;
  case sysType::CSVHFStats1down: iSysHF=6; break;
  case sysType::CSVHFStats2up:    iSysHF=7; break;
  case sysType::CSVHFStats2down: iSysHF=8; break;
  default : iSysHF = 0; break;
  }

  int iSysC = 0;
  switch(iSysType){
  case sysType::CSVCErr1up:   iSysC=1; break;
  case sysType::CSVCErr1down: iSysC=2; break;
  case sysType::CSVCErr2up:   iSysC=3; break;
  case sysType::CSVCErr2down: iSysC=4; break;
  default : iSysC = 0; break;
  }

  int iSysLF = 0;
  switch(iSysType){
  case sysType::JESup:            iSysLF=1; break;
  case sysType::JESdown:         iSysLF=2; break;
  case sysType::CSVHFup:         iSysLF=3; break;
  case sysType::CSVHFdown:       iSysLF=4; break;
  case sysType::CSVLFStats1up:    iSysLF=5; break;
  case sysType::CSVLFStats1down: iSysLF=6; break;
  case sysType::CSVLFStats2up:    iSysLF=7; break;
  case sysType::CSVLFStats2down: iSysLF=8; break;
  default : iSysLF = 0; break;
  }

  double csvWgthf = 1.;
  double csvWgtC  = 1.;
  double csvWgtlf = 1.;

  for( std::vector<JetObservable>::const_iterator iJet = iJets.begin(); iJet != iJets.end(); ++iJet ){ 

    double csv       = iJet->csv;
    double jetPt     = (iJet->p4).Pt();
    double jetAbsEta = TMath::Abs( (iJet->p4).Eta() );
    int flavor       = TMath::Abs( iJet->flavour );

    int iPt = -1; int iEta = -1;
    if (jetPt >=24.99 && jetPt<40) iPt = 0;
    else if (jetPt >=40 && jetPt<60) iPt = 1;
    else if (jetPt >=60 && jetPt<100) iPt = 2;
    else if (jetPt >=100 && jetPt<160) iPt = 3;
    else if (jetPt >=160 && jetPt<10000) iPt = 4;

    if (jetAbsEta >=0 &&  jetAbsEta<0.8) iEta = 0;
    else if ( jetAbsEta>=0.8 && jetAbsEta<1.6) iEta = 1;
    else if ( jetAbsEta>=1.6 && jetAbsEta<2.501) iEta = 2;

    if (iPt < 0 || iEta < 0){
      std::cout << "Error, couldn't find Pt, Eta bins for this b-flavor jet, jetPt = " << jetPt << ", jetAbsEta = " << jetAbsEta << std::endl;
      continue;
    }

    if (abs(flavor) == 5 ){
      int useCSVBin = (csv>=0.) ? h_csv_wgt_hf[iSysHF][iPt]->FindBin(csv) : 1;
      double iCSVWgtHF = h_csv_wgt_hf[iSysHF][iPt]->GetBinContent(useCSVBin);
      if( iCSVWgtHF!=0 ) csvWgthf *= iCSVWgtHF;

    }
    else if( abs(flavor) == 4 ){
      int useCSVBin = (csv>=0.) ? c_csv_wgt_hf[iSysC][iPt]->FindBin(csv) : 1;
      double iCSVWgtC = c_csv_wgt_hf[iSysC][iPt]->GetBinContent(useCSVBin);
      if( iCSVWgtC!=0 ) csvWgtC *= iCSVWgtC;

    }
    else {
      if (iPt >=2) iPt=2;       /// [30-40], [40-60] and [60-10000] only 3 Pt bins for lf
      int useCSVBin    = (csv>=0.) ? h_csv_wgt_lf[iSysLF][iPt][iEta]->FindBin(csv) : 1;
      double iCSVWgtLF = h_csv_wgt_lf[iSysLF][iPt][iEta]->GetBinContent(useCSVBin);
      if( iCSVWgtLF!=0 ) csvWgtlf *= iCSVWgtLF;


    }
  }


  double csvWgtTotal = csvWgthf * csvWgtC * csvWgtlf;

  return TMath::Max(csvWgtTotal,0.);
}








std::vector<std::string> GetInputExpressionsReg() {
    std::vector<std::string> values;
    values.resize(12, "");
    //values[0] = "breg_rawptJER := smear_pt_res(hJet_ptRaw, hJet_genPt, hJet_eta)";
    values[0] = "breg_pt := hJet_pt";
    values[1] = "breg_et := evalEt(hJet_pt, hJet_eta, hJet_phi, hJet_e)";
    values[2] = "breg_mt := evalMt(hJet_pt, hJet_eta, hJet_phi, hJet_e)";
    //values[4] = "breg_leadtrackpt := max(0,hJet_ptLeadTrack)";
    values[3] = "breg_vtx3dL := max(0,hJet_vtx3dL)";
    values[4] = "breg_vtx3deL := max(0,hJet_vtx3deL)";
    values[5] = "breg_vtxMass := max(0,hJet_vtxMass)";
    //values[8] = "breg_vtxPt := max(0,hJet_vtxPt)";
    values[6] = "breg_cef := hJet_cef";
    values[7] = "breg_ntot := hJet_nconstituents";
    values[8] = "breg_eJEC := hJet_JECUnc";
    values[9] = "breg_softlepptrel := max(0,hJet_SoftLeptptRel*(hJet_SoftLeptIdlooseMu==1 || hJet_SoftLeptId95==1))";
    values[10]= "breg_softleppt := max(0,hJet_SoftLeptPt*(hJet_SoftLeptIdlooseMu==1 || hJet_SoftLeptId95==1))";
    values[11]= "breg_softlepdR := max(0,hJet_SoftLeptdR*(hJet_SoftLeptIdlooseMu==1 || hJet_SoftLeptId95==1))";
    return values;
}

double quadsum(double a, double b)
{
    return TMath::Sqrt(a*a + b*b);
}

float smear_pt_res(float pt, float genpt, float eta)
{
    eta = fabs(eta);

    if (genpt>15. && (fabs(pt - genpt) / pt)<0.5) {  // limit the effect to the core

        double res    = 1.0;

        if (eta <= 0.5) {
            res    = 1.052;
        } else if (0.5 < eta && eta <= 1.1) {
            res    = 1.057;
        } else if (1.1 < eta && eta <= 1.7) {
            res    = 1.096;
        } else if (1.7 < eta && eta <= 2.3) {
            res    = 1.134;
        } else {
            res    = 1.288;
        }

        float deltapt = (pt - genpt) * res;
        return TMath::Max(float(0.), genpt + deltapt);
    }
    return pt;
}

double evalEt(double pt, double eta, double phi, double e)
{
    TLorentzVector j;
    j.SetPtEtaPhiE(pt, eta, phi, e);
    return j.Et();
}

double evalMt(double pt, double eta, double phi, double e)
{
    TLorentzVector j;
    j.SetPtEtaPhiE(pt, eta, phi, e);
    return j.Mt();
}


TMVA::Reader* getTMVAReader( std::string pathtofile, std::string target, std::string regMethod , Float_t readerVars[12]){

  TMVA::Tools::Instance(); 
  TMVA::Reader *reader = new TMVA::Reader("!Color:!Silent");

  const std::vector<std::string>& inputExpressionsReg = GetInputExpressionsReg();
  const UInt_t nvars = inputExpressionsReg.size();

  for (UInt_t iexpr = 0; iexpr < nvars; iexpr++) {
    const TString& expr = inputExpressionsReg.at(iexpr);
    reader->AddVariable(expr, &readerVars[iexpr]);
  }

  TString weightdir(pathtofile.c_str());
  TString weightfile = weightdir + "TMVARegression_" + target + "_" + regMethod + ".weights.xml";
  reader->BookMVA(regMethod + " method", weightfile);

  cout << "*** getTMVAReader has ben called ***" << endl;
  cout << " => A regression of type " << regMethod << " will be used. Reading data file from " <<
    string(weightfile.Data()) << endl;
  cout << " => Total of " << nvars << " variables used as input" << endl;

  return reader;
}

void getRegressionEnergy(float& output, std::string regMethod, 
			 TMVA::Reader *reader, Float_t readerVars[12], 
			 TTree* tree, Long64_t entry , int jetpos, float shift,
			 int verbose){

  TString jetColl =  "h" ;
  int j = jetpos>=0 ? jetpos : -jetpos-1;

  float hJet_pt[2],         hJet_genPt[2],         //hJet_ptRaw[2],        
    hJet_eta[2],  hJet_phi[2],    hJet_e[2], hJet_JECUnc[2];
  float hJet_vtx3dL[2],     hJet_vtx3deL[2],       hJet_vtxMass[2]   // hJet_vtxPt[2]
    ;
  float hJet_cef[2],        //hJet_ptLeadTrack[2],   
    hJet_nconstituents[2];
  float hJet_SoftLeptPt[2], hJet_SoftLeptptRel[2], hJet_SoftLeptdR[2];
  int hJet_SoftLeptIdlooseMu[2], hJet_SoftLeptId95[2];

  float aJet_pt[999],         aJet_genPt[999],         //aJet_ptRaw[999],
    aJet_eta[999],  aJet_phi[999],    aJet_e[999], aJet_JECUnc[999];
  float aJet_vtx3dL[999],     aJet_vtx3deL[999],       aJet_vtxMass[999]      //aJet_vtxPt[999]
    ;
  float aJet_cef[999],        //aJet_ptLeadTrack[999], 
    aJet_nconstituents[999];
  float aJet_SoftLeptPt[999], aJet_SoftLeptptRel[999], aJet_SoftLeptdR[999];
  int   aJet_SoftLeptIdlooseMu[999], aJet_SoftLeptId95[999];

  if(jetpos>=0){
    jetColl =  "h" ;
    tree->SetBranchAddress(jetColl+"Jet_pt",      hJet_pt);
    tree->SetBranchAddress(jetColl+"Jet_genPt",   hJet_genPt);
    //tree->SetBranchAddress(jetColl+"Jet_ptRaw",   hJet_ptRaw);
    tree->SetBranchAddress(jetColl+"Jet_eta",     hJet_eta);
    tree->SetBranchAddress(jetColl+"Jet_phi",     hJet_phi);
    tree->SetBranchAddress(jetColl+"Jet_e",       hJet_e);
    tree->SetBranchAddress(jetColl+"Jet_JECUnc",  hJet_JECUnc);
    tree->SetBranchAddress(jetColl+"Jet_vtx3dL",  hJet_vtx3dL );
    tree->SetBranchAddress(jetColl+"Jet_vtx3deL", hJet_vtx3deL);
    tree->SetBranchAddress(jetColl+"Jet_vtxMass", hJet_vtxMass);
    //tree->SetBranchAddress(jetColl+"Jet_vtxPt",   hJet_vtxPt);
    tree->SetBranchAddress(jetColl+"Jet_cef",           hJet_cef);
    //tree->SetBranchAddress(jetColl+"Jet_ptLeadTrack",   hJet_ptLeadTrack  );
    tree->SetBranchAddress(jetColl+"Jet_nconstituents", hJet_nconstituents);
    tree->SetBranchAddress(jetColl+"Jet_SoftLeptPt",        hJet_SoftLeptPt);
    tree->SetBranchAddress(jetColl+"Jet_SoftLeptptRel",     hJet_SoftLeptptRel);
    tree->SetBranchAddress(jetColl+"Jet_SoftLeptdR",        hJet_SoftLeptdR);
    tree->SetBranchAddress(jetColl+"Jet_SoftLeptIdlooseMu", hJet_SoftLeptIdlooseMu );
    tree->SetBranchAddress(jetColl+"Jet_SoftLeptId95",      hJet_SoftLeptId95);
  }
  else{
    jetColl =  "a" ;
    tree->SetBranchAddress(jetColl+"Jet_pt",      aJet_pt);
    tree->SetBranchAddress(jetColl+"Jet_genPt",   aJet_genPt);
    //tree->SetBranchAddress(jetColl+"Jet_ptRaw",   aJet_ptRaw);
    tree->SetBranchAddress(jetColl+"Jet_eta",     aJet_eta);
    tree->SetBranchAddress(jetColl+"Jet_phi",     aJet_phi);
    tree->SetBranchAddress(jetColl+"Jet_e",       aJet_e);
    tree->SetBranchAddress(jetColl+"Jet_JECUnc",  aJet_JECUnc);
    tree->SetBranchAddress(jetColl+"Jet_vtx3dL",  aJet_vtx3dL );
    tree->SetBranchAddress(jetColl+"Jet_vtx3deL", aJet_vtx3deL);
    tree->SetBranchAddress(jetColl+"Jet_vtxMass", aJet_vtxMass);
    //tree->SetBranchAddress(jetColl+"Jet_vtxPt",   aJet_vtxPt);
    tree->SetBranchAddress(jetColl+"Jet_cef",           aJet_cef);
    //tree->SetBranchAddress(jetColl+"Jet_ptLeadTrack",   aJet_ptLeadTrack  );
    tree->SetBranchAddress(jetColl+"Jet_nconstituents", aJet_nconstituents);
    tree->SetBranchAddress(jetColl+"Jet_SoftLeptPt",        aJet_SoftLeptPt);
    tree->SetBranchAddress(jetColl+"Jet_SoftLeptptRel",     aJet_SoftLeptptRel);
    tree->SetBranchAddress(jetColl+"Jet_SoftLeptdR",        aJet_SoftLeptdR);
    tree->SetBranchAddress(jetColl+"Jet_SoftLeptIdlooseMu", aJet_SoftLeptIdlooseMu );
    tree->SetBranchAddress(jetColl+"Jet_SoftLeptId95",      aJet_SoftLeptId95);
  }

  tree->GetEntry(entry);

  // fill the input variables
  //readerVars[0]  = jetpos>=0 ? 
  //smear_pt_res( hJet_ptRaw[j], hJet_genPt[j], hJet_eta[j]) : 
  //smear_pt_res( aJet_ptRaw[j], aJet_genPt[j], aJet_eta[j]);

  readerVars[0]  = jetpos>=0 ? 
    hJet_pt[j]*shift : 
    aJet_pt[j]*shift;

  readerVars[1]  = jetpos>=0 ? 
    evalEt( hJet_pt[j]*shift, hJet_eta[j], hJet_phi[j], hJet_e[j]*shift) : 
    evalEt( aJet_pt[j]*shift, aJet_eta[j], aJet_phi[j], aJet_e[j]*shift);

  readerVars[2]  = jetpos>=0 ? 
    evalMt( hJet_pt[j]*shift, hJet_eta[j], hJet_phi[j], hJet_e[j]*shift) : 
    evalMt( aJet_pt[j]*shift, aJet_eta[j], aJet_phi[j], aJet_e[j]*shift);

  //readerVars[4]  = jetpos>=0 ? 
  //TMath::Max(float(0.), hJet_ptLeadTrack[j] ) : 
  //TMath::Max(float(0.), aJet_ptLeadTrack[j] );

  readerVars[3]  = jetpos>=0 ?
    TMath::Max(float(0.), hJet_vtx3dL[j] )  :
    TMath::Max(float(0.), aJet_vtx3dL[j] );

  readerVars[4]  = jetpos>=0 ? 
    TMath::Max(float(0.), hJet_vtx3deL[j] ) : 
    TMath::Max(float(0.), aJet_vtx3deL[j] );

  readerVars[5]  = jetpos>=0 ? 
    TMath::Max(float(0.), hJet_vtxMass[j] ) : 
    TMath::Max(float(0.), aJet_vtxMass[j] );

  //readerVars[8]  = jetpos>=0 ? 
  //TMath::Max(float(0.), hJet_vtxPt[j] )   : 
  //TMath::Max(float(0.), aJet_vtxPt[j] );

  readerVars[6]  = jetpos>=0 ? 
    hJet_cef[j] :  
    aJet_cef[j];

  readerVars[7] = jetpos>=0 ? 
    hJet_nconstituents[j] : 
    aJet_nconstituents[j];

  readerVars[8] = jetpos>=0 ?
    hJet_JECUnc[j] : 
    aJet_JECUnc[j];

  readerVars[9] = jetpos>=0 ? 
    TMath::Max(float(0.), hJet_SoftLeptptRel[j]*(hJet_SoftLeptIdlooseMu[j]==1 || hJet_SoftLeptId95[j]==1)) :
    TMath::Max(float(0.), aJet_SoftLeptptRel[j]*(aJet_SoftLeptIdlooseMu[j]==1 || aJet_SoftLeptId95[j]==1));

  readerVars[10] = jetpos>=0 ? 
    TMath::Max(float(0.), hJet_SoftLeptPt[j]*   (hJet_SoftLeptIdlooseMu[j]==1 || hJet_SoftLeptId95[j]==1)) :
    TMath::Max(float(0.), aJet_SoftLeptPt[j]*   (aJet_SoftLeptIdlooseMu[j]==1 || aJet_SoftLeptId95[j]==1));

  readerVars[11] = jetpos>=0 ? 
    TMath::Max(float(0.), hJet_SoftLeptdR[j]*   (hJet_SoftLeptIdlooseMu[j]==1 || hJet_SoftLeptId95[j]==1)) :
    TMath::Max(float(0.), aJet_SoftLeptdR[j]*   (aJet_SoftLeptIdlooseMu[j]==1 || aJet_SoftLeptId95[j]==1));

  output = reader!=0 ? (reader->EvaluateRegression(regMethod+" method"))[0] : -99.;

  if(verbose){
    cout << ">>> Regression" << endl;
    cout << "   --> input:" << endl;
    for(int k = 0 ; k < 12 ; k++){
      cout << "        -> " << "readerVars[" << k << "] = " <<  readerVars[k] << endl;
    }
    cout << "    --> output = " << output << endl;
  }

}





void addRegressionBranchesPerJet( TTree* tree, Float_t readerVarsF[14], Int_t readerVarsI[2]){

  TString jetColl = "h" ;

  tree->Branch(jetColl+"Jet_pt", &(readerVarsF[0]) ,              jetColl+"Jet_pt/F");     
  tree->Branch(jetColl+"Jet_genPt", &(readerVarsF[1]) ,           jetColl+"Jet_genPt/F");  
  //tree->Branch(jetColl+"Jet_ptRaw", &(readerVarsF[2]) ,         jetColl+"Jet_ptRaw/F");  
  tree->Branch(jetColl+"Jet_eta", &(readerVarsF[2]) ,             jetColl+"Jet_eta/F");    
  tree->Branch(jetColl+"Jet_phi", &(readerVarsF[3]) ,             jetColl+"Jet_phi/F");    
  tree->Branch(jetColl+"Jet_e", &(readerVarsF[4]) ,               jetColl+"Jet_e/F");      
  tree->Branch(jetColl+"Jet_JECUnc", &(readerVarsF[5]) ,          jetColl+"Jet_JECUnc/F"); 
  tree->Branch(jetColl+"Jet_vtx3dL", &(readerVarsF[6]) ,          jetColl+"Jet_vtx3dL/F"); 
  tree->Branch(jetColl+"Jet_vtx3deL", &(readerVarsF[7]) ,         jetColl+"Jet_vtx3deL/F");
  tree->Branch(jetColl+"Jet_vtxMass", &(readerVarsF[8]) ,         jetColl+"Jet_vtxMass/F");
  //tree->Branch(jetColl+"Jet_vtxPt", &(readerVarsF[10]) ,         jetColl+"Jet_vtxPt/F");  
  tree->Branch(jetColl+"Jet_cef", &(readerVarsF[9]) ,             jetColl+"Jet_cef/F");           
  //tree->Branch(jetColl+"Jet_ptLeadTrack", &(readerVarsF[12]) ,   jetColl+"Jet_ptLeadTrack/F");   
  tree->Branch(jetColl+"Jet_nconstituents", &(readerVarsF[10]) ,  jetColl+"Jet_nconstituents/F"); 
  tree->Branch(jetColl+"Jet_SoftLeptPt", &(readerVarsF[11]) ,     jetColl+"Jet_SoftLeptPt/F");        
  tree->Branch(jetColl+"Jet_SoftLeptptRel", &(readerVarsF[12]) ,  jetColl+"Jet_SoftLeptptRel/F");     
  tree->Branch(jetColl+"Jet_SoftLeptdR", &(readerVarsF[13]) ,     jetColl+"Jet_SoftLeptdR/F");        
  tree->Branch(jetColl+"Jet_SoftLeptIdlooseMu", &(readerVarsI[0]),jetColl+"Jet_SoftLeptIdlooseMu/I"); 
  tree->Branch(jetColl+"Jet_SoftLeptId95", &(readerVarsI[1]) ,    jetColl+"Jet_SoftLeptId95/I");      
   

}

void fillRegressionBranchesPerJet( Float_t readerVarsF[14], 
				   Int_t readerVarsI[2], 
				   TTree* tree, Long64_t entry , 
				   int jetpos, int verbose){

  float hJet_pt[2],         hJet_genPt[2],         //hJet_ptRaw[2], 
    hJet_eta[2],  hJet_phi[2],    hJet_e[2], hJet_JECUnc[2];
  float hJet_vtx3dL[2],     hJet_vtx3deL[2],       hJet_vtxMass[2]     //hJet_vtxPt[2]
    ;
  float hJet_cef[2],        //hJet_ptLeadTrack[2],  
    hJet_nconstituents[2];
  float hJet_SoftLeptPt[2], hJet_SoftLeptptRel[2], hJet_SoftLeptdR[2];
  int hJet_SoftLeptIdlooseMu[2], hJet_SoftLeptId95[2];

  float aJet_pt[999],         aJet_genPt[999],         //aJet_ptRaw[999],
    aJet_eta[999],  aJet_phi[999],    aJet_e[999], aJet_JECUnc[999];
  float aJet_vtx3dL[999],     aJet_vtx3deL[999],       aJet_vtxMass[999]      //aJet_vtxPt[999]
    ;
  float aJet_cef[999],        //aJet_ptLeadTrack[999],   
    aJet_nconstituents[999];
  float aJet_SoftLeptPt[999], aJet_SoftLeptptRel[999], aJet_SoftLeptdR[999];
  int aJet_SoftLeptIdlooseMu[999], aJet_SoftLeptId95[999];

  //TString jetColl = jetpos>=0 ? "h": "a"; // : "a";
  int j      = jetpos>=0 ? jetpos : -jetpos-1;

  TString jetColl = "h";
  tree->SetBranchAddress(jetColl+"Jet_pt",      hJet_pt);
  tree->SetBranchAddress(jetColl+"Jet_genPt",   hJet_genPt);
  //tree->SetBranchAddress(jetColl+"Jet_ptRaw",   hJet_ptRaw);
  tree->SetBranchAddress(jetColl+"Jet_eta",     hJet_eta);
  tree->SetBranchAddress(jetColl+"Jet_phi",     hJet_phi);
  tree->SetBranchAddress(jetColl+"Jet_e",       hJet_e);
  tree->SetBranchAddress(jetColl+"Jet_JECUnc",  hJet_JECUnc);
  tree->SetBranchAddress(jetColl+"Jet_vtx3dL",  hJet_vtx3dL );
  tree->SetBranchAddress(jetColl+"Jet_vtx3deL", hJet_vtx3deL);
  tree->SetBranchAddress(jetColl+"Jet_vtxMass", hJet_vtxMass);
  //tree->SetBranchAddress(jetColl+"Jet_vtxPt",   hJet_vtxPt);
  tree->SetBranchAddress(jetColl+"Jet_cef",           hJet_cef);
  //tree->SetBranchAddress(jetColl+"Jet_ptLeadTrack",   hJet_ptLeadTrack  );
  tree->SetBranchAddress(jetColl+"Jet_nconstituents", hJet_nconstituents);
  tree->SetBranchAddress(jetColl+"Jet_SoftLeptPt",        hJet_SoftLeptPt);
  tree->SetBranchAddress(jetColl+"Jet_SoftLeptptRel",     hJet_SoftLeptptRel);
  tree->SetBranchAddress(jetColl+"Jet_SoftLeptdR",        hJet_SoftLeptdR);
  tree->SetBranchAddress(jetColl+"Jet_SoftLeptIdlooseMu", hJet_SoftLeptIdlooseMu );
  tree->SetBranchAddress(jetColl+"Jet_SoftLeptId95",      hJet_SoftLeptId95);
 
  jetColl = "a";
  tree->SetBranchAddress(jetColl+"Jet_pt",      aJet_pt);
  tree->SetBranchAddress(jetColl+"Jet_genPt",   aJet_genPt);
  //tree->SetBranchAddress(jetColl+"Jet_ptRaw",   aJet_ptRaw);
  tree->SetBranchAddress(jetColl+"Jet_eta",     aJet_eta);
  tree->SetBranchAddress(jetColl+"Jet_phi",     aJet_phi);
  tree->SetBranchAddress(jetColl+"Jet_e",       aJet_e);
  tree->SetBranchAddress(jetColl+"Jet_JECUnc",  aJet_JECUnc);
  tree->SetBranchAddress(jetColl+"Jet_vtx3dL",  aJet_vtx3dL );
  tree->SetBranchAddress(jetColl+"Jet_vtx3deL", aJet_vtx3deL);
  tree->SetBranchAddress(jetColl+"Jet_vtxMass", aJet_vtxMass);
  //tree->SetBranchAddress(jetColl+"Jet_vtxPt",   aJet_vtxPt);
  tree->SetBranchAddress(jetColl+"Jet_cef",           aJet_cef);
  //tree->SetBranchAddress(jetColl+"Jet_ptLeadTrack",   aJet_ptLeadTrack  );
  tree->SetBranchAddress(jetColl+"Jet_nconstituents", aJet_nconstituents);
  tree->SetBranchAddress(jetColl+"Jet_SoftLeptPt",        aJet_SoftLeptPt);
  tree->SetBranchAddress(jetColl+"Jet_SoftLeptptRel",     aJet_SoftLeptptRel);
  tree->SetBranchAddress(jetColl+"Jet_SoftLeptdR",        aJet_SoftLeptdR);
  tree->SetBranchAddress(jetColl+"Jet_SoftLeptIdlooseMu", aJet_SoftLeptIdlooseMu );
  tree->SetBranchAddress(jetColl+"Jet_SoftLeptId95",      aJet_SoftLeptId95);
 

  tree->GetEntry(entry);

  readerVarsF[0]  = jetpos>=0 ? hJet_pt[j] :  aJet_pt[j] ;
  readerVarsF[1]  = jetpos>=0 ? hJet_genPt[j] : aJet_genPt[j]  ;
  //readerVarsF[2]  = Jet_ptRaw[j] : ;
  readerVarsF[2]  = jetpos>=0 ? hJet_eta[j] :  aJet_eta[j];
  readerVarsF[3]  = jetpos>=0 ? hJet_phi[j] : aJet_phi[j];
  readerVarsF[4]  = jetpos>=0 ? hJet_e[j] :   aJet_e[j];
  readerVarsF[5]  = jetpos>=0 ? hJet_JECUnc[j] : aJet_JECUnc[j];
  readerVarsF[6]  = jetpos>=0 ? hJet_vtx3dL [j] : aJet_vtx3dL [j] ;
  readerVarsF[7]  = jetpos>=0 ? hJet_vtx3deL[j] : aJet_vtx3deL[j];
  readerVarsF[8]  = jetpos>=0 ? hJet_vtxMass[j] : aJet_vtxMass[j] ;
  //readerVarsF[10] = Jet_vtxPt[j] : ;
  readerVarsF[9] = jetpos>=0 ? hJet_cef[j] : aJet_cef[j];
  //readerVarsF[12] = Jet_ptLeadTrack[j] : ;
  readerVarsF[10] = jetpos>=0 ? hJet_nconstituents[j] : aJet_nconstituents[j];
  readerVarsF[11] = jetpos>=0 ? hJet_SoftLeptPt[j] :    aJet_SoftLeptPt[j];
  readerVarsF[12] = jetpos>=0 ? hJet_SoftLeptptRel[j] :  aJet_SoftLeptptRel[j];
  readerVarsF[13] = jetpos>=0 ? hJet_SoftLeptdR[j] : aJet_SoftLeptdR[j];
  readerVarsI[0]  = jetpos>=0 ? hJet_SoftLeptIdlooseMu[j] : aJet_SoftLeptIdlooseMu[j];
  readerVarsI[1]  = jetpos>=0 ? hJet_SoftLeptId95[j] : aJet_SoftLeptId95[j];
 
  if(verbose){
    cout << "j = " << j << ", jetColl = " << string(jetColl.Data()) << endl;
    cout << "   --> input:" << endl;
    for(int k = 0 ; k < 14 ; k++){
      cout << "        -> " << "readerVarsF[" << k << "] = " <<  readerVarsF[k] << endl;
    }
    for(int k = 0 ; k < 2 ; k++){
      cout << "        -> " << "readerVarsI[" << k << "] = " <<  readerVarsI[k] << endl;
    }
  }

}

float eleSF(float pt, float eta){
  if (pt >= 20.0 && pt < 25.0 && eta < -1.57000005245 && eta > -2.5) return 0.955429255962 ;
  if (pt >= 20.0 && pt < 25.0 && eta < -1.44000005722 && eta > -1.57000005245) return 0.927380621433 ;
  if (pt >= 20.0 && pt < 25.0 && eta < -0.800000011921 && eta > -1.44000005722) return 0.752811849117 ;
  if (pt >= 20.0 && pt < 25.0 && eta < 0.0 && eta > -0.800000011921) return 0.758898377419 ;
  if (pt >= 20.0 && pt < 25.0 && eta < 0.800000011921 && eta > 0.0) return 0.755395233631 ;
  if (pt >= 20.0 && pt < 25.0 && eta < 1.44000005722 && eta > 0.800000011921) return 0.765102207661 ;
  if (pt >= 20.0 && pt < 25.0 && eta < 1.57000005245 && eta > 1.44000005722) return 0.889689266682 ;
  if (pt >= 20.0 && pt < 25.0 && eta < 2.5 && eta > 1.57000005245) return 0.960859179497 ;
  if (pt >= 25.0 && pt < 30.0 && eta < -1.57000005245 && eta > -2.5) return 0.973749041557 ;
  if (pt >= 25.0 && pt < 30.0 && eta < -1.44000005722 && eta > -1.57000005245) return 0.95562505722 ;
  if (pt >= 25.0 && pt < 30.0 && eta < -0.800000011921 && eta > -1.44000005722) return 0.854979991913 ;
  if (pt >= 25.0 && pt < 30.0 && eta < 0.0 && eta > -0.800000011921) return 0.859907507896 ;
  if (pt >= 25.0 && pt < 30.0 && eta < 0.800000011921 && eta > 0.0) return 0.856850981712 ;
  if (pt >= 25.0 && pt < 30.0 && eta < 1.44000005722 && eta > 0.800000011921) return 0.854210674763 ;
  if (pt >= 25.0 && pt < 30.0 && eta < 1.57000005245 && eta > 1.44000005722) return 0.961790204048 ;
  if (pt >= 25.0 && pt < 30.0 && eta < 2.5 && eta > 1.57000005245) return 0.984032571316 ;
  if (pt >= 30.0 && pt < 35.0 && eta < -1.57000005245 && eta > -2.5) return 0.975343048573 ;
  if (pt >= 30.0 && pt < 35.0 && eta < -1.44000005722 && eta > -1.57000005245) return 0.971944391727 ;
  if (pt >= 30.0 && pt < 35.0 && eta < -0.800000011921 && eta > -1.44000005722) return 0.916224777699 ;
  if (pt >= 30.0 && pt < 35.0 && eta < 0.0 && eta > -0.800000011921) return 0.918354153633 ;
  if (pt >= 30.0 && pt < 35.0 && eta < 0.800000011921 && eta > 0.0) return 0.914323210716 ;
  if (pt >= 30.0 && pt < 35.0 && eta < 1.44000005722 && eta > 0.800000011921) return 0.918937265873 ;
  if (pt >= 30.0 && pt < 35.0 && eta < 1.57000005245 && eta > 1.44000005722) return 0.949005782604 ;
  if (pt >= 30.0 && pt < 35.0 && eta < 2.5 && eta > 1.57000005245) return 0.978435099125 ;
  if (pt >= 35.0 && pt < 40.0 && eta < -1.57000005245 && eta > -2.5) return 0.977416038513 ;
  if (pt >= 35.0 && pt < 40.0 && eta < -1.44000005722 && eta > -1.57000005245) return 0.96676659584 ;
  if (pt >= 35.0 && pt < 40.0 && eta < -0.800000011921 && eta > -1.44000005722) return 0.949674129486 ;
  if (pt >= 35.0 && pt < 40.0 && eta < 0.0 && eta > -0.800000011921) return 0.955099225044 ;
  if (pt >= 35.0 && pt < 40.0 && eta < 0.800000011921 && eta > 0.0) return 0.95435655117 ;
  if (pt >= 35.0 && pt < 40.0 && eta < 1.44000005722 && eta > 0.800000011921) return 0.949129760265 ;
  if (pt >= 35.0 && pt < 40.0 && eta < 1.57000005245 && eta > 1.44000005722) return 0.966977357864 ;
  if (pt >= 35.0 && pt < 40.0 && eta < 2.5 && eta > 1.57000005245) return 0.974912643433 ;
  if (pt >= 40.0 && pt < 45.0 && eta < -1.57000005245 && eta > -2.5) return 0.976379692554 ;
  if (pt >= 40.0 && pt < 45.0 && eta < -1.44000005722 && eta > -1.57000005245) return 0.96400809288 ;
  if (pt >= 40.0 && pt < 45.0 && eta < -0.800000011921 && eta > -1.44000005722) return 0.967367231846 ;
  if (pt >= 40.0 && pt < 45.0 && eta < 0.0 && eta > -0.800000011921) return 0.976113498211 ;
  if (pt >= 40.0 && pt < 45.0 && eta < 0.800000011921 && eta > 0.0) return 0.970276534557 ;
  if (pt >= 40.0 && pt < 45.0 && eta < 1.44000005722 && eta > 0.800000011921) return 0.965076506138 ;
  if (pt >= 40.0 && pt < 45.0 && eta < 1.57000005245 && eta > 1.44000005722) return 0.962332487106 ;
  if (pt >= 40.0 && pt < 45.0 && eta < 2.5 && eta > 1.57000005245) return 0.975438177586 ;
  if (pt >= 45.0 && pt < 50.0 && eta < -1.57000005245 && eta > -2.5) return 0.974642693996 ;
  if (pt >= 45.0 && pt < 50.0 && eta < -1.44000005722 && eta > -1.57000005245) return 0.976564764977 ;
  if (pt >= 45.0 && pt < 50.0 && eta < -0.800000011921 && eta > -1.44000005722) return 0.975869596004 ;
  if (pt >= 45.0 && pt < 50.0 && eta < 0.0 && eta > -0.800000011921) return 0.984652400017 ;
  if (pt >= 45.0 && pt < 50.0 && eta < 0.800000011921 && eta > 0.0) return 0.976347208023 ;
  if (pt >= 45.0 && pt < 50.0 && eta < 1.44000005722 && eta > 0.800000011921) return 0.974825322628 ;
  if (pt >= 45.0 && pt < 50.0 && eta < 1.57000005245 && eta > 1.44000005722) return 0.968582391739 ;
  if (pt >= 45.0 && pt < 50.0 && eta < 2.5 && eta > 1.57000005245) return 0.973198652267 ;
  if (pt >= 50.0 && pt < 200.0 && eta < -1.57000005245 && eta > -2.5) return 0.976521909237 ;
  if (pt >= 50.0 && pt < 200.0 && eta < -1.44000005722 && eta > -1.57000005245) return 0.968289792538 ;
  if (pt >= 50.0 && pt < 200.0 && eta < -0.800000011921 && eta > -1.44000005722) return 0.980251729488 ;
  if (pt >= 50.0 && pt < 200.0 && eta < 0.0 && eta > -0.800000011921) return 0.988307952881 ;
  if (pt >= 50.0 && pt < 200.0 && eta < 0.800000011921 && eta > 0.0) return 0.983105957508 ;
  if (pt >= 50.0 && pt < 200.0 && eta < 1.44000005722 && eta > 0.800000011921) return 0.976873219013 ;
  if (pt >= 50.0 && pt < 200.0 && eta < 1.57000005245 && eta > 1.44000005722) return 0.970499277115 ;
  if (pt >= 50.0 && pt < 200.0 && eta < 2.5 && eta > 1.57000005245) return 0.972752988338 ;
  return 1.;
}


float weightError( TTree* tree, float pt, float eta, float& scale_){

  float err = 0.;

  float  ptMin, ptMax, etaMin, etaMax, scale, error;
  tree->SetBranchAddress("ptMin",  &ptMin);
  tree->SetBranchAddress("ptMax",  &ptMax);
  tree->SetBranchAddress("etaMin", &etaMin);
  tree->SetBranchAddress("etaMax", &etaMax);
  tree->SetBranchAddress("scale",  &scale);
  tree->SetBranchAddress("error",  &error);

  Long64_t nentries = tree->GetEntries();
  for( Long64_t i = 0; i < nentries ; i++ ){
    tree->GetEntry(i);
    float pt_eq = TMath::Min( pt, float(199.9) );
    if( pt_eq>=ptMin && pt_eq<ptMax && eta>=etaMin && eta<etaMax ) {
      err    = scale>0 ? error/scale : 0.; 
      scale_ = scale;
    }
  }

  return err;

}

#endif
