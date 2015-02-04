#ifndef HELPERFUNCTIONS_H // header guards
#define HELPERFUNCTIONS_H

using namespace std;

#include <cassert>
#include <cstdlib>
#include <iostream>
#include <memory>
#include <map>
#include <string>
#include <vector>

#include "TMath.h"
#include "TFile.h"
#include "TLorentzVector.h"
#include "TTree.h"
#include "TString.h"
#include "TH1F.h"

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


bool isSamePSP( PhaseSpacePoint P, PhaseSpacePoint Q, float resolE, float resolDR);

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
float resolutionBias(float eta, int shift, int alreadyCorrect);


//SetUp CSV reweighting

void SetUpCSVreweighting( TString path , TFile* f_CSVwgt_HF , TFile* f_CSVwgt_LF,
			  TH1D* h_csv_wgt_hf[9][5],
			  TH1D* c_csv_wgt_hf[5][5],
			  TH1D* h_csv_wgt_lf[9][3][3]);



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
		    TH1D* h_csv_wgt_lf[9][3][3]);

std::vector<std::string> GetInputExpressionsReg();

double quadsum(double a, double b);

float smear_pt_res(float pt, float genpt, float eta);

double evalEt(double pt, double eta, double phi, double e);

double evalMt(double pt, double eta, double phi, double e);

TMVA::Reader* getTMVAReader( std::string pathtofile, std::string target, std::string regMethod , Float_t readerVars[12]);
void getRegressionEnergy(float& output, std::string regMethod, 
			 TMVA::Reader *reader, Float_t readerVars[12], 
			 TTree* tree, Long64_t entry , int jetpos, float shift,
			 int verbose);
void addRegressionBranchesPerJet( TTree* tree, Float_t readerVarsF[14], Int_t readerVarsI[2]);

void fillRegressionBranchesPerJet( Float_t readerVarsF[14], 
				   Int_t readerVarsI[2], 
				   TTree* tree, Long64_t entry , 
				   int jetpos, int verbose);

float eleSF(float pt, float eta);


float weightError( TTree* tree, float pt, float eta, float& scale_);


using namespace std;
class BTagLikelihood {
public:

  /*
  Keeps the jet CSV PDF values for the b, c and l hypotheses. 
  */
  class JetProbability {
  public:
    double b, c, l;
    JetProbability(double _b, double _c, double _l) {
      b = _b;
      c = _c;
      l = _l;
    }
  };

  enum EFlavour {
    b,
    c,
    l
  };

  enum EBin {
    Bin0,
    Bin1
  };

  map<tuple<EFlavour, EBin>, TH1F*> btagger;

  BTagLikelihood(TFile* fCP, TString csvName);
  double get_value(TH1F* h, double csv);
  std::vector<JetProbability> evaluate_jet_probabilities(std::vector<double>& jet_csv, std::vector<double>& jet_eta);
  double btag_likelihood(std::vector<JetProbability>& jet_probs, unsigned int nB, unsigned int nC, unsigned int nL, vector<int>& best_perm);
  double btag_lr_default(std::vector<JetProbability>& jet_probs, vector<int>& best_perm);

  //Case where W->cq is taken into account
  double btag_lr_wcq(vector<JetProbability>& jet_probs, vector<int>& best_perm);
  //Case where tt + cc is added to the likelihood
  double btag_lr_radcc(vector<JetProbability>& jet_probs, vector<int>& best_perm);

};

#endif
