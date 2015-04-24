#pragma once
#include "TFormula.h"
#include "TH1D.h"
#include "TH2D.h"

#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

//#include "TTH/Plotting/interface/joosep/sequenceLooper/Sequence.hh"
class Sequence;
#include "TTH/Looper/interface/Event.hh"

#define NDEBUG
#include "TTH/Looper/interface/easylogging++.h"

//Base class for all analyzers
class GenericAnalyzer
{
    Sequence *sequence;
    TFileDirectory *fs;
    TFileDirectory _fd;

public:
    long long processed = 0;
    const std::string name;

    GenericAnalyzer(
        TFileDirectory *_fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    );

    virtual bool process(EventContainer &event);

    template <typename T>
    void addData(EventContainer &event, const std::string dname, T d);

    template <typename T>
    T getData(EventContainer &event, const std::string dname);

    template <typename T, class ...Ts>
    T *fsmake(Ts... args);
    
    Sequence* getSequence() {
        return sequence;
    }
};

class EventPrinterAnalyzer : public GenericAnalyzer
{
    const bool printAll;
    const int processEvery;
public:
    EventPrinterAnalyzer(
        TFileDirectory *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    );

    virtual bool process(EventContainer &event);
};

class TFormulaEvaluator : public GenericAnalyzer
{
    TFormula form;

    const std::string xName, yName, zName;

public:
    TFormulaEvaluator(
        TFileDirectory *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    );

    virtual bool process(EventContainer &event);
};

template <class T>
class ValueSelector : public GenericAnalyzer
{

    const std::string branch;
    const T val;
public:
    ValueSelector(
        TFileDirectory *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    );

    virtual bool process(EventContainer &event);
};

template <class T>
class ValueRangeSelector : public GenericAnalyzer
{

    const std::string branch;
    const T low;
    const T high;
public:
    ValueRangeSelector(
        TFileDirectory *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    );

    virtual bool process(EventContainer &event);
};

template <typename T>
void GenericAnalyzer::addData(EventContainer &event, const std::string dname, T d)
{
    event.addData(name + "__" + dname, d);
}

template <class T>
GenericAnalyzer *createAnalyzerInstance(
    TFileDirectory *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset)
{
    return new T(fs, _sequence, pset);
}

template <class T>
ValueSelector<T>::ValueSelector(
    TFileDirectory *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    GenericAnalyzer(fs, _sequence, pset),
    branch(pset.getParameter<std::string>("branch")),
    val(pset.getParameter<T>("value"))
{
    LOG(DEBUG) << "ValueSelector: created ValueSelector ";
};

template <class T>
bool ValueSelector<T>::process(EventContainer &event)
{
    GenericAnalyzer::process(event);
    LOG(DEBUG) << "processing " << name << " " << event.i;
    T x = event.getData<T>(branch);
    LOG(DEBUG) << "ValueSelector " << name << " " << branch << " " << x << " " << val;
    return x == val;
};

template <class T>
ValueRangeSelector<T>::ValueRangeSelector(
    TFileDirectory *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    GenericAnalyzer(fs, _sequence, pset),
    branch(pset.getParameter<std::string>("branch")),
    low(pset.getParameter<T>("low")),
    high(pset.getParameter<T>("high"))
{
    LOG(DEBUG) << "ValueRangeSelector: created ValueRangeSelector ";
};
template <class T>
bool ValueRangeSelector<T>::process(EventContainer &event)
{
    GenericAnalyzer::process(event);
    LOG(DEBUG) << "processing " << name << " " << event.i;
    T x = event.getData<T>(branch);
    return (x >= low && x < high);
};

template <typename T>
T GenericAnalyzer::getData(EventContainer &event, const std::string dname)
{
    return event.getData<T>(name + "__" + dname);
}

typedef ValueSelector<bool> BoolSelector;
typedef ValueSelector<int> IntSelector;
typedef ValueRangeSelector<double> DoubleRangeSelector;
typedef ValueRangeSelector<int> IntRangeSelector;

class JetHistogramAnalyzer : public GenericAnalyzer
{
    TH1D* h_pt0 = 0; //leading jet pt
    TH1D* h_pt1 = 0; //sub-leading jet pt
    
    TH1D* h_eta0 = 0; //leading jet eta
    TH1D* h_eta1 = 0; //sub-leading jet eta
    
    TH1D* h_abseta0 = 0; //leading jet abs eta
    TH1D* h_abseta1 = 0; //sub-leading jet abs eta
    
    TH1D* h_csv0b = 0; //leading jet csv b
    TH1D* h_csv0c = 0; //leading jet csv c
    TH1D* h_csv0l = 0; //leading jet csv l
    TH1D* h_csv0g = 0; //leading jet csv g
    TH1D* h_csv0lg = 0;
    
    TH1D* h_csv1b = 0; //leading jet csv b
    TH1D* h_csv1c = 0; //leading jet csv c
    TH1D* h_csv1l = 0; //leading jet csv l
    TH1D* h_csv1g = 0; //leading jet csv g
    TH1D* h_csv1lg = 0;
    
    TH1D* h_Wmass = 0;
public:
    JetHistogramAnalyzer(
        TFileDirectory *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    );

    virtual bool process(EventContainer &event);
};

class BTagHistogramAnalyzer : public GenericAnalyzer
{
    TH1D* h_nBCSVM = 0;
    TH1D* h_nBCSVT = 0;

    TH1D* h_btagLR = 0;
    TH2D* h_btagLR_nMatchSimB = 0;
    
    TH2D* h_njets_nBCSVM = 0;

public:
    BTagHistogramAnalyzer(
        TFileDirectory *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    );

    virtual bool process(EventContainer &event);
};


class MEAnalyzer : public GenericAnalyzer
{
    const int me_index;
    
    //coarse ME
    TH1D* h_me_discr = 0;
    
    //coarse ME vs btag LR
    TH2D* h_me_discr_btagLR = 0;
    
    //Fine ME
    TH1D* h_me_discr2 = 0;
    
    TH2D* h_me_discr_tth_ttbb = 0;


public:
    MEAnalyzer(
        TFileDirectory *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    );

    virtual bool process(EventContainer &event);
};

class MEMultiHypoAnalyzer : public GenericAnalyzer
{
    TFormula formula;
    
    //coarse ME
    TH1D* h_me_discr = 0;
    
    //coarse ME vs btag LR
    TH2D* h_me_discr_btagLR = 0;
    
    //Fine ME
    TH1D* h_me_discr2 = 0;


public:
    MEMultiHypoAnalyzer(
        TFileDirectory *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    );

    virtual bool process(EventContainer &event);
};

class MatchAnalyzer : public GenericAnalyzer
{
    //Number of quarks matched to jets
    TH1D* h_nmatch_wq = 0;
    TH1D* h_nmatch_hb = 0;
    TH1D* h_nmatch_tb = 0;
    
    //Number of quarks matched to jets, taking into account b-tagging
    TH1D* h_nmatch_wq_btag = 0;
    TH1D* h_nmatch_hb_btag = 0;
    TH1D* h_nmatch_tb_btag = 0;
    
    //Quark pt
    TH1D* h_wq_pt = 0;
    TH1D* h_hb_pt = 0;
    TH1D* h_tb_pt = 0;

    //Quark eta
    TH1D* h_wq_eta = 0;
    TH1D* h_hb_eta = 0;
    TH1D* h_tb_eta = 0;
    
public:
    MatchAnalyzer(
        TFileDirectory *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    );

    virtual bool process(EventContainer &event);
};

class GenLevelAnalyzer : public GenericAnalyzer
{
    TH1D* h_n_wq = 0;
    TH1D* h_n_hb = 0;
    TH1D* h_n_tb = 0;
    TH1D* h_sample = 0;

public:
    GenLevelAnalyzer(
        TFileDirectory *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    );

    virtual bool process(EventContainer &event);
};
