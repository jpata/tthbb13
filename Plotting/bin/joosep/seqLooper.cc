#define NDEBUG

#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"

#include <cstdlib>
#include <iostream>
#include <fstream>
#include <map>
#include <string>
#include <algorithm>
//#include <boost/spirit/home/support/detail/hold_any.hpp>
#include <boost/any.hpp>

#include "TROOT.h"
#include "TChain.h"
#include "TSystem.h"

#include "TTH/Plotting/interface/joosep/Sample.h"
#include "TTH/MEAnalysis/interface/MECombination.h"

#include "TTH/Plotting/interface/joosep/sequenceLooper/Analyzer.hh"
#include "TTH/Plotting/interface/joosep/sequenceLooper/Sequence.hh"
#include "TTH/Plotting/interface/joosep/sequenceLooper/Input.hh"

#include "TTH/Plotting/interface/joosep/tth_inputs.hh"
#include "TTH/Plotting/interface/joosep/tth_analyzers.hh"

/////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////


//Need to define it here to specialize templates
template <typename T, class ...Ts>
T *GenericAnalyzer::fsmake(Ts... args)
{
    T *t = fs->make<T>(args...);
    t->SetName(
        (sequence->fullName + "__" + this->name + "__" + string(t->GetName())).c_str()
    );
    return t;
}

//Add all defined Input modules here
std::map<std::string, GenericInput*(*)(const edm::ParameterSet &pset)> input_registry =
{
    {"GenericInput", &createInputInstance<GenericInput>},
    {"TChainInput", &createInputInstance<TChainInput>},
    {"TTHSampleInput", &createInputInstance<TTHSampleInput>},
};

//Add all defined Analyzer modules here
AnalyzerRegistry analyzer_registry =
{
    {"GenericAnalyzer", &createAnalyzerInstance<GenericAnalyzer>},
    {"EventPrinterAnalyzer", &createAnalyzerInstance<EventPrinterAnalyzer>},
    {"TTHMETreeAnalyzer", &createAnalyzerInstance<TTHMETreeAnalyzer>},
    {"LeptonAnalyzer", &createAnalyzerInstance<LeptonAnalyzer>},
    {"MEDiscriminatorAnalyzer", &createAnalyzerInstance<MEDiscriminatorAnalyzer>},
    {"BoolSelector", &createAnalyzerInstance<BoolSelector>},
    {"IntSelector", &createAnalyzerInstance<IntSelector>},
    {"DoubleRangeSelector", &createAnalyzerInstance<DoubleRangeSelector>},
    {"TTHEventPrinterAnalyzer", &createAnalyzerInstance<TTHEventPrinterAnalyzer>},
};

_INITIALIZE_EASYLOGGINGPP

int main(int argc, const char *argv[])
{
    TH1::SetDefaultSumw2(true);

    _START_EASYLOGGINGPP(argc, argv);

    gROOT->SetBatch(true);
    gSystem->Load("libFWCoreFWLite");
    gSystem->Load("libDataFormatsFWLite");

    AutoLibraryLoader::enable();

    PythonProcessDesc builder(argv[1]);
    const edm::VParameterSet &inputs_par = builder.processDesc()->getProcessPSet()->getParameter<edm::VParameterSet>("inputs");
    const edm::ParameterSet &output_par = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("outputs");

    fwlite::TFileService *fs = new fwlite::TFileService(output_par.getParameter<std::string>("outFileName"));
    //const edm::ParameterSet& output = builder.processDesc()->getProcessPSet()->getParameter<edm::ParameterSet>("output");
    const edm::VParameterSet &list_of_sequences = builder.processDesc()->getProcessPSet()->getParameter<edm::VParameterSet>("sequences");

    std::vector<std::string> inputs_order;
    std::map<std::string, GenericInput *> inputs;
    for (auto &inp : inputs_par)
    {
        const auto k = inp.getParameter<std::string>("type");
        if (input_registry.find(k) == input_registry.end())
        {
            throw std::runtime_error("could not find input module with type " + k);
        }
        LOG(INFO) << "Booked input " << k;
        GenericInput *a = input_registry[k](inp);

        inputs_order.push_back(a->name);
        inputs[a->name] = a;
    }


    std::vector<Sequence *> all_sequences;

    for (const auto &input : inputs_order)
    {
        GenericInput *inp = inputs[input];
        std::cout << "Processing input " << input
                  << " from " << inp->getFirst()
                  << " to " << inp->getLast() << std::endl;

        std::vector<Sequence *> cur_sequences;

        for (long long i = inp->getFirst(); i < inp->getLast(); i++)
        {
            EventContainer ev = inp->getEvent(i);

            if (inp->remakeSequences)
            {
                LOG(INFO) << "Remaking sequences for " << inp->currentName;

                // for (auto& seq : sequences) {
                //  all_sequences.push_back(seq);
                // }

                cur_sequences.clear();
                for (auto &seqp : list_of_sequences)
                {
                    const auto &seq_name = seqp.getParameter<std::string>("name");
                    const auto &dependsOn = seqp.getParameter<std::vector<std::string>>("dependsOn");
                    const auto &sequence_pset = builder.processDesc()->getProcessPSet()->
                                                getParameter<edm::VParameterSet>(seq_name);

                    Sequence *seq = new Sequence(
                        analyzer_registry, fs,
                        seq_name, //name
                        (inp->currentName + "__" + seq_name), //fullName
                        dependsOn, //dependsOn
                        sequence_pset
                    );

                    all_sequences.push_back(seq);
                    cur_sequences.push_back(seq);
                };

            }

            for (auto *seq : cur_sequences)
            {
                seq->process(ev);
            }
        }
        std::cout << "Input " << input << " processed " << inp->processed << std::endl;
        for (auto &seq : all_sequences)
        {
            seq->printSummary();
        }
    }

    delete fs;
}