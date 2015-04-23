#include "TTH/Looper/interface/Analyzer.hh"
#include "TTH/Looper/interface/Sequence.hh"
#include "TTH/Looper/interface/Event.hh"
#include "TTH/Looper/interface/Input.hh"
#include "TTH/Looper/interface/AutoTree.hh"

#include <vector>

GenericAnalyzer::GenericAnalyzer(
    TFileDirectory *_fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    sequence(_sequence),
    name(pset.getParameter<std::string>("name"))
{
    //Create a new local directory
    _fd = _fs->mkdir(name.c_str());
    fs = &_fd;
    
    LOG(DEBUG) << "GenericAnalyzer: created analyzer with name " << name;
};

bool GenericAnalyzer::process(EventContainer &event)
{
    LOG(DEBUG) << "processing " << sequence->fullName << " " << name << " " << event.i;
    processed++;
    return true;
};

//Need to define it here to specialize templates
//Generates an object of type T with args using
//TFileService::make<T>(args...)
//The name of the object is configured to reflect the sequence and analyzer names
template <typename T, class ...Ts>
T *GenericAnalyzer::fsmake(Ts... args)
{
    T *t = fs->make<T>(args...);
    
    //Embed full path to title
    t->SetTitle(
        (std::string(t->GetTitle()) + (
            "(" +
            sequence->fullName +
            "_" +
            this->name +
            "_" +
            string(t->GetName()) + ")"
        )).c_str()
    );
    
    // prepend the analyzer name to the histogram to make it unique
    // t->SetName(
    //     (
    //         this->name + "_" +
    //         string(t->GetName())
    //     ).c_str()
    // );
    
    //Explicitly set name to be unique in case of flat storage
    // t->SetName(
    //     (sequence->fullName + "__" +
    //     this->name + "__" +
    //     string(t->GetName())
    //     ).c_str()
    // );
    return t;
}

EventPrinterAnalyzer::EventPrinterAnalyzer(
    TFileDirectory *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    GenericAnalyzer(fs, _sequence, pset),
    printAll(pset.getParameter<bool>("printAll")),
    processEvery(pset.getParameter<int>("processEvery"))
{
    LOG(DEBUG) << "EventPrinterAnalyzer: created EventPrinterAnalyzer";
};

bool EventPrinterAnalyzer::process(EventContainer &event)
{
    LOG(DEBUG) << "processing " << name << " " << event.i;

    if (processed % processEvery == 0)
    {
        std::cout << name << ":" << processed << ":" << event.i << std::endl;

        if (printAll)
        {
            for (auto const &k : event.data)
            {
                std::cout << k.first << " " << &(k.second) << std::endl;
            }
        }
    }
    GenericAnalyzer::process(event);
    return true;
};

TFormulaEvaluator::TFormulaEvaluator(
    TFileDirectory *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    GenericAnalyzer(fs, _sequence, pset),
    form(name.c_str(), pset.getParameter<std::string>("formula").c_str()),
    xName(pset.getParameter<std::string>("xName")),
    yName(pset.getParameter<std::string>("yName")),
    zName(pset.getParameter<std::string>("zName"))
{
    LOG(DEBUG) << "TFormulaEvaluator: created TFormulaEvaluator " << pset.getParameter<std::string>("formula");
};

bool TFormulaEvaluator::process(EventContainer &event)
{
    LOG(DEBUG) << "processing " << name << " " << event.i;

    const double x = xName.size() > 0 ? event.getData<double>(xName) : NAN;
    const double y = yName.size() > 0 ? event.getData<double>(yName) : NAN;
    const double z = zName.size() > 0 ? event.getData<double>(zName) : NAN;

    double prod = NAN;
    if (!std::isnan(x) && !std::isnan(y) && !std::isnan(z))
    {
        prod = form.Eval(x, y, z);
    }
    else if (!std::isnan(x) && !std::isnan(y) && std::isnan(z))
    {
        prod = form.Eval(x, y);
    }
    else if (!std::isnan(x) && std::isnan(y) && std::isnan(z))
    {
        prod = form.Eval(x);
    }
    addData(event, "f", prod);
    GenericAnalyzer::process(event);
    return true;
};

//Creates jet-related histograms
JetHistogramAnalyzer::JetHistogramAnalyzer(
    TFileDirectory *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    GenericAnalyzer(fs, _sequence, pset),
    h_pt0(fsmake<TH1D>("jet0_pt", "Leading jet pt", 30, 0.0, 500.0)),
    h_pt1(fsmake<TH1D>("jet1_pt", "Sub-leading jet pt", 30, 0.0, 500.0)),
    h_eta0(fsmake<TH1D>("jet0_eta", "Leading jet eta", 30, -5.0, 5.0)),
    h_eta1(fsmake<TH1D>("jet1_eta", "Sub-leading jet eta", 30, -5.0, 5.0)),
    
    h_abseta0(fsmake<TH1D>("jet0_abseta", "Leading jet abs eta", 30, 0.0, 5.0)),
    h_abseta1(fsmake<TH1D>("jet1_abseta", "Sub-leading jet abs eta", 30, 0.0, 5.0)),
    
    
    h_csv0b(fsmake<TH1D>("jet0_csvb", "Leading jet csv b", 30, 0, 1.0)),
    h_csv0c(fsmake<TH1D>("jet0_csvc", "Leading jet csv c", 30, 0, 1.0)),
    h_csv0l(fsmake<TH1D>("jet0_csvl", "Leading jet csv uds", 30, 0, 1.0)),
    h_csv0g(fsmake<TH1D>("jet0_csvg", "Leading jet csv g", 30, 0, 1.0)),
    h_csv0lg(fsmake<TH1D>("jet0_csvlg", "Leading jet csv udsg", 30, 0, 1.0)),
    
    h_csv1b(fsmake<TH1D>("jet1_csvb", "Sub-leading jet csv b", 30, 0, 1.0)),
    h_csv1c(fsmake<TH1D>("jet1_csvc", "Sub-leading jet csv c", 30, 0, 1.0)),
    h_csv1l(fsmake<TH1D>("jet1_csvl", "Sub-leading jet csv uds", 30, 0, 1.0)),
    h_csv1g(fsmake<TH1D>("jet1_csvg", "Sub-leading jet csv g", 30, 0, 1.0)),
    h_csv1lg(fsmake<TH1D>("jet1_csvlg", "Sub-leading jet csv udsg", 30, 0, 1.0))
{
    LOG(DEBUG) << "JetHistogramAnalyzer: created JetHistogramAnalyzer ";
};

//Fills jet-related histograms
bool JetHistogramAnalyzer::process(EventContainer &event)
{
    LOG(DEBUG) << "processing " << name << " " << event.i;
    
    AutoTree* inp = event.getData<AutoTree*>("input");
    assert(inp != nullptr);
    
    std::vector<double> jets_pt = inp->getValue<std::vector<double>>("jets_pt");
    std::vector<int> jets_mcFlavour = inp->getValue<std::vector<int>>("jets_mcFlavour");
    std::vector<double> jets_eta = inp->getValue<std::vector<double>>("jets_eta");
    std::vector<double> jets_csv = inp->getValue<std::vector<double>>("jets_btagCSV");
    
    h_pt0->Fill(jets_pt[0]);
    h_pt1->Fill(jets_pt[1]);
    
    h_eta0->Fill(jets_eta[0]);
    h_eta1->Fill(jets_eta[1]);
    
    h_abseta0->Fill(std::abs(jets_eta[0]));
    h_abseta1->Fill(std::abs(jets_eta[1]));
    
    TH1D* h0 = h_csv0l;
    TH1D* h1 = h_csv1l;
    
    int id0 = std::abs(jets_mcFlavour[0]);
    int id1 = std::abs(jets_mcFlavour[1]);
    
    if (id0 == 5) {
        h0 = h_csv0b;
    } else if(id0 == 4) {
        h0 = h_csv0c;
    } else if(id0 == 21) {
        h0 = h_csv0g;
    }
    
    if (id1 == 5) {
        h1 = h_csv1b;
    } else if(id0 == 4) {
        h1 = h_csv1c;
    } else if(id0 == 21) {
        h1 = h_csv1g;
    }
    
    //Fill udsg
    if (id0 < 4 || id0 == 21) {
        h_csv0lg->Fill(jets_csv[1]);
    }
    if (id1 < 4 || id1 == 21) {
        h_csv1lg->Fill(jets_csv[1]);
    }
    
    h0->Fill(jets_csv[0]);
    h1->Fill(jets_csv[1]);
    
    GenericAnalyzer::process(event);
    return true;
};

//Creates b-tag related histograms
BTagHistogramAnalyzer::BTagHistogramAnalyzer(
    TFileDirectory *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    GenericAnalyzer(fs, _sequence, pset),
    h_nBCSVM(fsmake<TH1D>("nBCSVM", "Number of b-tagged jets (CSVM)",
        10, 0, 10)
    ),
    h_nBCSVT(fsmake<TH1D>("nBCSVT", "Number of b-tagged jets (CSVT)",
        10, 0, 10)
    ),
    h_btagLR(fsmake<TH1D>("btagLR", "B-tag LR", 30, 0, 1)),
    h_btagLR_nMatchSimB(fsmake<TH2D>(
        "btagLR_nMatchSimB",
        "B-tag LR vs. number of b-quarks at gen-level not associated to tops",
        30, 0, 1, 10, 0, 10)
    ),
    h_njets_nBCSVM(fsmake<TH2D>(
        "njets_nBCSVM",
        "Njets vs NCSVM",
        10, 0, 10, 10, 0, 10)
    )
{
    LOG(DEBUG) << "BTagHistogramAnalyzer: created BTagHistogramAnalyzer ";
};

//Fills b-tag related histograms
bool BTagHistogramAnalyzer::process(EventContainer &event)
{
    LOG(DEBUG) << "processing " << name << " " << event.i;
    
    AutoTree* inp = event.getData<AutoTree*>("input");
    assert(inp != nullptr);
    
    int njets = inp->getValue<int>("njets");
    int n_bcsvm = inp->getValue<int>("nBCSVM");
    int n_bcsvt = inp->getValue<int>("nBCSVT");
    h_nBCSVM->Fill(n_bcsvm);
    h_nBCSVT->Fill(n_bcsvt);
    h_njets_nBCSVM->Fill(njets, n_bcsvm);
    
    double btagLR = inp->getValue<double>("btag_LR_4b_2b");
    int nMatchSimB = inp->getValue<int>("nMatchSimB");
    h_btagLR->Fill(btagLR);
    h_btagLR_nMatchSimB->Fill(btagLR, nMatchSimB);
    
    GenericAnalyzer::process(event);
    return true;
};


MEAnalyzer::MEAnalyzer(
    TFileDirectory *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    GenericAnalyzer(fs, _sequence, pset),
    label(pset.getParameter<std::string>("label")),
    me_index(pset.getParameter<int>("MEindex")),
    h_me_discr(fsmake<TH1D>("me_discr", "ME discriminator", 6, 0, 1)),
    h_me_discr_btagLR(fsmake<TH2D>("me_discr_btaglr",
        "ME discriminator vs btag LR", 6, 0, 1, 6, 0, 1)
    ),
    h_me_discr2(fsmake<TH1D>("me_discr2", "ME discriminator", 1000, 0, 1)),
    h_me_discr_tth_ttbb(fsmake<TH2D>("me_discr_tth_ttbb",
        "ME discriminator tth vs ttbb log10", 60, -25, -50, 60, -25, -50)
    )
    
{
    LOG(DEBUG) << "MEAnalyzer: created MEAnalyzer";
};

bool MEAnalyzer::process(EventContainer &event)
{
    LOG(DEBUG) << "processing " << name << " " << event.i;
    
    AutoTree* inp = event.getData<AutoTree*>("input");
    assert(inp != nullptr);
    
    int nmem_ttbb = inp->getValue<int>("nmem_ttbb");
    int nmem_tth = inp->getValue<int>("nmem_tth");

    if (nmem_ttbb > 0 && nmem_tth > 0) {
        std::vector<double> mem_ttbb = inp->getValue<std::vector<double>>(
            "mem_ttbb_p"
        );
        std::vector<double> mem_tth = inp->getValue<std::vector<double>>(
            "mem_tth_p"
        );
        
        assert(me_index < mem_ttbb.size());
        assert(me_index < mem_tth.size());
        //std::cout << nmem_tth << " " << nmem_ttbb << std::endl;
        double p0 = mem_tth[me_index];
        double p1 = mem_ttbb[me_index];
        
        h_me_discr_tth_ttbb->Fill(std::log10(p0), std::log10(p1));
        
        double d = p0 / (p0 + 0.15*p1);
        h_me_discr->Fill(d);
        h_me_discr2->Fill(d);
        
        double btagLR = inp->getValue<double>("btag_LR_4b_2b");
        h_me_discr_btagLR->Fill(d, btagLR);
    }
    
    GenericAnalyzer::process(event);
    return true;
};



// MEMultiHypoAnalyzer::MEMultiHypoAnalyzer(
//     TFileDirectory *fs,
//     Sequence *_sequence,
//     const edm::ParameterSet &pset
// ) :
//     GenericAnalyzer(fs, _sequence, pset),
//     label(pset.getParameter<std::string>("label")),
//     me_inds(pset.getParameter<std::vector<int>>("MEindices")),
//     h_me_discr(fsmake<TH1D>("me_discr", "ME discriminator", 6, 0, 1)),
//     h_me_discr_btagLR(fsmake<TH2D>("me_discr_btaglr",
//         "ME discriminator vs btag LR", 6, 0, 1, 6, 0, 1)
//     ),
//     h_me_discr2(fsmake<TH1D>("me_discr2", "ME discriminator", 1000, 0, 1)),
//     h_me_discr_tth_ttbb(fsmake<TH2D>("me_discr_tth_ttbb",
//         "ME discriminator tth vs ttbb log10", 60, -25, -50, 60, -25, -50)
//     )
//     
// {
//     LOG(DEBUG) << "MEAnalyzer: created MEAnalyzer";
// };

MatchAnalyzer::MatchAnalyzer(
    TFileDirectory *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    GenericAnalyzer(fs, _sequence, pset),
    h_nmatch_wq(fsmake<TH1D>("nmatch_wq",
        "Number of jets matched to quarks from W", 6, 0, 6)
    ),
    h_nmatch_hb(fsmake<TH1D>("nmatch_hb",
        "Number of jets matched to b quarks from H", 6, 0, 6)
    ),
    h_nmatch_tb(fsmake<TH1D>("nmatch_tb",
        "Number of jets matched to b quarks from top", 6, 0, 6)
    ),
    h_nmatch_wq_btag(fsmake<TH1D>("nmatch_wq_btag",
        "Number of untagged jets matched to quarks from W", 6, 0, 6)
    ),
    h_nmatch_hb_btag(fsmake<TH1D>("nmatch_hb_btag",
        "Number of tagged jets matched to b quarks from H", 6, 0, 6)
    ),
    h_nmatch_tb_btag(fsmake<TH1D>("nmatch_tb_btag",
        "Number of tagged jets matched to b quarks from top", 6, 0, 6)
    ),
    h_wq_pt(fsmake<TH1D>("wq_pt",
        "Generated W associated light quark pt", 30, 0, 300)
    ),
    h_hb_pt(fsmake<TH1D>("hb_pt",
        "Generated H associated b-quark pt", 30, 0, 300)
    ),
    h_tb_pt(fsmake<TH1D>("tb_pt",
        "Generated top associated b-quark pt", 30, 0, 300)
    ),
    h_wq_eta(fsmake<TH1D>("wq_eta",
        "Generated W associated light quark eta", 30, -5.0, 5.0)
    ),
    h_hb_eta(fsmake<TH1D>("hb_eta",
        "Generated H associated b-quark eta", 30, -5.0, 5.0)
    ),
    h_tb_eta(fsmake<TH1D>("tb_eta",
        "Generated top associated b-quark eta", 30, -5.0, 5.0)
    )

{
    LOG(DEBUG) << "MEAnalyzer: created MEAnalyzer";
};

bool MatchAnalyzer::process(EventContainer &event)
{
    LOG(DEBUG) << "processing " << name << " " << event.i;
    
    AutoTree* inp = event.getData<AutoTree*>("input");
    assert(inp != nullptr);
    
    int n_match_wq = inp->getValue<int>("nMatch_wq");
    int n_match_wq_btag = inp->getValue<int>("nMatch_wq_btag");
    int n_match_hb = inp->getValue<int>("nMatch_hb");
    int n_match_hb_btag = inp->getValue<int>("nMatch_hb_btag");
    int n_match_tb = inp->getValue<int>("nMatch_tb");
    int n_match_tb_btag = inp->getValue<int>("nMatch_tb_btag");
    
    h_nmatch_wq->Fill(n_match_wq);
    h_nmatch_wq_btag->Fill(n_match_wq_btag);

    h_nmatch_tb->Fill(n_match_tb);
    h_nmatch_tb_btag->Fill(n_match_tb_btag);
    
    h_nmatch_hb->Fill(n_match_hb);
    h_nmatch_hb_btag->Fill(n_match_hb_btag);
    
    vector<double> wq_pt = inp->getValue<vector<double>>("GenQFromW_pt");
    vector<double> hb_pt = inp->getValue<vector<double>>("GenBFromHiggs_pt");
    vector<double> tb_pt = inp->getValue<vector<double>>("GenBFromTop_pt");
    vector<double> wq_eta = inp->getValue<vector<double>>("GenQFromW_eta");
    vector<double> hb_eta = inp->getValue<vector<double>>("GenBFromHiggs_eta");
    vector<double> tb_eta = inp->getValue<vector<double>>("GenBFromTop_eta");

    for (double v : wq_pt) {
        h_wq_pt->Fill(v);
    }
    for (double v : hb_pt) {
        h_hb_pt->Fill(v);
    }
    for (double v : tb_pt) {
        h_tb_pt->Fill(v);
    }

    for (double v : wq_eta) {
        h_wq_eta->Fill(v);
    }
    for (double v : hb_eta) {
        h_hb_eta->Fill(v);
    }
    for (double v : tb_eta) {
        h_tb_eta->Fill(v);
    }


    GenericAnalyzer::process(event);
    return true;
};


GenLevelAnalyzer::GenLevelAnalyzer(
    TFileDirectory *fs,
    Sequence *_sequence,
    const edm::ParameterSet &pset
) :
    GenericAnalyzer(fs, _sequence, pset),
    h_n_wq(fsmake<TH1D>("n_wq",
        "Number of l-quarks associated with W", 4, 0, 4)
    ),
    h_n_hb(fsmake<TH1D>("n_hb",
        "Number of b-quarks associated with H", 4, 0, 4)
    ),
    h_n_tb(fsmake<TH1D>("n_tb",
        "Number of b-quarks associated with t", 4, 0, 4)
    ),
    h_sample(fsmake<TH1D>("sample",
        "Sample index", 4, 0, 4)
    )
{
    LOG(DEBUG) << "MEAnalyzer: created MEAnalyzer";
};

bool GenLevelAnalyzer::process(EventContainer &event)
{
    LOG(DEBUG) << "processing " << name << " " << event.i;
    
    AutoTree* inp = event.getData<AutoTree*>("input");
    assert(inp != nullptr);
    
    SampleTypeMajor::SampleTypeMajor sampleTypeMajor =
        event.getData<SampleTypeMajor::SampleTypeMajor>("sampleTypeMajor");
    
    h_sample->Fill((int)(sampleTypeMajor));
    
    const int nGenQFromW = inp->getValue<int>("nGenQFromW");
    const int nGenBFromHiggs = inp->getValue<int>("nGenBFromHiggs");
    const int nGenBFromTop = inp->getValue<int>("nGenBFromTop");
    
    bool ret = true;
    if (sampleTypeMajor == SampleTypeMajor::tth) {
        ret = ret && (nGenBFromHiggs==2);
    }
    
    const bool has_tops = (
        (sampleTypeMajor == SampleTypeMajor::tth) ||
        (sampleTypeMajor == SampleTypeMajor::ttjets)
    );
    
    if (has_tops) {
        ret = ret && (nGenBFromTop==2);
    }
    
    if (ret) {
        h_n_wq->Fill(nGenQFromW);
        h_n_hb->Fill(nGenBFromHiggs);
        h_n_tb->Fill(nGenBFromTop);
    }
    
    GenericAnalyzer::process(event);
    return ret;
};
