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
        return ev.is_sl && ev.passPV && ev.pass_trig_sl;
    }

    bool dl(const Event& ev) {
        return ev.is_dl && ev.passPV && ev.pass_trig_dl;
    }
}

// namespace std {
//   template <> struct hash<vector<CategoryKey::CategoryKey>>
//   {
//     //const static std::hash<unsigned long> ResultKey_hash_fn;
//     size_t operator()(const vector<CategoryKey::CategoryKey> & x) const
//     {
//         //make a compound hash
//         unsigned long long r = 0;
//         int ninc = 8; // how many bits to shift each
//         int ic = 0; //shift counter
// 
//         //shift vector of category keys
//         for (auto& v : x) {
//             r += static_cast<int>(v) << (ninc*ic);        
//         }
//         std::hash<unsigned long long> _hash_fn;
//         return _hash_fn(r);
//     }
//   };
// }

const vector<CategoryKey::CategoryKey> emptykey;

// Subdivide category to blr L/H
const vector<const CategoryProcessor*> makeBTagLRCategory(double blr) {
    return {
        //No blR cut applied
        // new CategoryProcessor(
        //     [blr](const Event& ev){
        //         return true;
        //     },
        //     emptykey
        // ),
        new MEMCategoryProcessor(
            [blr](const Event& ev){
                return ev.btag_LR_4b_2b_logit<blr;
            },
            {CategoryKey::blrL}
        ),
        new MEMCategoryProcessor(
            [blr](const Event& ev){
                return ev.btag_LR_4b_2b_logit>=blr;
            },
            {CategoryKey::blrH}
        )
    };
}

// Subdivides the category to boosted and nonboosted
// Each of these is further subdivided to bLR H/L
const vector<const CategoryProcessor*> makeBoostedCategory(double blr) {
    return {
        // new CategoryProcessor(
        //     [blr](const Event& ev){
        //         return true;
        //     },
        //     emptykey,
        //     makeBTagLRCategory(blr)
        // ),
        new MEMCategoryProcessor(
            [blr](const Event& ev){
                return ev.n_excluded_bjets<2 && ev.ntopCandidate==1;
            },
            {CategoryKey::boosted},
            makeBTagLRCategory(blr)
        ),
        new MEMCategoryProcessor(
            [blr](const Event& ev){
                return !(ev.n_excluded_bjets<2 && ev.ntopCandidate==1);
            },
            {CategoryKey::nonboosted},
            makeBTagLRCategory(blr)
        ),	
        new MEMCategoryProcessor(
            [](const Event& ev){
	      return ev.n_excluded_bjets<2 && ev.ntopCandidate==1 && (ev.topCandidate_mass > 120) && (ev.topCandidate_mass < 180) ;
            },
            {CategoryKey::boostedMass120_180}
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
	      return !(ev.n_excluded_bjets<2 && ev.ntopCandidate==1 && (ev.topCandidate_mass > 120) && (ev.topCandidate_mass < 180)) ;
            },
            {CategoryKey::nonboostedMass120_180}
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
	      return ev.n_excluded_bjets<2 && ev.ntopCandidate==1 && (ev.topCandidate_mass > 140) && (ev.topCandidate_mass < 180) ;
            },
            {CategoryKey::boostedMass140_180}
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
	      return !(ev.n_excluded_bjets<2 && ev.ntopCandidate==1 && (ev.topCandidate_mass > 140) && (ev.topCandidate_mass < 180)) ;
            },
            {CategoryKey::nonboostedMass140_180}
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
	      return ev.n_excluded_bjets<2 && ev.ntopCandidate==1 && (ev.topCandidate_n_subjettiness < 0.7);
            },
            {CategoryKey::boostedTau_07}
        ),
	new MEMCategoryProcessor(
            [](const Event& ev){
	      return !(ev.n_excluded_bjets<2 && ev.ntopCandidate==1 && (ev.topCandidate_n_subjettiness < 0.7));
            },
            {CategoryKey::nonboostedTau_07}
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
	      return ev.n_excluded_bjets<2 && ev.ntopCandidate==1 && (ev.topCandidate_fRec < 0.2);
            },
            {CategoryKey::boostedfRec_02}
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
	      return !(ev.n_excluded_bjets<2 && ev.ntopCandidate==1 && (ev.topCandidate_fRec < 0.2));
            },
            {CategoryKey::nonboostedfRec_02}
        ),


    };
}

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

        //Here we define a simple category for saving the MEM
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::dl(ev) && (ev.numJets==3) && (ev.nBCSVM==2) && ev.btag_LR_4b_2b>0.95;
            },
            {CategoryKey::dl, CategoryKey::j3_t2},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::dl, CategoryKey::j3_t2}))
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::dl(ev) && (ev.numJets>=4) && (ev.nBCSVM==2) && ev.btag_LR_4b_2b>0.95;
            },
            {CategoryKey::dl, CategoryKey::jge4_t2},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::dl, CategoryKey::jge4_t2}))
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::dl(ev) && (ev.numJets>=3) && (ev.nBCSVM>=3) && ev.btag_LR_4b_2b>0.95;
            },
            {CategoryKey::dl, CategoryKey::jge3_tge3},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::dl, CategoryKey::jge4_t2}))
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::dl(ev) && (ev.numJets>=4) && (ev.nBCSVM>=4) && ev.btag_LR_4b_2b>0.95;
            },
            {CategoryKey::dl, CategoryKey::jge4_tge4},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::dl, CategoryKey::jge4_tge4}))
        ),

        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && (ev.numJets==4) && (ev.nBCSVM==3) && ev.btag_LR_4b_2b>0.95;
            },
            {CategoryKey::sl, CategoryKey::j4_t3},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::sl, CategoryKey::j4_t3}))
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && (ev.numJets==4) && (ev.nBCSVM==4) && ev.btag_LR_4b_2b>0.95;
            },
            {CategoryKey::sl, CategoryKey::j4_t4},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::sl, CategoryKey::j4_t4}))
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && (ev.numJets==5) && (ev.nBCSVM==3) && ev.btag_LR_4b_2b>0.95;
            },
            {CategoryKey::sl, CategoryKey::j5_t3},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::sl, CategoryKey::j5_t3}))
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && (ev.numJets==5) && (ev.nBCSVM>=4) && ev.btag_LR_4b_2b>0.95;
            },
            {CategoryKey::sl, CategoryKey::j5_tge4},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::sl, CategoryKey::j5_tge4}))
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && (ev.numJets>=6) && (ev.nBCSVM==2) && ev.btag_LR_4b_2b>0.95;
            },
            {CategoryKey::sl, CategoryKey::jge6_t2},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::sl, CategoryKey::jge6_t2}))
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && (ev.numJets>=6) && (ev.nBCSVM==3) && ev.btag_LR_4b_2b>0.95;
            },
            {CategoryKey::sl, CategoryKey::jge6_t3},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::sl, CategoryKey::jge6_t3}))
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && (ev.numJets>=6) && (ev.nBCSVM>=4) && ev.btag_LR_4b_2b>0.95;
            },
            {CategoryKey::sl, CategoryKey::jge6_tge4},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::sl, CategoryKey::jge6_tge4}))
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && (ev.numJets>=6) && (ev.nBCSVM>=4) && ev.btag_LR_4b_2b>0.95 && (ev.Wmass > 60 && ev.Wmass < 100) ;
            },
            {CategoryKey::sl, CategoryKey::jge6_tge4, CategoryKey::Wmass60_100},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::sl, CategoryKey::jge6_tge4}))
        ),
        new MEMCategoryProcessor(
            [](const Event& ev){
                return BaseCuts::sl(ev) && (ev.numJets>=6) && (ev.nBCSVM>=4) && ev.btag_LR_4b_2b>0.95 && !(ev.Wmass > 60 && ev.Wmass < 100) ;
            },
            {CategoryKey::sl, CategoryKey::jge6_tge4, CategoryKey::nonWmass60_100},
            makeBoostedCategory(conf.btag_LR.at({CategoryKey::sl, CategoryKey::jge6_tge4}))
        ),
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
            {SystematicKey::nominal, EventFactory::makeNominal(data)},
            {SystematicKey::CMS_scale_jUp, EventFactory::makeJESUp(data)},
            {SystematicKey::CMS_scale_jDown, EventFactory::makeJESDown(data)}
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
    saveResults(results, conf.process, conf.outputFile);
    return 0;
}
