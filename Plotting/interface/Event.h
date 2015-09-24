#ifndef EVENT_H
#define EVENT_H

#include "TTH/Plotting/interface/metree.h"
//JSON parser https://github.com/vivkin/gason
#include "TTH/Plotting/interface/gason.h"
#include "TLorentzVector.h"

#include "TH1D.h"
#include "TFile.h"
#include <tuple>
#include <unordered_map>
#include <functional>
#include <cassert>
#include <sstream>
#include <iostream>
#include <fstream>

using namespace std;

class Configuration {
public:
    vector<string> filenames;
    double lumi;
    string process;
    long firstEntry;
    long numEntries;
    int printEvery;

    Configuration(
        vector<string>& _filenames,
        double _lumi,
        string _process,
        long _firstEntry,
        long _numEntries,
        int _printEvery
    );
    static const Configuration makeConfiguration(JsonValue& value);
    string to_string() const;
};

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

namespace CategoryKey {
enum CategoryKey {
    sl,
    dl,

    //DL
    j3_t2,
    jge4_t2,
    jge3_tge3,
    jge4_tge4,

    //SL
    j5_t3,
    j5_tge4,
    jge6_t2,
    jge6_t3,
    jge6_tge4,
    
    blrL,
    blrH,
};
const string to_string(CategoryKey k);
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
        std::hash<unsigned long long> ResultKey_hash_fn;
        return ResultKey_hash_fn(r);
    }
  };
}

//A map for ResultKey -> TH1D for all the output histograms
typedef unordered_map<
    ResultKey,
    TH1D,
    std::hash<ResultKey>
> ResultMap;

//Saves all results into a ROOT file in a structured way
void saveResults(ResultMap& res, const string& prefix, const string& filename);

//Writes the results into a string for debugging
string to_string(const ResultMap& res);

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
    vector<Jet> jets;
    WeightMap weightFuncs;
    double weight_xs;
    
    double mem_SL_0w2h2t;
    double mem_SL_2w2h2t;
    double mem_SL_2w2h2t_sj;
    double mem_DL_0w2h2t;

    double bTagWeight;
    double bTagWeight_Stats1Up;
    double bTagWeight_Stats1Down;
    double bTagWeight_Stats2Up;
    double bTagWeight_Stats2Down;
    double bTagWeight_LFUp;
    double bTagWeight_LFDown;
    double bTagWeight_HFUp;
    double bTagWeight_HFDown;

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
        double _mem_SL_0w2h2t,
        double _mem_SL_2w2h2t,
        double _mem_SL_2w2h2t_sj,
        double _mem_DL_0w2h2t,
        double _bTagWeight,
        double _bTagWeight_Stats1Up,
        double _bTagWeight_Stats1Down,
        double _bTagWeight_Stats2Up,
        double _bTagWeight_Stats2Down,
        double _bTagWeight_LFUp,
        double _bTagWeight_LFDown,
        double _bTagWeight_HFUp,
        double _bTagWeight_HFDown
    );

    const string to_string() const;
};

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
    static const Event makeNominal(const TreeData& data);
    static const Event makeJESUp(const TreeData& data);
    static const Event makeJESDown(const TreeData& data);
};

//A class combining a cut function, evaluated with this() along
//with a method that fills histograms
class CategoryProcessor {
public:
    CategoryProcessor(
        bool (*_cutFunc)(const Event&),
        const vector<CategoryProcessor*>& _subCategories={}
    ) :
    cutFunc(_cutFunc),
    subCategories(_subCategories)
    {}

    const bool operator()(const Event& ev) const {
        return cutFunc(ev);
    }

    vector<CategoryProcessor*> subCategories;
     
    virtual void fillHistograms(
        const Event& event,
        ResultMap& results,
        const tuple<
            vector<CategoryKey::CategoryKey>,
            SystematicKey::SystematicKey
        >,
        double weight
    ) const;

    void process(const Event& event, const Configuration& conf);
private:
    bool (*cutFunc)(const Event&);
};

class MEMCategoryProcessor : public CategoryProcessor {
public:
    MEMCategoryProcessor(bool (*_cutFunc)(const Event&)) :
      CategoryProcessor(_cutFunc) {};
     
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
