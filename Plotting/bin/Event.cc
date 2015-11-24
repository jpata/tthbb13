#include "TTH/Plotting/interface/Event.h"
#include "TTH/Plotting/interface/metree.h"

using namespace std;

bool pass_trig_dl(const TreeData& data) {
    return (
        data.HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v ||
        data.HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v ||
        data.HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v ||
        data.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v ||
        data.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v
    );
}

bool pass_trig_sl(const TreeData& data) {
    return (
        data.HLT_BIT_HLT_Ele27_WP85_Gsf_v ||
        data.HLT_BIT_HLT_IsoMu17_eta2p1_v
    );
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

const map<string, function<float(const Event& ev)>> AxisFunctions = {
    {"mem_SL_0w2h2t", [](const Event& ev) { return ev.mem_SL_0w2h2t;}},
    {"mem_SL_2w2h2t", [](const Event& ev) { return ev.mem_SL_2w2h2t;}},
    {"mem_SL_2w2h2t_sj", [](const Event& ev) { return ev.mem_SL_2w2h2t_sj;}},
    {"tth_mva", [](const Event& ev) { return ev.tth_mva;}},
    {"numJets", [](const Event& ev) { return ev.numJets;}},
    {"nBCSVM", [](const Event& ev) { return ev.nBCSVM;}},
    {"btag_LR_4b_2b_logit", [](const Event& ev) { return ev.btag_LR_4b_2b_logit;}},
    {"nBoosted", [](const Event& ev) { return ev.n_excluded_bjets<2 && ev.ntopCandidate==1;}},
    {"topCandidate_mass", [](const Event& ev) { return ev.topCandidate_mass;}},
    {"topCandidate_fRec", [](const Event& ev) { return ev.topCandidate_fRec;}},
    {"topCandidate_n_subjettiness", [](const Event& ev) { return ev.topCandidate_n_subjettiness;}},
    {"Wmass", [](const Event& ev) { return ev.Wmass;}},
    {"n_excluded_bjets", [](const Event& ev) { return ev.n_excluded_bjets;}},
    {"n_excluded_ljets", [](const Event& ev) { return ev.n_excluded_ljets;}}
};

const Configuration Configuration::makeConfiguration(JsonValue& value) {
    vector<string> filenames;
    double lumi = -1.0;
    ProcessKey::ProcessKey process = ProcessKey::UNKNOWN;
    string prefix;
    string outputFile = "UNDEFINED";
    long firstEntry = -1;
    long numEntries = -1;
    long printEvery = -1;

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
        else if (ks == "process") {
            process = ProcessKey::from_string(lev1->value.toString());
        }
        else if (ks == "prefix") {
            prefix = lev1->value.toString();
            cout << "json deserialized prefix " << prefix << endl;
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

                function<float(const Event& _ev)> _func;
                int nBins = -1;
                float xMin = 0.0;
                float xMax = 0.0;
                string name;
                //loop over keys in one sparse axis
                for (auto lev3 : lev2->value) {
                    const string spk = string(lev3->key);
                    if (spk == "func") {
                        name = lev3->value.toString();
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
        filenames, lumi,
        process,
        prefix,
        firstEntry, numEntries, printEvery,
        outputFile,
        sparseAxes
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
        const auto systKey = get<1>(rk);
        const auto histKey = get<2>(rk);
        stringstream ss;
        ss << prefix << "/";

        //Add all categories together with underscores
        int ind = 0;
        for (auto& catKey : get<0>(rk)) {
            ss << CategoryKey::to_string(catKey);
            if (ind < get<0>(rk).size() - 1) {
                ss << "_";
            }
            ind++;
        }
        //make root dir if doesn't exist
        const string dirname = ss.str();
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
    bool _pass_trig_sl,
    bool _pass_trig_dl,
    bool _passPV,
    int _numJets,
    int _nBCSVM,
    const vector<Jet>& _jets,
    const vector<Lepton>& _leptons,
    const Event::WeightMap& _weightFuncs,
    double _weight_xs,
    double _puWeight,
    double _Wmass,
    double _mem_SL_0w2h2t,
    double _mem_SL_2w2h2t,
    double _mem_SL_2w2h2t_sj,
    double _mem_DL_0w2h2t,
    double _tth_mva,
    double _bTagWeight,
    double _bTagWeight_Stats1Up,
    double _bTagWeight_Stats1Down,
    double _bTagWeight_Stats2Up,
    double _bTagWeight_Stats2Down,
    double _bTagWeight_LFUp,
    double _bTagWeight_LFDown,
    double _bTagWeight_HFUp,
    double _bTagWeight_HFDown,
    double _btag_LR_4b_2b,
    int _n_excluded_bjets,
    int _n_excluded_ljets,
    int _ntopCandidate,
    double _topCandidate_pt,
    double _topCandidate_eta,
    double _topCandidate_mass,
    double _topCandidate_masscal,
    double _topCandidate_fRec,
    double _topCandidate_n_subjettiness,
    int _nhiggsCandidate,
    double _higgsCandidate_pt,
    double _higgsCandidate_eta,
    double _higgsCandidate_mass,
    double _higgsCandidate_bbtag,
    double _higgsCandidate_n_subjettiness,
    double _higgsCandidate_dr_genHiggs
    ) :
    data(_data),
    is_sl(_is_sl),
    is_dl(_is_dl),
    pass_trig_sl(_pass_trig_sl),
    pass_trig_dl(_pass_trig_dl),
    passPV(_passPV),
    numJets(_numJets),
    nBCSVM(_nBCSVM),
    jets(_jets),
    leptons(_leptons),
    weightFuncs(_weightFuncs),
    weight_xs(_weight_xs),
    puWeight(_puWeight),
    Wmass(_Wmass),
    mem_SL_0w2h2t(_mem_SL_0w2h2t),
    mem_SL_2w2h2t(_mem_SL_2w2h2t),
    mem_SL_2w2h2t_sj(_mem_SL_2w2h2t_sj),
    mem_DL_0w2h2t(_mem_DL_0w2h2t),
    tth_mva(_tth_mva),
    bTagWeight(_bTagWeight),
    bTagWeight_Stats1Up(_bTagWeight_Stats1Up),
    bTagWeight_Stats1Down(_bTagWeight_Stats1Down),
    bTagWeight_Stats2Up(_bTagWeight_Stats2Up),
    bTagWeight_Stats2Down(_bTagWeight_Stats2Down),
    bTagWeight_LFUp(_bTagWeight_LFUp),
    bTagWeight_LFDown(_bTagWeight_LFDown),
    bTagWeight_HFUp(_bTagWeight_HFUp),
    bTagWeight_HFDown(_bTagWeight_HFDown),
    btag_LR_4b_2b(_btag_LR_4b_2b),
    btag_LR_4b_2b_logit(log(_btag_LR_4b_2b / (1.0 - _btag_LR_4b_2b))),
    n_excluded_bjets(_n_excluded_bjets),
    n_excluded_ljets(_n_excluded_ljets),

    ntopCandidate(_ntopCandidate),
    topCandidate_pt(_topCandidate_pt),
    topCandidate_eta(_topCandidate_eta),
    topCandidate_mass(_topCandidate_mass),
    topCandidate_masscal(_topCandidate_masscal),
    topCandidate_fRec(_topCandidate_fRec),
    topCandidate_n_subjettiness(_topCandidate_n_subjettiness),
    nhiggsCandidate(_nhiggsCandidate),
    higgsCandidate_pt(_higgsCandidate_pt),
    higgsCandidate_eta(_higgsCandidate_eta),
    higgsCandidate_mass(_higgsCandidate_mass),
    higgsCandidate_bbtag(_higgsCandidate_bbtag),
    higgsCandidate_n_subjettiness(_higgsCandidate_n_subjettiness),
    higgsCandidate_dr_genHiggs(_higgsCandidate_dr_genHiggs)
{
    
}


const string Event::to_string() const {
    stringstream ss;
    ss << "Event(" << this->numJets << "J, " << this->nBCSVM << "T";
    ss << endl;
    for (auto& jet : this->jets) {
        ss << " j " << jet.to_string() << endl;
    }
    ss << " bw=" << this->bTagWeight << endl;
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
        proc == ProcessKey::SingleElectron
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

double nominal_weight(const Event& ev, const Configuration& conf) {
    if (isMC(conf.process)) {
        return conf.lumi * ev.weight_xs * ev.puWeight;
    }
    return 1.0;
}

//Vector of nominal weight functions
static const Event::WeightMap nominalWeights = {
    {SystematicKey::nominal, nominal_weight}
};

//Systematically variated weights, applied only in case of nominal event
static const Event::WeightMap systWeights = {
    {SystematicKey::nominal, nominal_weight},
//    {
//        SystematicKey::CMS_ttH_CSVStats1Up,
//        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_Stats1Up;}
//    },
//    {
//        SystematicKey::CMS_ttH_CSVStats1Down,
//        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_Stats1Down;}
//    },
//    {
//        SystematicKey::CMS_ttH_CSVStats2Up,
//        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_Stats2Up;}
//    },
//    {
//        SystematicKey::CMS_ttH_CSVStats2Down,
//        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_Stats2Down;}
//    },
//    {
//        SystematicKey::CMS_ttH_CSVLFUp,
//        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_LFUp;}
//    },
//    {
//        SystematicKey::CMS_ttH_CSVLFDown,
//        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_LFDown;}
//    },
//    {
//        SystematicKey::CMS_ttH_CSVHFUp,
//        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_HFUp;}
//    },
//    {
//        SystematicKey::CMS_ttH_CSVHFDown,
//        [](const Event& ev){ return nominal_weight(ev)/ev.bTagWeight * ev.bTagWeight_HFDown;}
//    },
};

double process_weight(ProcessKey::ProcessKey proc) {
  return 1.0;

//    switch(proc) {
//        case ProcessKey::ttbarPlusBBbar:
//        case ProcessKey::ttbarPlusB:
//        case ProcessKey::ttbarPlus2B:
//        case ProcessKey::ttbarPlusCCbar:
//        case ProcessKey::ttbarOther:
//            return 0.5;
//        default:
//            return 1.0;
//    }
}

const Event EventFactory::makeNominal(const TreeData& data, const Configuration& conf) {
    
    const vector<Jet> jets = makeAllJets(data, &(JetFactory::makeNominal));
    const vector<Lepton> leptons = makeAllLeptons(data);

    const Event ev(
        &data,
        data.is_sl,
        data.is_dl,
        pass_trig_sl(data),
        pass_trig_dl(data),
        data.passPV,
        data.numJets,
        data.nBCSVM,
        jets,
        leptons,
        systWeights,
        data.weight_xs,
        data.puWeight,
        data.Wmass,
        mem_p(data.mem_tth_p[0], data.mem_ttbb_p[0]), //SL 022
        mem_p(data.mem_tth_p[5], data.mem_ttbb_p[5]), //SL 222
        mem_p(data.mem_tth_p[9], data.mem_ttbb_p[9], 0.05), //SL 222 sj
        mem_p(data.mem_tth_p[1], data.mem_ttbb_p[1]), //DL 022,
        data.tth_mva,
        data.bTagWeight,
        data.bTagWeight_Stats1Up,
        data.bTagWeight_Stats1Down,
        data.bTagWeight_Stats2Up,
        data.bTagWeight_Stats2Down,
        data.bTagWeight_LFUp,
        data.bTagWeight_LFDown,
        data.bTagWeight_HFUp,
        data.bTagWeight_HFDown,
        data.btag_LR_4b_2b,
        data.n_excluded_bjets,
        data.n_excluded_ljets,
        
        data.ntopCandidate,
        data.topCandidate_pt[0],
        data.topCandidate_eta[0],
        data.topCandidate_mass[0],
        data.topCandidate_masscal[0],
        data.topCandidate_fRec[0],
        data.topCandidate_n_subjettiness[0],
        
        data.nhiggsCandidate,
        data.higgsCandidate_pt[0],
        data.higgsCandidate_eta[0],
        data.higgsCandidate_mass[0],
        data.higgsCandidate_bbtag[0],
        data.higgsCandidate_n_subjettiness[0],
        data.higgsCandidate_dr_genHiggs[0]
    );
    return ev;
}

const Event EventFactory::makeJESUp(const TreeData& data, const Configuration& conf) {
    const vector<Jet> jets = makeAllJets(data, &(JetFactory::makeJESUp));
    const vector<Lepton> leptons = makeAllLeptons(data);

    return Event(
        &data,
        data.is_sl,
        data.is_dl,
        pass_trig_sl(data),
        pass_trig_dl(data),
        data.passPV,
        data.numJets_JESUp,
        data.nBCSVM_JESUp,
        jets,
        leptons,
        nominalWeights,
        data.weight_xs,
        data.puWeight,
        data.Wmass,
        mem_p(data.mem_tth_JESUp_p[0], data.mem_ttbb_JESUp_p[0]), //SL 022
        mem_p(data.mem_tth_JESUp_p[5], data.mem_ttbb_JESUp_p[5]), //SL 222
        mem_p(data.mem_tth_JESUp_p[9], data.mem_ttbb_JESUp_p[9], 0.05), //SL 222 sj
        mem_p(data.mem_tth_JESUp_p[1], data.mem_ttbb_JESUp_p[1]), //DL 022,
        data.tth_mva, 
        data.bTagWeight,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        data.btag_LR_4b_2b,
        data.n_excluded_bjets,
        data.n_excluded_ljets,
        
        data.ntopCandidate,
        data.topCandidate_pt[0],
        data.topCandidate_eta[0],
        data.topCandidate_mass[0],
        data.topCandidate_masscal[0],
        data.topCandidate_fRec[0],
        data.topCandidate_n_subjettiness[0],

        data.nhiggsCandidate,
        data.higgsCandidate_pt[0],
        data.higgsCandidate_eta[0],
        data.higgsCandidate_mass[0],
        data.higgsCandidate_bbtag[0],
        data.higgsCandidate_n_subjettiness[0],
        data.higgsCandidate_dr_genHiggs[0]
    );
}

const Event EventFactory::makeJESDown(const TreeData& data, const Configuration& conf) {
    const vector<Jet> jets = makeAllJets(data, &(JetFactory::makeJESDown));
    const vector<Lepton> leptons = makeAllLeptons(data);

    return Event(
        &data,
        data.is_sl,
        data.is_dl,
        pass_trig_sl(data),
        pass_trig_dl(data),
        data.passPV,
        data.numJets_JESDown,
        data.nBCSVM_JESDown,
        jets,
        leptons,
        nominalWeights,
        data.weight_xs,
        data.puWeight,
        data.Wmass,
        mem_p(data.mem_tth_JESDown_p[0], data.mem_ttbb_JESDown_p[0]), //SL 022
        mem_p(data.mem_tth_JESDown_p[5], data.mem_ttbb_JESDown_p[5]), //SL 222
        mem_p(data.mem_tth_JESDown_p[9], data.mem_ttbb_JESDown_p[9], 0.05), //SL 222 sj
        mem_p(data.mem_tth_JESDown_p[1], data.mem_ttbb_JESDown_p[1]), //DL 022,
        data.tth_mva,
        data.bTagWeight,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        data.btag_LR_4b_2b,
        data.n_excluded_bjets,
        data.n_excluded_ljets,
        
        data.ntopCandidate,
        data.topCandidate_pt[0],
        data.topCandidate_eta[0],
        data.topCandidate_mass[0],
        data.topCandidate_masscal[0],
        data.topCandidate_fRec[0],
        data.topCandidate_n_subjettiness[0],

        data.nhiggsCandidate,
        data.higgsCandidate_pt[0],
        data.higgsCandidate_eta[0],
        data.higgsCandidate_mass[0],
        data.higgsCandidate_bbtag[0],
        data.higgsCandidate_n_subjettiness[0],
        data.higgsCandidate_dr_genHiggs[0]
    );
}


Jet::Jet(const TLorentzVector& _p4, float _btagCSV, float _btagBDT) :
    p4(_p4),
    btagCSV(_btagCSV),
    btagBDT(_btagBDT)
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
    return Jet(
        p4,
        data.jets_btagCSV[njet],
        data.jets_btagBDT[njet]
    );
}

const Jet JetFactory::makeJESUp(const TreeData& data, int njet) {
    assert(njet <= data.njets);
    TLorentzVector p4;
    p4.SetPtEtaPhiM(
        data.jets_pt[njet],
        data.jets_eta[njet],
        data.jets_phi[njet],
        data.jets_mass[njet]
    );
    //Undo nominal correction, re-do JESUp correction
    const double corr = data.jets_corr_JESUp[njet] / data.jets_corr[njet];
    p4 *= (1.0 / corr);
    return Jet(
        p4,
        data.jets_btagCSV[njet],
        data.jets_btagBDT[njet]
    );
}


const Jet JetFactory::makeJESDown(const TreeData& data, int njet) {
    assert(njet <= data.njets);
    TLorentzVector p4;
    p4.SetPtEtaPhiM(
        data.jets_pt[njet],
        data.jets_eta[njet],
        data.jets_phi[njet],
        data.jets_mass[njet]
    );
    //Undo nominal correction, re-do JESDown correction
    const double corr = data.jets_corr_JESDown[njet] / data.jets_corr[njet];
    p4 *= (1.0 / corr);
    return Jet(
        p4,
        data.jets_btagCSV[njet],
        data.jets_btagBDT[njet]
    );
}


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
    const tuple<
        vector<CategoryKey::CategoryKey>,
        SystematicKey::SystematicKey
    > key,
    double weight
    ) const {
}

void CategoryProcessor::process(
    const Event& event,
    const Configuration& conf,
    ResultMap& results,
    const vector<CategoryKey::CategoryKey>& catKeys,
    SystematicKey::SystematicKey systKey
    ) const {
    const bool passes = (*this)(event);
    if (passes) {

        vector<CategoryKey::CategoryKey> _catKeys(catKeys);
        for (auto& k : this->keys) {
            _catKeys.push_back(k);
        }

        for (auto& kvWeight : event.weightFuncs) {
            //cout << "   weight " << SystematicKey::to_string(kvWeight.first) << endl;
            const double weight = kvWeight.second(event, conf);
            SystematicKey::SystematicKey _systKey = systKey;
            if (systKey == SystematicKey::nominal) {
                _systKey = kvWeight.first;
            }
            this->fillHistograms(
                event, results,
                make_tuple(_catKeys, _systKey),
                weight
            );
        } // weightFuncs
        
        //Process subcategories
        for (auto& subcat : this->subCategories) {
            subcat->process(event, conf, results, _catKeys, systKey);
        }
    } // passes
}

void MEMCategoryProcessor::fillHistograms(
    const Event& event,
    ResultMap& results,
    const tuple<
        vector<CategoryKey::CategoryKey>,
        SystematicKey::SystematicKey
    > key,
    double weight
    ) const {

    //fill base histograms
    CategoryProcessor::fillHistograms(event, results, key, weight);

    if (CategoryKey::is_sl(get<0>(key))) {
        const auto mem_SL_0w2h2t_key = make_tuple(
            get<0>(key),
            get<1>(key),
            HistogramKey::mem_SL_0w2h2t
        );
        
        const auto mem_SL_2w2h2t_sj_key = make_tuple(
            get<0>(key),
            get<1>(key),
            HistogramKey::mem_SL_2w2h2t_sj
        );
        
        const auto mem_SL_2w2h2t_key = make_tuple(
            get<0>(key),
            get<1>(key),
            HistogramKey::mem_SL_2w2h2t
        );


        if (!results.count(mem_SL_0w2h2t_key)) {
            results[mem_SL_0w2h2t_key] = new TH1D("mem_SL_0w2h2t", "mem SL 0w2h2t", 6, 0, 1);
        }
        if (!results.count(mem_SL_2w2h2t_sj_key)) {
            results[mem_SL_2w2h2t_sj_key] = new TH1D("mem_SL_2w2h2t_sj", "mem SL 0w2h2t subjet", 6, 0, 1);
        }
        if (!results.count(mem_SL_2w2h2t_key)) {
            results[mem_SL_2w2h2t_key] = new TH1D("mem_SL_2w2h2t", "mem SL 2w2h2t", 6, 0, 1);
        }
        static_cast<TH1D*>(results[mem_SL_0w2h2t_key])->Fill(event.mem_SL_0w2h2t, weight);
        static_cast<TH1D*>(results[mem_SL_2w2h2t_key])->Fill(event.mem_SL_2w2h2t, weight);
        static_cast<TH1D*>(results[mem_SL_2w2h2t_sj_key])->Fill(event.mem_SL_2w2h2t_sj, weight);
    } else if (CategoryKey::is_dl(get<0>(key))) {
        const auto mem_DL_0w2h2t_key = make_tuple(
            get<0>(key),
            get<1>(key),
            HistogramKey::mem_DL_0w2h2t
        );

        if (!results.count(mem_DL_0w2h2t_key)) {
            results[mem_DL_0w2h2t_key] = new TH1D("mem_DL_0w2h2t", "mem DL 0w2h2t", 6, 0, 1);
        }
        static_cast<TH1D*>(results[mem_DL_0w2h2t_key])->Fill(event.mem_DL_0w2h2t, weight);
    }
}

void SparseCategoryProcessor::fillHistograms(
    const Event& event,
    ResultMap& results,
    const tuple<
        vector<CategoryKey::CategoryKey>,
        SystematicKey::SystematicKey
    > key,
    double weight
    ) const {

    //fill base histograms
    CategoryProcessor::fillHistograms(event, results, key, weight);

    THnSparseF* h = nullptr;
    if (CategoryKey::is_sl(get<0>(key))) {
        const auto hkey = make_tuple(
            get<0>(key),
            get<1>(key),
            HistogramKey::sparse
        );
        
        if (!results.count(hkey)) {
            h = makeHist();
            results[hkey] = static_cast<TObject*>(h);
        } else {
            h = static_cast<THnSparseF*>(results.at(hkey));
        }
    } else if (CategoryKey::is_dl(get<0>(key))) {
        const auto hkey = make_tuple(
            get<0>(key),
            get<1>(key),
            HistogramKey::sparse
        );
        if (!results.count(hkey)) {
            h = makeHist();
            results[hkey] = static_cast<TObject*>(h);
        } else {
            h = static_cast<THnSparseF*>(results.at(hkey));
        }
    }
    if (h != nullptr) {
        vector<double> vals;
        for (auto& ax : axes) {
            double x = ax.evalFunc(event);
            if (x < ax.xMin) {
                x = ax.xMin;
            } else if (x >= ax.xMax) {
                x = ax.xMax - (ax.xMax-ax.xMin)/(double)ax.nBins;
            }
            vals.push_back(x);
        }

        h->Fill(&vals[0], weight);
    }
}

string to_string(const ResultKey& k) {
    stringstream ss;
    ss << "ResultKey(";
    for (auto& v : get<0>(k)) {
        ss << CategoryKey::to_string(v) << ", ";
    }
    ss << SystematicKey::to_string(get<1>(k)) << ", ";
    ss << HistogramKey::to_string(get<2>(k)) << ")";
    return ss.str();
}

string to_string(const ResultMap& res) {
    stringstream ss;
    ss << "ResultMap[" << endl;
    // for (auto& kv : res) {
    //     ss << " " << to_string(kv.first)
    //         << " " << kv.second.GetName()
    //         << " N=" << kv.second.GetEntries()
    //         << " I=" << kv.second.Integral()
    //         << " mu=" << kv.second.GetMean() << endl;
    // }
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
        return ev.is_sl && ev.passPV && ev.pass_trig_sl && ev.numJets>=4;
    }
    
    bool sl_mu(const Event& ev) {
        return sl(ev) && abs(ev.leptons.at(0).pdgId) == 13;
    }
    
    bool sl_el(const Event& ev) {
        return sl(ev) && abs(ev.leptons.at(0).pdgId) == 11;
    }

    bool dl(const Event& ev) {
        return (ev.is_dl && ev.passPV && ev.pass_trig_dl && true);
        //    ev.leptons.at(0).pdgId * ev.leptons.at(1).pdgId < 0 && (ev.data->ll_mass[0] > 20) && (
        //        //Z peak veto
        //        abs(ev.leptons.at(0).pdgId) == abs(ev.leptons.at(1).pdgId) ? !(ev.data->ll_mass[0] > 76 && ev.data->ll_mass[0] < 106) : true
        //    ) && (
        //        abs(ev.leptons.at(0).pdgId) == abs(ev.leptons.at(1).pdgId) ? (ev.data->met_pt[0] > 40) : true
        //    )
        //);
    }
    
    bool dl_mumu(const Event& ev) {
        return dl(ev) && abs(ev.leptons.at(0).pdgId)==13 && abs(ev.leptons.at(1).pdgId)==13;
    }

    bool dl_ee(const Event& ev) {
        return dl(ev) && abs(ev.leptons.at(0).pdgId)==11 && abs(ev.leptons.at(1).pdgId)==11;
    }
    bool dl_emu(const Event& ev) {
        return dl(ev) && (
            (abs(ev.leptons.at(0).pdgId)==13 && abs(ev.leptons.at(1).pdgId)==11) ||
            (abs(ev.leptons.at(0).pdgId)==11 && abs(ev.leptons.at(1).pdgId)==13)
        );
    }
}
