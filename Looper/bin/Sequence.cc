#include "TTH/Looper/interface/Sequence.hh"
#include "TTH/Looper/interface/Analyzer.hh"
//#include "TTH/Plotting/interface/joosep/sequenceLooper/Event.hh"

Sequence::Sequence(AnalyzerRegistry &analyzer_registry,
                   TFileDirectory *fs,
                   const std::string _name,
                   const std::string _fullName,
                   const std::vector<std::string> _dependsOn,
                   const edm::VParameterSet &sequence_vpset) :
    name(_name),
    fullName(_fullName),
    dependsOn(_dependsOn)
{
    //seq_fs = fs;
    seq_fs = fs->mkdir(_name.c_str());
    
    for (auto &seq_elem : sequence_vpset)
    {
        const auto& k = seq_elem.getParameter<std::string>("type");
        const auto& n = seq_elem.getParameter<std::string>("name");
        if (analyzer_registry.find(k) == analyzer_registry.end())
        {
            throw std::runtime_error("could not find analyzer with type " + k);
        }
        LOG(INFO) << "Booked analyzer " << fullName << ":" << k << ":" << n;
        GenericAnalyzer *a = analyzer_registry[k](
            &seq_fs, this, seq_elem
        );

        analyzers_order.push_back(a->name);
        analyzers[a->name] = a;
    }
};

bool Sequence::process(EventContainer &ev)
{
    LOG(DEBUG) << "Processing sequence " << name << ":" << fullName;

    ev.setWasRun(name, true);
    processed++;

    bool ret = true;

    for (const auto &dep : dependsOn)
    {
        if (!ev.wasRun(dep))
        {
            LOG(ERROR) << "Sequence "  << name << " requires " << dep;
            ev.print();
            throw std::runtime_error("missing sequence " + dep);
        }
        if (!ev.wasSuccess(dep)) {
            ret = false;
        }
    }

    if (ret) {
        for (const auto &analyzer : analyzers_order)
        {
            GenericAnalyzer *an = analyzers[analyzer];
            ret = an->process(ev);
            if (!ret)
            {
                LOG(DEBUG) << "Sequence " << name << " analyzer " << an->name << " did not pass, breaking";
                break;
            }
        }
    }

    ev.setWasSuccess(name, ret);

    return ret;
}

void Sequence::printSummary()
{
    std::cout << "Sequence " << fullName << " processed " << processed << std::endl;
    for (auto &k : analyzers_order)
    {
        std::cout << "Analyzer " << analyzers[k]->name << " processed " << analyzers[k]->processed << std::endl;
    }
    std::cout << "---" << std::endl;
}
