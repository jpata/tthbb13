#include "TTH/Plotting/interface/joosep/sequenceLooper/Analyzer.hh"
#include "TTH/Plotting/interface/joosep/sequenceLooper/Sequence.hh"
#include "TTH/Plotting/interface/joosep/sequenceLooper/Event.hh"

GenericAnalyzer::GenericAnalyzer(
    fwlite::TFileService *_fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    fs(_fs),
    sequence(_sequence),
    name(pset.getParameter<std::string>("name"))
{
    LOG(DEBUG) << "GenericAnalyzer: created analyzer with name " << name;
};

bool GenericAnalyzer::process(EventContainer &event)
{
    LOG(DEBUG) << "processing " << sequence->fullName << " " << name << " " << event.i;
    processed++;
    return true;
};

EventPrinterAnalyzer::EventPrinterAnalyzer(
    fwlite::TFileService *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    GenericAnalyzer(fs, _sequence, pset),
    printAll(pset.getParameter<bool>("printAll")),
    processEvery(pset.getParameter<int>("processEvery"))
{
    LOG(DEBUG) << "EventPrinterAnalyzer: created EventPrinterAnalyzer";
};

bool EventPrinterAnalyzer::process(EventContainer &event)
{
    GenericAnalyzer::process(event);
    LOG(DEBUG) << "processing " << name << " " << event.i;

    if (processed % processEvery == 0)
    {
        std::cout << name << ":" << processed << ":" << event.i << std::endl;

        if (printAll)
        {
            for (auto const &k : event.data)
            {
                std::cout << k.first << " " << &(k.second) << std::endl;
            }
        }
    }
    return true;
};

TFormulaEvaluator::TFormulaEvaluator(
    fwlite::TFileService *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    GenericAnalyzer(fs, _sequence, pset),
    form(name.c_str(), pset.getParameter<std::string>("formula").c_str()),
    xName(pset.getParameter<std::string>("xName")),
    yName(pset.getParameter<std::string>("yName")),
    zName(pset.getParameter<std::string>("zName"))
{
    LOG(DEBUG) << "TFormulaEvaluator: created TFormulaEvaluator " << pset.getParameter<std::string>("formula");
};

bool TFormulaEvaluator::process(EventContainer &event)
{
    GenericAnalyzer::process(event);
    LOG(DEBUG) << "processing " << name << " " << event.i;

    const double x = xName.size() > 0 ? event.getData<double>(xName) : NAN;
    const double y = yName.size() > 0 ? event.getData<double>(yName) : NAN;
    const double z = zName.size() > 0 ? event.getData<double>(zName) : NAN;

    double prod = NAN;
    if (!std::isnan(x) && !std::isnan(y) && !std::isnan(z))
    {
        prod = form.Eval(x, y, z);
    }
    else if (!std::isnan(x) && !std::isnan(y) && std::isnan(z))
    {
        prod = form.Eval(x, y);
    }
    else if (!std::isnan(x) && std::isnan(y) && std::isnan(z))
    {
        prod = form.Eval(x);
    }
    addData(event, "f", prod);
    return true;
};