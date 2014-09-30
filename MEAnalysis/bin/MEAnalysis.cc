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
#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/GeometryVector/interface/VectorUtil.h"
#include "DataFormats/FWLite/interface/LuminosityBlock.h"
#include "DataFormats/FWLite/interface/Run.h"
#include "DataFormats/Luminosity/interface/LumiSummary.h"

#include "TTH/MEAnalysis/interface/Samples.h"
#include "TTH/MEAnalysis/interface/MEIntegratorNew.h"
#include "TTH/MEAnalysis/interface/MECombination.h"
#include "TTH/MEAnalysis/interface/HelperFunctions.h"

// dR distance for reco-gen matching
#define GENJETDR  0.3

// maximum number of VEGAS evaluation
#define MAX_REEVAL_TRIES 3

// 3.141...
#define PI TMath::Pi()

// maximum number of permutations per event
#define NMAXPERMUT 60

// maximum number of mass points for likelihood scan
#define NMAXMASS   20

// maximum number of four-vectors per event saved in output
#define NMAXJETS   10

// if one, MC jets are already corrected for JER
#define JERCORRECTED 1

// max number of jets for which the SLw1j hypothesis will be tested in type3 events
#define NMAXJETSSLW1JTYPE3 5

// max number of trial (if enhance MC stat)
#define NMAXEVENTRIALS 999999

// a global flag to select RECO or GEN+SMEAR analysis
//#define DOGENLEVELANALYSIS 0

// allow for different channels events
#define ENABLE_EM   1
#define ENABLE_EJ   1
#define ENABLE_MJ   1
#define ENABLE_EE   1
#define ENABLE_MM   1
#define ENABLE_JJ   0

using namespace std;

//version numbering scheme according to CMSSW version major and minor version.
//ME analysis major version - generally incompatible in data format to previous
//minor version - data-compatible
#define VERSION "70X v0.1"

int main(int argc, const char* argv[])
{

    /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
    /* @@@@@@@@@@@@@@@@@@@@@@@@ FWLITE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */

    cout << "MEAnalysis version " << VERSION << endl;
    gROOT->SetBatch(true);

    gSystem->Load("libFWCoreFWLite");
    gSystem->Load("libDataFormatsFWLite");

    AutoLibraryLoader::enable();

    /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
    /* @@@@@@@@@@@@@@@@@@@@@@@ CONFIGURATION @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */

    PythonProcessDesc builder(argv[1]);
    const edm::ParameterSet& in = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("fwliteInput");

    //commented out to avoid not-in-use errors
    // SAMPLES
    const edm::VParameterSet& samples = in.getParameter<edm::VParameterSet>("samples");
    const string outFileName    (in.getParameter<string>            ("outFileName"));
    const string pathToFile     (in.getParameter<string>         ("pathToFile"));
    const string ordering       ( in.getParameter<std::string>  ("ordering" ) );
    const string pathToTF       (in.getParameter<string>  ("pathToTF"));
    const string pathToCP       ( in.getParameter<std::string>  ("pathToCP") );
    const string pathToCP_smear ( in.getParameter<std::string>  ("pathToCP_smear") );
    const bool   verbose             (in.getParameter<bool>         ("verbose"));
    const bool   isMC                (in.getParameter<bool>         ("isMC"));

    // PARAMETERS
    const double lumi               (in.getUntrackedParameter<double>("lumi",   19.04));
    const float  MH                 (in.getUntrackedParameter<double>("MH",     125.));
    const float  MT                 (in.getUntrackedParameter<double>("MT",     174.3));
    const float  MW                 (in.getUntrackedParameter<double>("MW",     80.19));
    const float  MwL                ( in.getUntrackedParameter<double> ("MwL",       60));
    const float  MwH                ( in.getUntrackedParameter<double> ("MwH",      100));
    const float  MwLType3           ( in.getUntrackedParameter<double> ("MwLType3",  60));
    const float  MwHType3           ( in.getUntrackedParameter<double> ("MwHType3", 100));


    const float  btag_prob_cut_6jets( in.getUntrackedParameter<double> ("btag_prob_cut_6jets",    0.));
    const float  btag_prob_cut_5jets( in.getUntrackedParameter<double> ("btag_prob_cut_5jets",    0.));
    const float  btag_prob_cut_4jets( in.getUntrackedParameter<double> ("btag_prob_cut_4jets",    0.));
    const double maxChi2_           ( in.getUntrackedParameter<double> ("maxChi2", 2.5));
    const vector<double> massesH    ( in.getParameter<vector<double> > ("massesH"));
    const vector<double> massesT    ( in.getParameter<vector<double> > ("massesT"));
    const float  csv_WP_L           ( in.getUntrackedParameter<double> ("csv_WP_L",      0.244));
    const float  csv_WP_M           ( in.getUntrackedParameter<double> ("csv_WP_M",      0.679));
    const float  csv_WP_T           ( in.getUntrackedParameter<double> ("csv_WP_T",      0.898));

    const double lepPtLoose         ( in.getUntrackedParameter<double>  ("lepPtLoose", 20.));
    const double lepPtTight         ( in.getUntrackedParameter<double>  ("lepPtTight", 30.));
    const double lepIsoLoose        ( in.getUntrackedParameter<double>  ("lepIsoLoose", 0.2));
    const double lepIsoTight        ( in.getUntrackedParameter<double>  ("lepIsoTight", 0.12));
    const double elEta              ( in.getUntrackedParameter<double>  ("elEta",      2.5));
    const double muEtaLoose         ( in.getUntrackedParameter<double>  ("muEtaLoose", 2.4));
    const double muEtaTight         ( in.getUntrackedParameter<double>  ("muEtaTight", 2.1));

    const int    jetMultLoose       ( in.getUntrackedParameter<int>     ("jetMultLoose",    4 ));
    const double jetPtLoose         ( in.getUntrackedParameter<double>  ("jetPtLoose",     40.));
    const double jetPtThreshold     ( in.getUntrackedParameter<double>  ("jetPtThreshold", 30.));

    const vector<int> systematics   ( in.getParameter<vector<int> > ("systematics"));

    // FLAGS
    const int   switchoffOL      ( in.getUntrackedParameter<int>    ("switchoffOL",      0));
    const int   speedup          ( in.getUntrackedParameter<int>    ("speedup",          0));
    const int   doubleGaussianB  ( in.getUntrackedParameter<int>    ("doubleGaussianB",  1));
    const int   useBtag          ( in.getUntrackedParameter<int>    ("useBtag",          1));
    const int   useCMVA          ( in.getUntrackedParameter<int>    ("useCMVA",          0));
    const int   selectByBTagShape( in.getUntrackedParameter<int>    ("selectByBTagShape",0));
    const int   useCSVcalibration( in.getUntrackedParameter<int>    ("useCSVcalibration",0));
    const int   recoverTopBTagBin( in.getUntrackedParameter<int>    ("recoverTopBTagBin",0));
    const int   useRegression    ( in.getUntrackedParameter<int>    ("useRegression",    0));

    const int   triggerErrors      ( in.getUntrackedParameter<int>    ("triggerErrors",    0));

    const string pathTo_f_Vtype1_id  ( in.getParameter<std::string>     ("pathTo_f_Vtype1_id") );
    const string pathTo_f_Vtype1L1_tr( in.getParameter<std::string>     ("pathTo_f_Vtype1L1_tr") );
    const string pathTo_f_Vtype1L2_tr( in.getParameter<std::string>     ("pathTo_f_Vtype1L2_tr") );
    const string pathTo_f_Vtype2_id  ( in.getParameter<std::string>     ("pathTo_f_Vtype2_id") );
    const string pathTo_f_Vtype2_tr  ( in.getParameter<std::string>     ("pathTo_f_Vtype2_tr") );
    const string pathTo_f_Vtype3_id  ( in.getParameter<std::string>     ("pathTo_f_Vtype3_id") );
    const string pathTo_f_Vtype3_tr  ( in.getParameter<std::string>     ("pathTo_f_Vtype3_tr") );

    const int   testSLw1jType3    ( in.getUntrackedParameter<int>("testSLw1jType3",    0));
    int   nMaxJetsSLw1jType3( in.getUntrackedParameter<int>("nMaxJetsSLw1jType3",4));

    const int   doTypeBTag4      ( in.getUntrackedParameter<int>    ("doTypeBTag4", 0));
    const int   doTypeBTag5      ( in.getUntrackedParameter<int>    ("doTypeBTag5", 0));
    const int   doTypeBTag6      ( in.getUntrackedParameter<int>    ("doTypeBTag6", 0));
    const int   doType0          ( in.getUntrackedParameter<int>    ("doType0",     0));
    const int   doType1          ( in.getUntrackedParameter<int>    ("doType1",     0));
    const int   doType2          ( in.getUntrackedParameter<int>    ("doType2",     0));
    const int   doType3          ( in.getUntrackedParameter<int>    ("doType3",     0));
    const int   doType6          ( in.getUntrackedParameter<int>    ("doType6",     0));
    const int   doType7          ( in.getUntrackedParameter<int>    ("doType7",     0));
    const int   doType0ByBTagShape(in.getUntrackedParameter<int>    ("doType0ByBTagShape", 0));
    const int   doType1ByBTagShape(in.getUntrackedParameter<int>    ("doType1ByBTagShape", 0));
    const int   doType2ByBTagShape(in.getUntrackedParameter<int>    ("doType2ByBTagShape", 0));
    const int   doType3ByBTagShape(in.getUntrackedParameter<int>    ("doType3ByBTagShape", 0));
    const int   doType6ByBTagShape(in.getUntrackedParameter<int>    ("doType6ByBTagShape", 0));
    const int   useME            ( in.getUntrackedParameter<int>    ("useME",              1));
    const int   useJac           ( in.getUntrackedParameter<int>    ("useJac",             1));
    const int   useMET           ( in.getUntrackedParameter<int>    ("useMET",             1));
    const int   useTF            ( in.getUntrackedParameter<int>    ("useTF",              1));
    const int   usePDF           ( in.getUntrackedParameter<int>    ("usePDF",             1));
    const int   useAnalyticalFormula ( in.getUntrackedParameter<int>("useAnalyticalFormula",0));
    const int   useDynamicalScale    ( in.getUntrackedParameter<int>("useDynamicalScale",   0));
    const int   norm             ( in.getUntrackedParameter<int>    ("norm",               0));
    const int   hypo             ( in.getUntrackedParameter<int>    ("hypo",               0));
    const int   SoB              ( in.getUntrackedParameter<int>    ("SoB",                1));
    const int   integralOption0  ( in.getUntrackedParameter<int>    ("integralOption0",    1));
    const int   integralOption1  ( in.getUntrackedParameter<int>    ("integralOption1",    1));
    const int   integralOption2  ( in.getUntrackedParameter<int>    ("integralOption2",    0));
    const int   integralOption2_niter      ( in.getUntrackedParameter<int>     ("integralOption2_niter",     1));
    const int   integralOption2_stage      ( in.getUntrackedParameter<int>     ("integralOption2_stage",     1));
    const double integralOption2_nevalfact ( in.getUntrackedParameter<double>  ("integralOption2_nevalfact", 1.));

    const int   doJERbias        ( in.getUntrackedParameter<int>    ("doJERbias",  0));
    //FIXME: better to make these const?
    int   doCSVup          ( in.getUntrackedParameter<int>    ("doCSVup",    0));
    int   doCSVdown        ( in.getUntrackedParameter<int>    ("doCSVdown",  0));
    int   doJECup          ( in.getUntrackedParameter<int>    ("doJECup",    0));
    int   doJECdown        ( in.getUntrackedParameter<int>    ("doJECdown",  0));
    int   doJERup          ( in.getUntrackedParameter<int>    ("doJERup",    0));
    int   doJERdown        ( in.getUntrackedParameter<int>    ("doJERdown",  0));

    const int   fixNumEvJob      ( in.getUntrackedParameter<int>    ("fixNumEvJob",1));
    const vector<string> functions(in.getParameter<vector<string> > ("functions"));
    const vector<int>    evLimits (in.getParameter<vector<int> >    ("evLimits"));
    const int   ntuplizeAll      ( in.getUntrackedParameter<int>    ("ntuplizeAll",0));
    const int   reject_pixel_misalign_evts ( in.getUntrackedParameter<int> ("reject_pixel_misalign_evts", 1));

    const int doGenLevelAnalysis ( in.getUntrackedParameter<int>    ("doGenLevelAnalysis",  0));
    const int smearJets          ( in.getUntrackedParameter<int>    ("smearJets",  doGenLevelAnalysis));
    const int enhanceMC          ( in.getUntrackedParameter<int>    ("enhanceMC",   0));
    const int max_n_trials       ( in.getUntrackedParameter<int>    ("max_n_trials",1));

    const int   print            ( in.getUntrackedParameter<int>    ("printout", 0));
    const int   debug            ( in.getUntrackedParameter<int>    ("debug",    0));

    /////////////////////////////////////////////////////////////////////////////

    /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
    /* @@@@@@@@@@@@@@@@@@@@@@@@@ INITIALIZE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */

    // upper and lower event bounds to be processed
    int evLow  = evLimits[0];
    int evHigh = evLimits[1];

    // a random engine (needed for GEN+SMEAR analysis)
    TRandom3* ran = 0;

    // the transfer functions
    TF1* jet_smear = 0;

    // a clock to monitor the integration CPU time
    TStopwatch* clock = new TStopwatch();

    // a clock to monitor the total job
    TStopwatch* clock2 = new TStopwatch();
    clock2->Start();

    // file with b-tag pdf
    TFile* fCP = TFile::Open(pathToCP.c_str(),"READ");

    // file with jet energy pdf: gen-jet --> reco-jet (for smearing)
    TFile* fCP_smear = doGenLevelAnalysis ? TFile::Open(pathToCP_smear.c_str(),"READ") : 0;

    // name of csv in the input file ()
    TString csvName = "csv_rec";
    if( useCMVA ) csvName = "csv_mva_rec";

    // b-tag pdf for b-quark ('b'), c-quark ('c'), and light jets ('l')
    map<string,TH1F*> btagger;

    // a map between gen-jets and energy TF
    map<string, TF1*> transferfunctions;

    // use th CSV calibration from BDT analysis
    TString path = "./root/";
    TFile*  f_CSVwgt_HF = 0;
    TFile*  f_CSVwgt_LF = 0;
    TH1D* h_csv_wgt_hf[9][5];
    TH1D* c_csv_wgt_hf[5][5];
    TH1D* h_csv_wgt_lf[9][3][3];

    for( int iSys=0; iSys<9; iSys++ ) {

        for( int iPt=0; iPt<5; iPt++ )
            h_csv_wgt_hf[iSys][iPt] = 0;

        if( iSys<5 ) {
            for( int iPt=0; iPt<5; iPt++ )
                c_csv_wgt_hf[iSys][iPt] = 0;
        }

        for( int iPt=0; iPt<3; iPt++ ) {
            for( int iEta=0; iEta<3; iEta++ )
                h_csv_wgt_lf[iSys][iPt][iEta] = 0;
        }

    }

    if(useCSVcalibration)
        SetUpCSVreweighting(path,f_CSVwgt_HF, f_CSVwgt_LF,
                            h_csv_wgt_hf, c_csv_wgt_hf, h_csv_wgt_lf ) ;



    if( useBtag && fCP!=0 ) {

        // load the correct histogram
        btagger["b_Bin0"] = fCP->Get("csv_b_Bin0__"+csvName)!=0 ? (TH1F*)fCP->Get("csv_b_Bin0__"+csvName) : 0;
        btagger["b_Bin1"] = fCP->Get("csv_b_Bin1__"+csvName)!=0 ? (TH1F*)fCP->Get("csv_b_Bin1__"+csvName) : 0;
        btagger["c_Bin0"] = fCP->Get("csv_c_Bin0__"+csvName)!=0 ? (TH1F*)fCP->Get("csv_c_Bin0__"+csvName) : 0;
        btagger["c_Bin1"] = fCP->Get("csv_c_Bin1__"+csvName)!=0 ? (TH1F*)fCP->Get("csv_c_Bin1__"+csvName) : 0;
        btagger["l_Bin0"] = fCP->Get("csv_l_Bin0__"+csvName)!=0 ? (TH1F*)fCP->Get("csv_l_Bin0__"+csvName) : 0;
        btagger["l_Bin1"] = fCP->Get("csv_l_Bin1__"+csvName)!=0 ? (TH1F*)fCP->Get("csv_l_Bin1__"+csvName) : 0;

        // check that all histograms have been found
        int countFailures = 0;
        for(map<string,TH1F*>::iterator it_b = btagger.begin() ; it_b != btagger.end() ; it_b++) {
            if( it_b->second == 0) {
                cout << "Could not find " << it_b->first << endl;
                countFailures++;
            }
        }
        if( countFailures>0 )  return 0;
    }

    else if( useBtag && fCP==0 ) {
        cout << "Cound not find " << pathToCP << ": exit" << endl;
        return 0;
    }

    if( doGenLevelAnalysis && fCP!=0 && fCP_smear!=0) {

        // initialize the random engine
        ran = new TRandom3();
        ran->SetSeed( 65539 );

        // initialize the function that smears the jet energy (Double-Gaussian w/ 5 parameters)
        jet_smear = new TF1("jet_smear",
                            Form("[0]*exp(-0.5*((x-[1])**2)/[2]/[2]) + (1-[0])*exp(-0.5*((x-[3])**2)/[4]/[4])"),
                            0, 4000);



        // read the TH1 histograms that contain the parametrization of the DG parameters as a function of the parton energy
        TH1F* histo = 0;

        // for Heavy jets:
        histo = (TH1F*)fCP_smear->Get("respG1HeavyBin0") ;
        if(histo!=0) transferfunctions["b_G1_m_Bin0"] = histo->GetFunction("meanG1HeavyBin0")  != 0 ? histo->GetFunction("meanG1HeavyBin0")  : 0;
        histo = (TH1F*)fCP_smear->Get("resolG1HeavyBin0") ;
        if(histo!=0) transferfunctions["b_G1_s_Bin0"] = histo->GetFunction("sigmaG1HeavyBin0") != 0 ? histo->GetFunction("sigmaG1HeavyBin0") : 0;
        histo = (TH1F*)fCP_smear->Get("respG2HeavyBin0") ;
        if(histo!=0) transferfunctions["b_G2_m_Bin0"] = histo->GetFunction("meanG2HeavyBin0")  != 0 ? histo->GetFunction("meanG2HeavyBin0")  : 0;
        histo = (TH1F*)fCP_smear->Get("resolG2HeavyBin0") ;
        if(histo!=0) transferfunctions["b_G2_s_Bin0"] = histo->GetFunction("sigmaG2HeavyBin0") != 0 ? histo->GetFunction("sigmaG2HeavyBin0") : 0;
        histo = (TH1F*)fCP_smear->Get("respG1HeavyBin1") ;
        if(histo!=0) transferfunctions["b_G1_m_Bin1"] = histo->GetFunction("meanG1HeavyBin1")  != 0 ? histo->GetFunction("meanG1HeavyBin1")  : 0;
        histo = (TH1F*)fCP_smear->Get("resolG1HeavyBin1") ;
        if(histo!=0) transferfunctions["b_G1_s_Bin1"] = histo->GetFunction("sigmaG1HeavyBin1") != 0 ? histo->GetFunction("sigmaG1HeavyBin1") : 0;
        histo = (TH1F*)fCP_smear->Get("respG2HeavyBin1") ;
        if(histo!=0) transferfunctions["b_G2_m_Bin1"] = histo->GetFunction("meanG2HeavyBin1")  != 0 ? histo->GetFunction("meanG2HeavyBin1")  : 0;
        histo = (TH1F*)fCP_smear->Get("resolG2HeavyBin1") ;
        if(histo!=0) transferfunctions["b_G2_s_Bin1"] = histo->GetFunction("sigmaG2HeavyBin1") != 0 ? histo->GetFunction("sigmaG2HeavyBin1") : 0;

        // for Light jets:
        histo = (TH1F*)fCP_smear->Get("respLightBin0") ;
        if(histo!=0) transferfunctions["l_G1_m_Bin0"] = histo->GetFunction("meanLightBin0")   != 0 ? histo->GetFunction("meanLightBin0")  : 0;
        histo = (TH1F*)fCP_smear->Get("resolLightBin0") ;
        if(histo!=0) transferfunctions["l_G1_s_Bin0"] = histo->GetFunction("sigmaLightBin0")  != 0 ? histo->GetFunction("sigmaLightBin0") : 0;
        histo = (TH1F*)fCP_smear->Get("respLightBin1") ;
        if(histo!=0) transferfunctions["l_G1_m_Bin1"] = histo->GetFunction("meanLightBin1")   != 0 ? histo->GetFunction("meanLightBin1")  : 0;
        histo = (TH1F*)fCP_smear->Get("resolLightBin1") ;
        if(histo!=0) transferfunctions["l_G1_s_Bin1"] = histo->GetFunction("sigmaLightBin1")  != 0 ? histo->GetFunction("sigmaLightBin1") : 0;

        // check that all histograms have been found
        int countFailures = 0;
        for(map<string,TF1*>::iterator it_b = transferfunctions.begin() ; it_b != transferfunctions.end() ; it_b++) {
            if( it_b->second == 0) {
                cout << "Could not find " << it_b->first << endl;
                countFailures++;
            }
        }
        if( countFailures>0 )  return 0;

    }
    else if( doGenLevelAnalysis && (fCP==0 || fCP_smear==0) ) {
        cout << "Cound not find " << pathToCP << " or " << pathToCP_smear << ": exit" << endl;
        return 0;
    }


    // for trigger/ID errors
    TFile* f_Vtype1_id = 0;
    TFile* f_Vtype1L1_tr = 0;
    TFile* f_Vtype1L2_tr = 0;
    TFile* f_Vtype2_id = 0;
    TFile* f_Vtype2_tr = 0;
    TFile* f_Vtype3_id = 0;
    TFile* f_Vtype3_tr = 0;

    TTree* t_Vtype1_id = 0;
    TTree* t_Vtype1L1_tr = 0;
    TTree* t_Vtype1L2_tr = 0;
    TTree* t_Vtype2_id = 0;
    TTree* t_Vtype2_tr = 0;
    TTree* t_Vtype3_id = 0;
    TTree* t_Vtype3_tr = 0;

    if( triggerErrors ) {

        cout << "Reading trigger/ID/iso errors from root files..." << endl;
        f_Vtype1_id   = TFile::Open(pathTo_f_Vtype1_id.c_str(),  "READ");
        f_Vtype1L1_tr = TFile::Open(pathTo_f_Vtype1L1_tr.c_str(),"READ");
        f_Vtype1L2_tr = TFile::Open(pathTo_f_Vtype1L2_tr.c_str(),"READ");
        f_Vtype2_id   = TFile::Open(pathTo_f_Vtype2_id.c_str(),  "READ");
        f_Vtype2_tr   = TFile::Open(pathTo_f_Vtype2_tr.c_str(),  "READ");
        f_Vtype3_id   = TFile::Open(pathTo_f_Vtype3_id.c_str(),  "READ");
        f_Vtype3_tr   = TFile::Open(pathTo_f_Vtype3_tr.c_str(),  "READ");

        t_Vtype1_id   = (TTree*)f_Vtype1_id->Get("tree");
        t_Vtype1L1_tr = (TTree*)f_Vtype1L1_tr->Get("tree");
        t_Vtype1L2_tr = (TTree*)f_Vtype1L2_tr->Get("tree");
        t_Vtype2_id   = (TTree*)f_Vtype2_id->Get("tree");
        t_Vtype2_tr   = (TTree*)f_Vtype2_tr->Get("tree");
        t_Vtype3_id   = (TTree*)f_Vtype3_id->Get("tree");
        t_Vtype3_tr   = (TTree*)f_Vtype3_tr->Get("tree");

    }



    // Higgs mass values for scan
    const int nHiggsMassPoints  = massesH.size();
    double mH[nHiggsMassPoints];
    for( unsigned int m = 0; m < massesH.size() ; m++)
        mH[m] = massesH[m];

    // Top mass values for scan
    const int nTopMassPoints  = massesT.size();
    double mT[nTopMassPoints];
    for( unsigned int m = 0; m < massesT.size() ; m++)
        mT[m] = massesT[m];


    // not supported...
    if( nHiggsMassPoints>1 && nTopMassPoints>1) {
        cout << "Cannot handle two mass scans at the same time... return." << endl;
        return 1;
    }
    if( nHiggsMassPoints>NMAXMASS || nTopMassPoints>NMAXMASS) {
        cout << "Too many mass points required... return" << endl;
        return 1;
    }


    // configure MEIntegrator
    MEIntegratorNew* meIntegrator = new MEIntegratorNew( pathToTF , 4 , int(verbose));
    if( norm == 0)
        meIntegrator->setWeightNorm( MEIntegratorNew::None );
    else if( norm==1 )
        meIntegrator->setWeightNorm( MEIntegratorNew::xSec );
    else if( norm==2 )
        meIntegrator->setWeightNorm( MEIntegratorNew::Acc );
    else {
        cout << "Unsupported normalization... exit" << endl;
        delete meIntegrator;
        return 0;
    }

    // set normalization formulas ( not used if norm==0 )
    meIntegrator->setNormFormulas( TString(functions[0].c_str()),
                                   TString(functions[1].c_str()),
                                   TString(functions[2].c_str()),
                                   TString(functions[3].c_str()),
                                   TString(functions[4].c_str()),
                                   TString(functions[5].c_str())
                                 );

    // initialize top and W mass
    meIntegrator->setTopMass( MT , MW );

    // configure ME calculation
    meIntegrator->setUseME (useME);
    meIntegrator->setUseJac(useJac);
    meIntegrator->setUseMET(useMET);
    meIntegrator->setUseTF (useTF);
    meIntegrator->setUsePDF(usePDF);
    meIntegrator->setUseAnalyticalFormula(useAnalyticalFormula);
    meIntegrator->setUseDynamicalScale   (useDynamicalScale);

    // use double-gaussian for b quark energy TF
    meIntegrator->setUseRefinedTF(doubleGaussianB);

    // use nominal TF from ROOT file
    meIntegrator->initTFparameters(1.0,1.0,1.0,1.0, 1.0);
    if(switchoffOL) {
        meIntegrator->switchOffOL();
        cout << "*** Switching off OpenLoops to speed-up the calculation ***" << endl;
    }


    Float_t readerVars[12];
    if( useRegression ) {
        cout << "The b-energy regression will be used..." << endl;
    }
    TMVA::Reader* reader =  useRegression ? getTMVAReader("./root/weights/", "target-pt_gen", "BDTG", readerVars) : 0;

    /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
    /* @@@@@@@@@@@@@@@@@@@@@@@ OUTPUT @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */


    // clean output file (if any)
    gSystem->Exec(("rm "+outFileName).c_str());

    // output file
    TFile* fout_tmp = TFile::Open(outFileName.c_str(),"UPDATE");

    // total event counter for normalization
    TH1F*  hcounter = new TH1F("hcounter","",2,0,2);

    // save a snapshot of the configuration parameters
    vector<std::string> paramsAll = in.getParameterNames();
    cout <<  "Tot. number of configuration parameters: " << paramsAll.size() << endl;
    vector<std::string> params;
    for( unsigned int pin = 0; pin < paramsAll.size() ; pin++ ) {
        if( in.existsAs<int>        ( paramsAll[pin], false ) )
            params.push_back( paramsAll[pin] );
        else if( in.existsAs<double>( paramsAll[pin], false ) )
            params.push_back( paramsAll[pin] );
    }
    int n_untr_param = (int)params.size();
    cout << "(of which " << n_untr_param << " are untracked int/double)" << endl;

    TH1F*  hparam   = new TH1F("hparam",  "", n_untr_param+9 ,0,n_untr_param+9);
    for( int pin = 0; pin < n_untr_param ; pin++ ) {
        hparam->GetXaxis()->SetBinLabel  ( pin+1, params[pin].c_str() );
        if(in.existsAs<double>( params[pin], false ) )
            hparam->SetBinContent( pin+1, in.getUntrackedParameter<double>( params[pin], -99. ) );
        else if(in.existsAs<int>( params[pin], false ) )
            hparam->SetBinContent( pin+1, in.getUntrackedParameter<int>   ( params[pin], -99  ) );
        else {}
    }
    hparam->SetBinContent            ( n_untr_param+1,  (in.getParameter<vector<int> >("evLimits"))[0]   );
    hparam->GetXaxis()->SetBinLabel  ( n_untr_param+1,  "evLow" );
    hparam->SetBinContent            ( n_untr_param+2,  (in.getParameter<vector<int> >("evLimits"))[1]   );
    hparam->GetXaxis()->SetBinLabel  ( n_untr_param+2,  "evHigh" );
    hparam->GetXaxis()->SetBinLabel  ( n_untr_param+3,  (in.getParameter<string>("outFileName")).c_str() );
    hparam->GetXaxis()->SetBinLabel  ( n_untr_param+4,  (in.getParameter<string>("pathToTF")).c_str() );
    hparam->GetXaxis()->SetBinLabel  ( n_untr_param+5,  (in.getParameter<string>("pathToCP")).c_str() );
    hparam->GetXaxis()->SetBinLabel  ( n_untr_param+6,  (in.getParameter<string>("pathToCP_smear")).c_str() );
    hparam->GetXaxis()->SetBinLabel  ( n_untr_param+7,  (in.getParameter<string>("pathToFile")).c_str() );
    hparam->GetXaxis()->SetBinLabel  ( n_untr_param+8,  (in.getParameter<string>("ordering")).c_str() );

    for( int sam = 0 ; sam < (int)samples.size(); sam++) {
        if( !(samples[sam].getParameter<bool>("skip")) ) {
            hparam->SetBinContent( n_untr_param+9, samples[sam].getParameter<double>("xSec") );
            hparam->GetXaxis()->SetBinLabel  ( n_untr_param+9, (samples[sam].getParameter<string>("nickName") ).c_str());
        }
    }

    // number of events that will be processed
    int events_     = 0;

    // output tree
    TTree* tree  = new TTree("tree","");

    // counts how many events have been analyzed (to have fixed-size jobs)
    int counter_;
    // number of jet-quark permutations (for signal and bkg hypotheses)
    int nPermut_, nPermut_alt_;
    // number of (Higgs/Top) mass points
    int nMassPoints_;
    // total number integration per event (nPermut*nMassPoints)
    int nTotInteg_,nTotInteg_alt_;

    // number of matches to higgs quarks among tagged jets
    int matchesH_;
    // number of matches to W quarks among un-tagged jets
    int matchesW_;
    // number of matches to top quarks among tagged jets
    int matchesT_;
    // number of matches to higgs quarks among all jets
    int matchesHAll_;
    // number of matches to W quarks among all jets
    int matchesWAll_;
    // number of matches to top quarks among all jets
    int matchesTAll_;
    // count how many quarks from W decay overlap by dR<0.5
    int overlapLight_;
    // count how many b-quarks overlap by dR<0.5
    int overlapHeavy_;

    // integration type
    int type_;

    // sytematics
    int syst_;

    // number of systematic loops per event
    int iterations_;

    // num. of b-hadrons and c-quarks
    int nSimBs_; //, nC_, nCTop_;

    // num of b-hadrons inside jets (backward compatibility)
    int nMatchSimBsOld_;
    // num of b-hadrons inside jets
    // gen_eta < 5, gen_pt > 20
    int nMatchSimBs_v1_;
    // gen_eta <2.5, gen_pt > 20
    int nMatchSimBs_v2_;
    // gen_eta < 2.5, gen_pt > 20, reco_pt > 30
    int nMatchSimBs_;
    // num of c-hadrons inside jets
    int nMatchSimCs_v1_;
    int nMatchSimCs_v2_;
    int nMatchSimCs_;

    // gen top/higgs informations
    float p4H_   [4];
    float p4T_   [4];
    float p4Tbar_[4];

    // a structure with tth gen system infos
    tthInfo ttH_;

    // type-dependent flags
    int flag_type0_;
    int flag_type1_;
    int flag_type2_;
    int flag_type3_;
    int flag_type4_;
    int flag_type6_;

    // event-wise **ME** probability (summed over permutations)
    // ...for ttH...
    float probAtSgn_ ;

    // ...for ttbb...
    float probAtSgn_alt_ ;

    // event-wise **ME X btag** probability (summed over permutations)
    // ...for ttH...
    float probAtSgn_ttbb_;
    // ...for tt(bb,jj,bj,cc)...
    float probAtSgn_alt_ttbb_;
    float probAtSgn_alt_ttjj_;
    float probAtSgn_alt_ttbj_;
    float probAtSgn_alt_ttcc_;

    // per-permutation and mass value **ME** probability
    float probAtSgn_permut_       [NMAXPERMUT*NMAXMASS];
    float probAtSgn_alt_permut_   [NMAXPERMUT*NMAXMASS];
    float probAtSgnErr_permut_    [NMAXPERMUT*NMAXMASS];
    float probAtSgnErr_alt_permut_[NMAXPERMUT*NMAXMASS];
    int   callsAtSgn_permut_      [NMAXPERMUT*NMAXMASS];
    int   callsAtSgn_alt_permut_  [NMAXPERMUT*NMAXMASS];
    float chi2AtSgn_permut_       [NMAXPERMUT*NMAXMASS];
    float chi2AtSgn_alt_permut_   [NMAXPERMUT*NMAXMASS];

    // per-permutation **btag** probability
    float probAtSgn_bb_permut_[NMAXPERMUT];
    float probAtSgn_bj_permut_[NMAXPERMUT];
    float probAtSgn_cc_permut_[NMAXPERMUT];
    float probAtSgn_jj_permut_[NMAXPERMUT];

    // masses to be scanned
    float mH_scan_[NMAXMASS];
    float mT_scan_[NMAXMASS];

    // a flag for the event type
    int Vtype_;
    // event-dependent weight (for normalization)
    float weight_;

    // event-dependent CSV weight (for normalization)
    float weightCSV_[19];

    // for theory systematics (tt+jets only)
    float SCALEsyst_[3];

    // additional gen top PT scale factor
    float weightTopPt_;
    // cpu time
    float time_;
    // event information
    EventInfo EVENT_;
    // num of PVs
    int nPVs_;
    // pu reweighting
    float PUweight_, PUweightP_, PUweightM_;
    // trigger turn-on
    float trigger_;
    float triggerErr_;
    // trigger bits (data)
    bool triggerFlags_[70];
    // number of gen jets
    float lheNj_;

    // number of b's, c's, l's, and gluons in the multi-leg ME
    int n_b_, n_c_, n_l_, n_g_;

    // lepton kinematic (at most two leptons)
    int   nLep_;
    float lepton_pt_    [2];
    float lepton_eta_   [2];
    float lepton_phi_   [2];
    float lepton_m_     [2];
    float lepton_charge_[2];
    float lepton_rIso_  [2];
    int   lepton_type_  [2];
    float lepton_dxy_   [2];
    float lepton_dz_    [2];
    float lepton_wp80_  [2];
    float lepton_wp95_  [2];
    float lepton_wp70_  [2];
    float lepton_MVAtrig_ [2];

    float Mll_, MTln_;

    // additional SF for electrons;
    float sf_ele_;

    // met kinematic
    float MET_pt_;
    float MET_phi_;
    float MET_sumEt_;

    // invisible particles kinematic
    float Nus_pt_;
    float Nus_phi_;

    // control variables
    float mH_matched_;
    float mTop_matched_;
    float mW_matched_;

    // jet kinematics (as passed via **jets** collection)
    int nJet_;
    float jet_pt_    [NMAXJETS];
    float jet_pt_alt_[NMAXJETS];
    float jet_eta_   [NMAXJETS];
    float jet_phi_   [NMAXJETS];
    float jet_m_     [NMAXJETS];
    float jet_csv_   [NMAXJETS];

    // number of selected hJets
    int hJetAmong_;
    int jetsAboveCut_;

    // number of trials
    int num_of_trials_;

    // number of selected jets passing CSV L,M,T
    int numBTagL_, numBTagM_, numBTagT_;
    // nummber of selected jets
    int numJets_;
    // btag likelihood ratio
    float btag_LR_;

    // permutation -> jets association
    int   perm_to_jet_    [NMAXPERMUT];
    int   perm_to_jet_alt_[NMAXPERMUT];
    // permutation -> gen association
    int   perm_to_gen_     [NMAXPERMUT];
    int   perm_to_gen_alt_ [NMAXPERMUT];

    tree->Branch("counter",      &counter_,       "counter/I");
    tree->Branch("nPermut_s",    &nPermut_,       "nPermut_s/I");
    tree->Branch("nPermut_b",    &nPermut_alt_,   "nPermut_b/I");
    tree->Branch("nMassPoints",  &nMassPoints_,   "nMassPoints/I");
    tree->Branch("nTotInteg_s",  &nTotInteg_,     "nTotInteg_s/I");
    tree->Branch("nTotInteg_b",  &nTotInteg_alt_, "nTotInteg_b/I");
    tree->Branch("matchesH",     &matchesH_,      "matchesH/I");
    tree->Branch("matchesW",     &matchesW_,      "matchesW/I");
    tree->Branch("matchesT",     &matchesT_,      "matchesT/I");
    tree->Branch("matchesHAll",  &matchesHAll_,   "matchesHAll/I");
    tree->Branch("matchesWAll",  &matchesWAll_,   "matchesWAll/I");
    tree->Branch("matchesTAll",  &matchesTAll_,   "matchesTAll/I");
    tree->Branch("overlapLight", &overlapLight_,  "overlapLight/I");
    tree->Branch("overlapHeavy", &overlapHeavy_,  "overlapHeavy/I");
    tree->Branch("type",         &type_,          "type/I");
    tree->Branch("syst",         &syst_,          "syst/I");
    tree->Branch("iterations",   &iterations_,    "iterations/I");

    tree->Branch("nSimBs",       &nSimBs_,        "nSimBs/I");
    tree->Branch("nMatchSimBsOld",&nMatchSimBsOld_,"nMatchSimBsOld/I");
    tree->Branch("nMatchSimBs_v1",&nMatchSimBs_v1_,"nMatchSimBs_v1/I");
    tree->Branch("nMatchSimBs_v2",&nMatchSimBs_v2_,"nMatchSimBs_v2/I");
    tree->Branch("nMatchSimBs",  &nMatchSimBs_,    "nMatchSimBs/I");
    tree->Branch("nMatchSimCs_v1",  &nMatchSimCs_v1_,    "nMatchSimCs_v1/I");
    tree->Branch("nMatchSimCs_v2",  &nMatchSimCs_v2_,    "nMatchSimCs_v2/I");
    tree->Branch("nMatchSimCs",  &nMatchSimCs_,    "nMatchSimCs/I");

    tree->Branch("weight",       &weight_,        "weight/F");
    tree->Branch("weightCSV",    weightCSV_,      "weightCSV[19]/F");
    tree->Branch("SCALEsyst",    SCALEsyst_,      "SCALEsyst[3]/F");

    tree->Branch("weightTopPt",  &weightTopPt_,   "weightTopPt/F");
    tree->Branch("time",         &time_,          "time/F");
    tree->Branch("flag_type0",   &flag_type0_,    "flag_type0/I");
    tree->Branch("flag_type1",   &flag_type1_,    "flag_type1/I");
    tree->Branch("flag_type2",   &flag_type2_,    "flag_type2/I");
    tree->Branch("flag_type3",   &flag_type3_,    "flag_type3/I");
    tree->Branch("flag_type4",   &flag_type4_,    "flag_type4/I");
    tree->Branch("flag_type6",   &flag_type6_,    "flag_type6/I");
    tree->Branch("Vtype",        &Vtype_,         "type/I");
    tree->Branch("EVENT",        &EVENT_,         "run/I:lumi/I:event/I:json/I");
    tree->Branch("nPVs",         &nPVs_,          "nPVs/I");
    tree->Branch("PUweight",     &PUweight_,      "PUweight/F");
    tree->Branch("PUweightP",    &PUweightP_,     "PUweightP/F");
    tree->Branch("PUweightM",    &PUweightM_,     "PUweightM/F");
    tree->Branch("lheNj",        &lheNj_,         "lheNj/F");
    tree->Branch("n_b",          &n_b_,           "n_b/I");
    tree->Branch("n_c",          &n_c_,           "n_c/I");
    tree->Branch("n_l",          &n_l_,           "n_l/I");
    tree->Branch("n_g",          &n_g_,           "n_g/I");
    tree->Branch("trigger",      &trigger_,       "trigger/F");
    tree->Branch("triggerErr",   &triggerErr_,    "triggerErr/F");
    tree->Branch("triggerFlags", triggerFlags_,   "triggerFlags[70]/b");
    tree->Branch("p4H",          p4H_,            "p4H[4]/F");
    tree->Branch("p4T",          p4T_,            "p4T[4]/F");
    tree->Branch("p4Tbar",       p4Tbar_,         "p4Tbar[4]/F");
    tree->Branch("ttH",          &ttH_,           "x1/F:x2/F:pdf/F:pt/F:eta/F:phi/F:m/F:me2_ttH/F:me2_ttbb/F");

    // marginalized over permutations (all <=> Sum_{p=0}^{nTotPermut}( mH=MH, mT=MT ) )
    tree->Branch(Form("p_%d_all_s",     int(MH)),   &probAtSgn_,           Form("p_%d_all_s/F",              int(MH)) );
    tree->Branch(Form("p_%d_all_b",     int(MH)),   &probAtSgn_alt_,       Form("p_%d_all_b/F",              int(MH)) );
    tree->Branch(Form("p_%d_all_s_ttbb",int(MH)),   &probAtSgn_ttbb_,      Form("p_%d_all_s_ttbb/F",         int(MH)) );
    tree->Branch(Form("p_%d_all_b_ttbb",int(MH)),   &probAtSgn_alt_ttbb_,  Form("p_%d_all_b_ttbb/F",         int(MH)) );
    tree->Branch(Form("p_%d_all_b_ttjj",int(MH)),   &probAtSgn_alt_ttjj_,  Form("p_%d_all_b_ttjj/F",         int(MH)) );
    tree->Branch(Form("p_%d_all_b_ttbj",int(MH)),   &probAtSgn_alt_ttbj_,  Form("p_%d_all_b_ttbj/F",         int(MH)) );
    tree->Branch(Form("p_%d_all_b_ttcc",int(MH)),   &probAtSgn_alt_ttcc_,  Form("p_%d_all_b_ttcc/F",         int(MH)) );

    // differential in permutations and mass value. E.g.:
    //  p_vsMH_s[0],          ..., p_vsMH_s[  nPermut-1] => prob. per-permutation and for mH = masses[0]
    //  p_vsMH_s[nPermut], ...,    p_vsMH_s[2*nPermut-1] => prob. per-permutation and for mH = masses[1]
    //  ....
    tree->Branch("p_vsMH_s",     probAtSgn_permut_,       "p_vsMH_s[nTotInteg_s]/F" );
    tree->Branch("p_vsMT_b",     probAtSgn_alt_permut_,   "p_vsMT_b[nTotInteg_b]/F");
    tree->Branch("p_vsMH_Err_s", probAtSgnErr_permut_,    "p_vsMH_Err_s[nTotInteg_s]/F" );
    tree->Branch("p_msMT_Err_b", probAtSgnErr_alt_permut_,"p_vsMT_Err_b[nTotInteg_b]/F" );
    tree->Branch("n_vsMH_s",     callsAtSgn_permut_,      "n_vsMH_s[nTotInteg_s]/I" );
    tree->Branch("n_vsMT_b",     callsAtSgn_alt_permut_,  "n_vsMT_b[nTotInteg_b]/I");
    tree->Branch("x_vsMH_s",     chi2AtSgn_permut_,       "x_vsMH_s[nTotInteg_s]/F" );
    tree->Branch("x_vsMT_b",     chi2AtSgn_alt_permut_,   "x_vsMT_b[nTotInteg_b]/F");

    // differential in permutation
    tree->Branch("p_tt_bb",      probAtSgn_bb_permut_,    "p_tt_bb[nPermut_s]/F");
    tree->Branch("p_tt_bj",      probAtSgn_bj_permut_,    "p_tt_bj[nPermut_b]/F");
    tree->Branch("p_tt_cc",      probAtSgn_cc_permut_,    "p_tt_cc[nPermut_b]/F");
    tree->Branch("p_tt_jj",      probAtSgn_jj_permut_,    "p_tt_jj[nPermut_b]/F");

    // # of mass points scanned
    tree->Branch("mH_scan",       mH_scan_,          "mH_scan[nMassPoints]/F");
    tree->Branch("mT_scan",       mT_scan_,          "mT_scan[nMassPoints]/F");

    // lepton kinematics
    tree->Branch("nLep",                    &nLep_,        "nLep/I");
    tree->Branch("lepton_pt",               lepton_pt_,    "lepton_pt[nLep]/F");
    tree->Branch("lepton_eta",              lepton_eta_,   "lepton_eta[nLep]/F");
    tree->Branch("lepton_phi",              lepton_phi_,   "lepton_phi[nLep]/F");
    tree->Branch("lepton_m",                lepton_m_,     "lepton_m[nLep]/F");
    tree->Branch("lepton_charge",           lepton_charge_,"lepton_charge[nLep]/F");
    tree->Branch("lepton_rIso",             lepton_rIso_,  "lepton_rIso[nLep]/F");
    tree->Branch("lepton_type",             lepton_type_,  "lepton_type[nLep]/I");
    tree->Branch("lepton_dxy",              lepton_dxy_,   "lepton_dxy[nLep]/F");
    tree->Branch("lepton_dz",               lepton_dz_,    "lepton_dz[nLep]/F");
    tree->Branch("lepton_wp80",             lepton_wp80_,  "lepton_wp80[nLep]/F");
    tree->Branch("lepton_wp95",             lepton_wp95_,  "lepton_wp95[nLep]/F");
    tree->Branch("lepton_wp70",             lepton_wp70_,  "lepton_wp70[nLep]/F");
    tree->Branch("lepton_MVAtrig",          lepton_MVAtrig_, "lepton_MVAtrig[nLep]/F");

    tree->Branch("Mll",                     &Mll_,         "Mll/F");
    tree->Branch("MTln",                    &MTln_,        "MTln/F");

    // additional electron SF
    tree->Branch("weightEle",               &sf_ele_,      "weightEle/F");

    // MET kinematics
    tree->Branch("MET_pt",                  &MET_pt_,    "MET_pt/F");
    tree->Branch("MET_phi",                 &MET_phi_,   "MET_phi/F");
    tree->Branch("MET_sumEt",               &MET_sumEt_, "MET_sumEt/F");

    // Invisible particles kinematics
    tree->Branch("Nus_pt",                  &Nus_pt_,    "Nus_pt/F");
    tree->Branch("Nus_phi",                 &Nus_phi_,   "Nus_phi/F");

    // jet kinematics
    tree->Branch("nJet",                    &nJet_,        "nJet/I");
    tree->Branch("jet_pt",                  jet_pt_,       "jet_pt[nJet]/F");
    tree->Branch("jet_pt_alt",              jet_pt_alt_,   "jet_pt_alt[nJet]/F");
    tree->Branch("jet_eta",                 jet_eta_,      "jet_eta[nJet]/F");
    tree->Branch("jet_phi",                 jet_phi_,      "jet_phi[nJet]/F");
    tree->Branch("jet_m",                   jet_m_,        "jet_m[nJet]/F");
    tree->Branch("jet_csv",                 jet_csv_,      "jet_csv[nJet]/F");
    tree->Branch("hJetAmong",               &hJetAmong_,   "hJetAmong/I");
    tree->Branch("jetsAboveCut",            &jetsAboveCut_,"jetsAboveCut/I");
    tree->Branch("num_of_trials",           &num_of_trials_,"num_of_trials/I");


    // Jet multiplicity
    tree->Branch("numBTagL",                &numBTagL_,    "numBTagL/I");
    tree->Branch("numBTagM",                &numBTagM_,    "numBTagM/I");
    tree->Branch("numBTagT",                &numBTagT_,    "numBTagT/I");
    tree->Branch("numJets",                 &numJets_,     "numJets/I");
    tree->Branch("btag_LR",                 &btag_LR_,     "btag_LR/F");

    // Control variables
    tree->Branch("mH_matched",              &mH_matched_,   "mH_matched/F");
    tree->Branch("mTop_matched",            &mTop_matched_, "mTop_matched/F");
    tree->Branch("mW_matched",              &mW_matched_,   "mW_matched/F");

    // a map that associates to each permutation [p=0...nTotPermut] to the corresponding jet,
    // indexed according to the order in the jet_* collection
    //  E.g.: perm_to_jets[0] = 234567 <==> the first permutation (element '0' of p_vsMH_s/p_vsMT_b )
    //        associates element '2' of jets_* to the bLep, element '3' to W1Had, '4' to 'W2Had', '5' to bHad, and '6','7'
    //        to non-top radiation
    tree->Branch("perm_to_jet_s",             perm_to_jet_,    "perm_to_jet[nPermut_s]/I");
    tree->Branch("perm_to_gen_s" ,            perm_to_gen_,    "perm_to_gen[nPermut_s]/I");
    tree->Branch("perm_to_jet_b",             perm_to_jet_alt_,"perm_to_jet[nPermut_b]/I");
    tree->Branch("perm_to_gen_b" ,            perm_to_gen_alt_,"perm_to_gen[nPermut_b]/I");


    //tree->Branch("",                        _,  "[]/F");

    /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
    /* @@@@@@@@@@@@@@@@@@@@@@@@@ OPEN FILES @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */


    // read input files
    bool openAllFiles  = false;
    Samples* mySamples = new Samples(openAllFiles, pathToFile, ordering, samples, lumi, verbose);
    vector<string> mySampleFiles;

    if(mySamples->IsOk()) {

        cout << "Ok!" << endl;
        mySampleFiles = mySamples->Files();

        for( unsigned int i = 0 ; i < mySampleFiles.size(); i++) {
            string sampleName       = mySampleFiles[i];

            if(verbose) {
                cout << mySampleFiles[i] << " ==> " << mySamples->GetXSec(sampleName)
                     << " pb,"
                     << " ==> weight = "            << mySamples->GetWeight(sampleName) << endl;
            }
        }
    }
    else {
        cout << "Problems... leaving" << endl;

        fout_tmp->Close();
        cout << "Delete meIntegrator..." << endl;
        delete meIntegrator;
        delete clock;
        delete clock2;
        if(ran!=0)       delete ran;
        if(jet_smear!=0) delete jet_smear;
        cout << "Finished!!!" << endl;
        cout << "*******************" << endl;

        return 0;
    }


    // open first sample for b-energy regression => get pointer to the tree
    string currentName0     = mySampleFiles[0];
    mySamples->OpenFile( currentName0 );
    TTree* currentTree_reg  = mySamples->GetTree( currentName0, "tree");

    // loop over input files
    for(unsigned int sample = 0 ; sample < mySampleFiles.size(); sample++) {

        string currentName       = mySampleFiles[sample];

        //if(currentName.find("Run2012")!=string::npos) isMC = false;

        mySamples->OpenFile( currentName );
        cout << "Opening file " << currentName << endl;
        TTree* currentTree       = mySamples->GetTree  (currentName, "tree");
        float scaleFactor        = mySamples->GetWeight(currentName);
        TH1F* count_Q2           = mySamples->GetHisto (currentName, "Count_Q2");
        float normDown           = count_Q2 ? count_Q2->GetBinContent(1)/count_Q2->GetBinContent(2) : 1.0;
        float normUp             = count_Q2 ? count_Q2->GetBinContent(3)/count_Q2->GetBinContent(2) : 1.0;
        cout << "Done!!" << endl;

        // variables to be used from the input files
        genParticleInfo genB, genBbar;
        genTopInfo      genTop, genTbar;
        metInfo         METtype1p2corr;
        EventInfo       EVENT;
        int             nvlep, nalep, nSimBs, nhJets, naJets, nPVs, Vtype;
        float           PUweight, PUweightP, PUweightM;
        float           lheNj;
        float           weightTrig2012;
        UChar_t         triggerFlags[70];
        float           SCALEsyst[12];

        Int_t   vLepton_type      [2];
        Float_t vLepton_mass      [2];
        Float_t vLepton_pt        [2];
        Float_t vLepton_eta       [2];
        Float_t vLepton_phi       [2];
        Float_t vLepton_genPt     [2];
        Float_t vLepton_genEta    [2];
        Float_t vLepton_genPhi    [2];
        Float_t vLepton_charge    [2];
        Float_t vLepton_pfCorrIso [2];
        Float_t vLepton_wp80      [2];
        Float_t vLepton_wp95      [2];
        Float_t vLepton_wp70      [2];
        Float_t vLepton_idMVAtrig [2];

        Float_t vLepton_dxy       [2];
        Float_t vLepton_dz        [2];
        //Float_t vLepton_id2012tight[2];

        Int_t   aLepton_type      [999];
        Float_t aLepton_mass      [999];
        Float_t aLepton_pt        [999];
        Float_t aLepton_eta       [999];
        Float_t aLepton_phi       [999];
        Float_t aLepton_genPt     [999];
        Float_t aLepton_genEta    [999];
        Float_t aLepton_genPhi    [999];
        Float_t aLepton_charge    [999];
        Float_t aLepton_pfCorrIso [999];
        Float_t aLepton_wp80      [999];
        Float_t aLepton_wp95      [999];
        Float_t aLepton_dxy       [999];
        Float_t aLepton_dz        [999];
        //Float_t aLepton_id2012tight[999];

        Float_t hJet_pt           [999];
        Float_t hJet_eta          [999];
        Float_t hJet_phi          [999];
        Float_t hJet_e            [999];
        Float_t hJet_flavour      [999];
        Float_t hJet_puJetIdL     [999];
        UChar_t hJet_id           [999];
        Float_t hJet_csv          [999];
        Float_t hJet_cmva         [999];
        Float_t hJet_csv_nominal  [999];
        Float_t hJet_csv_upBC     [999];
        Float_t hJet_csv_downBC   [999];
        Float_t hJet_csv_upL      [999];
        Float_t hJet_csv_downL    [999];
        Float_t hJet_JECUnc       [999];
        Float_t hJet_genPt        [999];
        Float_t hJet_genEta       [999];
        Float_t hJet_genPhi       [999];
        Float_t aJet_pt           [999];
        Float_t aJet_eta          [999];
        Float_t aJet_phi          [999];
        Float_t aJet_e            [999];
        Float_t aJet_flavour      [999];
        Float_t aJet_puJetIdL     [999];
        UChar_t aJet_id           [999];
        Float_t aJet_csv          [999];
        Float_t aJet_cmva         [999];
        Float_t aJet_csv_nominal  [999];
        Float_t aJet_csv_upBC     [999];
        Float_t aJet_csv_downBC   [999];
        Float_t aJet_csv_upL      [999];
        Float_t aJet_csv_downL    [999];
        Float_t aJet_JECUnc       [999];
        Float_t aJet_genPt        [999];
        Float_t aJet_genEta       [999];
        Float_t aJet_genPhi       [999];
        float SimBsmass           [999];
        float SimBspt             [999];
        float SimBseta            [999];
        float SimBsphi            [999];

        //if( currentTree->GetBranch("") )

        currentTree->SetBranchAddress("EVENT",            &EVENT);
        if   ( currentTree->GetBranch("PUweight") )       currentTree->SetBranchAddress("PUweight",         &PUweight);
        if   ( currentTree->GetBranch("PUweightP") )      currentTree->SetBranchAddress("PUweightP",        &PUweightP);
        if   ( currentTree->GetBranch("PUweightM") )      currentTree->SetBranchAddress("PUweightM",        &PUweightM);
        if   ( currentTree->GetBranch("lheNj") )          currentTree->SetBranchAddress("lheNj",            &lheNj);
        if   ( currentTree->GetBranch("weightTrig2012") ) currentTree->SetBranchAddress("weightTrig2012",   &weightTrig2012);
        if   ( currentTree->GetBranch("triggerFlags") )   currentTree->SetBranchAddress("triggerFlags",     triggerFlags);
        if   ( currentTree->GetBranch("SCALEsyst") )      currentTree->SetBranchAddress("SCALEsyst",        SCALEsyst);
        currentTree->SetBranchAddress("Vtype",            &Vtype);
        if   ( currentTree->GetBranch("nhJets") )         currentTree->SetBranchAddress("nhJets",           &nhJets);
        currentTree->SetBranchAddress("naJets",           &naJets);
        currentTree->SetBranchAddress("nSimBs",           &nSimBs);
        currentTree->SetBranchAddress("nvlep",            &nvlep);
        currentTree->SetBranchAddress("nalep",            &nalep);
        if   ( currentTree->GetBranch("nPVs") )           currentTree->SetBranchAddress("nPVs",             &nPVs);
        currentTree->SetBranchAddress("genB",             &genB);
        currentTree->SetBranchAddress("genBbar",          &genBbar);
        currentTree->SetBranchAddress("genTop",           &genTop);
        currentTree->SetBranchAddress("genTbar",          &genTbar);
        currentTree->SetBranchAddress("METtype1p2corr",   &METtype1p2corr);
        currentTree->SetBranchAddress("vLepton_charge",   vLepton_charge);
        currentTree->SetBranchAddress("vLepton_mass"  ,   vLepton_mass);
        currentTree->SetBranchAddress("vLepton_pt"    ,   vLepton_pt);
        currentTree->SetBranchAddress("vLepton_eta"   ,   vLepton_eta);
        currentTree->SetBranchAddress("vLepton_phi"   ,   vLepton_phi);
        currentTree->SetBranchAddress("vLepton_genPt" ,   vLepton_genPt);
        currentTree->SetBranchAddress("vLepton_genEta",   vLepton_genEta);
        currentTree->SetBranchAddress("vLepton_genPhi",   vLepton_genPhi);
        currentTree->SetBranchAddress("vLepton_charge",   vLepton_charge);
        currentTree->SetBranchAddress("vLepton_pfCorrIso",vLepton_pfCorrIso);
        currentTree->SetBranchAddress("vLepton_type",     vLepton_type);
        currentTree->SetBranchAddress("vLepton_wp80",     vLepton_wp80);
        currentTree->SetBranchAddress("vLepton_wp95",     vLepton_wp95);
        currentTree->SetBranchAddress("vLepton_wp70",     vLepton_wp70);
        currentTree->SetBranchAddress("vLepton_idMVAtrig", vLepton_idMVAtrig);

        currentTree->SetBranchAddress("vLepton_dxy",      vLepton_dxy);
        currentTree->SetBranchAddress("vLepton_dz",       vLepton_dz);
        //currentTree->SetBranchAddress("vLepton_id2012tight",vLepton_id2012tight);
        currentTree->SetBranchAddress("aLepton_charge",   aLepton_charge);
        currentTree->SetBranchAddress("aLepton_mass"  ,   aLepton_mass);
        currentTree->SetBranchAddress("aLepton_pt"    ,   aLepton_pt);
        currentTree->SetBranchAddress("aLepton_eta"   ,   aLepton_eta);
        currentTree->SetBranchAddress("aLepton_phi"   ,   aLepton_phi);
        currentTree->SetBranchAddress("aLepton_genPt" ,   aLepton_genPt);
        currentTree->SetBranchAddress("aLepton_genEta",   aLepton_genEta);
        currentTree->SetBranchAddress("aLepton_genPhi",   aLepton_genPhi);
        currentTree->SetBranchAddress("aLepton_charge",   aLepton_charge);
        currentTree->SetBranchAddress("aLepton_pfCorrIso",aLepton_pfCorrIso);
        currentTree->SetBranchAddress("aLepton_type",     aLepton_type);
        currentTree->SetBranchAddress("aLepton_wp80",     aLepton_wp80);
        currentTree->SetBranchAddress("aLepton_wp95",     aLepton_wp95);
        currentTree->SetBranchAddress("aLepton_dxy",      aLepton_dxy);
        currentTree->SetBranchAddress("aLepton_dz",       aLepton_dz);
        //currentTree->SetBranchAddress("aLepton_id2012tight",aLepton_id2012tight);

        if( currentTree->GetBranch("hJet_pt") ) {
            currentTree->SetBranchAddress("hJet_pt",          hJet_pt);
            currentTree->SetBranchAddress("hJet_eta",         hJet_eta);
            currentTree->SetBranchAddress("hJet_phi",         hJet_phi);
            currentTree->SetBranchAddress("hJet_e",           hJet_e);
            currentTree->SetBranchAddress("hJet_flavour",     hJet_flavour);
            currentTree->SetBranchAddress("hJet_puJetIdL",    hJet_puJetIdL);
            currentTree->SetBranchAddress("hJet_id",          hJet_id);
            currentTree->SetBranchAddress("hJet_csv",         hJet_csv);
            currentTree->SetBranchAddress("hJet_cmva",        hJet_cmva);
            currentTree->SetBranchAddress("hJet_csv_nominal", hJet_csv_nominal);
            currentTree->SetBranchAddress("hJet_csv_upBC",    hJet_csv_upBC);
            currentTree->SetBranchAddress("hJet_csv_downBC",  hJet_csv_downBC);
            currentTree->SetBranchAddress("hJet_csv_upL",     hJet_csv_upL);
            currentTree->SetBranchAddress("hJet_csv_downL",   hJet_csv_downL);
            currentTree->SetBranchAddress("hJet_JECUnc",      hJet_JECUnc);
            currentTree->SetBranchAddress("hJet_genPt",       hJet_genPt);
            currentTree->SetBranchAddress("hJet_genEta",      hJet_genEta);
            currentTree->SetBranchAddress("hJet_genPhi",      hJet_genPhi);
        }
        currentTree->SetBranchAddress("aJet_pt",          aJet_pt);
        currentTree->SetBranchAddress("aJet_eta",         aJet_eta);
        currentTree->SetBranchAddress("aJet_phi",         aJet_phi);
        currentTree->SetBranchAddress("aJet_e",           aJet_e);
        currentTree->SetBranchAddress("aJet_flavour",     aJet_flavour);
        currentTree->SetBranchAddress("aJet_puJetIdL",    aJet_puJetIdL);
        currentTree->SetBranchAddress("aJet_id",          aJet_id);
        currentTree->SetBranchAddress("aJet_csv",         aJet_csv);
        if( currentTree->GetBranch("aJet_cmva") )
            currentTree->SetBranchAddress("aJet_cmva",      aJet_cmva);
        currentTree->SetBranchAddress("aJet_csv_nominal", aJet_csv_nominal);
        currentTree->SetBranchAddress("aJet_csv_upBC",    aJet_csv_upBC);
        currentTree->SetBranchAddress("aJet_csv_downBC",  aJet_csv_downBC);
        currentTree->SetBranchAddress("aJet_csv_upL",     aJet_csv_upL);
        currentTree->SetBranchAddress("aJet_csv_downL",   aJet_csv_downL);
        currentTree->SetBranchAddress("aJet_JECUnc",      aJet_JECUnc);
        currentTree->SetBranchAddress("aJet_genPt",       aJet_genPt);
        currentTree->SetBranchAddress("aJet_genEta",      aJet_genEta);
        currentTree->SetBranchAddress("aJet_genPhi",      aJet_genPhi);
        currentTree->SetBranchAddress("SimBs_mass",       SimBsmass);
        currentTree->SetBranchAddress("SimBs_pt",         SimBspt);
        currentTree->SetBranchAddress("SimBs_eta",        SimBseta);
        currentTree->SetBranchAddress("SimBs_phi",        SimBsphi);

        /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
        /* @@@@@@@@@@@@@@@@@@@@@@@@@ EVENT LOOP @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */

        // loop over entries
        int counter = 0;
        Long64_t nentries = currentTree->GetEntries();
        cout << "Total number of entries: " << nentries << endl;
        cout << " -> This job will process events in the range [ " << evLow << ", " << evHigh << " ]" << endl;

        int event_trials  = 0;

        if( evHigh<0 ) evHigh = nentries;
        for (Long64_t i = 0; i < nentries ; i++) {

            // if fixed-size job and above upper bound, continue...
            if(counter>evHigh && fixNumEvJob) continue;

            // otherwise, if outside the event window, continue...
            if(!fixNumEvJob && !(i>=evLow && i<evHigh) ) continue;
            events_++;

            // print the processed event number
            if(i%500==0) {
                cout << i << " (" << float(i)/float(nentries)*100 << " %)" << endl;
            }

            // set variables that are used, but for which there may be no branches in the input tree
            PUweight       = 1.0;
            PUweightP      = 1.0;
            PUweightM      = 1.0;
            lheNj          = 1.0;
            weightTrig2012 = 1.0;
            for(int k = 0; k < 70 ; k++) {
                triggerFlags_[k] = 1;
            }
            for(int k = 0; k < 3 ; k++) {
                SCALEsyst_[k] = 1.0;
            }
            nhJets = 0;
            nPVs   = 1;


            // read event...
            currentTree->GetEntry(i);


            if( debug>=2 ) {
                cout << endl;
                cout << "******************************" << endl;
                cout << "Analyzing event " << EVENT.event << endl;
            }

            // RESET VARIABLES
            nPermut_            = 0;
            nPermut_alt_        = 0;
            nTotInteg_          = 0;
            nTotInteg_alt_      = 0;
            matchesH_           = -99;
            matchesT_           = -99;
            matchesHAll_        = -99;
            matchesWAll_        = -99;
            matchesTAll_        = -99;
            overlapLight_       = -99;
            overlapHeavy_       = -99;
            type_               = -99;
            syst_               = -99;
            iterations_         = -1;

            mH_matched_         = -99.;
            mW_matched_         = -99.;
            mTop_matched_       = -99.;

            nSimBs_             = nSimBs;
            nMatchSimBsOld_     = -99;
            nMatchSimBs_v1_     = -99;
            nMatchSimBs_v2_     = -99;
            nMatchSimBs_        = -99;
            nMatchSimCs_v1_     = -99;
            nMatchSimCs_v2_     = -99;
            nMatchSimCs_        = -99;
            time_               = 0.;

            num_of_trials_      = 0;

            counter_            = counter;
            weight_             = scaleFactor;
            weightTopPt_        = 1;
            nPVs_               = nPVs;
            Vtype_              = Vtype;

            EVENT_.run          = EVENT.run;
            EVENT_.lumi         = EVENT.lumi;
            EVENT_.event        = EVENT.event;
            EVENT_.json         = EVENT.json;

            PUweight_           = PUweight;
            PUweightP_          = PUweightP;
            PUweightM_          = PUweightM;

            lheNj_              = lheNj;
            n_b_                = SCALEsyst[9];
            n_c_                = SCALEsyst[8];
            n_l_                = SCALEsyst[7];
            n_g_                = SCALEsyst[6];

            trigger_     = weightTrig2012;
            triggerErr_  = 0.;
            sf_ele_      = -99;

            for(int k = 0; k < 70 ; k++) {
                triggerFlags_[k] = triggerFlags[k];
            }

            SCALEsyst_[0] = 1.0;
            if( count_Q2 ) {
                SCALEsyst_[1] = TMath::Power(SCALEsyst[2],SCALEsyst[1])*SCALEsyst[4]/normDown;
                SCALEsyst_[2] = TMath::Power(SCALEsyst[3],SCALEsyst[1])*SCALEsyst[5]/normUp;
            }

            probAtSgn_          =  0.;
            probAtSgn_alt_      =  0.;

            probAtSgn_ttbb_     =  0.;
            probAtSgn_alt_ttbb_ =  0.;
            probAtSgn_alt_ttbj_ =  0.;
            probAtSgn_alt_ttcc_ =  0.;
            probAtSgn_alt_ttjj_ =  0.;

            nMassPoints_        = TMath::Max(nHiggsMassPoints,nTopMassPoints);
            flag_type0_         = -99;
            flag_type1_         = -99;
            flag_type2_         = -99;
            flag_type3_         = -99;
            flag_type4_         = -99;
            flag_type6_         = -99;

            btag_LR_            = -99;

            for( int k = 0; k < 2; k++) {
                lepton_pt_[k] = -99;
                lepton_eta_[k] = -99;
                lepton_phi_[k] = -99;
                lepton_m_[k] = -99;
                lepton_charge_[k] = -99;
                lepton_rIso_[k] = -99;
                lepton_type_[k] = -99;
                lepton_dxy_[k] = -99;
                lepton_dz_[k] = -99;
                lepton_wp80_[k] = -99;
                lepton_wp70_[k] = -99;
                lepton_wp95_[k] = -99;
                lepton_MVAtrig_[k] = -99;
            }
            Mll_  = -99.;
            MTln_ = -99.;

            for( int k = 0; k < NMAXJETS; k++) {
                jet_pt_[k] = -99;
                jet_pt_alt_[k] = -99;
                jet_eta_[k] = -99;
                jet_phi_[k] = -99;
                jet_m_[k] = -99;
                jet_csv_[k] = -99;
            }
            for( int k = 0; k < NMAXPERMUT; k++) {
                perm_to_jet_    [k] = -99;
                perm_to_gen_    [k] = -99;
                perm_to_jet_alt_[k] = -99;
                perm_to_gen_alt_[k] = -99;
            }

            // save the values into the tree (save mH[0] in case no scan is required)
            for( unsigned int m = 0; m < (unsigned int)nHiggsMassPoints ; m++) {
                mH_scan_[m] = mH[m];
            }
            for( unsigned int t = 0; t < (unsigned int)nTopMassPoints ; t++) {
                mT_scan_[t] = mT[t];
            }

            // reset the gen top/Higgs 4-vector
            for(int elem=0; elem<4; elem++) {
                p4T_   [elem] = -99.;
                p4Tbar_[elem] = -99.;
                p4H_   [elem] = -99.;
            }
            ttH_.reset();

            // save jet kinematics into the tree...
            nJet_ = 8;
            for(int q = 0; q < nJet_ ; q++ ) {
                // kinematics
                jet_pt_     [q] = -99;
                jet_pt_alt_ [q] = -99;
                jet_eta_    [q] = -99;
                jet_phi_    [q] = -99;
                jet_m_      [q] = -99;
                jet_csv_    [q] = -99;
            }
            hJetAmong_    = 0;
            jetsAboveCut_ = 0;

            // set all prob. to 0.0;
            for(int p = 0 ; p < nTotInteg_; p++) {
                probAtSgn_permut_       [p] = 0.;
                probAtSgnErr_permut_    [p] = 0.;
                callsAtSgn_permut_      [p] = 0 ;
                chi2AtSgn_permut_       [p] = 0.;
            }
            for(int p = 0 ; p < nPermut_; p++) {
                probAtSgn_bb_permut_ [p] = 0.;
            }
            for(int p = 0 ; p < nTotInteg_alt_; p++) {
                probAtSgn_alt_permut_   [p] = 0.;
                probAtSgnErr_alt_permut_[p] = 0.;
                callsAtSgn_alt_permut_  [p] = 0 ;
                chi2AtSgn_alt_permut_   [p] = 0.;
            }
            for(int p = 0 ; p < nPermut_alt_; p++) {
                probAtSgn_bj_permut_ [p] = 0.;
                probAtSgn_cc_permut_ [p] = 0.;
                probAtSgn_jj_permut_ [p] = 0.;
            }


            // a map between a 'barcode' which identifies a set of four-vectors (modulo their magnitude)
            // and a GSLMCIntegrator
            map<string, ROOT::Math::GSLMCIntegrator*> perm_to_integrator;

            // a map between a 'barcode' which identifies a set of four-vectors (modulo their magnitude)
            // and a phase-space-point, i.e. a collection of four-vectors
            map<string, PhaseSpacePoint> perm_to_phasespacepoint;

            // a map between a 'barcode' which identifies a set of four-vectors (modulo their magnitude)
            // and its integral, error, and integration chi2
            map<string, double> perm_to_integral;
            map<string, double> perm_to_integralError;
            map<string, double> perm_to_integralChi2;

            /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
            /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ GEN PARTICLES @@@@@@@@@@@@@@@@@@@@@@@@@@  */



            // read top decay products from input files
            TLorentzVector topBLV   (1,0,0,1);
            TLorentzVector topW1LV  (1,0,0,1);
            TLorentzVector topW2LV  (1,0,0,1);
            TLorentzVector atopBLV  (1,0,0,1);
            TLorentzVector atopW1LV (1,0,0,1);
            TLorentzVector atopW2LV (1,0,0,1);
            TLorentzVector genBLV   (1,0,0,1);
            TLorentzVector genBbarLV(1,0,0,1);

            // here, we save possible W->cs decays
            TLorentzVector topCLV   (1,0,0,1);
            TLorentzVector atopCLV  (1,0,0,1);

            if(debug>=2) cout << "@A" << endl;

            // set-up top decay products (if available from input file...)
            // N.B. upper limit needed to prevent from using unfilled branches (<=> filled with std::max)
            //      (casues many WARNINGS to be thrown)

            if(genTop.bmass>0 && genTop.bmass<10) {
                topBLV.SetPtEtaPhiM(  genTop.bpt,genTop.beta,genTop.bphi,genTop.bmass );
                topW1LV.SetPtEtaPhiM( genTop.wdau1pt,genTop.wdau1eta, genTop.wdau1phi,genTop.wdau1mass);
                topW2LV.SetPtEtaPhiM( genTop.wdau2pt,genTop.wdau2eta, genTop.wdau2phi,genTop.wdau2mass);

                if( TMath::Abs(genTop.wdau1id)==4 )
                    topCLV.SetPtEtaPhiM( genTop.wdau1pt,genTop.wdau1eta, genTop.wdau1phi,genTop.wdau1mass);
                else if( TMath::Abs(genTop.wdau2id)==4 )
                    topCLV.SetPtEtaPhiM( genTop.wdau2pt,genTop.wdau2eta, genTop.wdau2phi,genTop.wdau2mass);
                else {}

                p4T_[0] = (topBLV+topW1LV+topW2LV).Pt();
                p4T_[1] = (topBLV+topW1LV+topW2LV).Eta();
                p4T_[2] = (topBLV+topW1LV+topW2LV).Phi();
                p4T_[3] = (topBLV+topW1LV+topW2LV).M();
            }
            if(genTbar.bmass>0 && genTbar.bmass<10) {
                atopBLV.SetPtEtaPhiM(  genTbar.bpt,genTbar.beta,genTbar.bphi,genTbar.bmass );
                atopW1LV.SetPtEtaPhiM( genTbar.wdau1pt,genTbar.wdau1eta, genTbar.wdau1phi,genTbar.wdau1mass);
                atopW2LV.SetPtEtaPhiM( genTbar.wdau2pt,genTbar.wdau2eta,genTbar.wdau2phi,genTbar.wdau2mass);

                if( TMath::Abs(genTbar.wdau1id)==4 )
                    atopCLV.SetPtEtaPhiM( genTbar.wdau1pt,genTbar.wdau1eta, genTbar.wdau1phi,genTbar.wdau1mass);
                else if( TMath::Abs(genTbar.wdau2id)==4 )
                    atopCLV.SetPtEtaPhiM( genTbar.wdau2pt,genTbar.wdau2eta, genTbar.wdau2phi,genTbar.wdau2mass);
                else {}

                p4Tbar_[0] = (atopBLV+atopW1LV+atopW2LV).Pt();
                p4Tbar_[1] = (atopBLV+atopW1LV+atopW2LV).Eta();
                p4Tbar_[2] = (atopBLV+atopW1LV+atopW2LV).Phi();
                p4Tbar_[3] = (atopBLV+atopW1LV+atopW2LV).M();
            }
            if(genB.mass>0 && genB.mass<10 && (genB.momid==25 || genB.momid==23)) {
                genBLV.SetPtEtaPhiM(genB.pt,genB.eta ,genB.phi, genB.mass );
            }
            if(genBbar.mass>0 && genBbar.mass<10 && (genBbar.momid==25 || genBbar.momid==23)) {
                genBbarLV.SetPtEtaPhiM(genBbar.pt,genBbar.eta ,genBbar.phi, genBbar.mass );
            }
            if( genBLV.Pt()>1 && genBbarLV.Pt()>1 ) {
                p4H_[0] = (genBLV+genBbarLV).Pt();
                p4H_[1] = (genBLV+genBbarLV).Eta();
                p4H_[2] = (genBLV+genBbarLV).Phi();
                p4H_[3] = (genBLV+genBbarLV).M();
            }

            if(debug>=2) cout << "@B" << endl;

            // Compute SF to correct gen top pT
            float weightTPt    = 1.;
            float weightTbarPt = 1.;

            if(p4T_[0] > 0) {
                if(p4T_[0] < 463.312)
                    weightTPt = 1.18246 + 2.10061*1e-6*p4T_[0]*(p4T_[0] - 2*463.312);
                else
                    weightTPt = 0.732;
            }
            if(p4Tbar_[0] > 0) {
                if(p4T_[0] < 463.312)
                    weightTbarPt = 1.18246 + 2.10061*1e-6*p4Tbar_[0]*(p4Tbar_[0] - 2*463.312);
                else
                    weightTbarPt = 0.732;
            }
            weightTopPt_ = weightTPt /**weightTbarPt */ ;

            if(debug>=2) std::cout << "top weight = " << weightTopPt_ << " = " << weightTPt << "(*" << weightTbarPt << ")" <<  std::endl;
            //------------------------------------------

            // dummy cut (for the moment)
            bool properEventSL = (genBLV.Pt()>0 && genBbarLV.Pt()>0 && topBLV.Pt()>0 && topW1LV.Pt()>0 && topW2LV.Pt()>0 && atopBLV.Pt()>0 && atopW1LV.Pt()>0 && atopW2LV.Pt()>0);
            bool properEventDL = (genBLV.Pt()>0 && genBbarLV.Pt()>0 && topBLV.Pt()>0 && topW1LV.Pt()>0 && topW2LV.Pt()>0 && atopBLV.Pt()>0 && atopW1LV.Pt()>0 && atopW2LV.Pt()>0);

            if(!(properEventSL || properEventDL)) {
                cout << "A dummy cut has failed..." << endl;
                cout << " => go to next event!" << endl;
                cout << "******************************" << endl;
                continue;
            }

            if(debug>=2) cout << "@C" << endl;

            // define LV for the 6 (8) particles in ttbb (ttH) events
            TLorentzVector TOPHADW1(1,0,0,1);
            TLorentzVector TOPHADW2(1,0,0,1);
            TLorentzVector TOPHADB (1,0,0,1);
            TLorentzVector TOPLEPW1(1,0,0,1);
            TLorentzVector TOPLEPW2(1,0,0,1);
            TLorentzVector TOPLEPB (1,0,0,1);
            TLorentzVector HIGGSB1 (1,0,0,1);
            TLorentzVector HIGGSB2 (1,0,0,1);

            HIGGSB1.SetPtEtaPhiM( genBLV.Pt(),    genBLV.Eta(),    genBLV.Phi(),    genBLV.M());
            HIGGSB2.SetPtEtaPhiM( genBbarLV.Pt(), genBbarLV.Eta(), genBbarLV.Phi(), genBbarLV.M());

            if(debug>=2) cout << "@D" << endl;

            /* ////// PDG numbering: ///////
            d  1      e-   11
            u  2      ve   12
            s  3      m-   13
            c  4      vmu  14
            b  5      tau- 15
            t  6      vtau 16
            */ /////////////////////////////

            // 1st case: t -> blv, t~ -> b~ud
            if( abs(genTop.wdau1id)>6 && abs(genTop.wdau1id)<=16 && abs(genTbar.wdau1id)<6 && abs(genTbar.wdau1id)>=1 ) {
                TOPHADW1.SetPxPyPzE( atopW1LV.Px(), atopW1LV.Py(), atopW1LV.Pz(), atopW1LV.E());
                TOPHADW2.SetPxPyPzE( atopW2LV.Px(), atopW2LV.Py(), atopW2LV.Pz(), atopW2LV.E());
                TOPHADB.SetPxPyPzE( atopBLV.Px(),  atopBLV.Py(),   atopBLV.Pz(),  atopBLV.E());
                if( abs(genTop.wdau1id)==11 || abs(genTop.wdau1id)==13 || abs(genTop.wdau1id)==15 ) {
                    TOPLEPW1.SetPxPyPzE  ( topW1LV.Px(), topW1LV.Py(), topW1LV.Pz(), topW1LV.E());
                    TOPLEPW2.SetPxPyPzE  ( topW2LV.Px(), topW2LV.Py(), topW2LV.Pz(), topW2LV.E());
                }
                else {
                    TOPLEPW1.SetPxPyPzE  ( topW2LV.Px(), topW2LV.Py(), topW2LV.Pz(), topW2LV.E());
                    TOPLEPW2.SetPxPyPzE  ( topW1LV.Px(), topW1LV.Py(), topW1LV.Pz(), topW1LV.E());
                }
                TOPLEPB.SetPxPyPzE(  topBLV.Px(),  topBLV.Py(),   topBLV.Pz(), topBLV.E());
            }

            // 2nd case: t -> bud, t~ -> b~lv
            else if(abs(genTop.wdau1id)<6 && abs(genTop.wdau1id)>=1 && abs(genTbar.wdau1id)>6 && abs(genTbar.wdau1id)<=16) {
                TOPHADW1.SetPxPyPzE( topW1LV.Px(), topW1LV.Py(), topW1LV.Pz(), topW1LV.E());
                TOPHADW2.SetPxPyPzE( topW2LV.Px(), topW2LV.Py(), topW2LV.Pz(), topW2LV.E());
                TOPHADB.SetPxPyPzE( topBLV.Px(),  topBLV.Py(),   topBLV.Pz(),  topBLV.E());
                if( abs(genTbar.wdau1id)==11 || abs(genTbar.wdau1id)==13 || abs(genTbar.wdau1id)==15 ) {
                    TOPLEPW1.SetPxPyPzE  ( atopW1LV.Px(), atopW1LV.Py(), atopW1LV.Pz(), atopW1LV.E());
                    TOPLEPW2.SetPxPyPzE  ( atopW2LV.Px(), atopW2LV.Py(), atopW2LV.Pz(), atopW2LV.E());
                }
                else {
                    TOPLEPW1.SetPxPyPzE  ( atopW2LV.Px(), atopW2LV.Py(), atopW2LV.Pz(), atopW2LV.E());
                    TOPLEPW2.SetPxPyPzE  ( atopW1LV.Px(), atopW1LV.Py(), atopW1LV.Pz(), atopW1LV.E());
                }
                TOPLEPB.SetPxPyPzE( atopBLV.Px(),  atopBLV.Py(),   atopBLV.Pz(),  atopBLV.E());
            }

            // 3rd case: t -> blv, t~ -> b~lv
            else if(abs(genTop.wdau1id)>6 && abs(genTop.wdau1id)<=16 && abs(genTbar.wdau1id)>6 && abs(genTbar.wdau1id)<=16) {
                if( abs(genTop.wdau1id)==11 || abs(genTop.wdau1id)==13 || abs(genTop.wdau1id)==15 ) {
                    TOPHADW1.SetPxPyPzE  ( topW1LV.Px(), topW1LV.Py(), topW1LV.Pz(), topW1LV.E());
                    TOPHADW2.SetPxPyPzE  ( topW2LV.Px(), topW2LV.Py(), topW2LV.Pz(), topW2LV.E());
                }
                else {
                    TOPHADW1.SetPxPyPzE  ( topW2LV.Px(), topW2LV.Py(), topW2LV.Pz(), topW2LV.E());
                    TOPHADW2.SetPxPyPzE  ( topW1LV.Px(), topW1LV.Py(), topW1LV.Pz(), topW1LV.E());
                }
                TOPHADB.SetPxPyPzE( topBLV.Px(),  topBLV.Py(),   topBLV.Pz(),  topBLV.E());
                if( abs(genTbar.wdau1id)==11 || abs(genTbar.wdau1id)==13 || abs(genTbar.wdau1id)==15 ) {
                    TOPLEPW1.SetPxPyPzE  ( atopW1LV.Px(), atopW1LV.Py(), atopW1LV.Pz(), atopW1LV.E());
                    TOPLEPW2.SetPxPyPzE  ( atopW2LV.Px(), atopW2LV.Py(), atopW2LV.Pz(), atopW2LV.E());
                }
                else {
                    TOPLEPW1.SetPxPyPzE  ( atopW2LV.Px(), atopW2LV.Py(), atopW2LV.Pz(), atopW2LV.E());
                    TOPLEPW2.SetPxPyPzE  ( atopW1LV.Px(), atopW1LV.Py(), atopW1LV.Pz(), atopW1LV.E());
                }
                TOPLEPB.SetPxPyPzE( atopBLV.Px(),  atopBLV.Py(),   atopBLV.Pz(),  atopBLV.E());
            }

            // all the rest...
            else {}

            if(debug>=2) cout << "@E" << endl;

            /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
            /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ NUs from top @@@@@@@@@@@@@@@@@@@@@@@@@@@  */


            // search for neutrinos in t and t~ separately (this way, also single-top events will be filled properly)
            TLorentzVector INVISIBLE(0,0,0,0);

            //  t -> blv
            if( abs(genTop.wdau1id)>6 && abs(genTop.wdau1id)<=16 ) {

                TLorentzVector INVISIBLE_tmp;
                if( abs(genTop.wdau1id)==11 || abs(genTop.wdau1id)==13 || abs(genTop.wdau1id)==15 )
                    INVISIBLE_tmp.SetPxPyPzE( topW2LV.Px(), topW2LV.Py(), topW2LV.Pz(), topW2LV.E());
                else
                    INVISIBLE_tmp.SetPxPyPzE( topW1LV.Px(), topW1LV.Py(), topW1LV.Pz(), topW1LV.E());

                INVISIBLE += INVISIBLE_tmp;
            }

            // t~ -> blv
            if( abs(genTbar.wdau1id)>6 && abs(genTbar.wdau1id)<=16 ) {

                TLorentzVector INVISIBLE_tmp;
                if( abs(genTbar.wdau1id)==11 || abs(genTbar.wdau1id)==13 || abs(genTbar.wdau1id)==15 )
                    INVISIBLE_tmp.SetPxPyPzE( atopW2LV.Px(), atopW2LV.Py(), atopW2LV.Pz(), atopW2LV.E());
                else
                    INVISIBLE_tmp.SetPxPyPzE( atopW1LV.Px(), atopW1LV.Py(), atopW1LV.Pz(), atopW1LV.E());

                INVISIBLE += INVISIBLE_tmp;
            }

            if(debug>=2) cout << "@F" << endl;

            // save informations on the ttH system
            if( switchoffOL==0 &&
                    p4T_[0]>0. && p4Tbar_[0]>0. && p4H_[0]>0. &&
                    TMath::Abs(HIGGSB1.Py())>0  && TMath::Abs(HIGGSB2.Py())>0) {

                if(debug>=2) {
                    cout <<  "p4T    = (" << p4T_   [0] << "," <<    p4T_   [1]<< "," <<    p4T_   [2] << "," <<    p4T_   [3] << ")" << endl;
                    cout <<  "p4Tbar = (" << p4Tbar_[0] << "," <<    p4Tbar_[1]<< "," <<    p4Tbar_[2] << "," <<    p4Tbar_[3] << ")" << endl;
                    cout <<  "p4H    = (" << p4H_   [0] << "," <<    p4H_   [1]<< "," <<    p4H_   [2] << "," <<    p4H_   [3] << ")" << endl;
                }

                TLorentzVector top(0,0,0,0);
                top.SetPtEtaPhiM  ( p4T_   [0],    p4T_   [1],    p4T_   [2],    p4T_   [3]);
                TLorentzVector atop(0,0,0,0);
                atop.SetPtEtaPhiM ( p4Tbar_[0],    p4Tbar_[1],    p4Tbar_[2],    p4Tbar_[3]);
                TLorentzVector higgs(0,0,0,0);
                higgs.SetPtEtaPhiM( p4H_   [0],    p4H_   [1],    p4H_   [2],    p4H_   [3]);

                // this is needed because if t+t~+h has 0 pT, tot.Eta() raises a warning
                double px = (top+atop+higgs).Px();
                double py = (top+atop+higgs).Py();
                //double pz = (top+atop+higgs).Pz();

                double x1,x2;
                ttH_.me2_ttH  = meIntegrator->meSquaredOpenLoops( &top, &atop, &higgs, x1, x2);
                ttH_.x1       = x1;
                ttH_.x2       = x2;
                ttH_.pdf      = meIntegrator->ggPdf( x1, x2, (2*MT + MH)/2. )*x1*x1*x2*x2;
                ttH_.pt       = TMath::Sqrt( px*px + py*py );
                ttH_.eta      = ttH_.pt>1e-03 ? (top+atop+higgs).Eta() : (top+atop+higgs).Rapidity();
                ttH_.phi      = (top+atop+higgs).Phi();
                ttH_.m        = (top+atop+higgs).M();
                ttH_.me2_ttbb = meIntegrator->meSquaredOpenLoops_ttbb( &top, &atop, &HIGGSB1, &HIGGSB2, x1, x2);
            }


            /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
            /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ GEN BHADRONS @@@@@@@@@@@@@@@@@@@@@@@@@@@  */

            if(debug>=2) cout << "@G" << endl;

            // find out number of b-hadrons in the event...
            nSimBs_         = nSimBs;
            nMatchSimBsOld_ = 0;
            nMatchSimBs_v1_ = 0;
            nMatchSimBs_v2_ = 0;
            nMatchSimBs_    = 0;
            nMatchSimCs_v1_ = 0;
            nMatchSimCs_v2_ = 0;
            nMatchSimCs_    = 0;



            for(int l = 0; l<nSimBs; l++) {
                TLorentzVector Bs(1,0,0,1);
                Bs.SetPtEtaPhiM( SimBspt[l], SimBseta[l], SimBsphi[l], SimBsmass[l]);

                if( topBLV.Pt()>10 && deltaR(topBLV,  Bs)<0.5 ) continue;
                if(atopBLV.Pt()>10 && deltaR(atopBLV, Bs)<0.5 ) continue;

                for(int hj = 0; hj<nhJets; hj++) {
                    TLorentzVector hJLV(1,0,0,1);
                    if(hJet_genPt[hj]>10)
                        hJLV.SetPtEtaPhiM( hJet_genPt[hj], hJet_genEta[hj], hJet_genPhi[hj], 0.0);
                    if( hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<5 && deltaR(Bs, hJLV)<0.5 ) nMatchSimBsOld_++;
                }
                for(int aj = 0; aj<naJets; aj++) {
                    TLorentzVector aJLV(1,0,0,1);
                    if(aJet_genPt[aj]>10)
                        aJLV.SetPtEtaPhiM( aJet_genPt[aj], aJet_genEta[aj], aJet_genPhi[aj], 0.0);
                    if( aJLV.Pt()>20 && TMath::Abs(aJLV.Eta())<5 && deltaR(Bs, aJLV)<0.5 ) nMatchSimBsOld_++;
                }
            }
            if( nSimBs>=2) {
                for(int l = 0; l<nSimBs-1; l++) {
                    TLorentzVector Bs1(1,0,0,1);
                    Bs1.SetPtEtaPhiM( SimBspt[l], SimBseta[l], SimBsphi[l], SimBsmass[l]);
                    if( topBLV.Pt()>10 && deltaR(topBLV,  Bs1)<0.5 ) continue;
                    if(atopBLV.Pt()>10 && deltaR(atopBLV, Bs1)<0.5 ) continue;
                    for(int m = l+1; m<nSimBs; m++) {
                        TLorentzVector Bs2(1,0,0,1);
                        Bs2.SetPtEtaPhiM( SimBspt[m], SimBseta[m], SimBsphi[m], SimBsmass[m]);
                        if( topBLV.Pt()>10 && deltaR(topBLV,  Bs2)<0.5 ) continue;
                        if(atopBLV.Pt()>10 && deltaR(atopBLV, Bs2)<0.5 ) continue;
                        if( deltaR(Bs1,Bs2)<0.50 ) nMatchSimBsOld_--;
                    }
                }
            }



            // now find out how many matched b's we have...
            for(int hj = 0; hj<nhJets; hj++) {
                TLorentzVector hJLV(1,0,0,1);
                if(hJet_genPt[hj]>10)
                    hJLV.SetPtEtaPhiM( hJet_genPt[hj], hJet_genEta[hj], hJet_genPhi[hj], 0.0);

                // if jet is within acceptance...
                if( hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<5 ) {
                    if( topBLV.Pt()>10 && deltaR(topBLV, hJLV )<0.5 ) continue;
                    if(atopBLV.Pt()>10 && deltaR(atopBLV,hJLV )<0.5 ) continue;
                    if( abs(hJet_flavour[hj])==5 ) nMatchSimBs_v1_++;
                }

                if( hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<2.5 ) {
                    if( topBLV.Pt()>10 && deltaR(topBLV, hJLV )<0.5 ) continue;
                    if(atopBLV.Pt()>10 && deltaR(atopBLV,hJLV )<0.5 ) continue;
                    if( abs(hJet_flavour[hj])==5 ) nMatchSimBs_v2_++;
                }

                if( hJet_pt[hj]>30 && hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<2.5 ) {
                    if( topBLV.Pt()>10 && deltaR(topBLV, hJLV )<0.5 ) continue;
                    if(atopBLV.Pt()>10 && deltaR(atopBLV,hJLV )<0.5 ) continue;
                    if( abs(hJet_flavour[hj])==5 ) nMatchSimBs_++; //baseline
                }

            }
            for(int aj = 0; aj<naJets; aj++) {
                TLorentzVector aJLV(1,0,0,1);
                if(aJet_genPt[aj]>10)
                    aJLV.SetPtEtaPhiM( aJet_genPt[aj], aJet_genEta[aj], aJet_genPhi[aj], 0.0);

                // if jet is within acceptance...
                if( aJLV.Pt()>20 && TMath::Abs(aJLV.Eta())<5 ) {
                    if( topBLV.Pt()>10 && deltaR(topBLV, aJLV )<0.5 ) continue;
                    if(atopBLV.Pt()>10 && deltaR(atopBLV,aJLV )<0.5 ) continue;
                    if( abs(aJet_flavour[aj])==5 ) nMatchSimBs_v1_++;
                }

                if( aJLV.Pt()>20 && TMath::Abs(aJLV.Eta())<2.5 ) {
                    if( topBLV.Pt()>10 && deltaR(topBLV, aJLV )<0.5 ) continue;
                    if(atopBLV.Pt()>10 && deltaR(atopBLV,aJLV )<0.5 ) continue;
                    if( abs(aJet_flavour[aj])==5 ) nMatchSimBs_v2_++;
                }

                if( aJet_pt[aj]>30 && aJLV.Pt()>20 && TMath::Abs(aJLV.Eta())<2.5 ) {
                    if( topBLV.Pt()>10 && deltaR(topBLV, aJLV )<0.5 ) continue;
                    if(atopBLV.Pt()>10 && deltaR(atopBLV,aJLV )<0.5 ) continue;
                    if( abs(aJet_flavour[aj])==5 ) nMatchSimBs_++;
                }

            }


            // now find out how many matched c's we have...
            for(int hj = 0; hj<nhJets; hj++) {
                TLorentzVector hJLV(1,0,0,1);
                if(hJet_genPt[hj]>10)
                    hJLV.SetPtEtaPhiM( hJet_genPt[hj], hJet_genEta[hj], hJet_genPhi[hj], 0.0);

                // if jet is within acceptance...
                if( hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<5 ) {
                    if( topCLV.Pt()>10 && deltaR(topCLV, hJLV )<0.5 ) continue;
                    if(atopCLV.Pt()>10 && deltaR(atopCLV,hJLV )<0.5 ) continue;
                    if( abs(hJet_flavour[hj])==4 ) nMatchSimCs_v1_++;
                }

                if( hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<2.5 ) {
                    if( topCLV.Pt()>10 && deltaR(topCLV, hJLV )<0.5 ) continue;
                    if(atopCLV.Pt()>10 && deltaR(atopCLV,hJLV )<0.5 ) continue;
                    if( abs(hJet_flavour[hj])==4 ) nMatchSimCs_v2_++;
                }

                if( hJet_pt[hj]>30 && hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<2.5 ) {
                    if( topCLV.Pt()>10 && deltaR(topCLV, hJLV )<0.5 ) continue;
                    if(atopCLV.Pt()>10 && deltaR(atopCLV,hJLV )<0.5 ) continue;
                    if( abs(hJet_flavour[hj])==4 ) nMatchSimCs_++;
                }

            }
            for(int aj = 0; aj<naJets; aj++) {
                TLorentzVector aJLV(1,0,0,1);
                if(aJet_genPt[aj]>10)
                    aJLV.SetPtEtaPhiM( aJet_genPt[aj], aJet_genEta[aj], aJet_genPhi[aj], 0.0);

                // if jet is within acceptance...
                if( aJLV.Pt()>20 && TMath::Abs(aJLV.Eta())<5 ) {
                    if( topCLV.Pt()>10 && deltaR(topCLV, aJLV )<0.5 ) continue;
                    if(atopCLV.Pt()>10 && deltaR(atopCLV,aJLV )<0.5 ) continue;
                    if( abs(aJet_flavour[aj])==4 ) nMatchSimCs_v1_++;
                }

                if( aJLV.Pt()>20 && TMath::Abs(aJLV.Eta())<2.5 ) {
                    if( topCLV.Pt()>10 && deltaR(topCLV, aJLV )<0.5 ) continue;
                    if(atopCLV.Pt()>10 && deltaR(atopCLV,aJLV )<0.5 ) continue;
                    if( abs(aJet_flavour[aj])==4 ) nMatchSimCs_v2_++;
                }

                if( aJet_pt[aj]>30 && aJLV.Pt()>20 && TMath::Abs(aJLV.Eta())<2.5 ) {
                    if( topCLV.Pt()>10 && deltaR(topCLV, aJLV )<0.5 ) continue;
                    if(atopCLV.Pt()>10 && deltaR(atopCLV,aJLV )<0.5 ) continue;
                    if( abs(aJet_flavour[aj])==4 ) nMatchSimCs_++;
                }

            }




            if(debug>=2) cout << "@H" << endl;

            int lock          = 0;
            int trial_success = 0;

            // loop over systematics
            for( unsigned int syst = 0; syst < systematics.size() ; syst++) {

                // which systematic is considered
                syst_ = systematics[ syst ];

                if( lock ) {
                    if(debug>=2) cout << "Skip systematics " << syst_ << " because the event is locked" << endl;
                    continue;
                }

                if(debug>=2) cout << "Dealing with systematics " << syst_  << endl;

                // decide which analysis to run
                doCSVup   = syst_==1 ;
                doCSVdown = syst_==2 ;
                doJECup   = syst_==3 ;
                doJECdown = syst_==4 ;
                doJERup   = syst_==5 ;
                doJERdown = syst_==6 ;

                // one more loop over the same event
                iterations_++;

                // reset additive probabilities
                probAtSgn_          =  0.;
                probAtSgn_alt_      =  0.;

                probAtSgn_ttbb_     =  0.;
                probAtSgn_alt_ttbb_ =  0.;
                probAtSgn_alt_ttbj_ =  0.;
                probAtSgn_alt_ttcc_ =  0.;
                probAtSgn_alt_ttjj_ =  0.;

                // reset the flags (events can migrate)
                flag_type0_         = -99;
                flag_type1_         = -99;
                flag_type2_         = -99;
                flag_type3_         = -99;
                flag_type4_         = -99;
                flag_type6_         = -99;

                /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
                /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@ LEPTON SELECTION @@@@@@@@@@@@@@@@@@@@@@@@@  */

                // keep track of the original leptons
                std::vector<int> lep_index;

                // charged leptons and MET
                TLorentzVector leptonLV, leptonLV2;
                TLorentzVector neutrinoLV;

                //count the number of loose leptons (muons or electrons) in the event
                int numLooseLep = 0;

                for( int k = 0; k < nvlep ; k++) {

                    float lep_pt   = vLepton_pt[k];
                    float lep_eta  = vLepton_eta[k];
                    float lep_type = vLepton_type[k];
                    float lep_iso  = vLepton_pfCorrIso[k];
                    float lep_dxy  = TMath::Abs(vLepton_dxy[k]);
                    float lep_dz   = TMath::Abs(vLepton_dz[k]);

                    if(
                        // muons
                        (lep_type==13 && lep_pt > lepPtLoose && TMath::Abs(lep_eta)<muEtaLoose && lep_iso < lepIsoLoose  && lep_dxy < 0.2 && lep_dz<0.5) ||

                        // electrons [FIX ME ]
                        (lep_type == 11 && lep_pt > lepPtLoose && TMath::Abs(lep_eta)<elEta && !(TMath::Abs(lep_eta) >1.442 && TMath::Abs(lep_eta)<1.566) &&
                         lep_iso < lepIsoLoose && vLepton_wp95[k] > 0 && lep_dxy < 0.04 && lep_dz<1.0 )

                    )
                        numLooseLep++;
                }

                //count the number of loose electrons in the event
                int numLooseAElec = 0;
                int aEle_index    = -99;

                for( int k = 0; k < nalep ; k++) {

                    float lep_pt   = aLepton_pt[k];
                    float lep_eta  = aLepton_eta[k];
                    float lep_type = aLepton_type[k];
                    float lep_iso  = aLepton_pfCorrIso[k];
                    float lep_dxy  = TMath::Abs(aLepton_dxy[k]);
                    float lep_dz   = TMath::Abs(aLepton_dz[k]);
                    //float lep_2012tight = aLepton_id2012tight[k];

                    if(  lep_type == 11 && lep_pt > lepPtLoose && TMath::Abs(lep_eta)<elEta && !(TMath::Abs(lep_eta) >1.442 && TMath::Abs(lep_eta)<1.566) &&
                            lep_iso < lepIsoLoose && aLepton_wp95[k] > 0.5 && lep_dxy < 0.04 && lep_dz<1.0) {
                        numLooseAElec++;
                        aEle_index  = k;
                    }

                }

                if(  debug>=2 && Vtype==2 && numLooseAElec>0) {
                    cout << numLooseLep << " loose leptons, "<< numLooseAElec << " loose electron(s) found in aLepton collection" << endl;
                }


                ///////////////////////////////////
                //         SL events:  e+j/m+j   //
                ///////////////////////////////////

                properEventSL = false;
                if( (ENABLE_EJ && numLooseLep==1 && Vtype==3) || (ENABLE_MJ && numLooseLep==1 && numLooseAElec<1 && Vtype==2) ) {

                    // first lepton...
                    leptonLV.SetPtEtaPhiM(vLepton_pt[0],vLepton_eta[0],vLepton_phi[0],vLepton_mass[0]);

                    lep_index.push_back( 0 );

                    if(doGenLevelAnalysis) {
                        if( vLepton_genPt[0]>5.)
                            leptonLV.SetPtEtaPhiM(vLepton_genPt[0], vLepton_genEta[0], vLepton_genPhi[0], (vLepton_type[0]==13 ? 0.113 : 0.0005 )  );
                        else
                            leptonLV.SetPtEtaPhiM( 5., 0., 0., 0. );
                    }

                    // tight cuts on lepton (SL)
                    int lepSelVtype2 =  (Vtype==2 && vLepton_type[0]==13 && leptonLV.Pt()>lepPtTight &&
                                         TMath::Abs(leptonLV.Eta())<muEtaTight && vLepton_pfCorrIso[0]<lepIsoTight);
                    int lepSelVtype3 =  (Vtype==3 && vLepton_type[0]==11 && leptonLV.Pt()>lepPtTight &&
                                         vLepton_pfCorrIso[0]<lepIsoTight && vLepton_wp80[0]>0 && TMath::Abs(vLepton_dxy[0])<0.02 );

                    // OR of four trigger paths:  "HLT_Mu40_eta2p1_v.*", "HLT_IsoMu24_eta2p1_v.*", "HLT_Mu40_v.*",  "HLT_IsoMu24_v.*"
                    int trigVtype2 =  (Vtype==2 && ( triggerFlags[22]>0 || triggerFlags[23]>0 || triggerFlags[14]>0 ||triggerFlags[21]>0 ));

                    // OR of two trigger paths:   "HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v.*", "HLT_Ele27_WP80_v.*"
                    int trigVtype3 =  (Vtype==3 &&  triggerFlags[44]>0 );

                    // for the moment, don't cut on trigger bit (save and cut offline)
                    trigVtype2 = 1;
                    trigVtype3 = 1;

                    // ID && trigger
                    properEventSL = (lepSelVtype2 && (isMC ? 1 : trigVtype2)) || (lepSelVtype3 && (isMC ? 1 : trigVtype3));

                    // trigger error
                    if( isMC && triggerErrors && (lepSelVtype2 && (isMC ? 1 : trigVtype2)) ) {
                        if( t_Vtype2_id && t_Vtype2_tr) {
                            float scale_id = 1.;
                            float id    = weightError( t_Vtype2_id, leptonLV.Pt(), leptonLV.Eta(), scale_id );
                            float scale_tr = 1.;
                            float tr    = weightError( t_Vtype2_tr, leptonLV.Pt(), leptonLV.Eta(), scale_tr );

                            float comb  = TMath::Sqrt( id*id + tr*tr )*(scale_id*scale_tr);
                            triggerErr_ = comb;

                            if( debug>=2 ) {
                                cout << "Vtype2: Trigger error: (" << leptonLV.Pt() << "," << leptonLV.Eta() << ")" << endl;
                                cout << " - scale_id = " << scale_id << " +/- " << scale_id*id << endl;
                                cout << " - scale_tr = " << scale_tr << " +/- " << scale_tr*tr << endl;
                                cout << " - comb = " << comb << endl;
                                cout << " - triggerWeight = " << trigger_ << ", from files: " << (scale_id*scale_tr) << endl;
                            }

                        }
                    }
                    if( isMC && triggerErrors && (lepSelVtype3 && (isMC ? 1 : trigVtype3)) ) {
                        if( t_Vtype3_id && t_Vtype3_tr) {
                            float scale_id = 1.;
                            float id    = weightError( t_Vtype3_id, leptonLV.Pt(), leptonLV.Eta(), scale_id );
                            float scale_tr = 1.;
                            float tr    = weightError( t_Vtype3_tr, leptonLV.Pt(), leptonLV.Eta(), scale_tr );

                            float comb  = TMath::Sqrt( id*id + tr*tr )*(scale_id*scale_tr);
                            triggerErr_ = comb;

                            if( debug>=2 ) {
                                cout << "Vtype3: Trigger error: (" << leptonLV.Pt() << "," << leptonLV.Eta() << ")" << endl;
                                cout << " - scale_id = " << scale_id << " +/- " << scale_id*id << endl;
                                cout << " - scale_tr = " << scale_tr << " +/- " << scale_tr*tr << endl;
                                cout << " - comb = " << comb << endl;
                                cout << " - triggerWeight = " << trigger_ << ", from files: " << (scale_id*scale_tr) << endl;
                            }
                        }
                    }

                    if( debug>=2 ) {
                        cout << "nvlep=" << nvlep << ", Vtype=" << Vtype << endl;
                        cout << "Lep sel. Vtype2 = " << lepSelVtype2 << ", lep sel. Vtype3 = " << lepSelVtype3 << endl;
                        cout << "Trigger: " <<  ((isMC ? 1 : trigVtype2) || (isMC ? 1 : trigVtype3)) << endl;
                        cout << "Passes = " << int (properEventSL) << endl;
                    }

                    // save lepton kinematics...
                    nLep_ = 1;

                    lepton_pt_     [0] = leptonLV.Pt();
                    lepton_eta_    [0] = leptonLV.Eta();
                    lepton_phi_    [0] = leptonLV.Phi();
                    lepton_m_      [0] = leptonLV.M();
                    lepton_charge_ [0] = vLepton_charge   [0];
                    lepton_rIso_   [0] = vLepton_pfCorrIso[0];
                    lepton_type_   [0] = vLepton_type[0];
                    lepton_dxy_    [0] = vLepton_dxy[0];
                    lepton_dz_     [0] = vLepton_dz[0];
                    lepton_wp80_   [0] = vLepton_wp80[0];
                    lepton_wp95_   [0] = vLepton_wp95[0];
                    lepton_wp70_   [0] = vLepton_wp70[0];
                    lepton_MVAtrig_[0] = vLepton_idMVAtrig[0];

                    if ( isMC && Vtype==3) // if single electron events
                        sf_ele_ = eleSF( lepton_pt_[0], lepton_eta_[0]);
                    else
                        sf_ele_ = 1;
                }

                ///////////////////////////////////
                //         DL events:  mm/ee     //
                ///////////////////////////////////

                properEventDL = false;
                if( numLooseLep==2 && ( (ENABLE_MM && Vtype==0) || (ENABLE_EE && Vtype==1) )) {

                    // first lepton...
                    leptonLV.SetPtEtaPhiM (vLepton_pt[0],vLepton_eta[0],vLepton_phi[0],vLepton_mass[0]);
                    lep_index.push_back( 0 );

                    // second lepton...
                    leptonLV2.SetPtEtaPhiM(vLepton_pt[1],vLepton_eta[1],vLepton_phi[1],vLepton_mass[1]);
                    lep_index.push_back( 1 );

                    if(doGenLevelAnalysis) {
                        if( vLepton_genPt[0]>5.)
                            leptonLV. SetPtEtaPhiM(vLepton_genPt[0], vLepton_genEta[0], vLepton_genPhi[0], (vLepton_type[0]==13 ? 0.113 : 0.0005 )  );
                        else
                            leptonLV. SetPtEtaPhiM( 5., 0., 0., 0. );
                        if( vLepton_genPt[1]>5.)
                            leptonLV2.SetPtEtaPhiM(vLepton_genPt[1], vLepton_genEta[1], vLepton_genPhi[1], (vLepton_type[1]==13 ? 0.113 : 0.0005 )  );
                        else
                            leptonLV2.SetPtEtaPhiM( 5., 0., 0., 0. );
                    }


                    // cut on leptons (DL)
                    int lepSelVtype0 = ( Vtype==0 && vLepton_type[0]==13 && vLepton_type[1]==13 &&
                                         ( (leptonLV.Pt() >20 && TMath::Abs(leptonLV.Eta()) <muEtaTight && vLepton_pfCorrIso[0]<lepIsoTight) ||
                                           (leptonLV2.Pt()>20 && TMath::Abs(leptonLV2.Eta())<muEtaTight && vLepton_pfCorrIso[1]<lepIsoTight) )
                                       ) && vLepton_charge[0]*vLepton_charge[1]<0;

                    int lepSelVtype1 = ( Vtype==1 && vLepton_type[0]==11 && vLepton_type[1]==11 &&
                                         ( (leptonLV.Pt() >20 && vLepton_pfCorrIso[0]<lepIsoTight && vLepton_wp95[0]>0.5 && TMath::Abs(vLepton_dxy[0])<0.02) ||
                                           (leptonLV2.Pt()>20 && vLepton_pfCorrIso[1]<lepIsoTight && vLepton_wp95[1]>0.5 && TMath::Abs(vLepton_dxy[1])<0.02) )
                                       ) && vLepton_charge[0]*vLepton_charge[1]<0;

                    // OR of four trigger paths:  "HLT_Mu40_eta2p1_v.*", "HLT_IsoMu24_eta2p1_v.*", "HLT_Mu40_v.*",  "HLT_IsoMu24_v.*"
                    int trigVtype0 =  (Vtype==0 && ( triggerFlags[22]>0 || triggerFlags[23]>0 || triggerFlags[14]>0 ||triggerFlags[21]>0 ));

                    // OR of two trigger paths:    "HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v.*", "HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v.*"
                    int trigVtype1 =  (Vtype==1 && ( triggerFlags[5]>0 || triggerFlags[6]>0 ) );

                    // for the moment, don't cut on trigger bit (save and cut offline)
                    trigVtype0 = 1;
                    trigVtype1 = 1;

                    // ID && trigger
                    properEventDL = (lepSelVtype0 && (isMC ? 1 : trigVtype0)) || (lepSelVtype1 && (isMC ? 1 : trigVtype1));

                    // trigger error
                    if( isMC && triggerErrors && (lepSelVtype0 && (isMC ? 1 : trigVtype0)) ) {
                        if( t_Vtype2_id && t_Vtype2_tr) {
                            float scale_id1 = 1.;
                            float id1       = weightError( t_Vtype2_id, leptonLV.Pt(),  leptonLV.Eta(),  scale_id1 );
                            float scale_tr1 = 1.;
                            float tr1       = weightError( t_Vtype2_tr, leptonLV.Pt(),  leptonLV.Eta(),  scale_tr1 );
                            float scale_id2 = 1.;
                            float id2       = weightError( t_Vtype2_id, leptonLV2.Pt(), leptonLV2.Eta(), scale_id2 );
                            float scale_tr2 = 1.0;
                            float tr2       = weightError( t_Vtype2_tr, leptonLV2.Pt(), leptonLV2.Eta(), scale_tr2 );

                            float scale_tr   =  scale_tr1 + scale_tr2 - scale_tr1*scale_tr2;

                            float scale_trUp   =  scale_tr1*(1+tr1) + scale_tr2*(1+tr2) - scale_tr1*(1+tr1)*scale_tr2*(1+tr2);
                            float scale_trDown =  scale_tr1*(1-tr1) + scale_tr2*(1-tr2) - scale_tr1*(1-tr1)*scale_tr2*(1-tr2);

                            float tr = scale_tr>0 ? TMath::Max( TMath::Abs(scale_tr-scale_trUp), TMath::Abs(scale_tr-scale_trDown) ) : 0.;

                            float comb  = TMath::Sqrt( tr*tr + id1*id1 + id2*id2 )*(scale_id1*scale_id2*scale_tr);
                            triggerErr_ = comb;

                            if( debug>=2 ) {
                                cout << "Vtype0: Trigger error: (" << leptonLV.Pt() << "," << leptonLV.Eta() << " ; " << leptonLV2.Pt() << "," << leptonLV2.Eta() << ")" << endl;
                                cout << " - scale_id1 = " << scale_id1 << " +/- " << scale_id1*id1 << endl;
                                cout << " - scale_id2 = " << scale_id2 << " +/- " << scale_id2*id2 << endl;
                                cout << " - scale_tr = " << scale_tr << " +/- " << scale_tr*tr << endl;
                                cout << " - comb = " << comb << endl;
                                cout << " - triggerWeight = " << trigger_ << ", from files: " << (scale_id1*scale_id2*scale_tr) << endl;
                            }

                        }
                    }
                    if( isMC && triggerErrors && (lepSelVtype1 && (isMC ? 1 : trigVtype1)) ) {
                        if( t_Vtype1_id && t_Vtype1L1_tr && t_Vtype1L2_tr) {

                            // L1 means Ele17, L2 means Ele8
                            float scale_tr1L1 = 1.;
                            float tr1L1       = weightError( t_Vtype1L1_tr, leptonLV.Pt(),  leptonLV.Eta(),  scale_tr1L1 );
                            float scale_tr1L2 = 1.;
                            float tr1L2       = weightError( t_Vtype1L2_tr, leptonLV.Pt(),  leptonLV.Eta(),  scale_tr1L2 );
                            float scale_tr2L1 = 1.;
                            float tr2L1       = weightError( t_Vtype1L1_tr, leptonLV2.Pt(),  leptonLV2.Eta(),  scale_tr2L1 );
                            float scale_tr2L2 = 1.;
                            float tr2L2       = weightError( t_Vtype1L2_tr, leptonLV2.Pt(),  leptonLV2.Eta(),  scale_tr2L2 );

                            // the scale factor
                            float scale_tr    =  scale_tr1L2*scale_tr2L1 + scale_tr2L2*scale_tr1L1 - scale_tr1L1*scale_tr2L1;

                            // scale_tr Up
                            float scale_trL1Up   = scale_tr1L2*(1+tr1L2)*scale_tr2L1*(1+tr2L1) + scale_tr2L2*(1+tr2L2)*scale_tr1L1*(1+tr1L1) - scale_tr1L1*(1+tr1L1)*scale_tr2L1*(1+tr2L1);
                            float scale_trL1Down = scale_tr1L2*(1-tr1L2)*scale_tr2L1*(1-tr2L1) + scale_tr2L2*(1-tr2L2)*scale_tr1L1*(1-tr1L1) - scale_tr1L1*(1-tr1L1)*scale_tr2L1*(1-tr2L1);
                            float tr = scale_tr>0 ? TMath::Max( TMath::Abs( scale_tr-scale_trL1Up ) , TMath::Abs( scale_tr-scale_trL1Down ) )/scale_tr : 0.;

                            float scale_id1 = 1.;
                            float id1       = weightError( t_Vtype1_id, leptonLV.Pt(),   leptonLV.Eta(),  scale_id1 );
                            float scale_id2 = 1.;
                            float id2       = weightError( t_Vtype1_id, leptonLV2.Pt(),  leptonLV2.Eta(),  scale_id2 );

                            float comb = TMath::Sqrt( tr*tr + id1*id1 + id2*id2)*(scale_tr*scale_id1*scale_id2);
                            triggerErr_ = comb;

                            if( debug>=2 ) {
                                cout << "Vtype1: Trigger error: (" << leptonLV.Pt() << "," << leptonLV.Eta() << " ; " << leptonLV2.Pt() << "," << leptonLV2.Eta() << ")" << endl;
                                cout << " - scale_id1 = " << scale_id1 << " +/- " << scale_id1*id1 << endl;
                                cout << " - scale_id2 = " << scale_id2 << " +/- " << scale_id2*id2 << endl;
                                cout << " - scale_tr = " << scale_tr << " +/- " << scale_tr*tr << endl;
                                cout << " - comb = " << comb << endl;
                                cout << " - triggerWeight = " << trigger_ << ", from files: " << (scale_id1*scale_id2*scale_tr) << endl;
                            }

                        }
                    }

                    if( debug>=2 ) {
                        cout << "nvlep=" << nvlep << ", Vtype=" << Vtype << endl;
                        cout << "Lep sel. Vtype2 = " << lepSelVtype0 << ", lep sel. Vtype3 = " << lepSelVtype1 << endl;
                        cout << "Trigger: " <<  ((isMC ? 1 : trigVtype0) || (isMC ? 1 : trigVtype1)) << endl;
                        cout << "Passes = " << int (properEventDL) << endl;
                    }

                    // save lepton(s) kinematics into the tree...
                    nLep_ = 2;

                    // lep 1...
                    lepton_pt_     [0] = leptonLV.Pt();
                    lepton_eta_    [0] = leptonLV.Eta();
                    lepton_phi_    [0] = leptonLV.Phi();
                    lepton_m_      [0] = leptonLV.M();
                    lepton_charge_ [0] = vLepton_charge   [0];
                    lepton_rIso_   [0] = vLepton_pfCorrIso[0];
                    lepton_type_   [0] = vLepton_type[0];
                    lepton_dxy_    [0] = vLepton_dxy[0];
                    lepton_dz_     [0] = vLepton_dz[0];
                    lepton_wp70_   [0] = vLepton_wp70[0];
                    lepton_wp80_   [0] = vLepton_wp80[0];
                    lepton_wp95_   [0] = vLepton_wp95[0];
                    lepton_MVAtrig_[0] = vLepton_idMVAtrig[0];

                    // lep 2...
                    lepton_pt_     [1] = leptonLV2.Pt();
                    lepton_eta_    [1] = leptonLV2.Eta();
                    lepton_phi_    [1] = leptonLV2.Phi();
                    lepton_m_      [1] = leptonLV2.M();
                    lepton_charge_ [1] = vLepton_charge   [1];
                    lepton_rIso_   [1] = vLepton_pfCorrIso[1];
                    lepton_type_   [1] = vLepton_type[1];
                    lepton_dxy_    [1] = vLepton_dxy[1];
                    lepton_dz_     [1] = vLepton_dz[1];
                    lepton_wp80_   [1] = vLepton_wp80[1];
                    lepton_wp70_   [1] = vLepton_wp70[1];
                    lepton_wp95_   [1] = vLepton_wp95[1];
                    lepton_MVAtrig_[1] = vLepton_idMVAtrig[1];

                    if ( isMC && Vtype==1 ) // if di-electron events
                        sf_ele_ = eleSF( lepton_pt_[0], lepton_eta_[0]) * eleSF( lepton_pt_[1], lepton_eta_[1]);
                    else
                        sf_ele_ = 1;

                }


                ///////////////////////////////////
                //         DL events:  em        //
                ///////////////////////////////////

                if( ENABLE_EM && Vtype==2 && numLooseLep==1 && numLooseAElec==1 && aEle_index>=0) {

                    // flag these events with different type
                    Vtype_ = 4;

                    // first lepton...
                    leptonLV.SetPtEtaPhiM (vLepton_pt[0],vLepton_eta[0],vLepton_phi[0],vLepton_mass[0]);
                    lep_index.push_back( 0 );

                    // second lepton...
                    leptonLV2.SetPtEtaPhiM(aLepton_pt[aEle_index],aLepton_eta[aEle_index],aLepton_phi[aEle_index],aLepton_mass[aEle_index]);
                    lep_index.push_back( -aEle_index-1 );

                    if(doGenLevelAnalysis) {
                        if( vLepton_genPt[0]>5.)
                            leptonLV. SetPtEtaPhiM(vLepton_genPt[0], vLepton_genEta[0], vLepton_genPhi[0], (vLepton_type[0]==13 ? 0.105 : 0.0005 )  );
                        else
                            leptonLV. SetPtEtaPhiM( 5., 0., 0., 0. );
                        if( aLepton_genPt[aEle_index]>5.)
                            leptonLV2.SetPtEtaPhiM(aLepton_genPt[aEle_index], aLepton_genEta[aEle_index], aLepton_genPhi[aEle_index], (aLepton_type[aEle_index]==13 ? 0.105 : 0.0005 )  );
                        else
                            leptonLV2.SetPtEtaPhiM( 5., 0., 0., 0. );
                    }

                    int lepSelVtype4 = (Vtype==2 && vLepton_type[0]==13 && aLepton_type[aEle_index]==11 &&
                                        (leptonLV.Pt() >20 && TMath::Abs(leptonLV.Eta()) <muEtaTight && vLepton_pfCorrIso[0]<lepIsoTight)
                                        /* do something for electrons ? */
                                        && vLepton_charge[0]*aLepton_charge[aEle_index]<0
                                       );

                    // OR of four trigger paths:  "HLT_Mu40_eta2p1_v.*", "HLT_IsoMu24_eta2p1_v.*", "HLT_Mu40_v.*",  "HLT_IsoMu24_v.*"
                    int trigVtype4 =  (Vtype==2 && ( triggerFlags[22]>0 || triggerFlags[23]>0 || triggerFlags[14]>0 ||triggerFlags[21]>0 ));

                    // for the moment, don't cut on trigger bit (save and cut offline)
                    trigVtype4 = 1;

                    // ID && trigger
                    properEventDL = lepSelVtype4 && (isMC ? 1 : trigVtype4) ;

                    // trigger error
                    if( isMC && triggerErrors && (lepSelVtype4 && (isMC ? 1 : trigVtype4)) ) {
                        if( t_Vtype2_id && t_Vtype2_tr && t_Vtype1_id) {

                            float scale_id1 = 1.;
                            float id1    = weightError( t_Vtype2_id, leptonLV.Pt(), leptonLV.Eta(), scale_id1 );
                            float scale_tr1 = 1.;
                            float tr1    = weightError( t_Vtype2_tr, leptonLV.Pt(), leptonLV.Eta(), scale_tr1 );
                            float scale_id2 = 1.;
                            float id2    = weightError( t_Vtype1_id, leptonLV2.Pt(), leptonLV2.Eta(), scale_id2 );
                            float scale_tr2 = 1.0;
                            float tr2       = 0.0;

                            float comb  = TMath::Sqrt( id1*id1 + tr1*tr1 + id2*id2 + tr2*tr2 )*(scale_id1*scale_tr1*scale_id2*scale_tr2);

                            triggerErr_ = comb;

                            if( debug>=2 ) {
                                cout << "Vtype4: Trigger error: (" << leptonLV.Pt() << "," << leptonLV.Eta() << " ; " << leptonLV2.Pt() << "," << leptonLV2.Eta() << ")" << endl;
                                cout << " - scale_id1 = " << scale_id1 << " +/- " << scale_id1*id1 << endl;
                                cout << " - scale_id2 = " << scale_id2 << " +/- " << scale_id2*id2 << endl;
                                cout << " - scale_tr = " << scale_tr1 << " +/- " << scale_tr1*tr1 << endl;
                                cout << " - comb = " << comb << endl;
                                cout << " - triggerWeight = " << trigger_ << ", from files: " << (scale_id1*scale_tr1) << endl;
                            }

                            // because events are selected from a subset of Vtype2
                            trigger_   *= (scale_id2*scale_tr2);

                        }
                    }

                    if( debug>=2 ) {
                        cout << "nvlep=" << nvlep << ", nalep=" << nalep  << ", Vtype=" << Vtype << endl;
                        cout << "Lep sel. Vtype4 = " << lepSelVtype4 << endl;
                        cout << "Trigger: " <<  (isMC ? 1 : trigVtype4)  << endl;
                        cout << "Passes = " << int (properEventDL) << endl;
                    }

                    // save lepton(s) kinematics into the tree...
                    nLep_ = 2;

                    // lep 1...
                    lepton_pt_     [0] = leptonLV.Pt();
                    lepton_eta_    [0] = leptonLV.Eta();
                    lepton_phi_    [0] = leptonLV.Phi();
                    lepton_m_      [0] = leptonLV.M();
                    lepton_charge_ [0] = vLepton_charge   [0];
                    lepton_rIso_   [0] = vLepton_pfCorrIso[0];
                    lepton_type_   [0] = vLepton_type[0];
                    lepton_dxy_    [0] = vLepton_dxy[0];
                    lepton_dz_     [0] = vLepton_dz[0];

                    // lep 2...
                    lepton_pt_     [1] = leptonLV2.Pt();
                    lepton_eta_    [1] = leptonLV2.Eta();
                    lepton_phi_    [1] = leptonLV2.Phi();
                    lepton_m_      [1] = leptonLV2.M();
                    lepton_charge_ [1] = aLepton_charge   [aEle_index];
                    lepton_rIso_   [1] = aLepton_pfCorrIso[aEle_index];
                    lepton_type_   [1] = aLepton_type[aEle_index];
                    lepton_dxy_    [1] = aLepton_dxy[aEle_index];
                    lepton_dz_     [1] = aLepton_dz[aEle_index];
                    lepton_wp80_   [1] = aLepton_wp80[aEle_index];
                    lepton_wp95_   [1] = aLepton_wp95[aEle_index];

                    if ( isMC && Vtype==4 ) // if EM events with triggered muon
                        sf_ele_ = eleSF( lepton_pt_[1], lepton_eta_[1]);
                    else
                        sf_ele_ = 1;

                } // end EM


                if ( !isMC && EVENT_.json < 0.5 ) {
                    if ( debug>=2 )
                        cout << "Event rejected: not present in json file"<<endl;
                    continue;
                }
                else if ( !isMC && reject_pixel_misalign_evts && (EVENT_.run > 207883 && EVENT_.run < 208307) ) {
                    if ( debug>=2 )
                        cout<<"Event rejected due to pixel misalignement"<<endl;
                    continue;
                }

                // continue if leptons do not satisfy cuts
                if( !(properEventSL || properEventDL) ) {
                    if( debug>=2 ) {
                        cout << "Rejected by lepton selection" << endl ;
                        cout << " => go to next event!" << endl;
                        cout << "******************************" << endl;
                    }
                    continue;
                }


                /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
                /* @@@@@@@@@@@@@@@@@@@@@@@@ JET SELECTION @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */

                // this container will hold the jets
                std::vector<JetObservable> jet_map;

                // for the MET
                float deltaPx = 0.;
                float deltaPy = 0.;

                // if doing the gen level analysis, read gen-jets
                if( doGenLevelAnalysis==0 ) {

                    // loop over jet collections
                    for(int coll = 0 ; coll < 2 ; coll++) {

                        // loop over jets
                        for(int hj = 0; hj < (coll==0 ? nhJets : naJets); hj++) {

                            float ptGen = -99.;
                            if(coll==0 && hJet_genPt[hj]>0.) ptGen = hJet_genPt[hj];
                            if(coll==1 && aJet_genPt[hj]>0.) ptGen = aJet_genPt[hj];

                            float pt     = (coll==0) ? hJet_pt [hj]  : aJet_pt [hj];
                            float eta    = (coll==0) ? hJet_eta[hj]  : aJet_eta[hj];
                            float phi    = (coll==0) ? hJet_phi[hj]  : aJet_phi[hj];
                            float e      = (coll==0) ? hJet_e  [hj]  : aJet_e  [hj];
                            float m2     = e*e - pt*pt*TMath::CosH(eta)*TMath::CosH(eta);
                            if(m2<0) m2 = 0.;
                            float m      = TMath::Sqrt( m2 );

                            int flavour  = (coll==0) ? hJet_flavour [hj] : aJet_flavour [hj];
                            int pu_id    = (coll==0) ? hJet_puJetIdL[hj] : aJet_puJetIdL[hj];
                            int id       = (coll==0) ? hJet_id      [hj] : aJet_id      [hj];
                            float JECUnc = (coll==0) ? hJet_JECUnc  [hj] : aJet_JECUnc  [hj];

                            // subtract the nominal JEC corrected jet (px,py)
                            deltaPx -= ( pt*TMath::Cos(phi) );
                            deltaPy -= ( pt*TMath::Sin(phi) );

                            // for JEC/JER systematics (N.B. this assumes that the jets are already corrected)
                            float shift     = 1.0;
                            if     ( doJECup   )  shift *= (1+JECUnc);
                            else if( doJECdown )  shift *= (1-JECUnc);
                            else if( doJERup   )  shift *= (ptGen>0. ?  1+resolutionBias(TMath::Abs(eta), +1, JERCORRECTED)*(1-ptGen/pt)   : 1.0);
                            else if( doJERdown )  shift *= (ptGen>0. ?  1+resolutionBias(TMath::Abs(eta), -1, JERCORRECTED)*(1-ptGen/pt)   : 1.0);
                            else {}

                            // if correct for bias in jet resolution (for sanity, enforce isMC)
                            if( isMC && doJERbias && !doJERup && !doJERdown)
                                shift *= (ptGen>0. ?  1+resolutionBias(TMath::Abs(eta), 0, JERCORRECTED)*(1-ptGen/pt)   : 1.0);

                            // change energy/mass by shift
                            pt *= shift;
                            m  *= shift;

                            // add the +/- JEC corrected jet (px,py)
                            deltaPx += ( pt*TMath::Cos(phi) );
                            deltaPy += ( pt*TMath::Sin(phi) );

                            // only jets in acceptance...
                            if( TMath::Abs(eta)> 2.5 ) continue;

                            // only jets passing pu ID...
                            if( pu_id < 0.5 ) continue;

                            // only jets passing id ID...
                            if( id < 0.5 ) continue;

                            // only jets above pt cut...
                            if( pt < jetPtThreshold  ) continue;

                            // if this is one of hJet, increment by one
                            if( coll==0 ) hJetAmong_++;

                            // the jet four-vector
                            TLorentzVector p4;
                            p4.SetPtEtaPhiM( pt, eta, phi, m );

                            // for csv systematics
                            float csv_nominal =  (coll==0) ? hJet_csv_nominal[hj] : aJet_csv_nominal[hj];
                            float csv_upBC    =  (coll==0) ? hJet_csv_upBC   [hj] : aJet_csv_upBC   [hj];
                            float csv_downBC  =  (coll==0) ? hJet_csv_downBC [hj] : aJet_csv_downBC [hj];
                            float csv_upL     =  (coll==0) ? hJet_csv_upL    [hj] : aJet_csv_upL    [hj];
                            float csv_downL   =  (coll==0) ? hJet_csv_downL  [hj] : aJet_csv_downL  [hj];

                            // default is csv_nominal ( <=> reshaped )
                            float csv         = csv_nominal;

                            // if doing cvs systematiics, use appropriate collection
                            if     ( doCSVup  ) csv =  TMath::Max(csv_upBC,   csv_upL);
                            else if( doCSVdown) csv =  TMath::Min(csv_downBC, csv_downL);
                            else {}

                            // if we apply SF for b-tag, or it is data, then deafult is 'reco' csv
                            if( useCSVcalibration || !isMC ) csv = (coll==0) ? hJet_csv[hj] : aJet_csv[hj];

                            // if using thr MVA btagger:
                            if( useCMVA ) {

                                // this is needed to remove the spike at zero!
                                if( csv>0. )
                                    csv = (coll==0) ? hJet_cmva[hj] : aJet_cmva[hj];
                                else
                                    csv = 0.;
                            }


                            if( enhanceMC && trial_success==0) {

                                string bin = "";
                                if( TMath::Abs( eta ) <= 1.0 )
                                    bin = "Bin0";
                                if( TMath::Abs( eta ) >  1.0 )
                                    bin = "Bin1";

                                string fl = "";
                                if(abs(flavour)==5)
                                    fl = "b";
                                if(abs(flavour)==4)
                                    fl = "c";
                                else
                                    fl = "l";

                                csv     =  btagger[fl+"_"+bin]->GetRandom();

                                if(coll==0) {
                                    hJet_csv        [hj] = csv;
                                    hJet_csv_nominal[hj] = csv;
                                }
                                if(coll==1) {
                                    aJet_csv        [hj] = csv;
                                    aJet_csv_nominal[hj] = csv;
                                }
                            }

                            // the jet observables (p4 and csv)
                            JetObservable myJet;
                            myJet.p4     = p4;
                            myJet.csv    = csv;
                            myJet.index  = (coll==0 ? hj : -hj-1);
                            myJet.shift  = shift;
                            myJet.flavour= flavour;

                            // push back the jet...
                            jet_map.push_back    ( myJet );

                            if( debug>=3 ) {
                                cout << "Jet #" << coll << "-" << hj << " => (" << pt << "," << eta << "," << phi << "," << m << "), ID=" << id << ", PU-ID=" << pu_id << ", csv = " << csv << ", flavour=" << flavour << endl;
                            }

                        }
                    }
                }
                // if doing the gen level analysis, read gen-jets
                else {

                    // reset everything
                    jet_map.clear();

                    // reset the sumEt
                    MET_sumEt_ = 0.;

                    // loop over jet collections
                    for(int coll = 0 ; coll < 2 ; coll++) {

                        // loop over jets
                        for(int hj = 0; hj < (coll==0 ? nhJets : naJets); hj++) {

                            float pt     = (coll==0) ? hJet_genPt [hj]  : aJet_genPt [hj];
                            float eta    = (coll==0) ? hJet_genEta[hj]  : aJet_genEta[hj];
                            float phi    = (coll==0) ? hJet_genPhi[hj]  : aJet_genPhi[hj];

                            // assume massless jets
                            // (unfortunately necessary because the mass of the genJet is not saved)
                            float e      = (coll==0) ? hJet_genPt [hj]*TMath::CosH(hJet_genEta[hj]) : aJet_genPt [hj]*TMath::CosH(aJet_genEta[hj]);
                            float m      = 0.;

                            float flavor = (coll==0) ? hJet_flavour [hj] : aJet_flavour [hj];

                            // only jets in acceptance
                            // (this is needed because the TF and csv shapes are valid only in the acceptance)
                            if( TMath::Abs(eta) > 2.5 ) continue;

                            if( debug>=3 ) {
                                cout << "Gen-Jet #" << coll << "-" << hj << " => (" << pt << "," << eta << "," << phi << "," << m  << "), flavor=" << flavor << endl;
                            }

                            // keep track of the per-jet smearing (for the MET...)
                            deltaPx -= ( pt*TMath::Cos(phi) );
                            deltaPy -= ( pt*TMath::Sin(phi) );

                            // needed to find appropriate PDF
                            string bin = "";
                            if( TMath::Abs( eta ) <= 1.0 )
                                bin = "Bin0";
                            if( TMath::Abs( eta ) >  1.0 )
                                bin = "Bin1";

                            // needed to find appropriate flavor
                            string fl = "";
                            if(abs(flavor)==5)
                                fl = "b";
                            else
                                fl = "l";

                            // set-up the TF parameters for the appropriate bin and flavor

                            // relative fraction of the two gaussians
                            jet_smear->SetParameter(0, fl == "b" ? 0.65 : 1.0);

                            // mean and sigma of the 1st
                            jet_smear->SetParameter(1, transferfunctions[fl+"_G1_m_"+bin]->Eval( e ));
                            jet_smear->SetParameter(2, transferfunctions[fl+"_G1_s_"+bin]->Eval( e ));

                            // mean and sigma of the 2nd
                            jet_smear->SetParameter(3, fl == "b" ? transferfunctions[fl+"_G2_m_"+bin]->Eval( e ) : e);
                            jet_smear->SetParameter(4, fl == "b" ? transferfunctions[fl+"_G2_s_"+bin]->Eval( e ) : 1.0);

                            // consider the range [0.2,2.0]*e, and evaluate every s1/5 GeV, s1 = width of the narrower gaussian
                            jet_smear->SetRange(e*0.2, e*2.0);
                            jet_smear->SetNpx( TMath::Min( TMath::Max( int( (1.8*e)/( jet_smear->GetParameter(2)/5 ) ), int(4)), 200 ) );

                            // the smeared energy
                            float e_smear = TMath::Max( float(jet_smear->GetRandom()), float(0.) );

                            // for c-quarks, we have a dedicated csv probability (but not a TF)
                            if(abs(flavor)==4)
                                fl = "c";

                            // the random csv value
                            float csv     =  btagger[fl+"_"+bin]->GetRandom();

                            // !!! smear the jet energy !!!
                            if(smearJets) pt *= (e_smear/e);

                            // add the jet transverse energy to the sumEt
                            MET_sumEt_ += pt;

                            if( debug>=3 ) {
                                cout << "Gen-Jet (smear)" << " => (" << pt << "," << eta << "," << phi << "," << m  << ")" << ", csv=" << csv  << endl;
                                cout << "jet_smear (" << jet_smear->GetNpx() << " points): " << string(Form("%.2f*exp(-0.5*((x-%.0f)**2)/%.1f**2) + %.2f*exp(-0.5*((x-%.0f)**2)/%.1f**2)",
                                        jet_smear->GetParameter(0), jet_smear->GetParameter(1),jet_smear->GetParameter(2),
                                        (1-jet_smear->GetParameter(0)), jet_smear->GetParameter(3), jet_smear->GetParameter(4)
                                                                                                           ))
                                     << " => ran : " << e << " --> " << e_smear << endl;
                            }

                            // keep track of the per-jet smearing (for the MET...)
                            deltaPx += ( pt*TMath::Cos(phi) );
                            deltaPy += ( pt*TMath::Sin(phi) );

                            // only jets above pt cut...
                            if( pt < jetPtThreshold ) continue;

                            // the jet four-vector
                            TLorentzVector p4;
                            p4.SetPtEtaPhiM( pt, eta, phi, m );

                            // the jet observables (p4 and csv)
                            JetObservable myJet;
                            myJet.p4     = p4;
                            myJet.csv    = csv;
                            myJet.flavour= flavor;
                            myJet.index  = (coll==0 ? hj : -hj-1);
                            myJet.shift  = 1.0;

                            // push back the jet...
                            jet_map.push_back    ( myJet );

                        }

                    }

                    // assume 16 average PU
                    //int nPU_ran        = ran->Poisson(16);
                    // assume each PU gives 50 GeV of sumEt
                    //float sumEt_PU_ran = nPU_ran*20.;
                    // add the extra smear
                    //MET_sumEt_ += sumEt_PU_ran;

                    deltaPx    += 0.;//ran->Gaus(0.,0.4*TMath::Sqrt(sumEt_PU_ran));
                    deltaPy    += 0.;//ran->Gaus(0.,0.4*TMath::Sqrt(sumEt_PU_ran));

                    // keep it fixed to a value such that sx~29 GeV
                    //MET_sumEt_ = 1800.;

                    // add to invisble particles pt the extra smearing coming from jets
                    float metPx = ( INVISIBLE.Px() - deltaPx /*- (nLep_==1 ? lepton_pt_[0]*TMath::Cos(lepton_phi_[0]) : (lepton_pt_[0]*TMath::Cos(lepton_phi_[0]) + lepton_pt_[1]*TMath::Cos(lepton_phi_[1])) )*/ );
                    float metPy = ( INVISIBLE.Py() - deltaPy /*- (nLep_==1 ? lepton_pt_[0]*TMath::Sin(lepton_phi_[0]) : (lepton_pt_[0]*TMath::Sin(lepton_phi_[0]) + lepton_pt_[1]*TMath::Sin(lepton_phi_[1])) )*/ );
                    neutrinoLV.SetPxPyPzE( metPx , metPy , 0., TMath::Sqrt( metPx*metPx + metPy*metPy) );

                    if( debug>=3 ) {
                        cout << "MET (from invisible) = (" << MET_pt_ << "," << MET_phi_ << ")" << endl;
                    }

                    // save smeared MET kinematics into the tree...
                    MET_pt_    = neutrinoLV.Pt();
                    MET_phi_   = neutrinoLV.Phi();

                    if( debug>=3 ) {
                        cout << "MET (smear) = (" << MET_pt_ << "," << MET_phi_ << ")" << endl;
                    }


                }


                ////////////////////////////////////////////////////////////////////////

                // MET
                float nuPx = METtype1p2corr.et*TMath::Cos(METtype1p2corr.phi);
                float nuPy = METtype1p2corr.et*TMath::Sin(METtype1p2corr.phi);

                // correct for JEC
                nuPx -= deltaPx;
                nuPy -= deltaPy;

                float nuE  = TMath::Sqrt(nuPx*nuPx+nuPy*nuPy);
                if( doGenLevelAnalysis==0 ) neutrinoLV.SetPxPyPzE(nuPx,nuPy,0. ,nuE);

                if( doGenLevelAnalysis==0 ) {
                    // save MET kinematics into the tree...
                    MET_pt_    = neutrinoLV.Pt();
                    MET_phi_   = neutrinoLV.Phi();
                    MET_sumEt_ = METtype1p2corr.sumet;
                }

                // save invisible particles kinematics into the tree...
                Nus_pt_    = INVISIBLE.Pt();
                Nus_phi_   = INVISIBLE.Phi();

                // save di-lepton mass
                if( properEventSL ) {
                    TLorentzVector l;
                    l.SetPtEtaPhiM( lepton_pt_[0], lepton_eta_[0], lepton_phi_[0], lepton_m_[0]);
                    TLorentzVector n;
                    n.SetPtEtaPhiM( MET_pt_, 0., MET_phi_, 0.);
                    MTln_ = (l+n).Mt();
                }
                if( properEventDL ) {
                    TLorentzVector l1;
                    l1.SetPtEtaPhiM( lepton_pt_[0], lepton_eta_[0], lepton_phi_[0], lepton_m_[0]);
                    TLorentzVector l2;
                    l2.SetPtEtaPhiM( lepton_pt_[1], lepton_eta_[1], lepton_phi_[1], lepton_m_[1]);
                    Mll_  = (l1+l2).M();
                }



                ////////////////////////////////////////////////////////////////////////


                // order jet list by Pt
                std::sort( jet_map.begin(),     jet_map.end(),     JetObservableListerByPt() );

                // if use btag shape, order by decreasing CSV
                // <=> when considering only a subset of the jets, this ensures that the combination
                // obtained from CSVM only jets is among those considered
                if( selectByBTagShape || recoverTopBTagBin)
                    std::sort( jet_map.begin(),   jet_map.end(),     JetObservableListerByCSV() );


                for( int csv_sys = 0; csv_sys < 19 ; csv_sys++) {
                    double csv_syst_value = 1.0;
                    if( useCSVcalibration )
                        csv_syst_value = GetCSVweight( jet_map, static_cast<sysType>(csv_sys), h_csv_wgt_hf, c_csv_wgt_hf, h_csv_wgt_lf);
                    weightCSV_[ csv_sys ] = csv_syst_value;
                }

                // fill arrays of jets
                std::vector<TLorentzVector>  jets_p4;
                std::vector<TLorentzVector>  jets_p4_reg;

                std::vector<double>          jets_csv;
                std::vector<double>          jets_csv_prob_b;
                std::vector<double>          jets_csv_prob_c;
                std::vector<double>          jets_csv_prob_j;

                std::vector<int>             jets_index;

                int jetsAboveCut = 0;

                for(unsigned int jj = 0; jj < jet_map.size() ; jj++ ) {

                    // the four-vector
                    TLorentzVector p4 = jet_map[jj].p4;

                    // the csv value
                    float csv = jet_map[jj].csv;

                    // FIX the b-tagger output
                    //  ==> Min needed because in csvUp, csv can exceed 1...,
                    //      Max needed because we crunch  [-inf,0[ -> {0.}
                    csv       =  TMath::Min( TMath::Max( csv, float(0.)), float(0.999999) );

                    // the index
                    int index = jet_map[jj].index;

                    // count jets above 40 GeV
                    if( p4.Pt()>jetPtLoose ) jetsAboveCut++;

                    // store jet p4...
                    jets_p4.push_back     ( p4 );
                    jets_p4_reg.push_back ( p4 );

                    // store csv
                    jets_csv.push_back( csv );

                    // store index
                    jets_index.push_back( index );

                    // needed to find appropriate csv PDF
                    string bin = "";
                    if( TMath::Abs( p4.Eta() ) <= 1.0 )
                        bin = "Bin0";
                    if( TMath::Abs( p4.Eta() ) >  1.0 )
                        bin = "Bin1";

                    // store PDF(csv)
                    jets_csv_prob_b.push_back( btagger["b_"+bin]!=0 ? btagger["b_"+bin]->GetBinContent( btagger["b_"+bin]->FindBin( csv ) ) : 1.);
                    jets_csv_prob_c.push_back( btagger["c_"+bin]!=0 ? btagger["c_"+bin]->GetBinContent( btagger["c_"+bin]->FindBin( csv ) ) : 1.);
                    jets_csv_prob_j.push_back( btagger["l_"+bin]!=0 ? btagger["l_"+bin]->GetBinContent( btagger["l_"+bin]->FindBin( csv ) ) : 1.);

                }

                jetsAboveCut_ = jetsAboveCut;

                // continue if not enough jets
                if( jetsAboveCut_<jetMultLoose ) {
                    if( debug>=2 ) {
                        cout << "Rejected by min jet cut (>= " <<jetMultLoose << " jets above " << jetPtLoose << " GeV)" << endl ;
                        cout << " => go to next event!" << endl;
                        cout << "******************************" << endl;
                    }
                    continue;
                }


                /* @@@@@@@@@@@@@@@@@@@@@@@@ JET ORDERING @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */

                // jet multiplicity
                int numJets30UntagM = 0;
                int numJets30UntagL = 0;
                int numJets30BtagL  = 0;
                int numJets30BtagM  = 0;
                int numJets30BtagT  = 0;

                // this vector contains the indices of up to 6 jets passing the CSVM(L) b-tag selection...
                // (type 7 uses two working points)
                vector<unsigned int> btag_indices;
                vector<unsigned int> btagLoose_indices;

                // this vector contains the indices of up to 6 jets failing the CSVM(L) b-tag selection...
                vector<unsigned int> buntag_indices;
                vector<unsigned int> buntagLoose_indices;

                // this vector contains the indices of those jets that should be preferred when looking at untag jets
                vector<unsigned int> buntag_indices_favorite;

                // this vector contains the indices of those unatagged jets in excess of the expectation
                vector<unsigned int> buntag_indices_extra;

                // this vector contains the indices of up to 12 jets passing ANY b-tag selection...
                vector<unsigned int> banytag_indices;


                for(unsigned int k = 0; k < jets_p4.size(); k++) {

                    float csv_k = jets_csv[k];
                    float pt_k  = (jets_p4[k]).Pt();

                    // passes CSVL...
                    int btag_L = csv_k>csv_WP_L ;
                    // passes CSVM...
                    int btag_M = csv_k>csv_WP_M ;
                    // passes CSVT...
                    int btag_T = csv_k>csv_WP_T ;

                    // any btag value...
                    if( pt_k>jetPtThreshold ) banytag_indices.push_back( k );

                    // passing at least CSVL...
                    if( pt_k>jetPtThreshold &&  btag_L ) {
                        numJets30BtagL ++;
                        btagLoose_indices.push_back( k );
                    }
                    // passing at least CSVM...
                    if( pt_k>jetPtThreshold &&  btag_M ) {
                        numJets30BtagM ++;
                        btag_indices.push_back( k );
                    }
                    // passing at least CSVT...
                    if( pt_k>jetPtThreshold &&  btag_T ) {
                        numJets30BtagT ++;
                    }

                    // failing at most CSVL...
                    if( pt_k>jetPtThreshold && !btag_L ) {
                        numJets30UntagL++;
                        buntagLoose_indices.push_back( k );
                    }
                    // failing at most CSVM...
                    if( pt_k>jetPtThreshold && !btag_M ) {
                        numJets30UntagM++;
                        buntag_indices.push_back( k );
                    }

                }

                numBTagL_ = numJets30BtagL;
                numBTagM_ = numJets30BtagM;
                numBTagT_ = numJets30BtagT;
                numJets_  = ( numJets30BtagM + numJets30UntagM);

                if( debug>=2 ) {
                    cout << "numBTagM = " << numBTagM_ << endl;
                    cout << "numJets = "  << numJets_ << endl;
                }

                /* @@@@@@@@@@@@@@@@@@@@@@@@ JET RE-ORDERING BY CSV PROB @@@@@@@@@@@@@@@@@@@@@@@@@@  */

                // in case the jet collections is reshuffled using the b-probability, keep a copy of old selection
                // (for debugging purposes)
                vector<unsigned int> btag_indices_backup   = btag_indices;
                vector<unsigned int> buntag_indices_backup = buntag_indices;

                // variable that flags events passing or failing the b-probability cut
                int passes_btagshape = 0;

                if( /*selectByBTagShape &&*/ useBtag &&                    // run this only if specified AND...
                                             ((properEventSL && banytag_indices.size()>=5) ||   // [ run this only if SL and at least 5 jets OR...
                                              (properEventDL && banytag_indices.size()>=4)) ) { //   run this only if DL and at least 4 jets ]

                    // map that transforms the indices into the permutation convention
                    std::map< unsigned int, unsigned int> btag_map;
                    btag_map.clear();

                    // number of inequivalent permutations
                    int nS, nB;

                    // sum of the b-tag probability over all permutations
                    float p_bb     =  0.;
                    float p_jj     =  0.;

                    // permutation with the largest probability
                    float max_p_bb = -1;
                    unsigned int selected_comb = 999;

                    // a flag to keep track of the jet multiplicity
                    int btag_flag = -999;

                    // if numJets>6, the first six jets ordered by decreasing pt, and
                    // then by decreasing csv are considered...
                    if( properEventSL && banytag_indices.size()>=6 ) {
                        btag_map[2] = banytag_indices[0];
                        btag_map[3] = banytag_indices[1];
                        btag_map[4] = banytag_indices[2];
                        btag_map[5] = banytag_indices[3];
                        btag_map[6] = banytag_indices[4];
                        btag_map[7] = banytag_indices[5];
                        nS = 15;
                        nB = 15;
                        btag_flag = 0;
                    }
                    else if( properEventSL && banytag_indices.size()==5 ) {
                        btag_map[2] = banytag_indices[0];
                        btag_map[3] = banytag_indices[1];
                        btag_map[4] = banytag_indices[1];
                        btag_map[5] = banytag_indices[2];
                        btag_map[6] = banytag_indices[3];
                        btag_map[7] = banytag_indices[4];
                        nS =  5;
                        nB = 10;
                        btag_flag = 1;
                    }
                    // if numJets>4, the first four jets ordered by decreasing pt, and
                    // then by decreasing csv are considered...
                    else if( properEventDL && banytag_indices.size()>=4 ) {
                        btag_map[2] = banytag_indices[0];
                        btag_map[3] = banytag_indices[0];
                        btag_map[4] = banytag_indices[0];
                        btag_map[5] = banytag_indices[1];
                        btag_map[6] = banytag_indices[2];
                        btag_map[7] = banytag_indices[3];
                        nS = 1;
                        nB = 6;
                        btag_flag = 2;
                    }
                    else {
                        cout << "Inconsistency in selectByBTagShape... continue" << endl;
                        cout << " => go to next event!" << endl;
                        cout << "******************************" << endl;
                        continue;
                    }

                    // loop over hypothesis [ TTH, TTbb ]
                    for(int hyp = 0 ; hyp<2;  hyp++) {

                        // list of permutations
                        int* permutList = 0;
                        if( btag_flag == 0 ) permutList = hyp==0 ?  permutations_6J_S : permutations_6J_B;
                        if( btag_flag == 1 ) permutList = hyp==0 ?  permutations_5J_S : permutations_5J_B;
                        if( btag_flag == 2 ) permutList = hyp==0 ?  permutations_4J_S : permutations_4J_B;

                        // loop over permutations
                        for(unsigned int pos = 0; pos < (unsigned int)( hyp==0 ? nS : nB ) ; pos++) {

                            // index of the four jets associated to b-quarks or W->qq
                            int bLep_pos = (permutList[pos])%1000000/100000;
                            int w1_pos   = (permutList[pos])%100000/10000;
                            int w2_pos   = (permutList[pos])%10000/1000;
                            int bHad_pos = (permutList[pos])%1000/100;
                            int b1_pos   = (permutList[pos])%100/10;
                            int b2_pos   = (permutList[pos])%10/1;

                            double p_b_bLep =  jets_csv_prob_b[  btag_map[bLep_pos] ];
                            double p_b_bHad =  jets_csv_prob_b[  btag_map[bHad_pos] ];
                            double p_b_b1   =  jets_csv_prob_b[  btag_map[b1_pos]   ];
                            double p_j_b1   =  jets_csv_prob_j[  btag_map[b1_pos]   ];
                            double p_b_b2   =  jets_csv_prob_b[  btag_map[b2_pos]   ];
                            double p_j_b2   =  jets_csv_prob_j[  btag_map[b2_pos]   ];
                            double p_j_w1   =  jets_csv_prob_j[  btag_map[w1_pos]   ];
                            double p_j_w2   =  jets_csv_prob_j[  btag_map[w2_pos]   ];

                            // the total probability
                            float p_pos = 0.;

                            // if sgn (ttbb)
                            if( hyp==0 ) {
                                p_pos =  p_b_bLep * p_b_bHad * p_b_b1 * p_b_b2 * p_j_w1 * p_j_w2;
                                p_bb += p_pos;

                                // look for a global maximum
                                if(  p_pos > max_p_bb ) {
                                    max_p_bb      = p_pos;
                                    selected_comb = pos;
                                }
                            }

                            // if bkg (ttjj)
                            if( hyp==1 ) {
                                p_pos =  p_b_bLep * p_b_bHad * p_j_b1 * p_j_b2 * p_j_w1 * p_j_w2;
                                p_jj += p_pos;
                            }

                        }

                    } // end loop over hypothesis

                    // normalize the probabilities...
                    p_bb /= nS;
                    p_jj /= nB;

                    // LR of ttbb vs ttjj hypotheses as variable to select events
                    btag_LR_ = (p_bb+p_jj)>0 ? p_bb/(p_bb+p_jj) : 0. ;

                    // depending on event type, check if the event passes the cut:
                    // if it does, check which combination yields the **largest** ttbb probability
                    int* permutListS = 0;
                    switch( btag_flag ) {
                    case 0:
                        passes_btagshape = ( btag_LR_ >= btag_prob_cut_6jets && selected_comb!=999);
                        permutListS      = permutations_6J_S;
                        break;
                    case 1:
                        passes_btagshape = ( btag_LR_ >= btag_prob_cut_5jets && selected_comb!=999);
                        permutListS      = permutations_5J_S;
                        break;
                    case 2:
                        passes_btagshape = ( btag_LR_ >= btag_prob_cut_4jets && selected_comb!=999);
                        permutListS      = permutations_4J_S;
                        break;
                    default:
                        break;
                    }

                    // if the event passes the cut, reshuffle jets into btag/buntag vectors
                    // N.B. ==> jets will be sorted by descending btag probaility!!!
                    if( passes_btagshape && selectByBTagShape) {

                        // reset old vector
                        btag_indices.clear();

                        // these are the four jets that are most compatible with four b-quarks
                        btag_indices.push_back(  btag_map[(permutListS[selected_comb])%1000000/100000] );
                        btag_indices.push_back(  btag_map[(permutListS[selected_comb])%1000/100]       );
                        btag_indices.push_back(  btag_map[(permutListS[selected_comb])%100/10]         );
                        btag_indices.push_back(  btag_map[(permutListS[selected_comb])%10/1]           );

                        // all other jets go into this collection
                        buntag_indices.clear();
                        for( unsigned int jj = 0 ; jj<banytag_indices.size(); jj++) {

                            // check for a match among the b-tagged jets
                            int isTagged = 0;
                            for( unsigned int bb = 0 ; bb<btag_indices.size(); bb++ )
                                if( banytag_indices[jj]==btag_indices[bb] ) isTagged = 1;

                            // if not matches, push back
                            if( isTagged == 0)
                                buntag_indices.push_back( banytag_indices[jj] );
                        }

                    }

                }



                /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
                /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@ EVENT SELECTION @@@@@@@@@@@@@@@@@@@@@@@@@  */


                ////////////////////////////////////////////////////
                // SEMILEPTONIC EVENTS                            //
                //        FULLLEPTONIC EVENTS                     //
                ////////////////////////////////////////////////////

                // if doing a cut-based analysis, reshuffle extra btag jets to recover >4 btag jets
                if( recoverTopBTagBin && !selectByBTagShape && numJets30BtagM>4 ) {

                    if( debug>=1 )
                        cout << numJets30BtagM << "(" << numJets30UntagM << ") b-tag(untag) jets found: trade the extra ones for light jets" << endl;

                    unsigned int extra = 0;
                    for( unsigned int w = 0; w<btag_indices.size(); w++) {
                        if( w > 3) {
                            buntag_indices.insert( buntag_indices.begin() , btag_indices[w] );
                            buntag_indices_favorite.push_back( extra ); // because we fill the vector from the top...
                            extra++;
                        }
                    }

                    // restore naive counting to make the event pass the cuts
                    numJets30BtagM  = 4;
                    numJets30UntagM = buntag_indices.size();

                    if( debug>=1 ) {
                        cout << "  After reshuffling:" << endl;
                        cout << "  --> numBTagM = "  << numJets30BtagM  << endl;
                        cout << "  --> numUntag = "  << numJets30UntagM << endl;
                    }

                }


                // categories defined by jet and btagged jet multiplicity (Nj,Nb)
                bool analyze_type0       = properEventSL  && numJets30UntagM==2  && doType0;
                bool analyze_type1       = properEventSL  && numJets30UntagM==2  && doType1;
                bool analyze_type2       = properEventSL  && numJets30UntagM==1  && doType2;
                bool analyze_type3       = properEventSL  && numJets30UntagM >2  && doType3;
                bool analyze_type6       = properEventDL                         && doType6;
                bool analyze_type7       = properEventDL  && numJets30BtagL==4   && doType7;

                // categories defined by jet multiplicity (Nj)
                bool analyze_typeBTag6   = properEventSL && (numJets_==6)                            && doTypeBTag6;
                bool analyze_typeBTag5   = properEventSL && (numJets_==5)                            && doTypeBTag5;
                bool analyze_typeBTag4   = properEventDL && (numJets_==4)                            && doTypeBTag4;

                // categories defined by jet multiplicity (Nj), but passing a minimum cut on the btag likelihood
                bool analyze_type0_BTag  = properEventSL && (numJets_==6)                            && doType0ByBTagShape;
                bool analyze_type1_BTag  = properEventSL && (numJets_==6)                            && doType1ByBTagShape;
                bool analyze_type2_BTag  = properEventSL && (numJets_==5)                            && doType2ByBTagShape;
                bool analyze_type3_BTag  = properEventSL && (numJets_ >6)                            && doType3ByBTagShape;
                bool analyze_type6_BTag  = properEventDL && (numJets_>=4)                            && doType6ByBTagShape;


                /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
                /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@ GEN MATCH @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */

                // temporary variables to count num. of matches
                int hMatches = 0;
                int tMatches = 0;
                int wMatches = 0;

                for( unsigned int w = 0; w<btag_indices.size(); w++) {

                    // use the Py() component to assess if the gen particle is present in the original tree
                    // (it is 0.0 otherwise)
                    if     (  TMath::Abs(HIGGSB1.Py()) >0  && deltaR(jets_p4[ btag_indices[w] ],HIGGSB1)  < GENJETDR ) hMatches++;
                    else if(  TMath::Abs(HIGGSB2.Py()) >0  && deltaR(jets_p4[ btag_indices[w] ],HIGGSB2)  < GENJETDR ) hMatches++;
                    if     (  TMath::Abs(TOPHADB.Py()) >0  && deltaR(jets_p4[ btag_indices[w] ],TOPHADB)  < GENJETDR ) tMatches++;
                    else if(  TMath::Abs(TOPLEPB.Py()) >0  && deltaR(jets_p4[ btag_indices[w] ],TOPLEPB)  < GENJETDR ) tMatches++;
                    if     (  TMath::Abs(TOPHADW1.Py())>0  && deltaR(jets_p4[ btag_indices[w] ],TOPHADW1) < GENJETDR ) wMatches++;
                    else if(  TMath::Abs(TOPHADW2.Py())>0  && deltaR(jets_p4[ btag_indices[w] ],TOPHADW2) < GENJETDR ) wMatches++;
                }
                matchesH_    = hMatches;
                matchesHAll_ = hMatches;
                matchesT_    = tMatches;
                matchesTAll_ = tMatches;
                matchesWAll_ = wMatches;
                wMatches = 0;

                for( unsigned int w = 0; w<buntag_indices.size(); w++) {

                    // use the Py() component to assess if the gen particle is present in the original tree
                    // (it is 0.0 otherwise)
                    if     (   TMath::Abs(HIGGSB1.Py())>0    && deltaR(jets_p4[ buntag_indices[w] ],HIGGSB1)  < GENJETDR ) matchesHAll_++;
                    else if(   TMath::Abs(HIGGSB2.Py())>0    && deltaR(jets_p4[ buntag_indices[w] ],HIGGSB2)  < GENJETDR ) matchesHAll_++;
                    if     (   TMath::Abs(TOPHADB.Py())>0    && deltaR(jets_p4[ buntag_indices[w] ],TOPHADB)  < GENJETDR ) matchesTAll_++;
                    else if(   TMath::Abs(TOPLEPB.Py())>0    && deltaR(jets_p4[ buntag_indices[w] ],TOPLEPB)  < GENJETDR ) matchesTAll_++;
                    if     (   TMath::Abs(TOPHADW1.Py())>0   && deltaR(jets_p4[ buntag_indices[w] ],TOPHADW1) < GENJETDR ) wMatches++;
                    else if(   TMath::Abs(TOPHADW2.Py())>0   && deltaR(jets_p4[ buntag_indices[w] ],TOPHADW2) < GENJETDR ) wMatches++;
                }
                matchesW_    =  wMatches;
                matchesWAll_ += wMatches;

                // gen level overlap
                vector<TLorentzVector> genHeavy;
                if( TMath::Abs(HIGGSB1.Py())>0) genHeavy.push_back( HIGGSB1);
                if( TMath::Abs(HIGGSB2.Py())>0) genHeavy.push_back( HIGGSB2);
                if( TMath::Abs(TOPHADB.Py())>0) genHeavy.push_back( TOPHADB);
                if( TMath::Abs(TOPLEPB.Py())>0) genHeavy.push_back( TOPLEPB);
                int overlapH = 0;
                if(genHeavy.size()>1) {
                    for(unsigned int k = 0; k < genHeavy.size()-1; k++) {
                        for(unsigned int l = k+1; l < genHeavy.size(); l++) {
                            if( deltaR(genHeavy[k], genHeavy[l])<0.5 ) overlapH++;
                        }
                    }
                }
                overlapHeavy_ = overlapH;
                vector<TLorentzVector> genLight;
                if(  TMath::Abs(TOPHADW1.Py())>0) genLight.push_back( TOPHADW1);
                if(  TMath::Abs(TOPHADW2.Py())>0) genLight.push_back( TOPHADW2);
                int overlapL = 0;
                for(unsigned int k = 0; k < genLight.size(); k++) {
                    for(unsigned int l = 0; l < genHeavy.size(); l++) {
                        if( deltaR(genLight[k], genHeavy[l])<0.5 ) overlapL++;
                    }
                }
                if( genLight.size()>1 && deltaR(genLight[0], genLight[1])<0.5  ) overlapL++;
                overlapLight_  = overlapL;


                // if ntuplize all event, then compute the regressed energy per jet...
                if( ntuplizeAll && useRegression ) {

                    // empty the array (was filled with the standard jets)
                    jets_p4_reg.clear();

                    // loop over all jets
                    for(unsigned int jj = 0; jj < jet_map.size() ; jj++ ) {

                        // the four-vector
                        TLorentzVector p4 = jet_map[jj].p4;

                        // the regressed pt of the jet
                        float pt_reg;

                        // call to the function that computes the regressed pt of the jet
                        getRegressionEnergy(pt_reg,            // the regressed pt (passed by &reference)
                                            "BDTG",            // the TMVA method
                                            reader,            // the TMVA reader
                                            readerVars,        // arrays with input variables
                                            currentTree_reg,   // the tree under process
                                            i,                 // the event of currentTree_reg under process
                                            jet_map[jj].index ,// index of hJet/aJet collection to be read
                                            jet_map[jj].shift, // a multiplicative variation of the input jet energy/pt
                                            (debug>=3) );      // if 1, print the input and output values (debug)

                        // protect against negative/too small values
                        if( pt_reg < 20. )
                            pt_reg = p4.Pt();

                        // set the jet (keep same direction as old jet)
                        TLorentzVector p4_reg;
                        p4_reg.SetPtEtaPhiM( pt_reg, p4.Eta(), p4.Phi(), p4.M()*(pt_reg/p4.Pt()) );

                        // push back the regressed jet
                        jets_p4_reg.push_back ( p4_reg );
                    }
                }


                /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
                /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ANALYSIS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */


                //  input 4-vectors
                vector<TLorentzVector> jets;
                vector<TLorentzVector> jets_alt;

                // internal map: [ position in "jets" ] -> [ position in "jets_p4" ]
                std::map< unsigned int, unsigned int> pos_to_index;

                // condition to trigger the ME calculation
                bool calcME =
                    (analyze_typeBTag6  || analyze_typeBTag5  || analyze_typeBTag4)  ||
                    ((analyze_type0      || analyze_type1      || analyze_type2      || analyze_type3      || analyze_type6 ) && numJets30BtagM==4 )  ||
                    (analyze_type7 && numJets30BtagM==3) ||
                    ((analyze_type0_BTag || analyze_type1_BTag || analyze_type2_BTag || analyze_type3_BTag || analyze_type6_BTag) && passes_btagshape);

                // consider th event only if of the desired type
                if( calcME ) {


                    if(debug>=2) {
                        cout << "Pass! Calc. ME..." << endl;
                    }


                    if( enhanceMC ) {
                        trial_success = 1;
                        cout << "Success after " << event_trials << " attempts!" << endl;
                        num_of_trials_ = event_trials;
                        event_trials   = 0;
                    }

                    // if the event has been accepted, then compute the regressed energy per jet
                    // (if not done before)
                    if( !ntuplizeAll && useRegression ) {

                        // empty the array (was filled with the standard jets)
                        jets_p4_reg.clear();

                        // loop over all jets
                        for(unsigned int jj = 0; jj < jet_map.size() ; jj++ ) {

                            // the four-vector
                            TLorentzVector p4 = jet_map[jj].p4;

                            // the regressed pt of the jet
                            float pt_reg;

                            // call to the function that computes the regressed pt of the jet
                            getRegressionEnergy(pt_reg,            // the regressed pt (passed by &reference)
                                                "BDTG",            // the TMVA method
                                                reader,            // the TMVA reader
                                                readerVars,        // arrays with input variables
                                                currentTree_reg,   // the tree under process
                                                i,                 // the event of currentTree_reg under process
                                                jet_map[jj].index ,// index of hJet/aJet collection to be read
                                                jet_map[jj].shift, // a multiplicative variation of the input jet energy/pt
                                                (debug>=3) );      // if 1, print the input and output values (debug)

                            // protect against negative/too small values
                            if( pt_reg < 20. )
                                pt_reg = p4.Pt();

                            // set the jet (keep same direction as old jet)
                            TLorentzVector p4_reg;
                            p4_reg.SetPtEtaPhiM( pt_reg, p4.Eta(), p4.Phi(), p4.M()*(pt_reg/p4.Pt()) );

                            // push back the regressed jet
                            jets_p4_reg.push_back ( p4_reg );
                        }
                    }



                    // find out which two untagged jets come from W->qq'
                    unsigned int ind1 = 999;
                    unsigned int ind2 = 999;

                    if( analyze_typeBTag4 ) {

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "\nProcessing event # " << counter << " (TYPE DL-4 JETS)." << " Event ID " << EVENT.event << endl;

                        /////////////////////////////////////////////////////
                        type_       = -3;
                        nPermut_    =  1;
                        nPermut_alt_=  6;
                        meIntegrator->setIntType( MEIntegratorNew::DL );
                        /////////////////////////////////////////////////////

                    }
                    else if( analyze_typeBTag5 ) {

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "\nProcessing event # " << counter << " (TYPE SL-5 JETS)." << " Event ID " << EVENT.event << endl;

                        /////////////////////////////////////////////////////
                        type_       = -1;
                        nPermut_    =  5;
                        nPermut_alt_= 10;
                        meIntegrator->setIntType( MEIntegratorNew::SL1wj );
                        /////////////////////////////////////////////////////

                    }
                    else if( analyze_typeBTag6 ) {

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "\nProcessing event # " << counter << " (TYPE SL6 JETS)." << " Event ID " << EVENT.event << endl;

                        /////////////////////////////////////////////////////
                        type_       =  -2;
                        nPermut_    =  15;
                        nPermut_alt_=  15;
                        meIntegrator->setIntType( MEIntegratorNew::SL2wj );
                        /////////////////////////////////////////////////////

                    }
                    else if( (analyze_type0 || analyze_type1 || analyze_type0_BTag || analyze_type1_BTag) ) {

                        // sanity check:
                        if(buntag_indices.size() != 2) {
                            cout << "Inconsistency found for (analyze_type0 || analyze_type1)... continue" << endl;
                            cout << " => go to next event!" << endl;
                            cout << "******************************" << endl;
                            continue;
                        }

                        // use untagged mass to assign to type 0 OR type 1
                        float WMass = (jets_p4[ buntag_indices[0] ]+jets_p4[  buntag_indices[1] ]).M();

                        // set index for untagged jets
                        ind1 = buntag_indices[0];
                        ind2 = buntag_indices[1];

                        if( (WMass>MwL && WMass<MwH)  && (analyze_type0 || analyze_type0_BTag) ) {

                            if(syst==0) counter++;
                            if( fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                            if(print) cout << "\nProcessing event # " << counter << " (TYPE 0), mW=" << WMass << " GeV." << " Event ID " << EVENT.event << endl;

                            /////////////////////////////////////////////////////
                            type_       =  0;
                            nPermut_    = 12;
                            nPermut_alt_= 12;
                            meIntegrator->setIntType( MEIntegratorNew::SL2wj );
                            /////////////////////////////////////////////////////
                        }
                        else if( !( WMass>MwL && WMass<MwH) && (analyze_type1 || analyze_type1_BTag)) {

                            if(syst==0) counter++;
                            if( fixNumEvJob && !(counter>=evLow && counter<=evHigh)  ) continue;
                            if(print) cout << "\nProcessing event # " << counter << " (TYPE 1), mW=" << WMass << " GeV." << " Event ID " << EVENT.event << endl;

                            /////////////////////////////////////////////////////
                            type_       =  1;
                            nPermut_    = 24;
                            nPermut_alt_= 24;
                            meIntegrator->setIntType( MEIntegratorNew::SL1wj );
                            /////////////////////////////////////////////////////
                        }
                        else {
                            continue;
                        }

                    }
                    else if( analyze_type2 || analyze_type2_BTag ) {

                        // sanity check:
                        if(buntag_indices.size() != 1) {
                            cout << "Inconsistency found for analyze_type2... continue" << endl;
                            cout << " => go to next event!" << endl;
                            cout << "******************************" << endl;
                            continue;
                        }

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "\nProcessing event # " << counter << " (TYPE 1)." << " Event ID " << EVENT.event << endl;

                        // set index for untagged jet
                        ind1 = buntag_indices[0];
                        ind2 = buntag_indices[0];

                        /////////////////////////////////////////////////////
                        type_       =  2;
                        nPermut_    = 12;
                        nPermut_alt_= 12;
                        meIntegrator->setIntType( MEIntegratorNew::SL1wj );
                        /////////////////////////////////////////////////////
                    }
                    else if( analyze_type3 || analyze_type3_BTag ) {

                        // sanity check:
                        if(buntag_indices.size() <= 2 ) {
                            cout << "Inconsistency found for analyze_type3... continue" << endl;
                            cout << " => go to next event!" << endl;
                            cout << "******************************" << endl;
                            continue;
                        }

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "\nProcessing event # " << counter << " (TYPE 3)." << " Event ID " << EVENT.event << endl;

                        // find out which are ind1 and ind2...
                        float minDiff     = 99999.;

                        // if 5 btag jets found, we choose to treat the 5th as untagged jet (is a c-quark ?)
                        if( buntag_indices_favorite.size()==1 ) {

                            ind1 =  buntag_indices[ buntag_indices_favorite[0] ];

                            if( debug>=1 )
                                cout << "Select the jet with index " <<  ind1 << " as first untagged jet...csv=" << jets_csv[ind1] <<  endl;

                            for(unsigned int uj2 = 0; uj2<buntag_indices.size(); uj2++) {

                                if( buntag_indices[uj2]==ind1 ) continue;

                                float WMass12 = (jets_p4[ ind1 ]+jets_p4[ buntag_indices[uj2] ]).M();
                                if( TMath::Abs(WMass12-MW)<minDiff ) {
                                    minDiff = TMath::Abs(WMass12-MW);
                                    ind2 = buntag_indices[uj2];
                                }

                            }
                        }

                        // if 6 btag jets found, we choose to treat the 5th and 6th as untagged jet (is a c/s-quark ?)
                        else if( buntag_indices_favorite.size()==2 ) {
                            ind1 =  buntag_indices[ buntag_indices_favorite[0] ];
                            ind2 =  buntag_indices[ buntag_indices_favorite[1] ];
                            if( debug>=1 )
                                cout << "Select the jet(s) with index(es) " <<  ind1 << "," << ind2 << " as untagged jets...csv=" << jets_csv[ind1] << "," << jets_csv[ind2] <<  endl;

                        }

                        // else just choose those w/ mass closest to MW
                        else {

                            for(unsigned int uj1 = 0; uj1<buntag_indices.size()-1; uj1++) {
                                for(unsigned int uj2 = uj1+1; uj2<buntag_indices.size(); uj2++) {

                                    float WMass12 = (jets_p4[ buntag_indices[uj1] ]+jets_p4[ buntag_indices[uj2] ]).M();
                                    if( TMath::Abs(WMass12-MW)<minDiff ) {
                                        minDiff = TMath::Abs(WMass12-MW);
                                        ind1 = buntag_indices[uj1];
                                        ind2 = buntag_indices[uj2];
                                    }

                                }
                            }
                        }

                        // keep record of those indices not selected
                        for(unsigned int ext = 0 ; ext < buntag_indices.size() ; ext++) {
                            if( buntag_indices[ext]!=ind1 && buntag_indices[ext]!=ind2 )
                                buntag_indices_extra.push_back( buntag_indices[ext] );
                        }
                        if( debug>=1 ) {
                            cout << "A total of " << buntag_indices_extra.size() << " extra indices cached:" << endl;
                            for(unsigned int ext = 0 ; ext < buntag_indices_extra.size() ; ext++) {
                                cout << " >> " << buntag_indices_extra[ext] << endl;
                            }
                        }


                        /////////////////////////////////////////////////////
                        type_       =  3;
                        nPermut_    = 12;
                        nPermut_alt_= 12;
                        meIntegrator->setIntType( MEIntegratorNew::SL2wj );
                        /////////////////////////////////////////////////////

                        if( testSLw1jType3 ) {

                            if( debug>=1 ) cout << "We will use the option of re-interpreting this event..." << endl;

                            // make sure we don't exceed the maximum array size
                            nMaxJetsSLw1jType3 = TMath::Min(nMaxJetsSLw1jType3, NMAXJETSSLW1JTYPE3);

                            float WMass =  (jets_p4[ ind1 ]+jets_p4[ ind2 ]).M() ;
                            if( WMass>MwLType3 && WMass<MwHType3 ) {
                                flag_type3_ = 1;

                                if( debug>=1 ) {
                                    cout << " > this event (originally type3) will be interpreted as type3, because W mass=" << WMass << " GeV..." << endl;
                                    cout << "   => total # of permutations = " << nPermut_ << endl;
                                }

                            }
                            else {

                                flag_type3_ = -1;

                                nPermut_    = 12*TMath::Min( int(buntag_indices_extra.size()+2), nMaxJetsSLw1jType3 );
                                nPermut_alt_= 12*TMath::Min( int(buntag_indices_extra.size()+2), nMaxJetsSLw1jType3 );
                                meIntegrator->setIntType( MEIntegratorNew::SL1wj );

                                if( debug>=1 ) {
                                    cout << " > this event (originally type3) will be re-interpreted as type1, because W mass=" << WMass << " GeV..." << endl;
                                    cout << "   => total # of permutations = " << nPermut_ << endl;
                                }

                            }
                        }



                    }
                    else if( analyze_type6 || analyze_type6_BTag ) {

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "Processing event # " << counter << " (TYPE 6)." << " Event ID " << EVENT.event << endl;

                        /////////////////////////////////////////////////////
                        type_       =  6;
                        nPermut_    = 12;
                        nPermut_alt_= 12;
                        meIntegrator->setIntType( MEIntegratorNew::DL );
                        /////////////////////////////////////////////////////

                    }
                    else if( analyze_type7 ) {

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "Processing event # " << counter << " (TYPE 7)." << " Event ID " << EVENT.event << endl;

                        /////////////////////////////////////////////////////
                        type_       =  7;
                        nPermut_    = 12;
                        nPermut_alt_= 12;
                        meIntegrator->setIntType( MEIntegratorNew::DL );
                        /////////////////////////////////////////////////////

                    }
                    else {
                        cout << "Inconsistency in the analysis... continue." << endl;
                        cout << " => go to next event!" << endl;
                        cout << "******************************" << endl;
                        continue;
                    }


                    // sanity-check
                    if(type_>=0 && type_<=3 && (ind1==999 || ind2==999)) {
                        cout << "Inconsistency found: ind1 or ind2 are not set...continue." << endl;
                        cout << " => go to next event!" << endl;
                        cout << "******************************" << endl;
                        continue;
                    }

                    // DEBUG
                    if(debug>=1) {
                        cout << "*** Event ID " << EVENT.event << " *** systematics: " << syst_ << endl;
                        cout << " ==> SL=" << int(properEventSL) << ", DL=" << properEventDL << endl;
                        cout << "     NJets " << numJets_ << " (" << numBTagM_ << " tagged)" << endl;
                        if(useRegression)
                            cout <<  "     !!! The b-tagged jets will undergo energy regression !!!" << endl;
                        cout << "     b-tagged: " << endl;
                        for( unsigned int jj = 0; jj<btag_indices_backup.size(); jj++) {
                            cout << "     ("
                                 << jets_p4[ btag_indices_backup[jj] ].Pt() << ","
                                 << jets_p4[ btag_indices_backup[jj] ].Eta() << ","
                                 << jets_p4[ btag_indices_backup[jj] ].Phi() << ","
                                 << jets_p4[ btag_indices_backup[jj] ].M() << "), CSV= "
                                 << jets_csv[btag_indices_backup[jj] ] << endl;
                            if( useRegression )
                                cout   << "R -> ("
                                       << jets_p4_reg[ btag_indices_backup[jj] ].Pt() << ","
                                       << jets_p4_reg[ btag_indices_backup[jj] ].Eta() << ","
                                       << jets_p4_reg[ btag_indices_backup[jj] ].Phi() << ","
                                       << jets_p4_reg[ btag_indices_backup[jj] ].M() << ")" << endl;
                        }
                        cout << "     b-untagged: " << endl;
                        for( unsigned int jj = 0; jj<buntag_indices_backup.size(); jj++)
                            cout << "     ("
                                 << jets_p4[ buntag_indices_backup[jj] ].Pt() << ","
                                 << jets_p4[ buntag_indices_backup[jj] ].Eta() << ","
                                 << jets_p4[ buntag_indices_backup[jj] ].Phi() << ","
                                 << jets_p4[ buntag_indices_backup[jj] ].M() << "), CSV= "
                                 << jets_csv[buntag_indices_backup[jj] ] << endl;
                        cout << "     btag probability is " << btag_LR_ << endl;

                        if(passes_btagshape && selectByBTagShape) {
                            cout << "     @@@@@ the jet collection has been re-ordered according to btag probability @@@@@@" << endl;
                            cout << "     b-tagged: " << endl;
                            for( unsigned int jj = 0; jj < btag_indices.size(); jj++) {
                                cout << "     (" << jets_p4[ btag_indices[jj] ].Pt() << "," << jets_p4[ btag_indices[jj] ].Eta() << ","
                                     << jets_p4[ btag_indices[jj] ].Phi() << "," << jets_p4[ btag_indices[jj] ].M() << "), CSV= " << jets_csv[ btag_indices[jj] ] << endl;
                                if( useRegression )
                                    cout << "R -> (" << jets_p4_reg[ btag_indices[jj] ].Pt() << "," << jets_p4_reg[ btag_indices[jj] ].Eta() << ","
                                         << jets_p4_reg[ btag_indices[jj] ].Phi() << "," << jets_p4_reg[ btag_indices[jj] ].M() << "), CSV= " << jets_csv[ btag_indices[jj] ] << endl;
                            }
                            cout << "     b-untagged: " << endl;
                            for( unsigned int jj = 0; jj<buntag_indices.size(); jj++)
                                cout << "     (" << jets_p4[ buntag_indices[jj] ].Pt() << "," << jets_p4[ buntag_indices[jj] ].Eta() << ","
                                     << jets_p4[ buntag_indices[jj] ].Phi() << "," << jets_p4[ buntag_indices[jj] ].M() << "), CSV= " << jets_csv[buntag_indices[jj] ] << endl;
                        }

                    }



                    // total number of integrations
                    nTotInteg_      = nPermut_    * nMassPoints_;
                    nTotInteg_alt_  = nPermut_alt_* nMassPoints_;


                    // setup jet collection
                    jets.clear();
                    jets.push_back( leptonLV     );
                    jets.push_back( neutrinoLV   );

                    // keep track of an alternative jet selection when doing regression
                    jets_alt.clear();
                    jets_alt.push_back( leptonLV   );
                    jets_alt.push_back( neutrinoLV );

                    // b1,...,w1,w2 are indices for jets_p4 collection;
                    // This is a map between the internal ordering bLep=2, W1Had=3, ..., higgs2 = 7, and jets_p4
                    pos_to_index.clear();

                    if( type_==-3) {
                        jets.push_back( jets_p4[ banytag_indices[0] ]);
                        jets.push_back( leptonLV2    );
                        jets.push_back( neutrinoLV   );       // dummy
                        jets.push_back( jets_p4[ banytag_indices[1] ]);
                        jets.push_back( jets_p4[ banytag_indices[2] ]);
                        jets.push_back( jets_p4[ banytag_indices[3] ]);

                        pos_to_index[2] = banytag_indices[0];
                        pos_to_index[3] = banytag_indices[0]; // dummy
                        pos_to_index[4] = banytag_indices[0]; // dummy
                        pos_to_index[5] = banytag_indices[1];
                        pos_to_index[6] = banytag_indices[2];
                        pos_to_index[7] = banytag_indices[3];
                    }
                    else if( type_==-2) {
                        jets.push_back( jets_p4[ banytag_indices[0] ]);
                        jets.push_back( jets_p4[ banytag_indices[1] ]);
                        jets.push_back( jets_p4[ banytag_indices[2] ]);
                        jets.push_back( jets_p4[ banytag_indices[3] ]);
                        jets.push_back( jets_p4[ banytag_indices[4] ]);
                        jets.push_back( jets_p4[ banytag_indices[5] ]);

                        pos_to_index[2] = banytag_indices[0];
                        pos_to_index[3] = banytag_indices[1];
                        pos_to_index[4] = banytag_indices[2];
                        pos_to_index[5] = banytag_indices[3];
                        pos_to_index[6] = banytag_indices[4];
                        pos_to_index[7] = banytag_indices[5];
                    }
                    else if( type_==-1) {
                        jets.push_back( jets_p4[ banytag_indices[0] ]);
                        jets.push_back( jets_p4[ banytag_indices[1] ]);
                        jets.push_back( jets_p4[ banytag_indices[1] ]); // dummy
                        jets.push_back( jets_p4[ banytag_indices[2] ]);
                        jets.push_back( jets_p4[ banytag_indices[3] ]);
                        jets.push_back( jets_p4[ banytag_indices[4] ]);

                        pos_to_index[2] = banytag_indices[0];
                        pos_to_index[3] = banytag_indices[1];
                        pos_to_index[4] = banytag_indices[1];           // dummy
                        pos_to_index[5] = banytag_indices[2];
                        pos_to_index[6] = banytag_indices[3];
                        pos_to_index[7] = banytag_indices[4];
                    }
                    else if( type_<=3 && type_>=0) {
                        jets.push_back( !useRegression ? jets_p4[ btag_indices[0] ] : jets_p4_reg[ btag_indices[0] ]  );
                        jets.push_back( jets_p4[ ind1 ]);
                        jets.push_back( jets_p4[ ind2 ]);
                        jets.push_back( !useRegression ? jets_p4[ btag_indices[1] ] : jets_p4_reg[ btag_indices[1] ] );
                        jets.push_back( !useRegression ? jets_p4[ btag_indices[2] ] : jets_p4_reg[ btag_indices[2] ] );
                        jets.push_back( !useRegression ? jets_p4[ btag_indices[3] ] : jets_p4_reg[ btag_indices[3] ] );

                        jets_alt.push_back( useRegression ? jets_p4[ btag_indices[0] ] : jets_p4_reg[ btag_indices[0] ]  );
                        jets_alt.push_back( jets_p4[ ind1 ]);
                        jets_alt.push_back( jets_p4[ ind2 ]);
                        jets_alt.push_back( useRegression ? jets_p4[ btag_indices[1] ] : jets_p4_reg[ btag_indices[1] ] );
                        jets_alt.push_back( useRegression ? jets_p4[ btag_indices[2] ] : jets_p4_reg[ btag_indices[2] ] );
                        jets_alt.push_back( useRegression ? jets_p4[ btag_indices[3] ] : jets_p4_reg[ btag_indices[3] ] );

                        pos_to_index[2] = btag_indices[0];
                        pos_to_index[3] = ind1;
                        pos_to_index[4] = ind2;
                        pos_to_index[5] = btag_indices[1];
                        pos_to_index[6] = btag_indices[2];
                        pos_to_index[7] = btag_indices[3];

                    }
                    else if( type_==6 ) {
                        jets.push_back( !useRegression ? jets_p4[ btag_indices[0] ] : jets_p4_reg[ btag_indices[0] ] );
                        jets.push_back( leptonLV2   );
                        jets.push_back( neutrinoLV  );      // dummy
                        jets.push_back( !useRegression ? jets_p4[ btag_indices[1] ] : jets_p4_reg[ btag_indices[1] ]);
                        jets.push_back( !useRegression ? jets_p4[ btag_indices[2] ] : jets_p4_reg[ btag_indices[2] ]);
                        jets.push_back( !useRegression ? jets_p4[ btag_indices[3] ] : jets_p4_reg[ btag_indices[3] ]);

                        jets_alt.push_back( useRegression ? jets_p4[ btag_indices[0] ] : jets_p4_reg[ btag_indices[0] ] );
                        jets_alt.push_back( leptonLV2   );
                        jets_alt.push_back( neutrinoLV  );      // dummy
                        jets_alt.push_back( useRegression ? jets_p4[ btag_indices[1] ] : jets_p4_reg[ btag_indices[1] ]);
                        jets_alt.push_back( useRegression ? jets_p4[ btag_indices[2] ] : jets_p4_reg[ btag_indices[2] ]);
                        jets_alt.push_back( useRegression ? jets_p4[ btag_indices[3] ] : jets_p4_reg[ btag_indices[3] ]);

                        pos_to_index[2] = btag_indices[0];
                        pos_to_index[3] = btag_indices[0];  // dummy
                        pos_to_index[4] = btag_indices[0];  // dummy
                        pos_to_index[5] = btag_indices[1];
                        pos_to_index[6] = btag_indices[2];
                        pos_to_index[7] = btag_indices[3];
                    }
                    else if( type_==7 ) {
                        jets.push_back( !useRegression ? jets_p4[ btagLoose_indices[0] ] : jets_p4_reg[ btagLoose_indices[0] ] );
                        jets.push_back( leptonLV2   );
                        jets.push_back( neutrinoLV  );           // dummy
                        jets.push_back( !useRegression ? jets_p4[ btagLoose_indices[1] ] : jets_p4_reg[ btagLoose_indices[1] ]);
                        jets.push_back( !useRegression ? jets_p4[ btagLoose_indices[2] ] : jets_p4_reg[ btagLoose_indices[2] ]);
                        jets.push_back( !useRegression ? jets_p4[ btagLoose_indices[3] ] : jets_p4_reg[ btagLoose_indices[3] ]);

                        jets_alt.push_back( useRegression ? jets_p4[ btagLoose_indices[0] ] : jets_p4_reg[ btagLoose_indices[0] ] );
                        jets_alt.push_back( leptonLV2   );
                        jets_alt.push_back( neutrinoLV  );           // dummy
                        jets_alt.push_back( useRegression ? jets_p4[ btagLoose_indices[1] ] : jets_p4_reg[ btagLoose_indices[1] ]);
                        jets_alt.push_back( useRegression ? jets_p4[ btagLoose_indices[2] ] : jets_p4_reg[ btagLoose_indices[2] ]);
                        jets_alt.push_back( useRegression ? jets_p4[ btagLoose_indices[3] ] : jets_p4_reg[ btagLoose_indices[3] ]);

                        pos_to_index[2] = btagLoose_indices[0];
                        pos_to_index[3] = btagLoose_indices[0];  // dummy
                        pos_to_index[4] = btagLoose_indices[0];  // dummy
                        pos_to_index[5] = btagLoose_indices[1];
                        pos_to_index[6] = btagLoose_indices[2];
                        pos_to_index[7] = btagLoose_indices[3];
                    }
                    else {
                        /* ... */
                    }

                    // save jet kinematics into the tree...
                    nJet_ = 8;
                    for(int q = 0; q < nJet_ ; q++ ) {
                        // kinematics
                        jet_pt_    [q] = jets[q].Pt() ;
                        jet_pt_alt_[q] = jets_alt[q].Pt();
                        jet_eta_   [q] = jets[q].Eta();
                        jet_phi_   [q] = jets[q].Phi();
                        jet_m_     [q] = jets[q].M();
                        jet_csv_   [q] = q>1 ? jets_csv[ pos_to_index[q] ] : -99.;
                    }

                    // set all prob. to 0.0;
                    for(int p = 0 ; p < nTotInteg_; p++) {
                        probAtSgn_permut_       [p] = 0.;
                        probAtSgnErr_permut_    [p] = 0.;
                        callsAtSgn_permut_      [p] = 0 ;
                        chi2AtSgn_permut_       [p] = 0.;
                    }
                    for(int p = 0 ; p < nPermut_; p++) {
                        probAtSgn_bb_permut_ [p] = 0.;
                    }
                    for(int p = 0 ; p < nTotInteg_alt_; p++) {
                        probAtSgn_alt_permut_   [p] = 0.;
                        probAtSgnErr_alt_permut_[p] = 0.;
                        callsAtSgn_alt_permut_  [p] = 0 ;
                        chi2AtSgn_alt_permut_   [p] = 0.;
                    }
                    for(int p = 0 ; p < nPermut_alt_; p++) {
                        probAtSgn_bj_permut_ [p] = 0.;
                        probAtSgn_cc_permut_ [p] = 0.;
                        probAtSgn_jj_permut_ [p] = 0.;
                    }

                    /////////////////////////////////////////////////////////////

                    // check if there is ***at least one*** tag-untag pair that satisfies the "cs-tag"
                    for( unsigned int w = 0; w<btag_indices.size(); w++) {

                        // this is needed if type>3
                        if(ind1==999 || ind2==999) continue;

                        float m1 = !useRegression ? ( jets_p4[btag_indices[w]] + jets_p4[ind1] ).M() : ( jets_p4_reg[btag_indices[w]] + jets_p4[ind1] ).M();
                        float m2 = !useRegression ? ( jets_p4[btag_indices[w]] + jets_p4[ind2] ).M() : ( jets_p4_reg[btag_indices[w]] + jets_p4[ind2] ).M();

                        if( flag_type0_<0 && ((m1>(MwL+5) && m1<(MwH-5)) || (m2>(MwL+5) && m2<(MwH-5))) && type_== 0 ) {
                            flag_type0_ = 0;
                            if( jets_csv[btag_indices[w]]<0.95 ) flag_type0_ = 1;
                            if( jets_csv[btag_indices[w]]<0.90 ) flag_type0_ = 2;
                            if( jets_csv[btag_indices[w]]<0.85 ) flag_type0_ = 3;
                            if( jets_csv[btag_indices[w]]<0.80 ) flag_type0_ = 4;
                        }
                        if( flag_type1_<0 && ((m1>(MwL+5) && m1<(MwH-5)) || (m2>(MwL+5) && m2<(MwH-5))) && type_== 1 ) {
                            flag_type1_ = 0;
                            if( jets_csv[btag_indices[w]]<0.95 ) flag_type1_ = 1;
                            if( jets_csv[btag_indices[w]]<0.90 ) flag_type1_ = 2;
                            if( jets_csv[btag_indices[w]]<0.85 ) flag_type1_ = 3;
                            if( jets_csv[btag_indices[w]]<0.80 ) flag_type1_ = 4;
                        }
                        if( flag_type2_<0 && ((m1>(MwL+5) && m1<(MwH-5)) || (m2>(MwL+5) && m2<(MwH-5))) && type_== 2 ) {
                            flag_type2_ = 0;
                            if( jets_csv[btag_indices[w]]<0.95 ) flag_type2_ = 1;
                            if( jets_csv[btag_indices[w]]<0.90 ) flag_type2_ = 2;
                            if( jets_csv[btag_indices[w]]<0.85 ) flag_type2_ = 3;
                            if( jets_csv[btag_indices[w]]<0.80 ) flag_type2_ = 4;
                        }
                    }

                    if(!testSLw1jType3) {
                        // for type 3, the W-tag is different...
                        float WMass = type_==3 ? (jets_p4[ ind1 ]+jets_p4[ ind2 ]).M() : -999.;
                        if( WMass>MwL && WMass<MwH )  flag_type3_ = 1;
                    }

                    /////////////////////////////////////////////////////////////

                    // init reco particles
                    meIntegrator->setJets(&jets);

                    // init MET stuff
                    meIntegrator->setSumEt( MET_sumEt_ );
                    meIntegrator->setMEtCov(-99,-99,0);

                    // specify if topLep has pdgid +6 or -6
                    meIntegrator->setTopFlags( vLepton_charge[0]==1 ? +1 : -1 , vLepton_charge[0]==1 ? -1 : +1 );

                    // if needed, switch off OL
                    if(switchoffOL) {
                        meIntegrator->switchOffOL();
                        cout << "*** Switching off OpenLoops to speed-up the calculation ***" << endl;
                    }

                    // start the clock...
                    clock->Start();

                    // loop over Higgs mass values...
                    for(int m = 0; m < nHiggsMassPoints ; m++) {
                        meIntegrator->setMass( mH[m] );

                        // loop over Top mass values...
                        for(int t = 0; t < nTopMassPoints ; t++) {
                            meIntegrator->setTopMass( mT[t] , MW );

                            // these are used for bookkeeping
                            double maxP_s = 0.;
                            double maxP_b = 0.;

                            // number of permutations for which p has been calculated
                            int num_s = 0;
                            int num_b = 0;

                            // loop over hypothesis [ TTH, TTbb ]
                            for(int hyp = 0 ; hyp<2;  hyp++) {

                                // choose which permutations to consider;
                                int* permutList = 0;
                                if     ( type_ == -3 ) permutList = hyp==0 ?  permutations_4J_S      : permutations_4J_B;
                                else if( type_ == -2 ) permutList = hyp==0 ?  permutations_6J_S      : permutations_6J_B;
                                else if( type_ == -1 ) permutList = hyp==0 ?  permutations_5J_S      : permutations_5J_B;
                                else if( type_ ==  0 ) permutList = hyp==0 ?  permutations_TYPE0_S   : permutations_TYPE0_B;
                                else if( type_ ==  1 ) permutList = hyp==0 ?  permutations_TYPE1_S   : permutations_TYPE1_B;
                                else if( type_ ==  2 ) permutList = hyp==0 ?  permutations_TYPE2_S   : permutations_TYPE2_B;
                                else if( type_ ==  3 ) permutList = hyp==0 ?  permutations_TYPE0_S   : permutations_TYPE0_B;
                                else if( type_ >=  6 ) permutList = hyp==0 ?  permutations_TYPE6_S   : permutations_TYPE6_B;
                                else {
                                    cout << "No permutations found...continue." << endl;
                                    continue;
                                }

                                if( testSLw1jType3 && type_==3 && flag_type3_<0) {
                                    permutList = hyp==0 ?  permutations_TYPE0_5EXTRA_S : permutations_TYPE0_5EXTRA_B;
                                }

                                // loop over permutations
                                for(unsigned int pos = 0; pos < (unsigned int)( hyp==0 ? nPermut_ : nPermut_alt_ ) ; pos++) {

                                    // try to recover these events
                                    if( testSLw1jType3 && type_==3 && flag_type3_<0 ) {

                                        if(buntag_indices_extra.size()<=0) {
                                            cout << "Inconsistency found in testSLw1jType3" << endl;
                                            continue;
                                        }

                                        if( pos<12 ) {
                                            jets[3]         = jets_p4[ ind1 ];
                                            jets_alt[3]     = jets_p4[ ind1 ];
                                            pos_to_index[3] = ind1;

                                            jets[4]         = jets_p4[ ind1 ];
                                            jets_alt[4]     = jets_p4[ ind1 ];
                                            pos_to_index[4] = ind1;
                                        }
                                        else if( pos>=11 && pos<24 ) {
                                            jets[3]         = jets_p4[ ind2 ];
                                            jets_alt[3]     = jets_p4[ ind2 ];
                                            pos_to_index[3] = ind2;

                                            jets[4]         = jets_p4[ ind2 ];
                                            jets_alt[4]     = jets_p4[ ind2 ];
                                            pos_to_index[4] = ind2;
                                        }
                                        else {

                                            int extra_jet_position = (pos-24)/12 ;

                                            jets[3]         = jets_p4[ buntag_indices_extra[extra_jet_position] ];
                                            jets_alt[3]     = jets_p4[ buntag_indices_extra[extra_jet_position] ];
                                            pos_to_index[3] = buntag_indices_extra[extra_jet_position];

                                            jets[4]         = jets_p4[ buntag_indices_extra[extra_jet_position] ];
                                            jets_alt[4]     = jets_p4[ buntag_indices_extra[extra_jet_position] ];
                                            pos_to_index[4] = buntag_indices_extra[extra_jet_position];
                                        }

                                        // update...
                                        meIntegrator->setJets(&jets);

                                    }

                                    // consider permutation #pos & save permutation-to-jet mas into the tree...
                                    meIntegrator->initVersors( permutList[pos] );
                                    if( hyp==0 ) perm_to_jet_    [pos] =  permutList[pos];
                                    if( hyp==1 ) perm_to_jet_alt_[pos] =  permutList[pos];

                                    // index of the four jets associated to b-quarks or W->qq
                                    int bLep_pos = (permutList[pos])%1000000/100000;
                                    int w1_pos   = (permutList[pos])%100000/10000;
                                    int w2_pos   = (permutList[pos])%10000/1000;
                                    int bHad_pos = (permutList[pos])%1000/100;
                                    int b1_pos   = (permutList[pos])%100/10;
                                    int b2_pos   = (permutList[pos])%10/1;

                                    // the barcode for this permutation
                                    string barcode = Form("%d%d_%d_%d%d%d_%d%d%d_%d%d",
                                                          type_, meIntegrator->getIntType(), hyp, lep_index[0], 0, jets_index[ pos_to_index[bLep_pos] ],
                                                          type_<6 ? jets_index[ pos_to_index[w1_pos] ] : lep_index[1], type_<6 ? jets_index[ pos_to_index[w2_pos] ] : 0, jets_index[ pos_to_index[bHad_pos] ],
                                                          jets_index[ pos_to_index[b1_pos] ], jets_index[ pos_to_index[b2_pos] ]);
                                    PhaseSpacePoint PSP;
                                    PSP.fill( jets );


                                    // find if this particular permutation matches the expectation
                                    int bLep_match = 0;
                                    if(TMath::Abs(TOPLEPB.Py())>0 && deltaR( jets_p4[ pos_to_index[bLep_pos] ], TOPLEPB ) < GENJETDR) {
                                        bLep_match = 1;
                                    }
                                    int w1_match = 0;
                                    int w2_match = 0;
                                    if( (TMath::Abs(TOPHADW1.Py())>0 && deltaR( jets_p4[ pos_to_index[w1_pos] ], TOPHADW1 ) < GENJETDR) ||
                                            (TMath::Abs(TOPHADW2.Py())>0 && deltaR( jets_p4[ pos_to_index[w1_pos] ], TOPHADW2 ) < GENJETDR)) {
                                        w1_match = 1;
                                    }
                                    if( (TMath::Abs(TOPHADW1.Py())>0 && deltaR( jets_p4[ pos_to_index[w2_pos] ], TOPHADW1 ) < GENJETDR) ||
                                            (TMath::Abs(TOPHADW2.Py())>0 && deltaR( jets_p4[ pos_to_index[w2_pos] ], TOPHADW2 ) < GENJETDR)) {
                                        w2_match = 1;
                                    }
                                    int bHad_match = 0;
                                    if(TMath::Abs(TOPHADB.Py())>0 && deltaR( jets_p4[ pos_to_index[bHad_pos] ], TOPHADB ) < GENJETDR) {
                                        bHad_match = 1;
                                    }
                                    int b1_match = 0;
                                    int b2_match = 0;
                                    if( (TMath::Abs(HIGGSB1.Py())>0 && deltaR( jets_p4[ pos_to_index[b1_pos] ], HIGGSB1 ) < GENJETDR) ||
                                            (TMath::Abs(HIGGSB2.Py())>0 && deltaR( jets_p4[ pos_to_index[b1_pos] ], HIGGSB2 ) < GENJETDR)) {
                                        b1_match = 1;
                                    }
                                    if( (TMath::Abs(HIGGSB1.Py())>0 && deltaR( jets_p4[ pos_to_index[b2_pos] ], HIGGSB1 ) < GENJETDR) ||
                                            (TMath::Abs(HIGGSB2.Py())>0 && deltaR( jets_p4[ pos_to_index[b2_pos] ], HIGGSB2 ) < GENJETDR)) {
                                        b2_match = 1;
                                    }

                                    // save an integer with this convention:
                                    //  > 1st digit = 1/0 if bLep candidate is correct/wrong
                                    //  > 2nd digit = 1/0 if matched/not matched to W-quark
                                    //  > ...
                                    if( hyp==0 ) perm_to_gen_    [pos] = 100000*bLep_match + 10000*w1_match + 1000*w2_match + 100*bHad_match + 10*b1_match + 1*b2_match;
                                    if( hyp==1 ) perm_to_gen_alt_[pos] = 100000*bLep_match + 10000*w1_match + 1000*w2_match + 100*bHad_match + 10*b1_match + 1*b2_match;

                                    // Higgs and top candidate masses, matched to gen (for illustrating b-regression performance)
                                    if( b1_match && b2_match ) {
                                        if(!useRegression)
                                            mH_matched_ = (jets_p4[pos_to_index[b1_pos]] + jets_p4[pos_to_index[b2_pos]]).M();
                                        else
                                            mH_matched_ = (jets_p4_reg[pos_to_index[b1_pos]] + jets_p4_reg[pos_to_index[b2_pos]]).M();
                                        if(debug>=2)
                                            std::cout<<"Higgs mass (matched to gen) = "<<mH_matched_<<std::endl;
                                    }

                                    if(w1_match && w2_match) {

                                        if(bHad_match) {
                                            if(!useRegression)
                                                mTop_matched_ = (jets_p4[pos_to_index[bHad_pos]] +  jets_p4[pos_to_index[w1_pos]] + jets_p4[pos_to_index[w2_pos]]).M();
                                            else
                                                mTop_matched_ = (jets_p4_reg[pos_to_index[bHad_pos]] +  jets_p4[pos_to_index[w1_pos]] + jets_p4[pos_to_index[w2_pos]]).M();
                                        }

                                        mW_matched_ = (jets_p4[pos_to_index[w1_pos]] + jets_p4[pos_to_index[w2_pos]]).M();

                                        if(debug>=2) {
                                            std::cout<<"Hadronic W mass   (matched to gen)= " << mW_matched_ << std::endl;
                                            std::cout<<"Hadronic top mass (matched to gen)= " << mTop_matched_ << std::endl;
                                        }
                                    }

                                    // check invariant mass of jet system:
                                    double mass, massLow, massHigh;
                                    bool skip        = !( meIntegrator->compatibilityCheck    (0.95, /*print*/ 0, mass, massLow, massHigh ) );
                                    bool skip_WHad   = false;
                                    bool skip_TopHad = false;
                                    if( type_==0 || type_==3 ) {
                                        skip_WHad   = !( meIntegrator->compatibilityCheck_WHad  (0.98, /*print*/ 0, mass, massLow, massHigh ) );
                                        skip_TopHad = !( meIntegrator->compatibilityCheck_TopHad(0.98, /*print*/ 0, mass, massLow, massHigh ) );
                                    }

                                    // remove skip optimization
                                    if( integralOption1==0 ) {
                                        skip        = false;
                                        skip_WHad   = false;
                                        skip_TopHad = false;
                                    }

                                    // if use btag, determine the b-tag probability density
                                    if( useBtag ) {
                                        double p_b_bLep =  jets_csv_prob_b[ pos_to_index[bLep_pos] ];
                                        double p_b_bHad =  jets_csv_prob_b[ pos_to_index[bHad_pos] ];
                                        double p_b_b1   =  jets_csv_prob_b[ pos_to_index[b1_pos] ];
                                        double p_c_b1   =  jets_csv_prob_c[ pos_to_index[b1_pos] ];
                                        double p_j_b1   =  jets_csv_prob_j[ pos_to_index[b1_pos] ];
                                        double p_b_b2   =  jets_csv_prob_b[ pos_to_index[b2_pos] ];
                                        double p_c_b2   =  jets_csv_prob_c[ pos_to_index[b2_pos] ];
                                        double p_j_b2   =  jets_csv_prob_j[ pos_to_index[b2_pos] ];
                                        double p_j_w1   =  1.0;
                                        double p_j_w2   =  1.0;

                                        // the b-tag probability for the two untagged jets...
                                        if( type_==0 || type_==3 || type_==-2) {
                                            p_j_w1 = jets_csv_prob_j[ pos_to_index[w1_pos] ];
                                            p_j_w2 = jets_csv_prob_j[ pos_to_index[w2_pos] ];
                                        }
                                        // the b-tag probability for the one untagged jet...
                                        else if( type_==1 || type_==2 || type_==-1) {
                                            p_j_w1 = jets_csv_prob_j[ pos_to_index[w1_pos] ];
                                            p_j_w2 = 1.0;
                                        }
                                        // there are untagged jets...
                                        else {
                                            p_j_w1 = 1.0;
                                            p_j_w2 = 1.0;
                                        }

                                        // DEBUG
                                        if( debug >= 3 ) {
                                            cout << "Hyp=" << hyp <<"  [BTag M="   << numBTagM_ << "]" << endl;
                                            cout << " bLep: p_b("   << jets_csv[pos_to_index[bLep_pos]] << ")=" << p_b_bLep;
                                            cout << " bHad: p_b("   << jets_csv[pos_to_index[bHad_pos]] << ")=" << p_b_bHad;
                                            cout << " b1  : p_b("   << jets_csv[pos_to_index[b1_pos]]   << ")=" << p_b_b1;
                                            cout << " b2  : p_b("   << jets_csv[pos_to_index[b2_pos]]   << ")=" << p_b_b2;
                                            if(!(type_>=6 || type_==-3))
                                                cout << " w1  : p_j(" << jets_csv[pos_to_index[w1_pos]]   << ")=" << p_j_w1;
                                            if(!(type_>=6 || type_==-3 || type_==1 || type_==2))
                                                cout << " w2  : p_j(" << jets_csv[pos_to_index[w2_pos]]   << ")=" << p_j_w2 << endl;
                                            cout << " P = "         <<  (p_b_bLep * p_b_bHad * p_b_b1 * p_b_b2 * p_j_w1 * p_j_w2) << endl;
                                        }

                                        // fill arrays with per-permutation probability
                                        if(hyp==0) {
                                            probAtSgn_bb_permut_[pos] =  p_b_bLep * p_b_bHad * p_b_b1 * p_b_b2 * p_j_w1 * p_j_w2;
                                        }
                                        if(hyp==1) {
                                            probAtSgn_bj_permut_[pos] =  p_b_bLep * p_b_bHad * (p_b_b1 * p_j_b2 + p_j_b1 * p_b_b2 )*0.5 * p_j_w1 * p_j_w2;
                                            probAtSgn_cc_permut_[pos] =  p_b_bLep * p_b_bHad * p_c_b1 * p_c_b2 * p_j_w1 * p_j_w2;
                                            probAtSgn_jj_permut_[pos] =  p_b_bLep * p_b_bHad * p_j_b1 * p_j_b2 * p_j_w1 * p_j_w2;
                                        }

                                    }

                                    // if doing scan over b-tag only, don't need amplitude...
                                    if( type_<0  ) continue;


                                    // if type 0/3 and incompatible with MW or MT (and we are not scanning vs MT) continue
                                    // ( this applies to both hypotheses )
                                    if( nTopMassPoints==1 && (skip_WHad || skip_TopHad) ) {
                                        if(print) cout << "Skip (THad check failed)...          Perm. #" << pos << endl;
                                        continue;
                                    }

                                    // retrieve integration boundaries from meIntegrator
                                    pair<double, double> range_x0 = (meIntegrator->getW1JetEnergyCI(0.95));
                                    pair<double, double> range_x1 =  make_pair(-1,1);
                                    pair<double, double> range_x2 =  make_pair(-PI,PI);
                                    pair<double, double> range_x3 =  make_pair(-1,1);
                                    pair<double, double> range_x4 =  useMET ? (meIntegrator->getNuPhiCI(0.95)) : make_pair(-PI,PI);
                                    pair<double, double> range_x5 = (meIntegrator->getB1EnergyCI(0.95));
                                    pair<double, double> range_x6 = (meIntegrator->getB2EnergyCI(0.95));

                                    // boundaries
                                    double x0L = range_x0.first;
                                    double x0U = range_x0.second;
                                    double x1L = range_x1.first;
                                    double x1U = range_x1.second;
                                    double x2L = range_x2.first;
                                    double x2U = range_x2.second;
                                    double x3L = range_x3.first;
                                    double x3U = range_x3.second;
                                    double x4L = range_x4.first;
                                    double x4U = range_x4.second;
                                    double x5L = range_x5.first;
                                    double x5U = range_x5.second;
                                    double x6L = range_x6.first;
                                    double x6U = range_x6.second;

                                    // these hold for the sgn integration and type0...
                                    double xLmode0_s[4] = {x0L, x3L, x4L, x5L};
                                    double xUmode0_s[4] = {x0U, x3U, x4U, x5U};
                                    // these hold for the bkg integration and type0...
                                    double xLmode0_b[5] = {x0L, x3L, x4L, x5L, x6L};
                                    double xUmode0_b[5] = {x0U, x3U, x4U, x5U, x6U};

                                    // these hold for the sgn integration and type1...
                                    double xLmode1_s[6] = {x0L, x1L, x2L, x3L, x4L, x5L};
                                    double xUmode1_s[6] = {x0U, x1U, x2U, x3U, x4U, x5U};
                                    // these hold for the bkg integration and type1...
                                    double xLmode1_b[7] = {x0L, x1L, x2L, x3L, x4L, x5L, x6L};
                                    double xUmode1_b[7] = {x0U, x1U, x2U, x3U, x4U, x5U, x6U};

                                    // these hold for the sgn integration and type2...
                                    double xLmode2_s[6] = {x0L, x1L, x2L, x3L, x4L, x5L};
                                    double xUmode2_s[6] = {x0U, x1U, x2U, x3U, x4U, x5U};
                                    // these hold for the bkg integration and type2...
                                    double xLmode2_b[7] = {x0L, x1L, x2L, x3L, x4L, x5L, x6L};
                                    double xUmode2_b[7] = {x0U, x1U, x2U, x3U, x4U, x5U, x6U};

                                    // these hold for the sgn integration and type3...
                                    double xLmode3_s[4] = {x0L, x3L, x4L, x5L};
                                    double xUmode3_s[4] = {x0U, x3U, x4U, x5U};
                                    // these hold for the bkg integration and type3...
                                    double xLmode3_b[5] = {x0L, x3L, x4L, x5L, x6L};
                                    double xUmode3_b[5] = {x0U, x3U, x4U, x5U, x6U};

                                    // these hold for the sgn integration and type6...
                                    double xLmode6_s[5] = {x1L, x2L, x1L, x2L, x5L};
                                    double xUmode6_s[5] = {x1U, x2U, x1U, x2U, x5U};
                                    // these hold for the bkg integration and type6...
                                    double xLmode6_b[6] = {x1L, x2L, x1L, x2L, x5L, x6L};
                                    double xUmode6_b[6] = {x1U, x2U, x1U, x2U, x5U, x6U};

                                    // these hold for the sgn integration and type7...
                                    double xLmode7_s[5] = {x1L, x2L, x1L, x2L, x5L};
                                    double xUmode7_s[5] = {x1U, x2U, x1U, x2U, x5U};
                                    // these hold for the bkg integration and type7...
                                    double xLmode7_b[6] = {x1L, x2L, x1L, x2L, x5L, x6L};
                                    double xUmode7_b[6] = {x1U, x2U, x1U, x2U, x5U, x6U};

                                    // number of integration variables (TTH hypothesis)
                                    int nParam;
                                    if     ( type_==0 )  nParam = 4; // Eq, eta_nu, phi_nu, Eb
                                    else if( type_==1 )  nParam = 6; // Eq, eta_q', phi_q', eta_nu, phi_nu, Eb
                                    else if( type_==2 )  nParam = 6; // Eq, eta_q', phi_q', eta_nu, phi_nu, Eb
                                    else if( type_==3 )  nParam = 4; // Eq, eta_nu, phi_nu, Eb
                                    else if( type_==6 )  nParam = 5; // eta_nu, phi_nu, eta_nu', phi_nu', Eb
                                    else if( type_==7 )  nParam = 5; // eta_nu, phi_nu, eta_nu', phi_nu', Eb
                                    else {
                                        cout << "No type match...contine." << endl;
                                        continue;
                                    }

                                    if( testSLw1jType3 && type_==3 && flag_type3_<0 ) {
                                        nParam = 6; // Eq, eta_q', phi_q', eta_nu, phi_nu, Eb
                                    }

                                    // per-permutation probability...
                                    double p     = 0.;

                                    // per-permutation probability error...
                                    double pErr  = 0.;

                                    // per-permutation chi2
                                    double chi2  = 0.;

                                    // if doing higgs mass scan, don't consider bkg hypo
                                    if( nHiggsMassPoints>1 && hyp==1 ) continue;

                                    // if doing top mass scan, don't consider sgn hypo
                                    if( nTopMassPoints>1 && hyp==0 ) continue;

                                    // if consider only one hypothesis (SoB=0)
                                    // and the current hypo is not the desired one, continue...
                                    if( SoB==0 && hyp!=hypo) continue;

                                    // if current hypo is TTH, but M(b1b2) incompatible with 125
                                    // (and we are not scanning vs MH) continue...
                                    if( hyp==0 && nHiggsMassPoints==1 && skip) {
                                        if(print) {
                                            cout << "Skip    hypo " << (hyp==0 ? "ttH " : "ttbb")
                                                 << " [MH=" << mH[m] << ", MT=" << mT[t]
                                                 << "] Perm. #" << pos;
                                            cout << " => p=" << p << endl;
                                        }
                                        continue;
                                    }

                                    // increment counters
                                    if(hyp==0) num_s++;
                                    if(hyp==1) num_b++;

                                    // if NOT doing top mass scan, and hyp==1
                                    // and no permutations for hyp==0 accepted, continue (the weight will be 0 anyway)
                                    if( nTopMassPoints==1 && hyp==1 && SoB==1 && num_s==0) {
                                        if(print) {
                                            cout << "Skip    hypo " << (hyp==0 ? "ttH " : "ttbb")
                                                 << " because no valid ttH permutations found" << endl;
                                        }
                                        continue;
                                    }

                                    // setup hypothesis
                                    if(print) {
                                        cout << "Testing hypo " << (hyp==0 ? "ttH " : "ttbb")
                                             << " [MH=" << mH[m] << ", MT=" << mT[t]
                                             << "] Perm. #" << pos;
                                    }
                                    meIntegrator->setHypo(hyp);

                                    // initial number of function calles
                                    int intPoints = 4000;
                                    if( type_==0 )  intPoints =  2000;
                                    if( type_==1 )  intPoints =  4000;
                                    if( type_==2 )  intPoints =  4000;
                                    if( type_==3 )  intPoints =  2000;
                                    if( type_==6 )  intPoints = 10000;
                                    if( type_==7 )  intPoints = 10000;

                                    if( testSLw1jType3 && type_==3 && flag_type3_<0 ) {
                                        intPoints =  4000;
                                    }


                                    // count how many time the integration is rerun per permutation
                                    int ntries = 0;
                                    // count number of Integral() calls
                                    int nCalls = 0;


                                    // skip ME calculation... for debugging
                                    if(speedup==0) {

                                        // setup # of parameters
                                        meIntegrator->SetPar( nParam+hyp );
                                        // integrand
                                        ROOT::Math::Functor toIntegrate(meIntegrator, &MEIntegratorNew::Eval, nParam+hyp);

                                        // first, check if the barcode is already there, and, in case, if it has the same PSP
                                        // ( <=> no need ro re-run, just use the already calculated values )
                                        bool need2Rerun = true;
                                        if( integralOption2==0 && perm_to_integral.find( barcode ) != perm_to_integral.end()) {

                                            need2Rerun = !isSamePSP( PSP, perm_to_phasespacepoint[barcode], 0.0001, 0.001 );
                                            if( !need2Rerun ) {
                                                p    = perm_to_integral      [barcode];
                                                pErr = perm_to_integralError [barcode];
                                                chi2 = perm_to_integralChi2  [barcode];
                                            }
                                        }

                                        // if run full VEGAS integration for the first time,
                                        // or run the optimized VEGAS integration, but the permutation is new...
                                        if( (integralOption2==0 && need2Rerun) ||
                                                ( integralOption2==1 && perm_to_integrator.find( barcode ) == perm_to_integrator.end() ) ) {

                                            // VEGAS integrator
                                            ROOT::Math::GSLMCIntegrator* ig2 = new ROOT::Math::GSLMCIntegrator( ROOT::Math::IntegrationMultiDim::kVEGAS , 1.e-12, 1.e-5, intPoints);
                                            ig2->SetFunction(toIntegrate);

                                            // refinement: redo integration if it returned a bad chi2
                                            while( ntries < MAX_REEVAL_TRIES) {

                                                ROOT::Math::IntegratorMultiDimOptions opts = ig2->Options();
                                                opts.SetNCalls( intPoints  );
                                                ig2->SetOptions( opts ) ;

                                                if ( debug>=2 ) {
                                                    // modufy the VEGAS parameters;
                                                    ROOT::Math::VegasParameters param( *(ig2->ExtraOptions()) );
                                                    ig2->SetParameters(param);

                                                    // print both...
                                                    cout << endl;
                                                    ig2->Options().Print(std::cout);
                                                    ig2->ExtraOptions()->Print(std::cout);
                                                }

                                                // one more call...
                                                nCalls++;

                                                // the integration ranges depend on hyp and type
                                                if     ( type_==0 ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode0_s, xUmode0_s) : ig2->Integral(xLmode0_b, xUmode0_b));
                                                }
                                                else if( type_==1 || (testSLw1jType3 && type_==3 && flag_type3_<0) ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode1_s, xUmode1_s) : ig2->Integral(xLmode1_b, xUmode1_b));
                                                }
                                                else if( type_==2 ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode2_s, xUmode2_s) : ig2->Integral(xLmode2_b, xUmode2_b));
                                                }
                                                else if( type_==3 ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode3_s, xUmode3_s) : ig2->Integral(xLmode3_b, xUmode3_b));
                                                }
                                                else if( type_==6 ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode6_s, xUmode6_s) : ig2->Integral(xLmode6_b, xUmode6_b));
                                                }
                                                else if( type_==7 ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode7_s, xUmode7_s) : ig2->Integral(xLmode7_b, xUmode7_b));
                                                }
                                                else {
                                                    nCalls--;
                                                }

                                                // chi2/ndof of the integration
                                                chi2 =  ig2->ChiSqr();

                                                // error from VEGAS
                                                pErr =  ig2->Error();

                                                // save the various integrators
                                                if( integralOption2==1 ) {
                                                    if( perm_to_integrator.find( barcode )!=perm_to_integrator.end() ) {
                                                        perm_to_integrator.erase     ( perm_to_integrator.find(barcode) );
                                                    }
                                                    perm_to_integrator     [barcode] = ig2;
                                                }

                                                // save the result...
                                                if( perm_to_phasespacepoint.find( barcode )!=perm_to_phasespacepoint.end() )
                                                    perm_to_phasespacepoint.erase( perm_to_phasespacepoint.find(barcode) );
                                                perm_to_phasespacepoint[barcode] = PSP;

                                                if( perm_to_integral.find( barcode )!=perm_to_integral.end() )
                                                    perm_to_integral.erase       ( perm_to_integral.find(barcode) );
                                                perm_to_integral       [barcode] = p;

                                                if( perm_to_integralError.find( barcode )!=perm_to_integralError.end() )
                                                    perm_to_integralError.erase( perm_to_integralError.find( barcode ) );
                                                perm_to_integralError [barcode] = pErr;

                                                if( perm_to_integralChi2.find( barcode )!=perm_to_integralChi2.end() )
                                                    perm_to_integralChi2.erase( perm_to_integralChi2.find( barcode ) );
                                                perm_to_integralChi2 [barcode] = chi2;

                                                // check if the actual permutation returned a small or large number...
                                                // if the value is less than 10% of the largest found that far, skip
                                                // the improvement
                                                if( hyp==0 ) {
                                                    if( p>maxP_s ) maxP_s = p;
                                                    else if( p<0.1*maxP_s) ntries = MAX_REEVAL_TRIES+1;
                                                }
                                                else {
                                                    if( p>maxP_b ) maxP_b = p;
                                                    else if( p<0.1*maxP_b) ntries = MAX_REEVAL_TRIES+1;
                                                }

                                                // if the chi2 is bad, increse # of points and repeat the integration
                                                if( integralOption0 && chi2 > maxChi2_ ) {
                                                    ntries++;
                                                    intPoints *= 1.5;
                                                }
                                                // otherwise, just go to the next permutation...
                                                else
                                                    ntries = MAX_REEVAL_TRIES+1;

                                            }

                                            // free the allocated memory
                                            if( integralOption2==0 ) delete ig2;

                                        }


                                        // re-run the integration using the last grid only
                                        // (optionally, change the VEGAS parameters)
                                        else if( integralOption2==1 && perm_to_integrator.find( barcode ) != perm_to_integrator.end()) {

                                            // check if the PSP are the same (all jets have the same magnitude within dE/E<1e-04 and direction dR<1e-03)
                                            bool isSamePoint =  isSamePSP( PSP, perm_to_phasespacepoint[barcode], 0.0001, 0.001 );

                                            // it is not the sdame point, then re-calculate the integration, but using the latest grid
                                            if( !isSamePoint ) {

                                                // change the options
                                                ROOT::Math::IntegratorMultiDimOptions opts = perm_to_integrator[barcode]->Options();
                                                opts.SetNCalls( int(intPoints*integralOption2_nevalfact) );
                                                perm_to_integrator[barcode]->SetOptions( opts ) ;
                                                perm_to_integrator[barcode]->SetAbsTolerance(1.e-12);
                                                perm_to_integrator[barcode]->SetRelTolerance(1.e-5);

                                                // change the VEGAS parameters
                                                ROOT::Math::VegasParameters param( *(perm_to_integrator[barcode]->ExtraOptions()) );
                                                param.iterations = integralOption2_niter;
                                                param.stage      = integralOption2_stage;
                                                perm_to_integrator[barcode]->SetParameters(param);

                                                // one more call...
                                                nCalls++;

                                                // re-run the integtarion
                                                if     ( type_==0 ) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode0_s, xUmode0_s) : perm_to_integrator[barcode]->Integral(xLmode0_b, xUmode0_b));
                                                }
                                                else if( type_==1 || (testSLw1jType3 && type_==3 && flag_type3_<0)) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode1_s, xUmode1_s) : perm_to_integrator[barcode]->Integral(xLmode1_b, xUmode1_b));
                                                }
                                                else if( type_==2 ) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode2_s, xUmode2_s) : perm_to_integrator[barcode]->Integral(xLmode2_b, xUmode2_b));
                                                }
                                                else if( type_==3 ) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode3_s, xUmode3_s) : perm_to_integrator[barcode]->Integral(xLmode3_b, xUmode3_b));
                                                }
                                                else if( type_==6 ) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode6_s, xUmode6_s) : perm_to_integrator[barcode]->Integral(xLmode6_b, xUmode6_b));
                                                }
                                                else if( type_==7 ) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode7_s, xUmode7_s) : perm_to_integrator[barcode]->Integral(xLmode7_b, xUmode7_b));
                                                }
                                                else {
                                                    nCalls--;
                                                }

                                            }

                                            // the point has already been calculated, just read the result...
                                            else p = perm_to_integral[barcode];


                                            chi2 =  perm_to_integrator[barcode]->ChiSqr();
                                            pErr =  perm_to_integrator[barcode]->Error();

                                        }

                                        else {
                                            /* ... */
                                        }


                                    }

                                    // can still be interested in b-tagging, so set p=1...
                                    else {
                                        p = 1.;
                                    }

                                    // to avoid problems
                                    if( TMath::IsNaN(p) )    p    = 0.;
                                    if( TMath::IsNaN(pErr) ) pErr = 0.;
                                    if(print) {
                                        cout << " => p  = (" << p << " +/- " << pErr << ")";
                                        if( integralOption2 ) {
                                            cout << ",   barcode: [" << barcode << "]" << endl;
                                        }
                                        else cout << endl;
                                    }

                                    /////////////////////////////////////////////////////////////

                                    if( useBtag ) {

                                        // total ME*btag probability for nominal MH and MT, sgn hypo
                                        if( hyp==0 && mH[m]<MH+1.5 && mH[m]>MH-1.5 && mT[t]<MT+1.5 && mT[t]>MT-1.5) {
                                            probAtSgn_ttbb_         += ( p * probAtSgn_bb_permut_[pos] );
                                        }

                                        // total ME*btag probability for nominal MH and MT, bkg hypo
                                        if( hyp==1 && mH[m]<MH+1.5 && mH[m]>MH-1.5 && mT[t]<MT+1.5 && mT[t]>MT-1.5) {
                                            probAtSgn_alt_ttbb_     += ( p * probAtSgn_bb_permut_[pos] );
                                            probAtSgn_alt_ttbj_     += ( p * probAtSgn_bj_permut_[pos] );
                                            probAtSgn_alt_ttcc_     += ( p * probAtSgn_cc_permut_[pos] );
                                            probAtSgn_alt_ttjj_     += ( p * probAtSgn_jj_permut_[pos] );
                                        }
                                    }

                                    /////////////////////////////////////////////////////////////

                                    // save TTH prob. per permutation AND mH
                                    if( hyp==0 && mT[t]<MT+1.5 && mT[t]>MT-1.5) {
                                        probAtSgn_permut_   [(unsigned int)(pos+m*nPermut_)] = p;
                                        probAtSgnErr_permut_[(unsigned int)(pos+m*nPermut_)] = pErr;
                                        callsAtSgn_permut_  [(unsigned int)(pos+m*nPermut_)] = nCalls;
                                        chi2AtSgn_permut_   [(unsigned int)(pos+m*nPermut_)] = chi2;
                                    }
                                    // save TTbb prob. per permutation AND mT
                                    if( hyp==1 && mH[m]<MH+1.5 && mH[m]>MH-1.5 ) {
                                        probAtSgn_alt_permut_   [(unsigned int)(pos+t*nPermut_alt_)] = p;
                                        probAtSgnErr_alt_permut_[(unsigned int)(pos+t*nPermut_alt_)] = pErr;
                                        callsAtSgn_alt_permut_  [(unsigned int)(pos+t*nPermut_alt_)] = nCalls;
                                        chi2AtSgn_alt_permut_   [(unsigned int)(pos+t*nPermut_alt_)] = chi2;
                                    }

                                    // total and per-permutation ME probability for nominal MH and MT
                                    if( mH[m]<MH+1.5 && mH[m]>MH-1.5 && mT[t]<MT+1.5 && mT[t]>MT-1.5) {
                                        if(hyp==0) {
                                            probAtSgn_     += p;
                                        }
                                        else {
                                            probAtSgn_alt_ += p;
                                        }
                                    }

                                    /////////////////////////////////////////////////////////////

                                }  // hypothesis
                            }  // permutations
                        }  // nTopMassPoints
                    }  // nHiggsMassPoints

                    // stop clock and reset
                    clock->Stop();
                    time_ = clock->CpuTime();
                    clock->Reset();

                    // this time is integrated over all hypotheses, permutations, and mass scan values
                    if(print) cout << "Done in " << time_ << " sec" << endl;
                }

                ///////////////////////////////////////////////////
                // ALL THE REST...                               //
                ///////////////////////////////////////////////////

                else {

                    if( enhanceMC ) {

                        bool retry =
                            ((analyze_type0      || analyze_type1      || analyze_type2      || analyze_type3      || analyze_type6 ) && numJets30BtagM<4 )  ||
                            (analyze_type7 && numJets30BtagM<3) ||
                            ((analyze_type0_BTag || analyze_type1_BTag || analyze_type2_BTag || analyze_type3_BTag || analyze_type6_BTag) && !passes_btagshape);

                        if(syst_ == 0 && retry && event_trials < max_n_trials && event_trials<NMAXEVENTRIALS) {
                            i--;
                            lock = 1;
                            event_trials++;
                            if( event_trials%10000==0 ) cout << "   >>> : " << event_trials << "th trial ---> btag_LR = " <<  btag_LR_  << ", numBtagM = " << numJets30BtagM << endl;
                            if(debug>=2) {
                                cout << "Enhance MC: stay with event " << i+1 << endl;
                                cout << "  - lock for systematics, # of trials = " <<  event_trials << "; btagLR = " << btag_LR_ << endl;
                            }
                            continue;
                        }
                        if( event_trials>=NMAXEVENTRIALS || event_trials>=max_n_trials) {
                            cout << "Failure after " << event_trials << " attempts... try with the next event :-(" << endl;
                            num_of_trials_ = event_trials;
                            event_trials   = 0;
                        }
                    }

                    // if save all events, fill the tree...
                    if(ntuplizeAll) {

                        if(debug>=3) {
                            for(unsigned int q = 0; q < jets_p4.size() ; q++) {
                                cout << jets_p4[q].Pt() << endl;
                            }
                        }

                        unsigned int jets_p4_ind = 0;

                        // save jet kinematics into the tree...
                        for(int q = 0; q < nJet_ ; q++ ) {

                            // fill elem 0th w/ lepton kinematics
                            if( q==0 ) {
                                jet_pt_    [q] = leptonLV.Pt();
                                jet_pt_alt_[q] = leptonLV.Pt();
                                jet_eta_   [q] = leptonLV.Eta();
                                jet_phi_   [q] = leptonLV.Phi();
                                jet_m_     [q] = leptonLV.M();
                                jet_csv_   [q] = -99.;
                            }

                            // fill elem 1st w/ MET kinematics
                            else if( q==1 ) {
                                jet_pt_    [q] = neutrinoLV.Pt();
                                jet_pt_alt_[q] = neutrinoLV.Pt();
                                jet_eta_   [q] = neutrinoLV.Eta();
                                jet_phi_   [q] = neutrinoLV.Phi();
                                jet_m_     [q] = neutrinoLV.M();
                                jet_csv_   [q] = -99.;
                            }

                            // fill other elems w/ the jet kinematics
                            else if( jets_p4_ind < jets_p4.size() && ( properEventSL || (properEventDL && !(q==3 || q==4)))   ) {
                                jet_pt_     [q] = !useRegression ? jets_p4[jets_p4_ind].Pt() : jets_p4_reg[jets_p4_ind].Pt();
                                jet_pt_alt_ [q] =  useRegression ? jets_p4[jets_p4_ind].Pt() : jets_p4_reg[jets_p4_ind].Pt();
                                jet_eta_    [q] = jets_p4 [jets_p4_ind].Eta();
                                jet_phi_    [q] = jets_p4 [jets_p4_ind].Phi();
                                jet_m_      [q] = jets_p4 [jets_p4_ind].M();
                                jet_csv_    [q] = jets_csv[jets_p4_ind];

                                jets_p4_ind++;
                            }

                            // if DL, fill elem 3rd w/ second lepton kinematics
                            else if( properEventDL && q==3 ) {
                                jet_pt_     [q] = leptonLV2.Pt();
                                jet_pt_alt_ [q] = leptonLV2.Pt();
                                jet_eta_    [q] = leptonLV2.Eta();
                                jet_phi_    [q] = leptonLV2.Phi();
                                jet_m_      [q] = leptonLV2.M();
                                jet_csv_    [q] = -99.;
                            }

                            //  if DL, fill elem 4th w/ MET kinematics
                            else if( properEventDL && q==4 ) {
                                jet_pt_    [q] = neutrinoLV.Pt();
                                jet_pt_alt_[q] = neutrinoLV.Pt();
                                jet_eta_   [q] = neutrinoLV.Eta();
                                jet_phi_   [q] = neutrinoLV.Phi();
                                jet_m_     [q] = neutrinoLV.M();
                                jet_csv_   [q] = -99.;
                            }

                            else {}

                        }

                        // fill the tree...
                        tree->Fill();
                    }

                    continue;
                }

                // fill the tree...
                tree->Fill();

            } // systematics

            if(debug>=2) cout << "@I" << endl;

            // clean the map
            int countGSL = 0;
            for( std::map<string, ROOT::Math::GSLMCIntegrator*>::iterator x = perm_to_integrator.begin() ;
                    x != perm_to_integrator.end() ; x++ ) {
                if( x->second ) {
                    countGSL++;
                    delete x->second;
                }
            }
            if(perm_to_integrator.size()>0 && print)
                cout << "Deleted " << countGSL << " GSLMCIntegrator(s)" << endl;

        } // nentries

        // this histogram keeps track of the fraction of analyzed events per sample
        hcounter->SetBinContent(1,float(events_)/nentries);
        hcounter->SetBinContent(2,nentries);

        if(debug>=2) cout << "@L" << endl;

    } // samples


    // close the CSV calibration files (if any)
    if( f_CSVwgt_HF!=0 ) {
        f_CSVwgt_HF->Close();
    }
    if( f_CSVwgt_LF!=0 ) {
        f_CSVwgt_LF->Close();
    }

    // close the trigger erro files (if any)
    if( triggerErrors ) {
        if(f_Vtype1_id)   f_Vtype1_id->Close();
        if(f_Vtype1L1_tr) f_Vtype1L1_tr->Close();
        if(f_Vtype1L2_tr) f_Vtype1L2_tr->Close();
        if(f_Vtype2_id)   f_Vtype2_id->Close();
        if(f_Vtype2_tr)   f_Vtype2_tr->Close();
        if(f_Vtype3_id)   f_Vtype3_id->Close();
        if(f_Vtype3_tr)   f_Vtype3_tr->Close();
    }

    // save the tree and the counting histo in the ROOT file
    fout_tmp->cd();
    hcounter->Write("",TObject::kOverwrite );
    hparam  ->Write("",TObject::kOverwrite );
    tree->Write("",TObject::kOverwrite );
    fout_tmp->Close();

    if(debug>=2) cout << "@M" << endl;

    // find out the total time needed for the job
    clock2->Stop();
    float totalTime = clock2->CpuTime();
    cout << "*******************" << endl;
    cout << "Job done in " << totalTime/60. << " min." << endl;

    // delete MEIntegrator and other allocated objects
    cout << "Delete meIntegrator..." << endl;
    delete meIntegrator;
    delete clock;
    delete clock2;
    if(ran!=0)       delete ran;
    if(jet_smear!=0) delete jet_smear;
    cout << "Finished!!!" << endl;
    cout << "*******************" << endl;

    // Done!!!
    return 0;
}
