#include "TChain.h"

#include "TTH/Looper/interface/AutoTree.hh"

//Represents the physical process
namespace SampleTypeMajor {
    enum SampleTypeMajor {
        data = 0,
        tth = 1,
        ttjets = 2,
    };
};

//Base class for all inputs
class GenericInput
{
public:
    //name of input
    const std::string name;
    const SampleTypeMajor::SampleTypeMajor sampleTypeMajor;

    //Number of events processed
    long long processed = 0;
    
    //If true, all Sequences and Analyzers are remade when changing event
    bool remakeSequences = true;

    std::string currentName = "";

    GenericInput(const edm::ParameterSet &pset) :
    name(pset.getParameter<std::string>("name")),
    sampleTypeMajor(static_cast<SampleTypeMajor::SampleTypeMajor>(
        pset.getParameter<unsigned int>("sampleTypeMajor")
    ))
    {
        LOG(DEBUG) << "GenericInput: created analyzer with name " << name;
    };

    //First entry to process
    virtual long long getFirst()
    {
        return 0;
    }

    //Last entry to process
    virtual long long getLast()
    {
        return 0;
    }
    
    //returns the current event
    virtual EventContainer getEvent(long long idx)
    {
        return EventContainer(idx);
    };
};

class TChainInput : public GenericInput
{
private:
    const std::string treeName = "";
    const long long firstEvent = 0;
    const long long lastEvent = 0;

public:

private:
    TChain *chain = 0;
    AutoTree* itree = 0;

public:

    TChainInput(const edm::ParameterSet&);
    
    /** 
    *   @brief  Returns the first event to be processed.
    *  
    *   @return Index of the first event to be processed.
    */ 
    virtual long long getFirst()
    {
        return firstEvent>=0 ? firstEvent : 0;
    }
    
    /** 
    *   @brief  Returns the last event that is processed.   
    *  
    *   @return Index of the last event to be processed.
    */  
    virtual long long getLast()
    {
        return lastEvent>=0 ? lastEvent : chain->GetEntries()-1;
    }
    
    /** 
    *   @brief  Loads the event into memory.
    *  
    *   @return EventContainer with the event data.
    */ 
    virtual EventContainer getEvent(long long idx)
    {
        chain->GetEntry(idx);
        EventContainer ev(idx);
        
        //Add the automatically generated TTree floats
        ev.addData<AutoTree*>("input", (AutoTree*)itree);
        for (auto& kv : itree->ints_map) {
            ev.addData<int>(kv.first, kv.second->val);
        }
        for (auto& kv : itree->doubles_map) {
            ev.addData<int>(kv.first, kv.second->val);
        }
        processed += 1;
        return ev;
    };
};

template <class T>
GenericInput *createInputInstance(const edm::ParameterSet &pset)
{
    return new T(pset);
}
