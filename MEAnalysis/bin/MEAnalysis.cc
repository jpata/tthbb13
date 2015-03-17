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

//the input ttree specification
#include "TTH/TTHNtupleAnalyzer/interface/tth_tree.hh"

//the output ttree specification
#include "TTH/MEAnalysis/interface/METree.hh"

//the output ttree specification
#include "TTH/TTHNtupleAnalyzer/interface/HypoEnums.hh"

#define MU_MASS 0.106
#define ELE_MASS 0.005

// dR distance for reco-gen matching
#define GENJETDR  0.3

// maximum number of VEGAS evaluation
#define MAX_REEVAL_TRIES 3

// 3.141...
#define PI TMath::Pi()

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

class CutHistogram {

    private:
    const unsigned int enum_length;
    
    public:
    TH1D* h;
    
    enum Cuts {
        NOTYPEMATCH,
        H_MASS_SCAN_BKG,
        T_MASS_SCAN_SIG,
        ONE_HYPO_MISMATCH,
        TTH_MBB_INCOMPATIBLE,
        TTJETS_MBB_INCOMPATIBLE,
        LEPTONS,
        JETS,
        BTAGSHAPE,
        WMASS,
        ME,
        TYPELESSZERO,
        passes,
        unknown
    };

    CutHistogram(const std::string name) :
        enum_length((int)Cuts::unknown + 1),
        h(new TH1D(name.c_str(), name.c_str(), enum_length, 0, enum_length)) 
    {
        h->GetXaxis()->SetBinLabel(1, "NOTYPEMATCH");
        h->GetXaxis()->SetBinLabel(2, "H_MASS_SCAN_BKG");
        h->GetXaxis()->SetBinLabel(3, "T_MASS_SCAN_SIG");
        h->GetXaxis()->SetBinLabel(4, "ONE_HYPO_MISMATCH");
        h->GetXaxis()->SetBinLabel(5, "TTH_MBB_INCOMPATIBLE");
        h->GetXaxis()->SetBinLabel(6, "TTJETS_MBB_INCOMPATIBLE");
        h->GetXaxis()->SetBinLabel(7, "LEPTONS");
        h->GetXaxis()->SetBinLabel(8, "JETS");
        h->GetXaxis()->SetBinLabel(9, "BTAGSHAPE");
        h->GetXaxis()->SetBinLabel(10, "WMASS");
        h->GetXaxis()->SetBinLabel(11, "ME");
        h->GetXaxis()->SetBinLabel(12, "TYPELESSZERO");
        h->GetXaxis()->SetBinLabel(13, "passes");
        h->GetXaxis()->SetBinLabel(14, "unknown");
    }

    void fill(Cuts c) {
        h->Fill((int)c);
    }

    void print() {
        for (int i=1; i<=h->GetNbinsX(); i++) {
            std::cout << h->GetXaxis()->GetBinLabel(i) << " " << h->GetBinContent(i) << endl;
        }
    }
};

#define DO_BTAG_LR_TREE

#ifdef DO_BTAG_LR_TREE
#include "TTH/MEAnalysis/interface/btag_lr_tree.hh"
#endif

int main(int argc, const char* argv[])
{

    /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
    /* @@@@@@@@@@@@@@@@@@@@@@@@ FWLITE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */

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

    //const double lepPtLoose         ( in.getUntrackedParameter<double>  ("lepPtLoose", 20.));
    const double lepPtTight         ( in.getUntrackedParameter<double>  ("lepPtTight", 30.));
    const double muPtTight         ( in.getUntrackedParameter<double>  ("muPtTight", 30.));
    const double elPtTight         ( in.getUntrackedParameter<double>  ("elPtTight", 30.));
    //const double lepIsoLoose        ( in.getUntrackedParameter<double>  ("lepIsoLoose", 0.2));
    const double lepIsoTight        ( in.getUntrackedParameter<double>  ("lepIsoTight", 0.12));
    //const double elEta              ( in.getUntrackedParameter<double>  ("elEta",      2.5));
    //const double muEtaLoose         ( in.getUntrackedParameter<double>  ("muEtaLoose", 2.4));
    const double muEtaTight         ( in.getUntrackedParameter<double>  ("muEtaTight", 2.1));
   
    //configures if the following skims are applied
    const bool cutLeptons           ( in.getUntrackedParameter<bool>  ("cutLeptons", true));
    const bool cutJets              ( in.getUntrackedParameter<bool>  ("cutJets", true));
    const bool cutWMass             ( in.getUntrackedParameter<bool>  ("cutWMass", true));
    const bool cutBTagShape         ( in.getUntrackedParameter<bool>  ("cutBTagShape", true));

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

    //FIXME: what are these
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
    //FIXME: unused
    //const int   reject_pixel_misalign_evts ( in.getUntrackedParameter<int> ("reject_pixel_misalign_evts", 1));

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

    BTagLikelihood btag_lh_calc(fCP, csvName);

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

    if(useCSVcalibration) {
        SetUpCSVreweighting(path,f_CSVwgt_HF, f_CSVwgt_LF,
                            h_csv_wgt_hf, c_csv_wgt_hf, h_csv_wgt_lf ) ;
    }

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
    if( norm == 0) {
        meIntegrator->setWeightNorm( MEIntegratorNew::None );
    }
    else if( norm==1 ) {
        meIntegrator->setWeightNorm( MEIntegratorNew::xSec );
    }
    else if( norm==2 ) {
        meIntegrator->setWeightNorm( MEIntegratorNew::Acc );
    }
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

    meIntegrator->setSqrtS(13000.);

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
        if (print) {
            cout << "*** Switching off OpenLoops to speed-up the calculation ***" << endl;
        }
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
    cout << "Writing to " << outFileName << endl;
    TFile* fout_tmp = TFile::Open(outFileName.c_str(),"UPDATE");
    
    TNamed* config_dump = new TNamed("configdump", builder.dump().c_str());

    // total event counter for normalization
    TH1F*  hcounter = new TH1F("hcounter", "", 3, 0, 3);
    hcounter->GetXaxis()->SetBinLabel(1, "fraction of processed events");
    hcounter->GetXaxis()->SetBinLabel(2, "number of events processed");
    hcounter->GetXaxis()->SetBinLabel(3, "number of events passing");
    
    fout_tmp->cd();
    CutHistogram cuts("cuts");

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
            hparam->SetBinContent( pin+1, in.getUntrackedParameter<double>( params[pin], DEF_VAL_FLOAT ) );
        else if(in.existsAs<int>( params[pin], false ) )
            hparam->SetBinContent( pin+1, in.getUntrackedParameter<int>   ( params[pin], DEF_VAL_FLOAT  ) );
        else {}
    }
    hparam->SetBinContent            (n_untr_param + 1,  (in.getParameter<vector<int> >("evLimits"))[0]   );
    hparam->GetXaxis()->SetBinLabel  (n_untr_param + 1,  "evLow" );
    hparam->SetBinContent            (n_untr_param + 2,  (in.getParameter<vector<int> >("evLimits"))[1]   );
    hparam->GetXaxis()->SetBinLabel  (n_untr_param + 2,  "evHigh" );
    hparam->GetXaxis()->SetBinLabel  (n_untr_param + 3,  (in.getParameter<string>("outFileName")).c_str() );
    hparam->GetXaxis()->SetBinLabel  (n_untr_param + 4,  (in.getParameter<string>("pathToTF")).c_str() );
    hparam->GetXaxis()->SetBinLabel  (n_untr_param + 5,  (in.getParameter<string>("pathToCP")).c_str() );
    hparam->GetXaxis()->SetBinLabel  (n_untr_param + 6,  (in.getParameter<string>("pathToCP_smear")).c_str() );
    hparam->GetXaxis()->SetBinLabel  (n_untr_param + 7,  (in.getParameter<string>("pathToFile")).c_str() );
    hparam->GetXaxis()->SetBinLabel  (n_untr_param + 8,  (in.getParameter<string>("ordering")).c_str() );

    for( int sam = 0 ; sam < (int)samples.size(); sam++) {
        if( !(samples[sam].getParameter<bool>("skip")) ) {
            hparam->SetBinContent( n_untr_param+9, samples[sam].getParameter<double>("xSec") );
            hparam->GetXaxis()->SetBinLabel  ( n_untr_param+9, (samples[sam].getParameter<string>("nickName") ).c_str());
        }
    }

    // number of events that will be processed
    int events_     = 0;

    //Output TTree is now wrapped in a separate class
    TTree* _otree = new TTree("tree", "");
    METree* otree = new METree(_otree);
    otree->make_branches(MH);

#ifdef DO_BTAG_LR_TREE
    TTree* _btag_tree = new TTree("btag_lr", "");
    assert(_btag_tree != 0); 
    BTagLRTree btag_tree(_btag_tree);
    btag_tree.make_branches();
#endif

    /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
    /* @@@@@@@@@@@@@@@@@@@@@@@@@ OPEN FILES @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */


    // read input files
    bool openAllFiles  = false;
    Samples* mySamples = new Samples(openAllFiles, pathToFile, ordering, samples, lumi, verbose);
    vector<string> mySampleFiles = mySamples->Files();
    assert(mySampleFiles.size() > 0);
    //if(mySamples->IsOk()) {

    //    cout << "Ok!" << endl;
    //    mySampleFiles = mySamples->Files();

    //    for( unsigned int i = 0 ; i < mySampleFiles.size(); i++) {
    //        string sampleName = mySampleFiles[i];

    //        cout << mySampleFiles[i] << " ==> " << mySamples->GetXSec(sampleName)
    //             << " pb,"
    //             << " ==> weight = "            << mySamples->GetWeight(sampleName) << endl;
    //    }
    //}
    //else {
    //    cout << "Problems... leaving" << endl;

    //    fout_tmp->Close();
    //    cout << "Delete meIntegrator..." << endl;
    //    delete meIntegrator;
    //    delete clock;
    //    delete clock2;
    //    if(ran!=0)       delete ran;
    //    if(jet_smear!=0) delete jet_smear;
    //    cout << "Finished!!!" << endl;
    //    cout << "*******************" << endl;

    //    return 1;
    //}


    // open first sample for b-energy regression => get pointer to the tree
    //string currentName0     = mySampleFiles[0];

    //TTree* currentTree_reg  = mySamples->GetTree( currentName0, TTH_TTREE_NAME);
    ////For 8 TeV 
    //if (currentTree_reg == 0) {
    //    currentTree_reg  = mySamples->GetTree( currentName0, "events");
    //}
    TTree* currentTree_reg = 0;

    cout << "Looping over samples " << endl;
    // loop over input files
    for(unsigned int sample = 0 ; sample < mySampleFiles.size(); sample++) {
        
        //Need to reinitialize for each file
        evHigh = evLimits[1];

        const string currentName = mySampleFiles[sample];
        const int bdisc = mySamples->bdiscriminator[currentName];

        //if(currentName.find("Run2012")!=string::npos) isMC = false;

        cout << "Opening file " << currentName << endl;
        TTree* currentTree = mySamples->GetTree  (currentName, TTH_TTREE_NAME);
        //For 8 TeV 
        if (currentTree == 0) {
            currentTree  = mySamples->GetTree( currentName, "events");
        }
        assert(currentTree != 0);
        //create the input TTree with branches
        TTHTree* itree = new TTHTree(currentTree);
        itree->set_branch_addresses();
        currentTree->SetBranchStatus("*", 1);

        float scaleFactor        = mySamples->GetWeight(currentName);

        //FIXME: insert into ntuples
        //TH1F* count_Q2           = mySamples->GetHisto (currentName, "Count_Q2");

        //FIXME: unused?
        //const float normDown           = count_Q2 ? count_Q2->GetBinContent(1)/count_Q2->GetBinContent(2) : 1.0;
        //const float normUp             = count_Q2 ? count_Q2->GetBinContent(3)/count_Q2->GetBinContent(2) : 1.0;
        TTH::EventHypothesis Vtype;

        cout << "Done loading input tree" << endl;

        //initialize empty structs
        ////FIXME: need to add to input ntuples
        genTopInfo genTop = {};
        genTopInfo genTbar = {};
        genParticleInfo genB = {};
        genParticleInfo genBbar = {};

        //float SimBsmass           [999];
        //float SimBspt             [999];
        //float SimBseta            [999];
        //float SimBsphi            [999];

        /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
        /* @@@@@@@@@@@@@@@@@@@@@@@@@ EVENT LOOP @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */

        // loop over entries
        int counter = 0;
        const Long64_t nentries = currentTree->GetEntries();
        int event_trials  = 0;

        if( evHigh < 0 ) {
            evHigh = nentries;
            cout << "evHigh " << evHigh << " < 0 " << endl;
            evHigh = nentries; 
        }
        if( evHigh > nentries ) {
            cout << "evHigh " << evHigh << " > nentries " << nentries << endl;
            evHigh = nentries; 
        }

        cout << "Total number of entries: " << nentries << endl;
        cout << " -> This job will process events in the range [ " << evLow << ", " << evHigh << " )" << endl;


        TStopwatch processing_sw;
        processing_sw.Start();
        cout << "Looping over samples " << endl;
        //event loop
        for (Long64_t i = evLow; i < evHigh ; i++) {
            // initialize branch variables
            itree->loop_initialize();
            otree->loop_initialize();

            // if fixed-size job and above upper bound, continue...
            if(counter>evHigh && fixNumEvJob) continue;
            
            // otherwise, if outside the event window, continue...
            if(!fixNumEvJob && !(i>=evLow && i<evHigh) ) continue;
            events_++;
            
            //fill histogram counter with number of processed events
            hcounter->SetBinContent(2, hcounter->GetBinContent(2)+1);

            // print the processed event number
            if(i%500==0) {
                processing_sw.Stop();
                float _swtime_c = processing_sw.CpuTime();
                float _swtime_r = processing_sw.RealTime();
                processing_sw.Reset();
                processing_sw.Start();
                cout << i << " (" << float(i)/float(nentries)*100 << " %) " << 500/_swtime_c << " " << 500/_swtime_r << endl;
            }

            // set variables that are used, but for which there may be no branches in the input tree
            itree->weight__pu = 1.0;
            itree->weight__pu_up = 1.0;
            itree->weight__pu_down = 1.0;
            itree->lhe__n_j = 1.0;

            //FIXME: implement machinery for trigger weights
            //weightTrig2012 = 1.0;

            //initialize trigger flags
            for(int k = 0; k < 70 ; k++) {
                otree->triggerFlags_[k] = 0;
            }
            for(int k = 0; k < 3 ; k++) {
                otree->SCALEsyst_[k] = 1.0;
            }

            //FIXME
            //nhJets = 0;
            //nPVs   = 1;


            // read event...
            long nbytes = currentTree->GetEntry(i);

            //otree->copy_branches(itree);
        
            if (is_undef(itree->hypo1)) {
                cerr << "hypo1 undefined " << itree->hypo1 << " probably there will be issues" << endl;
                continue;
            }
            
            Vtype = static_cast<TTH::EventHypothesis>(itree->hypo1);
            if (debug>3) cout << "hypo1 " << itree->hypo1 << " " << Vtype << endl;
            if (((int)Vtype < 0) || ((int)Vtype>11)) {
                cerr << "Vtype undefined " << (int)Vtype << " probably there will be issues" << endl;
                continue;
            }
            
            genTop.bmass = itree->gen_t__b__mass;
            genTop.bpt = itree->gen_t__b__pt;
            genTop.beta = itree->gen_t__b__eta;
            genTop.bphi = itree->gen_t__b__phi;
            genTop.bphi = itree->gen_t__b__phi;
            genTop.bstatus = itree->gen_t__b__status;
            
            genTop.wdau1mass = itree->gen_t__w_d1__mass;
            genTop.wdau1pt = itree->gen_t__w_d1__pt;
            genTop.wdau1eta = itree->gen_t__w_d1__eta;
            genTop.wdau1phi = itree->gen_t__w_d1__phi;
            genTop.wdau1id = itree->gen_t__w_d1__id;

            genTop.wdau2mass = itree->gen_t__w_d2__mass;
            genTop.wdau2pt = itree->gen_t__w_d2__pt;
            genTop.wdau2eta = itree->gen_t__w_d2__eta;
            genTop.wdau2phi = itree->gen_t__w_d2__phi;
            genTop.wdau2id = itree->gen_t__w_d2__id;
            
            genTbar.bmass = itree->gen_tbar__b__mass;
            genTbar.bpt = itree->gen_tbar__b__pt;
            genTbar.beta = itree->gen_tbar__b__eta;
            genTbar.bphi = itree->gen_tbar__b__phi;
            genTbar.bphi = itree->gen_tbar__b__phi;
            genTbar.bstatus = itree->gen_tbar__b__status;
            
            genTbar.wdau1mass = itree->gen_tbar__w_d1__mass;
            genTbar.wdau1pt = itree->gen_tbar__w_d1__pt;
            genTbar.wdau1eta = itree->gen_tbar__w_d1__eta;
            genTbar.wdau1phi = itree->gen_tbar__w_d1__phi;
            genTbar.wdau1id = itree->gen_tbar__w_d1__id;

            genTbar.wdau2mass = itree->gen_tbar__w_d2__mass;
            genTbar.wdau2pt = itree->gen_tbar__w_d2__pt;
            genTbar.wdau2eta = itree->gen_tbar__w_d2__eta;
            genTbar.wdau2phi = itree->gen_tbar__w_d2__phi;
            genTbar.wdau2id = itree->gen_tbar__w_d2__id;

            genB.mass = itree->gen_b__mass; 
            genB.pt = itree->gen_b__pt; 
            genB.eta = itree->gen_b__eta; 
            genB.phi = itree->gen_b__phi; 
            genB.status = itree->gen_b__status; 
            genB.charge = 0;
            genB.momid = 25;
            
            genBbar.mass = itree->gen_bbar__mass; 
            genBbar.pt = itree->gen_bbar__pt; 
            genBbar.eta = itree->gen_bbar__eta; 
            genBbar.phi = itree->gen_bbar__phi; 
            genBbar.status = itree->gen_bbar__status; 
            genBbar.charge = 0;
            genBbar.momid = 25;

            if( debug>=2 ) {
                cout << endl;
                cout << "******************************" << endl;
                cout << "Analyzing event " << itree->event__id << " bytes " << nbytes << " read" << endl;
            }

            otree->sample                = sample; 
            otree->counter_            = counter;
            otree->weight_             = scaleFactor;
            otree->weightTopPt_        = 1;
            otree->nPVs_               = itree->n__pv;

            otree->Vtype_              = (int)Vtype;

            otree->EVENT_.run          = itree->event__run;
            otree->EVENT_.lumi         = itree->event__lumi;
            otree->EVENT_.event        = itree->event__id;
            otree->EVENT_.json         = itree->event__json;

            otree->PUweight_           = itree->weight__pu;
            otree->PUweightP_          = itree->weight__pu_up;
            otree->PUweightM_          = itree->weight__pu_down;

            //get the madgraph generator product information
            //FIXME: what is this SCALEsyst, is it correct to take from LHE?
            otree->lheNj_              = itree->lhe__n_j;
            otree->n_b_                = itree->lhe__n_b;
            otree->n_c_                = itree->lhe__n_c;
            otree->n_l_                = itree->lhe__n_l;
            otree->n_g_                = itree->lhe__n_g;
            //otree->n_b_                = SCALEsyst[9];
            //otree->n_c_                = SCALEsyst[8];
            //otree->n_l_                = SCALEsyst[7];
            //otree->n_g_                = SCALEsyst[6];


            //FIXME: not needed any more, do we want to keep the trigger weight infrastructure
            //otree->trigger_     = weightTrig2012;


            //cout << "trigbits";
            for(int k = 0; k < 70 ; k++) {
                otree->triggerFlags_[k] = itree->trigger__bits[k];
                //if (debug>3)
                //    cout << " " << itree->trigger__bits[k];
            }
            //cout << endl;
            //if (debug>3)
            //    cout << "sumbits " << sumbits << endl;

            //FIXME: where to get this scalesyst
            //otree->SCALEsyst_[0] = 1.0;
            //if( count_Q2 ) {
            //    otree->SCALEsyst_[1] = TMath::Power(SCALEsyst[2],SCALEsyst[1])*SCALEsyst[4]/normDown;
            //    otree->SCALEsyst_[2] = TMath::Power(SCALEsyst[3],SCALEsyst[1])*SCALEsyst[5]/normUp;
            //}

            otree->probAtSgn_          =  0.;
            otree->probAtSgn_alt_      =  0.;

            otree->probAtSgn_ttbb_     =  0.;
            otree->probAtSgn_alt_ttbb_ =  0.;
            otree->probAtSgn_alt_ttbj_ =  0.;
            otree->probAtSgn_alt_ttcc_ =  0.;
            otree->probAtSgn_alt_ttjj_ =  0.;

            otree->nMassPoints_        = TMath::Max(nHiggsMassPoints,nTopMassPoints);
            otree->flag_type0_         = DEF_VAL_INT;
            otree->flag_type1_         = DEF_VAL_INT;
            otree->flag_type2_         = DEF_VAL_INT;
            otree->flag_type3_         = DEF_VAL_INT;
            otree->flag_type4_         = DEF_VAL_INT;
            otree->flag_type6_         = DEF_VAL_INT;

            otree->btag_LR            = DEF_VAL_INT;

            for( int k = 0; k < NMAXLEPTONS; k++) {
                otree->lepton_pt_[k]        = DEF_VAL_FLOAT;
                otree->lepton_eta_[k]       = DEF_VAL_FLOAT;
                otree->lepton_phi_[k]       = DEF_VAL_FLOAT;
                otree->lepton_m_[k]         = DEF_VAL_FLOAT;
                otree->lepton_charge_[k]    = DEF_VAL_FLOAT;
                otree->lepton_rIso_[k]      = DEF_VAL_FLOAT;
                otree->lepton_type_[k]      = DEF_VAL_FLOAT;
                otree->lepton_dxy_[k]       = DEF_VAL_FLOAT;
                otree->lepton_dz_[k]        = DEF_VAL_FLOAT;
                otree->lepton_wp80_[k]      = DEF_VAL_FLOAT;
                otree->lepton_wp70_[k]      = DEF_VAL_FLOAT;
                otree->lepton_wp95_[k]      = DEF_VAL_FLOAT;
                otree->lepton_MVAtrig_[k]   = DEF_VAL_FLOAT;
            }

            otree->Mll_  = DEF_VAL_FLOAT;
            otree->MTln_ = DEF_VAL_FLOAT;

            for( int k = 0; k < NMAXJETS; k++) {
                otree->jet_pt_[k] = DEF_VAL_FLOAT;
                otree->jet_pt_alt_[k] = DEF_VAL_FLOAT;
                otree->jet_eta_[k] = DEF_VAL_FLOAT;
                otree->jet_phi_[k] = DEF_VAL_FLOAT;
                otree->jet_m_[k] = DEF_VAL_FLOAT;
                otree->jet_csv_[k] = DEF_VAL_FLOAT;
                otree->jet_id_[k] = DEF_VAL_INT;
            }
            for( int k = 0; k < NMAXPERMUT; k++) {
                otree->perm_to_jet_    [k] = DEF_VAL_INT;
                otree->perm_to_gen_    [k] = DEF_VAL_INT;
                otree->perm_to_jet_alt_[k] = DEF_VAL_INT;
                otree->perm_to_gen_alt_[k] = DEF_VAL_INT;
            }

            // save the values into the tree (save mH[0] in case no scan is required)
            for( unsigned int m = 0; m < (unsigned int)nHiggsMassPoints ; m++) {
                otree->mH_scan_[m] = mH[m];
            }
            for( unsigned int t = 0; t < (unsigned int)nTopMassPoints ; t++) {
                otree->mT_scan_[t] = mT[t];
            }

            // reset the gen top/Higgs 4-vector
            for(int elem=0; elem<4; elem++) {
                otree->p4T_   [elem] = DEF_VAL_FLOAT;
                otree->p4Tbar_[elem] = DEF_VAL_FLOAT;
                otree->p4H_   [elem] = DEF_VAL_FLOAT;
            }
            otree->ttH_.reset();

            // save jet kinematics into the tree...
            otree->nJet_ = 8;
            for(int q = 0; q < otree->nJet_ ; q++ ) {
                // kinematics
                otree->jet_pt_     [q] = DEF_VAL_FLOAT;
                otree->jet_pt_alt_ [q] = DEF_VAL_FLOAT;
                otree->jet_eta_    [q] = DEF_VAL_FLOAT;
                otree->jet_phi_    [q] = DEF_VAL_FLOAT;
                otree->jet_m_      [q] = DEF_VAL_FLOAT;
                otree->jet_csv_    [q] = DEF_VAL_FLOAT;
                otree->jet_id_     [q] = DEF_VAL_INT;
            }
            otree->hJetAmong_    = 0;
            otree->jetsAboveCut_ = 0;

            // set all prob. to 0.0;
            for(int p = 0 ; p < otree->nTotInteg_; p++) {
                otree->probAtSgn_permut_       [p] = 0.;
                otree->probAtSgnErr_permut_    [p] = 0.;
                otree->callsAtSgn_permut_      [p] = 0 ;
                otree->chi2AtSgn_permut_       [p] = 0.;
            }
            for(int p = 0 ; p < otree->nPermut_; p++) {
                otree->probAtSgn_bb_permut_ [p] = 0.;
            }
            for(int p = 0 ; p < otree->nTotInteg_alt_; p++) {
                otree->probAtSgn_alt_permut_   [p] = 0.;
                otree->probAtSgnErr_alt_permut_[p] = 0.;
                otree->callsAtSgn_alt_permut_  [p] = 0 ;
                otree->chi2AtSgn_alt_permut_   [p] = 0.;
            }
            for(int p = 0 ; p < otree->nPermut_alt_; p++) {
                otree->probAtSgn_bj_permut_ [p] = 0.;
                otree->probAtSgn_cc_permut_ [p] = 0.;
                otree->probAtSgn_jj_permut_ [p] = 0.;
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

                otree->p4T_[0] = (topBLV+topW1LV+topW2LV).Pt();
                otree->p4T_[1] = (topBLV+topW1LV+topW2LV).Eta();
                otree->p4T_[2] = (topBLV+topW1LV+topW2LV).Phi();
                otree->p4T_[3] = (topBLV+topW1LV+topW2LV).M();
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

                otree->p4Tbar_[0] = (atopBLV+atopW1LV+atopW2LV).Pt();
                otree->p4Tbar_[1] = (atopBLV+atopW1LV+atopW2LV).Eta();
                otree->p4Tbar_[2] = (atopBLV+atopW1LV+atopW2LV).Phi();
                otree->p4Tbar_[3] = (atopBLV+atopW1LV+atopW2LV).M();
            }
            if(genB.mass>0 && genB.mass<10 && (genB.momid==25 || genB.momid==23)) {
                genBLV.SetPtEtaPhiM(genB.pt,genB.eta ,genB.phi, genB.mass );
            }
            if(genBbar.mass>0 && genBbar.mass<10 && (genBbar.momid==25 || genBbar.momid==23)) {
                genBbarLV.SetPtEtaPhiM(genBbar.pt,genBbar.eta ,genBbar.phi, genBbar.mass );
            }
            if( genBLV.Pt()>1 && genBbarLV.Pt()>1 ) {
                otree->p4H_[0] = (genBLV+genBbarLV).Pt();
                otree->p4H_[1] = (genBLV+genBbarLV).Eta();
                otree->p4H_[2] = (genBLV+genBbarLV).Phi();
                otree->p4H_[3] = (genBLV+genBbarLV).M();
            }

            if(debug>=2) cout << "@B" << endl;

            // Compute SF to correct gen top pT
            float weightTPt    = 1.;
            float weightTbarPt = 1.;

            if(otree->p4T_[0] > 0) {
                if(otree->p4T_[0] < 463.312)
                    weightTPt = 1.18246 + 2.10061*1e-6*otree->p4T_[0]*(otree->p4T_[0] - 2*463.312);
                else
                    weightTPt = 0.732;
            }
            if(otree->p4Tbar_[0] > 0) {
                if(otree->p4T_[0] < 463.312)
                    weightTbarPt = 1.18246 + 2.10061*1e-6*otree->p4Tbar_[0]*(otree->p4Tbar_[0] - 2*463.312);
                else
                    weightTbarPt = 0.732;
            }
            otree->weightTopPt_ = weightTPt /**weightTbarPt */ ;

            if(debug>=2) std::cout << "top weight = " << otree->weightTopPt_ << " = " << weightTPt << "(*" << weightTbarPt << ")" <<  std::endl;
            //------------------------------------------

            // dummy cut (for the moment)
            bool properEventSL = (genBLV.Pt()>0 && genBbarLV.Pt()>0 && topBLV.Pt()>0 && topW1LV.Pt()>0 && topW2LV.Pt()>0 && atopBLV.Pt()>0 && atopW1LV.Pt()>0 && atopW2LV.Pt()>0);
            bool properEventDL = (genBLV.Pt()>0 && genBbarLV.Pt()>0 && topBLV.Pt()>0 && topW1LV.Pt()>0 && topW2LV.Pt()>0 && atopBLV.Pt()>0 && atopW1LV.Pt()>0 && atopW2LV.Pt()>0);

            if(!(properEventSL || properEventDL)) {

                if (debug>=2) {
                    cout << "A dummy cut has failed..." << endl;
                    cout << " => go to next event!" << endl;
                    cout << "******************************" << endl;
                }
                if (cutLeptons) {
                    cuts.fill(CutHistogram::Cuts::LEPTONS);
                    continue;
                }
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
            if( switchoffOL==0 && otree->p4T_[0]>0. && otree->p4Tbar_[0]>0. && otree->p4H_[0]>0. && TMath::Abs(HIGGSB1.Py())>0  && TMath::Abs(HIGGSB2.Py())>0) {

                if(debug>=2) {
                    cout <<  "p4T    = (" << otree->p4T_   [0] << "," <<    otree->p4T_   [1]<< "," <<    otree->p4T_   [2] << "," <<    otree->p4T_   [3] << ")" << endl;
                    cout <<  "p4Tbar = (" << otree->p4Tbar_[0] << "," <<    otree->p4Tbar_[1]<< "," <<    otree->p4Tbar_[2] << "," <<    otree->p4Tbar_[3] << ")" << endl;
                    cout <<  "p4H    = (" << otree->p4H_   [0] << "," <<    otree->p4H_   [1]<< "," <<    otree->p4H_   [2] << "," <<    otree->p4H_   [3] << ")" << endl;
                }

                TLorentzVector top(0,0,0,0);
                top.SetPtEtaPhiM  ( otree->p4T_   [0],    otree->p4T_   [1],    otree->p4T_   [2],    otree->p4T_   [3]);
                TLorentzVector atop(0,0,0,0);
                atop.SetPtEtaPhiM ( otree->p4Tbar_[0],    otree->p4Tbar_[1],    otree->p4Tbar_[2],    otree->p4Tbar_[3]);
                TLorentzVector higgs(0,0,0,0);
                higgs.SetPtEtaPhiM( otree->p4H_   [0],    otree->p4H_   [1],    otree->p4H_   [2],    otree->p4H_   [3]);

                // this is needed because if t+t~+h has 0 pT, tot.Eta() raises a warning
                double px = (top+atop+higgs).Px();
                double py = (top+atop+higgs).Py();
                //double pz = (top+atop+higgs).Pz();

                double x1,x2;
                otree->ttH_.me2_ttH  = meIntegrator->meSquaredOpenLoops( &top, &atop, &higgs, x1, x2);
                otree->ttH_.x1       = x1;
                otree->ttH_.x2       = x2;
                otree->ttH_.pdf      = meIntegrator->ggPdf( x1, x2, (2*MT + MH)/2. )*x1*x1*x2*x2;
                otree->ttH_.pt       = TMath::Sqrt( px*px + py*py );
                otree->ttH_.eta      = otree->ttH_.pt>1e-03 ? (top+atop+higgs).Eta() : (top+atop+higgs).Rapidity();
                otree->ttH_.phi      = (top+atop+higgs).Phi();
                otree->ttH_.m        = (top+atop+higgs).M();
                otree->ttH_.me2_ttbb = meIntegrator->meSquaredOpenLoops_ttbb( &top, &atop, &HIGGSB1, &HIGGSB2, x1, x2);
            }


            /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
            /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ GEN BHADRONS @@@@@@@@@@@@@@@@@@@@@@@@@@@  */

            if(debug>=2) cout << "@G" << endl;

            // find out number of b-hadrons in the event...
            //FIXME: for this, a new recipe will be developed. For the moment, count reco jet -> genJet partonFlavour
            //otree->nSimBs_         = itree->n_sim_b;
            //otree->nSimCs_         = itree->n_sim_c;
            otree->nSimBs_         = 0;
            otree->nSimCs_         = 0;
            otree->nMatchSimBsOld_ = 0;
            otree->nMatchSimBs_v1_ = 0;
            otree->nMatchSimBs_v2_ = 0;
            otree->nMatchSimBs_    = 0;
            otree->nMatchSimCs_v1_ = 0;
            otree->nMatchSimCs_v2_ = 0;
            otree->nMatchSimCs_    = 0;

            //for(int l = 0; l < otree->nSimBs; l++) {
            //    TLorentzVector Bs(1,0,0,1);
            //    Bs.SetPtEtaPhiM( SimBspt[l], SimBseta[l], SimBsphi[l], SimBsmass[l]);

            //    if( topBLV.Pt()>10 && deltaR(topBLV,  Bs)<0.5 ) continue;
            //    if(atopBLV.Pt()>10 && deltaR(atopBLV, Bs)<0.5 ) continue;

            //    for(int hj = 0; hj < itree->n__jet; hj++) {
            //        TLorentzVector hJLV(1,0,0,1);
            //        if( itree->gen_jet__pt[hj] > 10 )
            //            hJLV.SetPtEtaPhiM( itree->gen_jet__pt[hj], itree->gen_jet__eta[hj], itree->gen_jet__phi[hj], 0.0);
            //        if( hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<5 && deltaR(Bs, hJLV)<0.5 ) otree->nMatchSimBsOld_++;
            //    }

            //    //FIXME: all jets now in the same vector
            //    //for(int aj = 0; aj<naJets; aj++) {
            //    //    TLorentzVector aJLV(1,0,0,1);
            //    //    if(aJet_genPt[aj]>10)
            //    //        aJLV.SetPtEtaPhiM( aJet_genPt[aj], aJet_genEta[aj], aJet_genPhi[aj], 0.0);
            //    //    if( aJLV.Pt()>20 && TMath::Abs(aJLV.Eta())<5 && deltaR(Bs, aJLV)<0.5 ) otree->nMatchSimBsOld_++;
            //    //}
            //}

            //if( otree->nSimBs>=2) {
            //    for(int l = 0; l<nSimBs-1; l++) {
            //        TLorentzVector Bs1(1,0,0,1);
            //        Bs1.SetPtEtaPhiM( SimBspt[l], SimBseta[l], SimBsphi[l], SimBsmass[l]);
            //        if( topBLV.Pt()>10 && deltaR(topBLV,  Bs1)<0.5 ) continue;
            //        if(atopBLV.Pt()>10 && deltaR(atopBLV, Bs1)<0.5 ) continue;
            //        for(int m = l+1; m<nSimBs; m++) {
            //            TLorentzVector Bs2(1,0,0,1);
            //            Bs2.SetPtEtaPhiM( SimBspt[m], SimBseta[m], SimBsphi[m], SimBsmass[m]);
            //            if( topBLV.Pt()>10 && deltaR(topBLV,  Bs2)<0.5 ) continue;
            //            if(atopBLV.Pt()>10 && deltaR(atopBLV, Bs2)<0.5 ) continue;
            //            if( deltaR(Bs1,Bs2)<0.50 ) otree->nMatchSimBsOld_--;
            //        }
            //    }
            //}

            //creates a TLorentzVector with the four-momentum of the gen jet with index nj
            auto vec_from_gen_jet = [&itree, debug] (const int nj) {
                TLorentzVector hJLV(1,0,0,1);
                hJLV.SetPtEtaPhiM( itree->gen_jet__pt[nj], itree->gen_jet__eta[nj], itree->gen_jet__phi[nj], itree->gen_jet__mass[nj]);

                if (is_undef(itree->gen_jet__pt[nj])) {
                    if (debug>3)
                        cerr << "gen jet " << nj << " pt is " << itree->gen_jet__pt[nj] << " -> was unset in TTree" << endl;
                    return TLorentzVector(0, 0, 0, 0);
                }

                return hJLV;
            };

            //// now find out how many matched b's we have...
            for(int hj = 0; hj<itree->n__jet; hj++) {
            
                if (debug>2) {
                    cout << "jet rec " << itree->jet__id[hj] << " pt " << itree->jet__pt[hj] << " eta " << itree->jet__eta[hj] << " phi " << itree->jet__phi[hj] << endl;
                    cout << "jet gen " << itree->gen_jet__id[hj] << " pt " << itree->gen_jet__pt[hj] << " eta " << itree->gen_jet__eta[hj] << " phi " << itree->gen_jet__phi[hj] << endl;
                }
                TLorentzVector hJLV = vec_from_gen_jet(hj);

                // if jet is within acceptance...
                if( hJLV.Pt() > 20 && TMath::Abs(hJLV.Eta()) < 5 ) {
                    if( topBLV.Pt() > 10 && deltaR(topBLV, hJLV ) < 0.5 ) continue;
                    if(atopBLV.Pt() > 10 && deltaR(atopBLV, hJLV ) < 0.5 ) continue;
                    if( abs(itree->jet__id[hj])==5 ) otree->nMatchSimBs_v1_++;
                }

                if( hJLV.Pt() > 20 && TMath::Abs(hJLV.Eta()) < 2.5 ) {
                    if( topBLV.Pt() > 10 && deltaR(topBLV, hJLV ) < 0.5 ) continue;
                    if(atopBLV.Pt() > 10 && deltaR(atopBLV,hJLV ) < 0.5 ) continue;
                    if( abs(itree->jet__id[hj])==5 ) otree->nMatchSimBs_v2_++;
                }
            
                //if( itree->jet__pt[hj]>30 && hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<2.5 ) {
                if( itree->jet__pt[hj] > 30 && hJLV.Pt() > 20 && TMath::Abs(hJLV.Eta())<2.5 ) {
                    if( topBLV.Pt() > 10 && deltaR(topBLV, hJLV ) < 0.5 ) continue;
                    if(atopBLV.Pt() > 10 && deltaR(atopBLV,hJLV ) < 0.5 ) continue;
                    if( abs(itree->jet__id[hj])==5 ) otree->nMatchSimBs_++; //baseline
                }

            }

            // now find out how many matched c's we have...
            for(int hj = 0; hj<itree->n__jet; hj++) {
                //TLorentzVector hJLV(1,0,0,1);
                //if(itree->gen_jet__pt[hj]>10)
                //    hJLV.SetPtEtaPhiM( itree->gen_jet__pt[hj], itree->gen_jet__eta[hj], itree->gen_jet__phi[hj], 0.0);
                TLorentzVector hJLV = vec_from_gen_jet(hj);

                // if jet is within acceptance...
                if( hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<5 ) {
                    if( topCLV.Pt()>10 && deltaR(topCLV, hJLV )<0.5 ) continue;
                    if(atopCLV.Pt()>10 && deltaR(atopCLV,hJLV )<0.5 ) continue;
                    if( abs(itree->jet__id[hj])==4 ) otree->nMatchSimCs_v1_++;
                }

                if( hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<2.5 ) {
                    if( topCLV.Pt()>10 && deltaR(topCLV, hJLV )<0.5 ) continue;
                    if(atopCLV.Pt()>10 && deltaR(atopCLV,hJLV )<0.5 ) continue;
                    if( abs(itree->jet__id[hj])==4 ) otree->nMatchSimCs_v2_++;
                }

                //FIXME: Why 2 Pt checks?
                //if( itree->jet__pt[hj]>30 && hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<2.5 ) {
                if( itree->jet__pt[hj]>30 && hJLV.Pt()>20 && TMath::Abs(hJLV.Eta())<2.5 ) {
                    if( topCLV.Pt()>10 && deltaR(topCLV, hJLV )<0.5 ) continue;
                    if(atopCLV.Pt()>10 && deltaR(atopCLV,hJLV )<0.5 ) continue;
                    if( abs(itree->jet__id[hj])==4 ) otree->nMatchSimCs_++;
                }
            }
            if (debug>3) {
                cout << "nsim "
                     << otree->nMatchSimBs_v1_ << " "
                     << otree->nMatchSimBs_v2_ << " "
                     << otree->nMatchSimBs_ << " "
                     << otree->nMatchSimCs_v1_ << " "
                     << otree->nMatchSimCs_v2_ << " "
                     << otree->nMatchSimCs_ << endl;
            }

            if(debug>=2) cout << "@H" << endl;

            int lock          = 0;

            //int trial_success = 0;

            // loop over systematics
            for( unsigned int syst = 0; syst < systematics.size() ; syst++) {

                // which systematic is considered
                otree->syst_ = systematics[ syst ];

                if( lock ) {
                    if(debug>=2) cout << "Skip systematics " << otree->syst_ << " because the event is locked" << endl;
                    continue;
                }

                if(debug>=2) cout << "Dealing with systematics " << otree->syst_  << endl;

                // decide which analysis to run
                doCSVup   = otree->syst_==1 ;
                doCSVdown = otree->syst_==2 ;
                doJECup   = otree->syst_==3 ;
                doJECdown = otree->syst_==4 ;
                doJERup   = otree->syst_==5 ;
                doJERdown = otree->syst_==6 ;

                // one more loop over the same event
                otree->iterations_++;

                // reset additive probabilities
                otree->probAtSgn_          =  0.;
                otree->probAtSgn_alt_      =  0.;

                otree->probAtSgn_ttbb_     =  0.;
                otree->probAtSgn_alt_ttbb_ =  0.;
                otree->probAtSgn_alt_ttbj_ =  0.;
                otree->probAtSgn_alt_ttcc_ =  0.;
                otree->probAtSgn_alt_ttjj_ =  0.;

                // reset the flags (events can migrate)
                otree->flag_type0_         = -99;
                otree->flag_type1_         = -99;
                otree->flag_type2_         = -99;
                otree->flag_type3_         = -99;
                otree->flag_type4_         = -99;
                otree->flag_type6_         = -99;

                /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  */
                /* @@@@@@@@@@@@@@@@@@@@@@@@@@@@ LEPTON SELECTION @@@@@@@@@@@@@@@@@@@@@@@@@  */

                // keep track of the original leptons
                std::vector<int> lep_index;

                // charged leptons and MET
                TLorentzVector leptonLV, leptonLV2;
                TLorentzVector neutrinoLV;


                //loop over leptons
                //Find number of loose leptons with custom conditions
                //useful for re-tightening the loose lepton definition
                //for( int k = 0; k < itree->n__lep ; k++) {

                //    const float lep_pt   = itree->lep__pt[k];
                //    const float lep_eta  = itree->lep__eta[k];
                //    const float lep_phi  = itree->lep__phi[k];
                //    const float lep_type = abs(itree->lep__id[k]);
                //    const float lep_iso  = itree->lep__rel_iso[k];
                //    const float lep_dxy  = TMath::Abs(itree->lep__dxy[k]);
                //    const float lep_dz   = TMath::Abs(itree->lep__dz[k]);
                //    const float lep_charge = itree->lep__charge[k];

                //    if (debug > 2) {
                //        cout << "lepton rec " << lep_type << " pt " << lep_pt
                //             << " eta " << lep_eta << " phi " << lep_phi
                //             << " iso " << lep_iso << " dxy " << lep_dxy
                //             << " dz " << lep_dz << " charge " << lep_charge << endl;
                //    }

                //    const float gen_lep_pt   = itree->lep__pt[k];
                //    const float gen_lep_eta  = itree->lep__eta[k];
                //    const float gen_lep_phi  = itree->lep__phi[k];
                //    const float gen_lep_type = abs(itree->lep__id[k]);

                //    if (debug > 2) {
                //        cout << "lepton gen " << gen_lep_type << " pt " << gen_lep_pt << " eta " << gen_lep_eta << " phi " << gen_lep_phi << endl;
                //    }

                //    if(
                //        // muons
                //        (lep_type==13 && lep_pt > lepPtLoose && TMath::Abs(lep_eta)<muEtaLoose && lep_iso < lepIsoLoose  && lep_dxy < 0.2 && lep_dz<0.5) ||

                //        // electrons, FIXME, add lepton WP to input ntuple
                //        //(lep_type == 11 && lep_pt > lepPtLoose && TMath::Abs(lep_eta)<elEta && !(TMath::Abs(lep_eta) >1.442 && TMath::Abs(lep_eta)<1.566) &&
                //        // lep_iso < lepIsoLoose && vLepton_wp95[k] > 0 && lep_dxy < 0.04 && lep_dz<1.0 )
                //        (lep_type == 11 && lep_pt > lepPtLoose && TMath::Abs(lep_eta)<elEta && !(TMath::Abs(lep_eta) >1.442 && TMath::Abs(lep_eta)<1.566) &&
                //         lep_iso < lepIsoLoose &&  lep_dxy < 0.04 && lep_dz<1.0 )
                //    ) {
                //        //numLooseLep++;
                //    }


                //    //FIXME: missing WP
                //    if(  lep_type == 11 && lep_pt > lepPtLoose && TMath::Abs(lep_eta)<elEta && !(TMath::Abs(lep_eta) >1.442 && TMath::Abs(lep_eta)<1.566) &&
                //            lep_iso < lepIsoLoose && lep_dxy < 0.04 && lep_dz<1.0) {
                //        //numLooseAElec++;
                //    }
                //}


                ////FIXME, removed Vtype from here
                //if( debug>=2 ) {
                //    cout << numLooseLep << " loose leptons, "<< numLooseAElec << " loose electron(s) found in aLepton collection" << endl;
                //}
                
                if (debug > 3) {
                    cout << "n__sig_lep " << itree->n__sig_lep << " hypo " << Vtype << endl;    
                    for (int _i=0; _i < itree->n__sig_lep; _i++) {
                        cout << "sig_lep " << _i << " "
                            << itree->sig_lep__idx[_i] << " "
                            << itree->sig_lep__id[_i] << " "
                            << itree->sig_lep__type[_i] << " "
                            << itree->sig_lep__pt[_i] << " "
                            << itree->sig_lep__eta[_i] << " "
                            << itree->sig_lep__phi[_i] << " "
                            << itree->sig_lep__mass[_i] << endl;
                    }
                }

                ///////////////////////////////////
                //         SL events:  e+j/m+j   //
                ///////////////////////////////////

                properEventSL = false;
                if( (ENABLE_EJ && Vtype == TTH::EventHypothesis::en) || (ENABLE_MJ && Vtype == TTH::EventHypothesis::mun) ) {

                    if(debug>3) cout << "EJ/MJ" << endl;
                    
                    //for SL, the first lepton in the sig_lep array is always filled with THE signal lepton
                    leptonLV.SetPtEtaPhiM(itree->sig_lep__pt[0], itree->sig_lep__eta[0], itree->sig_lep__phi[0], itree->sig_lep__mass[0]);
                    
                    //index in the main lepton array    
                    const int lepton_idx = itree->sig_lep__idx[0]; 
                    if(debug>3) cout << "lepton idx " << lepton_idx << endl;
                    lep_index.push_back(0);

                    if(doGenLevelAnalysis) {
                        if( itree->gen_lep__pt[lepton_idx] > 5.)
                            leptonLV.SetPtEtaPhiM(itree->gen_lep__pt[0], itree->gen_lep__eta[0], itree->gen_lep__phi[0], (itree->gen_lep__type[0]==13 ? MU_MASS : ELE_MASS )  );
                        else
                            leptonLV.SetPtEtaPhiM( 5., 0., 0., 0. );
                    }

                    // tight cuts on lepton (SL)
                    int lepSelVtype2 =  (Vtype == TTH::EventHypothesis::mun && itree->sig_lep__type[0] == 13 && leptonLV.Pt() > muPtTight &&
                                         TMath::Abs(leptonLV.Eta()) < muEtaTight && itree->lep__rel_iso[lepton_idx] < lepIsoTight);
                    //int lepSelVtype3 =  (Vtype==3 && itree->lep__type[0]==11 && leptonLV.Pt()>lepPtTight &&
                    //                     itree->lep__rel_iso[0]<lepIsoTight && vLepton_wp80[0]>0 && TMath::Abs(itree->lep__dxy[0])<0.02 );
                    int lepSelVtype3 =  (Vtype == TTH::EventHypothesis::en && itree->sig_lep__type[0] == 11 && leptonLV.Pt() > elPtTight &&
                                         itree->lep__rel_iso[lepton_idx] < lepIsoTight && TMath::Abs(itree->lep__dxy[lepton_idx]) < 0.02);
                    
                    if (debug>3) {
                        cout << "lepSelVtype2,3 " << itree->sig_lep__type[0] << "==13 " <<
                            leptonLV.Pt() << " (" << lepPtTight << ") " <<
                            TMath::Abs(leptonLV.Eta()) << " (" << muEtaTight << ") " <<
                            TMath::Abs(itree->lep__dxy[lepton_idx]) << " (" << 0.02 << ") " <<
                            itree->lep__rel_iso[lepton_idx] << " (" << lepIsoTight << ")" << endl;
                    }

                    //FIXME: need to put trigger bits here
                    // OR of four trigger paths:  "HLT_Mu40_eta2p1_v.*", "HLT_IsoMu24_eta2p1_v.*", "HLT_Mu40_v.*",  "HLT_IsoMu24_v.*"
                    //int trigVtype2 =  Vtype == TTH::EventHypothesis::mun && ( triggerFlags[20]>0 || triggerFlags[21]>0 || triggerFlags[25]>0 ||triggerFlags[26]>0 ));

                    // OR of two trigger paths:   "HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v.*", "HLT_Ele27_WP80_v.*"
                    //int trigVtype3 =  Vtype == TTH::EventHypothesis::en && triggerFlags[44]>0;

                    // for the moment, don't cut on trigger bit (save and cut offline)
                    int trigVtype2 = 1;
                    int trigVtype3 = 1;

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
                            otree->triggerErr_ = comb;

                            if( debug>=2 ) {
                                cout << "Vtype2: Trigger error: (" << leptonLV.Pt() << "," << leptonLV.Eta() << ")" << endl;
                                cout << " - scale_id = " << scale_id << " +/- " << scale_id*id << endl;
                                cout << " - scale_tr = " << scale_tr << " +/- " << scale_tr*tr << endl;
                                cout << " - comb = " << comb << endl;
                                cout << " - triggerWeight = " << otree->trigger_ << ", from files: " << (scale_id*scale_tr) << endl;
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
                            otree->triggerErr_ = comb;

                            if( debug>=2 ) {
                                cout << "Vtype3: Trigger error: (" << leptonLV.Pt() << "," << leptonLV.Eta() << ")" << endl;
                                cout << " - scale_id = " << scale_id << " +/- " << scale_id*id << endl;
                                cout << " - scale_tr = " << scale_tr << " +/- " << scale_tr*tr << endl;
                                cout << " - comb = " << comb << endl;
                                cout << " - triggerWeight = " << otree->trigger_ << ", from files: " << (scale_id*scale_tr) << endl;
                            }
                        }
                    }

                    if( debug>=2 ) {
                        cout << "nvlep=" << itree->n__lep << ", Vtype=" << Vtype << endl;
                        cout << "Lep sel. Vtype2 = " << lepSelVtype2 << ", lep sel. Vtype3 = " << lepSelVtype3 << endl;
                        cout << "Trigger: " <<  ((isMC ? 1 : trigVtype2) || (isMC ? 1 : trigVtype3)) << endl;
                        cout << "Passes = " << int (properEventSL) << " SL" << endl;
                    }

                    // save lepton kinematics...
                    otree->nLep_ = 1;

                    otree->lepton_pt_     [0] = leptonLV.Pt();
                    otree->lepton_eta_    [0] = leptonLV.Eta();
                    otree->lepton_phi_    [0] = leptonLV.Phi();
                    otree->lepton_m_      [0] = leptonLV.M();
                    otree->lepton_charge_ [0] = itree->lep__charge[lepton_idx];
                    otree->lepton_rIso_   [0] = itree->lep__rel_iso[lepton_idx];
                    otree->lepton_type_   [0] = itree->lep__type[lepton_idx];
                    otree->lepton_dxy_    [0] = itree->lep__dxy[lepton_idx];
                    otree->lepton_dz_     [0] = itree->lep__dz[lepton_idx];
                    //otree->gen_lepton_pt  [0] = itree->gen_lep__pt[lepton_idx];
                    //otree->gen_lepton_eta [0] = itree->gen_lep__eta[lepton_idx];
                    //otree->gen_lepton_phi [0] = itree->gen_lep__phi[lepton_idx];
                    //otree->gen_lepton_m   [0] = itree->gen_lep__m[lepton_idx];
                    //otree->gen_lepton_id  [0] = itree->gen_lep__id[lepton_idx];
                    //FIXME
                    //otree->lepton_wp80_   [0] = vLepton_wp80[0];
                    //otree->lepton_wp95_   [0] = vLepton_wp95[0];
                    //otree->lepton_wp70_   [0] = vLepton_wp70[0];
                    //otree->lepton_MVAtrig_[0] = vLepton_idMVAtrig[0];

                    if ( isMC && Vtype == TTH::EventHypothesis::en) // if single electron events
                        otree->sf_ele_ = eleSF( otree->lepton_pt_[0], otree->lepton_eta_[0]);
                    else
                        otree->sf_ele_ = 1;
                }

                ///////////////////////////////////
                //         DL events:  mm/ee     //
                ///////////////////////////////////

                properEventDL = false;
                if((ENABLE_MM && Vtype == TTH::EventHypothesis::mumu) || (ENABLE_EE && Vtype == TTH::EventHypothesis::ee)) {


                    //sig_lep always contain 2 leptons
                    leptonLV.SetPtEtaPhiM (itree->sig_lep__pt[0], itree->sig_lep__eta[0], itree->sig_lep__phi[0], itree->sig_lep__mass[0]);
                    const int lep_idx_1 = itree->sig_lep__idx[0];
                    lep_index.push_back(0);

                    leptonLV2.SetPtEtaPhiM(itree->sig_lep__pt[1], itree->sig_lep__eta[1], itree->sig_lep__phi[1], itree->sig_lep__mass[1]);
                    const int lep_idx_2 = itree->sig_lep__idx[1];
                    lep_index.push_back(1);

                    //FIXME: hardcoded masses
                    if(doGenLevelAnalysis) {
                        if( itree->gen_lep__pt[0]>5.)
                            leptonLV. SetPtEtaPhiM(itree->gen_lep__pt[lep_idx_1], itree->gen_lep__eta[lep_idx_1], itree->gen_lep__phi[lep_idx_1], (itree->lep__type[lep_idx_1]==13 ? MU_MASS : ELE_MASS ) );
                        else
                            leptonLV. SetPtEtaPhiM( 5., 0., 0., 0. );
                        if( itree->gen_lep__pt[1]>5.)
                            leptonLV2.SetPtEtaPhiM(itree->gen_lep__pt[lep_idx_2], itree->gen_lep__eta[lep_idx_2], itree->gen_lep__phi[lep_idx_2], (itree->lep__type[lep_idx_2]==13 ? MU_MASS : ELE_MASS ) );
                        else
                            leptonLV2.SetPtEtaPhiM( 5., 0., 0., 0. );
                    }
                    
                    if (debug>3) {
                        cout << "EE/MM "
                            << "idx " << lep_idx_1 << " " << lep_idx_2 << " " 
                            << "type " << itree->lep__type[lep_idx_1] << " "
                            << itree->lep__type[lep_idx_2] << " "
                            << "pt " << itree->lep__pt[lep_idx_1] << " "
                            << itree->lep__pt[lep_idx_2] << " "
                            << "riso " << itree->lep__rel_iso[lep_idx_1] << " "
                            << itree->lep__rel_iso[lep_idx_2] << " "
                            << "dxy " << itree->lep__dxy[lep_idx_1] << " "
                            << itree->lep__dxy[lep_idx_2] << " "
                            << "q " << itree->sig_lep__charge[lep_idx_1] << " "
                            << itree->sig_lep__charge[lep_idx_2] << endl;
                    }


                    // cut on leptons (DL)
                    int lepSelVtype0 = ( Vtype == TTH::EventHypothesis::mumu && itree->sig_lep__type[0]==13 && itree->sig_lep__type[1]==13 &&
                                         ( (leptonLV.Pt() >20 && TMath::Abs(leptonLV.Eta()) < muEtaTight && itree->lep__rel_iso[lep_idx_1]<lepIsoTight) ||
                                           (leptonLV2.Pt()>20 && TMath::Abs(leptonLV2.Eta()) < muEtaTight && itree->lep__rel_iso[lep_idx_1]<lepIsoTight) )
                                       ) && itree->sig_lep__charge[0] * itree->sig_lep__charge[1]<0;

                    //FIXME, removed lepton WP
                    //int lepSelVtype1 = ( Vtype==1 && itree->lep__type[0]==11 && itree->lep__type[1]==11 &&
                    //                     ( (leptonLV.Pt() >20 && itree->lep__rel_iso[0]<lepIsoTight && vLepton_wp95[0]>0.5 && TMath::Abs(itree->lep__dxy[0])<0.02) ||
                    //                       (leptonLV2.Pt()>20 && itree->lep__rel_iso[1]<lepIsoTight && vLepton_wp95[1]>0.5 && TMath::Abs(itree->lep__dxy[1])<0.02) )
                    //                   ) && itree->lep__charge[0]*itree->lep__charge[1]<0;
                    int lepSelVtype1 = ( Vtype == TTH::EventHypothesis::ee && itree->sig_lep__type[0] == 11 && itree->sig_lep__type[1]==11 &&
                                         ( (leptonLV.Pt() >20 && itree->lep__rel_iso[lep_idx_1] < lepIsoTight && TMath::Abs(itree->lep__dxy[lep_idx_1]) < 0.02) ||
                                           (leptonLV2.Pt()>20 && itree->lep__rel_iso[lep_idx_2] < lepIsoTight && TMath::Abs(itree->lep__dxy[lep_idx_2]) < 0.02) )
                                       ) && itree->sig_lep__charge[0]*itree->sig_lep__charge[1] < 0;

                    //FIXME: need to implement trigger bits
                    // OR of four trigger paths:  "HLT_Mu40_eta2p1_v.*", "HLT_IsoMu24_eta2p1_v.*", "HLT_Mu40_v.*",  "HLT_IsoMu24_v.*"
                    //int trigVtype0 =  (Vtype == TTH::EventHypothesis::mumu && ( triggerFlags[21]>0 || triggerFlags[26]>0 || triggerFlags[20]>0 ||triggerFlags[25]>0 ));

                    // OR of two trigger paths:    "HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v.*", "HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v.*"
                    //int trigVtype1 =  (Vtype == TTH::EventHypothesis::ee && ( triggerFlags[42]>0 || triggerFlags[42]>0 ) );

                    // for the moment, don't cut on trigger bit (save and cut offline)
                    int trigVtype0 = 1;
                    int trigVtype1 = 1;
                    
                    if (debug>3) {
                        cout << "EE/MM " << lepSelVtype0 << " " << lepSelVtype1 << endl;    
                    }

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
                            otree->triggerErr_ = comb;

                            if( debug>=2 ) {
                                cout << "Vtype0: Trigger error: (" << leptonLV.Pt() << "," << leptonLV.Eta() << " ; " << leptonLV2.Pt() << "," << leptonLV2.Eta() << ")" << endl;
                                cout << " - scale_id1 = " << scale_id1 << " +/- " << scale_id1*id1 << endl;
                                cout << " - scale_id2 = " << scale_id2 << " +/- " << scale_id2*id2 << endl;
                                cout << " - scale_tr = " << scale_tr << " +/- " << scale_tr*tr << endl;
                                cout << " - comb = " << comb << endl;
                                cout << " - triggerWeight = " << otree->trigger_ << ", from files: " << (scale_id1*scale_id2*scale_tr) << endl;
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
                            otree->triggerErr_ = comb;

                            if( debug>=2 ) {
                                cout << "Vtype1: Trigger error: (" << leptonLV.Pt() << "," << leptonLV.Eta() << " ; " << leptonLV2.Pt() << "," << leptonLV2.Eta() << ")" << endl;
                                cout << " - scale_id1 = " << scale_id1 << " +/- " << scale_id1*id1 << endl;
                                cout << " - scale_id2 = " << scale_id2 << " +/- " << scale_id2*id2 << endl;
                                cout << " - scale_tr = " << scale_tr << " +/- " << scale_tr*tr << endl;
                                cout << " - comb = " << comb << endl;
                                cout << " - triggerWeight = " << otree->trigger_ << ", from files: " << (scale_id1*scale_id2*scale_tr) << endl;
                            }

                        }
                    }

                    if( debug>=2 ) {
                        cout << "nvlep=" << itree->n__lep << ", Vtype=" << Vtype << endl;
                        //FIXME: mismatch between type names(?)
                        cout << "Lep sel. Vtype2 = " << lepSelVtype0 << ", lep sel. Vtype3 = " << lepSelVtype1 << endl;
                        cout << "Trigger: " <<  ((isMC ? 1 : trigVtype0) || (isMC ? 1 : trigVtype1)) << endl;
                        cout << "Passes = " << int (properEventDL) << " DL ee/mm" << endl;
                    }

                    // save lepton(s) kinematics into the tree...
                    otree->nLep_ = 2;

                    // lep 1...
                    otree->lepton_pt_     [0] = leptonLV.Pt();
                    otree->lepton_eta_    [0] = leptonLV.Eta();
                    otree->lepton_phi_    [0] = leptonLV.Phi();
                    otree->lepton_m_      [0] = leptonLV.M();
                    otree->lepton_charge_ [0] = itree->lep__charge[lep_idx_1];
                    otree->lepton_rIso_   [0] = itree->lep__rel_iso[lep_idx_1];
                    otree->lepton_type_   [0] = itree->lep__type[lep_idx_1];
                    otree->lepton_dxy_    [0] = itree->lep__dxy[lep_idx_1];
                    otree->lepton_dz_     [0] = itree->lep__dz[lep_idx_1];
                    //otree->gen_lepton_pt  [0] = itree->gen_lep__pt[lep_idx_1];
                    //otree->gen_lepton_eta [0] = itree->gen_lep__eta[lep_idx_1];
                    //otree->gen_lepton_phi [0] = itree->gen_lep__phi[lep_idx_1];
                    //otree->gen_lepton_m   [0] = itree->gen_lep__m[lep_idx_1];
                    //otree->gen_lepton_id  [0] = itree->gen_lep__id[lep_idx_1];
                    //FIXME: need to add ID-s
                    //otree->lepton_wp70_   [0] = vLepton_wp70[0];
                    //otree->lepton_wp80_   [0] = vLepton_wp80[0];
                    //otree->lepton_wp95_   [0] = vLepton_wp95[0];
                    //otree->lepton_MVAtrig_[0] = vLepton_idMVAtrig[0];

                    // lep 2...
                    otree->lepton_pt_     [1] = leptonLV2.Pt();
                    otree->lepton_eta_    [1] = leptonLV2.Eta();
                    otree->lepton_phi_    [1] = leptonLV2.Phi();
                    otree->lepton_m_      [1] = leptonLV2.M();
                    otree->lepton_charge_ [1] = itree->lep__charge[lep_idx_2];
                    otree->lepton_rIso_   [1] = itree->lep__rel_iso[lep_idx_2];
                    otree->lepton_type_   [1] = itree->lep__type[lep_idx_2];
                    otree->lepton_dxy_    [1] = itree->lep__dxy[lep_idx_2];
                    otree->lepton_dz_     [1] = itree->lep__dz[lep_idx_2];
                    //otree->gen_lepton_pt  [0] = itree->gen_lep__pt[lep_idx_2];
                    //otree->gen_lepton_eta [0] = itree->gen_lep__eta[lep_idx_2];
                    //otree->gen_lepton_phi [0] = itree->gen_lep__phi[lep_idx_2];
                    //otree->gen_lepton_m   [0] = itree->gen_lep__m[lep_idx_2];
                    //otree->gen_lepton_id  [0] = itree->gen_lep__id[lep_idx_2];
                    //otree->lepton_wp80_   [1] = vLepton_wp80[1];
                    //otree->lepton_wp70_   [1] = vLepton_wp70[1];
                    //otree->lepton_wp95_   [1] = vLepton_wp95[1];
                    //otree->lepton_MVAtrig_[1] = vLepton_idMVAtrig[1];

                    if ( isMC && Vtype==TTH::EventHypothesis::ee ) // if di-electron events
                        otree->sf_ele_ = eleSF( otree->lepton_pt_[0], otree->lepton_eta_[0]) * eleSF( otree->lepton_pt_[1], otree->lepton_eta_[1]);
                    else
                        otree->sf_ele_ = 1;

                }


                ///////////////////////////////////
                //         DL events:  em        //
                ///////////////////////////////////

                if( ENABLE_EM && Vtype==TTH::EventHypothesis::emu) {

                    // flag these events with different type
                    //otree->type_ = 4;

                    // first lepton...
                    leptonLV.SetPtEtaPhiM (itree->sig_lep__pt[0], itree->sig_lep__eta[0], itree->sig_lep__phi[0], itree->sig_lep__mass[0]);
                    lep_index.push_back(0);
                    const int lep_idx_1 = itree->sig_lep__idx[0];
                    
                    //// second lepton...
                    leptonLV2.SetPtEtaPhiM (itree->sig_lep__pt[1], itree->sig_lep__eta[1], itree->sig_lep__phi[1], itree->sig_lep__mass[1]);
                    lep_index.push_back(1);
                    const int lep_idx_2 = itree->sig_lep__idx[1];

                    if(doGenLevelAnalysis) {
                        if( itree->gen_lep__pt[0] > 5.0) {
                            leptonLV.SetPtEtaPhiM(
                                itree->gen_lep__pt[lep_idx_1],
                                itree->gen_lep__eta[lep_idx_1],
                                itree->gen_lep__phi[lep_idx_1],
                                (itree->lep__type[lep_idx_1]==13 ? MU_MASS : ELE_MASS )
                            );
                        } else {
                            leptonLV.SetPtEtaPhiM( 5., 0., 0., 0. );
                        }
                        if( itree->gen_lep__pt[lep_idx_2] > 5.0 ) {
                            leptonLV2.SetPtEtaPhiM(
                                itree->gen_lep__pt[lep_idx_2],
                                itree->gen_lep__eta[lep_idx_2],
                                itree->gen_lep__phi[lep_idx_2],
                                (itree->gen_lep__type[lep_idx_2]==13 ? MU_MASS : ELE_MASS )
                            );
                        } else {
                            leptonLV2.SetPtEtaPhiM( 5., 0., 0., 0. );
                        }
                    }

                    //First lepton is mu
                    //FIXME: if electron is the first, does not work
                    int lepSelVtype4 = (Vtype == TTH::EventHypothesis::emu && (
                        (itree->sig_lep__type[0] == 13 && itree->sig_lep__type[1] == 11) ||
                        (itree->sig_lep__type[0] == 11 && itree->sig_lep__type[1] == 13)) &&
                        (leptonLV.Pt() > 20 && TMath::Abs(leptonLV.Eta()) < muEtaTight && itree->lep__rel_iso[lep_idx_1] < lepIsoTight) &&
                        itree->sig_lep__charge[0] * itree->sig_lep__charge[1]<0
                    );

                    // OR of four trigger paths:  "HLT_Mu40_eta2p1_v.*", "HLT_IsoMu24_eta2p1_v.*", "HLT_Mu40_v.*",  "HLT_IsoMu24_v.*"
                    //int trigVtype4 =  (Vtype == TTH::EventHypothesis::emu && ( triggerFlags[21]>0 || triggerFlags[26]>0 || triggerFlags[20]>0 ||triggerFlags[25]>0 ));

                    // for the moment, don't cut on trigger bit (save and cut offline)
                    int trigVtype4 = 1;

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

                            otree->triggerErr_ = comb;

                            if( debug>=2 ) {
                                cout << "Vtype4: Trigger error: (" << leptonLV.Pt() << "," << leptonLV.Eta() << " ; " << leptonLV2.Pt() << "," << leptonLV2.Eta() << ")" << endl;
                                cout << " - scale_id1 = " << scale_id1 << " +/- " << scale_id1*id1 << endl;
                                cout << " - scale_id2 = " << scale_id2 << " +/- " << scale_id2*id2 << endl;
                                cout << " - scale_tr = " << scale_tr1 << " +/- " << scale_tr1*tr1 << endl;
                                cout << " - comb = " << comb << endl;
                                cout << " - triggerWeight = " << otree->trigger_ << ", from files: " << (scale_id1*scale_tr1) << endl;
                            }

                            // because events are selected from a subset of Vtype2
                            otree->trigger_   *= (scale_id2*scale_tr2);

                        }
                    }

                    if( debug>=2 ) {
                        cout << "nvlep=" << itree->n__lep << ", Vtype=" << Vtype << endl;
                        cout << "Lep sel. Vtype4 = " << lepSelVtype4 << endl;
                        cout << "Trigger: " <<  (isMC ? 1 : trigVtype4)  << endl;
                        cout << "Passes = " << int (properEventDL) << " DL em" << endl;
                    }

                    // save lepton(s) kinematics into the tree...
                    otree->nLep_ = 2;

                    //FIXME: need the correct index
                    // lep 1...
                    otree->lepton_pt_     [0] = leptonLV.Pt();
                    otree->lepton_eta_    [0] = leptonLV.Eta();
                    otree->lepton_phi_    [0] = leptonLV.Phi();
                    otree->lepton_m_      [0] = leptonLV.M();
                    otree->lepton_charge_ [0] = itree->lep__charge[lep_idx_1];
                    otree->lepton_rIso_   [0] = itree->lep__rel_iso[lep_idx_1];
                    otree->lepton_type_   [0] = itree->lep__type[lep_idx_1];
                    otree->lepton_dxy_    [0] = itree->lep__dxy[lep_idx_1];
                    otree->lepton_dz_     [0] = itree->lep__dz[lep_idx_1];

                    // lep 2...
                    otree->lepton_pt_     [1] = leptonLV2.Pt();
                    otree->lepton_eta_    [1] = leptonLV2.Eta();
                    otree->lepton_phi_    [1] = leptonLV2.Phi();
                    otree->lepton_m_      [1] = leptonLV2.M();
                    otree->lepton_charge_ [1] = itree->lep__charge[lep_idx_2];
                    otree->lepton_rIso_   [1] = itree->lep__rel_iso[lep_idx_2];
                    otree->lepton_type_   [1] = itree->lep__type[lep_idx_2];
                    otree->lepton_dxy_    [1] = itree->lep__dxy[lep_idx_2];
                    otree->lepton_dz_     [1] = itree->lep__dz[lep_idx_2];
                    //FIXME: add working points
                    //otree->lepton_wp80_   [1] = aLepton_wp80[lep_idx_2];
                    //otree->lepton_wp95_   [1] = aLepton_wp95[lep_idx_2];

                    //FIXME: =4 correct?
                    if ( isMC && Vtype == 4 ) { // if EM events with triggered muon
                        otree->sf_ele_ = eleSF( otree->lepton_pt_[1], otree->lepton_eta_[1]);
                    } else {
                        otree->sf_ele_ = 1;
                    }

                } // end dilepton, electron muon


                if ( !isMC && otree->EVENT_.json < 0.5 ) {
                    if ( debug>=2 )
                        cout << "Event rejected: not present in json file"<<endl;
                    continue;
                }

                // continue if leptons do not satisfy cuts
                if(!(properEventSL || properEventDL) ) {
                    if (cutLeptons) {
                        if( debug>=2 ) {
                            cout << "Rejected by lepton selection" << endl ;
                            cout << " => go to next event!" << endl;
                            cout << "******************************" << endl;
                        }
                        cuts.fill(CutHistogram::Cuts::LEPTONS);
                        continue;
                    }
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

                    // loop over jets
                    for(int hj = 0; hj < itree->n__jet; hj++) {

                        float ptGen = DEF_VAL_FLOAT;

                        if(itree->gen_jet__pt[hj]>0.) ptGen = itree->gen_jet__pt[hj];

                        float pt     = itree->jet__pt[hj];
                        float eta    = itree->jet__eta[hj];
                        float phi    = itree->jet__phi[hj];
                        float e      = itree->jet__energy[hj];
                        float m2     = e*e - pt*pt*TMath::CosH(eta)*TMath::CosH(eta);

                        if(m2<0) {
                            cerr << "jet " << hj << " m2 " << m2 << " " << pt << " " << eta << " " << phi << " " << e << endl;
                            m2 = 0.;
                        }

                        float m      = TMath::Sqrt( m2 );

                        int flavour  = itree->jet__id[hj];
                        //FIXME: jet pile-up ID
                        //int pass_pu_id    = itree->jet__pass_pileupJetId[hj];
                        float pu_id    = itree->jet__pileupJetId[hj];
                        int id       = itree->jet__jetId[hj];

                        //FIXME: where to get JEC uncertainty?
                        //float JECUnc = hJet_JECUnc  [hj];
                        float JECUnc = 0.; // this has no effect

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
                        
                        const double csv_val = (bdisc == 0 ? itree->jet__bd_cisvv2[hj] : itree->jet__bd_csv[hj]);
                        if (debug>3) {
                            cout << "jet " << pt << " " << eta << " " << phi << " " << id << " " << pu_id << " " << csv_val << endl;
                        }

                        // only jets in acceptance...
                        if( TMath::Abs(eta)> 2.5 ) continue;

                        //FIXME: disabled jet PU ID and jet ID
                        //// only jets passing pu ID...
                        //if( pass_pu_id != 1 ) continue;

                        //// only jets passing id ID...
                        //Jet ID now a boolean
                        //if( id < 0.5 ) continue;
                        //if( id != 1 ) continue;

                        // only jets above pt cut...
                        if( pt < jetPtThreshold  ) continue;

                        otree->hJetAmong_++;

                        // the jet four-vector
                        TLorentzVector p4;
                        p4.SetPtEtaPhiM( pt, eta, phi, m );

                        // for csv systematics
                        float csv_nominal =  csv_val;
                        //float csv_upBC    =  hJet_csv_upBC   [hj]
                        //float csv_downBC  =  hJet_csv_downBC [hj]
                        //float csv_upL     =  hJet_csv_upL    [hj]
                        //float csv_downL   =  hJet_csv_downL  [hj]
                        //FIXME: jet b-discriminator systematics
                        const float csv_upBC    = DEF_VAL_FLOAT;
                        const float csv_downBC  = DEF_VAL_FLOAT;
                        const float csv_upL     = DEF_VAL_FLOAT;
                        const float csv_downL   = DEF_VAL_FLOAT;

                        // default is csv_nominal ( <=> reshaped )
                        float csv = csv_nominal;

                        // if doing cvs systematiics, use appropriate collection
                        if( doCSVup  ) {
                            csv = TMath::Max(csv_upBC, csv_upL);
                        }
                        else if( doCSVdown) {
                            csv = TMath::Min(csv_downBC, csv_downL);
                        }

                        // if we apply SF for b-tag, or it is data, then deafult is 'reco' csv
                        if( useCSVcalibration || !isMC ) {
                            csv = csv_val;
                        }

                        // if using thr MVA btagger:
                        if( useCMVA ) {

                            // this is needed to remove the spike at zero! FIXME
                            if( csv>0. )
                                //FIXME: what is cmva
                                //csv = hJet_cmva[hj];
                                csv = DEF_VAL_FLOAT;
                            else {
                                csv = 0.;
                            }
                        }


                        //disable MC enhancment for now
                        //if( enhanceMC && trial_success==0) {

                        //    string bin = "";
                        //    if( TMath::Abs( eta ) <= 1.0 )
                        //        bin = "Bin0";
                        //    if( TMath::Abs( eta ) >  1.0 )
                        //        bin = "Bin1";

                        //    string fl = "";
                        //    if(abs(flavour)==5)
                        //        fl = "b";
                        //    if(abs(flavour)==4)
                        //        fl = "c";
                        //    else
                        //        fl = "l";

                        //    csv     =  btagger[fl+"_"+bin]->GetRandom();

                        //    if(coll==0) {

                        //        //FIXME: what is the difference between hJet_csv and hJet_csv_nominal?
                        //        hJet_csv        [hj] = csv;
                        //        hJet_csv_nominal[hj] = csv;
                        //    }
                        //    if(coll==1) {
                        //        aJet_csv        [hj] = csv;
                        //        aJet_csv_nominal[hj] = csv;
                        //    }
                        //}

                        // the jet observables (p4 and csv)
                        JetObservable myJet;
                        myJet.p4     = p4;
                        myJet.csv    = csv;
                        //FIXME
                        //myJet.index  = (coll==0 ? hj : -hj-1);
                        myJet.index  = hj;
                        myJet.shift  = shift;
                        myJet.flavour= flavour;

                        // push back the jet...
                        jet_map.push_back    ( myJet );

                        if( debug>=3 ) {
                            cout << "Jet #" << hj << " => (" << pt << "," << eta << "," << phi << "," << m << "), ID=" << id << ", PU-ID=" << pu_id << ", csv = " << csv << ", flavour=" << flavour << endl;
                        }

                    }
                }
                // if doing the gen level analysis, read gen-jets
                else {

                    // reset everything
                    jet_map.clear();

                    // reset the sumEt
                    otree->MET_sumEt_ = 0.;

                    // loop over jets
                    for(int hj = 0; hj < itree->n__jet; hj++) {

                        float pt     = itree->gen_jet__pt [hj];
                        float eta    = itree->gen_jet__eta[hj];
                        float phi    = itree->gen_jet__phi[hj];
                        // assume massless jets
                        // (unfortunately necessary because the mass of the genJet is not saved)
                        float e      = itree->gen_jet__pt [hj]*TMath::CosH(itree->gen_jet__eta[hj]);
                        float m      = 0.;

                        float flavor = itree->jet__id [hj];

                        // only jets in acceptance
                        // (this is needed because the TF and csv shapes are valid only in the acceptance)
                        if( TMath::Abs(eta) > 2.5 ) continue;

                        if( debug>=3 ) {
                            cout << "Gen-Jet #" << hj << " => (" << pt << "," << eta << "," << phi << "," << m  << "), flavor=" << flavor << endl;
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
                        otree->MET_sumEt_ += pt;

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
                        myJet.p4      = p4;
                        myJet.csv     = csv;
                        myJet.flavour = flavor;
                        //FIXME
                        //myJet.index  = (coll==0 ? hj : -hj-1);
                        myJet.index  = hj;
                        myJet.shift  = 1.0;

                        // push back the jet...
                        jet_map.push_back(myJet);

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
                        cout << "MET (from invisible) = (" << otree->MET_pt_ << "," << otree-> MET_phi_ << ")" << endl;
                    }

                    // save smeared MET kinematics into the tree...
                    otree->MET_pt_    = neutrinoLV.Pt();
                    otree->MET_phi_   = neutrinoLV.Phi();

                    if( debug>=3 ) {
                        cout << "MET (smear) = (" << otree->MET_pt_ << "," << otree->MET_phi_ << ")" << endl;
                    }


                }


                ////////////////////////////////////////////////////////////////////////

                // MET
                //float nuPx = METtype1p2corr.et*TMath::Cos(METtype1p2corr.phi);
                //float nuPy = METtype1p2corr.et*TMath::Sin(METtype1p2corr.phi);
                float nuPx = itree->met__pt * TMath::Cos(itree->met__phi);
                float nuPy = itree->met__pt * TMath::Sin(itree->met__phi);

                // correct for JEC
                nuPx -= deltaPx;
                nuPy -= deltaPy;

                float nuE  = TMath::Sqrt(nuPx*nuPx+nuPy*nuPy);
                if( doGenLevelAnalysis==0 ) neutrinoLV.SetPxPyPzE(nuPx,nuPy,0. ,nuE);

                if( doGenLevelAnalysis==0 ) {
                    // save MET kinematics into the tree...
                    otree->MET_pt_    = neutrinoLV.Pt();
                    otree->MET_phi_   = neutrinoLV.Phi();

                    //FIXME: what is the difference between et and sumet for MET?
                    //otree->MET_sumEt_ = METtype1p2corr.sumet;
                    otree->MET_sumEt_ = DEF_VAL_FLOAT;
                }

                // save invisible particles kinematics into the tree...
                otree->Nus_pt_    = INVISIBLE.Pt();
                otree->Nus_phi_   = INVISIBLE.Phi();

                // save di-lepton mass
                if( properEventSL ) {
                    TLorentzVector l;
                    l.SetPtEtaPhiM( otree->lepton_pt_[0], otree->lepton_eta_[0], otree->lepton_phi_[0], otree->lepton_m_[0]);
                    TLorentzVector n;
                    n.SetPtEtaPhiM( otree->MET_pt_, 0., otree->MET_phi_, 0.);
                    otree->MTln_ = (l+n).Mt();
                }
                if( properEventDL ) {
                    TLorentzVector l1;
                    l1.SetPtEtaPhiM( otree->lepton_pt_[0], otree->lepton_eta_[0], otree->lepton_phi_[0], otree->lepton_m_[0]);
                    TLorentzVector l2;
                    l2.SetPtEtaPhiM( otree->lepton_pt_[1], otree->lepton_eta_[1], otree->lepton_phi_[1], otree->lepton_m_[1]);
                    otree->Mll_  = (l1+l2).M();
                }



                ////////////////////////////////////////////////////////////////////////


                // order jet list by Pt
                std::sort( jet_map.begin(),     jet_map.end(),     JetObservableListerByPt() );

                // if use btag shape, order by decreasing CSV
                // <=> when considering only a subset of the jets, this ensures that the combination
                // obtained from CSVM only jets is among those considered
                if( selectByBTagShape || recoverTopBTagBin) {
                    std::sort( jet_map.begin(),   jet_map.end(),     JetObservableListerByCSV() );
                }

                for( int csv_sys = 0; csv_sys < 19 ; csv_sys++) {
                    double csv_syst_value = 1.0;
                    if( useCSVcalibration ) {
                        csv_syst_value = GetCSVweight( jet_map, static_cast<sysType>(csv_sys), h_csv_wgt_hf, c_csv_wgt_hf, h_csv_wgt_lf);
                    }
                    otree->weightCSV_[ csv_sys ] = csv_syst_value;
                }

                // fill arrays of jets
                std::vector<TLorentzVector>    jets_p4;
                std::vector<TLorentzVector>    jets_p4_reg;

                std::vector<double>            jets_csv;
                std::vector<double>            jets_csv_prob_b;
                std::vector<double>            jets_csv_prob_c;
                std::vector<double>            jets_csv_prob_j;

                std::vector<int>               jets_index;
                std::vector<int>               jets_flavour;

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
                    int flavour = jet_map[jj].flavour;

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

                    jets_flavour.push_back(flavour);

                    jets_csv_prob_b.push_back( btagger["b_"+bin]!=0 ? btagger["b_"+bin]->GetBinContent( btagger["b_"+bin]->FindBin( csv ) ) : 1.);
                    jets_csv_prob_c.push_back( btagger["c_"+bin]!=0 ? btagger["c_"+bin]->GetBinContent( btagger["c_"+bin]->FindBin( csv ) ) : 1.);
                    jets_csv_prob_j.push_back( btagger["l_"+bin]!=0 ? btagger["l_"+bin]->GetBinContent( btagger["l_"+bin]->FindBin( csv ) ) : 1.);

                }

                otree->jetsAboveCut_ = jetsAboveCut;

                // continue if not enough jets
                if(otree->jetsAboveCut_<jetMultLoose ) {
                    if( debug>=2 ) {
                        cout << "Rejected by min jet cut (>= " <<jetMultLoose << " jets above " << jetPtLoose << " GeV)" << endl ;
                        cout << " => go to next event!" << endl;
                        cout << "******************************" << endl;
                    }
                    if (cutJets) { 
                        cuts.fill(CutHistogram::Cuts::JETS);
                        continue;
                    }
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
                    if( pt_k>jetPtThreshold ) {
                        banytag_indices.push_back( k );
                    }

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

                otree->numBTagL_ = numJets30BtagL;
                otree->numBTagM_ = numJets30BtagM;
                otree->numBTagT_ = numJets30BtagT;
                otree->numJets_  = ( numJets30BtagM + numJets30UntagM);

                if( debug>=2 ) {
                    cout << "numBTagM = " << otree->numBTagM_ << endl;
                    cout << "numJets = "  << otree->numJets_ << endl;
                }

                /* @@@@@@@@@@@@@@@@@@@@@@@@ JET RE-ORDERING BY CSV PROB @@@@@@@@@@@@@@@@@@@@@@@@@@  */

                // in case the jet collections is reshuffled using the b-probability, keep a copy of old selection
                // (for debugging purposes)
                vector<unsigned int> btag_indices_backup   = btag_indices;
                vector<unsigned int> buntag_indices_backup = buntag_indices;

                // variable that flags events passing or failing the b-probability cut
                int passes_btagshape = 0;

                //LH ratio
                if( /*selectByBTagShape &&*/ useBtag &&               // run this only if specified AND...
                    ((properEventSL && banytag_indices.size()>=5) ||  // [ run this only if SL and at least 5 jets OR...
                    (properEventDL && banytag_indices.size()>=4)) ) { //   run this only if DL and at least 4 jets ]

                    // map that transforms the indices into the permutation convention
                    std::map< unsigned int, unsigned int> btag_map;
                    btag_map.clear();

                    // number of inequivalent permutations
                    int nS=0, nB=0;

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
                    else if (cutBTagShape) {
                        if (debug >= 2) {
                            cout << "Inconsistency in selectByBTagShape... continue" << endl;
                            cout << " => go to next event!" << endl;
                            cout << "******************************" << endl;
                        }
                        cuts.fill(CutHistogram::Cuts::BTAGSHAPE);
                        continue;
                    }


                    // loop over hypothesis [ TTH, TTbb ]
                    for(int hyp = 0 ; hyp<2;  hyp++) {

                        if (debug >= 2) {
                            cout << "hypothesis loop " << hyp << endl;
                        }
                        // list of permutations
                        const int* permutList = 0;
                        if( btag_flag == 0 ) permutList = hyp==0 ?  permutations_6J_S : permutations_6J_B;
                        if( btag_flag == 1 ) permutList = hyp==0 ?  permutations_5J_S : permutations_5J_B;
                        if( btag_flag == 2 ) permutList = hyp==0 ?  permutations_4J_S : permutations_4J_B;

                        // loop over permutations
                        for(unsigned int pos = 0; pos < (unsigned int)( hyp==0 ? nS : nB ) ; pos++) {

                            if (debug >= 2) {
                                cout << "permutation loop " << pos << endl;
                            }


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
                           
#ifdef DO_BTAG_LR_TREE
                            double id_bLep =  jets_flavour[  btag_map[bLep_pos] ];
                            double id_bHad =  jets_flavour[  btag_map[bHad_pos] ];
                            double id_b1   =  jets_flavour[  btag_map[b1_pos]   ];
                            double id_b2   =  jets_flavour[  btag_map[b2_pos]   ];
                            double id_w1   =  jets_flavour[  btag_map[w1_pos]   ];
                            double id_w2   =  jets_flavour[  btag_map[w2_pos]   ];
#endif //btag lr tree

                            // the total probability
                            float p_pos = 0.;

                            // if signal (ttbb)
                            if( hyp==0 ) {
                                p_pos =  p_b_bLep * p_b_bHad * p_b_b1 * p_b_b2 * p_j_w1 * p_j_w2;
                                p_bb += p_pos;

                                // look for a global maximum
                                if(  p_pos > max_p_bb ) {
                                    max_p_bb      = p_pos;
                                    selected_comb = pos;
                                }
                            }

                            // if background (ttjj)
                            if( hyp==1 ) {
                                p_bb += p_pos;

                                p_pos =  p_b_bLep * p_b_bHad * p_j_b1 * p_j_b2 * p_j_w1 * p_j_w2;
                                p_jj += p_pos;
                            }

#ifdef DO_BTAG_LR_TREE
                            btag_tree.permutation = permutList[pos];
                            btag_tree.event = counter;
                            btag_tree.event_run = itree->event__run;
                            btag_tree.event_lumi = itree->event__lumi;
                            btag_tree.event_id = itree->event__id;
                            btag_tree.syst = syst;
                            btag_tree.permutation_pos = pos;
                            btag_tree.bLep_pos = bLep_pos;
                            btag_tree.w1_pos = w1_pos;
                            btag_tree.w2_pos = w2_pos;
                            btag_tree.bHad_pos = bHad_pos;
                            btag_tree.b1_pos = b2_pos;
                            
                            btag_tree.jets_bLep_pos = btag_map[bLep_pos];
                            btag_tree.jets_w1_pos = btag_map[w1_pos];
                            btag_tree.jets_w2_pos = btag_map[w2_pos];
                            btag_tree.jets_bHad_pos = btag_map[bHad_pos];
                            btag_tree.jets_b1_pos = btag_map[b2_pos];
                            
                            btag_tree.p_b_bLep = p_b_bLep;
                            btag_tree.p_b_bHad = p_b_bHad;
                            btag_tree.p_b_b1   = p_b_b1;
                            btag_tree.p_j_b1   = p_j_b1;
                            btag_tree.p_b_b2   = p_b_b2;
                            btag_tree.p_j_b2   = p_j_b2;
                            btag_tree.p_j_w1   = p_j_w1;
                            btag_tree.p_j_w2   = p_j_w2;
                            
                            btag_tree.id_bLep = id_bLep;
                            btag_tree.id_bHad = id_bHad;
                            btag_tree.id_b1   = id_b1;
                            btag_tree.id_b2   = id_b2;
                            btag_tree.id_w1   = id_w1;
                            btag_tree.id_w2   = id_w2;
                            
                            btag_tree.hypo = hyp;
                            btag_tree.p_pos = p_pos;
                            
                            btag_tree.p_bb = p_bb;
                            btag_tree.p_jj = p_jj;
                            
                            btag_tree.nS = nS;
                            btag_tree.nB = nB;
                            btag_tree.tree->Fill();
#endif //DO_BTAG_LR_TREE

                        } //permutations

                    } // end loop over hypothesis

                    // normalize the probabilities...
                    p_bb /= nS;
                    p_jj /= nB;

                    // LR of ttbb vs ttjj hypotheses as variable to select events
                    otree->btag_LR = (p_bb+p_jj)>0 ? p_bb/(p_bb+p_jj) : 0. ;

                    vector<double> lh_jet_csvs, lh_jet_etas;
                    for (uint i=0; i < min(banytag_indices.size(), (long unsigned int)6); i++) {
                        int idx = banytag_indices[i];
                        //cout << i << "=>" << idx << " ";
                        lh_jet_csvs.push_back(jets_csv[idx]);
                        lh_jet_etas.push_back(jets_p4[idx].Eta());
                    }
                    //cout << endl;

                    vector<int> best_perm_lh_indices;
                    vector<BTagLikelihood::JetProbability> jet_probs = btag_lh_calc.evaluate_jet_probabilities(
                        lh_jet_csvs, lh_jet_etas
                    );
                    otree->btag_LR2 = btag_lh_calc.btag_lr_default(jet_probs, best_perm_lh_indices);
                    vector<int> best_perm_lh;
                    for (int i : best_perm_lh_indices) {
                        best_perm_lh.push_back(banytag_indices[i]);
                    }

                    vector<int> best_perm_dummy;
                    otree->btag_LR3 = btag_lh_calc.btag_lr_wcq(jet_probs, best_perm_lh_indices);
                    otree->btag_LR4 = btag_lh_calc.btag_lr_radcc(jet_probs, best_perm_lh_indices);

                    double l_bbbb = btag_lh_calc.btag_likelihood(jet_probs, 4, 0, 2, best_perm_dummy);
                    double l_bbbj = btag_lh_calc.btag_likelihood(jet_probs, 3, 0, 3, best_perm_dummy);
                    double l_bbjj = btag_lh_calc.btag_likelihood(jet_probs, 2, 0, 4, best_perm_dummy);
                    double l_bbcc = btag_lh_calc.btag_likelihood(jet_probs, 2, 2, 2, best_perm_dummy);
                    double l_bbbbcq = btag_lh_calc.btag_likelihood(jet_probs, 4, 1, 1, best_perm_dummy);
                    double l_bbjjcq = btag_lh_calc.btag_likelihood(jet_probs, 2, 1, 3, best_perm_dummy);
                    double l_bbcccq = btag_lh_calc.btag_likelihood(jet_probs, 2, 3, 1, best_perm_dummy);

                    otree->btag_lr_l_bbbb = l_bbbb;
                    otree->btag_lr_l_bbbj = l_bbbj;
                    otree->btag_lr_l_bbjj = l_bbjj;
                    otree->btag_lr_l_bbcc = l_bbcc;
                    otree->btag_lr_l_bbbbcq = l_bbbbcq;
                    otree->btag_lr_l_bbjjcq = l_bbjjcq;
                    otree->btag_lr_l_bbcccq = l_bbcccq;

                    //cout << "LR " << otree->btag_LR << " " << otree->btag_LR2_ << endl;
                    // depending on event type, check if the event passes the cut:
                    // if it does, check which combination yields the **largest** ttbb probability
                    const int* permutListS = 0;
                    switch( btag_flag ) {
                    case 0:
                        passes_btagshape = ( otree->btag_LR >= btag_prob_cut_6jets && selected_comb!=999);
                        permutListS      = permutations_6J_S;
                        break;
                    case 1:
                        passes_btagshape = ( otree->btag_LR >= btag_prob_cut_5jets && selected_comb!=999);
                        permutListS      = permutations_5J_S;
                        break;
                    case 2:
                        passes_btagshape = ( otree->btag_LR >= btag_prob_cut_4jets && selected_comb!=999);
                        permutListS      = permutations_4J_S;
                        break;
                    default:
                        break;
                    }
                    otree->selected_comb = selected_comb;

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
                        //cout << "LR best perm " << btag_indices[0] << " " << btag_indices[1] << " " << btag_indices[2] << " " << btag_indices[3] << endl;
                        //cout << "LR2 best perm " << best_perm_lh[0] << " " << best_perm_lh[1] << " " << best_perm_lh[2] << " " << best_perm_lh[3] << endl;
                        
                        // all other jets go into this collection
                        buntag_indices.clear();
                        for( unsigned int jj = 0 ; jj<banytag_indices.size(); jj++) {

                            // check for a match among the b-tagged jets
                            int isTagged = 0;
                            for( unsigned int bb = 0 ; bb<btag_indices.size(); bb++ ) {
                                if( banytag_indices[jj]==btag_indices[bb] ) isTagged = 1;
                            }

                            // if not matches, push back
                            if( isTagged == 0 ) {
                                buntag_indices.push_back( banytag_indices[jj] );
                            }
                        }

                    } //passes b-tagshape

                } //useBTag & properEvent SL or DL with jets



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

                } //recover


                // categories defined by jet and btagged jet multiplicity (Nj,Nb)
                bool analyze_type0       = properEventSL  && numJets30UntagM==2  && doType0;
                bool analyze_type1       = properEventSL  && numJets30UntagM==2  && doType1;
                bool analyze_type2       = properEventSL  && numJets30UntagM==1  && doType2;
                bool analyze_type3       = properEventSL  && numJets30UntagM >2  && doType3;
                bool analyze_type6       = properEventDL                         && doType6;
                bool analyze_type7       = properEventDL  && numJets30BtagL==4   && doType7;

                // categories defined by jet multiplicity (Nj)
                bool analyze_typeBTag6   = properEventSL && (otree->numJets_==6)                            && doTypeBTag6;
                bool analyze_typeBTag5   = properEventSL && (otree->numJets_==5)                            && doTypeBTag5;
                bool analyze_typeBTag4   = properEventDL && (otree->numJets_==4)                            && doTypeBTag4;

                // categories defined by jet multiplicity (Nj), but passing a minimum cut on the btag likelihood
                bool analyze_type0_BTag  = properEventSL && (otree->numJets_==6)                            && doType0ByBTagShape;
                bool analyze_type1_BTag  = properEventSL && (otree->numJets_==6)                            && doType1ByBTagShape;
                bool analyze_type2_BTag  = properEventSL && (otree->numJets_==5)                            && doType2ByBTagShape;
                bool analyze_type3_BTag  = properEventSL && (otree->numJets_ >6)                            && doType3ByBTagShape;
                bool analyze_type6_BTag  = properEventDL && (otree->numJets_>=4)                            && doType6ByBTagShape;


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
                otree->matchesH_    = hMatches;
                otree->matchesHAll_ = hMatches;
                otree->matchesT_    = tMatches;
                otree->matchesTAll_ = tMatches;
                otree->matchesWAll_ = wMatches;
                wMatches = 0;

                for( unsigned int w = 0; w<buntag_indices.size(); w++) {

                    // use the Py() component to assess if the gen particle is present in the original tree
                    // (it is 0.0 otherwise)
                    if     (   TMath::Abs(HIGGSB1.Py())>0    && deltaR(jets_p4[ buntag_indices[w] ],HIGGSB1)  < GENJETDR ) otree->matchesHAll_++;
                    else if(   TMath::Abs(HIGGSB2.Py())>0    && deltaR(jets_p4[ buntag_indices[w] ],HIGGSB2)  < GENJETDR ) otree->matchesHAll_++;
                    if     (   TMath::Abs(TOPHADB.Py())>0    && deltaR(jets_p4[ buntag_indices[w] ],TOPHADB)  < GENJETDR ) otree->matchesTAll_++;
                    else if(   TMath::Abs(TOPLEPB.Py())>0    && deltaR(jets_p4[ buntag_indices[w] ],TOPLEPB)  < GENJETDR ) otree->matchesTAll_++;
                    if     (   TMath::Abs(TOPHADW1.Py())>0   && deltaR(jets_p4[ buntag_indices[w] ],TOPHADW1) < GENJETDR ) wMatches++;
                    else if(   TMath::Abs(TOPHADW2.Py())>0   && deltaR(jets_p4[ buntag_indices[w] ],TOPHADW2) < GENJETDR ) wMatches++;
                }
                otree->matchesW_    =  wMatches;
                otree->matchesWAll_ += wMatches;

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
                otree->overlapHeavy_ = overlapH;
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
                otree->overlapLight_  = overlapL;


                // if ntuplize all event, then compute the regressed energy per jet...
                if( ntuplizeAll && useRegression ) {
                    assert(currentTree_reg != 0);
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

                if (debug >= 2) {
                    cout << "@Analysis" << endl;
                }

                //  input 4-vectors
                vector<TLorentzVector> jets;
                vector<int> jet_ids;
                vector<TLorentzVector> jets_alt;

                // internal map: [ position in "jets" ] -> [ position in "jets_p4" ]
                std::map< unsigned int, unsigned int> pos_to_index;

                // condition to trigger the ME calculation
                const bool calcME =
                    (analyze_typeBTag6  || analyze_typeBTag5  || analyze_typeBTag4)  ||
                    ((analyze_type0      || analyze_type1      || analyze_type2      || analyze_type3      || analyze_type6 ) && numJets30BtagM==4 )  ||
                    (analyze_type7 && numJets30BtagM==3) ||
                    ((analyze_type0_BTag || analyze_type1_BTag || analyze_type2_BTag || analyze_type3_BTag || analyze_type6_BTag) && passes_btagshape);

                if(debug>=2) {
                    cout << "calcME " << calcME << endl;
                }

                // consider th event only if of the desired type
                if( calcME ) {

                    if(debug>=2) {
                        cout << "Pass! Calc. ME..." << endl;
                    }

                    if( enhanceMC ) {
                        //trial_success = 1;
                        cout << "Success after " << event_trials << " attempts!" << endl;
                        otree->num_of_trials_ = event_trials;
                        event_trials   = 0;
                    }

                    // if the event has been accepted, then compute the regressed energy per jet
                    // (if not done before)
                    if( !ntuplizeAll && useRegression ) {
                        assert(currentTree_reg != 0);
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
                    } //useRegression



                    // find out which two untagged jets come from W->qq'
                    unsigned int ind1 = 999;
                    unsigned int ind2 = 999;

                    if( analyze_typeBTag4 ) {

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "\nProcessing event # " << counter << " (TYPE DL-4 JETS)." << " Event ID " << itree->event__id << endl;

                        /////////////////////////////////////////////////////
                        otree->type_       = -3;
                        otree->nPermut_    =  1;
                        otree->nPermut_alt_=  6;
                        meIntegrator->setIntType( MEIntegratorNew::DL );
                        /////////////////////////////////////////////////////

                    }
                    else if( analyze_typeBTag5 ) {

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "\nProcessing event # " << counter << " (TYPE SL-5 JETS)." << " Event ID " << itree->event__id << endl;

                        /////////////////////////////////////////////////////
                        otree->type_       = -1;
                        otree->nPermut_    =  5;
                        otree->nPermut_alt_= 10;
                        meIntegrator->setIntType( MEIntegratorNew::SL1wj );
                        /////////////////////////////////////////////////////

                    }
                    else if( analyze_typeBTag6 ) {

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "\nProcessing event # " << counter << " (TYPE SL6 JETS)." << " Event ID " << itree->event__id << endl;

                        /////////////////////////////////////////////////////
                        otree->type_       =  -2;
                        otree->nPermut_    =  15;
                        otree->nPermut_alt_=  15;
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
                        otree->mW = WMass;
                        // set index for untagged jets
                        ind1 = buntag_indices[0];
                        ind2 = buntag_indices[1];

                        if( (WMass>MwL && WMass<MwH)  && (analyze_type0 || analyze_type0_BTag) ) {

                            if(syst==0) counter++;
                            if( fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                            if(print) cout << "\nProcessing event # " << counter << " (TYPE 0), mW=" << WMass << " GeV." << " Event ID " << itree->event__id << endl;

                            /////////////////////////////////////////////////////
                            otree->type_       =  0;
                            otree->nPermut_    = 12;
                            otree->nPermut_alt_= 12;
                            meIntegrator->setIntType( MEIntegratorNew::SL2wj );
                            /////////////////////////////////////////////////////
                        }
                        else if( !( WMass>MwL && WMass<MwH) && (analyze_type1 || analyze_type1_BTag)) {

                            if(syst==0) counter++;
                            if( fixNumEvJob && !(counter>=evLow && counter<=evHigh)  ) continue;
                            if(print) cout << "\nProcessing event # " << counter << " (TYPE 1), mW=" << WMass << " GeV." << " Event ID " << itree->event__id << endl;

                            /////////////////////////////////////////////////////
                            otree->type_       =  1;
                            otree->nPermut_    = 24;
                            otree->nPermut_alt_= 24;
                            meIntegrator->setIntType( MEIntegratorNew::SL1wj );
                            /////////////////////////////////////////////////////
                        }
                        else if (cutWMass) {
                            cuts.fill(CutHistogram::Cuts::WMASS);
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
                        if(print) cout << "\nProcessing event # " << counter << " (TYPE 1)." << " Event ID " << itree->event__id << endl;

                        // set index for untagged jet
                        ind1 = buntag_indices[0];
                        ind2 = buntag_indices[0];

                        /////////////////////////////////////////////////////
                        otree->type_       =  2;
                        otree->nPermut_    = 12;
                        otree->nPermut_alt_= 12;
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
                        if(print) cout << "\nProcessing event # " << counter << " (TYPE 3)." << " Event ID " << itree->event__id << endl;

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
                        otree->type_       =  3;
                        otree->nPermut_    = 12;
                        otree->nPermut_alt_= 12;
                        meIntegrator->setIntType( MEIntegratorNew::SL2wj );
                        /////////////////////////////////////////////////////

                        if( testSLw1jType3 ) {

                            if( debug>=1 ) cout << "We will use the option of re-interpreting this event..." << endl;

                            // make sure we don't exceed the maximum array size
                            nMaxJetsSLw1jType3 = TMath::Min(nMaxJetsSLw1jType3, NMAXJETSSLW1JTYPE3);

                            float WMass =  (jets_p4[ ind1 ]+jets_p4[ ind2 ]).M() ;
                            if( WMass>MwLType3 && WMass<MwHType3 ) {
                                otree->flag_type3_ = 1;

                                if( debug>=1 ) {
                                    cout << " > this event (originally type3) will be interpreted as type3, because W mass=" << WMass << " GeV..." << endl;
                                    cout << "   => total # of permutations = " << otree->nPermut_ << endl;
                                }

                            }
                            else {

                                otree->flag_type3_ = -1;

                                otree->nPermut_    = 12*TMath::Min( int(buntag_indices_extra.size()+2), nMaxJetsSLw1jType3 );
                                otree->nPermut_alt_= 12*TMath::Min( int(buntag_indices_extra.size()+2), nMaxJetsSLw1jType3 );
                                meIntegrator->setIntType( MEIntegratorNew::SL1wj );

                                if( debug>=1 ) {
                                    cout << " > this event (originally type3) will be re-interpreted as type1, because W mass=" << WMass << " GeV..." << endl;
                                    cout << "   => total # of permutations = " << otree->nPermut_ << endl;
                                }

                            }
                        }



                    } //analyze_type3 || analyze_type3_BTag
                    else if( analyze_type6 || analyze_type6_BTag ) {

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "Processing event # " << counter << " (TYPE 6)." << " Event ID " << itree->event__id << endl;

                        /////////////////////////////////////////////////////
                        otree->type_       =  6;
                        otree->nPermut_    = 12;
                        otree->nPermut_alt_= 12;
                        meIntegrator->setIntType( MEIntegratorNew::DL );
                        /////////////////////////////////////////////////////

                    }
                    else if( analyze_type7 ) {

                        if(syst==0) counter++;
                        if(fixNumEvJob && !(counter>=evLow && counter<=evHigh) ) continue;
                        if(print) cout << "Processing event # " << counter << " (TYPE 7)." << " Event ID " << itree->event__id << endl;

                        /////////////////////////////////////////////////////
                        otree->type_       =  7;
                        otree->nPermut_    = 12;
                        otree->nPermut_alt_= 12;
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
                    if(otree->type_>=0 && otree->type_<=3 && (ind1==999 || ind2==999)) {
                        cout << "Inconsistency found: ind1 or ind2 are not set...continue." << endl;
                        cout << " => go to next event!" << endl;
                        cout << "******************************" << endl;
                        continue;
                    }

                    // DEBUG
                    if(debug>=1) {
                        cout << "*** Event ID " << itree->event__id << " *** systematics: " << otree->syst_ << endl;
                        cout << " ==> SL=" << int(properEventSL) << ", DL=" << properEventDL << endl;
                        cout << "     NJets " << otree->numJets_ << " (" << otree->numBTagM_ << " tagged)" << endl;
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
                        cout << "     btag probability is " << otree->btag_LR << endl;

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
                    otree->nTotInteg_      = otree->nPermut_    * otree->nMassPoints_;
                    otree->nTotInteg_alt_  = otree->nPermut_alt_* otree->nMassPoints_;

                    // setup jet collection
                    jets.clear();
                    jets.push_back( leptonLV     );
                    jets.push_back( neutrinoLV   );
                    jet_ids.push_back(0);
                    jet_ids.push_back(0);

                    // keep track of an alternative jet selection when doing regression
                    jets_alt.clear();
                    jets_alt.push_back( leptonLV   );
                    jets_alt.push_back( neutrinoLV );

                    // b1,...,w1,w2 are indices for jets_p4 collection;
                    // This is a map between the internal ordering bLep=2, W1Had=3, ..., higgs2 = 7, and jets_p4
                    pos_to_index.clear();
                    
                    if( otree->type_==-3) {
                        jets.push_back( jets_p4[banytag_indices[0]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[0]]);

                        jets.push_back( leptonLV2    );
                        jets.push_back( neutrinoLV   );       // dummy
                        jet_ids.push_back(0);
                        jet_ids.push_back(0);

                        jets.push_back( jets_p4[ banytag_indices[1] ]);
                        jets.push_back( jets_p4[ banytag_indices[2] ]);
                        jets.push_back( jets_p4[ banytag_indices[3] ]);
                        jet_ids.push_back(jets_flavour[banytag_indices[1]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[2]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[3]]);


                        pos_to_index[2] = banytag_indices[0];
                        pos_to_index[3] = banytag_indices[0]; // dummy
                        pos_to_index[4] = banytag_indices[0]; // dummy
                        pos_to_index[5] = banytag_indices[1];
                        pos_to_index[6] = banytag_indices[2];
                        pos_to_index[7] = banytag_indices[3];
                    }
                    else if( otree->type_==-2) {
                        jets.push_back( jets_p4[ banytag_indices[0] ]);
                        jets.push_back( jets_p4[ banytag_indices[1] ]);
                        jets.push_back( jets_p4[ banytag_indices[2] ]);
                        jets.push_back( jets_p4[ banytag_indices[3] ]);
                        jets.push_back( jets_p4[ banytag_indices[4] ]);
                        jets.push_back( jets_p4[ banytag_indices[5] ]);

                        jet_ids.push_back(jets_flavour[banytag_indices[0]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[1]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[2]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[3]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[4]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[5]]);

                        pos_to_index[2] = banytag_indices[0];
                        pos_to_index[3] = banytag_indices[1];
                        pos_to_index[4] = banytag_indices[2];
                        pos_to_index[5] = banytag_indices[3];
                        pos_to_index[6] = banytag_indices[4];
                        pos_to_index[7] = banytag_indices[5];
                    }
                    else if( otree->type_==-1) {
                        jets.push_back( jets_p4[ banytag_indices[0] ]);
                        jets.push_back( jets_p4[ banytag_indices[1] ]);
                        jets.push_back( jets_p4[ banytag_indices[1] ]); // dummy
                        jets.push_back( jets_p4[ banytag_indices[2] ]);
                        jets.push_back( jets_p4[ banytag_indices[3] ]);
                        jets.push_back( jets_p4[ banytag_indices[4] ]);

                        jet_ids.push_back(jets_flavour[banytag_indices[0]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[1]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[1]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[2]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[3]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[4]]);

                        pos_to_index[2] = banytag_indices[0];
                        pos_to_index[3] = banytag_indices[1];
                        pos_to_index[4] = banytag_indices[1];           // dummy
                        pos_to_index[5] = banytag_indices[2];
                        pos_to_index[6] = banytag_indices[3];
                        pos_to_index[7] = banytag_indices[4];
                    }
                    else if( otree->type_<=3 && otree->type_>=0) {
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

                        jet_ids.push_back(jets_flavour[banytag_indices[0]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[ind1]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[ind2]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[1]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[2]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[3]]);

                        pos_to_index[2] = btag_indices[0];
                        pos_to_index[3] = ind1;
                        pos_to_index[4] = ind2;
                        pos_to_index[5] = btag_indices[1];
                        pos_to_index[6] = btag_indices[2];
                        pos_to_index[7] = btag_indices[3];

                    }
                    else if( otree->type_==6 ) {
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

                        jet_ids.push_back(jets_flavour[banytag_indices[0]]);
                        jet_ids.push_back(0);
                        jet_ids.push_back(0);
                        jet_ids.push_back(jets_flavour[banytag_indices[1]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[2]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[3]]);

                        pos_to_index[2] = btag_indices[0];
                        pos_to_index[3] = btag_indices[0];  // dummy
                        pos_to_index[4] = btag_indices[0];  // dummy
                        pos_to_index[5] = btag_indices[1];
                        pos_to_index[6] = btag_indices[2];
                        pos_to_index[7] = btag_indices[3];
                    }
                    else if( otree->type_==7 ) {
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

                        jet_ids.push_back(jets_flavour[banytag_indices[0]]);
                        jet_ids.push_back(0);
                        jet_ids.push_back(0);
                        jet_ids.push_back(jets_flavour[banytag_indices[1]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[2]]);
                        jet_ids.push_back(jets_flavour[banytag_indices[3]]);

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
                    otree->nJet_ = 8;
                    for(int q = 0; q < otree->nJet_ ; q++ ) {
                        // kinematics
                        otree->jet_pt_    [q] = jets[q].Pt() ;
                        otree->jet_pt_alt_[q] = jets_alt[q].Pt();
                        otree->jet_eta_   [q] = jets[q].Eta();
                        otree->jet_phi_   [q] = jets[q].Phi();
                        otree->jet_m_     [q] = jets[q].M();
                        otree->jet_id_    [q] = jet_ids[q];
                        otree->jet_csv_   [q] = q>1 ? jets_csv[ pos_to_index[q] ] : DEF_VAL_FLOAT ;
                        //otree->jet_id_    [q] = jets_id[q] ;
                    }
                    for (int pos=0; pos<6; pos++) {
                        otree->pos_to_index[pos] = pos_to_index[pos];
                    }

                    // set all prob. to 0.0;
                    for(int p = 0 ; p < otree->nTotInteg_; p++) {
                        otree->probAtSgn_permut_       [p] = 0.;
                        otree->probAtSgnErr_permut_    [p] = 0.;
                        otree->callsAtSgn_permut_      [p] = 0 ;
                        otree->chi2AtSgn_permut_       [p] = 0.;
                    }
                    for(int p = 0 ; p < otree->nPermut_; p++) {
                        otree->probAtSgn_bb_permut_ [p] = 0.;
                    }
                    for(int p = 0 ; p < otree->nTotInteg_alt_; p++) {
                        otree->probAtSgn_alt_permut_   [p] = 0.;
                        otree->probAtSgnErr_alt_permut_[p] = 0.;
                        otree->callsAtSgn_alt_permut_  [p] = 0 ;
                        otree->chi2AtSgn_alt_permut_   [p] = 0.;
                    }
                    for(int p = 0 ; p < otree->nPermut_alt_; p++) {
                        otree->probAtSgn_bj_permut_ [p] = 0.;
                        otree->probAtSgn_cc_permut_ [p] = 0.;
                        otree->probAtSgn_jj_permut_ [p] = 0.;
                    }

                    /////////////////////////////////////////////////////////////

                    // check if there is ***at least one*** tag-untag pair that satisfies the "cs-tag"
                    for( unsigned int w = 0; w<btag_indices.size(); w++) {

                        // this is needed if type>3
                        if(ind1==999 || ind2==999) continue;

                        float m1 = !useRegression ? ( jets_p4[btag_indices[w]] + jets_p4[ind1] ).M() : ( jets_p4_reg[btag_indices[w]] + jets_p4[ind1] ).M();
                        float m2 = !useRegression ? ( jets_p4[btag_indices[w]] + jets_p4[ind2] ).M() : ( jets_p4_reg[btag_indices[w]] + jets_p4[ind2] ).M();

                        if( otree->flag_type0_<0 && ((m1>(MwL+5) && m1<(MwH-5)) || (m2>(MwL+5) && m2<(MwH-5))) && otree->type_== 0 ) {
                            otree->flag_type0_ = 0;
                            if( jets_csv[btag_indices[w]]<0.95 ) otree->flag_type0_ = 1;
                            if( jets_csv[btag_indices[w]]<0.90 ) otree->flag_type0_ = 2;
                            if( jets_csv[btag_indices[w]]<0.85 ) otree->flag_type0_ = 3;
                            if( jets_csv[btag_indices[w]]<0.80 ) otree->flag_type0_ = 4;
                        }
                        if( otree->flag_type1_<0 && ((m1>(MwL+5) && m1<(MwH-5)) || (m2>(MwL+5) && m2<(MwH-5))) && otree->type_== 1 ) {
                            otree->flag_type1_ = 0;
                            if( jets_csv[btag_indices[w]]<0.95 ) otree->flag_type1_ = 1;
                            if( jets_csv[btag_indices[w]]<0.90 ) otree->flag_type1_ = 2;
                            if( jets_csv[btag_indices[w]]<0.85 ) otree->flag_type1_ = 3;
                            if( jets_csv[btag_indices[w]]<0.80 ) otree->flag_type1_ = 4;
                        }
                        if( otree->flag_type2_<0 && ((m1>(MwL+5) && m1<(MwH-5)) || (m2>(MwL+5) && m2<(MwH-5))) && otree->type_== 2 ) {
                            otree->flag_type2_ = 0;
                            if( jets_csv[btag_indices[w]]<0.95 ) otree->flag_type2_ = 1;
                            if( jets_csv[btag_indices[w]]<0.90 ) otree->flag_type2_ = 2;
                            if( jets_csv[btag_indices[w]]<0.85 ) otree->flag_type2_ = 3;
                            if( jets_csv[btag_indices[w]]<0.80 ) otree->flag_type2_ = 4;
                        }
                    }

                    if(!testSLw1jType3) {
                        // for type 3, the W-tag is different...
                        float WMass = otree->type_==3 ? (jets_p4[ ind1 ]+jets_p4[ ind2 ]).M() : -999.;
                        if( WMass>MwL && WMass<MwH )  otree->flag_type3_ = 1;
                    }

                    /////////////////////////////////////////////////////////////

                    // init reco particles
                    meIntegrator->setJets(&jets);

                    // init MET stuff
                    meIntegrator->setSumEt( otree->MET_sumEt_ );
                    meIntegrator->setMEtCov(-99,-99,0);

                    // specify if topLep has pdgid +6 or -6
                    meIntegrator->setTopFlags( itree->sig_lep__charge[0]==1 ? +1 : -1 , itree->sig_lep__charge[0]==1 ? -1 : +1 );

                    // if needed, switch off OL
                    if(switchoffOL) {
                        meIntegrator->switchOffOL();
                        if (print) {
                            cout << "*** Switching off OpenLoops to speed-up the calculation ***" << endl;
                        }
                    }

                    // start the clock...
                    clock->Start();
                    std::cout << "calculating ME t=" << otree->type_  << std::endl;

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
                                const int* permutList = 0;
                                if     ( otree->type_ == -3 ) permutList = hyp==0 ?  permutations_4J_S      : permutations_4J_B;
                                else if( otree->type_ == -2 ) permutList = hyp==0 ?  permutations_6J_S      : permutations_6J_B;
                                else if( otree->type_ == -1 ) permutList = hyp==0 ?  permutations_5J_S      : permutations_5J_B;
                                else if( otree->type_ ==  0 ) permutList = hyp==0 ?  permutations_TYPE0_S   : permutations_TYPE0_B;
                                else if( otree->type_ ==  1 ) permutList = hyp==0 ?  permutations_TYPE1_S   : permutations_TYPE1_B;
                                else if( otree->type_ ==  2 ) permutList = hyp==0 ?  permutations_TYPE2_S   : permutations_TYPE2_B;
                                else if( otree->type_ ==  3 ) permutList = hyp==0 ?  permutations_TYPE0_S   : permutations_TYPE0_B;
                                else if( otree->type_ >=  6 ) permutList = hyp==0 ?  permutations_TYPE6_S   : permutations_TYPE6_B;
                                else {
                                    cout << "No permutations found...continue." << endl;
                                    continue;
                                }

                                if( testSLw1jType3 && otree->type_==3 && otree->flag_type3_<0) {
                                    permutList = hyp==0 ?  permutations_TYPE0_5EXTRA_S : permutations_TYPE0_5EXTRA_B;
                                }

                                // loop over permutations
                                for(unsigned int pos = 0; pos < (unsigned int)( hyp==0 ? otree->nPermut_ : otree->nPermut_alt_ ) ; pos++) {

                                    // try to recover these events
                                    if( testSLw1jType3 && otree->type_==3 && otree->flag_type3_<0 ) {

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

                                    } //try to recover events

                                    // consider permutation #pos & save permutation-to-jet mas into the tree...
                                    meIntegrator->initVersors( permutList[pos] );
                                    if( hyp==0 ) otree->perm_to_jet_    [pos] =  permutList[pos];
                                    if( hyp==1 ) otree->perm_to_jet_alt_[pos] =  permutList[pos];

                                    // index of the four jets associated to b-quarks or W->qq
                                    int bLep_pos = (permutList[pos])%1000000/100000;
                                    int w1_pos   = (permutList[pos])%100000/10000;
                                    int w2_pos   = (permutList[pos])%10000/1000;
                                    int bHad_pos = (permutList[pos])%1000/100;
                                    int b1_pos   = (permutList[pos])%100/10;
                                    int b2_pos   = (permutList[pos])%10/1;

                                    // the barcode for this permutation
                                    string barcode = Form("%d%d_%d_%d%d%d_%d%d%d_%d%d",
                                                          otree->type_, meIntegrator->getIntType(), hyp, 
                                                          lep_index[0], 0, jets_index[ pos_to_index[bLep_pos] ],
                                                          otree->type_<6 ? jets_index[ pos_to_index[w1_pos] ] : lep_index[1], otree->type_<6 ? jets_index[ pos_to_index[w2_pos] ] : 0, jets_index[ pos_to_index[bHad_pos] ],
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

                                    //check if b1 and b2 match H->bb
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
                                    if( hyp==0 ) otree->perm_to_gen_    [pos] = 100000*bLep_match + 10000*w1_match + 1000*w2_match + 100*bHad_match + 10*b1_match + 1*b2_match;
                                    if( hyp==1 ) otree->perm_to_gen_alt_[pos] = 100000*bLep_match + 10000*w1_match + 1000*w2_match + 100*bHad_match + 10*b1_match + 1*b2_match;

                                    // Higgs and top candidate masses, matched to gen (for illustrating b-regression performance)
                                    if( b1_match && b2_match ) {
                                        if(!useRegression)
                                            otree->mH_matched_ = (jets_p4[pos_to_index[b1_pos]] + jets_p4[pos_to_index[b2_pos]]).M();
                                        else
                                            otree->mH_matched_ = (jets_p4_reg[pos_to_index[b1_pos]] + jets_p4_reg[pos_to_index[b2_pos]]).M();
                                        if(debug>=2)
                                            std::cout<<"Higgs mass (matched to gen) = "<< otree->mH_matched_<<std::endl;
                                    }

                                    if(w1_match && w2_match) {

                                        if(bHad_match) {
                                            if(!useRegression)
                                                otree->mTop_matched_ = (jets_p4[pos_to_index[bHad_pos]] +  jets_p4[pos_to_index[w1_pos]] + jets_p4[pos_to_index[w2_pos]]).M();
                                            else
                                                otree->mTop_matched_ = (jets_p4_reg[pos_to_index[bHad_pos]] +  jets_p4[pos_to_index[w1_pos]] + jets_p4[pos_to_index[w2_pos]]).M();
                                        }

                                        otree->mW_matched_ = (jets_p4[pos_to_index[w1_pos]] + jets_p4[pos_to_index[w2_pos]]).M();

                                        if(debug>=2) {
                                            std::cout<<"Hadronic W mass   (matched to gen)= " << otree->mW_matched_ << std::endl;
                                            std::cout<<"Hadronic top mass (matched to gen)= " << otree->mTop_matched_ << std::endl;
                                        }
                                    }

                                    // check invariant mass of jet system:
                                    double mass, massLow, massHigh;
                                    bool skip        = !( meIntegrator->compatibilityCheck    (0.95, /*print*/ 0, mass, massLow, massHigh ) );
                                    bool skip_WHad   = false;
                                    bool skip_TopHad = false;
                                    if( otree->type_==0 || otree->type_==3 ) {
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
                                        if( otree->type_==0 || otree->type_==3 || otree->type_==-2) {
                                            p_j_w1 = jets_csv_prob_j[ pos_to_index[w1_pos] ];
                                            p_j_w2 = jets_csv_prob_j[ pos_to_index[w2_pos] ];
                                        }
                                        // the b-tag probability for the one untagged jet...
                                        else if( otree->type_==1 || otree->type_==2 || otree->type_==-1) {
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
                                            cout << "Hyp=" << hyp <<"  [BTag M="   << otree->numBTagM_ << "]" << endl;
                                            cout << " bLep: p_b("   << jets_csv[pos_to_index[bLep_pos]] << ")=" << p_b_bLep;
                                            cout << " bHad: p_b("   << jets_csv[pos_to_index[bHad_pos]] << ")=" << p_b_bHad;
                                            cout << " b1  : p_b("   << jets_csv[pos_to_index[b1_pos]]   << ")=" << p_b_b1;
                                            cout << " b2  : p_b("   << jets_csv[pos_to_index[b2_pos]]   << ")=" << p_b_b2;
                                            if(!(otree->type_>=6 || otree->type_==-3))
                                                cout << " w1  : p_j(" << jets_csv[pos_to_index[w1_pos]]   << ")=" << p_j_w1;
                                            if(!(otree->type_>=6 || otree->type_==-3 || otree->type_==1 || otree->type_==2))
                                                cout << " w2  : p_j(" << jets_csv[pos_to_index[w2_pos]]   << ")=" << p_j_w2 << endl;
                                            cout << " P = "         <<  (p_b_bLep * p_b_bHad * p_b_b1 * p_b_b2 * p_j_w1 * p_j_w2) << endl;
                                        }

                                        // fill arrays with per-permutation probability
                                        if(hyp==0) {
                                            otree->probAtSgn_bb_permut_[pos] =  p_b_bLep * p_b_bHad * p_b_b1 * p_b_b2 * p_j_w1 * p_j_w2;
                                        }
                                        if(hyp==1) {
                                            otree->probAtSgn_bj_permut_[pos] =  p_b_bLep * p_b_bHad * (p_b_b1 * p_j_b2 + p_j_b1 * p_b_b2 )*0.5 * p_j_w1 * p_j_w2;
                                            otree->probAtSgn_cc_permut_[pos] =  p_b_bLep * p_b_bHad * p_c_b1 * p_c_b2 * p_j_w1 * p_j_w2;
                                            otree->probAtSgn_jj_permut_[pos] =  p_b_bLep * p_b_bHad * p_j_b1 * p_j_b2 * p_j_w1 * p_j_w2;
                                        }

                                    } //use b-tag

                                    // if doing scan over b-tag only, don't need amplitude...
                                    if(otree->type_<0) {
                                        cuts.fill(CutHistogram::Cuts::TYPELESSZERO);
                                        continue;
                                    }


                                    // if type 0/3 and incompatible with MW or MT (and we are not scanning vs MT) continue
                                    // ( this applies to both hypotheses )
                                    if( nTopMassPoints==1 && (skip_WHad || skip_TopHad) ) {
                                        if(print) cout << "Skip (THad check failed)...          Perm. #" << pos << endl;
                                        continue;
                                    }

                                    // retrieve integration boundaries from meIntegrator
                                    const pair<double, double> range_x0 = (meIntegrator->getW1JetEnergyCI(0.95));
                                    const pair<double, double> range_x1 =  make_pair(-1,1);
                                    const pair<double, double> range_x2 =  make_pair(-PI,PI);
                                    const pair<double, double> range_x3 =  make_pair(-1,1);
                                    const pair<double, double> range_x4 =  useMET ? (meIntegrator->getNuPhiCI(0.95)) : make_pair(-PI,PI);
                                    const pair<double, double> range_x5 = (meIntegrator->getB1EnergyCI(0.95));
                                    const pair<double, double> range_x6 = (meIntegrator->getB2EnergyCI(0.95));

                                    // boundaries
                                    const double x0L = range_x0.first;
                                    const double x0U = range_x0.second;
                                    const double x1L = range_x1.first;
                                    const double x1U = range_x1.second;
                                    const double x2L = range_x2.first;
                                    const double x2U = range_x2.second;
                                    const double x3L = range_x3.first;
                                    const double x3U = range_x3.second;
                                    const double x4L = range_x4.first;
                                    const double x4U = range_x4.second;
                                    const double x5L = range_x5.first;
                                    const double x5U = range_x5.second;
                                    const double x6L = range_x6.first;
                                    const double x6U = range_x6.second;

                                    // these hold for the sgn integration and type0...
                                    const double xLmode0_s[4] = {x0L, x3L, x4L, x5L};
                                    const double xUmode0_s[4] = {x0U, x3U, x4U, x5U};
                                    // these hold for the bkg integration and type0...
                                    const double xLmode0_b[5] = {x0L, x3L, x4L, x5L, x6L};
                                    const double xUmode0_b[5] = {x0U, x3U, x4U, x5U, x6U};
 
                                    // these hold for the sgn integration and type1...
                                    const double xLmode1_s[6] = {x0L, x1L, x2L, x3L, x4L, x5L};
                                    const double xUmode1_s[6] = {x0U, x1U, x2U, x3U, x4U, x5U};
                                    // these hold for the bkg integration and type1...
                                    const double xLmode1_b[7] = {x0L, x1L, x2L, x3L, x4L, x5L, x6L};
                                    const double xUmode1_b[7] = {x0U, x1U, x2U, x3U, x4U, x5U, x6U};
 
                                    // these hold for the sgn integration and type2...
                                    const double xLmode2_s[6] = {x0L, x1L, x2L, x3L, x4L, x5L};
                                    const double xUmode2_s[6] = {x0U, x1U, x2U, x3U, x4U, x5U};
                                    // these hold for the bkg integration and type2...
                                    const double xLmode2_b[7] = {x0L, x1L, x2L, x3L, x4L, x5L, x6L};
                                    const double xUmode2_b[7] = {x0U, x1U, x2U, x3U, x4U, x5U, x6U};
 
                                    // these hold for the sgn integration and type3...
                                    const double xLmode3_s[4] = {x0L, x3L, x4L, x5L};
                                    const double xUmode3_s[4] = {x0U, x3U, x4U, x5U};
                                    // these hold for the bkg integration and type3...
                                    const double xLmode3_b[5] = {x0L, x3L, x4L, x5L, x6L};
                                    const double xUmode3_b[5] = {x0U, x3U, x4U, x5U, x6U};
 
                                    // these hold for the sgn integration and type6...
                                    const double xLmode6_s[5] = {x1L, x2L, x1L, x2L, x5L};
                                    const double xUmode6_s[5] = {x1U, x2U, x1U, x2U, x5U};
                                    // these hold for the bkg integration and type6...
                                    const double xLmode6_b[6] = {x1L, x2L, x1L, x2L, x5L, x6L};
                                    const double xUmode6_b[6] = {x1U, x2U, x1U, x2U, x5U, x6U};
 
                                    // these hold for the sgn integration and type7...
                                    const double xLmode7_s[5] = {x1L, x2L, x1L, x2L, x5L};
                                    const double xUmode7_s[5] = {x1U, x2U, x1U, x2U, x5U};
                                    // these hold for the bkg integration and type7...
                                    const double xLmode7_b[6] = {x1L, x2L, x1L, x2L, x5L, x6L};
                                    const double xUmode7_b[6] = {x1U, x2U, x1U, x2U, x5U, x6U};

                                    // number of integration variables (TTH hypothesis)
                                    int nParam;
                                    if     ( otree->type_==0 )  nParam = 4; // Eq, eta_nu, phi_nu, Eb
                                    else if( otree->type_==1 )  nParam = 6; // Eq, eta_q', phi_q', eta_nu, phi_nu, Eb
                                    else if( otree->type_==2 )  nParam = 6; // Eq, eta_q', phi_q', eta_nu, phi_nu, Eb
                                    else if( otree->type_==3 )  nParam = 4; // Eq, eta_nu, phi_nu, Eb
                                    else if( otree->type_==6 )  nParam = 5; // eta_nu, phi_nu, eta_nu', phi_nu', Eb
                                    else if( otree->type_==7 )  nParam = 5; // eta_nu, phi_nu, eta_nu', phi_nu', Eb
                                    else {
                                        cout << "No type match...continue." << endl;
                                        cuts.fill(CutHistogram::Cuts::NOTYPEMATCH);
                                        continue; //continue permutation loop
                                    }

                                    if( testSLw1jType3 && otree->type_==3 && otree->flag_type3_<0 ) {
                                        nParam = 6; // Eq, eta_q', phi_q', eta_nu, phi_nu, Eb
                                    }

                                    // per-permutation probability...
                                    double p     = 0.;

                                    // per-permutation probability error...
                                    double pErr  = 0.;

                                    // per-permutation chi2
                                    double chi2  = 0.;

                                    // if doing higgs mass scan, don't consider bkg hypo
                                    if( nHiggsMassPoints>1 && hyp==1 ) {
                                        cuts.fill(CutHistogram::Cuts::H_MASS_SCAN_BKG);
                                        continue; //continue permutation loop
                                    }

                                    // if doing top mass scan, don't consider sgn hypo
                                    if( nTopMassPoints>1 && hyp==0) {
                                        cuts.fill(CutHistogram::Cuts::T_MASS_SCAN_SIG);
                                        continue; //continue permutation loop
                                    }

                                    // if consider only one hypothesis (SoB=0)
                                    // and the current hypo is not the desired one, continue...
                                    if( SoB==0 && hyp!=hypo) {
                                        cuts.fill(CutHistogram::Cuts::ONE_HYPO_MISMATCH);
                                        continue; //continue permutation loop
                                    }

                                    // if current hypo is TTH, but M(b1b2) incompatible with 125
                                    // (and we are not scanning vs MH) continue...
                                    if( hyp==0 && nHiggsMassPoints==1 && skip) {
                                        if(print) {
                                            cout << "Skip    hypo " << (hyp==0 ? "ttH " : "ttbb")
                                                 << " [MH=" << mH[m] << ", MT=" << mT[t]
                                                 << "] Perm. #" << pos;
                                            cout << " => p=" << p << endl;
                                        }
                                        cuts.fill(CutHistogram::Cuts::TTH_MBB_INCOMPATIBLE);
                                        continue; //continue permutation loop
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
                                        cuts.fill(CutHistogram::Cuts::TTJETS_MBB_INCOMPATIBLE);
                                        continue; //continue permutation loop
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
                                    if( otree->type_==0 )  intPoints =  2000;
                                    if( otree->type_==1 )  intPoints =  4000;
                                    if( otree->type_==2 )  intPoints =  4000;
                                    if( otree->type_==3 )  intPoints =  2000;
                                    if( otree->type_==6 )  intPoints = 10000;
                                    if( otree->type_==7 )  intPoints = 10000;

                                    if( testSLw1jType3 && otree->type_==3 && otree->flag_type3_<0 ) {
                                        intPoints =  4000;
                                    }


                                    // count how many time the integration is rerun per permutation
                                    int ntries = 0;
                                    // count number of Integral() calls
                                    int nCalls = 0;

                                    meIntegrator->resetEvaluation();

                                    // skip ME calculation if 1... for debugging
                                    if(speedup==0) {

                                        // setup # of parameters
                                        meIntegrator->SetPar(nParam + hyp);
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
                                        if((integralOption2==0 && need2Rerun) ||
                                            (integralOption2==1 && perm_to_integrator.find( barcode ) == perm_to_integrator.end())) {

                                            // VEGAS integrator
                                            ROOT::Math::GSLMCIntegrator* ig2 = new ROOT::Math::GSLMCIntegrator(
                                                ROOT::Math::IntegrationMultiDim::kVEGAS ,
                                                1.e-12, //absolute tolerance
                                                1.e-5, //relative tolerance
                                                intPoints //maximum number of calls
                                            );
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
                                                if     ( otree->type_==0 ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode0_s, xUmode0_s) : ig2->Integral(xLmode0_b, xUmode0_b));
                                                }
                                                else if( otree->type_==1 || (testSLw1jType3 && otree->type_==3 && otree->flag_type3_<0) ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode1_s, xUmode1_s) : ig2->Integral(xLmode1_b, xUmode1_b));
                                                }
                                                else if( otree->type_==2 ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode2_s, xUmode2_s) : ig2->Integral(xLmode2_b, xUmode2_b));
                                                }
                                                else if( otree->type_==3 ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode3_s, xUmode3_s) : ig2->Integral(xLmode3_b, xUmode3_b));
                                                }
                                                else if( otree->type_==6 ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode6_s, xUmode6_s) : ig2->Integral(xLmode6_b, xUmode6_b));
                                                }
                                                else if( otree->type_==7 ) {
                                                    p = (hyp==0 ? ig2->Integral(xLmode7_s, xUmode7_s) : ig2->Integral(xLmode7_b, xUmode7_b));
                                                }
                                                else {
                                                    nCalls--;
                                                }

                                                // chi2/ndof of the integration
                                                chi2 =  ig2->ChiSqr();

                                                // error from VEGAS
                                                pErr =  ig2->Error();

                                                cout << "INT0 hyp " << hyp <<
                                                    " ev " << itree->event__id <<
                                                    " syst " << syst <<
                                                    " pm " << permutList[pos] <<
                                                    " bc " << barcode <<
                                                    " NT " << ntries <<
                                                    " IP " << intPoints <<
                                                    " chi2 " << chi2 <<
                                                    " pErr " << pErr <<
                                                    " N " << meIntegrator->getEvaluations() <<
                                                    " Ne " << ig2->NEval() <<
                                                    endl;

                                                // save the various integrators
                                                if( integralOption2==1 ) {
                                                    if(perm_to_integrator.find( barcode )!=perm_to_integrator.end()) {
                                                        perm_to_integrator.erase(perm_to_integrator.find(barcode));
                                                    }
                                                    perm_to_integrator[barcode] = ig2;
                                                }

                                                // save the result...
                                                if( perm_to_phasespacepoint.find( barcode )!=perm_to_phasespacepoint.end() ) {
                                                    perm_to_phasespacepoint.erase( perm_to_phasespacepoint.find(barcode) );
                                                }
                                                perm_to_phasespacepoint[barcode] = PSP;

                                                if( perm_to_integral.find( barcode )!=perm_to_integral.end() ) {
                                                    perm_to_integral.erase( perm_to_integral.find(barcode) );
                                                }
                                                perm_to_integral[barcode] = p;

                                                if( perm_to_integralError.find( barcode )!=perm_to_integralError.end() ) {
                                                    perm_to_integralError.erase( perm_to_integralError.find( barcode ) );
                                                }
                                                perm_to_integralError[barcode] = pErr;

                                                if( perm_to_integralChi2.find( barcode )!=perm_to_integralChi2.end() ) {
                                                    perm_to_integralChi2.erase( perm_to_integralChi2.find( barcode ) );
                                                }
                                                perm_to_integralChi2[barcode] = chi2;

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
                                                else {
                                                    ntries = MAX_REEVAL_TRIES+1;
                                                }

                                            } //integration eval loop

                                            // free the allocated memory
                                            if( integralOption2==0 ) delete ig2;
                                        } // end full VEGAS run integralOption==0 or ==1 and no barcode

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
                                                if     ( otree->type_==0 ) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode0_s, xUmode0_s) : perm_to_integrator[barcode]->Integral(xLmode0_b, xUmode0_b));
                                                }
                                                else if( otree->type_==1 || (testSLw1jType3 && otree->type_==3 && otree->flag_type3_<0)) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode1_s, xUmode1_s) : perm_to_integrator[barcode]->Integral(xLmode1_b, xUmode1_b));
                                                }
                                                else if( otree->type_==2 ) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode2_s, xUmode2_s) : perm_to_integrator[barcode]->Integral(xLmode2_b, xUmode2_b));
                                                }
                                                else if( otree->type_==3 ) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode3_s, xUmode3_s) : perm_to_integrator[barcode]->Integral(xLmode3_b, xUmode3_b));
                                                }
                                                else if( otree->type_==6 ) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode6_s, xUmode6_s) : perm_to_integrator[barcode]->Integral(xLmode6_b, xUmode6_b));
                                                }
                                                else if( otree->type_==7 ) {
                                                    p = (hyp==0 ? perm_to_integrator[barcode]->Integral(xLmode7_s, xUmode7_s) : perm_to_integrator[barcode]->Integral(xLmode7_b, xUmode7_b));
                                                }
                                                else {
                                                    nCalls--;
                                                }

                                            } //isSamePoint

                                            // the point has already been calculated, just read the result...
                                            else p = perm_to_integral[barcode];


                                            chi2 =  perm_to_integrator[barcode]->ChiSqr();
                                            pErr =  perm_to_integrator[barcode]->Error();

                                            cout << "INT1 hyp " << hyp <<
                                                " ev " << itree->event__id <<
                                                " syst " << syst <<
                                                " pm " << permutList[pos] <<
                                                " bc " << barcode <<
                                                " NT " << ntries <<
                                                " IP " << intPoints <<
                                                " chi2 " << chi2 <<
                                                " pErr " << pErr <<
                                                " N " << meIntegrator->getEvaluations() <<
                                                " Ne " << perm_to_integrator[barcode]->NEval() <<
                                                endl;
                                        } //end VEGAS re-run with integralOption==1

                                        else {
                                            /* ... */
                                        }
                                        cuts.fill(CutHistogram::Cuts::ME);



                                    } //speedup to skip ME

                                    // can still be interested in b-tagging, so set p=1...
                                    else {
                                        if (debug>=3) {
                                            cout << "setting p to 1" << endl;
                                        }
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
                                            otree->probAtSgn_ttbb_         += ( p * otree->probAtSgn_bb_permut_[pos] );
                                        }

                                        // total ME*btag probability for nominal MH and MT, bkg hypo
                                        if( hyp==1 && mH[m]<MH+1.5 && mH[m]>MH-1.5 && mT[t]<MT+1.5 && mT[t]>MT-1.5) {
                                            otree->probAtSgn_alt_ttbb_     += ( p * otree->probAtSgn_bb_permut_[pos] );
                                            otree->probAtSgn_alt_ttbj_     += ( p * otree->probAtSgn_bj_permut_[pos] );
                                            otree->probAtSgn_alt_ttcc_     += ( p * otree->probAtSgn_cc_permut_[pos] );
                                            otree->probAtSgn_alt_ttjj_     += ( p * otree->probAtSgn_jj_permut_[pos] );
                                        }
                                    }

                                    /////////////////////////////////////////////////////////////

                                    // save TTH prob. per permutation AND mH
                                    if( hyp==0 && mT[t]<MT+1.5 && mT[t]>MT-1.5) {
                                        otree->probAtSgn_permut_   [(unsigned int)(pos + m * otree->nPermut_)] = p;
                                        otree->probAtSgnErr_permut_[(unsigned int)(pos + m * otree->nPermut_)] = pErr;
                                        otree->callsAtSgn_permut_  [(unsigned int)(pos + m * otree->nPermut_)] = nCalls;
                                        otree->chi2AtSgn_permut_   [(unsigned int)(pos + m * otree->nPermut_)] = chi2;
                                    }
                                    // save TTbb prob. per permutation AND mT
                                    if( hyp==1 && mH[m]<MH+1.5 && mH[m]>MH-1.5 ) {
                                        otree->probAtSgn_alt_permut_   [(unsigned int)(pos + t * otree->nPermut_alt_)] = p;
                                        otree->probAtSgnErr_alt_permut_[(unsigned int)(pos + t * otree->nPermut_alt_)] = pErr;
                                        otree->callsAtSgn_alt_permut_  [(unsigned int)(pos + t * otree->nPermut_alt_)] = nCalls;
                                        otree->chi2AtSgn_alt_permut_   [(unsigned int)(pos + t * otree->nPermut_alt_)] = chi2;
                                    }

                                    // total and per-permutation ME probability for nominal MH and MT
                                    if( mH[m]<MH+1.5 && mH[m]>MH-1.5 && mT[t]<MT+1.5 && mT[t]>MT-1.5) {
                                        if(hyp==0) {
                                            otree->probAtSgn_     += p;
                                        }
                                        else {
                                            otree->probAtSgn_alt_ += p;
                                        }
                                    }

                                    /////////////////////////////////////////////////////////////

                                }  // hypothesis FIXME: actually permutations?
                            }  // permutations  FIXME actually hypothesis?
                        }  // nTopMassPoints
                    }  // nHiggsMassPoints

                    // stop clock and reset
                    clock->Stop();
                    otree->time_ = clock->CpuTime();
                    clock->Reset();

                    cout << "ME p_s=" << otree->probAtSgn_
                        << " p_b=" << otree->probAtSgn_alt_
                        << " calculated in " << otree->time_ << endl;

                    // this time is integrated over all hypotheses, permutations, and mass scan values
                    if(print) cout << "Done in " << otree->time_ << " sec" << endl;

                } //calculate matrix element

                ///////////////////////////////////////////////////
                // ALL THE REST...                               //
                ///////////////////////////////////////////////////

                else { //not calcME

                    if( enhanceMC ) {

                        bool retry =
                            ((analyze_type0      || analyze_type1      || analyze_type2      || analyze_type3      || analyze_type6 ) && numJets30BtagM<4 )  ||
                            (analyze_type7 && numJets30BtagM<3) ||
                            ((analyze_type0_BTag || analyze_type1_BTag || analyze_type2_BTag || analyze_type3_BTag || analyze_type6_BTag) && !passes_btagshape);

                        if(otree->syst_ == 0 && retry && event_trials < max_n_trials && event_trials<NMAXEVENTRIALS) {
                            i--;
                            lock = 1;
                            event_trials++;
                            if( event_trials%10000==0 ) cout << "   >>> : " << event_trials << "th trial ---> btag_LR = " <<  otree->btag_LR  << ", numBtagM = " << numJets30BtagM << endl;
                            if(debug>=2) {
                                cout << "Enhance MC: stay with event " << i+1 << endl;
                                cout << "  - lock for systematics, # of trials = " <<  event_trials << "; btagLR = " << otree->btag_LR << endl;
                            }
                            continue;
                        }
                        if( event_trials>=NMAXEVENTRIALS || event_trials>=max_n_trials) {
                            cout << "Failure after " << event_trials << " attempts... try with the next event :-(" << endl;
                            otree->num_of_trials_ = event_trials;
                            event_trials   = 0;
                        }
                    }

                    // if save all events, fill the tree...
                    if(ntuplizeAll) {

                        unsigned int jets_p4_ind = 0;

                        // save jet kinematics into the tree...
                        for(int q = 0; q < otree->nJet_ ; q++ ) {

                            if (debug>2) {
                                cout << " filling jet " << q << ":" << otree->nJet_ << ":" << jets_p4.size() << endl;
                            }
                            // fill elem 0th w/ lepton kinematics
                            if( q==0 ) {
                                otree->jet_pt_    [q] = leptonLV.Pt();
                                otree->jet_pt_alt_[q] = leptonLV.Pt();
                                otree->jet_eta_   [q] = leptonLV.Eta();
                                otree->jet_phi_   [q] = leptonLV.Phi();
                                otree->jet_m_     [q] = leptonLV.M();
                                otree->jet_csv_   [q] = -99.;
                                otree->jet_id_    [q] = 0;
                            }

                            // fill elem 1st w/ MET kinematics
                            else if( q==1 ) {
                                otree->jet_pt_    [q] = neutrinoLV.Pt();
                                otree->jet_pt_alt_[q] = neutrinoLV.Pt();
                                otree->jet_eta_   [q] = neutrinoLV.Eta();
                                otree->jet_phi_   [q] = neutrinoLV.Phi();
                                otree->jet_m_     [q] = neutrinoLV.M();
                                otree->jet_csv_   [q] = -99.;
                                otree->jet_id_    [q] = 0;
                            }

                            // fill other elems w/ the jet kinematics
                            else if( jets_p4_ind < jets_p4.size() && ( properEventSL || (properEventDL && !(q==3 || q==4)))   ) {

                                assert(jets_p4.size() == jets_csv.size());
                                assert(jets_p4.size() == jets_flavour.size());

                                otree->jet_pt_     [q] = !useRegression ? jets_p4[jets_p4_ind].Pt() : jets_p4_reg[jets_p4_ind].Pt();
                                otree->jet_pt_alt_ [q] =  useRegression ? jets_p4[jets_p4_ind].Pt() : jets_p4_reg[jets_p4_ind].Pt();
                                otree->jet_eta_    [q] = jets_p4 [jets_p4_ind].Eta();
                                otree->jet_phi_    [q] = jets_p4 [jets_p4_ind].Phi();
                                otree->jet_m_      [q] = jets_p4 [jets_p4_ind].M();
                                otree->jet_csv_    [q] = jets_csv[jets_p4_ind];
                                otree->jet_id_    [q] = jets_flavour[jets_p4_ind];

                                jets_p4_ind++;
                            }

                            // if DL, fill elem 3rd w/ second lepton kinematics
                            else if( properEventDL && q==3 ) {
                                otree->jet_pt_     [q] = leptonLV2.Pt();
                                otree->jet_pt_alt_ [q] = leptonLV2.Pt();
                                otree->jet_eta_    [q] = leptonLV2.Eta();
                                otree->jet_phi_    [q] = leptonLV2.Phi();
                                otree->jet_m_      [q] = leptonLV2.M();
                                otree->jet_csv_    [q] = -99.;
                                otree->jet_id_    [q] = 0;
                            }

                            //  if DL, fill elem 4th w/ MET kinematics
                            else if( properEventDL && q==4 ) {
                                otree->jet_pt_    [q] = neutrinoLV.Pt();
                                otree->jet_pt_alt_[q] = neutrinoLV.Pt();
                                otree->jet_eta_   [q] = neutrinoLV.Eta();
                                otree->jet_phi_   [q] = neutrinoLV.Phi();
                                otree->jet_m_     [q] = neutrinoLV.M();
                                otree->jet_csv_   [q] = -99.;
                                otree->jet_id_    [q] = 0;
                            }

                            else {}

                        } //jet loop

                        // fill the tree
                        if(debug >= 2) {
                            cout << "@ntuplizeAllFill" << endl;
                        }
                        if(debug >= 2) {
                            cout << otree->nLep_ << ":" << otree->nJet_ << ":" << otree->numJets_ << endl;
                        }
                        cuts.fill(CutHistogram::Cuts::passes);
                        int nfill = otree->tree->Fill();
                        assert(nfill > 0);
                        hcounter->SetBinContent(3, hcounter->GetBinContent(3)+1);
                    } //ntuplizeAll

                    continue; //continue systematics loop in case ntuplizeAll
                } //case where matrix element is not calculated

                if(debug >= 2) {
                    cout << "@notNtuplizeAllFill" << endl; 
                }
                // fill the tree in case !ntuplizeAll
                // FIXME: why is this here twice?
                cuts.fill(CutHistogram::Cuts::passes);
                otree->tree->Fill();
                
                //fill histogram counter with number of passing events
                hcounter->SetBinContent(3, hcounter->GetBinContent(3)+1);

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
        
        } // nentries, event loop

        // this histogram keeps track of the fraction of analyzed events per sample
        hcounter->SetBinContent(1,float(events_)/nentries);

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

    fout_tmp->cd();
    config_dump->Write("", TObject::kOverwrite);
    hcounter->Write("", TObject::kOverwrite );
    hparam->Write("", TObject::kOverwrite );
    otree->tree->Write("", TObject::kOverwrite );
#ifdef DO_BTAG_LR_TREE
    btag_tree.tree->Write("", TObject::kOverwrite );
#endif
    cuts.h->Write("", TObject::kOverwrite);
    cout << "Cut histogram" << endl;
    cuts.print();
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
