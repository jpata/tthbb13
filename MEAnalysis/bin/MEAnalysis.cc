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
    const string pathToTF       (in.getParameter<string>  ("pathToTF"));
    const bool   verbose             (in.getParameter<bool>         ("verbose"));
    const bool   isMC                (in.getParameter<bool>         ("isMC"));

    // PARAMETERS
    const double lumi               (in.getUntrackedParameter<double>("lumi",   19.04));
    const float  MH                 (in.getUntrackedParameter<double>("MH",     125.));
    const float  MT                 (in.getUntrackedParameter<double>("MT",     174.3));
    const float  MW                 (in.getUntrackedParameter<double>("MW",     80.19));

    const vector<int> evLimits(in.getParameter<vector<int>>("evLimits"));

    // upper and lower event bounds to be processed
    const int evLow  = evLimits[0];
    const int evHigh = evLimits[1];

    cout << "samples=" << endl;
    for (auto& s : samples){
        cout << "sample " << s.getParameter<string>("name")<< " " << s.getParameter<string>("nickName") << endl;
    }

    Samples file_samples(true, pathToFile, "", samples, lumi, verbose);

    if (!file_samples.IsOk()){
        cerr << "Error opening samples" << endl;
    } else {
        cout << "Samples opened successfully" << endl;
    }

    cout << "outFileName " << outFileName << endl;
    cout << "verbose " << verbose << endl;
    cout << "isMC " << isMC << endl;

    cout << "lumi " << lumi << endl;
    cout << "MH " << MH << " MT " << MT << " MW " << MW << endl;

    cout << "evLow " << evLow << " evHigh " << evHigh << endl;
 

    cout << "Creating ME Integrator" << endl;
    MEIntegratorNew* meIntegrator = new MEIntegratorNew(pathToTF , 4 , int(verbose));
    

    cout << "Finished!!!" << endl;
    cout << "*******************" << endl;
    delete meIntegrator;

    return 0;
}
