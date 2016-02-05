#include "TFile.h"
#include "TChain.h"
#include "TStopwatch.h"
#include <iostream>

#include "TTH/Plotting/interface/Event.h"
#include "TTH/Plotting/interface/categories.h"

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
    //tree->SetCacheSize(10 * 1024 * 1024);
    //tree->AddBranchToCache("*");
    return tree;
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
    const vector<const CategoryProcessor*> categorymap = makeCategories(conf);

    cout << "Attaching branches..." << endl;
    TreeData data;
    data.loadTree(tree);

    long nentries = 0;
    long nbytes = 0;
    
    ResultMap results;

    cout << "Looping over events [" << conf.firstEntry << "," << conf.firstEntry+conf.numEntries << ")" << endl;

    if (conf.recalculateBTagWeight) {
        TPython::Exec("import os");
        TPython::Exec("from PhysicsTools.Heppy.physicsutils.BTagWeightCalculator import BTagWeightCalculator");
        TPython::Exec("csvpath = os.environ['CMSSW_BASE']+'/src/PhysicsTools/Heppy/data'");
        TPython::Exec("bweightcalc = BTagWeightCalculator(csvpath + '/csv_rwt_fit_hf_2015_11_20.root', csvpath + '/csv_rwt_fit_lf_2015_11_20.root')");
    }
    TStopwatch timer;
    timer.Start();

    for (long iEntry=conf.firstEntry; iEntry<conf.firstEntry+conf.numEntries; iEntry++) {

        const bool do_print = (conf.printEvery>0 && iEntry % conf.printEvery == 0);
        //std::vector<long> randoms;
        //
        //for (int ir=0; ir<1000; ir++) {
        //}
        data.init();
        nbytes += tree->GetEntry(iEntry);
        nentries += 1;
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
    timer.Stop();
    double t_real = timer.RealTime();
    double t_cpu = timer.CpuTime();

    //Finalize with output
    cout << "Read " << nbytes/1024/1024 << " MB" << endl;
    cout << "speedMB " << (double)nbytes/1024.0/1024.0 / t_real << " MB/s (real) " << (double)nbytes/1024.0/1024.0 / t_cpu << " MB/s (cpu)" << endl; 
    cout << "speedEV " << (double)nentries / t_real << " ev/s (real) " << (double)nentries / t_cpu << " ev/s (cpu)" << endl; 
    cout << to_string(results) << endl;
    const string outname = ProcessKey::to_string(conf.process) + conf.prefix;
    saveResults(results, outname, conf.outputFile);
    return 0;
}
