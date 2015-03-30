
//Base class for all analyzers
class GenericInput
{
public:
    long long processed = 0;
    const std::string name;
    bool remakeSequences = false;
    std::string currentName = "";

    GenericInput(const edm::ParameterSet &pset) : name(pset.getParameter<std::string>("name"))
    {
        LOG(DEBUG) << "GenericInput: created analyzer with name " << name;
    };

    virtual long long getFirst()
    {
        return 0;
    }

    virtual long long getLast()
    {
        return 0;
    }
    virtual EventContainer getEvent(long long idx)
    {
        return EventContainer(idx);
    };
};

class TChainInput : public GenericInput
{

    TChain *chain = 0;
    std::string treeName = "";

public:
    TChainInput(const edm::ParameterSet &pset) : GenericInput(pset)
    {
        LOG(DEBUG) << "TChainInput: created TChainInput";

        treeName = pset.getParameter<std::string>("treeName");
        chain = new TChain(treeName.c_str());

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
    };

    virtual long long getFirst()
    {
        return 0;
    }

    virtual long long getLast()
    {
        return 0;
    }
    virtual EventContainer getEvent(long long idx)
    {
        return EventContainer(idx);
    };
};