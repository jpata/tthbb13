#include "TTH/Plotting/interface/joosep/sequenceLooper/Sequence.hh"
#include "TTH/Plotting/interface/joosep/sequenceLooper/Analyzer.hh"
//#include "TTH/Plotting/interface/joosep/sequenceLooper/Event.hh"

Sequence::Sequence(AnalyzerRegistry &analyzer_registry,
                   fwlite::TFileService *fs,
                   const std::string _name,
                   const edm::VParameterSet &sequence_vpset) :
    name(_name)
{
    for (auto &seq_elem : sequence_vpset)
    {
        const auto k = seq_elem.getParameter<std::string>("type");
        if (analyzer_registry.find(k) == analyzer_registry.end())
        {
            throw std::runtime_error("could not find analyzer with type " + k);
        }
        LOG(INFO) << "Booked analyzer " << k;
        GenericAnalyzer *a = analyzer_registry[k](fs, this, seq_elem);

        analyzers_order.push_back(a->name);
        analyzers[a->name] = a;
    }
};

bool Sequence::process(EventContainer &ev)
{
    for (const auto &analyzer : analyzers_order)
    {
        GenericAnalyzer *an = analyzers[analyzer];
        bool ret = an->process(ev);
        if (!ret)
        {
            break;
        }
    }
    processed++;
    return true;
}

void Sequence::printSummary()
{
    std::cout << "Sequence " << name << " processed " << processed << std::endl;
    for (auto &k : analyzers_order)
    {
        std::cout << "Analyzer " << k << " processed " << analyzers[k]->processed << std::endl;
    }
    std::cout << "---" << std::endl;
}
