#include "TTH/Looper/interface/Analyzer.hh"
#include "TTH/Looper/interface/Input.hh"
#include "TTH/Looper/interface/AutoTree.hh"

TChainInput::TChainInput(const edm::ParameterSet &pset) : GenericInput(pset)
{
    LOG(DEBUG) << "TChainInput: created TChainInput";

    treeName = pset.getParameter<std::string>("treeName");
    lastEvent = pset.getParameter<long long>("lastEvent");
    firstEvent = pset.getParameter<long long>("firstEvent");
    chain = new TChain(treeName.c_str());
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
