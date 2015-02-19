#pragma once
#include <map>
#include <string>
#include <algorithm>
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"

#define NDEBUG
#include "TTH/Plotting/interface/easylogging++.h"

// #include "TTH/Plotting/interface/joosep/sequenceLooper/Event.hh"
// #include "TTH/Plotting/interface/joosep/sequenceLooper/Analyzer.hh"

//Forward declaration
class Sequence;
class GenericAnalyzer;
class EventContainer;

typedef std::map<std::string, GenericAnalyzer*(*)(
    fwlite::TFileService *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
)> AnalyzerRegistry;

class Sequence
{
public:
    std::vector<std::string> analyzers_order;
    std::map<std::string, GenericAnalyzer *> analyzers;
    long long processed = 0;
    const std::string name;
    const std::string fullName;
    const std::vector<std::string> dependsOn;

    Sequence(AnalyzerRegistry &analyzer_registry,
             fwlite::TFileService *fs,
             const std::string _name,
             const std::string _fullName,
             const std::vector<std::string> _dependsOn,
             const edm::VParameterSet &sequence_vpset
            );
    bool process(EventContainer &ev);
    void printSummary();
};