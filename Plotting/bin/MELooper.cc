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
    return tree;
}

namespace BaseCuts {
    bool sl(const Event& ev) {
        return ev.is_sl && ev.passPV && ev.pass_trig_sl;
    }

    bool dl(const Event& ev) {
        return ev.is_dl && ev.passPV && ev.pass_trig_dl;
    }
}

namespace std {
  template <> struct hash<vector<CategoryKey::CategoryKey>>
  {
    //const static std::hash<unsigned long> ResultKey_hash_fn;
    size_t operator()(const vector<CategoryKey::CategoryKey> & x) const
    {
        //make a compound hash
        unsigned long long r = 0;
        int ninc = 8; // how many bits to shift each
        int ic = 0; //shift counter

        //shift vector of category keys
        for (auto& v : x) {
            r += static_cast<int>(v) << (ninc*ic);        
        }
        std::hash<unsigned long long> _hash_fn;
        return _hash_fn(r);
    }
  };
}

const unordered_map<
    vector<CategoryKey::CategoryKey>,
    const CategoryProcessor*,
    std::hash<vector<CategoryKey::CategoryKey>>
> categorymap = {
    {
    {CategoryKey::dl, CategoryKey::j3_t2},
    new MEMCategoryProcessor(
        [](const Event& ev){
            return BaseCuts::dl(ev) && (ev.numJets==3) && (ev.nBCSVM==2);
        }
    )
    },

    {
    {CategoryKey::dl, CategoryKey::jge4_t2},
    new MEMCategoryProcessor(
        [](const Event& ev){
            return BaseCuts::dl(ev) && (ev.numJets>=4) && (ev.nBCSVM==2);
        }
    )
    },


    {
    {CategoryKey::dl, CategoryKey::jge3_tge3},
    new MEMCategoryProcessor(
        [](const Event& ev){
            return BaseCuts::dl(ev) && (ev.numJets>=3) && (ev.nBCSVM>=3);
        }
    )
    },

    {
    {CategoryKey::dl, CategoryKey::jge4_tge4},
    new MEMCategoryProcessor(
        [](const Event& ev){
            return BaseCuts::dl(ev) && (ev.numJets>=4) && (ev.nBCSVM>=4);
        }
    )
    },
    {
    {CategoryKey::sl, CategoryKey::j5_t3},
    new MEMCategoryProcessor(
        [](const Event& ev){
            return BaseCuts::sl(ev) && (ev.numJets==5) && (ev.nBCSVM==3);
        }
    )
    },

    {
    {CategoryKey::sl, CategoryKey::j5_tge4},
    new MEMCategoryProcessor(
        [](const Event& ev){
            return BaseCuts::sl(ev) && (ev.numJets==5) && (ev.nBCSVM>=4);
        }
    )
    },
    {
    {CategoryKey::sl, CategoryKey::jge6_t2},
    new CategoryProcessor(
        [](const Event& ev){
            return BaseCuts::sl(ev) && (ev.numJets>=6) && (ev.nBCSVM==2);
        }
    )
    },

    {
    {CategoryKey::sl, CategoryKey::jge6_t3},
    new MEMCategoryProcessor(
        [](const Event& ev){
            return BaseCuts::sl(ev) && (ev.numJets>=6) && (ev.nBCSVM==3);
        }
    )
    },

    {
    {CategoryKey::sl, CategoryKey::jge6_tge4},
    new MEMCategoryProcessor(
        [](const Event& ev){
            return BaseCuts::sl(ev) && (ev.numJets>=6) && (ev.nBCSVM>=4);
        }
    )
    },
};

int main(int argc, const char** argv) {
    //Switch off histogram naming for memory management
    TH1::AddDirectory(false);

    const Configuration conf = parseArgs(argc, argv);
    TChain* tree = loadFiles(conf);

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
            {SystematicKey::nominal, EventFactory::makeNominal(data)},
            {SystematicKey::CMS_scale_jUp, EventFactory::makeJESUp(data)},
            {SystematicKey::CMS_scale_jDown, EventFactory::makeJESDown(data)}
        };

        for (auto& kvSyst : systmap) {
            const Event& event = kvSyst.second;
            if (do_print) {
                cout << SystematicKey::to_string(kvSyst.first) << " " << event.to_string();
            }
            for (auto& kvCat : categorymap) {
                const bool passes = (*kvCat.second)(event);
                if (passes) {
                    for (auto& kvWeight : event.weightFuncs) {
                        const double weight = conf.lumi * kvWeight.second(event);
                        if (do_print) {
                            cout << "w " << SystematicKey::to_string(kvWeight.first) << " " << weight << endl;;
                        }

                        SystematicKey::SystematicKey systKey = kvSyst.first;
                        if (kvSyst.first == SystematicKey::nominal) {
                            systKey = kvWeight.first;
                        }
                        kvCat.second->fillHistograms(
                            event, results,
                            make_tuple(kvCat.first, systKey),
                            weight
                        );
                    } // weightFuncs
                } // passes
            } //categorymap
        } // systmap
    } //entries

    //Finalize with output
    cout << "Read " << nbytes/1024/1024 << " Mb" << endl;
    cout << to_string(results) << endl;
    saveResults(results, conf.process, "ControlPlots.root");
    return 0;
}
