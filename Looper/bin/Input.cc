#include "TTH/Looper/interface/Analyzer.hh"
#include "TTH/Looper/interface/Input.hh"
#include "TTH/Looper/interface/AutoTree.hh"

TChainInput::TChainInput(const edm::ParameterSet &pset) :
    GenericInput(pset),
    treeName(pset.getParameter<std::string>("treeName")),
    firstEvent(pset.getParameter<long long>("firstEvent")),
    lastEvent(pset.getParameter<long long>("lastEvent")),
    chain(new TChain(treeName.c_str()))
{
    LOG(DEBUG) << "TChainInput: created TChainInput";
    LOG(INFO) << "Sample " << name << " type=" << sampleTypeMajor;

    
    currentName = name;
    
    for (auto &file : pset.getParameter<edm::VParameterSet>("files"))
    {
        const auto fn = file.getParameter<std::string>("fileName");
        LOG(INFO) << "TChainInput " << name << " adding file " << fn;
        int ret = chain->AddFile(fn.c_str());
        if (ret != 1)
        {
            throw std::runtime_error("could not add file " + fn + " with tree name " + treeName);
        }
    }
    itree = new AutoTree(chain);
}
