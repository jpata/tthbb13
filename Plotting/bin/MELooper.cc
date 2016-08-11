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

    // Note: this vector is made const, so that it is fully known and will not change at runtime.
    const vector<const CategoryProcessor*> categorymap = makeCategories(conf);

    cout << "Attaching branches..." << endl;
    TreeData data;
    data.loadTree(tree);

    long nentries = 0;
    long nbytes = 0;
    
    ResultMap results;


    if (conf.recalculateBTagWeight) {
        TPython::Exec("import os");
        TPython::Exec("from PhysicsTools.Heppy.physicsutils.BTagWeightCalculator import BTagWeightCalculator");
        TPython::Exec("csvpath = os.environ['CMSSW_BASE']+'/src/PhysicsTools/Heppy/data'");
        TPython::Exec("bweightcalc = BTagWeightCalculator(csvpath + '/csv_rwt_fit_hf_2015_11_20.root', csvpath + '/csv_rwt_fit_lf_2015_11_20.root')");
    }
    TStopwatch timer;
    timer.Start();
   
    long maxEntries = 0;
    if (conf.numEntries >= 0) { 
        maxEntries = conf.firstEntry + conf.numEntries;
    } else {
        maxEntries = tree->GetEntries();
    }
    cout << "Looping over events [" << conf.firstEntry << "," << maxEntries << ")" << endl;

    for (long iEntry=conf.firstEntry; iEntry < maxEntries; iEntry++) {
        const bool do_print = (conf.printEvery>0 && iEntry % conf.printEvery == 0);
       
        //std::vector<long> randoms;
        //
        //for (int ir=0; ir<1000; ir++) {
        //}
        data.init();
        nbytes += tree->GetEntry(iEntry);
        nentries += 1;
        if (iEntry == conf.firstEntry) {
            cout << "first entry " << data.run << ":" << data.lumi << ":" << data.evt << endl;
        }
        if (iEntry == maxEntries - 1) {
            cout << "last entry " << data.run << ":" << data.lumi << ":" << data.evt << endl;
        }

        if (do_print) {
            cout << "------" << endl;
            cout << "entry " << iEntry << endl;
        }

        const unordered_map<SystematicKey::SystematicKey, Event, std::hash<int> > systmap = {
            {SystematicKey::nominal, EventFactory::makeNominal(data, conf)},
            //{SystematicKey::CMS_scale_jUp, EventFactory::makeJESUp(data, conf)},
            //{SystematicKey::CMS_scale_jDown, EventFactory::makeJESDown(data, conf)},
            //{SystematicKey::CMS_scale_jUp, EventFactory::makeJERUp(data, conf)},
            //{SystematicKey::CMS_scale_jDown, EventFactory::makeJERDown(data, conf)}
        };

        for (auto& kvSyst : systmap) {
            //cout << " syst " << SystematicKey::to_string(kvSyst.first) << endl;
            const Event& event = kvSyst.second;
            //FIXME: seems that some DL events pass, even though no jets were identified 
            if (event.jets.size() == 0) {
                continue;
            }
            Configuration ev_conf(conf);
            ev_conf.process = getProcessKey(event, conf.process);
            if (do_print) {
                cout << SystematicKey::to_string(kvSyst.first) << " " << event.to_string();
            }
            for (auto& cat : categorymap) {
                cat->process(event, ev_conf, results, {}, kvSyst.first);
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
    const string outname = conf.prefix;
    saveResults(results, outname, conf.outputFile);
    return 0;
}
