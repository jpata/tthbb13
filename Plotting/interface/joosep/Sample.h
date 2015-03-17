#ifndef SAMPLE_STEP2_H
#define SAMPLE_STEP2_H
#include "TFile.h"
#include "TChain.h"
#include "TTH/Plotting/interface/easylogging++.h"
#include "FWCore/ParameterSet/interface/ProcessDesc.h"
#include "FWCore/PythonParameterSet/interface/PythonProcessDesc.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "TTH/Plotting/interface/joosep/helpers_step2.hh"

using namespace std;

class Sample
{
public:
    const string nickName;
    const vector<string> fileNamesS1;
    const vector<string> fileNamesS2;
    const double fractionToProcess;
    long long totalEvents;
    const SampleType type;
    const Process process;
    const bool skip;

    const bool step1Enabled;
    const bool step2Enabled;

    TChain *chainS1, *chainS2;

    TTHTree *treeS1;
    METree *treeS2;

    map<tuple<long long, long long, long long>, long long> event_map_S1;

    Sample(const edm::ParameterSet &pars);

    long long getFirstEvent()
    {
        if (skip)
        {
            return 0;
        }
        return 0;
    }

    long long getLastEvent()
    {
        if (skip)
        {
            return -1;
        }
        if (fractionToProcess < 1.0)
        {
            LOG(INFO) << "Processing a fraction of sample " << nickName << ": " << fractionToProcess;
            return (long long)(fractionToProcess * totalEvents);
        }
        return totalEvents;
    }

    long long getIndexS1(long long event, long long run, long long lumi)
    {
        const auto event_key = make_tuple(run, lumi, event);
        const long long idx = event_map_S1[event_key];
        assert(idx >= 0);
        return idx;
    }

};


#endif