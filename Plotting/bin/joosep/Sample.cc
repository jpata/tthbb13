#include "TTH/Plotting/interface/joosep/Sample.h"

Sample::Sample(const edm::ParameterSet& pars) : 
	nickName(pars.getParameter<string>("nickName")),
	fileNamesS1(pars.getParameter<vector<string>>("fileNamesS1")),
	fileNamesS2(pars.getParameter<vector<string>>("fileNamesS2")),
	fractionToProcess(pars.getParameter<double>("fractionToProcess")),
	totalEvents(pars.getParameter<long long>("totalEvents")),
	type(static_cast<SampleType>(pars.getParameter<int>("type"))),
	process(static_cast<Process>(pars.getParameter<int>("process"))),
	skip(pars.getParameter<bool>("skip")),
	step1Enabled(fileNamesS1.size() > 0),
	step2Enabled(fileNamesS2.size() > 0)
{
	if (!step1Enabled) {
		LOG(INFO) << "Disabling step 1 files";
	}

	if (!step2Enabled) {
		LOG(INFO) << "Disabling step 1 files";
	}

	chainS1 = new TChain("tthNtupleAnalyzer/events");
	chainS2 = new TChain("tree");

	if (step1Enabled) {
		for (auto& fn : fileNamesS1) {
			chainS1->AddFile(fn.c_str(), -1);
		}
		TTHTree t((TTree*)(chainS1));
	}

	if (step2Enabled) {
		for (auto& fn : fileNamesS2) {
			chainS2->AddFile(fn.c_str(), -1);
		}

		treeS2 = new METree((TTree*)(chainS2));
	}

	if (totalEvents <= 0) {
		if (step2Enabled) {
			totalEvents = chainS2->GetEntries();
			LOG(INFO) << "Total entries from S2 " << totalEvents;
		} else if(step1Enabled) {
			totalEvents = chainS1->GetEntries();
			LOG(INFO) << "Total entries from S1 " << totalEvents;
		}
	}


}