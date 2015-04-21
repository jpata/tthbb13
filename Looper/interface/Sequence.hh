#pragma once
#include <map>
#include <string>
#include <algorithm>
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"

#define NDEBUG
#include "TTH/Looper/interface/easylogging++.h"

//Forward declaration to define map
class Sequence;
class GenericAnalyzer;
class EventContainer;

typedef std::map<std::string, GenericAnalyzer*(*)(
    TFileDirectory *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
)> AnalyzerRegistry;

class Sequence
{
public:
    
    //The ordered list of analyzers to process
    std::vector<std::string> analyzers_order;
    
    //name -> Analyzer map of the analyzers to process
    std::map<std::string, GenericAnalyzer *> analyzers;
    
    //Number of events processed
    long long processed = 0;
    
    //Name of sequence
    const std::string name;
    
    //Full name of sequence
    const std::string fullName;
    
    //List of sequence names on which this sequence depends on
    const std::vector<std::string> dependsOn;

    //TFileService of this sequence
    TFileDirectory seq_fs;
    
    Sequence(AnalyzerRegistry &analyzer_registry,
            TFileDirectory *fs,
             const std::string _name,
             const std::string _fullName,
             const std::vector<std::string> _dependsOn,
             const edm::VParameterSet &sequence_vpset
            );
    bool process(EventContainer &ev);
    void printSummary();
};
