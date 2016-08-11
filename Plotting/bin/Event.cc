#include "TTH/Plotting/interface/Event.h"
#include "TTH/Plotting/interface/metree.h"

using namespace std;

double logit(double x) {
    return log(x/(1.0 - x));
}

namespace trigger {
    bool mumu(const TreeData& data) {
        return (
            data.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v ||
            data.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v
        );
    }
    bool emu(const TreeData& data) {
        return (
            data.HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v ||
            data.HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v
        );
    }
    bool ee(const TreeData& data) {
        return (
            data.HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v
        );
    }
    
    bool sl_el(const TreeData& data) {
        return (
            data.HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_v
        );
    }
    
    bool sl_mu(const TreeData& data) {
        return (
            data.HLT_BIT_HLT_IsoMu20_v ||
            data.HLT_BIT_HLT_IsoTkMu20_v
        );
    }
}


//Evaluate mem probability
double mem_p(double p_tth, double p_ttbb, double w=0.15) {
    return p_tth > 0.0 ? p_tth / (p_tth + w * p_ttbb) : 0.0;
}

//http://stackoverflow.com/questions/236129/split-a-string-in-c
std::vector<std::string>& split(const std::string &s, char delim, std::vector<std::string> &elems) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}


std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, elems);
    return elems;
}

//Functions that define how an axis in the sparse histogram should be filled
const map<string, AxisFunction> AxisFunctions = {
    {"counting", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return 1;}},
    {"eventParity", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.data->evt%2;}},

    //tt+bb discriminators
    {"mem_SL_0w2h2t", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.mem_SL_0w2h2t;}},
    {"mem_SL_1w2h2t", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.mem_SL_1w2h2t;}},
    {"mem_SL_2w2h2t", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.mem_SL_2w2h2t;}},
    {"mem_SL_2w2h2t_sj", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.mem_SL_2w2h2t_sj;}},
    {"mem_DL_0w2h2t", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.mem_DL_0w2h2t;}},
    {"common_bdt", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.common_bdt;}},

    //categorization variables
    {"numJets", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.numJets;}},
    {"nBCSVM", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.nBCSVM;}},
    {"nBCMVAM", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.nBCMVAM;}},
    {"nBCSVL", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.nBCSVL;}},
    {"bkgCat1", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) {
        const int ttCls = ev.data->ttCls;
        if (ev.data->ttCls == 51) {
            return 1;
        }
        else if (ev.data->ttCls == 52) {
            return 2;
        }
        else if (ev.data->ttCls >= 53) {
            return 3;
        }
        else if (ev.data->ttCls >= 41) {
            return 4;
        }
        else if (ev.data->ttCls <= 0) {
            return 0;
        }
    }},

    //Resolved control variables
    {"Wmass", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.Wmass;}},
    {"jet0_pt", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.jets.size() > 0 ? ev.jets.at(0).p4.Pt() : -99;}},
    {"jet0_eta", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.jets.size() > 0 ? ev.jets.at(0).p4.Eta() : -99;}},
    {"jet0_btagCSV", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.jets.size() > 0 ? ev.jets.at(0).btagCSV : -99;}},
    {"jet1_pt", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.jets.size() > 1 ? ev.jets.at(1).p4.Pt() : -99;}},
    {"jet1_eta", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.jets.size() > 1 ? ev.jets.at(1).p4.Eta() : -99;}},
    {"jet1_btagCSV", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.jets.size() > 1 ? ev.jets.at(1).btagCSV : -99;}},
    {"lep0_pt", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.leptons.size() > 0 ? ev.leptons.at(0).p4.Pt() : -99;}},
    {"lep0_eta", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.leptons.size() > 0 ? ev.leptons.at(0).p4.Eta() : -99;}},
    {"btag_LR_4b_2b_logit_btagCSV", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return logit(ev.blr1);}},
    {"btag_LR_4b_2b_logit_btagCMVA", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return logit(ev.blr2);}},
   
    //boosted control variables
    {"topCandidate_mass", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.topCandidate_mass;}},
    {"topCandidate_fRec", [](const Event& ev, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { return ev.topCandidate_fRec;}},
    
    //This is needed to correctly divide the data 
    {"leptonFlavour", [](const Event& event, const ProcessKey::ProcessKey& proc, const vector<CategoryKey::CategoryKey>& cats, const SystematicKey::SystematicKey& syst) { 
        if (BaseCuts::sl_mu(event)) {
            return 1;
        }
        else if (BaseCuts::sl_el(event)) {
            return 2;
        }
        else if (BaseCuts::dl_mumu(event)) {
            return 3;
        }
        else if (BaseCuts::dl_emu(event)) {
            return 4;
        }
        else if (BaseCuts::dl_ee(event)) {
            return 5;
        }
        return 0;
    }}
};

const Configuration Configuration::makeConfiguration(JsonValue& value) {
    vector<string> filenames;
    double lumi = -1.0;
    double xsweight = -1.0;
    ProcessKey::ProcessKey process = ProcessKey::UNKNOWN;
    string prefix;
    string outputFile = "UNDEFINED";
    long firstEntry = -1;
    long numEntries = -1;
    long printEvery = -1;
    
    vector<vector<CategoryKey::CategoryKey>> enabledCategories;

    vector<SparseAxis> sparseAxes;
    for (auto lev1 : value) {
        const string ks = string(lev1->key);
        if (ks == "filenames") {
            for (auto lev2 : lev1->value) {
                if (lev2->value.getTag() == JSON_STRING) {
                    filenames.push_back(lev2->value.toString());
                }
            }
        }
        else if (ks == "lumi") {
            lumi = lev1->value.toNumber();
        }
        else if (ks == "xsweight") {
            xsweight = lev1->value.toNumber();
        }
        else if (ks == "enabledCategories") {
            //loop over list of enabled categories

            for (auto lev2 : lev1->value) {
                vector<CategoryKey::CategoryKey> keys;
                //Loop over category keys
                for (auto lev3 : lev2->value) {
                    keys.push_back(CategoryKey::from_string(lev3->value.toString()));
                }
                enabledCategories.push_back(keys);
            }
        }
        else if (ks == "process") {
            process = ProcessKey::from_string(lev1->value.toString());
        }
        else if (ks == "prefix") {
            prefix = lev1->value.toString();
        }
        else if (ks == "firstEntry") {
            firstEntry = (long)(lev1->value.toNumber());
        }
        else if (ks == "numEntries") {
            numEntries = (long)(lev1->value.toNumber());
        }
        else if (ks == "printEvery") {
            printEvery = (long)(lev1->value.toNumber());
        }
        else if (ks == "outputFile") {
            outputFile = lev1->value.toString();
        }
        else if (ks == "sparseAxes") {
            //loop over list of sparse
            for (auto lev2 : lev1->value) {

                AxisFunction _func;
                int nBins = -1;
                float xMin = 0.0;
                float xMax = 0.0;
                string name;
                //loop over keys in one sparse axis
                for (auto lev3 : lev2->value) {
                    const string spk = string(lev3->key);
                    if (spk == "func") {
                        name = lev3->value.toString();
                        if (AxisFunctions.find(name) == AxisFunctions.end()) {
                            cerr << "could not find function " << name << " in map of predefined functions: AxisFunctions" << endl;
                            throw std::runtime_error("UndefinedAxisFunction");
                        }
                        _func = AxisFunctions.at(name);
                    } else if (spk == "nBins") {
                        nBins = (int)(lev3->value.toNumber());
                        assert(nBins > 0);
                    } else if (spk == "xMin") {
                        xMin = (float)(lev3->value.toNumber());
                    } else if (spk == "xMax") {
                        xMax = (float)(lev3->value.toNumber());
                    }
                }
                assert(xMax>xMin);
                sparseAxes.push_back(
                    SparseAxis(name, _func, nBins, xMin, xMax)
                );
            }
        }
    }
    return Configuration(
        filenames,
        lumi,
        xsweight,
        process,
        prefix,
        firstEntry, numEntries, printEvery,
        outputFile,
        sparseAxes,
        enabledCategories
    );
}

string Configuration::to_string() const {
    stringstream ss;
    ss << "Configuration(" << endl;;
    for (auto fn : this->filenames) {
        ss << "  file=" << fn << "," << endl;
    }
    ss << "  lumi=" << this->lumi << endl;
    ss << "  process=" << this->process << endl;
    ss << "  prefix=" << this->prefix << endl;
    ss << "  firstEntry=" << this->firstEntry << endl;
    ss << "  numEntries=" << this->numEntries << endl;
    ss << ")" << endl;
    return ss.str();
}
//["n_excluded_bjets<2", "ntopCandidate==1"]

namespace CategoryKey {
    bool is_sl(vector<CategoryKey> k) {
        return k[0] == sl;
    }

    bool is_dl(vector<CategoryKey> k) {
        return k[0] == dl;
    }

    bool is_any(vector<CategoryKey> k) {
        return (is_sl(k) || is_dl(k));
    }
}

void saveResults(ResultMap& res, const string& prefix, const string& filename) {
    cout << "Saving results to " << filename << ":" << prefix << endl;
    TFile of(filename.c_str(), "RECREATE");
    
    vector<ResultMap::key_type> resKeys;
    for (auto& kv : res) {
        resKeys.push_back(kv.first);
    }
    sort(resKeys.begin(), resKeys.end());

    for (auto rk : resKeys) {
        const auto procKey = get<0>(rk);
        const auto systKey = get<2>(rk);
        const auto histKey = get<3>(rk);

        //Add all categories together with underscores
        int ind = 0;
        stringstream ss;
        ss << prefix << "/";
        ss << ProcessKey::to_string(procKey) << "/";
        for (auto& catKey : get<1>(rk)) {
            ss << CategoryKey::to_string(catKey);
            if (ind < get<1>(rk).size() - 1) {
                ss << "_";
            }
            ind++;
        }
        //make root dir if doesn't exist
        const string dirname = ss.str();
        cout << "dirname=" << dirname << endl;
        TDirectory* dir = (TDirectory*)(of.Get(dirname.c_str()));
        if (dir == nullptr) {
            of.mkdir(dirname.c_str());
            dir = (TDirectory*)(of.Get(dirname.c_str()));
        }
        assert(dir != nullptr);
        
        //rename histogram
        stringstream ss2;
        ss2 << HistogramKey::to_string(histKey);

        //For variations, add also systematic name to histogram
        if (systKey != SystematicKey::nominal) {
            ss2 << "_" << SystematicKey::to_string(systKey);
        }
        const string histname = ss2.str();
        assert(dir->Get(histname.c_str()) == nullptr);
        cout << dirname << "/" << histname << endl;

        //We need to make a copy of the histogram here, otherwise ROOT scoping goes crazy
        //and of.Close() segfaults later
        TNamed* obj = (TNamed*)(res.at(rk))->Clone();
        obj->SetName(histname.c_str());
        dir->Add(obj);
        //cout << "writing... ";
        //dir->Write("", TObject::kOverwrite);
        //cout << "done" << endl;
    }
    cout << "writing..." << endl;
    of.Write();
    of.Close();
    cout << "done..." << endl;
}


Event::Event(
    const TreeData *_data,
    bool _is_sl,
    bool _is_dl,
    bool _passPV,
    int _numJets,
    int _nBCSVM,
    int _nBCSVL,
    const vector<Jet>& _jets,
    const vector<Lepton>& _leptons,
    double _weight_xs,
    double _puWeight,
    double _Wmass,
    double _mem_SL_0w2h2t,
    double _mem_SL_1w2h2t,
    double _mem_SL_2w2h2t,
    double _mem_SL_2w2h2t_sj,
    double _mem_DL_0w2h2t,
    double _tth_mva,
    double _common_bdt,
    double _blr1,
    double _blr2
    ) :
    data(_data),
    is_sl(_is_sl),
    is_dl(_is_dl),
    passPV(_passPV),
    numJets(_numJets),
    nBCSVM(_nBCSVM),
    nBCSVL(_nBCSVL),
    jets(_jets),
    leptons(_leptons),
    weight_xs(_weight_xs),
    puWeight(_puWeight),
    Wmass(_Wmass),
    mem_SL_0w2h2t(_mem_SL_0w2h2t),
    mem_SL_1w2h2t(_mem_SL_1w2h2t),
    mem_SL_2w2h2t(_mem_SL_2w2h2t),
    mem_SL_2w2h2t_sj(_mem_SL_2w2h2t_sj),
    mem_DL_0w2h2t(_mem_DL_0w2h2t),
    tth_mva(_tth_mva),
    common_bdt(_common_bdt),
    blr1(_blr1),
    blr2(_blr2)
{
    
}


const string Event::to_string() const {
    stringstream ss;
    ss << "Event(" << this->numJets << "J, " << this->nBCSVM << "T";
    ss << endl;
    for (auto& jet : this->jets) {
        ss << " j " << jet.to_string() << endl;
    }
    ss << ");" << endl;
    return ss.str();
}
//jetMaker - a function from JetFactory to make the jets
const vector<Jet> makeAllJets(const TreeData& data,
    const Jet (*jetMaker)(const TreeData&, int)) {
    vector<Jet> jets;

    for (int nj=0; nj<data.njets; nj++) {
        const Jet& jet = jetMaker(data, nj); 
        jets.push_back(jet);
    }
    return jets;
}


const vector<Lepton> makeAllLeptons(const TreeData& data) {
    vector<Lepton> leps;
    assert(data.is_sl && data.nleps==1 || data.is_dl && data.nleps==2 || data.nleps==0);
    for (int n=0; n<data.nleps; n++) {
        TLorentzVector p4;
        p4.SetPtEtaPhiM(
            data.leps_pt[n],
            data.leps_eta[n],
            data.leps_phi[n],
            data.leps_mass[n]
        );
        Lepton lep(p4, (int)(data.leps_pdgId[n]));
        leps.push_back(lep);
    }
    return leps;
}

bool isData(ProcessKey::ProcessKey proc) {
    return (
        proc == ProcessKey::SingleMuon ||
        proc == ProcessKey::SingleElectron ||
        proc == ProcessKey::DoubleMuon ||
        proc == ProcessKey::DoubleEG ||
        proc == ProcessKey::MuonEG
    );
}

bool isMC(ProcessKey::ProcessKey proc) {
    return !isData(proc);
}

bool isSignalMC(ProcessKey::ProcessKey proc) {
    return (
        proc == ProcessKey::ttH ||
        proc == ProcessKey::ttH_hbb
    );
}

//Given a base process key, e.g. ttbarUnsplit, produces a final process key, e.g. ttbarOther,
//based on the properties of the event
ProcessKey::ProcessKey getProcessKey(const Event& ev, ProcessKey::ProcessKey proc_key) {
    if (proc_key == ProcessKey::ttbarUnsplit) {
        if (ev.data->ttCls == 51) {
            return ProcessKey::ttbarPlusB;
        }
        else if (ev.data->ttCls == 52) {
            return ProcessKey::ttbarPlus2B;
        }
        else if (ev.data->ttCls >= 53) {
            return ProcessKey::ttbarPlusBBbar;
        }
        else if (ev.data->ttCls >= 41) {
            return ProcessKey::ttbarPlusCCbar;
        }
        else if (ev.data->ttCls <= 0) {
            return ProcessKey::ttbarOther;
        }
    }
    return proc_key;
}

double nominal_weight(const Event& ev, const Configuration& conf) {
    if (isMC(conf.process)) {
        return conf.lumi * conf.xsweight * ev.puWeight * ev.data->bTagWeight * process_weight(conf.process, conf) * ev.data->genWeight;
    }
    return 1.0;
}

///FIXME: these ad-hoc process weights are here to fix a wrong value of nGen in processing
double process_weight(ProcessKey::ProcessKey proc, const Configuration& conf) {

    double w = 1.0;

    switch(proc) {
        case ProcessKey::ttbarPlusBBbar:
        case ProcessKey::ttbarPlusB:
        case ProcessKey::ttbarPlus2B:
        case ProcessKey::ttbarPlusCCbar:
        case ProcessKey::ttbarOther:
        case ProcessKey::ttH_hbb:
        default:
            return w;
    }
    return w;
}

const char* btag_syst_to_string(SystematicKey::SystematicKey syst) {
    switch (syst) {
        case SystematicKey::nominal:
            return "nominal";
        case SystematicKey::CMS_ttH_CSVcErr1Up:
            return "cErr1Up";
        case SystematicKey::CMS_ttH_CSVcErr1Down:
            return "cErr1Down";
        case SystematicKey::CMS_ttH_CSVcErr2Up:
            return "cErr2Up";
        case SystematicKey::CMS_ttH_CSVcErr2Down:
            return "cErr2Down";
        case SystematicKey::CMS_ttH_CSVLFUp:
            return "LFUp";
        case SystematicKey::CMS_ttH_CSVLFDown:
            return "LFDown";
        case SystematicKey::CMS_ttH_CSVHFUp:
            return "HFUp";
        case SystematicKey::CMS_ttH_CSVHFDown:
            return "HFDown";
        case SystematicKey::CMS_ttH_CSVLFStats1Up:
            return "LFStats1Up";
        case SystematicKey::CMS_ttH_CSVLFStats1Down:
            return "LFStats1Down";
        case SystematicKey::CMS_ttH_CSVLFStats2Up:
            return "LFStats2Up";
        case SystematicKey::CMS_ttH_CSVLFStats2Down:
            return "LFStats2Down";
        case SystematicKey::CMS_ttH_CSVHFStats1Up:
            return "HFStats1Up";
        case SystematicKey::CMS_ttH_CSVHFStats1Down:
            return "HFStats1Down";
        case SystematicKey::CMS_ttH_CSVHFStats2Up:
            return "HFStats2Up";
        case SystematicKey::CMS_ttH_CSVHFStats2Down:
            return "HFStats2Down";
        default:
            return "none";
    };
}

//map<SystematicKey::SystematicKey, double> recalc_bweights(vector<Jet> jets) {
//    const auto btag_syst = { 
//        SystematicKey::nominal,
//        SystematicKey::CMS_ttH_CSVcErr1Up,
//        SystematicKey::CMS_ttH_CSVcErr1Down,
//        SystematicKey::CMS_ttH_CSVcErr2Up,
//        SystematicKey::CMS_ttH_CSVcErr2Down,
//        SystematicKey::CMS_ttH_CSVLFUp,
//        SystematicKey::CMS_ttH_CSVLFDown,
//        SystematicKey::CMS_ttH_CSVHFUp,
//        SystematicKey::CMS_ttH_CSVHFDown,
//        SystematicKey::CMS_ttH_CSVHFStats1Up,
//        SystematicKey::CMS_ttH_CSVHFStats1Down,
//        SystematicKey::CMS_ttH_CSVHFStats2Up,
//        SystematicKey::CMS_ttH_CSVHFStats2Down,
//        SystematicKey::CMS_ttH_CSVLFStats1Up,
//        SystematicKey::CMS_ttH_CSVLFStats1Down,
//        SystematicKey::CMS_ttH_CSVLFStats2Up,
//        SystematicKey::CMS_ttH_CSVLFStats2Down,
//    };
//
//    map<SystematicKey::SystematicKey, double> bweights;
//    for (auto k : btag_syst) {
//        bweights[k] = 1.0;
//    }
//
//    for (auto & jet : jets) {
//        for (auto syst : btag_syst) {
//            stringstream s;
//            if (
//                std::isnan(jet.p4.Eta()) ||
//                std::isnan(jet.p4.Pt()) ||
//                std::isnan(jet.btagCSV)
//            ) {
//                std::cerr << "bad jet " << jet.p4.Pt() << " " << jet.p4.Eta() << " " << jet.btagCSV << " " << jet.hadronFlavour << std::endl;
//                continue;
//            }
//            s << "bweightcalc.calcJetWeightImpl("
//                << jet.p4.Pt() <<"," << std::abs(jet.p4.Eta())
//                << "," << jet.hadronFlavour
//                << "," << jet.btagCSV
//                << ",\"final\",\"" << btag_syst_to_string(syst) << "\")";
//            double ret = (double)(TPython::Eval(s.str().c_str()));
//            bweights[syst] *= ret;
//        }
//    }
//    return bweights;
//}

//map<SystematicKey::SystematicKey, double> get_bweights(const TreeData& data) {
//    map<SystematicKey::SystematicKey, double> bweight;
//    bweight[SystematicKey::nominal] = data.bTagWeight;
//    bweight[SystematicKey::CMS_ttH_CSVcErr1Up] = data.bTagWeight_cErr1Up;
//    bweight[SystematicKey::CMS_ttH_CSVcErr1Down] = data.bTagWeight_cErr1Down;
//    bweight[SystematicKey::CMS_ttH_CSVcErr2Up] =  data.bTagWeight_cErr2Up;
//    bweight[SystematicKey::CMS_ttH_CSVcErr2Down] =  data.bTagWeight_cErr2Down;
//    bweight[SystematicKey::CMS_ttH_CSVLFUp] =  data.bTagWeight_LFUp;
//    bweight[SystematicKey::CMS_ttH_CSVLFDown] =  data.bTagWeight_LFDown;
//    bweight[SystematicKey::CMS_ttH_CSVHFUp] =  data.bTagWeight_HFUp;
//    bweight[SystematicKey::CMS_ttH_CSVHFDown] =  data.bTagWeight_HFDown;
//    bweight[SystematicKey::CMS_ttH_CSVHFStats1Up] =  0.0;
//    bweight[SystematicKey::CMS_ttH_CSVHFStats1Down] =  0.0;
//    bweight[SystematicKey::CMS_ttH_CSVLFStats1Up] =  0.0;
//    bweight[SystematicKey::CMS_ttH_CSVLFStats1Down] =  0.0;
//    bweight[SystematicKey::CMS_ttH_CSVHFStats2Up] =  0.0;
//    bweight[SystematicKey::CMS_ttH_CSVHFStats2Down] =  0.0;
//    bweight[SystematicKey::CMS_ttH_CSVLFStats2Up] =  0.0;
//    bweight[SystematicKey::CMS_ttH_CSVLFStats2Down] =  0.0;
//    return bweight;
//}

const Event EventFactory::makeNominal(const TreeData& data, const Configuration& conf) {
    const vector<Jet> jets = makeAllJets(data, &(JetFactory::makeNominal));
    const vector<Lepton> leptons = makeAllLeptons(data);

    const Event ev(
        &data,
        data.is_sl,
        data.is_dl,
        data.passPV,
        data.numJets,
        data.nBCSVM,
        data.nBCSVL,
        data.nBCMVAM,
        jets,
        leptons,
        1.0,
        data.puWeight,
        data.Wmass,
        mem_p(data.mem_tth_SL_0w2h2t_p[0], data.mem_ttbb_SL_0w2h2t_p[0]),
        mem_p(data.mem_tth_SL_1w2h2t_p[0], data.mem_ttbb_SL_1w2h2t_p[0]),
        mem_p(data.mem_tth_SL_2w2h2t_p[0], data.mem_ttbb_SL_2w2h2t_p[0]), //SL 222
        0.0,
        //mem_p(data.mem_tth_SL_2w2h2t_sj_p[0], data.mem_ttbb_SL_2w2h2t_sh_p[0], 0.05), //SL 222 sj
        mem_p(data.mem_tth_DL_0w2h2t_p[0], data.mem_ttbb_DL_0w2h2t_p[0]), //DL 022,
        data.tth_mva,
        data.common_bdt,
        logit(data.btag_LR_4b_2b_btagCSV),
        logit(data.btag_LR_4b_2b_btagCMVA)
    );
    return ev;
}

//const Event EventFactory::makeJESUp(const TreeData& data, const Configuration& conf) {
//    const vector<Jet> jets = makeAllJets(data, &(JetFactory::makeJESUp));
//    const vector<Lepton> leptons = makeAllLeptons(data);
//
//    return Event(
//        &data,
//        data.is_sl,
//        data.is_dl,
//        data.passPV,
//        data.numJets_JESUp,
//        data.nBCSVM_JESUp,
//        data.nBCSVL_JESUp,
//        jets,
//        leptons,
//        data.weight_xs,
//        data.puWeight,
//        data.Wmass,
//        mem_p(data.mem_tth_JESUp_p[0], data.mem_ttbb_JESUp_p[0]), //SL 022
//        mem_p(data.mem_tth_JESUp_p[2], data.mem_ttbb_JESUp_p[2]), //SL 122
//        mem_p(data.mem_tth_JESUp_p[5], data.mem_ttbb_JESUp_p[5]), //SL 222
//        mem_p(data.mem_tth_JESUp_p[9], data.mem_ttbb_JESUp_p[9], 0.05), //SL 222 sj
//        mem_p(data.mem_tth_JESUp_p[1], data.mem_ttbb_JESUp_p[1]), //DL 022,
//        data.tth_mva_JESUp,
//        data.common_bdt_JESUp,
//        logit(data.btag_LR_4b_2b_btagCSV_JESUp),
//        logit(data.btag_LR_4b_2b_btagCMVA_JESUp)
//    );
//}
//
//const Event EventFactory::makeJESDown(const TreeData& data, const Configuration& conf) {
//    const vector<Jet> jets = makeAllJets(data, &(JetFactory::makeJESDown));
//    const vector<Lepton> leptons = makeAllLeptons(data);
//
//    return Event(
//        &data,
//        data.is_sl,
//        data.is_dl,
//        data.passPV,
//        data.numJets_JESDown,
//        data.nBCSVM_JESDown,
//        data.nBCSVL_JESDown,
//        jets,
//        leptons,
//        data.weight_xs,
//        data.puWeight,
//        data.Wmass,
//        mem_p(data.mem_tth_JESDown_p[0], data.mem_ttbb_JESDown_p[0]), //SL 022
//        mem_p(data.mem_tth_JESDown_p[2], data.mem_ttbb_JESDown_p[2]), //SL 122
//        mem_p(data.mem_tth_JESDown_p[5], data.mem_ttbb_JESDown_p[5]), //SL 222
//        mem_p(data.mem_tth_JESDown_p[9], data.mem_ttbb_JESDown_p[9], 0.05), //SL 222 sj
//        mem_p(data.mem_tth_JESDown_p[1], data.mem_ttbb_JESDown_p[1]), //DL 022,
//        data.tth_mva,
//        data.common_bdt_JESDown,
//        logit(data.btag_LR_4b_2b_btagCSV_JESDown),
//        logit(data.btag_LR_4b_2b_btagCMVA_JESDown)
//    );
//}
//
//const Event EventFactory::makeJERUp(const TreeData& data, const Configuration& conf) {
//    const vector<Jet> jets = makeAllJets(data, &(JetFactory::makeJERUp));
//    const vector<Lepton> leptons = makeAllLeptons(data);
//
//    return Event(
//        &data,
//        data.is_sl,
//        data.is_dl,
//        data.passPV,
//        data.numJets_JERUp,
//        data.nBCSVM_JERUp,
//        data.nBCSVL_JERUp,
//        jets,
//        leptons,
//        data.weight_xs,
//        data.puWeight,
//        data.Wmass,
//        mem_p(data.mem_tth_JERUp_p[0], data.mem_ttbb_JERUp_p[0]), //SL 022
//        mem_p(data.mem_tth_JERUp_p[2], data.mem_ttbb_JERUp_p[2]), //SL 122
//        mem_p(data.mem_tth_JERUp_p[5], data.mem_ttbb_JERUp_p[5]), //SL 222
//        mem_p(data.mem_tth_JERUp_p[9], data.mem_ttbb_JERUp_p[9], 0.05), //SL 222 sj
//        mem_p(data.mem_tth_JERUp_p[1], data.mem_ttbb_JERUp_p[1]), //DL 022,
//        data.tth_mva_JERUp,
//        data.common_bdt_JERUp,
//        logit(data.btag_LR_4b_2b_btagCSV_JERUp),
//        logit(data.btag_LR_4b_2b_btagCMVA_JERUp)
//    );
//}
//
//const Event EventFactory::makeJERDown(const TreeData& data, const Configuration& conf) {
//    const vector<Jet> jets = makeAllJets(data, &(JetFactory::makeJERDown));
//    const vector<Lepton> leptons = makeAllLeptons(data);
//
//    return Event(
//        &data,
//        data.is_sl,
//        data.is_dl,
//        data.passPV,
//        data.numJets_JERDown,
//        data.nBCSVM_JERDown,
//        data.nBCSVL_JERDown,
//        jets,
//        leptons,
//        data.weight_xs,
//        data.puWeight,
//        data.Wmass,
//        mem_p(data.mem_tth_JERDown_p[0], data.mem_ttbb_JERDown_p[0]), //SL 022
//        mem_p(data.mem_tth_JERDown_p[2], data.mem_ttbb_JERDown_p[2]), //SL 122
//        mem_p(data.mem_tth_JERDown_p[5], data.mem_ttbb_JERDown_p[5]), //SL 222
//        mem_p(data.mem_tth_JERDown_p[9], data.mem_ttbb_JERDown_p[9], 0.05), //SL 222 sj
//        mem_p(data.mem_tth_JERDown_p[1], data.mem_ttbb_JERDown_p[1]), //DL 022,
//        data.tth_mva,
//        data.common_bdt_JERDown,
//        logit(data.btag_LR_4b_2b_btagCSV_JERDown),
//        logit(data.btag_LR_4b_2b_btagCMVA_JERDown)
//    );
//}


Jet::Jet(TLorentzVector& _p4, float _btagCSV, float _btagBDT, int _hadronFlavour) :
    p4(_p4),
    btagCSV(_btagCSV),
    btagBDT(_btagBDT),
    hadronFlavour(_hadronFlavour)
{
}

Lepton::Lepton(const TLorentzVector& _p4, int _pdgId) : 
    p4(_p4),
    pdgId(_pdgId)
{
}

const Jet JetFactory::makeNominal(const TreeData& data, int njet) {
    assert(njet <= data.njets);
    TLorentzVector p4;
    p4.SetPtEtaPhiM(
        data.jets_pt[njet],
        data.jets_eta[njet],
        data.jets_phi[njet],
        data.jets_mass[njet]
    );

    double csv = data.jets_btagCSV[njet];
    if (std::isnan(csv)) {
        csv = -10.0;
    }
    return Jet(
        p4,
        csv,
        data.jets_btagCMVA[njet],
        data.jets_hadronFlavour[njet]
    );
}

//const Jet JetFactory::makeJESUp(const TreeData& data, int njet) {
//    assert(njet <= data.njets);
//    TLorentzVector p4;
//    p4.SetPtEtaPhiM(
//        data.jets_pt[njet],
//        data.jets_eta[njet],
//        data.jets_phi[njet],
//        data.jets_mass[njet]
//    );
//    //Undo nominal correction, re-do JESUp correction
//    const double corr = data.jets_corr_JESUp[njet] / data.jets_corr[njet];
//    p4 *= (1.0 / corr);
//    double csv = data.jets_btagCSV[njet];
//    if (std::isnan(csv)) {
//        csv = -10.0;
//    }
//    return Jet(
//        p4,
//        csv,
//        data.jets_btagCMVA[njet],
//        data.jets_hadronFlavour[njet]
//    );
//}
//
//
//const Jet JetFactory::makeJESDown(const TreeData& data, int njet) {
//    assert(njet <= data.njets);
//    TLorentzVector p4;
//    p4.SetPtEtaPhiM(
//        data.jets_pt[njet],
//        data.jets_eta[njet],
//        data.jets_phi[njet],
//        data.jets_mass[njet]
//    );
//    //Undo nominal correction, re-do JESDown correction
//    const double corr = data.jets_corr_JESDown[njet] / data.jets_corr[njet];
//    p4 *= (1.0 / corr);
//    
//    double csv = data.jets_btagCSV[njet];
//    if (std::isnan(csv)) {
//        csv = -10.0;
//    }
//    return Jet(
//        p4,
//        csv,
//        data.jets_btagCMVA[njet],
//        data.jets_hadronFlavour[njet]
//    );
//}


//const Jet JetFactory::makeJERUp(const TreeData& data, int njet) {
//    assert(njet <= data.njets);
//    TLorentzVector p4;
//    p4.SetPtEtaPhiM(
//        data.jets_pt[njet],
//        data.jets_eta[njet],
//        data.jets_phi[njet],
//        data.jets_mass[njet]
//    );
//    //Undo nominal correction, re-do JERUp correction
//    const double corr = data.jets_corr_JERUp[njet] / data.jets_corr_JER[njet];
//    p4 *= (1.0 / corr);
//    double csv = data.jets_btagCSV[njet];
//    if (std::isnan(csv)) {
//        csv = -10.0;
//    }
//    return Jet(
//        p4,
//        csv,
//        data.jets_btagCSV[njet],
//        data.jets_hadronFlavour[njet]
//    );
//}
//
//
//const Jet JetFactory::makeJERDown(const TreeData& data, int njet) {
//    assert(njet <= data.njets);
//    TLorentzVector p4;
//    p4.SetPtEtaPhiM(
//        data.jets_pt[njet],
//        data.jets_eta[njet],
//        data.jets_phi[njet],
//        data.jets_mass[njet]
//    );
//    //Undo nominal correction, re-do JERDown correction
//    const double corr = data.jets_corr_JERDown[njet] / data.jets_corr_JER[njet];
//    p4 *= (1.0 / corr);
//    
//    double csv = data.jets_btagCSV[njet];
//    if (std::isnan(csv)) {
//        csv = -10.0;
//    }
//    return Jet(
//        p4,
//        csv,
//        data.jets_btagCSV[njet],
//        data.jets_hadronFlavour[njet]
//    );
//}


const string Jet::to_string() const {
    stringstream ss;
    ss << "pt=" << this->p4.Pt()
        << " eta=" << this->p4.Eta()
        << " phi=" << this->p4.Phi()
        << " m=" << this->p4.M()
        << " btagCSV=" << this->btagCSV;
    return ss.str();
}

void CategoryProcessor::fillHistograms(
    const Event& event,
    ResultMap& results,
    tuple<
        ProcessKey::ProcessKey,
        vector<CategoryKey::CategoryKey>,
        SystematicKey::SystematicKey> key,
    double weight,
    const Configuration& conf
    ) const {
}

void CategoryProcessor::process(
    const Event& event,
    const Configuration& conf,
    ResultMap& results,
    const vector<CategoryKey::CategoryKey>& catKeys,
    SystematicKey::SystematicKey systKey
    ) const {

    //Check if event passes cuts
    bool passes = isCategoryEnabled(conf, catKeys);
    if (passes) {
        passes = passes && (*this)(event, conf.process, catKeys, systKey);
    } 

    if (passes) {

        vector<CategoryKey::CategoryKey> _catKeys(catKeys);
        for (auto& k : this->keys) {
            _catKeys.push_back(k);
        }

        WeightMap _weightFuncs;

        //in case it's not a nominal event (instead e.g. JESUp) we use only nominal weights
        if (systKey != SystematicKey::nominal || isData(conf.process)) {
            _weightFuncs = getNominalWeights();
        //if it's a nominal event, can also use variated weights
        } else {
            _weightFuncs = this->weightFuncs;
        }
        for (auto& kvWeight : _weightFuncs) {
            //cout << "   weight " << SystematicKey::to_string(kvWeight.first) << endl;
            const double weight = kvWeight.second(event, conf);
            SystematicKey::SystematicKey _systKey = systKey;
            if (systKey == SystematicKey::nominal) {
                _systKey = kvWeight.first;
            }
            this->fillHistograms(
                event, results,
                make_tuple(conf.process, _catKeys, _systKey),
                weight,
                conf
            );
        } // weightFuncs
        
        //Process subcategories
        for (auto& subcat : this->subCategories) {
            subcat->process(event, conf, results, _catKeys, systKey);
        }
    } // passes
}

void SparseCategoryProcessor::fillHistograms(
    const Event& event,
    ResultMap& results,
    tuple<
        ProcessKey::ProcessKey,
        vector<CategoryKey::CategoryKey>,
        SystematicKey::SystematicKey> key,
    double weight,
    const Configuration& conf
    ) const {

    //fill base histograms
    CategoryProcessor::fillHistograms(event, results, key, weight, conf);
    const auto proc = get<0>(key);
    const auto cats = get<1>(key);
    const auto syst = get<2>(key);
    THnSparseF* h = nullptr;

    //check that the category is defined
    const auto hkey = make_tuple(
        proc, //process
        cats, //categories (vector)
        syst, //systematic
        HistogramKey::sparse //histo name
    );
    
    //Make output histo if doesn't exist
    if (!results.count(hkey)) {
        h = makeHist();
        results[hkey] = static_cast<TObject*>(h);
    } else {
        h = static_cast<THnSparseF*>(results.at(hkey));
    }
    assert(h != nullptr);

    //Evaluate all axis functions of the sparse histo
    vector<double> vals;
    for (auto& ax : axes) {
        double x = ax.evalFunc(event, proc, cats, syst);
        if (x < ax.xMin) {
            x = ax.xMin;
        } else if (x >= ax.xMax) {
            x = ax.xMax - (ax.xMax-ax.xMin)/(double)ax.nBins;
        }
        vals.push_back(x);
    }

    h->Fill(&vals[0], weight);
    
}

string to_string(const ResultKey& k) {
    stringstream ss;
    ss << "ResultKey(";
    ss << ProcessKey::to_string(get<0>(k)) << ", ";
    for (auto& v : get<1>(k)) {
        ss << CategoryKey::to_string(v) << ", ";
    }
    ss << SystematicKey::to_string(get<2>(k)) << ", ";
    ss << HistogramKey::to_string(get<3>(k)) << ")";
    return ss.str();
}

string to_string(const ResultMap& res) {
    stringstream ss;
    ss << "ResultMap[" << endl;
    for (auto& kv : res) {
        ss << " " << to_string(kv.first) << endl;
    }
    ss << "]" << endl;
    return ss.str();
}

Configuration parseJsonConf(const string& infile) {
    cout << "Loading json configuration from " << infile << endl;

    std::ifstream t(infile);
    if (!t.good()) {
        cerr << "Could not open file " << infile << endl;
        exit(EXIT_FAILURE);
    }
    std::stringstream buffer;
    buffer << t.rdbuf();

    char *endptr = nullptr;
    string indata = buffer.str();
    char *pindata = new char[indata.length() + 1];
    strcpy(pindata, indata.c_str());

    JsonValue value;
    JsonAllocator jsonAllocator;

    int status = jsonParse(pindata, &endptr, &value, jsonAllocator);
    if (status != JSON_OK) {
        cerr << jsonStrError(status) << endptr - pindata << endl;
        exit(EXIT_FAILURE);
    }
    
    return Configuration::makeConfiguration(value);
}

namespace BaseCuts {
    bool sl(const Event& ev) {
        return ev.is_sl && ev.passPV && ev.numJets>=4 && ev.data->json==1.0 && (
            (abs(ev.leptons.at(0).pdgId) == 13 && trigger::sl_mu(*(ev.data))) ||
            (abs(ev.leptons.at(0).pdgId) == 11 && trigger::sl_el(*(ev.data)))
        );
    }
    
    bool sl_mu(const Event& ev) {
        return sl(ev) && abs(ev.leptons.at(0).pdgId) == 13 && trigger::sl_mu(*(ev.data));
    }
    
    bool sl_el(const Event& ev) {
        return sl(ev) && abs(ev.leptons.at(0).pdgId) == 11 && trigger::sl_el(*(ev.data));
    }

    bool dl(const Event& ev) {
        return (ev.is_dl && ev.passPV &&
            ev.leptons.at(0).pdgId * ev.leptons.at(1).pdgId < 0 && (ev.data->ll_mass[0] > 20) && (
                //Z peak veto
                abs(ev.leptons.at(0).pdgId) == abs(ev.leptons.at(1).pdgId) ? !(ev.data->ll_mass[0] > 76 && ev.data->ll_mass[0] < 106) : true
            ) && (
                abs(ev.leptons.at(0).pdgId) == abs(ev.leptons.at(1).pdgId) ? (ev.data->met_pt[0] > 40) : true
            ) && ev.data->json==1.0 && (
                (abs(ev.leptons.at(0).pdgId)==13 && abs(ev.leptons.at(1).pdgId)==13 && trigger::mumu(*(ev.data))) ||
                (abs(ev.leptons.at(0).pdgId)==11 && abs(ev.leptons.at(1).pdgId)==11 && trigger::ee(*(ev.data))) || (
                (
                    (abs(ev.leptons.at(0).pdgId)==13 && abs(ev.leptons.at(1).pdgId)==11) ||
                    (abs(ev.leptons.at(0).pdgId)==11 && abs(ev.leptons.at(1).pdgId)==13)
                ) && trigger::emu(*(ev.data))
                )
            )
        );
    }
    
    bool dl_mumu(const Event& ev) {
        return dl(ev) && abs(ev.leptons.at(0).pdgId)==13 && abs(ev.leptons.at(1).pdgId)==13 && trigger::mumu(*(ev.data));
    }

    bool dl_ee(const Event& ev) {
        return dl(ev) && abs(ev.leptons.at(0).pdgId)==11 && abs(ev.leptons.at(1).pdgId)==11 && trigger::ee(*(ev.data));
    }
    bool dl_emu(const Event& ev) {
        return dl(ev) && (
            (abs(ev.leptons.at(0).pdgId)==13 && abs(ev.leptons.at(1).pdgId)==11) ||
            (abs(ev.leptons.at(0).pdgId)==11 && abs(ev.leptons.at(1).pdgId)==13)
        ) && trigger::emu(*(ev.data));
    }
}

bool isCategoryEnabled(const Configuration& conf, const vector<CategoryKey::CategoryKey>& catKeys) {
    if (conf.enabledCategories.size() == 0) {
        return true;
    }
    for (auto& ec : conf.enabledCategories) {
        if (ec == catKeys) {
            return true;
        }
    }
    return false;
}
