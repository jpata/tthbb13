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
			LOG(INFO) << "Adding S1 file " << fn;
			chainS1->AddFile(fn.c_str(), -1);
		}
		treeS1 = new TTHTree(chainS1);
		treeS1->set_branch_addresses();
	}

	if (step2Enabled) {
		for (auto& fn : fileNamesS2) {
			LOG(INFO) << "Adding S2 file " << fn;
			chainS2->AddFile(fn.c_str(), -1);
		}

		treeS2 = new METree(chainS2);
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

	if (step1Enabled) {
		///Maps event (run, lumi, id) to an index in the step1 file
		LOG(INFO) << "Creating S1 index map";
		treeS1->tree->SetBranchStatus("*", false);
		treeS1->tree->SetBranchStatus("event__*", true);

		long nb = 0;
		for (long long entry = 0; entry < chainS1->GetEntries(); entry++) {
			nb += treeS1->tree->GetEntry(entry);
            const auto k = make_tuple(treeS1->event__run, treeS1->event__lumi, treeS1->event__id);
			event_map_S1[k] = entry;
		}
		treeS1->tree->SetBranchStatus("*", true);
		treeS1->set_branch_addresses();
		LOG(INFO) << "Index map created, read " << nb << "b";

	}


}