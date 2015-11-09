#ifndef EVENT_H
#define EVENT_H

#include "TTH/Plotting/interface/metree.h"
//JSON parser https://github.com/vivkin/gason
#include "TTH/Plotting/interface/gason.h"
#include "TLorentzVector.h"

#include "TH1D.h"
#include "THnSparse.h"
#include "TFile.h"
#include <tuple>
#include <unordered_map>
#include <functional>
#include <cassert>
#include <sstream>
#include <iostream>
#include <fstream>

using namespace std;

namespace SystematicKey {
enum SystematicKey {
    nominal,
    CMS_scale_jUp,
    CMS_scale_jDown,
    CMS_ttH_CSVStats1Up,
    CMS_ttH_CSVStats1Down,
    CMS_ttH_CSVStats2Up,
    CMS_ttH_CSVStats2Down,
    CMS_ttH_CSVLFUp,
    CMS_ttH_CSVLFDown,
    CMS_ttH_CSVHFUp,
    CMS_ttH_CSVHFDown,
};
const string to_string(SystematicKey k);
}

namespace ProcessKey {
enum ProcessKey {
  ttH,
  ttH_hbb,
  ttbarPlusBBbar,
  ttbarPlusB,
  ttbarPlus2B,
  ttbarPlusCCbar,
  ttbarOther,
  ttH_nohbb,
  ttw_wlnu,
  ttw_wqq,
  ttz_zqq,
  ttz_zllnunu,
  UNKNOWN
};
const string to_string(ProcessKey k);
const ProcessKey from_string(const string& k);
}

namespace CategoryKey {
enum CategoryKey {
    sl,
    dl,

    //DL
    j3_t2,
    jge4_t2,
    jge3_t3,
    jge4_tge4,

    //SL
    j4_t3,
    j4_t4,
    j5_t3,
    j5_tge4,
    jge6_t2,
    jge6_t3,
    jge6_tge4,
    
    blrL,
    blrH,
    
    Wmass60_100,
    nonWmass60_100,

    boosted,
    nonboosted,
    boostedMass120_180,
    nonboostedMass120_180,
    boostedMass140_180,
    nonboostedMass140_180,
    boostedTau_07,
    nonboostedTau_07,
    boostedfRec_02,
    nonboostedfRec_02            
};
const string to_string(CategoryKey k);
const CategoryKey from_string(const string& k);
}

//Names of all possible histograms we want to save
//without systematic variation suffix
namespace HistogramKey {
enum HistogramKey {
    jet0_pt,
    mem_SL_0w2h2t,
    mem_DL_0w2h2t,
    mem_SL_2w2h2t,
    mem_SL_2w2h2t_sj,
    sparse,
};
//convert enum to the corresponding string
//NB: Have to add all these to Event.cc/HistogramKey::to_string manually!!!
//This could be auto-generated with C++ macro magic but here we are explicit
const string to_string(HistogramKey k);
}

//Simple 3-tuple of (category, systematic, histname) to keep track of
//final histograms.
typedef tuple<
    vector<CategoryKey::CategoryKey>,
    SystematicKey::SystematicKey,
    HistogramKey::HistogramKey
> ResultKey;

//Write ResultKey to string
string to_string(const ResultKey& k);

//We need to specialize the std::hash function for ResultKey
//To define ResultMap
namespace std {
  template <> struct hash<ResultKey>
  {
    //const static std::hash<unsigned long> ResultKey_hash_fn;
    size_t operator()(const ResultKey & x) const
    {
        //make a compound hash
        unsigned long long r = 0;
        int ninc = 8; // how many bits to shift each
        int ic = 0; //shift counter

        //shift vector of category keys
        for (auto& v : get<0>(x)) {
            r += static_cast<int>(v) << (ninc*ic);        
        }
        ic++;
        r += static_cast<int>(get<1>(x)) << (ninc*ic);
        ic++;
        r += static_cast<int>(get<2>(x)) << (ninc*ic);
        std::hash<unsigned long long> _hash_fn;
        return _hash_fn(r);
    }
  };

template <> struct hash<vector<CategoryKey::CategoryKey>>
{
  //const static std::hash<unsigned long> ResultKey_hash_fn;
  size_t operator()(const vector<CategoryKey::CategoryKey> & x) const
  {
        //make a compound hash
        unsigned long long r = 0;
        int ninc = 8; // how many bits to shift each
        int ic = 0; //shift counter

        //shift vector of category keys
        for (auto& v : x) {
          r += static_cast<int>(v) << (ninc*ic);        
        }
        std::hash<unsigned long long> _hash_fn;
        return _hash_fn(r);
  }
};
}

//Simple representation of a jet
class Jet {
public:
    const TLorentzVector p4;
    const float btagCSV;

    Jet(const TLorentzVector& _p4, int _btagCSV);
    const string to_string() const;
};


//Simple event representation
//Designed to be immutable
class Event {
public:
typedef unordered_map<
    SystematicKey::SystematicKey,
    double (*)(const Event&),
    hash<int>
> WeightMap;

    bool is_sl;
    bool is_dl;
    bool pass_trig_sl;
    bool pass_trig_dl;
    bool passPV;

    int numJets;
    int nBCSVM;

    //list of all jets
    vector<Jet> jets;

    //map of SystematicKey -> weight func(event) of all syst. weights to evaluate
    WeightMap weightFuncs;

    //cross-section weight
    double weight_xs;
    
    double Wmass;
    
    //mem hypotheses
    double mem_SL_0w2h2t;
    double mem_SL_2w2h2t;
    double mem_SL_2w2h2t_sj;
    double mem_DL_0w2h2t;

    // Our BDT
    double tth_mva;

    //btag weights
    double bTagWeight;
    double bTagWeight_Stats1Up;
    double bTagWeight_Stats1Down;
    double bTagWeight_Stats2Up;
    double bTagWeight_Stats2Down;
    double bTagWeight_LFUp;
    double bTagWeight_LFDown;
    double bTagWeight_HFUp;
    double bTagWeight_HFDown;

    //btag likelihood
    double btag_LR_4b_2b;
    double btag_LR_4b_2b_logit; // log(x/(1 - x))

    //boosted variables
    int n_excluded_bjets;
    int n_excluded_ljets;
    int ntopCandidate;
    double topCandidate_mass;
    double topCandidate_fRec;
    double topCandidate_n_subjettiness;

    Event(
        bool _is_sl,
        bool _is_dl,
        bool _pass_trig_sl,
        bool _pass_trig_dl,
        bool _passPV,
        int _numJets,
        int _nBCSVM,
        const vector<Jet>& _jets,
        const WeightMap& _weightFuncs,
        double _weight_xs,
        double _Wmass,
        double _mem_SL_0w2h2t,
        double _mem_SL_2w2h2t,
        double _mem_SL_2w2h2t_sj,
        double _mem_DL_0w2h2t,
	double _tth_mva,
        double _bTagWeight,
        double _bTagWeight_Stats1Up,
        double _bTagWeight_Stats1Down,
        double _bTagWeight_Stats2Up,
        double _bTagWeight_Stats2Down,
        double _bTagWeight_LFUp,
        double _bTagWeight_LFDown,
        double _bTagWeight_HFUp,
        double _bTagWeight_HFDown,
        double _btag_LR_4b_2b,
        int _n_excluded_bjets,
        int _n_excluded_ljets,
        int _ntopCandidate,
        double _topCandidate_mass,
        double _topCandidate_fRec,
        double _topCandidate_n_subjettiness
    );

    const string to_string() const;
};

class SparseAxis {
public:
    SparseAxis(
        const string& _name,
        std::function<float(const Event& ev)> _evalFunc,
        int _nBins,
        float _xMin,
        float _xMax
        ) : 
        name(_name),
        evalFunc(_evalFunc),
        nBins(_nBins),
        xMin(_xMin),
        xMax(_xMax) {};
    string name;
    std::function<float(const Event& ev)> evalFunc;
    int nBins;
    float xMin, xMax;
};

class Configuration {
public:
    typedef unordered_map<
        const vector<CategoryKey::CategoryKey>,
        double,
        hash<vector<CategoryKey::CategoryKey>>
    > CutValMap;

    vector<string> filenames;
    double lumi;
    ProcessKey::ProcessKey process;
    long firstEntry;
    long numEntries;
    int printEvery;
    string outputFile;
    vector<SparseAxis> sparseAxes;

    Configuration(
        vector<string>& _filenames,
        double _lumi,
        ProcessKey::ProcessKey _process,
        long _firstEntry,
        long _numEntries,
        int _printEvery,
        string _outputFile,
        vector<SparseAxis> _sparseAxes
        ) :
        filenames(_filenames),
        lumi(_lumi),
        process(_process),
        firstEntry(_firstEntry),
        numEntries(_numEntries),
        printEvery(_printEvery),
        outputFile(_outputFile),
        sparseAxes(_sparseAxes)
    {
    }
    static const Configuration makeConfiguration(JsonValue& value);
    string to_string() const;
};

//A map for ResultKey -> TH1D for all the output histograms
typedef unordered_map<
    ResultKey,
    TObject*,
    std::hash<ResultKey>
> ResultMap;

//Saves all results into a ROOT file in a structured way
void saveResults(ResultMap& res, const string& prefix, const string& filename);

//Writes the results into a string for debugging
string to_string(const ResultMap& res);

//Helper class to make various variated jet collections from TreeData
class JetFactory {
public:
    static const Jet makeNominal(const TreeData& data, int njet);
    static const Jet makeJESUp(const TreeData& data, int njet);
    static const Jet makeJESDown(const TreeData& data, int njet);
};

//Helper class to make various variated Event representations from TreeData
class EventFactory {
public:
    static const Event makeNominal(const TreeData& data, const Configuration& conf);
    static const Event makeJESUp(const TreeData& data, const Configuration& conf);
    static const Event makeJESDown(const TreeData& data, const Configuration& conf);
};

//A class combining a cut function, evaluated with this() along
//with a method that fills histograms
class CategoryProcessor {
public:
    CategoryProcessor(
        std::function<int(const Event& ev)> _cutFunc,
        const vector<CategoryKey::CategoryKey>& _keys,
        const Configuration& _conf,
        const vector<const CategoryProcessor*>& _subCategories={}
    ) :
    cutFunc(_cutFunc),
    keys(_keys),
    conf(_conf),
    subCategories(_subCategories)
    {}

    const bool operator()(const Event& ev) const {
        return cutFunc(ev);
    }

    const vector<CategoryKey::CategoryKey> keys;
    const Configuration& conf;
    const vector<const CategoryProcessor*> subCategories;
     
    virtual void fillHistograms(
        const Event& event,
        ResultMap& results,
        const tuple<
            vector<CategoryKey::CategoryKey>,
            SystematicKey::SystematicKey
        >,
        double weight
    ) const;

    void process(
        const Event& event,
        const Configuration& conf,
        ResultMap& results,
        const vector<CategoryKey::CategoryKey>& catKeys,
        SystematicKey::SystematicKey systKey
    ) const;
private:
    std::function<int(const Event& ev)> cutFunc;
};

class MEMCategoryProcessor : public CategoryProcessor {
public:
    MEMCategoryProcessor(
        std::function<int(const Event& ev)> _cutFunc,
        const vector<CategoryKey::CategoryKey>& _keys,
        const Configuration& _conf,
        const vector<const CategoryProcessor*>& _subCategories={}
    ) :
      CategoryProcessor(_cutFunc, _keys, _conf, _subCategories) {};
     
    virtual void fillHistograms(
        const Event& event,
        ResultMap& results,
        const tuple<
            vector<CategoryKey::CategoryKey>,
            SystematicKey::SystematicKey
        >,
        double weight
    ) const;
};

class SparseCategoryProcessor : public CategoryProcessor {
public:
    SparseCategoryProcessor(
        std::function<int(const Event& ev)> _cutFunc,
        const vector<CategoryKey::CategoryKey>& _keys,
        const Configuration& _conf,
        const vector<const CategoryProcessor*>& _subCategories={}
    ) :
    CategoryProcessor(_cutFunc, _keys, _conf, _subCategories),
    axes(_conf.sparseAxes)
    {
        nAxes = axes.size();
        for (auto& ax : _conf.sparseAxes) {
            nBinVec.push_back(ax.nBins);
            xMinVec.push_back(ax.xMin);
            xMaxVec.push_back(ax.xMax);
        }
    };
    
    vector<SparseAxis> axes;
    int nAxes;
    vector<int> nBinVec;
    vector<double> xMinVec;
    vector<double> xMaxVec;

    THnSparseF* makeHist() const {
        THnSparseF* h = new THnSparseF("sparse", "sparse events", nAxes, &(nBinVec[0]), &(xMinVec[0]), &(xMaxVec[0]));
        h->CalculateErrors(true); //Enable THnSparse error accounting (otherwise wrong) 
        int iax = 0;
        for (auto& ax : axes) {
            h->GetAxis(iax)->SetName(ax.name.c_str());
            h->GetAxis(iax)->SetTitle(ax.name.c_str());
            iax += 1;
        }
        return h;
    }

    virtual void fillHistograms(
        const Event& event,
        ResultMap& results,
        const tuple<
            vector<CategoryKey::CategoryKey>,
            SystematicKey::SystematicKey
        >,
        double weight
    ) const;
};

Configuration parseJsonConf(const string& infile);
#endif
