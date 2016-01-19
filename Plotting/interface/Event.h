#ifndef EVENT_H
#define EVENT_H

#include "TTH/Plotting/interface/metree.h"
//JSON parser https://github.com/vivkin/gason
#include "TTH/Plotting/interface/gason.h"
#include "TTH/Plotting/interface/gen.h"
#include "TLorentzVector.h"

#include "TH1D.h"
#include "THnSparse.h"
#include "TFile.h"
#include "TPython.h"
#include <tuple>
#include <unordered_map>
#include <functional>
#include <cassert>
#include <sstream>
#include <iostream>
#include <fstream>

using namespace std;

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
    TLorentzVector p4;
    float btagCSV;
    float btagBDT;
    int hadronFlavour;

    Jet(TLorentzVector& _p4, float _btagCSV, float _btagBDT, int _hadronFlavour);
    const string to_string() const;
};

//Simple representation of a jet
class Lepton {
public:
    const TLorentzVector p4;
    int pdgId;

    Lepton(const TLorentzVector& _p4, int _pdgId);
    const string to_string() const;
};

//fwd decl
class Event;

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
    string prefix;
    long firstEntry;
    long numEntries;
    int printEvery;
    string outputFile;
    vector<SparseAxis> sparseAxes;
    vector<vector<CategoryKey::CategoryKey>> enabledCategories;
    bool recalculateBTagWeight;

    Configuration(
        vector<string>& _filenames,
        double _lumi,
        ProcessKey::ProcessKey _process,
        string _prefix,
        long _firstEntry,
        long _numEntries,
        int _printEvery,
        string _outputFile,
        vector<SparseAxis> _sparseAxes,
        vector<vector<CategoryKey::CategoryKey>> _enabledCategories
        ) :
        filenames(_filenames),
        lumi(_lumi),
        process(_process),
        prefix(_prefix),
        firstEntry(_firstEntry),
        numEntries(_numEntries),
        printEvery(_printEvery),
        outputFile(_outputFile),
        sparseAxes(_sparseAxes),
        enabledCategories(_enabledCategories),
        recalculateBTagWeight(true)
    {
    }
    static const Configuration makeConfiguration(JsonValue& value);
    string to_string() const;
};

//maps systematics to function(event, conf)->double
typedef unordered_map<
    SystematicKey::SystematicKey,
    double (*)(const Event&, const Configuration& conf),
    hash<int>
> WeightMap;
double nominal_weight(const Event& ev, const Configuration& conf);

//These functions return the list of weights used
//all systematic weights
WeightMap getSystWeights();

//only nominal weights
WeightMap getNominalWeights();

//Simple event representation
//Designed to be immutable
class Event {
public:

    bool is_sl;
    bool is_dl;
    bool passPV;

    int numJets;
    int nBCSVM;
    int nBCSVL;

    //list of all jets
    vector<Jet> jets;
    
    //list of all jets
    vector<Lepton> leptons;

    //map of SystematicKey -> weight func(event) of all syst. weights to evaluate
    //WeightMap weightFuncs;

    //cross-section weight
    double weight_xs;

    double puWeight;
    
    double Wmass;
    
    //mem hypotheses
    double mem_SL_0w2h2t;
    double mem_SL_2w2h2t;
    double mem_SL_2w2h2t_sj;
    double mem_DL_0w2h2t;

    // Our BDT
    double tth_mva;

    //KIT BDT
    double common_bdt;

    //btag weights
    double bTagWeight;

    //btag likelihood
    double btag_LR_4b_2b;
    double btag_LR_4b_2b_logit; // log(x/(1 - x))

    //boosted variables
    int n_excluded_bjets;
    int n_excluded_ljets;

    int ntopCandidate;
    double topCandidate_pt;
    double topCandidate_eta;
    double topCandidate_mass;
    double topCandidate_masscal;
    double topCandidate_fRec;
    double topCandidate_n_subjettiness;

    int nhiggsCandidate;
    double higgsCandidate_pt;
    double higgsCandidate_eta;
    double higgsCandidate_mass;
    double higgsCandidate_bbtag;
    double higgsCandidate_n_subjettiness;
    double higgsCandidate_dr_genHiggs;
    const TreeData *data;

    Event(
        const TreeData *_data,
        bool _is_sl,
        bool _is_dl,
        bool _passPV,
        int _numJets,
        int _nBCSVM,
        int _nBCSVL,
        const vector<Jet>& _jets,
        const vector<Lepton>& _leptons,
        //const WeightMap& _weightFuncs,
        double _weight_xs,
        double _puWeight,
        double _Wmass,
        double _mem_SL_0w2h2t,
        double _mem_SL_2w2h2t,
        double _mem_SL_2w2h2t_sj,
        double _mem_DL_0w2h2t,
        double _tth_mva,
        double _common_bdt,
        double _bTagWeight,
        double _btag_LR_4b_2b,
        int _n_excluded_bjets,
        int _n_excluded_ljets,
        
        int _ntopCandidate,
        double _topCandidate_pt,
        double _topCandidate_eta,
        double _topCandidate_mass,
        double _topCandidate_masscal,
        double _topCandidate_fRec,
        double _topCandidate_n_subjettiness,

        int _nhiggsCandidate,
        double _higgsCandidate_pt,
        double _higgsCandidate_eta,
        double _higgsCandidate_mass,
        double _higgsCandidate_bbtag,
        double _higgsCandidate_n_subjettiness,
        double _higgsCandidate_dr_genHiggs
    );

    const string to_string() const;
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
        const vector<const CategoryProcessor*>& _subCategories={},
        const WeightMap _weightFuncs={
            {SystematicKey::nominal, nominal_weight}
        }
    ) :
    cutFunc(_cutFunc),
    keys(_keys),
    conf(_conf),
    subCategories(_subCategories),
    weightFuncs(_weightFuncs)
    {}

    const bool operator()(const Event& ev) const {
        return cutFunc(ev);
    }

    const vector<CategoryKey::CategoryKey> keys;
    const Configuration& conf;
    const vector<const CategoryProcessor*> subCategories;
    const WeightMap weightFuncs;

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
        const vector<const CategoryProcessor*>& _subCategories={},
        const WeightMap _weightFuncs=getSystWeights()
    ) :
    CategoryProcessor(_cutFunc, _keys, _conf, _subCategories, _weightFuncs),
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

namespace BaseCuts {
    bool sl(const Event& ev);
    bool sl_mu(const Event& ev);
    bool sl_el(const Event& ev);
    bool dl(const Event& ev);
    bool dl_mumu(const Event& ev);
    bool dl_ee(const Event& ev);
    bool dl_emu(const Event& ev);
}

bool isMC(ProcessKey::ProcessKey proc);
bool isSignalMC(ProcessKey::ProcessKey proc);
bool isData(ProcessKey::ProcessKey proc);
double process_weight(ProcessKey::ProcessKey proc);

//Checks if this category, specified by a list of keys, was enabled in the JSON
bool isCategoryEnabled(const Configuration& conf, const vector<CategoryKey::CategoryKey>& catKeys);

#endif
