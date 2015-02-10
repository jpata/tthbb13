/*
  Author: L. Bianchini (ETH Zurich)
  Class that integrates over the tth/ttbb phase-space

  Create libraries for OpenLoops processes:
   1) gfortran -shared -fPIC -o libpphttxcallme2born.so pphttxcallme2born.f -O2 -L../../../../lib/slc5_amd64_gcc462/  -lopenloops_ppHtt_1tL -lopenloops -lb
ar -lcoli
  Compile with OpenLoops library:
   2) scram b -j 6 USER_CXXFLAGS="-lopenloops\ -lbar\ -lcoli\ -lpphttxcallme2born\ -lppttxbbxcallme2born"
*/


#ifndef MEINTEGRATORNEW_H
#define MEINTEGRATORNEW_H

#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TPluginManager.h"

#include "TFile.h"
#include "TCanvas.h"
#include "TPad.h"
#include "TF1.h"
#include "TF2.h"
#include "TLegend.h"
#include "TList.h"
#include "THStack.h"
#include "TCut.h"
#include "TArrayF.h"
#include "TObjArray.h"
#include "TVector3.h"
#include "TStyle.h"
#include "TDirectory.h"
#include "TGraph.h"
#include "TKey.h"
#include "TMultiGraph.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "Math/GenVector/LorentzVector.h"
#include "TLorentzVector.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "RooArgSet.h"
#include "RooAbsPdf.h"
#include "TH1.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TString.h"
#include "TStopwatch.h"
#include "TRandom3.h"

#include <string>
#include <map>
#include <limits>


#define DEBUG 0
#define PI TMath::Pi()


using namespace RooFit;
using namespace std;

namespace LHAPDF {
void   initPDFSet(int nset, const std::string& filename, int member=0);
int    numberPDF  (int nset);
void   usePDFMember(int nset, int member);
double xfx(int nset, double x, double Q, int fl);
double getXmin(int nset, int member);
double getXmax(int nset, int member);
double getQ2min(int nset, int member);
double getQ2max(int nset, int member);
void   extrapolate(bool extrapolate=true);
}


float deltaR( TLorentzVector reco, TLorentzVector gen) {
    return TMath::Sqrt( (reco.Eta()-gen.Eta())*(reco.Eta()-gen.Eta()) +  TMath::ACos( TMath::Cos(reco.Phi()-gen.Phi()) )*TMath::ACos( TMath::Cos(reco.Phi()-gen.Phi()) ) )  ;
}


extern "C" {
    void pphttxcallme2born_( double*, double[20],  double*, double* );
}

extern "C" {
    void ppttxbbxcallme2born_( double*, double[24],  double*, double* );
}


class MEIntegratorNew {

public:

    MEIntegratorNew( string , int , int);
    ~MEIntegratorNew();

    double Eval(const double* ) const;
    double EvalPdf(const double* ) const;

    enum IntegrationType {
        SL2wj = 0,
        SL1wj,
        SLNoBHad,
        SLNoBLep,
        SLNoHiggs,
        SL3b,
        DL,
        SLXSec,
        SLAcc,
        SLAcc2wj,
        SLAcc1wj,
        SLAccNoBHad,
        SLAccNoBLep,
        SLAccNoHiggs,
        Unknown
    };

    enum NormalizationType {
        None = 0,
        xSec,
        Acc
    };

    void   setIntType( IntegrationType );
    int    getIntType() ;
    void   setHypo( int );
    void   SetPar(int);
    void   setJets( vector<TLorentzVector>* );
    void   setBtag( std::vector<float>* );
    void   createMash();
    double        probabilitySL2wj(const double*, int) const;
    double        probabilitySL1wj(const double*, int) const;
    double        probabilitySLNoBHad(const double*, int) const;
    double        probabilitySLNoBLep(const double*, int) const;
    double        probabilitySLNoHiggs(const double*, int) const;
    double        probabilityDL(const double*, int) const;
    double        probabilitySLUnconstrained(const double*, int ) const;
    unsigned int  findMatch(double, double) const;
    void   initTFparameters(float,float,float,float,float);
    void   cachePdf( const string , const string , int );
    void   cachePdf( const string , const string , const string, int,    int );
    void   cachePdf( const string , const string , const string, string, int, int, int );
    void   cachePdf( const string , const string , const string, TArrayF, TArrayF);
    void   cachePdf( const string , const string , const string, const string, TArrayF, TArrayF, TArrayF);
    void   setMass   (double);
    void   setQ      (double);
    void   setSqrtS  (double);
    void   setTopMass(double, double);
    void   setSumEt  (double);
    void   setMEtCov  (double, double, double);
    void   setPtPhiParam (int);
    void   setPartonLuminosity(TH1F*);
    bool   smearByTF(float, int);

    void   switchOffOL();
    void   setUseME   (int);
    void   setUseJac  (int);
    void   setUseMET  (int);
    void   setUseTF   (int);
    void   setUsePDF  (int);
    void   setUseAnalyticalFormula(int);
    void   setUseDynamicalScale(int);
    void   setTopFlags(int,int);
    void   setWeightNorm(NormalizationType);
    void   setNormFormulas(TString, TString, TString, TString, TString, TString);
    void   resetEvaluation();

    void   setConstrainToRecoil  (int);
    void   setUseRefinedTF       (int);

    TH1*   getCachedPdf( const string ) const;
    TH1*   getCachedTF ( const string ) const;
    TH2F*  getMash( );
    TH1F*  getDebugHisto( );
    void   debug();
    void   printJetList();

    void   initVersors(int);
    void   initTF() ;
    void   deleteTF();
    void   adaptRange(TF1*, float&, float&, float, float);
    void   adaptRange(TH1*, float&, float&, float, float);
    void   createTFjet(const string, float , float, string , float, float);
    void   createTFmet(const string , float , float, float, float);
    void   createTFmetFromCovM(string, float);

    pair<double,double> getNuPhiCI      (float);
    pair<double,double> getJetEnergyCI  (float, float, const string, float);
    pair<double,double> getBLepEnergyCI (float);
    pair<double,double> getW1JetEnergyCI(float);
    pair<double,double> getW2JetEnergyCI(float);
    pair<double,double> getBHadEnergyCI (float);
    pair<double,double> getB1EnergyCI   (float);
    pair<double,double> getB2EnergyCI   (float);

    TLorentzVector jetAt(unsigned int);

    bool compatibilityCheck       (float, int, double&, double&, double&);
    bool compatibilityCheck_WHad  (float, int, double&, double&, double&);
    bool compatibilityCheck_TopHad(float, int, double&, double&, double&);

    double jetEnergyTF(float, double, double, const string) const;

    int    topHadEnergies     (double, double&, double&, double&, double&, int&) const;
    int    topLepEnergies     (double, double,  double&, double&, double&, double&, int&) const;
    int    topLep2Energies    (double, double,  double&, double&, double&, double&, int&) const;
    int    topLepBLostEnergies(double, double,  double, double, double&, double&, double&, double&, int&) const;
    void   topLepEnergiesFromPtPhi    (int, double, double,  double&, double&, double&, double&, double&, int&) const;
    void   topLepEnergiesFromEbPhi    (int, double, double,  double&, double&, double&, double&, int& ) const ;
    int    topHadLostEnergies (double, double,  double&,  double, double&, double&, double&, int&) const;
    int    topHadBLostEnergies(double, double,  double,  double&, double&, double&, double&, int&) const;
    int    higgsEnergies     (double, double&, double&, int&) const;

    double topHadJakobi     (double, double,  double, TLorentzVector*) const;
    double topHadLostJakobi (double, double,  double, TLorentzVector*) const;
    double topHadBLostJakobi(double, double,  double, TLorentzVector*) const;
    double topLepJakobi     (double, double,  double, TLorentzVector*) const;
    double topLepBLostJakobi(double, double,  double, TLorentzVector*) const;
    double higgsJakobi      (double, double ) const;

    double topHadDensity   (double, double)  const;
    double topLepDensity   (double, double)  const;
    double higgsDensity    (double)  const;

    double topHadDensity_analytical( TLorentzVector*, TLorentzVector*, TLorentzVector*, TLorentzVector*) const;
    double topLepDensity_analytical( TLorentzVector*, TLorentzVector*, TLorentzVector*, TLorentzVector*) const;


    //double tthDensity      (double, double, double, double)  const;
    //double meSquaredAtQ    (double, double, double, double) const;
    double meSquaredOpenLoops      (TLorentzVector*, TLorentzVector*, TLorentzVector*, double&, double&) const;
    double meSquaredOpenLoops_ttbb (TLorentzVector*, TLorentzVector*, TLorentzVector*, TLorentzVector*, double&, double&) const;
    double xSection           (int) const;
    double evaluateCahchedPdf (TH1*, double, double, double)  const;
    double ggPdf              ( double, double, double) const;
    double qqPdf              ( double, double, double) const;


private:

    //TFile* out_;
    RooWorkspace *w_;
    std::map<string, double> jetParam_;
    std::map<string, TH1F*> variables1D_;
    std::map<string, TH2F*> variables2D_;
    std::map<string, TH3F*> variables3D_;
    std::map<string, TH1* > transferFunctions_;

    // 0- lep
    // 1- MET
    // 2- b from top lep
    // 3- j1 from W
    // 4- j2 from W
    // 5- b from top hadr
    // 6- b1 from H
    // 7- b2 from H

    vector<TLorentzVector> jets_;
    vector<TLorentzVector> jets_backup_;
    vector<float> bTagging_;
    TVector3 eLep_;
    TVector3 eBLep_;
    TVector3 eBHad_;
    TVector3 eW1Had_;
    TVector3 eW2Had_;
    TVector3 eB1_;
    TVector3 eB2_;
    TVector3 eMEt_;

    IntegrationType intType_;
    int top1Flag_;  // +1 <=> top lep is top
    int top2Flag_;
    NormalizationType normalizeToXSec_;
    int hypo_;
    int useRefinedTF_;

    int par_;
    const int verbose_;
    int usePtPhiParam_;
    int constrainToRecoil_;
    int evaluation_;
    double M_;
    float Q_;
    float pStar_;
    float EbStar_;
    float EWStar_;
    float EuStar_;
    double dM2_;
    double dMh2_;
    double Mtop_;
    double Mb_;
    double Mw_;
    double SqrtS_;
    double sumEt_;
    TH2F* mash_;
    int useME_;
    int useJac_;
    int useMET_;
    int useTF_;
    int usePDF_;
    int useAnalyticalFormula_;
    int useDynamicalScale_;

    TH1F* debugHisto1_;
    TH1F* partonLuminosity_;
    TH1F pdfBetaWHad_, pdfGammaWHad_, pdfBetaWLep_, pdfGammaWLep_;//, pdfGammaTTH_;
    TH2F pdf2D_;
    TH3F pdf3D_;
    TH1F* tfWjet1_;
    TH1F* tfWjet2_;
    TH1F* tfbHad_;
    TH1F* tfbLep_;
    TH1F* tfMetPt_;
    TH1F* tfHiggs1_;
    TH1F* tfHiggs2_;
    TH2F* tfMetPhi_;

    double Vx_, Vy_, Vxy_, rho_;

    TF1* xSecFormula_;
    TF1* accSL2wjFormula_;
    TF1* accSL1wjFormula_;
    TF1* accSLNoBHadFormula_;
    TF1* accSLNoHiggsFormula_;

    TF1* tthPtFormula_;

    TStopwatch* clock_;
    TRandom3* ran_;

public:
    double getEvaluations() {
        return this->evaluation_;
    }

};


MEIntegratorNew::MEIntegratorNew( string fileName , int param , int verbose ) : verbose_(verbose) {

    cout << "Begin constructor" << endl;

    //nset (first arg) was 0, however LHAPDF seems to have 1-based indexing?
    //this just indexes PDFS in the wrapper, has no physical effect. Not clear why LHAPDF low runs and full does not, though
    LHAPDF::initPDFSet(1, "cteq65.LHgrid");
    cout << "initPDFSet successul" << endl;

    clock_ = new TStopwatch();
    ran_ = new TRandom3();

    //TODO: seed fixed to a value?
    ran_->SetSeed(65539);

    intType_       = SL2wj;
    par_           = param;
    sumEt_         = 1500.;
    usePtPhiParam_ = 0;
    evaluation_    = 0;

    jets_.    clear();
    jets_backup_.clear();
    bTagging_.clear();
    initVersors(0);

    constrainToRecoil_ = 0;
    useRefinedTF_      = 0;

    Mtop_   =  174.3;
    Mb_     =  4.8;
    Mw_     =  80.19;
    pStar_  =  TMath::Sqrt( (Mtop_*Mtop_-(Mw_+Mb_)*(Mw_+Mb_) )*( Mtop_*Mtop_-(Mw_-Mb_)*(Mw_-Mb_) ) )/2./Mtop_;
    EbStar_ =  (Mtop_*Mtop_ - Mw_*Mw_ + Mb_*Mb_)/2./Mtop_;
    EWStar_ =  (Mtop_*Mtop_ + Mw_*Mw_ - Mb_*Mb_)/2./Mtop_;
    EuStar_ =  Mw_/2;
    dM2_    =  (Mtop_*Mtop_-Mb_*Mb_-Mw_*Mw_)*0.5;
    M_      =  125.;
    Q_      =  500;
    dMh2_   =  (M_*M_-2*Mb_*Mb_)*0.5;
    SqrtS_  =  8000.;
    Vx_     = -99;
    Vy_     = -99;
    Vxy_    = 0.;
    rho_    = 0.;

    mash_             = 0;
    debugHisto1_      = 0;
    partonLuminosity_ = 0;

    useME_   = 1;
    useJac_  = 1;
    useMET_  = 1;
    useTF_   = 1;
    usePDF_  = 1;
    useAnalyticalFormula_ = 0;
    useDynamicalScale_    = 0;

    top1Flag_ = 0;
    top2Flag_ = 0;

    hypo_ = 0;

    normalizeToXSec_ = NormalizationType::None;

    xSecFormula_         = 0;
    accSL2wjFormula_     = 0;
    accSL1wjFormula_     = 0;
    accSLNoBHadFormula_  = 0;
    accSLNoHiggsFormula_ = 0;
    tthPtFormula_        = 0;

    TFile* file = TFile::Open(fileName.c_str(),"READ");
    if(file == 0 || file->IsZombie()) {
        cerr << "Failed to open transfer functions from file " << fileName << endl;
        throw;
    }
    w_ = (RooWorkspace*)file->Get("transferFuntions");

    // jets
    RooArgSet allVars = w_->allVars();
    TIterator* iter = allVars.createIterator();
    RooRealVar* var = 0;
    while( (var = (RooRealVar*)(*iter)() ) ) {
        jetParam_[ string(var->GetName()) ] = var->getVal();

        //FIXME: make jetParam a map of enums
        //param0resolHeavyBin0
        //jetParamEnum_
        cout << string(var->GetName()) << ": " << var->getVal() << endl;
    }

    cachePdf( "pdfGammaWHad",     "GammaW",    100);
    cachePdf( "pdfBetaWHad",      "BetaW",     100);
    cachePdf( "pdfGammaWLep",     "GammaWLep", 100);
    cachePdf( "pdfBetaWLep",      "BetaWLep",  100);

    pdfGammaWHad_ = *((TH1F*)this->getCachedPdf("pdfGammaWHad"));
    pdfBetaWHad_  = *((TH1F*)this->getCachedPdf("pdfBetaWHad"));
    pdfBetaWLep_  = *((TH1F*)this->getCachedPdf("pdfBetaWLep"));
    pdfGammaWLep_ = *((TH1F*)this->getCachedPdf("pdfGammaWLep"));

    cout << "End constructor" << endl;

}


MEIntegratorNew::~MEIntegratorNew() {

    cout << "Start destructor" << endl;

    for(std::map<string, TH1F*>::iterator it = variables1D_.begin(); it!=variables1D_.end(); it++) {
        if(it->second)
            delete (it->second);
    }
    for(std::map<string, TH2F*>::iterator it = variables2D_.begin(); it!=variables2D_.end(); it++) {
        if(it->second)
            delete (it->second);
    }
    for(std::map<string, TH3F*>::iterator it = variables3D_.begin(); it!=variables3D_.end(); it++) {
        if(it->second)
            delete (it->second);
    }
    //for(std::map<string, TH1*>::iterator it = transferFunctions_.begin(); it!=transferFunctions_.end(); it++){
    //if(it->second)
    //  delete (it->second);
    //}
    //delete mash_;
    //delete debugHisto1_;

    //out_->Close();
    //delete out_;
    delete clock_;
    delete ran_;

    if(xSecFormula_)        delete xSecFormula_;
    if(accSL2wjFormula_)    delete accSL2wjFormula_;
    if(accSL1wjFormula_)    delete accSL1wjFormula_;
    if(accSLNoBHadFormula_) delete accSLNoBHadFormula_;
    if(accSLNoHiggsFormula_)delete accSLNoHiggsFormula_;
    if(tthPtFormula_)       delete tthPtFormula_;

    cout << "End destructor" << endl;

}

void MEIntegratorNew::deleteTF() {

    resetEvaluation();

    for(std::map<string, TH1*>::iterator it = transferFunctions_.begin(); it!=transferFunctions_.end(); it++) {
        if(it->second) {
            delete (it->second);
        }
    }
    transferFunctions_.clear();
}

void MEIntegratorNew::initVersors(int withJetList) {

    resetEvaluation();

    if(withJetList==0) {
        eLep_   = TVector3(0.,0.,1.);
        eBLep_  = TVector3(0.,0.,1.);
        eBHad_  = TVector3(0.,0.,1.);
        eW1Had_ = TVector3(0.,0.,1.);
        eW2Had_ = TVector3(0.,0.,1.);
        eB1_    = TVector3(0.,0.,1.);
        eB2_    = TVector3(0.,0.,1.);
        eMEt_   = TVector3(0.,0.,1.);
        return;
    }
    else if( withJetList==1 && jets_.size() < 7 ) {
        cout << "Jets are not properly initliazied!!" << endl;
        return;
    }
    else if(  withJetList==1 && jets_.size() == 8 ) {
        eLep_  = (jets_backup_[0].Vect()).Unit();
        eMEt_  = (jets_backup_[1].Vect()).Unit();
        eBLep_ = (jets_backup_[2].Vect()).Unit();
        eW1Had_= (jets_backup_[3].Vect()).Unit();
        eW2Had_= (jets_backup_[4].Vect()).Unit();
        eBHad_ = (jets_backup_[5].Vect()).Unit();
        eB1_   = (jets_backup_[6].Vect()).Unit();
        eB2_   = (jets_backup_[7].Vect()).Unit();
    }
    else if(  withJetList>1 && jets_.size() == 8 ) {
        int iBLep  = withJetList/100000;
        if(iBLep>7 || iBLep<0) {
            cout << iBLep << endl;
            cout << "iBLep Error in MEIntegratorNew::initVersors.. return" << endl;
            return;
        }
        int iW1Had = (withJetList - iBLep*100000)/10000;
        if(iW1Had>7 || iW1Had<0 || iW1Had==iBLep) {
            cout << iW1Had << endl;
            cout << "iW1Had Error in MEIntegratorNew::initVersors.. return" << endl;
            return;
        }
        int iW2Had = (withJetList - iBLep*100000 - iW1Had*10000)/1000;
        if(iW2Had>7 || iW2Had<0 || iW2Had==iW1Had || iW2Had==iBLep) {
            cout << iW2Had << endl;
            cout << "iW2Had Error in MEIntegratorNew::initVersors.. return" << endl;
            return;
        }
        int iBHad  = (withJetList - iBLep*100000 - iW1Had*10000 - iW2Had*1000)/100;
        if(iBHad>7 || iBHad<0 || iW2Had==iW1Had || iW2Had==iBLep || iBHad==iW2Had) {
            cout << iBHad << endl;
            cout << "iBHad Error in MEIntegratorNew::initVersors.. return" << endl;
            return;
        }
        int iB1    = (withJetList - iBLep*100000 - iW1Had*10000 - iW2Had*1000 - iBHad*100)/10;
        if(iB1>7 || iB1<0 || iW2Had==iW1Had || iW2Had==iBLep || iBHad==iW2Had || iB1==iBHad) {
            cout << iB1 << endl;
            cout << "iB1 Error in MEIntegratorNew::initVersors.. return" << endl;
            return;
        }
        int iB2    = (withJetList - iBLep*100000 - iW1Had*10000 - iW2Had*1000 - iBHad*100 - iB1*10)/1;
        if(iB2>7 || iB2<0 || iW2Had==iW1Had || iW2Had==iBLep || iBHad==iW2Had || iB2==iBHad || iB2==iB1) {
            cout << iB2 << endl;
            cout << "iB2 Error in MEIntegratorNew::initVersors.. return" << endl;
            return;
        }

        vector<TLorentzVector> newjets_;
        newjets_.push_back( jets_backup_[0] );
        newjets_.push_back( jets_backup_[1] );
        newjets_.push_back( jets_backup_[iBLep] );
        newjets_.push_back( jets_backup_[iW1Had] );
        newjets_.push_back( jets_backup_[iW2Had] );
        newjets_.push_back( jets_backup_[iBHad] );
        newjets_.push_back( jets_backup_[iB1] );
        newjets_.push_back( jets_backup_[iB2] );

        jets_.swap( newjets_ );
        newjets_.clear();

        eLep_  = (jets_[0].Vect()).Unit();
        eMEt_  = (jets_[1].Vect()).Unit();
        eBLep_ = (jets_[2].Vect()).Unit();
        eW1Had_= (jets_[3].Vect()).Unit();
        eW2Had_= (jets_[4].Vect()).Unit();
        eBHad_ = (jets_[5].Vect()).Unit();
        eB1_   = (jets_[6].Vect()).Unit();
        eB2_   = (jets_[7].Vect()).Unit();

        if(verbose_) cout << "Permutation: " << iBLep << iW1Had << iW2Had << iBHad << iB1 << iB2 << endl;

    }
    else {
        cout << "Problems in MEIntegratorNew::initVersors" << endl;
    }

    return;
}


void MEIntegratorNew::adaptRange(TF1* f, float& xLow, float& xHigh, float quantile, float margin) {

    double probSum[2] = {quantile, 1-quantile};
    double q[2];
    f->GetQuantiles(2,q,probSum);

    if(margin<=1) {
        xLow  = q[0]*(1-margin);
        xHigh = q[1]*(1+margin);
    }
    else {
        xLow  = q[0];
        xHigh = q[1];
    }
}

void MEIntegratorNew::adaptRange(TH1* f, float& xLow, float& xHigh, float quantile, float margin) {

    double probSum[2] = {quantile, 1-quantile};
    double q[2];
    f->GetQuantiles(2,q,probSum);

    if(margin<=1) {
        xLow  = q[0]*(1-margin);
        xHigh = q[1]*(1+margin);
    }
    else {
        xLow  = q[0];
        xHigh = q[1];
    }
}


void MEIntegratorNew::createTFjet(string tfName, float eta, float pt, string flavor, float quantile, float margin) {

    cout << "MEIntegratorNew::createTFjet is deprecated..." << endl;
    return;
    //cout << "Creating " << tfName << endl;

    float xLow  =    0.;
    float xHigh = 1000.;
    float gevStep = 2.;

    string bin = "Bin0";
    if(  TMath::Abs( eta )<1.0 ) bin = "Bin0";
    else bin = "Bin1";

    if(gDirectory->FindObject("tf")!=0) {
        gDirectory->Remove(gDirectory->FindObject("tf"));
    }

    //clock_->Start();
    double param0resol = (jetParam_.find("param0resol"+flavor+bin))->second;
    double param1resol = (jetParam_.find("param1resol"+flavor+bin))->second;
    double param0resp  = (jetParam_.find("param0resp" +flavor+bin))->second;
    double param1resp  = (jetParam_.find("param1resp" +flavor+bin))->second;

    //clock_->Stop();
    //cout << "Eval parameters: " << clock_->RealTime() << endl;

    //clock_->Start();
    //TF1* tf = new TF1("tf",Form("TMath::Gaus( x, %f*[0]+%f , [0]*TMath::Sqrt( %f/[0] + %f/[0]/[0]) , 1) ",
    //			      param0resp, param1resp,
    //		      param0resol*param0resol, param1resol*param1resol ),1, (pt+5*trialWidth));

    //TF1* tf = new TF1("tf", "1",1,1000); //toy
    //clock_->Stop();
    //cout << "Create TF1: " << clock_->RealTime() << endl;

    //clock_->Start();
    ////tf->SetNpx(100);

    /* OLD
    tf->SetParameter(0, pt );
    adaptRange(tf, xLow, xHigh, quantile, margin);
    if(xLow<0) xLow = 0.0;
    */

    float meanTmp  = (pt*param0resp + param1resp);
    float sigmaTmp = meanTmp*TMath::Sqrt( (param0resol*param0resol)/meanTmp + (param1resol*param1resol)/meanTmp/meanTmp );
    int nSigmaLow  = 2;
    int nSigmaHigh = tfName.find("Wjet1")!=string::npos || tfName.find("Higgs1")!=string::npos ?
                     3 : 4;

    xLow    = TMath::Max( float(0.), meanTmp - nSigmaLow *(1+margin)*sigmaTmp  ); // -2 sigma
    xHigh   = meanTmp + nSigmaHigh*(1+margin)*sigmaTmp   ;                 // +3/4 sigma
    gevStep = sigmaTmp / 10.;

    //clock_->Stop();
    //cout << "Adapt range : " << clock_->RealTime() << endl;


    if(gDirectory->FindObject(("htf"+tfName).c_str())!=0) {
        gDirectory->Remove(gDirectory->FindObject(("htf"+tfName).c_str()));
    }

    //clock_->Start();
    TH1F* htf_ = new TH1F(("htf"+tfName).c_str(), "", int((xHigh-xLow)/gevStep), xLow, xHigh);
    for( int i = 1; i <= htf_->GetNbinsX(); i++) {
        float binC = htf_->GetBinCenter(i);

        double value = TMath::Gaus( pt , param0resp*binC+param1resp , binC*TMath::Sqrt( (param0resol*param0resol)/binC + (param1resol*param1resol)/binC/binC) , 1);
        htf_->SetBinContent(i, value);
        /* OLD
        tf->SetParameter(0, binC);
        htf_->SetBinContent(i, tf->Eval( pt ) );
        */
    }
    //clock_->Stop();
    //cout << "Fill TH1 : " << clock_->RealTime() << endl;

    //clock_->Start();
    if( transferFunctions_.find("tf"+tfName)!=transferFunctions_.end()) {
        delete (transferFunctions_.find("tf"+tfName)->second);
        transferFunctions_.erase( transferFunctions_.find("tf"+tfName) );
        transferFunctions_["tf"+tfName] = htf_;
    }
    else
        transferFunctions_["tf"+tfName] = htf_;

    if(tfName.find("Wjet1")!=string::npos)
        tfWjet1_ = htf_;
    else if (tfName.find("Wjet2")!=string::npos)
        tfWjet2_ = htf_;
    else if (tfName.find("bHad")!=string::npos)
        tfbHad_ = htf_;
    else if (tfName.find("bLep")!=string::npos)
        tfbLep_ = htf_;
    else if (tfName.find("Higgs1")!=string::npos)
        tfHiggs1_ = htf_;
    else if (tfName.find("Higgs2")!=string::npos)
        tfHiggs2_ = htf_;
    else {
        if(verbose_) cout << "Name in createTFjet is not valid" << endl;
    }
    //clock_->Stop();
    //cout << "Copy TH1 : " << clock_->RealTime() << endl;
    //cout << "**** End ****" << endl;

//delete tf;
}


void MEIntegratorNew::createTFmet(string tfName, float phi, float pt, float quantile, float margin) {

    cout << "MEIntegratorNew::createTFmet is deprecated..." << endl;
    return;

    float xLowEt  =    0.;
    float xHighEt = 1000.;
    float xLowPhi =    0;
    float xHighPhi= PI;
    float gevStep = 4.;
    float etaStep = 0.04;

    string bin = "Bin0";
    if (sumEt_ < 1200.)
        bin =  "Bin0";
    else if ( sumEt_ > 1200. && sumEt_ < 1800.)
        bin =  "Bin1";
    else
        bin =  "Bin2";

    if(gDirectory->FindObject(("tf"+tfName+"Pt").c_str())!=0) {
        gDirectory->Remove(gDirectory->FindObject(("tf"+tfName+"Pt").c_str()));
    }

    double param0EtMean  = (jetParam_.find("param0EtMean"+bin))->second;
    double param1EtMean  = (jetParam_.find("param1EtMean"+bin))->second;
    double param2EtMean  = (jetParam_.find("param2EtMean"+bin))->second;
    double param3EtMean  = (jetParam_.find("param3EtMean"+bin))->second;
    double param0EtWidth = (jetParam_.find("param0EtWidth"+bin))->second*(jetParam_.find("param0EtWidth"+bin))->second;
    double param1EtWidth = (jetParam_.find("param1EtWidth"+bin))->second*(jetParam_.find("param1EtWidth"+bin))->second;


    TF1* tfMetPt   = new TF1(("tf"+tfName+"Pt").c_str(), Form("TMath::Gaus(x, (%f + %f*TMath::Exp(%f*[0]+%f) ),  [0]*TMath::Sqrt(%f/[0] + %f/[0]/[0])  , 1)",
                             param0EtMean,param1EtMean,param2EtMean,param3EtMean,
                             param0EtWidth,param1EtWidth
                                                             ), -1000.,1000.); // x = reco - gen
    /* OLD
    ////tfMetPt->SetNpx(2000);
    tfMetPt->SetParameter(0, pt );
    adaptRange(tfMetPt, xLowEt, xHighEt, quantile, margin);
    if(xLowEt>0){
      xLowEt  += pt;
      xHighEt += pt;
    }
    else{
      xLowEt  =  0.;
      xHighEt += pt;
    }
    */

    float meanTmp    = (param0EtMean + param1EtMean*TMath::Exp(param2EtMean*pt+param3EtMean) );
    float sigmaEtTmp = pt*TMath::Sqrt( (param0EtWidth)/pt + (param1EtWidth)/pt/pt );
    int nSigmaEtLow  = 2;
    int nSigmaEtHigh = 3;
    xLowEt   = TMath::Max( pt + meanTmp - nSigmaEtLow *sigmaEtTmp , float(0.)) ; // -2 sigma
    xHighEt  =             pt + meanTmp + nSigmaEtHigh*sigmaEtTmp  ;             // +3 sigma
    gevStep  = sigmaEtTmp / 10.;

    if(gDirectory->FindObject(("htf"+tfName+"Pt").c_str())!=0) {
        gDirectory->Remove(gDirectory->FindObject(("htf"+tfName+"Pt").c_str()));
    }

    TH1F* htfMetPt_ = new TH1F(("htf"+tfName+"Pt").c_str(), "", int((xHighEt-xLowEt)/gevStep), xLowEt, xHighEt);
    for( int i = 1; i <= htfMetPt_->GetNbinsX(); i++) {
        float binC = htfMetPt_->GetBinCenter(i);
        tfMetPt->SetParameter(0, binC);
        htfMetPt_->SetBinContent(i, tfMetPt->Eval( pt - binC) );
    }
    if( transferFunctions_.find("tf"+tfName+"Pt")!=transferFunctions_.end()) {
        delete (transferFunctions_.find("tf"+tfName+"Pt")->second);
        transferFunctions_.erase( transferFunctions_.find("tf"+tfName+"Pt") );
        transferFunctions_["tf"+tfName+"Pt"] = htfMetPt_;
    }
    else
        transferFunctions_["tf"+tfName+"Pt"] = htfMetPt_;

    tfMetPt_ = htfMetPt_;
    delete tfMetPt;

    if(gDirectory->FindObject(("tf"+tfName+"Phi").c_str())!=0) {
        gDirectory->Remove(gDirectory->FindObject(("tf"+tfName+"Phi").c_str()));
    }


    double param0PhiWidth = (jetParam_.find("param0PhiWidth"+bin))->second;
    double param1PhiWidth = (jetParam_.find("param1PhiWidth"+bin))->second;

    TF1* tfMetPhi   = new TF1(("tf"+tfName+"Phi").c_str(),Form("(2./(TMath::Erf(TMath::Pi()/ (%f/[0] + %f/[0]/[0]) )))*TMath::Gaus(x, 0.0, %f/[0] + %f/[0]/[0] ,1)",
                              param0PhiWidth,param1PhiWidth, param0PhiWidth,param1PhiWidth
                                                              ), 0., PI);  // x = |reco-gen|

    /* OLD
    //tfMetPhi->SetNpx(1000);
    tfMetPhi->SetParameter(0, pt );
    adaptRange(tfMetPhi, xLowPhi, xHighPhi, quantile, margin );
    if((PI - xHighPhi) < 0.2) xHighPhi =  PI;
    */

    float sigmaPhiTmp = ( (param0PhiWidth)/pt + (param1PhiWidth)/pt/pt );
    int nSigmaPhiHigh = 2;
    xHighPhi  = TMath::Min( nSigmaPhiHigh*sigmaPhiTmp , float(PI) )  ; // +2 sigma



    if(gDirectory->FindObject(("htf"+tfName+"Phi").c_str())!=0) {
        gDirectory->Remove(gDirectory->FindObject(("htf"+tfName+"Phi").c_str()));
    }


    TH2F* htfMetPhi_ = new TH2F(("htf"+tfName+"Phi").c_str(), "", int((xHighEt-xLowEt)/gevStep), xLowEt, xHighEt, int((xHighPhi-xLowPhi)/etaStep), xLowPhi, xHighPhi);
    for( int i = 1; i <= htfMetPhi_->GetNbinsX(); i++) {
        float binCX = htfMetPhi_->GetXaxis()->GetBinCenter(i);
        tfMetPhi->SetParameter(0, binCX);
        for( int j = 1; j <= htfMetPhi_->GetNbinsY(); j++) {
            float binCY = htfMetPhi_->GetYaxis()->GetBinCenter(j);
            /////////htfMetPhi_->SetBinContent(i,j, tfMetPhi->Eval( TMath::ACos(TMath::Cos( phi - binCY)) ) );
            htfMetPhi_->SetBinContent(i,j, tfMetPhi->Eval( binCY ) );
        }
    }
    if( transferFunctions_.find("tf"+tfName+"Phi")!=transferFunctions_.end()) {
        delete (transferFunctions_.find("tf"+tfName+"Phi")->second);
        transferFunctions_.erase( transferFunctions_.find("tf"+tfName+"Phi") );
        transferFunctions_["tf"+tfName+"Phi"] = htfMetPhi_;
    }
    else
        transferFunctions_["tf"+tfName+"Phi"] = htfMetPhi_;

    tfMetPhi_ = htfMetPhi_;
    delete tfMetPhi;

}

void MEIntegratorNew::initTF() {

    cout << "MEIntegratorNew::initTF is deprecated..." << endl;
    return;

    createTFjet("Wjet1",  eW1Had_.Eta(), jets_[3].E(), "Light", 0.025, 0.30);
    createTFjet("Wjet2",  eW2Had_.Eta(), jets_[4].E(), "Light", 0.025, 0.30);
    createTFjet("bHad",   eBHad_.Eta(),  jets_[5].E(), "Heavy", 0.025, 0.30);
    createTFjet("bLep",   eBLep_.Eta(),  jets_[2].E(), "Heavy", 0.025, 0.30);
    createTFjet("Higgs1", eB1_.Eta(),    jets_[6].E(), "Heavy", 0.025, 0.30);
    createTFjet("Higgs2", eB2_.Eta(),    jets_[7].E(), "Heavy", 0.025, 0.30);

    createTFmet("Met", jets_[1].Phi() , jets_[1].Pt() , 0.025, 0.50);

    //createTFmetFromCovM("Met", 0.95);
}



void MEIntegratorNew::createTFmetFromCovM(string tfName, float quantile)  {

    cout << "MEIntegratorNew::createTFmetFromCovM is deprecated..." << endl;
    return;

    // DUMMY
    TH1F* htfMetPt_ = new TH1F(("htf"+tfName+"Pt").c_str(), "", 1 , 0,1);
    if( transferFunctions_.find("tf"+tfName+"Pt")!=transferFunctions_.end()) {
        delete (transferFunctions_.find("tf"+tfName+"Pt")->second);
        transferFunctions_.erase( transferFunctions_.find("tf"+tfName+"Pt") );
        transferFunctions_["tf"+tfName+"Pt"] = htfMetPt_;
    }
    else
        transferFunctions_["tf"+tfName+"Pt"] = htfMetPt_;

    tfMetPt_ = htfMetPt_;


    float xLowPhi = 0;
    float xHighPhi= PI;
    float phiStep = 0.04;

    float Px  = jets_[1].Px();
    float Py  = jets_[1].Py();
    float Phi = jets_[1].Phi()>0 ? jets_[1].Phi() : 2*PI+jets_[1].Phi() ;
    float chi2Cut = TMath::ChisquareQuantile(quantile ,2);

    if(Vx_<0 || Vy_<0) {
        if(verbose_) cout << "Use MEt parametrization from root file" << endl;
        double p0 = (jetParam_.find("param0PxWidthModel"))->second;
        double p1 = (jetParam_.find("param1PxWidthModel"))->second;
        double sigma = sumEt_*TMath::Sqrt(p0*p0/sumEt_ + p1*p1/sumEt_/sumEt_);
        Vx_  = sigma*sigma;
        Vy_  = sigma*sigma;
        Vxy_ = 0.0;
        rho_ = 0.0;
    }

    float PxMax = Px + TMath::Sqrt(Vx_*TMath::ChisquareQuantile(quantile ,1));
    float PxMin = Px - TMath::Sqrt(Vx_*TMath::ChisquareQuantile(quantile ,1));
    float PyMax = Py + TMath::Sqrt(Vy_*TMath::ChisquareQuantile(quantile ,1));
    float PyMin = Py - TMath::Sqrt(Vy_*TMath::ChisquareQuantile(quantile ,1));

    if( TMath::Abs(rho_)<1 ) {
        double tfAtZero = (1/(1-rho_*rho_))*( Px*Px/Vx_ + Py*Py/Vy_ - 2*rho_*Px*Py/TMath::Sqrt(Vx_*Vy_)  );
        if( tfAtZero <= chi2Cut ) {
            if(verbose_) cout << "(0,0) is inside the 2-sigma CL => integrate over -pi/+pi" << endl;
        }
        else {
            if(verbose_) cout << "(0,0) is outside the 2-sigma CL => find phi-window with interpolation..." << endl;

            //find phiLow
            for(unsigned int step = 0; step<= (unsigned int)(PI/phiStep); step++) {
                float phi = Phi - step*phiStep;
                float sin = TMath::Sin(phi);
                float cos = TMath::Cos(phi);
                bool stopPhiScan = false;
                bool crossing    = false;
                bool exceeded    = false;
                bool alreadyInTheBox = PxMax*PxMin<=0 &&  PyMax*PyMin<=0;
                for(unsigned int stepP = 0; stepP<1000 && !exceeded && !crossing && !stopPhiScan; stepP++) {

                    if( alreadyInTheBox && (stepP*cos>PxMax ||  stepP*cos<PxMin || stepP*sin>PyMax ||  stepP*sin<PyMin)) {
                        exceeded = true;
                        continue;
                    }
                    else if( !alreadyInTheBox && (stepP*cos>PxMax ||  stepP*cos<PxMin || stepP*sin>PyMax ||  stepP*sin<PyMin)) {
                        continue;
                    }


                    if( (1/(1-rho_*rho_))*( (stepP*cos-Px)*(stepP*cos-Px)/Vx_ + (stepP*sin-Py)*(stepP*sin-Py)/Vy_ - 2*rho_*(stepP*cos - Px)*(stepP*sin - Py)/TMath::Sqrt(Vx_*Vy_) ) < chi2Cut ) {
                        crossing = true;
                    }

                }
                if(!crossing) {
                    xLowPhi     =  phi+0.5*phiStep;
                    stopPhiScan = true;
                }
            }


            //find phiHigh
            for(unsigned int step = 0; step<= (unsigned int)(PI/phiStep); step++) {
                float phi = Phi + step*phiStep;
                float sin = TMath::Sin(phi);
                float cos = TMath::Cos(phi);
                bool stopPhiScan = false;
                bool crossing    = false;
                bool exceeded    = false;
                bool alreadyInTheBox = PxMax*PxMin<=0 &&  PyMax*PyMin<=0;
                for(unsigned int stepP = 0; stepP<1000 && !exceeded && !crossing && !stopPhiScan; stepP++) {

                    if( alreadyInTheBox && (stepP*cos>PxMax ||  stepP*cos<PxMin || stepP*sin>PyMax ||  stepP*sin<PyMin)) {
                        exceeded = true;
                        continue;
                    }
                    else if( !alreadyInTheBox && (stepP*cos>PxMax ||  stepP*cos<PxMin || stepP*sin>PyMax ||  stepP*sin<PyMin)) {
                        continue;
                    }


                    if( (1/(1-rho_*rho_))*( (stepP*cos-Px)*(stepP*cos-Px)/Vx_ + (stepP*sin-Py)*(stepP*sin-Py)/Vy_ - 2*rho_*(stepP*cos - Px)*(stepP*sin - Py)/TMath::Sqrt(Vx_*Vy_) ) < chi2Cut ) {
                        crossing = true;
                    }

                }
                if(!crossing) {
                    xLowPhi     =  phi-0.5*phiStep;
                    stopPhiScan = true;
                }
            }

            xLowPhi  = -TMath::ACos(TMath::Cos( Phi - xLowPhi ));
            xHighPhi = +TMath::ACos(TMath::Cos( Phi - xHighPhi));

        }
    }


    TH2F* htfMetPhi_ = new TH2F(("htf"+tfName+"Phi").c_str(), "", 1,0,1,  1, xLowPhi, xHighPhi);
    if( transferFunctions_.find("tf"+tfName+"Phi")!=transferFunctions_.end()) {
        delete (transferFunctions_.find("tf"+tfName+"Phi")->second);
        transferFunctions_.erase( transferFunctions_.find("tf"+tfName+"Phi") );
        transferFunctions_["tf"+tfName+"Phi"] = htfMetPhi_;
    }
    else
        transferFunctions_["tf"+tfName+"Phi"] = htfMetPhi_;
    htfMetPhi_->Fill(0.5,  (xLowPhi+xHighPhi)/2.  );

    tfMetPhi_ = htfMetPhi_;

}




pair<double, double> MEIntegratorNew::getNuPhiCI(float quantile)  {

    double xLowPhi  = -PI;
    double xHighPhi =  PI;
    float phiStep = 0.04;

    float Px  = jets_[1].Px();
    float Py  = jets_[1].Py();
    float Phi = jets_[1].Phi()>0 ? jets_[1].Phi() : 2*PI+jets_[1].Phi() ;
    float chi2Cut = TMath::ChisquareQuantile(quantile ,2);

    if(Vx_<0 || Vy_<0) {
        if(verbose_) cout << "Use MEt parametrization from root file" << endl;
        double p0 = (jetParam_.find("param0PxWidthModel"))->second;
        double p1 = (jetParam_.find("param1PxWidthModel"))->second;
        double sigma = sumEt_*TMath::Sqrt(p0*p0/sumEt_ + p1*p1/sumEt_/sumEt_);
        Vx_  = sigma*sigma;
        Vy_  = sigma*sigma;
        Vxy_ = 0.0;
        rho_ = 0.0;
    }

    float PxMax = Px + TMath::Sqrt(Vx_*TMath::ChisquareQuantile(quantile ,1));
    float PxMin = Px - TMath::Sqrt(Vx_*TMath::ChisquareQuantile(quantile ,1));
    float PyMax = Py + TMath::Sqrt(Vy_*TMath::ChisquareQuantile(quantile ,1));
    float PyMin = Py - TMath::Sqrt(Vy_*TMath::ChisquareQuantile(quantile ,1));

    if( TMath::Abs(rho_)<1 ) {
        double tfAtZero = (1/(1-rho_*rho_))*( Px*Px/Vx_ + Py*Py/Vy_ - 2*rho_*Px*Py/TMath::Sqrt(Vx_*Vy_)  );
        if( tfAtZero <= chi2Cut ) {
            if(verbose_)
                cout << "(0,0) is inside the 2-sigma CL => integrate over -pi/+pi" << endl;
        }
        else {
            if(verbose_)
                cout << "(0,0) is outside the 2-sigma CL => find phi-window with interpolation..." << endl;

            //find phiLow
            bool stopPhiScan = false;
            for(unsigned int step = 0; step<= (unsigned int)(PI/phiStep) && !stopPhiScan; step++) {
                float phi = Phi - step*phiStep;
                if(phi<0)    phi = 2*PI-phi;
                if(phi>2*PI) phi = -2*PI+phi;
                float sin = TMath::Sin(phi);
                float cos = TMath::Cos(phi);
                bool crossing    = false;
                bool exceeded    = false;
                bool alreadyInTheBox = PxMax*PxMin<=0 &&  PyMax*PyMin<=0;
                for(unsigned int stepP = 0; stepP<1000 && !exceeded && !crossing && !stopPhiScan; stepP++) {

                    if( alreadyInTheBox && (stepP*cos>PxMax ||  stepP*cos<PxMin || stepP*sin>PyMax ||  stepP*sin<PyMin)) {
                        exceeded = true;
                        continue;
                    }
                    else if( !alreadyInTheBox && (stepP*cos>PxMax ||  stepP*cos<PxMin || stepP*sin>PyMax ||  stepP*sin<PyMin)) {
                        continue;
                    }


                    if( (1/(1-rho_*rho_))*( (stepP*cos-Px)*(stepP*cos-Px)/Vx_ + (stepP*sin-Py)*(stepP*sin-Py)/Vy_ - 2*rho_*(stepP*cos - Px)*(stepP*sin - Py)/TMath::Sqrt(Vx_*Vy_) ) < chi2Cut ) {
                        crossing = true;
                        if(verbose_) cout << "Found crossing at (" << stepP*cos << "," << stepP*sin << ")" << endl;
                    }

                }
                if(!crossing) {
                    if(verbose_) cout << "No crossing at " << phi << " => exit" << endl;
                    xLowPhi     =  phi+0.5*phiStep;
                    stopPhiScan = true;
                }
            }

            stopPhiScan = false;
            //find phiHigh
            for(unsigned int step = 0; step<= (unsigned int)(PI/phiStep)  && !stopPhiScan; step++) {
                float phi = Phi + step*phiStep;
                if(phi<0)    phi = 2*PI-phi;
                if(phi>2*PI) phi = -2*PI+phi;
                float sin = TMath::Sin(phi);
                float cos = TMath::Cos(phi);
                bool crossing    = false;
                bool exceeded    = false;
                bool alreadyInTheBox = PxMax*PxMin<=0 &&  PyMax*PyMin<=0;
                for(unsigned int stepP = 0; stepP<1000 && !exceeded && !crossing && !stopPhiScan; stepP++) {

                    if( alreadyInTheBox && (stepP*cos>PxMax ||  stepP*cos<PxMin || stepP*sin>PyMax ||  stepP*sin<PyMin)) {
                        exceeded = true;
                        continue;
                    }
                    else if( !alreadyInTheBox && (stepP*cos>PxMax ||  stepP*cos<PxMin || stepP*sin>PyMax ||  stepP*sin<PyMin)) {
                        continue;
                    }


                    if( (1/(1-rho_*rho_))*( (stepP*cos-Px)*(stepP*cos-Px)/Vx_ + (stepP*sin-Py)*(stepP*sin-Py)/Vy_ - 2*rho_*(stepP*cos - Px)*(stepP*sin - Py)/TMath::Sqrt(Vx_*Vy_) ) < chi2Cut ) {
                        crossing = true;
                        if(verbose_) cout << "Found crossing at (" << stepP*cos << "," << stepP*sin << ")" << endl;
                    }

                }
                if(!crossing) {
                    if(verbose_) cout << "No crossing at " << phi  << " => exit"  << endl;
                    xHighPhi     =  phi-0.5*phiStep;
                    stopPhiScan = true;
                }
            }

            xLowPhi  = -TMath::ACos(TMath::Cos( Phi - xLowPhi ));
            xHighPhi = +TMath::ACos(TMath::Cos( Phi - xHighPhi));

        }
    }

    return make_pair(xLowPhi,xHighPhi);

}




pair<double, double> MEIntegratorNew::getJetEnergyCI(float eta, float Erec, string flavor, float quantile) {

    double Elow  = 0.;
    double Ehigh = 1000.;

    float chi2Cut = TMath::ChisquareQuantile(quantile ,1);

    string bin = "Bin0";
    if(  TMath::Abs( eta )<1.0 ) bin = "Bin0";
    else bin = "Bin1";

    float Egen  = Erec;
    float sigma = 0.;
    double mean = 0.;

    double param0resol = (jetParam_.find("param0resol"+flavor+bin))->second;
    double param1resol = (jetParam_.find("param1resol"+flavor+bin))->second;
    double param2resol = (jetParam_.find("param2resol"+flavor+bin))->second;
    double param0resp  = (jetParam_.find("param0resp" +flavor+bin))->second;
    double param1resp  = (jetParam_.find("param1resp" +flavor+bin))->second;

    //sigma = Egen*TMath::Sqrt( (param0resol*param0resol)/Egen + (param1resol*param1resol)/Egen/Egen );
    //mean  = (Egen*param0resp + param1resp);
    sigma = TMath::Sqrt( (param0resol*param0resol) + Egen*(param1resol*param1resol) + Egen*Egen*(param2resol*param2resol) );
    mean  = (Egen*param0resp + param1resp);


    float GevStep = (sigma/10.);
    while( (Erec-mean)*(Erec-mean)/sigma/sigma < chi2Cut && Egen>0 && Egen<8000.) {
        Egen -= GevStep;
        sigma = TMath::Sqrt( (param0resol*param0resol) + Egen*(param1resol*param1resol) + Egen*Egen*(param2resol*param2resol) );
        mean  = (Egen*param0resp + param1resp);
        //sigma = Egen*TMath::Sqrt( (param0resol*param0resol)/Egen + (param1resol*param1resol)/Egen/Egen );
        //mean  = (Egen*param0resp + param1resp);
    }
    Elow = Egen;

    Egen  = Erec;
    sigma = TMath::Sqrt( (param0resol*param0resol) + Egen*(param1resol*param1resol) + Egen*Egen*(param2resol*param2resol) );
    mean  = (Egen*param0resp + param1resp);
    //sigma = Egen*TMath::Sqrt( (param0resol*param0resol)/Egen + (param1resol*param1resol)/Egen/Egen );
    //mean  = (Egen*param0resp + param1resp);

    while( (Erec-mean)*(Erec-mean)/sigma/sigma < chi2Cut && Egen>0 && Egen<8000.) {
        Egen += GevStep;
        sigma = TMath::Sqrt( (param0resol*param0resol) + Egen*(param1resol*param1resol) + Egen*Egen*(param2resol*param2resol) );
        mean  = (Egen*param0resp + param1resp);
        //sigma = Egen*TMath::Sqrt( (param0resol*param0resol)/Egen + (param1resol*param1resol)/Egen/Egen );
        //mean  = (Egen*param0resp + param1resp);
    }
    Ehigh = Egen;

    return make_pair(Elow,Ehigh);
}


pair<double, double> MEIntegratorNew::getBLepEnergyCI( float quantile ) {
    return getJetEnergyCI( jets_[2].Eta(), jets_[2].E(), "Heavy", quantile);
}

pair<double, double> MEIntegratorNew::getW1JetEnergyCI( float quantile ) {
    return getJetEnergyCI( jets_[3].Eta(), jets_[3].E(), "Light", quantile);
}

pair<double, double> MEIntegratorNew::getW2JetEnergyCI( float quantile ) {
    return getJetEnergyCI( jets_[4].Eta(), jets_[4].E(), "Light", quantile);
}

pair<double, double> MEIntegratorNew::getBHadEnergyCI( float quantile ) {
    return getJetEnergyCI( jets_[5].Eta(), jets_[5].E(), "Heavy", quantile);
}

pair<double, double> MEIntegratorNew::getB1EnergyCI( float quantile ) {
    return getJetEnergyCI( jets_[6].Eta(), jets_[6].E(), "Heavy", quantile);
}

pair<double, double> MEIntegratorNew::getB2EnergyCI( float quantile ) {
    return getJetEnergyCI( jets_[7].Eta(), jets_[7].E(), "Heavy", quantile);
}


TLorentzVector MEIntegratorNew::jetAt(unsigned int pos) {
    if( pos>7) return TLorentzVector(TVector3(1,0,0), 1);
    else return jets_[pos];
}



bool MEIntegratorNew::compatibilityCheck(float quantile, int print, double& mass, double& massLow, double& massHigh) {

    pair<double,double> boundsH1 = getB1EnergyCI(quantile);
    pair<double,double> boundsH2 = getB2EnergyCI(quantile);

    TLorentzVector h1Low, h2Low;
    h1Low.SetPtEtaPhiM( (boundsH1.first/jets_[6].E())*jets_[6].Pt(), jets_[6].Eta(), jets_[6].Phi(), (boundsH1.first/jets_[6].E())*jets_[6].M()  );
    h2Low.SetPtEtaPhiM( (boundsH2.first/jets_[7].E())*jets_[7].Pt(), jets_[7].Eta(), jets_[7].Phi(), (boundsH2.first/jets_[7].E())*jets_[7].M()  );

    TLorentzVector h1High, h2High;
    h1High.SetPtEtaPhiM( (boundsH1.second/jets_[6].E())*jets_[6].Pt(), jets_[6].Eta(), jets_[6].Phi(), (boundsH1.second/jets_[6].E())*jets_[6].M()  );
    h2High.SetPtEtaPhiM( (boundsH2.second/jets_[7].E())*jets_[7].Pt(), jets_[7].Eta(), jets_[7].Phi(), (boundsH2.second/jets_[7].E())*jets_[7].M()  );

    mass     =  (jets_[6] + jets_[7]).M();
    massLow  =  (h1Low+h2Low).M();
    massHigh =  (h1High+h2High).M();

    bool isCompatible = (M_>=massLow && M_<=massHigh);
    if(!isCompatible) {
        if(verbose_ || print) printf("H-Comp: %.0f CL for Mjj=%.0f is [-%.0f,+%.0f]; M=%.0f is outside\n",quantile*100, mass , massLow, massHigh, M_);
    }


    return isCompatible;

}

bool MEIntegratorNew::compatibilityCheck_WHad(float quantile, int print, double& mass, double& massLow, double& massHigh) {

    pair<double,double> boundsW1 = getW1JetEnergyCI(quantile);
    pair<double,double> boundsW2 = getW2JetEnergyCI(quantile);

    TLorentzVector w1Low, w2Low;
    w1Low.SetPtEtaPhiM( (boundsW1.first/jets_[3].E())*jets_[3].Pt(), jets_[3].Eta(), jets_[3].Phi(), (boundsW1.first/jets_[3].E())*jets_[3].M()  );
    w2Low.SetPtEtaPhiM( (boundsW2.first/jets_[4].E())*jets_[4].Pt(), jets_[4].Eta(), jets_[4].Phi(), (boundsW2.first/jets_[4].E())*jets_[4].M()  );

    TLorentzVector w1High, w2High;
    w1High.SetPtEtaPhiM( (boundsW1.second/jets_[3].E())*jets_[3].Pt(), jets_[3].Eta(), jets_[3].Phi(), (boundsW1.second/jets_[3].E())*jets_[3].M()  );
    w2High.SetPtEtaPhiM( (boundsW2.second/jets_[4].E())*jets_[4].Pt(), jets_[4].Eta(), jets_[4].Phi(), (boundsW2.second/jets_[4].E())*jets_[4].M()  );

    mass     =  (jets_[3] + jets_[4]).M();
    massLow  =  (w1Low+w2Low).M();
    massHigh =  (w1High+w2High).M();

    bool isCompatible = (Mw_>=massLow && Mw_<=massHigh);
    if(!isCompatible) {
        if(verbose_ || print) printf("W-Comp: %.0f CL for Mjj=%.0f is [-%.0f,+%.0f]; M=%.0f is outside\n",quantile*100, mass , massLow, massHigh, Mw_);
    }


    return isCompatible;

}

bool MEIntegratorNew::compatibilityCheck_TopHad(float quantile, int print, double& mass, double& massLow, double& massHigh) {

    pair<double,double> boundsW1   = getW1JetEnergyCI (quantile);
    pair<double,double> boundsW2   = getW2JetEnergyCI (quantile);
    pair<double,double> boundsBHad = getBHadEnergyCI  (quantile);

    TLorentzVector w1Low, w2Low, bHadLow;
    w1Low.SetPtEtaPhiM  ( (boundsW1.first/jets_[3].E())*jets_[3].Pt(),   jets_[3].Eta(), jets_[3].Phi(), (boundsW1.first/jets_[3].E())  *jets_[3].M()  );
    w2Low.SetPtEtaPhiM  ( (boundsW2.first/jets_[4].E())*jets_[4].Pt(),   jets_[4].Eta(), jets_[4].Phi(), (boundsW2.first/jets_[4].E())  *jets_[4].M()  );
    bHadLow.SetPtEtaPhiM( (boundsBHad.first/jets_[5].E())*jets_[5].Pt(), jets_[5].Eta(), jets_[5].Phi(), (boundsBHad.first/jets_[5].E())*jets_[5].M()  );

    TLorentzVector w1High, w2High, bHadHigh;
    w1High.SetPtEtaPhiM  ( (boundsW1.second/jets_[3].E())*jets_[3].Pt(),   jets_[3].Eta(), jets_[3].Phi(), (boundsW1.second/jets_[3].E())  *jets_[3].M()  );
    w2High.SetPtEtaPhiM  ( (boundsW2.second/jets_[4].E())*jets_[4].Pt(),   jets_[4].Eta(), jets_[4].Phi(), (boundsW2.second/jets_[4].E())  *jets_[4].M()  );
    bHadHigh.SetPtEtaPhiM( (boundsBHad.second/jets_[5].E())*jets_[5].Pt(), jets_[5].Eta(), jets_[5].Phi(), (boundsBHad.second/jets_[5].E())*jets_[5].M()  );

    mass     =  (jets_[3] + jets_[4] + jets_[5]).M();
    massLow  =  (w1Low+w2Low+bHadLow).M();
    massHigh =  (w1High+w2High+bHadHigh).M();

    bool isCompatible = (Mtop_>=massLow && Mtop_<=massHigh);
    if(!isCompatible) {
        if(verbose_ || print) printf("T-Comp: %.0f CL for Mjj=%.0f is [-%.0f,+%.0f]; M=%.0f is outside\n",quantile*100, mass , massLow, massHigh, Mtop_);
    }


    return isCompatible;

}

double MEIntegratorNew::jetEnergyTF(float eta, double Erec, double Egen, const string flavor) const {

    const string bin = TMath::Abs( eta )<1.0 ? "Bin0" : "Bin1"; 
    //if(  TMath::Abs( eta )<1.0 ) bin = "Bin0";
    //else bin = "Bin1";

    if( useRefinedTF_==0 || flavor.find("Light")!=string::npos) {

        double param0resol = (jetParam_.find("param0resol"+flavor+bin))->second;
        double param1resol = (jetParam_.find("param1resol"+flavor+bin))->second;
        double param2resol = (jetParam_.find("param2resol"+flavor+bin))->second;
        double param0resp  = (jetParam_.find("param0resp" +flavor+bin))->second;
        double param1resp  = (jetParam_.find("param1resp" +flavor+bin))->second;

        double sigma = TMath::Sqrt( (param0resol*param0resol) + Egen*(param1resol*param1resol) + Egen*Egen*(param2resol*param2resol) );
        double mean  = (Egen*param0resp + param1resp);

        return ( TMath::Gaus(Erec, mean, sigma, 1) );
    }
    else if( useRefinedTF_==1 && flavor.find("Heavy")!=string::npos ) {

        double param0resolG1 = (jetParam_.find("param0resolG1"+flavor+bin))->second;
        double param1resolG1 = (jetParam_.find("param1resolG1"+flavor+bin))->second;
        double param2resolG1 = (jetParam_.find("param2resolG1"+flavor+bin))->second;
        double param0resolG2 = (jetParam_.find("param0resolG2"+flavor+bin))->second;
        double param1resolG2 = (jetParam_.find("param1resolG2"+flavor+bin))->second;
        double param2resolG2 = (jetParam_.find("param2resolG2"+flavor+bin))->second;
        double param0respG1  = (jetParam_.find("param0respG1"+flavor+bin))->second;
        double param1respG1  = (jetParam_.find("param1respG1"+flavor+bin))->second;
        double param0respG2  = (jetParam_.find("param0respG2"+flavor+bin))->second;
        double param1respG2  = (jetParam_.find("param1respG2"+flavor+bin))->second;

        double sigma1 = TMath::Sqrt( param0resolG1*param0resolG1 + Egen*param1resolG1*param1resolG1 + Egen*Egen*param2resolG1*param2resolG1);
        double mean1  = param0respG1*Egen + param1respG1;

        double sigma2 = TMath::Sqrt( param0resolG2*param0resolG2 + Egen*param1resolG2*param1resolG2 + Egen*Egen*param2resolG2*param2resolG2);
        double mean2  = param0respG2*Egen + param1respG2;

        return (0.65*TMath::Gaus(Erec, mean1, sigma1, 1) + 0.35*TMath::Gaus(Erec, mean2, sigma2, 1));

    }
    else {}


    return 1.0;
}



bool MEIntegratorNew::smearByTF(float ptCut, int print) {

    if(Vx_<0 || Vy_<0) {
        if(verbose_) cout << "Use MEt parametrization from root file" << endl;
        double p0 = (jetParam_.find("param0PxWidthModel"))->second;
        double p1 = (jetParam_.find("param1PxWidthModel"))->second;
        double sigma = sumEt_*TMath::Sqrt(p0*p0/sumEt_ + p1*p1/sumEt_/sumEt_);
        Vx_  = sigma*sigma;
        Vy_  = sigma*sigma;
        Vxy_ = 0.0;
        rho_ = 0.0;
    }

    if(TMath::Abs(rho_)>1) {
        cout << "MEt correlation has problems.. return" << endl;
        return false;
    }


    double Px = ran_->Gaus( 0., 1.);
    double Py = ran_->Gaus( 0., 1.);
    Py = TMath::Sqrt(1-rho_*rho_)*Py + rho_*Px;

    Px = jets_[1].Px() + TMath::Sqrt(Vx_)*Px;
    Py = jets_[1].Py() + TMath::Sqrt(Vy_)*Py;

    if( constrainToRecoil_ ) {
        // smear the recoil
        if(intType_ == SL2wj) {
            Px =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]+jets_[5]+jets_[6]+jets_[7]).Px() + TMath::Sqrt(Vx_)*Px ;
            Py =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]+jets_[5]+jets_[6]+jets_[7]).Py() + TMath::Sqrt(Vy_)*Py ;
        }
        if(intType_ == SL1wj) {
            Px =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]/*+jets_[4]*/+jets_[5]+jets_[6]+jets_[7]).Px() + TMath::Sqrt(Vx_)*Px ;
            Py =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]/*+jets_[4]*/+jets_[5]+jets_[6]+jets_[7]).Py() + TMath::Sqrt(Vy_)*Py ;
        }
        if(intType_ == SLNoBHad) {
            Px =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]/*+jets_[5]*/+jets_[6]+jets_[7]).Px() + TMath::Sqrt(Vx_)*Px ;
            Py =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]/*+jets_[5]*/+jets_[6]+jets_[7]).Py() + TMath::Sqrt(Vy_)*Py ;
        }
        if(intType_ == SLNoBLep) {
            Px =  -(jets_[0]+jets_[1]/*+jets_[2]*/+jets_[3]+jets_[4]+jets_[5]+jets_[6]+jets_[7]).Px() + TMath::Sqrt(Vx_)*Px ;
            Py =  -(jets_[0]+jets_[1]/*+jets_[2]*/+jets_[3]+jets_[4]+jets_[5]+jets_[6]+jets_[7]).Py() + TMath::Sqrt(Vy_)*Py ;
        }
        if(intType_ == SLNoHiggs || intType_ == SL3b ) {
            Px =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]+jets_[5]+jets_[6]/*+jets_[7]*/).Px() + TMath::Sqrt(Vx_)*Px ;
            Py =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]+jets_[5]+jets_[6]/*+jets_[7]*/).Py() + TMath::Sqrt(Vy_)*Py ;
        }
        if(intType_ == DL) {
            Px =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]/*+jets_[4]*/+jets_[5]+jets_[6]+jets_[7]).Px() + TMath::Sqrt(Vx_)*Px;
            Py =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]/*+jets_[4]*/+jets_[5]+jets_[6]+jets_[7]).Py() + TMath::Sqrt(Vy_)*Py;
        }
    }

    //cout << "Px gen = " << Px << endl;

    ////////// DEBUG /////////////
    //Px = jets_[1].Px() ;
    //Py = jets_[1].Py() ;
    /////////////////////////////


    std::vector<double> vsE;
    for(unsigned int j = 2; j <8; j++) {

        string flavor = "Light";
        if(j==2 || j>=5) flavor = "Heavy";

        string bin = "Bin0";
        if(  TMath::Abs( jets_[j].Eta() )<1.0 )
            bin = "Bin0";
        else
            bin = "Bin1";

        double param0resol = (jetParam_.find("param0resol"+flavor+bin))->second;
        double param1resol = (jetParam_.find("param1resol"+flavor+bin))->second;
        double param2resol = (jetParam_.find("param2resol"+flavor+bin))->second;

        double param0resp  = (jetParam_.find("param0resp" +flavor+bin))->second;
        double param1resp  = (jetParam_.find("param1resp" +flavor+bin))->second;

        /////////////// DEBUG ///////////////
        //double p = ran_->Gaus( param0resp*jets_[j].E() + param1resp,
        //		   jets_[j].E()*TMath::Sqrt( param0resol*param0resol/jets_[j].E() + param1resol*param1resol/jets_[j].E()/jets_[j].E())  );
        double p = ran_->Gaus( param0resp*jets_[j].E() + param1resp,
                               TMath::Sqrt( (param0resol*param0resol) +
                                            jets_[j].E()*(param1resol*param1resol) +
                                            jets_[j].E()*jets_[j].E()*(param2resol*param2resol) ) );
        /////////////////////////////////////

        p = TMath::Max(0.0,p);

        vsE.push_back( p );
    }

    TLorentzVector sLep = jets_[0];

    TLorentzVector sBLep (  eBLep_*TMath::Sqrt(vsE[0]*vsE[0] - Mb_*Mb_), vsE[0] );
    TLorentzVector sW1Had(  eW1Had_*vsE[1], vsE[1]);
    if( intType_ == DL )
        sW1Had = jets_[3];
    TLorentzVector sW2Had(  eW2Had_*vsE[2], vsE[2]);
    TLorentzVector sBHad (  eBHad_*TMath::Sqrt(vsE[3]*vsE[3] - Mb_*Mb_), vsE[3]);
    TLorentzVector sB1   (  eB1_  *TMath::Sqrt(vsE[4]*vsE[4] - Mb_*Mb_), vsE[4]);
    TLorentzVector sB2   (  eB2_  *TMath::Sqrt(vsE[5]*vsE[5] - Mb_*Mb_), vsE[5]);

    TLorentzVector sNeut;
    sNeut.SetPxPyPzE( Px, Py, 0.0, TMath::Sqrt(Px*Px + Py*Py));

    if( constrainToRecoil_ ) {
        double nuX = Px;
        double nuY = Py;
        if( intType_ == SL2wj ) {
            nuX = -(Px+sLep.Px()+sBLep.Px()+sW1Had.Px()+sW2Had.Px()+sBHad.Px()+sB1.Px()+sB2.Px());
            nuY = -(Py+sLep.Py()+sBLep.Py()+sW1Had.Py()+sW2Had.Py()+sBHad.Py()+sB1.Py()+sB2.Py());
        }
        if( intType_ == SL1wj ) {
            nuX = -(Px+sLep.Px()+sBLep.Px()+sW1Had.Px()/*+sW2Had.Px()*/+sBHad.Px()+sB1.Px()+sB2.Px());
            nuY = -(Py+sLep.Py()+sBLep.Py()+sW1Had.Py()/*+sW2Had.Py()*/+sBHad.Py()+sB1.Py()+sB2.Py());
        }
        if( intType_ == SLNoBHad ) {
            nuX = -(Px+sLep.Px()+sBLep.Px()+sW1Had.Px()+sW2Had.Px()/*+sBHad.Px()*/+sB1.Px()+sB2.Px());
            nuY = -(Py+sLep.Py()+sBLep.Py()+sW1Had.Py()+sW2Had.Py()/*+sBHad.Py()*/+sB1.Py()+sB2.Py());
        }
        if( intType_ == SLNoBLep ) {
            nuX = -(Px+sLep.Px()/*+sBLep.Px()*/+sW1Had.Px()+sW2Had.Px()+sBHad.Px()+sB1.Px()+sB2.Px());
            nuY = -(Py+sLep.Py()/*+sBLep.Py()*/+sW1Had.Py()+sW2Had.Py()+sBHad.Py()+sB1.Py()+sB2.Py());
        }
        if( intType_ == SLNoHiggs || intType_ == SL3b ) {
            nuX = -(Px+sLep.Px()+sBLep.Px()+sW1Had.Px()+sW2Had.Px()+sBHad.Px()+sB1.Px()/*+sB2.Px()*/);
            nuY = -(Py+sLep.Py()+sBLep.Py()+sW1Had.Py()+sW2Had.Py()+sBHad.Py()+sB1.Py()/*+sB2.Py()*/);
        }
        if( intType_ == DL ) {
            nuX = -(Px+sLep.Px()+sBLep.Px()+sW1Had.Px()/*+sW2Had.Px()*/+sBHad.Px()+sB1.Px()+sB2.Px());
            nuY = -(Py+sLep.Py()+sBLep.Py()+sW1Had.Py()/*+sW2Had.Py()*/+sBHad.Py()+sB1.Py()+sB2.Py());
        }
        sNeut.SetPxPyPzE( nuX, nuY, 0.,  TMath::Sqrt(nuX*nuX + nuY*nuY) );
    }

    if(verbose_ || print ) {
        cout << "lep   (input): jet0.SetPtEtaPhiM(" << jets_[0].Pt() << "," << jets_[0].Eta() << "," << jets_[0].Phi() << "," << jets_[0].M() << ")" << endl;
        cout << "met   (input): jet1.SetPtEtaPhiM(" << jets_[1].Pt() << "," << jets_[1].Eta() << "," << jets_[1].Phi() << "," << jets_[1].M() << ")" << endl;
        cout << "bLep  (input): jet2.SetPtEtaPhiM(" << jets_[2].Pt() << "," << jets_[2].Eta() << "," << jets_[2].Phi() << "," << jets_[2].M() << ")" << endl;
        cout << "w1    (input): jet3.SetPtEtaPhiM(" << jets_[3].Pt() << "," << jets_[3].Eta() << "," << jets_[3].Phi() << "," << jets_[3].M() << ")" << endl;
        cout << "w2    (input): jet4.SetPtEtaPhiM(" << jets_[4].Pt() << "," << jets_[4].Eta() << "," << jets_[4].Phi() << "," << jets_[4].M() << ")" << endl;
        cout << "bHad  (input): jet5.SetPtEtaPhiM(" << jets_[5].Pt() << "," << jets_[5].Eta() << "," << jets_[5].Phi() << "," << jets_[5].M() << ")" << endl;
        cout << "h1    (input): jet6.SetPtEtaPhiM(" << jets_[6].Pt() << "," << jets_[6].Eta() << "," << jets_[6].Phi() << "," << jets_[6].M() << ")" << endl;
        cout << "h2    (input): jet7.SetPtEtaPhiM(" << jets_[7].Pt() << "," << jets_[7].Eta() << "," << jets_[7].Phi() << "," << jets_[7].M() << ")" << endl;
        cout << " ********************* " << endl;
    }

    jets_.clear();
    jets_.push_back( sLep  );
    jets_.push_back( sNeut );
    jets_.push_back( sBLep );
    jets_.push_back( sW1Had);
    jets_.push_back( sW2Had);
    jets_.push_back( sBHad );
    jets_.push_back( sB1 );
    jets_.push_back( sB2 );

    jets_backup_.clear();
    jets_backup_.push_back( sLep  );
    jets_backup_.push_back( sNeut );
    jets_backup_.push_back( sBLep );
    jets_backup_.push_back( sW1Had);
    jets_backup_.push_back( sW2Had);
    jets_backup_.push_back( sBHad );
    jets_backup_.push_back( sB1 );
    jets_backup_.push_back( sB2 );

    if(intType_ == SL1wj) {
        TLorentzVector w1 = jets_[3];
        TLorentzVector w2 = jets_[4];
        if( (w1.Pt()<ptCut || TMath::Abs(w1.Eta())>2.5) && (w2.Pt()>ptCut && TMath::Abs(w2.Eta())<2.5)) {
            jets_[3] = w2;
            jets_[4] = w1;
            jets_backup_[3] = w2;
            jets_backup_[4] = w1;
        }
        else if( (w2.Pt()<ptCut || TMath::Abs(w2.Eta())>2.5) && (w1.Pt()>ptCut && TMath::Abs(w1.Eta())<2.5)) {
            jets_[3] = w1;
            jets_[4] = w2;
            jets_backup_[3] = w1;
            jets_backup_[4] = w2;
        }
        else {
            cout << "smearByTF: Inconsistentcy of mode and jet selections" << endl;
            return false;
        }
    }


    if(intType_ == SLNoHiggs ) {
        TLorentzVector h1 = jets_[6];
        TLorentzVector h2 = jets_[7];
        if( (h1.Pt()<ptCut || TMath::Abs(h1.Eta())>2.5) && (h2.Pt()>ptCut && TMath::Abs(h2.Eta())<2.5)) {
            jets_[6] = h2;
            jets_[7] = h1;
            jets_backup_[6] = h2;
            jets_backup_[7] = h1;
        }
        else if( (h2.Pt()<ptCut || TMath::Abs(h2.Eta())>2.5) && (h1.Pt()>ptCut && TMath::Abs(h1.Eta())<2.5)) {
            jets_[6] = h1;
            jets_[7] = h2;
            jets_backup_[6] = h1;
            jets_backup_[7] = h2;
        }
        else {
            cout << "smearByTF: Inconsistentcy of mode and jet selections" << endl;
            return false;
        }
    }

    if(intType_ == SL3b ) {
        TLorentzVector h1 = jets_[6];
        TLorentzVector h2 = jets_[7];
        if( (h1.Pt()<ptCut || TMath::Abs(h1.Eta())>2.5) && (h2.Pt()>ptCut && TMath::Abs(h2.Eta())<2.5)) {
            jets_[6] = h2;
            jets_[7] = h1;
            jets_backup_[6] = h2;
            jets_backup_[7] = h1;
        }
        else if( (h2.Pt()<ptCut || TMath::Abs(h2.Eta())>2.5) && (h1.Pt()>ptCut && TMath::Abs(h1.Eta())<2.5)) {
            jets_[6] = h1;
            jets_[7] = h2;
            jets_backup_[6] = h1;
            jets_backup_[7] = h2;
        }
        else {}
    }


    if(verbose_ || print) {
        cout << "lep   (output): jet0.SetPtEtaPhiM(" << jets_[0].Pt() << "," << jets_[0].Eta() << "," << jets_[0].Phi() << "," << jets_[0].M() << ")" << endl;
        cout << "met   (output): jet1.SetPtEtaPhiM(" << jets_[1].Pt() << "," << jets_[1].Eta() << "," << jets_[1].Phi() << "," << jets_[1].M() << ")" << endl;
        cout << "bLep  (output): jet2.SetPtEtaPhiM(" << jets_[2].Pt() << "," << jets_[2].Eta() << "," << jets_[2].Phi() << "," << jets_[2].M() << ")" << endl;
        cout << "w1    (output): jet3.SetPtEtaPhiM(" << jets_[3].Pt() << "," << jets_[3].Eta() << "," << jets_[3].Phi() << "," << jets_[3].M() << ")" << endl;
        cout << "w2    (output): jet4.SetPtEtaPhiM(" << jets_[4].Pt() << "," << jets_[4].Eta() << "," << jets_[4].Phi() << "," << jets_[4].M() << ")" << endl;
        cout << "bHad  (output): jet5.SetPtEtaPhiM(" << jets_[5].Pt() << "," << jets_[5].Eta() << "," << jets_[5].Phi() << "," << jets_[5].M() << ")" << endl;
        cout << "h1    (output): jet6.SetPtEtaPhiM(" << jets_[6].Pt() << "," << jets_[6].Eta() << "," << jets_[6].Phi() << "," << jets_[6].M() << ")" << endl;
        cout << "h2    (output): jet7.SetPtEtaPhiM(" << jets_[7].Pt() << "," << jets_[7].Eta() << "," << jets_[7].Phi() << "," << jets_[7].M() << ")" << endl;
    }

    if(intType_ == SL2wj)
        return (sBLep.Pt()>ptCut && sW1Had.Pt()>ptCut && sW2Had.Pt()>ptCut && sBHad.Pt()>ptCut && sB1.Pt()>ptCut && sB2.Pt()>ptCut);

    else if( intType_ == SL1wj )
        return (sBLep.Pt()>ptCut && ( (jets_[3].Pt()>ptCut && TMath::Abs(jets_[3].Eta())<2.5) && (jets_[4].Pt()<ptCut || TMath::Abs(jets_[4].Eta())>2.5) ) && sBHad.Pt()>ptCut && sB1.Pt()>ptCut && sB2.Pt()>ptCut);

    else if( intType_ == SLNoBHad )
        return (sBLep.Pt()>ptCut && sW1Had.Pt()>ptCut && sW2Had.Pt()>ptCut && (sBHad.Pt()<ptCut || TMath::Abs(sBHad.Eta())>2.5) && sB1.Pt()>ptCut && sB2.Pt()>ptCut);

    else if( intType_ == SLNoBLep )
        return ( (sBLep.Pt()<ptCut || TMath::Abs(sBLep.Eta())>2.5) && sW1Had.Pt()>ptCut && sW2Had.Pt()>ptCut && sBHad.Pt()>ptCut && sB1.Pt()>ptCut && sB2.Pt()>ptCut);

    else if( intType_ == SLNoHiggs )
        return (sBLep.Pt()>ptCut && sW1Had.Pt()>ptCut && sW2Had.Pt()>ptCut && sBHad.Pt()>ptCut && ( (jets_[6].Pt()>ptCut && TMath::Abs(jets_[6].Eta())<2.5) && (jets_[7].Pt()<ptCut || TMath::Abs(jets_[7].Eta())>2.5) ) );

    else if( intType_ == SL3b )
        return ( ( sBLep.Pt()>ptCut && sW1Had.Pt()>ptCut && sW2Had.Pt()>ptCut && (sBHad.Pt()<ptCut || TMath::Abs(sBHad.Eta())>2.5) && sB1.Pt()>ptCut && sB2.Pt()>ptCut)  ||
                 ((sBLep.Pt()<ptCut || TMath::Abs(sBLep.Eta())>2.5) && sW1Had.Pt()>ptCut && sW2Had.Pt()>ptCut && sBHad.Pt()>ptCut && sB1.Pt()>ptCut && sB2.Pt()>ptCut) ||
                 ( sBLep.Pt()>ptCut && sW1Had.Pt()>ptCut && sW2Had.Pt()>ptCut && sBHad.Pt()>ptCut && ( (jets_[6].Pt()>ptCut && TMath::Abs(jets_[6].Eta())<2.5) && (jets_[7].Pt()<ptCut || TMath::Abs(jets_[7].Eta())>2.5) ) ) );

    else if( intType_ == DL )
        return (sBLep.Pt()>ptCut /*&& sW1Had.Pt()>ptCut && sW2Had.Pt()>ptCut*/ && sBHad.Pt()>ptCut && sB1.Pt()>ptCut && sB2.Pt()>ptCut);

    else {}

    return true;
}


void MEIntegratorNew::setPartonLuminosity(TH1F* h) {
    partonLuminosity_ =  h;
}

void MEIntegratorNew::setMass(double mass) {
    resetEvaluation();
    M_    = mass;
    dMh2_ = (M_*M_-2*Mb_*Mb_)*0.5;
}

void MEIntegratorNew::setQ(double Q) {
    Q_    = Q;
}

void MEIntegratorNew::setSqrtS(double S) {
    SqrtS_    = S;
}

void MEIntegratorNew::setTopMass(double massTop, double massW) {
    Mtop_    = massTop;
    Mw_      = massW;
    pStar_  =  TMath::Sqrt( (massTop*massTop-(massW+Mb_)*(massW+Mb_) )*( massTop*massTop-(massW-Mb_)*(massW-Mb_) ) )/2./massTop;
    EbStar_ =  (massTop*massTop - massW*massW + Mb_*Mb_)/2./massTop;
    EWStar_ =  (massTop*massTop + massW*massW - Mb_*Mb_)/2./massTop;
    EuStar_ =  massW/2;
    dM2_    =  (massTop*massTop-Mb_*Mb_-massW*massW)*0.5;
}

void MEIntegratorNew::setSumEt(double sumEt) {
    sumEt_ = sumEt;
}

void MEIntegratorNew::setMEtCov(double Vx, double Vy, double Vxy) {
    Vx_  = Vx;
    Vy_  = Vy;
    Vxy_ = Vxy;
    rho_ = (Vx>0 && Vy>0) ? Vxy/TMath::Sqrt(Vx*Vy) : -99.;

    if(Vx_<0 || Vy_<0) {
        if(verbose_) cout << "Use MEt parametrization from root file" << endl;
        double p0 = (jetParam_.find("param0PxWidthModel"))->second;
        double p1 = (jetParam_.find("param1PxWidthModel"))->second;
        double sigma = sumEt_*TMath::Sqrt(p0*p0/sumEt_ + p1*p1/sumEt_/sumEt_);
        Vx_  = sigma*sigma;
        Vy_  = sigma*sigma;
        Vxy_ = 0.0;
        rho_ = 0.0;
        //cout << "s_x = s_y = " << sqrt(Vx_) << " (GeV), rho = 0" << endl;
    }
    else {
        //cout << "s_x = " << sqrt(Vx_) << ", s_y = " << sqrt(Vy_) << " (GeV), rho = " << rho_ << endl;
    }

    if(rho_<-1 || rho_>1)
        cout << "Invalid Cov mtrix entries... please check them" << endl;
    if(rho_>0.99 || rho_<-0.99)
        cout << "Highly correlated Px/Py can make the TF go crazy !!!" << endl;


}


void MEIntegratorNew::setPtPhiParam(int usePtPhiParam) {
    usePtPhiParam_ =  usePtPhiParam;
}

void MEIntegratorNew::setConstrainToRecoil(int constrain) {
    constrainToRecoil_ = constrain;
}

void MEIntegratorNew::setUseRefinedTF(int use) {
    useRefinedTF_ = use;
}

void MEIntegratorNew::setUseAnalyticalFormula(int use) {
    useAnalyticalFormula_ = use;
}

void MEIntegratorNew::setUseDynamicalScale(int use) {
    useDynamicalScale_ = use;
}

void MEIntegratorNew::switchOffOL() {
    top1Flag_ = 0;
    top2Flag_ = 0;
}

void MEIntegratorNew::setUseME   (int use) {
    useME_  = use;
}
void MEIntegratorNew::setUseJac  (int use) {
    useJac_ = use;
}
void MEIntegratorNew::setUseMET  (int use) {
    useMET_ = use;
}
void MEIntegratorNew::setUseTF   (int use) {
    useTF_  = use;
}
void MEIntegratorNew::setUsePDF  (int use) {
    usePDF_ = use;
}

void MEIntegratorNew::setTopFlags(int flag1, int flag2) {
    top1Flag_ = flag1;
    top2Flag_ = flag2;
}

void MEIntegratorNew::setWeightNorm(NormalizationType norm) {
    normalizeToXSec_ = norm;
    cout << "*** MEIntegratorNew:  Weights will be divided by " ;
    if( norm == None ) cout << "1" << endl;
    if( norm == xSec ) cout << "the inclusive cross-section" << endl;
    if( norm == Acc )  cout << "the cross-section in acceptance" << endl;
    return;
}

int MEIntegratorNew::topHadEnergies(double E1, double& E2, double& E3, double& cos1, double& cos2, int& errFlag ) const {

    int nSol = 0;

    double a12 = eW1Had_.Angle(eW2Had_);
    double a13 = eW1Had_.Angle(eBHad_);
    double a23 = eW2Had_.Angle(eBHad_);

    E2 = Mw_*Mw_/E1/(4*TMath::Sin(a12/2.)*TMath::Sin(a12/2.));

    double a = E1+E2;
    double b = E1*TMath::Cos(a13)+E2*TMath::Cos(a23);

    if( (dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_) < 0) {
        errFlag = 1;
        return nSol;
    }

    double E3_1 =  (a*dM2_ + b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;
    double E3_2 =  (a*dM2_ - b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;

    double E3tmp1 = -999.;
    double E3tmp2 = -999.;

    if( b>0 ) {
        if(E3_1>dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2>dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }
    else {
        if(E3_1<dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2<dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }

    if( E3tmp1>0 && E3tmp2>0 )
        E3 = TMath::Max( E3tmp1,E3tmp2 );
    else if( E3tmp1>0 &&  E3tmp2<0)
        E3 = E3tmp1;
    else if( E3tmp1<0 &&  E3tmp2>0)
        E3 = E3tmp2;
    else {
        errFlag = 1;
        return nSol;
    }

    if(E3<Mb_) {
        errFlag = 1;
        return nSol;
    }

    TLorentzVector w1 ( eW1Had_*E1,   E1);
    TLorentzVector w2 ( eW2Had_*E2,   E2);
    TLorentzVector blv( eBHad_*(TMath::Sqrt(E3*E3 - Mb_*Mb_)), E3);


    TVector3 boost = (w1+w2+blv).BoostVector();
    w1.Boost(  -boost );
    w2.Boost(  -boost );
    blv.Boost( -boost );

    cos1 = TMath::Cos( blv.Angle(boost) );

    TVector3 boostW = (w1+w2).BoostVector();
    w1.Boost(  -boostW );
    w2.Boost(  -boostW );

    cos2 = TMath::Cos( w1.Angle(boostW) );

    return nSol;
}


void MEIntegratorNew::topLepEnergiesFromPtPhi(int sign , double nuPhi, double nuPt, double& Enu, double& Eb, double& cos1, double& cos2, double& Jacob, int& errFlag ) const {


    TVector3 e3T( nuPt*TMath::Cos(nuPhi), nuPt*TMath::Sin(nuPhi) , 0.);
    TVector3 e1T( jets_[0].Px(),  jets_[0].Py(), 0.);

    double rho = e1T.Dot(e3T) + Mw_*Mw_/2.;

    double a   = jets_[0].Pz()/jets_[0].P();
    double b   = rho/jets_[0].P();
    double c2 =  nuPt*nuPt - b*b;

    if( (a*a*b*b - c2*(1-a*a))<0 ) {
        errFlag = 1;
        return;
    }

    double pz1 = (a*b + sqrt(a*a*b*b - c2*(1-a*a)))/(1-a*a);
    double pz2 = (a*b - sqrt(a*a*b*b - c2*(1-a*a)))/(1-a*a);

    double pz = -999;
    if( a>0 ) {
        if( pz1 > -b/a && sign == -1) pz = pz1;
        if( pz2 > -b/a && sign == +1) pz = pz2;
    }
    else {
        if( pz1 < b/a && sign == -1) pz = pz1;
        if( pz2 < b/a && sign == +1) pz = pz2;
    }

    if( pz == -999 ) {
        errFlag = 1;
        return;
    }


    Enu = TMath::Sqrt(nuPt*nuPt + pz*pz);
    double nuTheta = pz/Enu;

    Jacob = 1.0;//TMath::Abs((1-nuTheta*nuTheta)/nuTheta);

    topLepEnergies( nuPhi, nuTheta, Enu, Eb, cos1, cos2, errFlag  );

    return;
}


void MEIntegratorNew::topLepEnergiesFromEbPhi(int sign , double nuPhi, double Eb, double& Enu, double& cosTheta, double& cos1, double& cos2,  int& errFlag ) const {

    TLorentzVector lep ( eLep_ * jets_[0].E() , jets_[0].E());
    double cosPhi = TMath::Cos(nuPhi);
    double sinPhi = TMath::Sin(nuPhi);

    TLorentzVector blv( eBLep_ * sqrt(Eb*Eb-Mb_*Mb_) , Eb);

    double betaB = TMath::Sqrt(Eb*Eb-Mb_*Mb_)/Eb;
    double M2 = Mtop_*Mtop_ - Mw_*Mw_ - (lep+blv).M()*(lep+blv).M();

    if(M2<0) {
        errFlag = 1;
        return;
    }

    double K = M2/Mw_/Mw_*jets_[0].E()/Eb;

    TVector3 eLT(eLep_. Px(),eLep_. Py(),0.0 );
    TVector3 eBT(eBLep_.Px(),eBLep_.Py(),0.0 );

    TVector3 eNT( cosPhi , sinPhi ,0  );

    double a = betaB*eBLep_.Px()*eNT.Px() - K*eLep_.Px()*eNT.Px() +  betaB*eBLep_.Py()*eNT.Py() - K*eLep_.Py()*eNT.Py();
    double b = (eBLep_*betaB - K*eLep_).Pz();
    double c = K-1;

    if( (a*a + b*b - c*c)<0 ) {
        errFlag = 1;
        return;
    }

    double cosTheta1 = (-b*c + TMath::Abs(a)*sqrt( a*a + b*b - c*c))/(a*a + b*b);
    double cosTheta2 = (-b*c - TMath::Abs(a)*sqrt( a*a + b*b - c*c))/(a*a + b*b);

    double sol1 = -999;
    double sol2 = -999;

    if( a>0 ) {
        if( b>0 ) {
            if( cosTheta1 < -c/b ) {
                sol1 = cosTheta1;
            }
            if( cosTheta2 < -c/b ) {
                sol2 = cosTheta2;
            }
        }
        else {
            if( cosTheta1 > -c/b ) {
                sol1 = cosTheta1;
            }
            if( cosTheta2 > -c/b ) {
                sol2 = cosTheta2;
            }
        }
    }
    else {
        if( b>0 ) {
            if( cosTheta1 > -c/b ) {
                sol1 = cosTheta1;
            }
            if( cosTheta2 > -c/b ) {
                sol2 = cosTheta2;
            }
        }
        else {
            if( cosTheta1 < -c/b ) {
                sol1 = cosTheta1;
            }
            if( cosTheta2 < -c/b ) {
                sol2 = cosTheta2;
            }
        }
    }

    if(sol1>=-1. && sign == -1) {
        cosTheta = sol1;
        double sinTheta = sqrt(1-cosTheta*cosTheta);
        TVector3 eN( sinTheta*cosPhi, sinTheta*sinPhi ,  cosTheta);
        Enu = Mw_*Mw_/2/ jets_[0].E() / (1-eN.Dot(eLep_));
    }
    else if( sol2>=-1. && sign == +1) {
        cosTheta = sol2;
        double sinTheta = sqrt(1-cosTheta*cosTheta);
        TVector3 eN( sinTheta*cosPhi, sinTheta*sinPhi ,  cosTheta);
        Enu = Mw_*Mw_/2/  jets_[0].E() / (1-eN.Dot(eLep_));
    }
    else {
        errFlag = 1;
        return;
    }

    topLepEnergies( nuPhi, cosTheta , Enu, Eb, cos1, cos2, errFlag  );

    return;
}


int MEIntegratorNew::topLepEnergies(double nuPhi, double nuTheta, double& Enu, double& Eb, double& cos1, double& cos2, int& errFlag ) const {

    int nSol = 0;

    double Elep =  jets_[0].E();

    TVector3 e3(0.,0.,1.); // neutrino
    e3.SetTheta( TMath::ACos( nuTheta ) );
    e3.SetPhi  ( nuPhi);
    e3.SetMag  ( 1.);

    double a12 = eLep_.Angle(eBLep_); // lep - b
    double a13 = eLep_.Angle(e3);     // lep - nu
    double a23 = eBLep_.Angle(e3);    // b   - nu

    Enu = Mw_*Mw_/ Elep / (4*TMath::Sin(a13/2.)*TMath::Sin(a13/2.));

    double a = Elep+Enu;
    double b = Elep*TMath::Cos(a12)+Enu*TMath::Cos(a23);

    if( (dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_) < 0) {
        errFlag = 1;
        return nSol;
    }

    double E3_1 =  (a*dM2_ + b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;
    double E3_2 =  (a*dM2_ - b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;

    double E3tmp1 = -999.;
    double E3tmp2 = -999.;

    if( b>0 ) {
        if(E3_1>dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2>dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }
    else {
        if(E3_1<dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2<dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }

    if( E3tmp1>0 && E3tmp2>0 )
        Eb = TMath::Max( E3tmp1,E3tmp2 );
    else if( E3tmp1>0 &&  E3tmp2<0)
        Eb = E3tmp1;
    else if( E3tmp1<0 &&  E3tmp2>0)
        Eb = E3tmp2;
    else {
        errFlag = 1;
        return nSol;
    }


    if(Eb<Mb_) {
        errFlag = 1;
        return nSol;
    }

    TLorentzVector wLep( eLep_*Elep,   Elep);
    TLorentzVector blv ( eBLep_*(TMath::Sqrt(Eb*Eb - Mb_*Mb_)), Eb);
    TLorentzVector wNu ( (e3.Unit())*Enu,    Enu);


    TVector3 boost = (wLep+wNu+blv).BoostVector();
    wLep.Boost ( -boost );
    wNu.Boost  ( -boost );
    blv.Boost  ( -boost );

    cos1 = TMath::Cos( blv.Angle(boost) );

    TVector3 boostW = (wLep+wNu).BoostVector();
    wLep.Boost( -boostW );
    wNu.Boost ( -boostW );

    cos2 = TMath::Cos( wLep.Angle(boostW) );

    return nSol;
}



int MEIntegratorNew::topLep2Energies(double nuPhi, double nuTheta, double& Enu, double& Eb, double& cos1, double& cos2, int& errFlag ) const {

    int nSol = 0;

    double Elep =  jets_[3].E(); // W1Had for DL contains the 2nd lepton

    TVector3 e3(0.,0.,1.); // neutrino
    e3.SetTheta( TMath::ACos( nuTheta ) );
    e3.SetPhi  ( nuPhi);
    e3.SetMag  ( 1.);

    double a12 = eW1Had_.Angle(eBHad_); // lep - b
    double a13 = eW1Had_.Angle(e3);     // lep - nu
    double a23 = eBHad_.Angle(e3);    // b   - nu

    Enu = Mw_*Mw_/ Elep / (4*TMath::Sin(a13/2.)*TMath::Sin(a13/2.));

    double a = Elep+Enu;
    double b = Elep*TMath::Cos(a12)+Enu*TMath::Cos(a23);

    if( (dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_) < 0) {
        errFlag = 1;
        return nSol;
    }

    double E3_1 =  (a*dM2_ + b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;
    double E3_2 =  (a*dM2_ - b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;

    double E3tmp1 = -999.;
    double E3tmp2 = -999.;

    if( b>0 ) {
        if(E3_1>dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2>dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }
    else {
        if(E3_1<dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2<dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }

    if( E3tmp1>0 && E3tmp2>0 )
        Eb = TMath::Max( E3tmp1,E3tmp2 );
    else if( E3tmp1>0 &&  E3tmp2<0)
        Eb = E3tmp1;
    else if( E3tmp1<0 &&  E3tmp2>0)
        Eb = E3tmp2;
    else {
        errFlag = 1;
        return nSol;
    }


    if(Eb<Mb_) {
        errFlag = 1;
        return nSol;
    }

    TLorentzVector wLep( eW1Had_*Elep,   Elep);
    TLorentzVector blv ( eBHad_*(TMath::Sqrt(Eb*Eb - Mb_*Mb_)), Eb);
    TLorentzVector wNu ( (e3.Unit())*Enu,    Enu);


    TVector3 boost = (wLep+wNu+blv).BoostVector();
    wLep.Boost ( -boost );
    wNu.Boost  ( -boost );
    blv.Boost  ( -boost );

    cos1 = TMath::Cos( blv.Angle(boost) );

    TVector3 boostW = (wLep+wNu).BoostVector();
    wLep.Boost( -boostW );
    wNu.Boost ( -boostW );

    cos2 = TMath::Cos( wLep.Angle(boostW) );

    return nSol;
}



int MEIntegratorNew::topLepBLostEnergies(double nuPhi, double nuTheta, double phiBLep, double cosThetaBLep,  double& Enu, double& Eb, double& cos1, double& cos2, int& errFlag ) const {

    int nSol = 0;

    double Elep =  jets_[0].E();

    TVector3 e3(0.,0.,1.); // neutrino
    e3.SetTheta( TMath::ACos( nuTheta ) );
    e3.SetPhi  ( nuPhi);
    e3.SetMag  ( 1.);

    TVector3 eMiss(0.,0.,1.); // bLep lost
    eMiss.SetTheta( TMath::ACos( cosThetaBLep ) );
    eMiss.SetPhi  ( phiBLep );
    eMiss.SetMag  ( 1.);

    double a12 = eLep_.Angle(eMiss); // lep - b
    double a13 = eLep_.Angle(e3);    // lep - nu
    double a23 = eMiss.Angle(e3);    // b   - nu

    Enu = Mw_*Mw_/ Elep / (4*TMath::Sin(a13/2.)*TMath::Sin(a13/2.));

    double a = Elep+Enu;
    double b = Elep*TMath::Cos(a12)+Enu*TMath::Cos(a23);

    if( (dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_) < 0) {
        errFlag = 1;
        return nSol;
    }

    double E3_1 =  (a*dM2_ + b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;
    double E3_2 =  (a*dM2_ - b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;

    double E3tmp1 = -999.;
    double E3tmp2 = -999.;

    if( b>0 ) {
        if(E3_1>dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2>dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }
    else {
        if(E3_1<dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2<dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }

    if( E3tmp1>0 && E3tmp2>0 )
        Eb = TMath::Max( E3tmp1,E3tmp2 );
    else if( E3tmp1>0 &&  E3tmp2<0)
        Eb = E3tmp1;
    else if( E3tmp1<0 &&  E3tmp2>0)
        Eb = E3tmp2;
    else {
        errFlag = 1;
        return nSol;
    }


    if(Eb<Mb_) {
        errFlag = 1;
        return nSol;
    }

    TLorentzVector wLep( eLep_*Elep,   Elep);
    TLorentzVector blv ( eMiss*(TMath::Sqrt(Eb*Eb - Mb_*Mb_)), Eb);
    TLorentzVector wNu ( (e3.Unit())*Enu,    Enu);


    TVector3 boost = (wLep+wNu+blv).BoostVector();
    wLep.Boost ( -boost );
    wNu.Boost  ( -boost );
    blv.Boost  ( -boost );

    cos1 = TMath::Cos( blv.Angle(boost) );

    TVector3 boostW = (wLep+wNu).BoostVector();
    wLep.Boost( -boostW );
    wNu.Boost ( -boostW );

    cos2 = TMath::Cos( wLep.Angle(boostW) );

    return nSol;
}



int MEIntegratorNew::topHadLostEnergies(double missPhi, double missTheta, double& Emiss, double E1, double& Eb, double& cos1, double& cos2, int& errFlag ) const {

    int nSol = 0;

    TVector3 eMiss(0.,0.,1.);
    eMiss.SetTheta( TMath::ACos( missTheta ) );
    eMiss.SetPhi  ( missPhi );
    eMiss.SetMag  ( 1.);

    double a12 = eW1Had_.Angle(eBHad_); // w1 - b
    double a13 = eW1Had_.Angle(eMiss);  // lep - miss
    double a23 = eBHad_. Angle(eMiss);  // b   - miss

    Emiss = Mw_*Mw_/ E1 / (4*TMath::Sin(a13/2.)*TMath::Sin(a13/2.));

    double a = E1+Emiss;
    double b = E1*TMath::Cos(a12)+Emiss*TMath::Cos(a23);

    if( (dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_) < 0) {
        errFlag = 1;
        return nSol;
    }

    double E3_1 =  (a*dM2_ + b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;
    double E3_2 =  (a*dM2_ - b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;

    double E3tmp1 = -999.;
    double E3tmp2 = -999.;

    if( b>0 ) {
        if(E3_1>dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2>dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }
    else {
        if(E3_1<dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2<dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }

    if( E3tmp1>0 && E3tmp2>0 )
        Eb = TMath::Max( E3tmp1,E3tmp2 );
    else if( E3tmp1>0 &&  E3tmp2<0)
        Eb = E3tmp1;
    else if( E3tmp1<0 &&  E3tmp2>0)
        Eb = E3tmp2;
    else {
        errFlag = 1;
        return nSol;
    }

    if(Eb<Mb_) {
        errFlag = 1;
        return nSol;
    }

    TLorentzVector w1( eW1Had_*E1,   E1);
    TLorentzVector w2( eMiss *Emiss,   Emiss);
    TLorentzVector blv ( eBHad_*(TMath::Sqrt(Eb*Eb - Mb_*Mb_)), Eb);

    TVector3 boost = (w1+w2+blv).BoostVector();
    w1.Boost ( -boost );
    w2.Boost ( -boost );
    blv.Boost( -boost );

    cos1 = TMath::Cos( blv.Angle(boost) );

    TVector3 boostW = (w1+w2).BoostVector();
    w1.Boost ( -boostW );
    w2.Boost ( -boostW );

    cos2 = TMath::Cos( w1.Angle(boostW) );

    return nSol;

}


int MEIntegratorNew::topHadBLostEnergies(double missPhi, double missTheta, double E1, double& E2, double& E3, double& cos1, double& cos2, int& errFlag ) const {

    int nSol = 0;

    TVector3 eMiss(0.,0.,1.);
    eMiss.SetTheta( TMath::ACos( missTheta ) );
    eMiss.SetPhi  ( missPhi );
    eMiss.SetMag  ( 1.);

    double a12 = eW1Had_.Angle(eW2Had_);
    double a13 = eW1Had_.Angle(eMiss);
    double a23 = eW2Had_.Angle(eMiss);

    E2 = Mw_*Mw_/E1/(4*TMath::Sin(a12/2.)*TMath::Sin(a12/2.));

    double a = E1+E2;
    double b = E1*TMath::Cos(a13)+E2*TMath::Cos(a23);

    if( (dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_) < 0) {
        errFlag = 1;
        return nSol;
    }

    double E3_1 =  (a*dM2_ + b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;
    double E3_2 =  (a*dM2_ - b*TMath::Sqrt(dM2_*dM2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b) ;

    double E3tmp1 = -999.;
    double E3tmp2 = -999.;

    if( b>0 ) {
        if(E3_1>dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2>dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }
    else {
        if(E3_1<dM2_/a) {
            E3tmp1 = E3_1;
            nSol++;
        }
        if(E3_2<dM2_/a) {
            E3tmp2 = E3_2;
            nSol++;
        }
    }

    if( E3tmp1>0 && E3tmp2>0 )
        E3 = TMath::Max( E3tmp1,E3tmp2 );
    else if( E3tmp1>0 &&  E3tmp2<0)
        E3 = E3tmp1;
    else if( E3tmp1<0 &&  E3tmp2>0)
        E3 = E3tmp2;
    else {
        errFlag = 1;
        return nSol;
    }

    if(E3<Mb_) {
        errFlag = 1;
        return nSol;
    }

    TLorentzVector w1 ( eW1Had_*E1,   E1);
    TLorentzVector w2 ( eW2Had_*E2,   E2);
    TLorentzVector blv( eMiss*(TMath::Sqrt(E3*E3 - Mb_*Mb_)), E3);


    TVector3 boost = (w1+w2+blv).BoostVector();
    w1.Boost(  -boost );
    w2.Boost(  -boost );
    blv.Boost( -boost );

    cos1 = TMath::Cos( blv.Angle(boost) );

    TVector3 boostW = (w1+w2).BoostVector();
    w1.Boost(  -boostW );
    w2.Boost(  -boostW );

    cos2 = TMath::Cos( w1.Angle(boostW) );

    return nSol;

}



int MEIntegratorNew::higgsEnergies(double E1, double& E2, double& cos1, int& errFlag) const {

    int nSol = 0;

    if(E1<Mb_) {
        errFlag = 1;
        return nSol;
    }


    double a12 = eB1_.Angle(eB2_); // b1 - b2

    double a = E1;
    double b = TMath::Sqrt(E1*E1 - Mb_*Mb_)*TMath::Cos(a12);

    if( (dMh2_*dMh2_ - (a*a - b*b)*Mb_*Mb_) < 0) {
        errFlag = 1;
        return nSol;
    }

    double E2_1 = (a*dMh2_ + b*TMath::Sqrt(dMh2_*dMh2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b);
    double E2_2 = (a*dMh2_ - b*TMath::Sqrt(dMh2_*dMh2_ - (a*a - b*b)*Mb_*Mb_))/(a*a - b*b);

    double E2tmp1 = -999.;
    double E2tmp2 = -999.;

    if( b>0 ) {
        if(E2_1>dMh2_/a) {
            E2tmp1 = E2_1;
            nSol++;
        }
        if(E2_2>dMh2_/a) {
            E2tmp2 = E2_2;
            nSol++;
        }
    }
    else {
        if(E2_1<dMh2_/a) {
            E2tmp1 = E2_1;
            nSol++;
        }
        if(E2_2<dMh2_/a) {
            E2tmp2 = E2_2;
            nSol++;
        }
    }

    if( E2tmp1>0 && E2tmp2>0 )
        E2 = TMath::Max( E2tmp1,E2tmp2 );
    else if( E2tmp1>0 &&  E2tmp2<0)
        E2 = E2tmp1;
    else if( E2tmp1<0 &&  E2tmp2>0)
        E2 = E2tmp2;
    else {
        errFlag = 1;
        return nSol;
    }

    if(E2<Mb_) {
        errFlag = 1;
        return nSol;
    }

    TLorentzVector b1( eB1_*(TMath::Sqrt(E1*E1 - Mb_*Mb_)),   E1);
    TLorentzVector b2( eB2_*(TMath::Sqrt(E2*E2 - Mb_*Mb_)),   E2);

    TVector3 boost = (b1+b2).BoostVector();
    b1.Boost( -boost );
    b2.Boost( -boost );

    cos1 = TMath::Cos( b1.Angle(boost) );

    return nSol;
}


double MEIntegratorNew::ggPdf( double x1, double x2, double Q) const {

    double lumiGG =  LHAPDF::xfx(1, x1, Q, 0) *  LHAPDF::xfx(1, x2 , Q, 0)
                     /x1/x1/x2/x2;

    return lumiGG;
}


double MEIntegratorNew::qqPdf( double x1, double x2, double Q) const {

    double lumiQQ =  2*(LHAPDF::xfx(1, x1, Q, 1) *  LHAPDF::xfx(1, x2, Q, -1) +
                        LHAPDF::xfx(1, x1, Q, 2) *  LHAPDF::xfx(1, x2, Q, -2) +
                        LHAPDF::xfx(1, x1, Q, 3) *  LHAPDF::xfx(1, x2, Q, -3) +
                        LHAPDF::xfx(1, x1, Q, 4) *  LHAPDF::xfx(1, x2, Q, -4) +
                        LHAPDF::xfx(1, x1, Q, 5) *  LHAPDF::xfx(1, x2, Q, -5)
                       )
                     /x1/x1/x2/x2;

    return lumiQQ;
}



double MEIntegratorNew::EvalPdf(const double* x) const {

    double lumiGG =  LHAPDF::xfx(1, x[0], Q_, 0) *  LHAPDF::xfx(1, Q_*Q_/x[0]/SqrtS_/SqrtS_, Q_, 0)
                     /x[0]/x[0]/x[0]/Q_/Q_; //SqrtS_/SqrtS_
    //double lumiQQ =  2*(LHAPDF::xfx(1, x[0], Q_, 1) *  LHAPDF::xfx(1, Q_*Q_/x[0]/SqrtS_/SqrtS_, Q_, -1) +
    //	      LHAPDF::xfx(1, x[0], Q_, 2) *  LHAPDF::xfx(1, Q_*Q_/x[0]/SqrtS_/SqrtS_, Q_, -2) +
    //	      LHAPDF::xfx(1, x[0], Q_, 3) *  LHAPDF::xfx(1, Q_*Q_/x[0]/SqrtS_/SqrtS_, Q_, -3) +
    //	      LHAPDF::xfx(1, x[0], Q_, 4) *  LHAPDF::xfx(1, Q_*Q_/x[0]/SqrtS_/SqrtS_, Q_, -4) +
    //	      LHAPDF::xfx(1, x[0], Q_, 5) *  LHAPDF::xfx(1, Q_*Q_/x[0]/SqrtS_/SqrtS_, Q_, -5)
    //	      )
    ///x[0]/x[0]/x[0]/Q_/Q_; //SqrtS_/SqrtS_

    return lumiGG;
}



double MEIntegratorNew::Eval(const double* x) const {

    (const_cast<MEIntegratorNew*>(this)->evaluation_)++;

    double prob = 0.0;
    if(intType_ == IntegrationType::SL2wj )
        prob = probabilitySL2wj(x,0);
    else if(intType_ == IntegrationType::SL1wj) {
        prob = probabilitySL1wj(x,0);
    }
    else if(intType_ == IntegrationType::SLNoBHad) {
        prob = probabilitySLNoBHad(x,0);
    }
    else if(intType_ == IntegrationType::SLNoBLep) {
        prob = probabilitySLNoBLep(x,0);
    }
    else if(intType_ == IntegrationType::SLNoHiggs) {
        prob = probabilitySLNoHiggs(x,0);
    }
    else if(intType_ == IntegrationType::DL) {
        prob = probabilityDL(x,0);
    }
    else if(intType_ == IntegrationType::SLXSec) {
        prob = probabilitySLUnconstrained(x,0);
    }
    else if( (intType_ == IntegrationType::SLAcc)       || (intType_ == IntegrationType::SLAcc2wj)    ||
             (intType_ == IntegrationType::SLAcc1wj)    || (intType_ == IntegrationType::SLAccNoBHad) ||
             (intType_ == IntegrationType::SLAccNoBLep) || (intType_ == IntegrationType::SLAccNoHiggs) ) {
        prob = probabilitySLUnconstrained(x,1);
    }
    else {
        cout << "Unsupported method... return" << endl;
        return 0.0;
    }

    if ( TMath::IsNaN(prob) ) prob = 0.;

    if(normalizeToXSec_ == NormalizationType::xSec)
        prob /=  xSection(0);
    else if(normalizeToXSec_ == NormalizationType::Acc)
        prob /=  xSection(1);
    else {}

    //if(verbose_) cout << "#" << evaluation_ << ": " << prob << endl;

    return prob;
}


void MEIntegratorNew::SetPar(int p) {
    par_ = p;
}

void MEIntegratorNew::setIntType( IntegrationType type ) {
    intType_ = type;
}

int MEIntegratorNew::getIntType() {
    return intType_;
}

void MEIntegratorNew::setHypo( int hyp ) {
    hypo_ = hyp;
}

void MEIntegratorNew::setJets( std::vector<TLorentzVector>* jets) {

    resetEvaluation();

    jets_.clear();
    jets_backup_.clear();
    for(unsigned int k = 0 ; k<jets->size() ; k++) {
        jets_.push_back( (*jets)[k] );
        jets_backup_.push_back( (*jets)[k] );
    }
}

void MEIntegratorNew::setBtag( std::vector<float>* bTagging ) {
    bTagging_.clear();
    for(unsigned int k = 0 ; k<bTagging->size() ; k++)
        bTagging_.push_back( (*bTagging)[k] );
}


void   MEIntegratorNew::createMash() {

    if(!mash_) return;

    mash_->Reset();

    for(unsigned int j = 0; j < jets_.size() ; j++) {

        float eta = jets_[j].Eta();
        float phi = jets_[j].Phi();

        for(int binX = 1; binX<mash_->GetNbinsX(); binX++ ) {
            float binCenterX = mash_->GetXaxis()->GetBinCenter(binX);
            for(int binY = 1; binY<mash_->GetNbinsY(); binY++ ) {
                float binCenterY = mash_->GetYaxis()->GetBinCenter(binY);

                float dist = TMath::Sqrt( (eta-binCenterX)*(eta-binCenterX) + (phi-binCenterY)*(phi-binCenterY) );
                if( j<4 ) { // jets to veto
                    if( dist<0.50 || mash_->GetBinContent(binX,binY)==-1 )
                        mash_->SetBinContent(binX,binY,  -1);
                    else
                        mash_->SetBinContent(binX,binY,   0);
                }
                else { // jets candidate W had
                    if( mash_->GetBinContent(binX,binY)==0 && dist<0.10 )
                        mash_->SetBinContent(binX,binY,   j);
                }

            }
        }

    }


}


TH2F*  MEIntegratorNew::getMash( ) {
    return mash_;
}

TH1F* MEIntegratorNew::getDebugHisto() {
    return debugHisto1_;
}

void MEIntegratorNew::initTFparameters( float mu_l, float s_l, float mu_b, float s_b , float s_met) {

    cout << "TF parameters will be initialized from RooWorkspace" << endl;
    cout << " ==> Light-jets (mu,sigma) will be changed to (" << mu_l << ","  << s_l   << ") times the nominal value !!!" << endl;
    cout << " ==> Heavy-jets (mu,sigma) will be changed to (" << mu_b << ","  << s_b   << ") times the nominal value !!!" << endl;
    cout << " ==> MEt (s_Px,s_Py) will be changed to ("       << s_met << "," << s_met << ") times the nominal value !!!" << endl;


    RooArgSet allVars = w_->allVars();
    TIterator* iter   = allVars.createIterator();
    RooRealVar* var   = 0;
    while( (var = (RooRealVar*)(*iter)() ) ) {
        string varname = string(var->GetName());
        float shift = 1.0;
        if     ( varname.find("resolLight")     !=string::npos ) shift *=  s_l;
        else if( varname.find("param0respLight")!=string::npos ) shift *= mu_l;
        else if( varname.find("resolHeavy")     !=string::npos ) shift *=  s_b;
        else if( varname.find("param0respHeavy")!=string::npos ) shift *= mu_b;
        else if( varname.find("PxWidthModel")   !=string::npos ) shift *= s_met;
        else {}
        jetParam_[ varname ] = (var->getVal()*shift);
        if((verbose_ || true) && TMath::Abs(shift-1)>0.01 )
            cout << "Parameter " << varname << " shifted by " << shift << " times its nominal value of " << var->getVal() << endl;
    }

    /*
    RooRealVar* var = w_->var(paramName.c_str());
    jetParam_[ paramName ] = var->getVal();
    */
}

void MEIntegratorNew::cachePdf( string pdfName, string varName, int nBins) {

    RooAbsPdf* pdf = w_->pdf( pdfName.c_str() );
    if(pdf) {
        RooRealVar* var = w_->var( varName.c_str() );

        TH1F* hCache = new TH1F(pdfName.c_str(),"", nBins, var->getMin(), var->getMax() );

        for(int j = 1; j <= hCache->GetNbinsX(); j++) {
            float lvalue = hCache->GetXaxis()->GetBinCenter(j);
            var->setVal( lvalue );
            hCache->SetBinContent(j, pdf->getVal( RooArgSet(*var) ) );
        }

        variables1D_[ pdfName ] = hCache;

    }

}


void MEIntegratorNew::cachePdf( string pdfName, string varName1, string varName2, int nBins1, int nBins2) {

    RooAbsPdf* pdf = w_->pdf( pdfName.c_str() );
    if(pdf) {
        RooRealVar* var1 = w_->var( varName1.c_str() );
        RooRealVar* var2 = w_->var( varName2.c_str() );

        TH2F* hCache = new TH2F("hCache","", nBins1, var1->getMin(), var1->getMax(), nBins2, var2->getMin(), var2->getMax() );

        for(int j = 1; j <= hCache->GetNbinsX(); j++) {
            float lvalue1 = hCache->GetXaxis()->GetBinCenter(j);
            var1->setVal( lvalue1 );
            for(int k = 1; k <= hCache->GetNbinsY(); k++) {
                float lvalue2 = hCache->GetYaxis()->GetBinCenter(k);
                var2->setVal( lvalue2 );
                hCache->SetBinContent(j,k, pdf->getVal( RooArgSet(*var1,*var2) ) );
            }
        }

        variables2D_[ pdfName ] = hCache;

    }

}


void MEIntegratorNew::cachePdf( string pdfName, string varName1, string varName2, string varName3, int nBins1, int nBins2, int nBins3) {

    RooAbsPdf* pdf = w_->pdf( pdfName.c_str() );
    if(pdf) {
        RooRealVar* var1 = w_->var( varName1.c_str() );
        RooRealVar* var2 = w_->var( varName2.c_str() );
        RooRealVar* var3 = w_->var( varName3.c_str() );

        TH3F* hCache = new TH3F("hCache","", nBins1, var1->getMin(), var1->getMax(), nBins2, var2->getMin(), var2->getMax(), nBins3, var3->getMin(), var3->getMax() );

        for(int j = 1; j <= hCache->GetNbinsX(); j++) {
            float lvalue1 = hCache->GetXaxis()->GetBinCenter(j);
            float bvalue1 = hCache->GetXaxis()->GetBinWidth(j);
            var1->setVal( lvalue1 );
            for(int k = 1; k <= hCache->GetNbinsY(); k++) {
                float lvalue2 =  hCache->GetYaxis()->GetBinCenter(k);
                float bvalue2 =  hCache->GetYaxis()->GetBinWidth(k);
                var2->setVal( lvalue2 );
                for(int m = 1; m <= hCache->GetNbinsZ(); m++) {
                    float lvalue3 =  hCache->GetZaxis()->GetBinCenter(m);
                    float bvalue3 =  hCache->GetZaxis()->GetBinWidth(m);
                    var3->setVal( lvalue3 );
                    hCache->SetBinContent(j,k,m, pdf->getVal( RooArgSet(*var1,*var2,*var3) ) / (bvalue1*bvalue2*bvalue3) );
                }
            }
        }

        variables3D_[ pdfName ] = hCache;

    }

}



void MEIntegratorNew::cachePdf( string pdfName, string varName1, string varName2,  TArrayF bins1, TArrayF bins2) {

    RooAbsPdf* pdf = w_->pdf( pdfName.c_str() );
    if(pdf) {
        RooRealVar* var1 = w_->var( varName1.c_str() );
        RooRealVar* var2 = w_->var( varName2.c_str() );

        TH2F* hCache = new TH2F("hCache","",
                                bins1.GetSize()-1, bins1.GetArray() ,
                                bins2.GetSize()-1, bins2.GetArray() );

        for(int j = 1; j <= hCache->GetNbinsX(); j++) {
            float lvalue1 = hCache->GetXaxis()->GetBinCenter(j);
            float bvalue1 = hCache->GetXaxis()->GetBinWidth(j);
            var1->setVal( lvalue1 );
            for(int k = 1; k <= hCache->GetNbinsY(); k++) {
                float lvalue2 =  hCache->GetYaxis()->GetBinCenter(k);
                float bvalue2 =  hCache->GetYaxis()->GetBinWidth(k);
                var2->setVal( lvalue2 );
                hCache->SetBinContent(j,k, pdf->getVal( RooArgSet(*var1,*var2) ) / (bvalue1*bvalue2) );
                //cout << lvalue1 << ", " << lvalue2 << ", " <<  lvalue3 << " ==> " << pdf->getVal( RooArgSet(*var1,*var2,*var3) )/ (bvalue1*bvalue2*bvalue3) << endl;
            }
        }

        variables2D_[ pdfName ] = hCache;

    }

}




void MEIntegratorNew::cachePdf( string pdfName, string varName1, string varName2, string varName3 , TArrayF bins1, TArrayF bins2, TArrayF bins3) {

    RooAbsPdf* pdf = w_->pdf( pdfName.c_str() );
    if(pdf) {
        RooRealVar* var1 = w_->var( varName1.c_str() );
        RooRealVar* var2 = w_->var( varName2.c_str() );
        RooRealVar* var3 = w_->var( varName3.c_str() );

        TH3F* hCache = new TH3F("hCache","",
                                bins1.GetSize()-1, bins1.GetArray() ,
                                bins2.GetSize()-1, bins2.GetArray(),
                                bins3.GetSize()-1, bins3.GetArray());

        for(int j = 1; j <= hCache->GetNbinsX(); j++) {
            float lvalue1 = hCache->GetXaxis()->GetBinCenter(j);
            float bvalue1 = hCache->GetXaxis()->GetBinWidth(j);
            var1->setVal( lvalue1 );
            for(int k = 1; k <= hCache->GetNbinsY(); k++) {
                float lvalue2 =  hCache->GetYaxis()->GetBinCenter(k);
                float bvalue2 =  hCache->GetYaxis()->GetBinWidth(k);
                var2->setVal( lvalue2 );
                for(int m = 1; m <= hCache->GetNbinsZ(); m++) {
                    float lvalue3 =  hCache->GetZaxis()->GetBinCenter(m);
                    float bvalue3 =  hCache->GetZaxis()->GetBinWidth(m);
                    var3->setVal( lvalue3 );
                    hCache->SetBinContent(j,k,m, pdf->getVal( RooArgSet(*var1,*var2,*var3) ) / (bvalue1*bvalue2*bvalue3) );
                    //cout << lvalue1 << ", " << lvalue2 << ", " <<  lvalue3 << " ==> " << pdf->getVal( RooArgSet(*var1,*var2,*var3) )/ (bvalue1*bvalue2*bvalue3) << endl;
                }
            }
        }


        variables3D_[ pdfName ] = hCache;

    }

}




TH1* MEIntegratorNew::getCachedPdf( string pdfName ) const {

    if( variables1D_.find(pdfName) !=  variables1D_.end() )
        return (variables1D_.find(pdfName))->second;
    else if( variables2D_.find(pdfName) !=  variables2D_.end() )
        return (variables2D_.find(pdfName))->second;
    else if( variables3D_.find(pdfName) !=  variables3D_.end() )
        return (variables3D_.find(pdfName))->second;

    else return 0;
}


TH1* MEIntegratorNew::getCachedTF( string tfName ) const {

    if( transferFunctions_.find(tfName) != transferFunctions_.end() )
        return (transferFunctions_.find(tfName))->second;

    else return 0;
}


double MEIntegratorNew::topHadJakobi( double Eq1, double Eq2, double EbHad, TLorentzVector* WHad)  const {

    double betaW = (WHad->BoostVector()).Mag();
    double betaB = TMath::Sqrt(EbHad*EbHad - Mb_*Mb_) / EbHad;

    return (2 * EbHad * Eq2 * Eq2 * Eq1 / (Mw_*Mw_ * ( Eq1 + Eq2 ) ) / TMath::Abs( betaW/betaB * ((WHad->Vect()).Unit()).Dot(eBHad_) - 1) ) ;
}

double MEIntegratorNew::topHadLostJakobi( double Eq1, double Eq2, double EbHad, TLorentzVector* WHad)  const {
    return topHadJakobi( Eq1, Eq2, EbHad, WHad);
}

double MEIntegratorNew::topHadBLostJakobi( double Eq1, double Eq2, double EbHad, TLorentzVector* WHad)  const {
    return topHadJakobi( Eq1, Eq2, EbHad, WHad);
}


double MEIntegratorNew::topLepJakobi( double Enu, double Elep, double EbLep, TLorentzVector* WLep)  const {

    double betaW = (WLep->BoostVector()).Mag();
    double betaB = TMath::Sqrt(EbLep*EbLep - Mb_*Mb_) / EbLep;

    return (2 * EbLep * Enu * Enu * Elep / (Mw_*Mw_ * ( Elep + Enu ) ) / TMath::Abs( betaW/betaB * ((WLep->Vect()).Unit()).Dot(eBLep_) - 1) ) ;
}

double MEIntegratorNew::topLepBLostJakobi( double Enu, double Elep, double EbLep, TLorentzVector* WLep)  const {
    return topLepJakobi(Enu, Elep, EbLep, WLep );
}


double MEIntegratorNew::higgsJakobi ( double Eh1, double Eh2)  const {
    return (Eh2 / TMath::Abs(  TMath::Sqrt(Eh1*Eh1 - Mb_*Mb_)/TMath::Sqrt(Eh2*Eh2 - Mb_*Mb_) * Eh2/Eh1 * eB1_.Dot(eB2_) - 1 )) ;
}




double MEIntegratorNew::evaluateCahchedPdf(TH1* h, double val1, double val2, double val3) const {

    if( (val1 < h->GetXaxis()->GetBinLowEdge(1) ||  val1 > h->GetXaxis()->GetBinUpEdge( h->GetNbinsX() ))  ||
            (val2 < h->GetYaxis()->GetBinLowEdge(1) ||  val2 > h->GetYaxis()->GetBinUpEdge( h->GetNbinsY() ))  ||
            (val3 < h->GetZaxis()->GetBinLowEdge(1) ||  val3 > h->GetZaxis()->GetBinUpEdge( h->GetNbinsZ() ))
      )
        return 0.0;
    else if( (val1 <= h->GetXaxis()->GetBinCenter(1) || val1 >= h->GetXaxis()->GetBinCenter(h->GetNbinsX()) ) ||
             (val2 <= h->GetYaxis()->GetBinCenter(1) || val2 >= h->GetYaxis()->GetBinCenter(h->GetNbinsY()) ) ||
             (val3 <= h->GetZaxis()->GetBinCenter(1) || val3 >= h->GetZaxis()->GetBinCenter(h->GetNbinsZ()) )
           ) {
        //double newVal1 = val1;
        //double newVal2 = val2;
        //double newVal3 = val3;
        //if( val1 <= h->GetXaxis()->GetBinCenter(1) )              newVal1 = h->GetXaxis()->GetBinUpEdge(1);
        //if( val1 >= h->GetXaxis()->GetBinCenter(h->GetNbinsX()) ) newVal1 = h->GetXaxis()->GetBinLowEdge(h->GetNbinsX());
        //if( val2 <= h->GetYaxis()->GetBinCenter(1) )              newVal2 = h->GetYaxis()->GetBinUpEdge(1);
        //if( val2 >= h->GetYaxis()->GetBinCenter(h->GetNbinsY()) ) newVal2 = h->GetYaxis()->GetBinLowEdge(h->GetNbinsY());
        //if( val3 <= h->GetZaxis()->GetBinCenter(1) )              newVal3 = h->GetZaxis()->GetBinUpEdge(1);
        //if( val3 >= h->GetZaxis()->GetBinCenter(h->GetNbinsZ()) ) newVal3 = h->GetZaxis()->GetBinLowEdge(h->GetNbinsZ());
        return
            //h->Interpolate(newVal1 ,newVal2, newVal3);
            h->GetBinContent( h->FindBin(val1,val2,val3) );
    }
    else
        //return  h->Interpolate( val1,val2,val3 );
        return h->GetBinContent( h->FindBin(val1,val2,val3) );

}



double MEIntegratorNew::topHadDensity ( double cos1, double cos2) const {

    double val1 = const_cast<TH1F*>(&pdfBetaWHad_) ->Interpolate(cos1);
    double val2 = const_cast<TH1F*>(&pdfGammaWHad_)->Interpolate(cos2);
    double res  = val1*val2;

    return res;

}

double MEIntegratorNew::topLepDensity ( double cos1, double cos2)  const {

    double val1 = const_cast<TH1F*>(&pdfBetaWLep_)->Interpolate(cos1);
    double val2 = const_cast<TH1F*>(&pdfGammaWLep_)->Interpolate(cos2);

    return val1*val2;

}


double MEIntegratorNew::higgsDensity ( double cos1 )  const {
    return 1.0;
}


double MEIntegratorNew::topLepDensity_analytical( TLorentzVector* t, TLorentzVector* b, TLorentzVector* l, TLorentzVector* v) const {

    double ampl = ( (*t)*(*l) * ((*b)*(*v)) );

    return TMath::Max( ampl , 0.);
}

double MEIntegratorNew::topHadDensity_analytical( TLorentzVector* t, TLorentzVector* b, TLorentzVector* q1, TLorentzVector* q2) const {

    double ampl_sym = ( (*t)*(*q1) * ((*b)*(*q2)) + (*t)*(*q2) * ((*b)*(*q1)) );

    return TMath::Max( ampl_sym, 0.);
}



double MEIntegratorNew::meSquaredOpenLoops (TLorentzVector* top, TLorentzVector* atop, TLorentzVector* higgs, double& x1, double& x2) const {


    TLorentzVector t, tx, h;
    t. SetPtEtaPhiM(   top->Pt(),  top->Eta(),   top->Phi(), Mtop_);
    tx.SetPtEtaPhiM(  atop->Pt(), atop->Eta(),  atop->Phi(), Mtop_);
    h. SetPtEtaPhiM( higgs->Pt(),higgs->Eta(), higgs->Phi(), M_   );

    TLorentzVector vSum = t+tx+h;
    TVector3 boostPt( vSum.Px()/vSum.E(), vSum.Py()/vSum.E(), 0.0 );

    t.Boost ( -boostPt );
    tx.Boost( -boostPt );
    h.Boost ( -boostPt );

    // fix for rounding
    double hPx = -(t.Px()  + tx.Px());
    double hPy = -(t.Py()  + tx.Py());
    double hPz = h.Pz();
    h.SetPxPyPzE( hPx, hPy, hPz, sqrt(hPx*hPx + hPy*hPy + hPz*hPz + M_*M_) );

    double E  = t.E() +tx.E() + h.E();
    double Pz = t.Pz()+tx.Pz()+ h.Pz();
    TLorentzVector g1 = TLorentzVector(0.,0.,  (E+Pz)/2., (E+Pz)/2.);
    TLorentzVector g2 = TLorentzVector(0.,0., -(E-Pz)/2., (E-Pz)/2.);

    x1 = ( Pz + E)/SqrtS_;
    x2 = (-Pz + E)/SqrtS_;

    double M2;
    double ccP[20] = {
        g1.E(), g1.Px(), g1.Py(), g1.Pz(),
        g2.E(), g2.Px(), g2.Py(), g2.Pz(),
        h.E(),  h.Px(),  h.Py(),  h.Pz(),
        t.E(),  t.Px(),  t.Py(),  t.Pz(),
        tx.E(), tx.Px(), tx.Py(), tx.Pz()
    };

    if(verbose_) {
        cout << "h:  " << h.M() << endl;
        cout << "t:  " << t.M() << endl;
        cout << "tx: " << tx.M() << endl;
    }

    pphttxcallme2born_(const_cast<double*>(&M2), ccP, const_cast<double*>(&Mtop_), const_cast<double*>(&M_));

    return M2;

}

double MEIntegratorNew::meSquaredOpenLoops_ttbb (TLorentzVector* top, TLorentzVector* atop, TLorentzVector* b1, TLorentzVector* b2, double& x1, double& x2) const {


    TLorentzVector t, tx, b, bx;
    t. SetPtEtaPhiM(   top->Pt(),  top->Eta(),   top->Phi(), Mtop_);
    tx.SetPtEtaPhiM(  atop->Pt(), atop->Eta(),  atop->Phi(), Mtop_);
    b. SetPtEtaPhiM(    b1->Pt(),   b1->Eta(),    b1->Phi(),  0.   );
    bx.SetPtEtaPhiM(    b2->Pt(),   b2->Eta(),    b2->Phi(),  0.   );

    TLorentzVector vSum = t+tx+b+bx;
    TVector3 boostPt( vSum.Px()/vSum.E(), vSum.Py()/vSum.E(), 0.0 );

    t.Boost ( -boostPt );
    tx.Boost( -boostPt );
    b.Boost ( -boostPt );
    bx.Boost( -boostPt );

    // fix for rounding
    double bPx = -(t.Px()  + tx.Px() + bx.Px());
    double bPy = -(t.Py()  + tx.Py() + bx.Py());
    double bPz = b.Pz();
    b.SetPxPyPzE( bPx, bPy, bPz, sqrt(bPx*bPx + bPy*bPy + bPz*bPz ) );

    double E  = t.E() +tx.E() + b.E() + bx.E();
    double Pz = t.Pz()+tx.Pz()+ b.Pz()+ bx.Pz();
    TLorentzVector g1 = TLorentzVector(0.,0.,  (E+Pz)/2., (E+Pz)/2.);
    TLorentzVector g2 = TLorentzVector(0.,0., -(E-Pz)/2., (E-Pz)/2.);

    x1 = ( Pz + E)/SqrtS_;
    x2 = (-Pz + E)/SqrtS_;

    double M2;
    double ccP[24] = {
        g1.E(), g1.Px(), g1.Py(), g1.Pz(),
        g2.E(), g2.Px(), g2.Py(), g2.Pz(),
        t.E(),  t.Px(),  t.Py(),  t.Pz(),
        tx.E(), tx.Px(), tx.Py(), tx.Pz(),
        b.E(),  b.Px(),  b.Py(),  b.Pz(),
        bx.E(), bx.Px(), bx.Py(), bx.Pz(),
    };

    if(verbose_) {
        cout << "b:  " << b.M() << endl;
        cout << "bx:  "<< bx.M() << endl;
        cout << "t:  " << t.M() << endl;
        cout << "tx: " << tx.M() << endl;
    }


    ppttxbbxcallme2born_(const_cast<double*>(&M2), ccP, const_cast<double*>(&Mtop_), const_cast<double*>(&M_));

    return M2;

}



void MEIntegratorNew::setNormFormulas(TString fxSec, TString facc1, TString facc2, TString facc3, TString facc4, TString fPt) {

    xSecFormula_  = new TF1("xSecFormula", fxSec.Data(), 20., 300.);
    xSecFormula_->SetNpx(300);

    accSL2wjFormula_   = new TF1("accSL2wjFormula",  facc1.Data() , 20., 300.);
    accSL2wjFormula_->SetNpx(300);

    accSL1wjFormula_   = new TF1("accSL1wjFormula",  facc2.Data() , 20., 300.);
    accSL1wjFormula_->SetNpx(300);

    accSLNoBHadFormula_   = new TF1("accSLNoBHadFormula",  facc3.Data() , 20., 300.);
    accSLNoBHadFormula_->SetNpx(300);

    accSLNoHiggsFormula_   = new TF1("accSLNoHiggsFormula",  facc4.Data() , 20., 300.);
    accSLNoHiggsFormula_->SetNpx(300);

    tthPtFormula_ = new TF1("tthPtFormula",fPt.Data(),   0., 1000.);
    tthPtFormula_->SetNpx(500);

    cout << "Cross-section formula:       " << string(xSecFormula_->GetTitle())  << endl;
    cout << "Acceptance SLw2j formula:    " << string(accSL2wjFormula_->GetTitle())   << endl;
    cout << "Acceptance SLw1j formula:    " << string(accSL1wjFormula_->GetTitle())   << endl;
    cout << "Acceptance SLNoBHad formula: " << string(accSLNoBHadFormula_->GetTitle())   << endl;
    cout << "Acceptance SLNoHiggs formula:" << string(accSLNoHiggsFormula_->GetTitle())   << endl;
    cout << "tth system formula:          " << string(tthPtFormula_->GetTitle()) << endl;

}

double MEIntegratorNew::xSection(int flag) const {

    double xsec = 1.0;
    double acc  = 1.0;
    if( SqrtS_>7999 && SqrtS_<8001 ) {

        xsec = xSecFormula_!=0 ?  xSecFormula_->Eval(M_) : 1.0;

        if( intType_ == SL2wj && accSL2wjFormula_)
            acc  = accSL2wjFormula_->Eval(M_) ;
        else if( (intType_ == SL1wj || intType_ == DL) && accSL1wjFormula_)
            acc  = accSL1wjFormula_->Eval(M_) ;
        else if( (intType_ == SLNoBHad || intType_ == SLNoBLep) && accSLNoBHadFormula_)
            acc  = accSLNoBHadFormula_->Eval(M_) ;
        else if( intType_ == SLNoHiggs && accSLNoHiggsFormula_)
            acc  = accSLNoHiggsFormula_->Eval(M_) ;

    }
    else {
        cout << "Cross-section not available" << endl;
    }

    return (flag==0 ? xsec : acc);
}



void MEIntegratorNew::resetEvaluation() {
    evaluation_ = 0;
}


double MEIntegratorNew::probabilitySL2wj(const double* x, int sign) const {

    //default hypo_ = 0 (SGN)

    int errFlag = 0;
    double prob = 1.0;

    double Eq1         = x[0];
    double cosThetaNu  = x[1];
    double phiNu       = x[2];
    double Eh1         = x[3];

    double Elep = jets_[0].P();

    // trasnform phiNu into an absolute phi:
    phiNu += eMEt_.Phi();
    if( phiNu < -PI ) phiNu += (2*PI);
    if( phiNu >  PI)  phiNu -= (2*PI);


    if(verbose_) {
        cout << "#" << evaluation_ << " SL2wj" << endl;
        cout << "Eq1 = "         << Eq1 << endl;
        cout << "cosThetaNu = " << cosThetaNu << endl;
        cout << "phiNu = "      << phiNu  << endl;
        cout << "Eh1 = "         << Eh1  << endl;
    }

    double Eq2, EbHad, cos1Had, cos2Had;
    int nSolTopHad = topHadEnergies( Eq1, Eq2, EbHad, cos1Had, cos2Had, errFlag );

    if(errFlag) {
        if(verbose_) cout << "Problems with topHadEnergies (" << nSolTopHad << " solutions)" << endl;
        return 0.0;
    }

    TVector3 eNu(0.,0.,1.); // neutrino
    double Enu, EbLep, cos1Lep, cos2Lep /*Jacob*/;
    int nSolTopLep = topLepEnergies( phiNu, cosThetaNu, Enu, EbLep, cos1Lep, cos2Lep, errFlag  );
    eNu.SetTheta( TMath::ACos( cosThetaNu ) );
    eNu.SetPhi  ( phiNu );
    eNu.SetMag  ( 1.);


    if(errFlag) {
        if(verbose_) cout << "Problems with topLepEnergies (" << nSolTopLep << " solutions)" << endl;
        return 0.0;
    }

    double Eh2, cos1Higgs;
    int nSolHiggs = higgsEnergies( Eh1, Eh2, cos1Higgs, errFlag );

    if(errFlag && hypo_==0) {
        if(verbose_) cout << "Problems with higgsEnergies (" << nSolHiggs << " solutions)" << endl;
        return 0.0;
    }

    if(hypo_==1) {
        Eh2       =  x[4];
        cos1Higgs = 1.; // dummy
    }

    if(verbose_) {
        cout << "Eh2 = "         << Eh2  << endl;
        cout << "EbHad = " << EbHad << " (Pt = " << EbHad*TMath::Sin(eBHad_.Theta()) << ")" << endl;
        cout << "EbLep = " << EbLep << " (Pt = " << EbLep*TMath::Sin(eBLep_.Theta()) << ")" << endl;
        cout << "Enu = " << Enu << " (Pt = " << Enu*sqrt(1-cosThetaNu*cosThetaNu) << ")"  << endl;
        cout << "cos1Had = " << cos1Had << endl;
        cout << "cos2Had = " << cos2Had << endl;
        cout << "********" << endl;
    }

    TLorentzVector W1Had( eW1Had_*Eq1, Eq1 );
    TLorentzVector W2Had( eW2Had_*Eq2, Eq2 );
    TLorentzVector WHad = W1Had + W2Had;
    TLorentzVector bHad ( eBHad_*TMath::Sqrt(EbHad*EbHad - Mb_*Mb_), EbHad );
    TLorentzVector topHad = WHad + bHad;

    TLorentzVector WLepLep = jets_[0];
    TLorentzVector WLepNu( eNu*Enu, Enu);
    TLorentzVector WLep = WLepLep + WLepNu;
    TLorentzVector bLep  ( eBLep_*TMath::Sqrt(EbLep*EbLep - Mb_*Mb_), EbLep );
    TLorentzVector topLep = WLep + bLep;

    TLorentzVector higgs1(  eB1_*TMath::Sqrt(Eh1*Eh1 -  Mb_*Mb_), Eh1);
    TLorentzVector higgs2(  eB2_*TMath::Sqrt(Eh2*Eh2 -  Mb_*Mb_), Eh2);
    TLorentzVector higgs = higgs1 + higgs2;

    TLorentzVector tot = topHad+topLep+higgs;

    TVector3 boostToCMS  = tot.BoostVector();

    double x1 = (  tot.Pz() + tot.E() )/SqrtS_;
    double x2 = ( -tot.Pz() + tot.E() )/SqrtS_;
    double Q  = (2*Mtop_ + M_)/2.;

    if( useDynamicalScale_ && hypo_==1 ) Q = TMath::Sqrt( 4*Mtop_*Mtop_ + TMath::Power(higgs1.Pt() + higgs2.Pt(), 2) );

    //cout << "x1 (NLO) = " << x1 << ", x2 (NLO) = " << x2 << endl;

    double me2;
    if(useME_==1 && top1Flag_ == +1 && top2Flag_ == -1)               // topLep = t,  topHad = tx
        me2 = hypo_==0 ? meSquaredOpenLoops( &topLep, &topHad, &higgs, x1, x2 ) : meSquaredOpenLoops_ttbb( &topLep, &topHad, &higgs1, &higgs2, x1, x2 );
    else if(useME_==1 && top1Flag_ == -1 && top2Flag_ == +1)          // topLep = tx, topHad = t
        me2 = hypo_==0 ? meSquaredOpenLoops( &topHad, &topLep, &higgs, x1, x2 ) : meSquaredOpenLoops_ttbb( &topHad, &topLep, &higgs1, &higgs2, x1, x2 );
    else {
        if(verbose_) cout << "Undefined top flavors" << endl;
        me2 = 1.;
    }

    double MEpart = 1.0;
    if( useAnalyticalFormula_==0 )
        MEpart =
            topHadDensity(cos1Had,cos2Had) *
            topLepDensity(cos1Lep,cos2Lep) *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;
    else
        MEpart =
            topLepDensity_analytical( &topLep, &bLep, &WLepLep, &WLepNu ) *
            topHadDensity_analytical( &topHad, &bHad, &W1Had,   &W2Had )  *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;

    double Jpart =
        topHadJakobi( Eq1,  Eq2, EbHad, &WHad ) *
        topLepJakobi( Enu, Elep, EbLep, &WLep ) *
        (hypo_==0 ? higgsJakobi( Eh1, Eh2 ) : Eh1*Eh2/4)
        ;

    double tf1 = jetEnergyTF( jets_[2].Eta(), jets_[2].E(),  bLep.E(),    "Heavy");
    double tf2 = jetEnergyTF( jets_[3].Eta(), jets_[3].E(),  W1Had.E(),   "Light");
    double tf3 = jetEnergyTF( jets_[4].Eta(), jets_[4].E(),  W2Had.E(),   "Light");
    double tf4 = jetEnergyTF( jets_[5].Eta(), jets_[5].E(),  bHad.E(),    "Heavy");
    double tf5 = jetEnergyTF( jets_[6].Eta(), jets_[6].E(),  higgs1.E(),  "Heavy");
    double tf6 = jetEnergyTF( jets_[7].Eta(), jets_[7].E(),  higgs2.E(),  "Heavy");


    double dPx = WLepNu.Px() - jets_[1].Px();
    double dPy = WLepNu.Py() - jets_[1].Py();
    if( constrainToRecoil_ ) {
        dPx =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]+jets_[5]+jets_[6]+jets_[7]).Px() + tot.Px() ;
        dPy =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]+jets_[5]+jets_[6]+jets_[7]).Py() + tot.Py() ;
    }

    double tf7 =
        (Vx_*Vy_ - rho_*rho_*Vx_*Vy_)>0 ? 1./2./PI/TMath::Sqrt(Vx_*Vy_ - rho_*rho_*Vx_*Vy_)*TMath::Exp( -0.5*( 1/(1-rho_*rho_)*( dPx*dPx/Vx_ + dPy*dPy/Vy_ - 2*rho_*dPx*dPy/TMath::Sqrt(Vx_*Vy_) ) ) ) : 1.0 ;

    //cout << "dPx= " << dPx << endl;
    //cout << "dPy= " << dPy << endl;
    //cout << " ==> " << tf7 << endl;

    double TFpart =
        tf1 *
        tf2 *
        tf3 *
        tf4 *
        tf5 *
        tf6
        ;

    double METpart =
        tf7
        ;

    double PDFpart = ggPdf( x1, x2 , Q);

    if(useME_)  prob *= MEpart;
    if(useJac_) prob *= Jpart;
    if(useMET_) prob *= METpart;
    if(useTF_)  prob *= TFpart;
    if(usePDF_) prob *= PDFpart;

    if(verbose_) {
      cout << tf1 << ", " << tf2 << ", " << tf3 << ", "<< tf4 << ", "<< tf5 << ", "<< tf6 << ", " << tf7 << endl;
      cout << MEpart << ", " << Jpart << ", " << PDFpart << " (x1,x2)=" << x1 << "," << x2 << endl;
    }

    ////////////////////////

    if( TMath::IsNaN(prob) ) {
        if(verbose_) {
            cout << tf1 << ", " << tf2 << ", " << tf3 << ", "<< tf4 << ", "<< tf5 << ", "<< tf6 << ", " << tf7 << endl;
            cout << MEpart << ", " << Jpart << ", " << PDFpart << endl;
        }
        prob = 0.;
    }

    return prob;
}


double MEIntegratorNew::probabilitySL1wj(const double* x, int sign) const {

    int errFlag = 0;
    double prob = 1.0;

    double Eq1         = x[0];
    double cosThetaq2  = x[1];
    double phiNuq2     = x[2];
    double cosThetaNu  = x[3];
    double phiNu       = x[4];
    double Eh1         = x[5];

    double Elep = jets_[0].P();

    // trasnform phiNu into an absolute phi:
    phiNu += eMEt_.Phi();
    if( phiNu < -PI ) phiNu += (2*PI);
    if( phiNu >  PI)  phiNu -= (2*PI);


    if(verbose_) {
        cout << "#" << evaluation_ << " SL1wj" << endl;
        cout << "Eq1 =        "  << Eq1 << endl;
        cout << "cosThetaq2 = "  << cosThetaq2 << endl;
        cout << "phiNuq2 =    "  << phiNuq2 << endl;
        cout << "cosThetaNu = "  << cosThetaNu << endl;
        cout << "phiNu =      "  << phiNu  << endl;
        cout << "Eh1 =        "  << Eh1  << endl;
    }

    double Eq2, EbHad, cos1Had, cos2Had;
    int nSolTopHad = topHadLostEnergies( phiNuq2, cosThetaq2, Eq2, Eq1, EbHad, cos1Had, cos2Had, errFlag );

    if(errFlag) {
        if(verbose_) cout << "Problems with topHadLostEnergies (" << nSolTopHad << " solutions)" << endl;
        return 0.0;
    }

    TVector3 eMiss(0.,0.,1.); // w lost
    eMiss.SetTheta( TMath::ACos( cosThetaq2 ) );
    eMiss.SetPhi  ( phiNuq2 );
    eMiss.SetMag  ( 1.);

    TVector3 eNu(0.,0.,1.); // neutrino
    double Enu, EbLep, cos1Lep, cos2Lep /*Jacob*/;
    int nSolTopLep = topLepEnergies( phiNu, cosThetaNu, Enu, EbLep, cos1Lep, cos2Lep, errFlag  );
    eNu.SetTheta( TMath::ACos( cosThetaNu ) );
    eNu.SetPhi  ( phiNu );
    eNu.SetMag  ( 1.);

    if(errFlag) {
        if(verbose_) cout << "Problems with topLepEnergies (" << nSolTopLep << " solutions)" << endl;
        return 0.0;
    }

    double Eh2, cos1Higgs;
    int nSolHiggs = higgsEnergies( Eh1, Eh2, cos1Higgs, errFlag );

    if(errFlag && hypo_==0) {
        if(verbose_) cout << "Problems with higgsEnergies (" << nSolHiggs << " solutions)" << endl;
        return 0.0;
    }

    if(hypo_==1) {
        Eh2       =  x[6];
        cos1Higgs = 1.; // dummy
    }

    if(verbose_) {
        cout << "Eq2   = " << Eq2 << " (Pt = " << Eq2*TMath::Sin(eMiss.Theta()) << ")" << endl;
        cout << "EbHad = " << EbHad << " (Pt = " << EbHad*TMath::Sin(eBHad_.Theta()) << ")" << endl;
        cout << "EbLep = " << EbLep << " (Pt = " << EbLep*TMath::Sin(eBLep_.Theta()) << ")" << endl;
        cout << "Enu = " << Enu << " (Pt = " << Enu*sqrt(1-cosThetaNu*cosThetaNu) << ")"  << endl;
        cout << "cos1Had = " << cos1Had << endl;
        cout << "cos2Had = " << cos2Had << endl;
        cout << "********" << endl;
    }

    TLorentzVector W1Had( eW1Had_*Eq1, Eq1 );
    TLorentzVector W2Had( eMiss  *Eq2,  Eq2 );
    TLorentzVector WHad = W1Had + W2Had;
    TLorentzVector bHad ( eBHad_*TMath::Sqrt(EbHad*EbHad - Mb_*Mb_), EbHad );
    TLorentzVector topHad = WHad + bHad;

    if(verbose_) {
        cout << "W   had mass = " << WHad.M() << endl;
        cout << "Top had mass = " << topHad.M() << endl;
    }

    TLorentzVector WLepLep = jets_[0];
    TLorentzVector WLepNu( eNu*Enu, Enu);
    TLorentzVector WLep = WLepLep + WLepNu;
    TLorentzVector bLep  ( eBLep_*TMath::Sqrt(EbLep*EbLep - Mb_*Mb_), EbLep );
    TLorentzVector topLep = WLep + bLep;

    TLorentzVector higgs1(  eB1_*TMath::Sqrt(Eh1*Eh1 -  Mb_*Mb_), Eh1);
    TLorentzVector higgs2(  eB2_*TMath::Sqrt(Eh2*Eh2 -  Mb_*Mb_), Eh2);
    TLorentzVector higgs = higgs1 + higgs2;

    TLorentzVector tot = topHad+topLep+higgs;

    double x1 = (  tot.Pz() + tot.E() )/SqrtS_;
    double x2 = ( -tot.Pz() + tot.E() )/SqrtS_;
    double Q  = (2*Mtop_ + M_)/2.;

    if( useDynamicalScale_ && hypo_==1 ) Q = TMath::Sqrt( 4*Mtop_*Mtop_ + TMath::Power(higgs1.Pt() + higgs2.Pt(), 2) );

    TVector3 boostToCMS  = tot.BoostVector();

    double me2 = 1.0;
    if(useME_==1 && top1Flag_ == +1 && top2Flag_ == -1)               // topLep = t,  topHad = tx
        me2 = hypo_==0 ? meSquaredOpenLoops( &topLep, &topHad, &higgs, x1, x2 ) : meSquaredOpenLoops_ttbb( &topLep, &topHad, &higgs1, &higgs2, x1, x2 );
    else if(useME_==1 && top1Flag_ == -1 && top2Flag_ == +1)          // topLep = tx, topHad = t
        me2 = hypo_==0 ? meSquaredOpenLoops( &topHad, &topLep, &higgs, x1, x2 ) : meSquaredOpenLoops_ttbb( &topLep, &topHad, &higgs1, &higgs2, x1, x2 );
    else {
        if(useME_==1 && verbose_) cout << "Undefined top flavors" << endl;
        me2 = 1.;
    }

    double MEpart = 1.0;
    if( useAnalyticalFormula_==0 )
        MEpart =
            topHadDensity(cos1Had,cos2Had) *
            topLepDensity(cos1Lep,cos2Lep) *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;
    else
        MEpart =
            topLepDensity_analytical( &topLep, &bLep, &WLepLep, &WLepNu ) *
            topHadDensity_analytical( &topHad, &bHad, &W1Had,   &W2Had )  *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;

    double Jpart =
        topHadLostJakobi( Eq1,  Eq2, EbHad, &WHad ) *
        topLepJakobi( Enu, Elep, EbLep, &WLep ) *
        (hypo_==0 ? higgsJakobi( Eh1, Eh2 ) : Eh1*Eh2/4)
        ;

    double tf1 = jetEnergyTF( jets_[2].Eta(), jets_[2].E(),  bLep.E(),    "Heavy");
    double tf2 = jetEnergyTF( jets_[3].Eta(), jets_[3].E(),  W1Had.E(),   "Light");
    double tf3 = 1.0;
    double tf4 = jetEnergyTF( jets_[5].Eta(), jets_[5].E(),  bHad.E(),    "Heavy");
    double tf5 = jetEnergyTF( jets_[6].Eta(), jets_[6].E(),  higgs1.E(),  "Heavy");
    double tf6 = jetEnergyTF( jets_[7].Eta(), jets_[7].E(),  higgs2.E(),  "Heavy");

    double dPx = WLepNu.Px() - jets_[1].Px();
    double dPy = WLepNu.Py() - jets_[1].Py();
    if( constrainToRecoil_ ) {
        dPx =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]/*+jets_[4]*/+jets_[5]+jets_[6]+jets_[7]).Px() + (tot-W2Had).Px() ;
        dPy =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]/*+jets_[4]*/+jets_[5]+jets_[6]+jets_[7]).Py() + (tot-W2Had).Py() ;
    }

    double tf7 = (Vx_*Vy_ - rho_*rho_*Vx_*Vy_)>0 ?
                 1./2./PI/TMath::Sqrt(Vx_*Vy_ - rho_*rho_*Vx_*Vy_)*TMath::Exp( -0.5*( 1/(1-rho_*rho_)*( dPx*dPx/Vx_ + dPy*dPy/Vy_ - 2*rho_*dPx*dPy/TMath::Sqrt(Vx_*Vy_) ) ) ) : 1.0 ;


    ///////////////////////////////////////////////////////////////////////////
    if( TMath::Abs(eMiss.Eta())<2.5 ) {

        double Ptq2 = W2Had.Pt();

        string bin = "Bin0";
        if(  TMath::Abs( eMiss.Eta() )<1.0 )
            bin = "Bin0";
        else
            bin = "Bin1";

        double param0resol = (jetParam_.find("param0resolLight"+bin))->second;
        double param1resol = (jetParam_.find("param1resolLight"+bin))->second;
        double param2resol = (jetParam_.find("param2resolLight"+bin))->second;
        double param0resp  = (jetParam_.find("param0respLight" +bin))->second;
        double param1resp  = (jetParam_.find("param1respLight" +bin))->second;

        //double Width  = Eq2*TMath::Sqrt( param0resol*param0resol/Eq2 + param1resol*param1resol/Eq2/Eq2) * (Ptq2/Eq2);
        //double Mean   = (Eq2*param0resp + param1resp) * (Ptq2/Eq2) ;
        double Width  = TMath::Sqrt( (param0resol*param0resol) + Eq2*(param1resol*param1resol) + Eq2*Eq2*(param2resol*param2resol) ) * (Ptq2/Eq2);
        double Mean   = (Eq2*param0resp + param1resp) * (Ptq2/Eq2) ;

        tf3 = 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 )  ;

        if( deltaR(W2Had, WLepLep)< 0.5 ) {
            if(verbose_) cout << "Overlap with lepton " << endl;
            tf3 = (Ptq2 < 0.10*WLepLep.Pt()) ? 1.0 : 0.0;
        }
        else if( deltaR(W2Had, bLep)  < 0.5 ) {
            if(verbose_) cout << "Overlap with bLep " << endl;
            tf3 = 1.;
            tf1 = jetEnergyTF( jets_[2].Eta(), jets_[2].E(),  (bLep.E()+W2Had.E()),     "Heavy");
        }
        else if( deltaR(W2Had, W1Had)  < 0.5 ) {
            if(verbose_) cout << "Overlap with W1 " << endl;
            tf3 = 1.;
            tf2 = jetEnergyTF( jets_[3].Eta(), jets_[3].E(),  (W1Had.E()+W2Had.E()),    "Light");
        }
        else if( deltaR(W2Had, bHad)  < 0.5 ) {
            if(verbose_) cout << "Overlap with bHad " << endl;
            tf3 = 1.;
            tf4 = jetEnergyTF( jets_[5].Eta(), jets_[5].E(),  (bHad.E()+W2Had.E()),     "Heavy");
        }
        else if( deltaR(W2Had, higgs1) < 0.5 ) {
            if(verbose_) cout << "Overlap with h1 " << endl;
            tf3 = 1.;
            tf5 = jetEnergyTF( jets_[6].Eta(), jets_[6].E(),  (higgs1.E()+W2Had.E()),   "Heavy");
        }
        else if( deltaR(W2Had, higgs2) < 0.5 ) {
            if(verbose_) cout << "Overlap with h2 " << endl;
            tf3 = 1.;
            tf5 = jetEnergyTF( jets_[7].Eta(), jets_[7].E(),  (higgs2.E()+W2Had.E()),   "Heavy");
        }
        else {}

    }
    ///////////////////////////////////////////////////////////////////////////


    double TFpart =
        tf1 *
        tf2 *
        tf3 *
        tf4 *
        tf5 *
        tf6
        ;

    double METpart =
        tf7
        ;

    double PDFpart = ggPdf( x1, x2 , Q);

    if(useME_)   prob *= MEpart;
    if(useJac_)  prob *= Jpart;
    if(useMET_)  prob *= METpart;
    if(useTF_)   prob *= TFpart;
    if(usePDF_)  prob *= PDFpart;

    ////////////////////////

    if( TMath::IsNaN(prob) ) {
        if(verbose_) {
            cout << tf1 << ", " << tf2 << ", " << tf3 << ", "<< tf4 << ", "<< tf5 << ", "<< tf6 << ", " << tf7 << endl;
            cout << MEpart << ", " << Jpart << ", " << PDFpart << endl;
        }
        prob = 0.;
    }

    return prob;
}


double MEIntegratorNew::probabilitySLNoBHad(const double* x, int sign) const {

    int errFlag = 0;
    double prob = 1.0;

    double Eq1           = x[0];
    double cosThetaBHad  = x[1];
    double phiBHad       = x[2];
    double cosThetaNu    = x[3];
    double phiNu         = x[4];
    double Eh1           = x[5];

    double Elep = jets_[0].P();

    // trasnform phiNu into an absolute phi:
    phiNu += eMEt_.Phi();
    if( phiNu < -PI ) phiNu += (2*PI);
    if( phiNu >  PI)  phiNu -= (2*PI);


    if(verbose_) {
        cout << "#" << evaluation_ << " SLNoBHad" << endl;
        cout << "Eq1 =          "  << Eq1 << endl;
        cout << "cosThetaBHad = "  << cosThetaBHad << endl;
        cout << "phiNuBHad =    "  << phiBHad << endl;
        cout << "cosThetaNu =   "  << cosThetaNu << endl;
        cout << "phiNu =        "  << phiNu  << endl;
        cout << "Eh1 =          "  << Eh1  << endl;
    }

    double Eq2, EbHad, cos1Had, cos2Had;
    int nSolTopHad = topHadBLostEnergies( phiBHad, cosThetaBHad, Eq1, Eq2, EbHad, cos1Had, cos2Had, errFlag );

    if(errFlag) {
        if(verbose_) cout << "Problems with topHadLostEnergies (" << nSolTopHad << " solutions)" << endl;
        return 0.0;
    }

    TVector3 eMiss(0.,0.,1.); // bHad lost
    eMiss.SetTheta( TMath::ACos( cosThetaBHad ) );
    eMiss.SetPhi  ( phiBHad );
    eMiss.SetMag  ( 1.);

    TVector3 eNu(0.,0.,1.); // neutrino
    double Enu, EbLep, cos1Lep, cos2Lep /*Jacob*/;
    int nSolTopLep = topLepEnergies( phiNu, cosThetaNu, Enu, EbLep, cos1Lep, cos2Lep, errFlag  );
    eNu.SetTheta( TMath::ACos( cosThetaNu ) );
    eNu.SetPhi  ( phiNu );
    eNu.SetMag  ( 1.);

    if(errFlag) {
        if(verbose_) cout << "Problems with topLepEnergies (" << nSolTopLep << " solutions)" << endl;
        return 0.0;
    }

    double Eh2, cos1Higgs;
    int nSolHiggs = higgsEnergies( Eh1, Eh2, cos1Higgs, errFlag );

    if(errFlag && hypo_==0) {
        if(verbose_) cout << "Problems with higgsEnergies (" << nSolHiggs << " solutions)" << endl;
        return 0.0;
    }

    if(hypo_==1) {
        Eh2       =  x[6];
        cos1Higgs = 1.; // dummy
    }

    if(verbose_) {
        cout << "Eq2   = " << Eq2 << " (Pt = " << Eq2*TMath::Sin(eMiss.Theta()) << ")" << endl;
        cout << "EbHad = " << EbHad << " (Pt = " << EbHad*TMath::Sin(eBHad_.Theta()) << ")" << endl;
        cout << "EbLep = " << EbLep << " (Pt = " << EbLep*TMath::Sin(eBLep_.Theta()) << ")" << endl;
        cout << "Enu = " << Enu << " (Pt = " << Enu*sqrt(1-cosThetaNu*cosThetaNu) << ")"  << endl;
        cout << "cos1Had = " << cos1Had << endl;
        cout << "cos2Had = " << cos2Had << endl;
        cout << "********" << endl;
    }

    TLorentzVector W1Had( eW1Had_*Eq1, Eq1 );
    TLorentzVector W2Had( eW2Had_*Eq2,  Eq2 );
    TLorentzVector WHad = W1Had + W2Had;
    TLorentzVector bHad ( eMiss*TMath::Sqrt(EbHad*EbHad - Mb_*Mb_), EbHad );
    TLorentzVector topHad = WHad + bHad;

    if(verbose_ ) {
        cout << "W   had mass = " << WHad.M() << endl;
        cout << "Top had mass = " << topHad.M() << endl;
    }

    TLorentzVector WLepLep = jets_[0];
    TLorentzVector WLepNu( eNu*Enu, Enu);
    TLorentzVector WLep = WLepLep + WLepNu;
    TLorentzVector bLep  ( eBLep_*TMath::Sqrt(EbLep*EbLep - Mb_*Mb_), EbLep );
    TLorentzVector topLep = WLep + bLep;

    if(verbose_ ) {
        cout << "W   lep mass = " << WLep.M() << endl;
        cout << "Top lep mass = " << topLep.M() << endl;
    }

    TLorentzVector higgs1(  eB1_*TMath::Sqrt(Eh1*Eh1 -  Mb_*Mb_), Eh1);
    TLorentzVector higgs2(  eB2_*TMath::Sqrt(Eh2*Eh2 -  Mb_*Mb_), Eh2);
    TLorentzVector higgs = higgs1 + higgs2;

    if(verbose_ ) {
        cout << "H   had mass = " << higgs.M() << endl;
    }


    TLorentzVector tot = topHad+topLep+higgs;

    double x1 = (  tot.Pz() + tot.E() )/SqrtS_;
    double x2 = ( -tot.Pz() + tot.E() )/SqrtS_;
    double Q  = (2*Mtop_ + M_)/2.;

    if( useDynamicalScale_ && hypo_==1 ) Q = TMath::Sqrt( 4*Mtop_*Mtop_ + TMath::Power(higgs1.Pt() + higgs2.Pt(), 2) );

    TVector3 boostToCMS  = tot.BoostVector();

    double me2 = 1.0;
    if(useME_==1 && top1Flag_ == +1 && top2Flag_ == -1)               // topLep = t,  topHad = tx
        me2 =  hypo_==0 ? meSquaredOpenLoops( &topLep, &topHad, &higgs, x1, x2  ) : meSquaredOpenLoops_ttbb( &topLep, &topHad, &higgs1, &higgs2, x1, x2 );
    else if(useME_==1 && top1Flag_ == -1 && top2Flag_ == +1)          // topLep = tx, topHad = t
        me2 =  hypo_==0 ? meSquaredOpenLoops( &topHad, &topLep, &higgs, x1, x2  ) : meSquaredOpenLoops_ttbb( &topLep, &topHad, &higgs1, &higgs2, x1, x2 );
    else {
        if(useME_==1 && verbose_) cout << "Undefined top flavors" << endl;
        me2 = 1.;
    }

    double MEpart = 1.0;
    if( useAnalyticalFormula_==0 )
        MEpart =
            topHadDensity(cos1Had,cos2Had) *
            topLepDensity(cos1Lep,cos2Lep) *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;
    else
        MEpart =
            topLepDensity_analytical( &topLep, &bLep, &WLepLep, &WLepNu ) *
            topHadDensity_analytical( &topHad, &bHad, &W1Had,   &W2Had )  *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;

    double Jpart =
        topHadBLostJakobi( Eq1,  Eq2, EbHad, &WHad ) *
        topLepJakobi( Enu, Elep, EbLep, &WLep ) *
        (hypo_==0 ? higgsJakobi( Eh1, Eh2 ) : Eh1*Eh2/4)
        ;

    double tf1 = jetEnergyTF( jets_[2].Eta(), jets_[2].E(),  bLep.E(),    "Heavy");
    double tf2 = jetEnergyTF( jets_[3].Eta(), jets_[3].E(),  W1Had.E(),   "Light");
    double tf3 = jetEnergyTF( jets_[4].Eta(), jets_[4].E(),  W2Had.E(),   "Light");
    double tf4 = 1.0;
    double tf5 = jetEnergyTF( jets_[6].Eta(), jets_[6].E(),  higgs1.E(),  "Heavy");
    double tf6 = jetEnergyTF( jets_[7].Eta(), jets_[7].E(),  higgs2.E(),  "Heavy");

    double dPx = WLepNu.Px() - jets_[1].Px();
    double dPy = WLepNu.Py() - jets_[1].Py();
    if( constrainToRecoil_ ) {
        dPx =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]/*+jets_[5]*/+jets_[6]+jets_[7]).Px() + (tot-bHad).Px() ;
        dPy =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]/*+jets_[5]*/+jets_[6]+jets_[7]).Py() + (tot-bHad).Py() ;
    }

    double tf7 = (Vx_*Vy_ - rho_*rho_*Vx_*Vy_)>0 ?
                 1./2./PI/TMath::Sqrt(Vx_*Vy_ - rho_*rho_*Vx_*Vy_)*TMath::Exp( -0.5*( 1/(1-rho_*rho_)*( dPx*dPx/Vx_ + dPy*dPy/Vy_ - 2*rho_*dPx*dPy/TMath::Sqrt(Vx_*Vy_) ) ) ) : 1.0 ;


    ///////////////////////////////////////////////////////////////////////////
    if( TMath::Abs(bHad.Eta())<2.5 ) {

        double PtBHad = bHad.Pt();

        string bin = "Bin0";
        if(  TMath::Abs( bHad.Eta() )<1.0 )
            bin = "Bin0";
        else
            bin = "Bin1";

        double param0resol = (jetParam_.find("param0resolHeavy"+bin))->second;
        double param1resol = (jetParam_.find("param1resolHeavy"+bin))->second;
        double param2resol = (jetParam_.find("param2resolHeavy"+bin))->second;
        double param0resp  = (jetParam_.find("param0respHeavy" +bin))->second;
        double param1resp  = (jetParam_.find("param1respHeavy" +bin))->second;

        //double Width  = EbHad*TMath::Sqrt( param0resol*param0resol/EbHad + param1resol*param1resol/EbHad/EbHad) * (PtBHad/EbHad);
        //double Mean   = (EbHad*param0resp + param1resp) * (PtBHad/EbHad) ;

        double Width  = TMath::Sqrt( (param0resol*param0resol) + EbHad*(param1resol*param1resol) + EbHad*EbHad*(param2resol*param2resol) ) * (PtBHad/EbHad);
        double Mean   = (EbHad*param0resp + param1resp) * (PtBHad/EbHad) ;

        tf4 = 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 )  ;

        if( deltaR(bHad, WLepLep)< 0.5 ) {
            if(verbose_) cout << "Overlap with lepton " << endl;
            tf4 = (PtBHad < 0.10*WLepLep.Pt()) ? 1.0 : 0.0;
        }
        else if( deltaR(bHad, bLep)  < 0.5 ) {
            if(verbose_) cout << "Overlap with bLep " << endl;
            tf4 = 1.;
            tf1 = jetEnergyTF( jets_[2].Eta(), jets_[2].E(),  (bLep.E()+bHad.E()),     "Heavy");
        }
        else if( deltaR(bHad, W1Had)  < 0.5 ) {
            if(verbose_) cout << "Overlap with W1 " << endl;
            tf4 = 1.;
            tf2 = jetEnergyTF( jets_[3].Eta(), jets_[3].E(),  (W1Had.E()+bHad.E()),    "Light");
        }
        else if( deltaR(bHad, W2Had)  < 0.5 ) {
            if(verbose_) cout << "Overlap with W2 " << endl;
            tf4 = 1.;
            tf3 = jetEnergyTF( jets_[4].Eta(), jets_[4].E(),  (W2Had.E()+bHad.E()),    "Light");
        }
        else if( deltaR(bHad, higgs1) < 0.5 ) {
            if(verbose_) cout << "Overlap with h1 " << endl;
            tf4 = 1.;
            tf5 = jetEnergyTF( jets_[6].Eta(), jets_[6].E(),  (higgs1.E()+bHad.E()),   "Heavy");
        }
        else if( deltaR(bHad, higgs2) < 0.5 ) {
            if(verbose_) cout << "Overlap with h2 " << endl;
            tf4 = 1.;
            tf5 = jetEnergyTF( jets_[7].Eta(), jets_[7].E(),  (higgs2.E()+bHad.E()),   "Heavy");
        }
        else {}

    }
    ///////////////////////////////////////////////////////////////////////////


    double TFpart =
        tf1 *
        tf2 *
        tf3 *
        tf4 *
        tf5 *
        tf6
        ;

    double METpart =
        tf7
        ;

    double PDFpart = ggPdf( x1, x2 , Q);

    if(useME_)   prob *= MEpart;
    if(useJac_)  prob *= Jpart;
    if(useMET_)  prob *= METpart;
    if(useTF_)   prob *= TFpart;
    if(usePDF_)  prob *= PDFpart;

    ////////////////////////

    if( TMath::IsNaN(prob) ) {
        if(verbose_) {
            cout << tf1 << ", " << tf2 << ", " << tf3 << ", "<< tf4 << ", "<< tf5 << ", "<< tf6 << ", " << tf7 << endl;
            cout << MEpart << ", " << Jpart << ", " << PDFpart << endl;
        }
        prob = 0.;
    }

    return prob;
}


double MEIntegratorNew::probabilitySLNoBLep(const double* x, int sign) const {

    int errFlag = 0;
    double prob = 1.0;

    double Eq1           = x[0];
    double cosThetaBLep  = x[1];
    double phiBLep       = x[2];
    double cosThetaNu    = x[3];
    double phiNu         = x[4];
    double Eh1           = x[5];

    double Elep = jets_[0].P();

    // trasnform phiNu into an absolute phi:
    phiNu += eMEt_.Phi();
    if( phiNu < -PI ) phiNu += (2*PI);
    if( phiNu >  PI)  phiNu -= (2*PI);


    if(verbose_) {
        cout << "#" << evaluation_ << " SLNoBLep" << endl;
        cout << "Eq1 =          "  << Eq1 << endl;
        cout << "cosThetaBLep = "  << cosThetaBLep << endl;
        cout << "phiBLep =      "  << phiBLep << endl;
        cout << "cosThetaNu =   "  << cosThetaNu << endl;
        cout << "phiNu =        "  << phiNu  << endl;
        cout << "Eh1 =          "  << Eh1  << endl;
    }

    double Eq2, EbHad, cos1Had, cos2Had;
    int nSolTopHad = topHadEnergies( Eq1, Eq2, EbHad, cos1Had, cos2Had, errFlag );

    if(errFlag) {
        if(verbose_) cout << "Problems with topHadLostEnergies (" << nSolTopHad << " solutions)" << endl;
        return 0.0;
    }

    TVector3 eMiss(0.,0.,1.); // bHad lost
    eMiss.SetTheta( TMath::ACos( cosThetaBLep ) );
    eMiss.SetPhi  ( phiBLep );
    eMiss.SetMag  ( 1.);

    TVector3 eNu(0.,0.,1.); // neutrino
    double Enu, EbLep, cos1Lep, cos2Lep /*Jacob*/;
    int nSolTopLep = topLepBLostEnergies( phiNu, cosThetaNu, phiBLep, cosThetaBLep, Enu, EbLep, cos1Lep, cos2Lep, errFlag  );
    eNu.SetTheta( TMath::ACos( cosThetaNu ) );
    eNu.SetPhi  ( phiNu );
    eNu.SetMag  ( 1.);

    if(errFlag) {
        if(verbose_) cout << "Problems with topLepEnergies (" << nSolTopLep << " solutions)" << endl;
        return 0.0;
    }

    double Eh2, cos1Higgs;
    int nSolHiggs = higgsEnergies( Eh1, Eh2, cos1Higgs, errFlag );

    if(errFlag && hypo_==0) {
        if(verbose_) cout << "Problems with higgsEnergies (" << nSolHiggs << " solutions)" << endl;
        return 0.0;
    }

    if(hypo_==1) {
        Eh2       =  x[6];
        cos1Higgs = 1.; // dummy
    }

    if(verbose_) {
        cout << "Eq2   = " << Eq2 << " (Pt = " << Eq2*TMath::Sin(eMiss.Theta()) << ")" << endl;
        cout << "EbHad = " << EbHad << " (Pt = " << EbHad*TMath::Sin(eBHad_.Theta()) << ")" << endl;
        cout << "EbLep = " << EbLep << " (Pt = " << EbLep*TMath::Sin(eBLep_.Theta()) << ")" << endl;
        cout << "Enu = " << Enu << " (Pt = " << Enu*sqrt(1-cosThetaNu*cosThetaNu) << ")"  << endl;
        cout << "cos1Had = " << cos1Had << endl;
        cout << "cos2Had = " << cos2Had << endl;
        cout << "********" << endl;
    }

    TLorentzVector W1Had( eW1Had_*Eq1, Eq1 );
    TLorentzVector W2Had( eW2Had_*Eq2,  Eq2 );
    TLorentzVector WHad = W1Had + W2Had;
    TLorentzVector bHad ( eBHad_*TMath::Sqrt(EbHad*EbHad - Mb_*Mb_), EbHad );
    TLorentzVector topHad = WHad + bHad;

    if(verbose_  ) {
        cout << "W   had mass = " << WHad.M() << endl;
        cout << "Top had mass = " << topHad.M() << endl;
    }

    TLorentzVector WLepLep = jets_[0];
    TLorentzVector WLepNu( eNu*Enu, Enu);
    TLorentzVector WLep = WLepLep + WLepNu;
    TLorentzVector bLep  ( eMiss*TMath::Sqrt(EbLep*EbLep - Mb_*Mb_), EbLep );
    TLorentzVector topLep = WLep + bLep;

    if(verbose_  ) {
        cout << "W   lep mass = " << WLep.M() << endl;
        cout << "Top lep mass = " << topLep.M() << endl;
    }

    TLorentzVector higgs1(  eB1_*TMath::Sqrt(Eh1*Eh1 -  Mb_*Mb_), Eh1);
    TLorentzVector higgs2(  eB2_*TMath::Sqrt(Eh2*Eh2 -  Mb_*Mb_), Eh2);
    TLorentzVector higgs = higgs1 + higgs2;

    if(verbose_  ) {
        cout << "H   had mass = " << higgs.M() << endl;
    }


    TLorentzVector tot = topHad+topLep+higgs;

    double x1 = (  tot.Pz() + tot.E() )/SqrtS_;
    double x2 = ( -tot.Pz() + tot.E() )/SqrtS_;
    double Q  = (2*Mtop_ + M_)/2.;

    if( useDynamicalScale_ && hypo_==1 ) Q = TMath::Sqrt( 4*Mtop_*Mtop_ + TMath::Power(higgs1.Pt() + higgs2.Pt(), 2) );

    TVector3 boostToCMS  = tot.BoostVector();

    double me2 = 1.0;
    if(useME_==1 && top1Flag_ == +1 && top2Flag_ == -1)               // topLep = t,  topHad = tx
        me2 =  hypo_==0 ? meSquaredOpenLoops( &topLep, &topHad, &higgs, x1, x2  ): meSquaredOpenLoops_ttbb( &topLep, &topHad, &higgs1, &higgs2, x1, x2 );
    else if(useME_==1 && top1Flag_ == -1 && top2Flag_ == +1)          // topLep = tx, topHad = t
        me2 =  hypo_==0 ? meSquaredOpenLoops( &topHad, &topLep, &higgs, x1, x2  ): meSquaredOpenLoops_ttbb( &topLep, &topHad, &higgs1, &higgs2, x1, x2 );
    else {
        if(useME_==1 && verbose_) cout << "Undefined top flavors" << endl;
        me2 = 1.;
    }

    double MEpart = 1.0;
    if( useAnalyticalFormula_==0 )
        MEpart =
            topHadDensity(cos1Had,cos2Had) *
            topLepDensity(cos1Lep,cos2Lep) *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;
    else
        MEpart =
            topLepDensity_analytical( &topLep, &bLep, &WLepLep, &WLepNu ) *
            topHadDensity_analytical( &topHad, &bHad, &W1Had,   &W2Had )  *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;

    double Jpart =
        topHadJakobi( Eq1,  Eq2, EbHad, &WHad ) *
        topLepBLostJakobi( Enu, Elep, EbLep, &WLep ) *
        (hypo_==0 ? higgsJakobi( Eh1, Eh2 ) : Eh1*Eh2/4)
        ;

    double tf1 = 1.0;
    double tf2 = jetEnergyTF( jets_[3].Eta(), jets_[3].E(),  W1Had.E(),   "Light");
    double tf3 = jetEnergyTF( jets_[4].Eta(), jets_[4].E(),  W2Had.E(),   "Light");
    double tf4 = jetEnergyTF( jets_[5].Eta(), jets_[5].E(),  bHad.E(),    "Heavy");
    double tf5 = jetEnergyTF( jets_[6].Eta(), jets_[6].E(),  higgs1.E(),  "Heavy");
    double tf6 = jetEnergyTF( jets_[7].Eta(), jets_[7].E(),  higgs2.E(),  "Heavy");

    double dPx = WLepNu.Px() - jets_[1].Px();
    double dPy = WLepNu.Py() - jets_[1].Py();
    if( constrainToRecoil_ ) {
        dPx =  -(jets_[0]+jets_[1]/*+jets_[2]*/+jets_[3]+jets_[4]+jets_[5]+jets_[6]+jets_[7]).Px() + (tot-bLep).Px() ;
        dPy =  -(jets_[0]+jets_[1]/*+jets_[2]*/+jets_[3]+jets_[4]+jets_[5]+jets_[6]+jets_[7]).Py() + (tot-bLep).Py() ;
    }

    double tf7 = (Vx_*Vy_ - rho_*rho_*Vx_*Vy_)>0 ?
                 1./2./PI/TMath::Sqrt(Vx_*Vy_ - rho_*rho_*Vx_*Vy_)*TMath::Exp( -0.5*( 1/(1-rho_*rho_)*( dPx*dPx/Vx_ + dPy*dPy/Vy_ - 2*rho_*dPx*dPy/TMath::Sqrt(Vx_*Vy_) ) ) ) : 1.0 ;


    ///////////////////////////////////////////////////////////////////////////
    if( TMath::Abs(bLep.Eta())<2.5 ) {

        double PtBLep = bLep.Pt();

        string bin = "Bin0";
        if(  TMath::Abs( bLep.Eta() )<1.0 )
            bin = "Bin0";
        else
            bin = "Bin1";

        double param0resol = (jetParam_.find("param0resolHeavy"+bin))->second;
        double param1resol = (jetParam_.find("param1resolHeavy"+bin))->second;
        double param2resol = (jetParam_.find("param2resolHeavy"+bin))->second;
        double param0resp  = (jetParam_.find("param0respHeavy" +bin))->second;
        double param1resp  = (jetParam_.find("param1respHeavy" +bin))->second;

        //double Width  = EbLep*TMath::Sqrt( param0resol*param0resol/EbLep + param1resol*param1resol/EbLep/EbLep) * (PtBLep/EbLep);
        //double Mean   = (EbLep*param0resp + param1resp) * (PtBLep/EbLep) ;
        double Width  = TMath::Sqrt( (param0resol*param0resol) + EbLep*(param1resol*param1resol) + EbLep*EbLep*(param2resol*param2resol) ) * (PtBLep/EbLep);
        double Mean   = (EbLep*param0resp + param1resp) * (PtBLep/EbLep) ;

        tf1 = 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 )  ;

        if( deltaR(bLep, WLepLep)< 0.5 ) {
            if(verbose_) cout << "Overlap with lepton " << endl;
            tf1 = (PtBLep < 0.10*WLepLep.Pt()) ? 1.0 : 0.0;
        }
        else if( deltaR(bLep, W1Had)  < 0.5 ) {
            if(verbose_) cout << "Overlap with W1 " << endl;
            tf1 = 1.;
            tf2 = jetEnergyTF( jets_[3].Eta(), jets_[3].E(),  (W1Had.E()+bLep.E()),    "Light");
        }
        else if( deltaR(bLep, W2Had)  < 0.5 ) {
            if(verbose_) cout << "Overlap with W2 " << endl;
            tf1 = 1.;
            tf3 = jetEnergyTF( jets_[4].Eta(), jets_[4].E(),  (W2Had.E()+bLep.E()),    "Light");
        }
        else if( deltaR(bLep, bHad) < 0.5 ) {
            if(verbose_) cout << "Overlap with bHad " << endl;
            tf1 = 1.;
            tf4 = jetEnergyTF( jets_[5].Eta(), jets_[5].E(),  (bHad.E()+bLep.E()),     "Heavy");
        }
        else if( deltaR(bLep, higgs1) < 0.5 ) {
            if(verbose_) cout << "Overlap with h1 " << endl;
            tf1 = 1.;
            tf5 = jetEnergyTF( jets_[6].Eta(), jets_[6].E(),  (higgs1.E()+bLep.E()),   "Heavy");
        }
        else if( deltaR(bLep, higgs2) < 0.5 ) {
            if(verbose_) cout << "Overlap with h2 " << endl;
            tf1 = 1.;
            tf6 = jetEnergyTF( jets_[7].Eta(), jets_[7].E(),  (higgs2.E()+bLep.E()),   "Heavy");
        }
        else {}

    }
    ///////////////////////////////////////////////////////////////////////////


    double TFpart =
        tf1 *
        tf2 *
        tf3 *
        tf4 *
        tf5 *
        tf6
        ;

    double METpart =
        tf7
        ;

    double PDFpart = ggPdf( x1, x2 , Q);

    if(useME_)   prob *= MEpart;
    if(useJac_)  prob *= Jpart;
    if(useMET_)  prob *= METpart;
    if(useTF_)   prob *= TFpart;
    if(usePDF_)  prob *= PDFpart;

    ////////////////////////

    if( TMath::IsNaN(prob) ) {
        if(verbose_) {
            cout << tf1 << ", " << tf2 << ", " << tf3 << ", "<< tf4 << ", "<< tf5 << ", "<< tf6 << ", " << tf7 << endl;
            cout << MEpart << ", " << Jpart << ", " << PDFpart << endl;
        }
        prob = 0.;
    }

    return prob;
}



double MEIntegratorNew::probabilitySLNoHiggs(const double* x, int sign) const {

    int errFlag = 0;
    double prob = 1.0;

    double Eq1           = x[0];
    double cosThetaB2    = x[1];
    double phiB2         = x[2];
    double cosThetaNu    = x[3];
    double phiNu         = x[4];
    double Eh1           = x[5];

    double Elep = jets_[0].P();

    // trasnform phiNu into an absolute phi:
    phiNu += eMEt_.Phi();
    if( phiNu < -PI ) phiNu += (2*PI);
    if( phiNu >  PI)  phiNu -= (2*PI);


    if(verbose_) {
        cout << "#" << evaluation_ << " SLNoHiggs" << endl;
        cout << "Eq1 =          "  << Eq1 << endl;
        cout << "cosThetaB2 = "  << cosThetaB2 << endl;
        cout << "phiNuB2 =    "  << phiB2 << endl;
        cout << "cosThetaNu =   "  << cosThetaNu << endl;
        cout << "phiNu =        "  << phiNu  << endl;
        cout << "Eh1 =          "  << Eh1  << endl;
    }

    double Eq2, EbHad, cos1Had, cos2Had;
    int nSolTopHad = topHadEnergies( Eq1, Eq2, EbHad, cos1Had, cos2Had, errFlag );

    if(errFlag) {
        if(verbose_) cout << "Problems with topHadLostEnergies (" << nSolTopHad << " solutions)" << endl;
        return 0.0;
    }

    TVector3 eNu(0.,0.,1.); // neutrino
    double Enu, EbLep, cos1Lep, cos2Lep /*Jacob*/;
    int nSolTopLep = topLepEnergies( phiNu, cosThetaNu, Enu, EbLep, cos1Lep, cos2Lep, errFlag  );
    eNu.SetTheta( TMath::ACos( cosThetaNu ) );
    eNu.SetPhi  ( phiNu );
    eNu.SetMag  ( 1.);

    if(errFlag) {
        if(verbose_) cout << "Problems with topLepEnergies (" << nSolTopLep << " solutions)" << endl;
        return 0.0;
    }


    (const_cast<MEIntegratorNew*>(this)->eB2_).SetTheta( TMath::ACos( cosThetaB2 ) );
    (const_cast<MEIntegratorNew*>(this)->eB2_).SetPhi  ( phiB2 );
    (const_cast<MEIntegratorNew*>(this)->eB2_).SetMag  ( 1.);

    double Eh2, cos1Higgs;
    int nSolHiggs = higgsEnergies( Eh1, Eh2, cos1Higgs, errFlag );

    if(errFlag && hypo_==0) {
        if(verbose_) cout << "Problems with higgsEnergies (" << nSolHiggs << " solutions)" << endl;
        return 0.0;
    }

    if(hypo_==1) {
        Eh2       =  x[6];
        cos1Higgs = 1.; // dummy
    }

    if(verbose_) {
        cout << "EbHad = " << EbHad << " (Pt = " << EbHad*TMath::Sin(eBHad_.Theta()) << ")" << endl;
        cout << "EbLep = " << EbLep << " (Pt = " << EbLep*TMath::Sin(eBLep_.Theta()) << ")" << endl;
        cout << "Enu = " << Enu << " (Pt = " << Enu*sqrt(1-cosThetaNu*cosThetaNu) << ")"  << endl;
        cout << "cos1Had = " << cos1Had << endl;
        cout << "cos2Had = " << cos2Had << endl;
        cout << "********" << endl;
    }

    TLorentzVector W1Had( eW1Had_*Eq1,  Eq1 );
    TLorentzVector W2Had( eW2Had_*Eq2,  Eq2 );
    TLorentzVector WHad = W1Had + W2Had;
    TLorentzVector bHad ( eBHad_*TMath::Sqrt(EbHad*EbHad - Mb_*Mb_), EbHad );
    TLorentzVector topHad = WHad + bHad;

    if(verbose_ ) {
        cout << "W   had mass = " << WHad.M() << endl;
        cout << "Top had mass = " << topHad.M() << endl;
    }

    TLorentzVector WLepLep = jets_[0];
    TLorentzVector WLepNu( eNu*Enu, Enu);
    TLorentzVector WLep = WLepLep + WLepNu;
    TLorentzVector bLep  ( eBLep_*TMath::Sqrt(EbLep*EbLep - Mb_*Mb_), EbLep );
    TLorentzVector topLep = WLep + bLep;

    if(verbose_ ) {
        cout << "W   lep mass = " << WLep.M() << endl;
        cout << "Top lep mass = " << topLep.M() << endl;
    }

    TLorentzVector higgs1(  eB1_*TMath::Sqrt(Eh1*Eh1 -  Mb_*Mb_), Eh1);
    TLorentzVector higgs2(  eB2_*TMath::Sqrt(Eh2*Eh2 -  Mb_*Mb_), Eh2);
    TLorentzVector higgs = higgs1 + higgs2;

    if(verbose_ ) {
        cout << "H   had mass = " << higgs.M() << endl;
    }


    TLorentzVector tot = topHad+topLep+higgs;

    double x1 = (  tot.Pz() + tot.E() )/SqrtS_;
    double x2 = ( -tot.Pz() + tot.E() )/SqrtS_;
    double Q  = (2*Mtop_ + M_)/2.;

    if( useDynamicalScale_ && hypo_==1 ) Q = TMath::Sqrt( 4*Mtop_*Mtop_ + TMath::Power(higgs1.Pt() + higgs2.Pt(), 2) );

    TVector3 boostToCMS  = tot.BoostVector();

    double me2 = 1.0;
    if(useME_==1 && top1Flag_ == +1 && top2Flag_ == -1)               // topLep = t,  topHad = tx
        me2 =  hypo_==0 ? meSquaredOpenLoops( &topLep, &topHad, &higgs, x1, x2  ): meSquaredOpenLoops_ttbb( &topLep, &topHad, &higgs1, &higgs2, x1, x2 );
    else if(useME_==1 && top1Flag_ == -1 && top2Flag_ == +1)          // topLep = tx, topHad = t
        me2 =  hypo_==0 ? meSquaredOpenLoops( &topHad, &topLep, &higgs, x1, x2  ): meSquaredOpenLoops_ttbb( &topLep, &topHad, &higgs1, &higgs2, x1, x2 );
    else {
        if(useME_==1 && verbose_) cout << "Undefined top flavors" << endl;
        me2 = 1.;
    }

    double MEpart = 1.0;
    if( useAnalyticalFormula_==0 )
        MEpart =
            topHadDensity(cos1Had,cos2Had) *
            topLepDensity(cos1Lep,cos2Lep) *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;
    else
        MEpart =
            topLepDensity_analytical( &topLep, &bLep, &WLepLep, &WLepNu ) *
            topHadDensity_analytical( &topHad, &bHad, &W1Had,   &W2Had )  *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;

    double Jpart =
        topHadBLostJakobi( Eq1,  Eq2, EbHad, &WHad ) *
        topLepJakobi( Enu, Elep, EbLep, &WLep ) *
        (hypo_==0 ? higgsJakobi( Eh1, Eh2 ) : Eh1*Eh2/4)
        ;

    double tf1 = jetEnergyTF( jets_[2].Eta(), jets_[2].E(),  bLep.E(),    "Heavy");
    double tf2 = jetEnergyTF( jets_[3].Eta(), jets_[3].E(),  W1Had.E(),   "Light");
    double tf3 = jetEnergyTF( jets_[4].Eta(), jets_[4].E(),  W2Had.E(),   "Light");
    double tf4 = jetEnergyTF( jets_[5].Eta(), jets_[5].E(),  bHad.E(),    "Heavy");
    double tf5 = jetEnergyTF( jets_[6].Eta(), jets_[6].E(),  higgs1.E(),  "Heavy");
    double tf6 = 1.0;

    double dPx = WLepNu.Px() - jets_[1].Px();
    double dPy = WLepNu.Py() - jets_[1].Py();
    if( constrainToRecoil_ ) {
        dPx =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]+jets_[5]+jets_[6]/*+jets_[7]*/).Px() + (tot-higgs2).Px() ;
        dPy =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]+jets_[4]+jets_[5]+jets_[6]/*+jets_[7]*/).Py() + (tot-higgs2).Py() ;
    }

    double tf7 = (Vx_*Vy_ - rho_*rho_*Vx_*Vy_)>0 ?
                 1./2./PI/TMath::Sqrt(Vx_*Vy_ - rho_*rho_*Vx_*Vy_)*TMath::Exp( -0.5*( 1/(1-rho_*rho_)*( dPx*dPx/Vx_ + dPy*dPy/Vy_ - 2*rho_*dPx*dPy/TMath::Sqrt(Vx_*Vy_) ) ) ) : 1.0 ;


    ///////////////////////////////////////////////////////////////////////////
    if( TMath::Abs(higgs2.Eta())<2.5 ) {

        double PtB2 = higgs2.Pt();

        string bin = "Bin0";
        if(  TMath::Abs( higgs2.Eta() )<1.0 )
            bin = "Bin0";
        else
            bin = "Bin1";

        double param0resol = (jetParam_.find("param0resolHeavy"+bin))->second;
        double param1resol = (jetParam_.find("param1resolHeavy"+bin))->second;
        double param2resol = (jetParam_.find("param2resolHeavy"+bin))->second;
        double param0resp  = (jetParam_.find("param0respHeavy" +bin))->second;
        double param1resp  = (jetParam_.find("param1respHeavy" +bin))->second;

        //double Width  = Eh2*TMath::Sqrt( param0resol*param0resol/Eh2 + param1resol*param1resol/Eh2/Eh2) * (PtB2/Eh2);
        //double Mean   = (Eh2*param0resp + param1resp) * (PtB2/Eh2) ;
        double Width  = TMath::Sqrt( (param0resol*param0resol) + Eh2*(param1resol*param1resol) + Eh2*Eh2*(param2resol*param2resol) )  * (PtB2/Eh2);
        double Mean   = (Eh2*param0resp + param1resp) * (PtB2/Eh2) ;

        tf6 = 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 )  ;

        if( deltaR(higgs2, WLepLep)< 0.5 ) {
            if(verbose_) cout << "Overlap with lepton " << endl;
            tf6 = (PtB2 < 0.10*WLepLep.Pt()) ? 1.0 : 0.0;
        }
        else if( deltaR(higgs2, bLep)  < 0.5 ) {
            if(verbose_) cout << "Overlap with bLep " << endl;
            tf6 = 1.;
            tf1 = jetEnergyTF( jets_[2].Eta(), jets_[2].E(),  (bLep.E()+higgs2.E()),     "Heavy");
        }
        else if( deltaR(higgs2, W1Had)  < 0.5 ) {
            if(verbose_) cout << "Overlap with W1 " << endl;
            tf6 = 1.;
            tf2 = jetEnergyTF( jets_[3].Eta(), jets_[3].E(),  (W1Had.E()+higgs2.E()),    "Light");
        }
        else if( deltaR(higgs2, W2Had)  < 0.5 ) {
            if(verbose_) cout << "Overlap with W2 " << endl;
            tf6 = 1.;
            tf3 = jetEnergyTF( jets_[4].Eta(), jets_[4].E(),  (W2Had.E()+higgs2.E()),    "Light");
        }
        else if( deltaR(higgs2, bHad)  < 0.5 ) {
            if(verbose_) cout << "Overlap with bHad " << endl;
            tf6 = 1.;
            tf4 = jetEnergyTF( jets_[5].Eta(), jets_[5].E(),  (bHad.E()+higgs2.E()),     "Heavy");
        }
        else if( deltaR(higgs2, higgs1) < 0.5 ) {
            if(verbose_) cout << "Overlap with h1 " << endl;
            tf6 = 1.;
            tf5 = jetEnergyTF( jets_[6].Eta(), jets_[6].E(),  (higgs1.E()+higgs2.E()),   "Heavy");
        }
        else {}

    }
    ///////////////////////////////////////////////////////////////////////////


    double TFpart =
        tf1 *
        tf2 *
        tf3 *
        tf4 *
        tf5 *
        tf6
        ;

    double METpart =
        tf7
        ;

    double PDFpart = ggPdf( x1, x2 , Q);

    if(useME_)   prob *= MEpart;
    if(useJac_)  prob *= Jpart;
    if(useMET_)  prob *= METpart;
    if(useTF_)   prob *= TFpart;
    if(usePDF_)  prob *= PDFpart;

    ////////////////////////

    if( TMath::IsNaN(prob) ) {
        if(verbose_) {
            cout << tf1 << ", " << tf2 << ", " << tf3 << ", "<< tf4 << ", "<< tf5 << ", "<< tf6 << ", " << tf7 << endl;
            cout << MEpart << ", " << Jpart << ", " << PDFpart << endl;
        }
        prob = 0.;
    }

    return prob;
}




double MEIntegratorNew::probabilityDL(const double* x, int sign) const {

    int errFlag = 0;
    double prob = 1.0;

    double cosThetaNu1  = x[0];
    double phiNu1       = x[1];
    double cosThetaNu2  = x[2];
    double phiNu2       = x[3];
    double Eh1          = x[4];

    double Elep1 = jets_[0].P();
    double Elep2 = jets_[3].P();

    // trasnform phiNu into an absolute phi:
    //phiNu += eMEt_.Phi();
    //if( phiNu < -PI ) phiNu += (2*PI);
    //if( phiNu >  PI)  phiNu -= (2*PI);


    if(verbose_) {
        cout << "#" << evaluation_ << " DL" << endl;
        cout << "cosThetaNu1 = " << cosThetaNu1 << endl;
        cout << "phiNu1 = "      << phiNu1  << endl;
        cout << "cosThetaNu2 = " << cosThetaNu2 << endl;
        cout << "phiNu2 = "      << phiNu2  << endl;
        cout << "Eh1 = "         << Eh1  << endl;
    }


    TVector3 eNu1(0.,0.,1.); // neutrino
    double Enu1, EbLep1, cos1Lep1, cos2Lep1;
    int nSolTopLep1 = topLepEnergies( phiNu1, cosThetaNu1, Enu1, EbLep1, cos1Lep1, cos2Lep1, errFlag  );
    eNu1.SetTheta( TMath::ACos( cosThetaNu1 ) );
    eNu1.SetPhi  ( phiNu1 );
    eNu1.SetMag  ( 1.);

    if(errFlag) {
        if(verbose_) cout << "Problems with topLepEnergies (" << nSolTopLep1 << " solutions)" << endl;
        return 0.0;
    }

    TVector3 eNu2(0.,0.,1.); // neutrino
    double Enu2, EbLep2, cos1Lep2, cos2Lep2;
    int nSolTopLep2 = topLep2Energies( phiNu2, cosThetaNu2, Enu2, EbLep2, cos1Lep2, cos2Lep2, errFlag  );
    eNu2.SetTheta( TMath::ACos( cosThetaNu2 ) );
    eNu2.SetPhi  ( phiNu2 );
    eNu2.SetMag  ( 1.);

    if(errFlag) {
        if(verbose_) cout << "Problems with topLepEnergies2 (" << nSolTopLep2 << " solutions)" << endl;
        return 0.0;
    }

    double Eh2, cos1Higgs;
    int nSolHiggs = higgsEnergies( Eh1, Eh2, cos1Higgs, errFlag );

    if(errFlag && hypo_==0) {
        if(verbose_) cout << "Problems with higgsEnergies (" << nSolHiggs << " solutions)" << endl;
        return 0.0;
    }

    if(hypo_==1) {
        Eh2       =  x[5];
        cos1Higgs = 1.; // dummy
    }

    if(verbose_) {
        cout << "********" << endl;
    }

    TLorentzVector WLep1Lep( eLep_*Elep1, Elep1 );
    TLorentzVector WLep1Nu ( eNu1*Enu1,   Enu1 );
    TLorentzVector WLep1 = WLep1Lep + WLep1Nu;
    TLorentzVector bLep1   ( eBLep_*TMath::Sqrt(EbLep1*EbLep1 - Mb_*Mb_), EbLep1 );
    TLorentzVector topLep1 = WLep1 + bLep1;

    if(verbose_ ) {
        cout << "W   lep1 mass = " << WLep1.M() << endl;
        cout << "Top lep1 mass = " << topLep1.M() << endl;
    }

    TLorentzVector WLep2Lep( eW1Had_*Elep2, Elep2 );
    TLorentzVector WLep2Nu ( eNu2*Enu2,     Enu2 );
    TLorentzVector WLep2 = WLep2Lep + WLep2Nu;
    TLorentzVector bLep2   ( eBHad_*TMath::Sqrt(EbLep2*EbLep2 - Mb_*Mb_), EbLep2 );
    TLorentzVector topLep2 = WLep2 + bLep2;

    if(verbose_ ) {
        cout << "W   lep2 mass = " << WLep2.M() << endl;
        cout << "Top lep2 mass = " << topLep2.M() << endl;
    }

    TLorentzVector higgs1(  eB1_*TMath::Sqrt(Eh1*Eh1 -  Mb_*Mb_), Eh1);
    TLorentzVector higgs2(  eB2_*TMath::Sqrt(Eh2*Eh2 -  Mb_*Mb_), Eh2);
    TLorentzVector higgs = higgs1 + higgs2;

    TLorentzVector tot = topLep1+topLep2+higgs;

    double x1 = (  tot.Pz() + tot.E() )/SqrtS_;
    double x2 = ( -tot.Pz() + tot.E() )/SqrtS_;
    double Q  = (2*Mtop_ + M_)/2.;

    if( useDynamicalScale_ && hypo_==1 ) Q = TMath::Sqrt( 4*Mtop_*Mtop_ + TMath::Power(higgs1.Pt() + higgs2.Pt(), 2) );

    double me2;
    if(useME_==1 && top1Flag_ == +1 && top2Flag_ == -1)               // topLep = t,  topHad = tx
        me2 =  hypo_==0 ? meSquaredOpenLoops( &topLep1, &topLep2, &higgs, x1, x2 ): meSquaredOpenLoops_ttbb( &topLep1, &topLep2, &higgs1, &higgs2, x1, x2 );
    else if(useME_==1 && top1Flag_ == -1 && top2Flag_ == +1)          // topLep = tx, topHad = t
        me2 =  hypo_==0 ? meSquaredOpenLoops( &topLep1, &topLep2, &higgs, x1, x2 ): meSquaredOpenLoops_ttbb( &topLep1, &topLep2, &higgs1, &higgs2, x1, x2 );
    else {
        if(verbose_) cout << "Undefined top flavors" << endl;
        me2 = 1.;
    }


    double MEpart = 1.0;
    if( useAnalyticalFormula_==0 )
        MEpart =
            topLepDensity(cos1Lep1,cos2Lep1) *
            topLepDensity(cos1Lep2,cos2Lep2) *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;
    else
        MEpart =
            topLepDensity_analytical( &topLep1, &bLep1, &WLep1Lep, &WLep1Nu ) *
            topLepDensity_analytical( &topLep2, &bLep2, &WLep2Lep, &WLep2Nu ) *
            (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0)*
            me2 ;


    double Jpart =
        topLepJakobi( Enu1, Elep1, EbLep1, &WLep1 ) *
        topLepJakobi( Enu2, Elep2, EbLep2, &WLep2 ) *
        (hypo_==0 ? higgsJakobi( Eh1, Eh2 ) : Eh1*Eh2/4)
        ;

    double tf1 = jetEnergyTF( jets_[2].Eta(), jets_[2].E(),  bLep1.E(),   "Heavy");
    double tf4 = jetEnergyTF( jets_[5].Eta(), jets_[5].E(),  bLep2.E(),   "Heavy");
    double tf5 = jetEnergyTF( jets_[6].Eta(), jets_[6].E(),  higgs1.E(),  "Heavy");
    double tf6 = jetEnergyTF( jets_[7].Eta(), jets_[7].E(),  higgs2.E(),  "Heavy");

    double dPx = (WLep1Nu+WLep2Nu).Px() - jets_[1].Px();
    double dPy = (WLep1Nu+WLep2Nu).Py() - jets_[1].Py();
    if( constrainToRecoil_ ) {
        dPx =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]/*+jets_[4]*/+jets_[5]+jets_[6]+jets_[7]).Px() + (tot).Px() ;
        dPy =  -(jets_[0]+jets_[1]+jets_[2]+jets_[3]/*+jets_[4]*/+jets_[5]+jets_[6]+jets_[7]).Py() + (tot).Py() ;
    }

    double tf7 =
        (Vx_*Vy_ - rho_*rho_*Vx_*Vy_)>0 ? 1./2./PI/TMath::Sqrt(Vx_*Vy_ - rho_*rho_*Vx_*Vy_)*TMath::Exp( -0.5*( 1/(1-rho_*rho_)*( dPx*dPx/Vx_ + dPy*dPy/Vy_ - 2*rho_*dPx*dPy/TMath::Sqrt(Vx_*Vy_) ) ) ) : 1.0 ;

    //cout << "dPx= " << dPx << endl;
    //cout << "dPy= " << dPy << endl;
    //cout << " ==> " << tf7 << endl;

    double TFpart =
        tf1 *
        tf4 *
        tf5 *
        tf6
        ;

    double METpart =
        tf7
        ;

    double PDFpart = ggPdf( x1, x2 , Q);

    if(useME_)  prob *= MEpart;
    if(useJac_) prob *= Jpart;
    if(useMET_) prob *= METpart;
    if(useTF_)  prob *= TFpart;
    if(usePDF_) prob *= PDFpart;

    ////////////////////////

    if( TMath::IsNaN(prob) ) {
        if(verbose_) {
            cout << tf1 << ", " << tf4 << ", "<< tf5 << ", "<< tf6 << ", " << tf7 << endl;
            cout << MEpart << ", " << Jpart << ", " << PDFpart << endl;
        }
        prob = 0.;
    }

    return prob;
}




double MEIntegratorNew::probabilitySLUnconstrained(const double* x, int acceptance) const {

    int errFlag = 0;
    double prob = 1.0;

    (const_cast<MEIntegratorNew*>(this)->jets_).clear();

    //return prob;
    //cout << "Start" << endl;

    const_cast<MEIntegratorNew*>(this)->top1Flag_ = +1;
    const_cast<MEIntegratorNew*>(this)->top2Flag_ = -1;

    //cout << "flags" << endl;

    // top lep
    double cosThetaLep = x[0];
    double phiLep      = x[1];
    double Elep        = x[2];
    double cosThetaNu  = x[3];
    double phiNu       = x[4];
    double cosThetaBLep= x[5];
    double phiBLep     = x[6];

    //cout << "First read" << endl;

    TVector3 eLep(0.,0.,1.);
    eLep.SetTheta( TMath::ACos( cosThetaLep ) );
    eLep.SetPhi  ( phiLep );
    eLep.SetMag  ( 1.);
    const_cast<MEIntegratorNew*>(this)->eLep_ = eLep;
    TLorentzVector WLepLep( eLep_*Elep, Elep);
    TLorentzVector dummy( TVector3(1,0,0) , 1.0);
    (const_cast<MEIntegratorNew*>(this)->jets_).push_back( WLepLep );
    (const_cast<MEIntegratorNew*>(this)->jets_).push_back( dummy ); // tmp for MET
    (const_cast<MEIntegratorNew*>(this)->jets_).push_back( dummy ); // tmp for BLEP

    //cout << "Lep" << endl;

    TVector3 eMEt(0.,0.,1.);
    eMEt.SetTheta( TMath::ACos( cosThetaNu ) );
    eMEt.SetPhi  ( phiNu );
    eMEt.SetMag  ( 1.);
    const_cast<MEIntegratorNew*>(this)->eMEt_ = eMEt;

    //cout << "MET" << endl;

    TVector3 eBLep(0.,0.,1.);
    eBLep.SetTheta( TMath::ACos( cosThetaBLep ) );
    eBLep.SetPhi  ( phiBLep );
    eBLep.SetMag  ( 1.);
    const_cast<MEIntegratorNew*>(this)->eBLep_ = eBLep;

    //cout << "BLep" << endl;

    // top had
    double Eq1         = x[7];
    double cosThetaq1  = x[8];
    double phiq1       = x[9];
    double cosThetaq2  = x[10];
    double phiq2       = x[11];
    double cosThetaBHad= x[12];
    double phiBHad     = x[13];

    TVector3 eW1Had(0.,0.,1.);
    eW1Had.SetTheta( TMath::ACos( cosThetaq1 ) );
    eW1Had.SetPhi  ( phiq1 );
    eW1Had.SetMag  ( 1.);
    const_cast<MEIntegratorNew*>(this)->eW1Had_ = eW1Had;

    TVector3 eW2Had(0.,0.,1.);
    eW2Had.SetTheta( TMath::ACos( cosThetaq2 ) );
    eW2Had.SetPhi  ( phiq2 );
    eW2Had.SetMag  ( 1.);
    const_cast<MEIntegratorNew*>(this)->eW2Had_ = eW2Had;

    TVector3 eBHad(0.,0.,1.);
    eBHad.SetTheta( TMath::ACos( cosThetaBHad ) );
    eBHad.SetPhi  ( phiBHad );
    eBHad.SetMag  ( 1.);
    const_cast<MEIntegratorNew*>(this)->eBHad_ = eBHad;

    // higgs
    double Eh1         = x[14];
    double cosThetah1  = x[15];
    double phih1       = x[16];
    double cosThetah2  = x[17]; // can eliminate
    double phih2       = x[18]; // can eliminate

    TVector3 eB1(0.,0.,1.);
    eB1.SetTheta( TMath::ACos( cosThetah1 ) );
    eB1.SetPhi  ( phih1 );
    eB1.SetMag  ( 1.);
    const_cast<MEIntegratorNew*>(this)->eB1_ = eB1;

    TVector3 eB2(0.,0.,1.);
    eB2.SetTheta( TMath::ACos( cosThetah2 ) );
    eB2.SetPhi  ( phih2 );
    eB2.SetMag  ( 1.);
    const_cast<MEIntegratorNew*>(this)->eB2_ = eB2;


    double Eq2, EbHad, cos1Had, cos2Had;
    int nSolTopHad = topHadLostEnergies( phiq2, cosThetaq2, Eq2, Eq1, EbHad, cos1Had, cos2Had, errFlag );

    if(errFlag) {
        if(verbose_) cout << "Problems with topHadLostEnergies (" << nSolTopHad << " solutions)" << endl;
        return 0.0;
    }

    TLorentzVector W1Had( eW1Had_*Eq1, Eq1);
    (const_cast<MEIntegratorNew*>(this)->jets_).push_back( W1Had );
    TLorentzVector W2Had( eW2Had_*Eq2, Eq2);
    (const_cast<MEIntegratorNew*>(this)->jets_).push_back( W2Had );
    TLorentzVector bHad( eBHad_*TMath::Sqrt(EbHad*EbHad - Mb_*Mb_), EbHad);
    (const_cast<MEIntegratorNew*>(this)->jets_).push_back( bHad);
    TLorentzVector WHad = W1Had + W2Had;
    TLorentzVector topHad = WHad + bHad;


    double Enu, EbLep, cos1Lep, cos2Lep;
    int nSolTopLep = topLepEnergies( phiNu, cosThetaNu, Enu, EbLep, cos1Lep, cos2Lep, errFlag  );

    TLorentzVector WLepNu( eMEt_*Enu, Enu);
    (const_cast<MEIntegratorNew*>(this)->jets_)[1] = WLepNu;
    TLorentzVector bLep( eBLep_*TMath::Sqrt(EbLep*EbLep - Mb_*Mb_), EbLep);
    (const_cast<MEIntegratorNew*>(this)->jets_)[2] = bLep;
    TLorentzVector WLep = WLepLep + WLepNu;
    TLorentzVector topLep = WLep + bLep;

    if(errFlag) {
        if(verbose_) cout << "Problems with topLepEnergies (" << nSolTopLep << " solutions)" << endl;
        return 0.0;
    }

    // impose balance
    TLorentzVector higgs1( eB1_*TMath::Sqrt(Eh1*Eh1 - Mb_*Mb_), Eh1);
    (const_cast<MEIntegratorNew*>(this)->jets_).push_back(  higgs1 );
    //const_cast<MEIntegratorNew*>(this)->eB2_ = -(topHad.Vect() + topLep.Vect() + higgs1.Vect()).Unit();

    double Eh2, cos1Higgs;
    int nSolHiggs = higgsEnergies( Eh1, Eh2, cos1Higgs, errFlag );

    if(hypo_==1) {
        Eh2       =  x[19];
        cos1Higgs = 1.; // dummy
    }

    TLorentzVector higgs2( eB2_*TMath::Sqrt(Eh2*Eh2 - Mb_*Mb_), Eh2);
    (const_cast<MEIntegratorNew*>(this)->jets_).push_back( higgs2 );
    TLorentzVector higgs = higgs1 + higgs2;

    if(errFlag && hypo_==0) {
        if(verbose_) cout << "Problems with higgsEnergies (" << nSolHiggs << " solutions)" << endl;
        return 0.0;
    }
    if(hypo_==1) {
        if( deltaR(higgs1,higgs2)<0.5 ||  higgs1.Pt()<20 || higgs2.Pt()<20)  return 0.0;
    }

    //cout << topHad.M() << ", " << ", " << WHad.M() << ", " << topLep.M() << ", " << WLep.M() << ", " << higgs.M() << endl;

    TLorentzVector tot = topHad+topLep+higgs;

    double x1 = (  tot.Pz() + tot.E() )/SqrtS_;
    double x2 = ( -tot.Pz() + tot.E() )/SqrtS_;
    double Q  = (2*Mtop_ + M_)/2.;

    if( useDynamicalScale_ && hypo_==1 ) Q = TMath::Sqrt( 4*Mtop_*Mtop_ + TMath::Power(higgs1.Pt() + higgs2.Pt(), 2) );

    float SumPt  = tot.Pt() ;
    //cout << "Sum Pt = " << tot.Pt() << endl;

    double me2 = 1.0;
    if(useME_==1 && top1Flag_ == +1 && top2Flag_ == -1)               // topLep = t,  topHad = tx
        me2 = hypo_==0 ? meSquaredOpenLoops( &topLep, &topHad, &higgs, x1, x2 ) : meSquaredOpenLoops_ttbb( &topLep, &topHad, &higgs1, &higgs2, x1, x2 );
    else if(useME_==1 && top1Flag_ == -1 && top2Flag_ == +1)          // topLep = tx, topHad = t
        me2 = hypo_==0 ? meSquaredOpenLoops( &topHad, &topLep, &higgs, x1, x2 ) : meSquaredOpenLoops_ttbb( &topHad, &topLep, &higgs1, &higgs2, x1, x2 );
    else {
        if(useME_==1 && verbose_) cout << "Undefined top flavors" << endl;
        me2 = 1.;
    }

    //cout << "ME2 = " << me2 << endl;

    double MEpart =
        topHadDensity(cos1Had,cos2Had) *
        topLepDensity(cos1Lep,cos2Lep) *
        (hypo_==0 ? higgsDensity(cos1Higgs) : 1.0) *
        me2 ;

    double Jpart =
        topHadLostJakobi( Eq1,  Eq2, EbHad, &WHad ) *
        topLepJakobi( Enu, Elep, EbLep, &WLep ) *
        (hypo_==0 ? higgsJakobi(  Eh1, Eh2 ) : Eh1*Eh2/4)
        ;



    double AccPart = 1.0;
    if( acceptance==1 ) {

        // no overlap
        for( unsigned int j = 2; j < 7; j++) {
            if( TMath::Abs(jets_[j].Eta())<2.5 && deltaR(jets_[j], jets_[0])<0.50 ) {
                AccPart *= 0.0;
                continue;
            }
            for( unsigned int jj = j+1; jj < 8; jj++) {
                if( TMath::Abs(jets_[j].Eta())<2.5 && TMath::Abs(jets_[jj].Eta())<2.5 &&
                        deltaR(jets_[j], jets_[jj])<0.50 ) AccPart *= 0.0;
            }
        }

        //lep pt
        if( jets_[0].Pt()<20 || TMath::Abs(jets_[0].Eta())>2.1 ) AccPart *= 0.0;


        if( intType_ == SLAcc ) {

            for(unsigned int j = 2; j <8; j++) {

                if(TMath::Abs(jets_[j].Eta())>2.5) continue;

                string flavor = "Light";
                if(j==2 || j>=5) flavor = "Heavy";

                string bin = "Bin0";
                if(  TMath::Abs( jets_[j].Eta() )<1.0 )
                    bin = "Bin0";
                else
                    bin = "Bin1";

                double param0resol = (jetParam_.find("param0resol"+flavor+bin))->second;
                double param1resol = (jetParam_.find("param1resol"+flavor+bin))->second;
                double param2resol = (jetParam_.find("param2resol"+flavor+bin))->second;
                double param0resp  = (jetParam_.find("param0resp" +flavor+bin))->second;
                double param1resp  = (jetParam_.find("param1resp" +flavor+bin))->second;

                //double Width  = jets_[j].E()*TMath::Sqrt( param0resol*param0resol/jets_[j].E() + param1resol*param1resol/jets_[j].E()/jets_[j].E()) * TMath::Sin( jets_[j].Theta() );
                //double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;
                double Width  = TMath::Sqrt( (param0resol*param0resol) + jets_[j].E()*(param1resol*param1resol) + jets_[j].E()*jets_[j].E()*(param2resol*param2resol) ) * TMath::Sin( jets_[j].Theta() );
                double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;

                AccPart *= (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
            }

        }
        else if( intType_ == SLAcc2wj) {

            for(unsigned int j = 2; j <8; j++) {

                if(TMath::Abs(jets_[j].Eta())>2.5) {
                    AccPart *= 0.0;
                    continue;
                }

                string flavor = "Light";
                if(j==2 || j>=5) flavor = "Heavy";

                string bin = "Bin0";
                if(  TMath::Abs( jets_[j].Eta() )<1.0 )
                    bin = "Bin0";
                else
                    bin = "Bin1";

                double param0resol = (jetParam_.find("param0resol"+flavor+bin))->second;
                double param1resol = (jetParam_.find("param1resol"+flavor+bin))->second;
                double param2resol = (jetParam_.find("param2resol"+flavor+bin))->second;
                double param0resp  = (jetParam_.find("param0resp" +flavor+bin))->second;
                double param1resp  = (jetParam_.find("param1resp" +flavor+bin))->second;

                //double Width  =  jets_[j].E()*TMath::Sqrt( param0resol*param0resol/jets_[j].E() + param1resol*param1resol/jets_[j].E()/jets_[j].E()) * TMath::Sin( jets_[j].Theta() );
                //double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;
                double Width  = TMath::Sqrt( (param0resol*param0resol) + jets_[j].E()*(param1resol*param1resol) + jets_[j].E()*jets_[j].E()*(param2resol*param2resol) ) * TMath::Sin( jets_[j].Theta() );
                double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;

                AccPart *= (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
            }

        }
        else if( intType_ == SLAcc1wj) {

            double AccW1 = 1.0;
            double AccW2 = 1.0;
            for(unsigned int j = 2; j <8; j++) {

                if(j!=3 && j!=4 && TMath::Abs(jets_[j].Eta())>2.5) {
                    AccPart *= 0.0;
                    continue;
                }

                string flavor = "Light";
                if(j==2 || j>=5) flavor = "Heavy";

                string bin = "Bin0";
                if(  TMath::Abs( jets_[j].Eta() )<1.0 )
                    bin = "Bin0";
                else
                    bin = "Bin1";

                double param0resol = (jetParam_.find("param0resol"+flavor+bin))->second;
                double param1resol = (jetParam_.find("param1resol"+flavor+bin))->second;
                double param2resol = (jetParam_.find("param2resol"+flavor+bin))->second;
                double param0resp  = (jetParam_.find("param0resp" +flavor+bin))->second;
                double param1resp  = (jetParam_.find("param1resp" +flavor+bin))->second;

                //double Width  = jets_[j].E()*TMath::Sqrt( param0resol*param0resol/jets_[j].E() + param1resol*param1resol/jets_[j].E()/jets_[j].E()) * TMath::Sin( jets_[j].Theta() );
                //double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;
                double Width  = TMath::Sqrt( (param0resol*param0resol) + jets_[j].E()*(param1resol*param1resol) + jets_[j].E()*jets_[j].E()*(param2resol*param2resol) ) * TMath::Sin( jets_[j].Theta() );
                double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;

                if(j!=3 && j!=4)
                    AccPart *= (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
                else {
                    if(j==3)
                        AccW1 *= (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
                    else
                        AccW2 *= (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
                }
            }

            if( TMath::Abs(jets_[3].Eta())>2.5 && TMath::Abs(jets_[4].Eta())>2.5 )
                AccPart *= 0.0;
            else if( TMath::Abs(jets_[3].Eta())<2.5 && TMath::Abs(jets_[4].Eta())>2.5 )
                AccPart *= AccW1;
            else if( TMath::Abs(jets_[3].Eta())>2.5 && TMath::Abs(jets_[4].Eta())<2.5 )
                AccPart *= AccW2;
            else
                AccPart *= ( AccW1*(1-AccW2) +  (1-AccW1)*AccW2 );

        }
        else if( intType_ == SLAccNoBHad ) {

            for(unsigned int j = 2; j <8; j++) {

                if(j!=5 && TMath::Abs(jets_[j].Eta())>2.5) {
                    AccPart *= 0.0;
                    continue;
                }

                string flavor = "Light";
                if(j==2 || j>=5) flavor = "Heavy";

                string bin = "Bin0";
                if(  TMath::Abs( jets_[j].Eta() )<1.0 )
                    bin = "Bin0";
                else
                    bin = "Bin1";

                double param0resol = (jetParam_.find("param0resol"+flavor+bin))->second;
                double param1resol = (jetParam_.find("param1resol"+flavor+bin))->second;
                double param2resol = (jetParam_.find("param2resol"+flavor+bin))->second;
                double param0resp  = (jetParam_.find("param0resp" +flavor+bin))->second;
                double param1resp  = (jetParam_.find("param1resp" +flavor+bin))->second;

                //double Width  = jets_[j].E()*TMath::Sqrt( param0resol*param0resol/jets_[j].E() + param1resol*param1resol/jets_[j].E()/jets_[j].E()) * TMath::Sin( jets_[j].Theta() );
                //double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;
                double Width  = TMath::Sqrt( (param0resol*param0resol) + jets_[j].E()*(param1resol*param1resol) + jets_[j].E()*jets_[j].E()*(param2resol*param2resol) ) * TMath::Sin( jets_[j].Theta() );
                double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;

                if(j!=5)
                    AccPart *= (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
                else if( j==5 && TMath::Abs( jets_[j].Eta() )>2.5 )
                    AccPart *= 1.0;
                else if( j==5 && TMath::Abs( jets_[j].Eta() )<2.5 )
                    AccPart *= 1 - (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
                else {}

            }

        }
        else if( intType_ == SLAccNoBLep) {

            for(unsigned int j = 2; j <8; j++) {

                if(j!=2 && TMath::Abs(jets_[j].Eta())>2.5) {
                    AccPart *= 0.0;
                    continue;
                }

                string flavor = "Light";
                if(j==2 || j>=5) flavor = "Heavy";

                string bin = "Bin0";
                if(  TMath::Abs( jets_[j].Eta() )<1.0 )
                    bin = "Bin0";
                else
                    bin = "Bin1";

                double param0resol = (jetParam_.find("param0resol"+flavor+bin))->second;
                double param1resol = (jetParam_.find("param1resol"+flavor+bin))->second;
                double param2resol = (jetParam_.find("param2resol"+flavor+bin))->second;
                double param0resp  = (jetParam_.find("param0resp" +flavor+bin))->second;
                double param1resp  = (jetParam_.find("param1resp" +flavor+bin))->second;

                //double Width  = jets_[j].E()*TMath::Sqrt( param0resol*param0resol/jets_[j].E() + param1resol*param1resol/jets_[j].E()/jets_[j].E()) * TMath::Sin( jets_[j].Theta() );
                //double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;
                double Width  = TMath::Sqrt( (param0resol*param0resol) + jets_[j].E()*(param1resol*param1resol) + jets_[j].E()*jets_[j].E()*(param2resol*param2resol) ) * TMath::Sin( jets_[j].Theta() );
                double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;

                if(j!=2)
                    AccPart *= (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
                else if( j==2 && TMath::Abs( jets_[j].Eta() )>2.5 )
                    AccPart *= 1.0;
                else if( j==2 && TMath::Abs( jets_[j].Eta() )<2.5 )
                    AccPart *= 1 - (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
                else {}
            }

        }
        else if( intType_ == SLAccNoHiggs) {

            double AccH1 = 1.0;
            double AccH2 = 1.0;
            for(unsigned int j = 2; j <8; j++) {

                if(j!=6 && j!=7 && TMath::Abs(jets_[j].Eta())>2.5) {
                    AccPart *= 0.0;
                    continue;
                }

                string flavor = "Light";
                if(j==2 || j>=5) flavor = "Heavy";

                string bin = "Bin0";
                if(  TMath::Abs( jets_[j].Eta() )<1.0 )
                    bin = "Bin0";
                else
                    bin = "Bin1";

                double param0resol = (jetParam_.find("param0resol"+flavor+bin))->second;
                double param1resol = (jetParam_.find("param1resol"+flavor+bin))->second;
                double param2resol = (jetParam_.find("param2resol"+flavor+bin))->second;
                double param0resp  = (jetParam_.find("param0resp" +flavor+bin))->second;
                double param1resp  = (jetParam_.find("param1resp" +flavor+bin))->second;

                //double Width  = jets_[j].E()*TMath::Sqrt( param0resol*param0resol/jets_[j].E() + param1resol*param1resol/jets_[j].E()/jets_[j].E()) * TMath::Sin( jets_[j].Theta() );
                //double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;
                double Width  = TMath::Sqrt( (param0resol*param0resol) + jets_[j].E()*(param1resol*param1resol) + jets_[j].E()*jets_[j].E()*(param2resol*param2resol) ) * TMath::Sin( jets_[j].Theta() );
                double Mean   = (jets_[j].E()*param0resp + param1resp) * TMath::Sin( jets_[j].Theta() ) ;

                if(j!=6 && j!=7)
                    AccPart *= (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
                else {
                    if(j==6)
                        AccH1 *= (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
                    else
                        AccH2 *= (1 - 0.5*(TMath::Erf( (30. - Mean)/Width ) + 1 ));
                }
            }

            if( TMath::Abs(jets_[6].Eta())>2.5 && TMath::Abs(jets_[7].Eta())>2.5 )
                AccPart *= 0.0;
            else if( TMath::Abs(jets_[6].Eta())<2.5 && TMath::Abs(jets_[7].Eta())>2.5 )
                AccPart *= AccH1;
            else if( TMath::Abs(jets_[6].Eta())>2.5 && TMath::Abs(jets_[7].Eta())<2.5 )
                AccPart *= AccH2;
            else
                AccPart *= ( AccH1*(1-AccH2) +  (1-AccH1)*AccH2 );
        }
    }

    prob *= AccPart;

    double PDFpart = ggPdf( x1, x2 , Q);

    //cout << "MEpart = " << MEpart << endl;
    //cout << "Jpart = " << Jpart << endl;
    //cout << "PDFpart = " << PDFpart << endl;

    /////////////////////
    // Approximate Empirical fit to tth pt spectrum [0]*x^([1])*exp([2]*x) for x > cutoff, then regularize to 0.
    //( SumPt>=12. ? TMath::Power(SumPt, -2.01013e-01)*TMath::Exp((-1.57856e-02)*SumPt) : 4.184e-02*SumPt );

    prob *= (tthPtFormula_!=0 ? tthPtFormula_->Eval(SumPt) : 1.0 );

    /////////////////////

    if(useME_)   prob *= MEpart;
    if(useJac_)  prob *= Jpart;
    if(usePDF_)  prob *= PDFpart;

    return prob;
}



unsigned int MEIntegratorNew::findMatch(double eta, double phi) const {

    unsigned int match = 99;
    int bin   = mash_->FindBin(eta, phi);
    float res = mash_->GetBinContent(bin);
    if( res>-0.5 && res<0.5 )
        match = 99; // no match
    else if(  res<-0.5 )
        match = 98; // veto
    else
        match = res;


    return match;
}




void MEIntegratorNew::debug() {

    cout << "*** debug start *** " << endl;

    for(std::map<string, double>::iterator it = jetParam_.begin(); it!=jetParam_.end(); it++) {
        cout << it->first << " => " << it->second << endl;
    }
    for(std::map<string, TH1F*>::iterator it = variables1D_.begin(); it!=variables1D_.end(); it++) {
        if(it->second)
            cout << it->first << " => " << (it->second)->Integral() << endl;
        else
            cout << it->first << " => null pointer" << endl;
    }
    for(std::map<string, TH2F*>::iterator it = variables2D_.begin(); it!=variables2D_.end(); it++) {
        if(it->second)
            cout << it->first << " => " << (it->second)->Integral() << endl;
        else
            cout << it->first << " => null pointer" << endl;
    }
    for(std::map<string, TH3F*>::iterator it = variables3D_.begin(); it!=variables3D_.end(); it++) {
        if(it->second)
            cout << it->first << " => " << (it->second)->Integral() << endl;
        else
            cout << it->first << " => null pointer" << endl;
    }


    cout << "*** debug end *** " << endl;

}


void MEIntegratorNew::printJetList() {
    cout << "******* START printJetList *******" << endl;
    cout << "lep   : jet0.SetPtEtaPhiM(" << jets_[0].Pt() << "," << jets_[0].Eta() << "," << jets_[0].Phi() << "," << jets_[0].M() << ")" << endl;
    cout << "met   : jet1.SetPtEtaPhiM(" << jets_[1].Pt() << "," << jets_[1].Eta() << "," << jets_[1].Phi() << "," << jets_[1].M() << ")" << endl;
    cout << "bLep  : jet2.SetPtEtaPhiM(" << jets_[2].Pt() << "," << jets_[2].Eta() << "," << jets_[2].Phi() << "," << jets_[2].M() << ")" << endl;
    cout << "w1    : jet3.SetPtEtaPhiM(" << jets_[3].Pt() << "," << jets_[3].Eta() << "," << jets_[3].Phi() << "," << jets_[3].M() << ")" << endl;
    cout << "w2    : jet4.SetPtEtaPhiM(" << jets_[4].Pt() << "," << jets_[4].Eta() << "," << jets_[4].Phi() << "," << jets_[4].M() << ")" << endl;
    cout << "bHad  : jet5.SetPtEtaPhiM(" << jets_[5].Pt() << "," << jets_[5].Eta() << "," << jets_[5].Phi() << "," << jets_[5].M() << ")" << endl;
    cout << "h1    : jet6.SetPtEtaPhiM(" << jets_[6].Pt() << "," << jets_[6].Eta() << "," << jets_[6].Phi() << "," << jets_[6].M() << ")" << endl;
    cout << "h2    : jet7.SetPtEtaPhiM(" << jets_[7].Pt() << "," << jets_[7].Eta() << "," << jets_[7].Phi() << "," << jets_[7].M() << ")" << endl;
    cout << "******* END printJetList *******" << endl;
}


#endif
