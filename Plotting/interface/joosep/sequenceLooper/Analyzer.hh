#pragma once
#include "TFormula.h"

#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

//#include "TTH/Plotting/interface/joosep/sequenceLooper/Sequence.hh"
class Sequence;
#include "TTH/Plotting/interface/joosep/sequenceLooper/Event.hh"

#define NDEBUG
#include "TTH/Plotting/interface/easylogging++.h"

//Base class for all analyzers
class GenericAnalyzer
{
    fwlite::TFileService *fs;
    Sequence *sequence;

public:
    long long processed = 0;
    const std::string name;

    GenericAnalyzer(
        fwlite::TFileService *_fs,
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
};

class EventPrinterAnalyzer : public GenericAnalyzer
{
    const bool printAll;
    const int processEvery;
public:
    EventPrinterAnalyzer(
        fwlite::TFileService *fs,
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
        fwlite::TFileService *fs,
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
        fwlite::TFileService *fs,
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
        fwlite::TFileService *fs,
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
    fwlite::TFileService *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset)
{
    return new T(fs, _sequence, pset);
}

template <class T>
ValueSelector<T>::ValueSelector(
    fwlite::TFileService *fs,
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
    fwlite::TFileService *fs,
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
