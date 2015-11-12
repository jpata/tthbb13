#include "TFile.h"
#include "TChain.h"
#include <iostream>

#include "TTH/Plotting/interface/Event.h"

using namespace std;

const Configuration parseArgs(int argc, const char** argv) {
    if (argc != 2) {
        cerr << "Usage: ./melooper conf.json" << endl;
        cerr << "No json file specified, exiting" << endl;
        exit(EXIT_FAILURE);
    }
    const string jsonFilename(argv[1]); 
    Configuration conf = parseJsonConf(jsonFilename);
    cout << "Done loading configuration" << endl;
    cout << conf.to_string() << endl;
    return conf;
}

TChain* loadFiles(const Configuration& conf) {
    cout << "Loading input files" << endl;

    TChain* tree = new TChain("tree");
    for (auto& fn : conf.filenames) {
        cout << "Adding file " << fn << endl;
        int isgood = tree->AddFile(fn.c_str());
        if (!isgood) {
            cerr << "Failed to load file " << fn << endl;
            exit(EXIT_FAILURE);
        }
    }
    //https://root.cern.ch/doc/master/classTTreeCache.html
    tree->SetCacheSize(10 * 1024 * 1024);
    tree->AddBranchToCache("*");
    return tree;
}

namespace BaseCuts {
    bool sl(const Event& ev) {
        return ev.is_sl && ev.passPV && ev.pass_trig_sl && ev.numJets>=4;
    }

    bool dl(const Event& ev) {
        return ev.is_dl && ev.passPV && ev.pass_trig_dl;
    }
}

const vector<CategoryKey::CategoryKey> emptykey;

int main(int argc, const char** argv) {
    //Switch off histogram naming for memory management
    TH1::AddDirectory(false);

    const Configuration conf = parseArgs(argc, argv);
    TChain* tree = loadFiles(conf);

    // Here a tree of categories is defined
    // Each category is specified by a list of CategoryKeys (called name) which form the name
    // in the output root file.
    // A category is only processed if it passes a cut, specified by a lambda function
    // of the form cutFunc: const Event& -> bool
    // Different CategoryProcessors may be created, each with their own fillHistograms
    // method, which fill different histograms depending on need.
    // As an example, we have CategoryProcessor, which fills jet0_pt
    // and MEMCategoryProcessor which fills, in addition, the MEM histograms.
    // Each category can contain subcategories, which are processed only if
    // the parent category cut passed. The subcategories need only specify the additional
    // names, which will be added to the parent category name to create the final
    // output directory of the histogram.

    // Note: this vector is made const, so that it is fully known and will not change at runtime.
    const vector<const CategoryProcessor*> categorymap = {
        new SparseCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && ev.btag_LR_4b_2b > 0.95;
            },
            {CategoryKey::sl},
            conf
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && ev.numJets>=6 && ev.nBCSVM>=4;
            },
            {CategoryKey::sl, CategoryKey::jge6_tge4},
            conf
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && ev.btag_LR_4b_2b > 0.95 && ev.numJets>=6 && ev.nBCSVM>=4;
            },
            {CategoryKey::sl, CategoryKey::jge6_tge4, CategoryKey::blrH},
            conf
        ),
        new SparseCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::dl(ev);
            },
            {CategoryKey::dl},
            conf
        )
    };

    cout << "Attaching branches..." << endl;
    TreeData data;
    data.loadTree(tree);

    int njtot = 0;
    long nbytes = 0;
    
    ResultMap results;

    cout << "Looping over events [" << conf.firstEntry << "," << conf.firstEntry+conf.numEntries << ")" << endl;

    for (long iEntry=conf.firstEntry; iEntry<conf.firstEntry+conf.numEntries; iEntry++) {

        const bool do_print = (conf.printEvery>0 && iEntry % conf.printEvery == 0);
        nbytes += tree->GetEntry(iEntry);
        if (do_print) {
            cout << "------" << endl;
            cout << "entry " << iEntry << endl;
        }

        const unordered_map<SystematicKey::SystematicKey, Event, std::hash<int> > systmap = {
            {SystematicKey::nominal, EventFactory::makeNominal(data, conf)},
            {SystematicKey::CMS_scale_jUp, EventFactory::makeJESUp(data, conf)},
            {SystematicKey::CMS_scale_jDown, EventFactory::makeJESDown(data, conf)}
        };

        for (auto& kvSyst : systmap) {
            //cout << " syst " << SystematicKey::to_string(kvSyst.first) << endl;
            const Event& event = kvSyst.second;
            if (do_print) {
                cout << SystematicKey::to_string(kvSyst.first) << " " << event.to_string();
            }
            for (auto& cat : categorymap) {
                cat->process(event, conf, results, {}, kvSyst.first);
            } //categorymap
        } // systmap
    } //entries

    //Finalize with output
    cout << "Read " << nbytes/1024/1024 << " Mb" << endl;
    cout << to_string(results) << endl;
    saveResults(results, ProcessKey::to_string(conf.process), conf.outputFile);
    return 0;
}
