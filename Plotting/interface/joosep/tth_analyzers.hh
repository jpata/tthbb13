class TTHMETreeAnalyzer : public GenericAnalyzer
{
public:
    TTHMETreeAnalyzer(
        fwlite::TFileService *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    ) : GenericAnalyzer(fs, _sequence, pset)
    {
        LOG(DEBUG) << "TTHMETreeAnalyzer: created TTHMETreeAnalyzer";
    };

    virtual bool process(EventContainer &event)
    {
        GenericAnalyzer::process(event);
        LOG(DEBUG) << "processing " << name << " " << event.i;

        METree *t = static_cast<METree *>(event.getData<void *>("metree"));
        Sample *s = static_cast<Sample *>(event.getData<void *>("sample"));

        addData(event, "sample", s);
        addData(event, "tree", t);
        addData(event, "weight", (double)t->weight_);
        addData(event, "syst", t->syst_);
        addData(event, "Vtype", static_cast<TTH::EventHypothesis>(t->Vtype_));
        addData(event, "is_sl", is_single_lepton(t, s->type));
        addData(event, "is_dl", is_double_lepton(t, s->type));
        addData(event, "cat", assign_me_category(t, s->type));
        addData(event, "rad", classify_radiation(t, s->process));
        addData(event, "btag_LR", t->btag_LR);
        return true;
    };
};

class LeptonAnalyzer : public GenericAnalyzer
{

    TH1D *h_pt1 = 0;
    TH1D *h_pt2 = 0;

    TH1D *h_iso1 = 0;
    TH1D *h_iso2 = 0;
    TH1D *h_ntags = 0;

    TH1D *h_btag_lr_dl = 0;
    TH1D *h_btag_lr_dl2 = 0;

public:
    LeptonAnalyzer(
        fwlite::TFileService *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    ) : GenericAnalyzer(fs, _sequence, pset)
    {
        LOG(DEBUG) << "LeptonAnalyzer: created LeptonAnalyzer";

        h_pt1 = fsmake<TH1D>("lep1_pt", "Leading lepton p_t", 100, 0, 600);
        h_pt2 = fsmake<TH1D>("lep2_pt", "Subleading lepton p_t", 100, 0, 600);

        h_iso1 = fsmake<TH1D>("lep1_pt", "Leading lepton relative isolation", 100, 0, 1);
        h_iso2 = fsmake<TH1D>("lep2_pt", "Subleading lepton relative isolation", 100, 0, 1);

        h_ntags = fsmake<TH1D>("ntags", "Number of CSVM b-tagged jets", 8, 0, 8);

        h_btag_lr_dl = fsmake<TH1D>("btag_lr", "B-tagging likelihood ratio", 100, 0, 1);
        h_btag_lr_dl2 = fsmake<TH1D>("btag_lr2", "B-tagging likelihood ratio", 100, 0.8, 1.0);
    };

    virtual bool process(EventContainer &event)
    {
        GenericAnalyzer::process(event);
        LOG(DEBUG) << "processing " << name << " " << event.i;
        METree *t = event.getData<METree *>("tth_metree__tree");

        double w = event.getData<double>("tth_metree__weight");

        h_pt1->Fill(t->lepton_pt_[0], w);
        h_pt2->Fill(t->lepton_pt_[1], w);

        h_iso1->Fill(t->lepton_rIso_[0], w);
        h_iso2->Fill(t->lepton_rIso_[1], w);

        h_ntags->Fill(t->numBTagM_, w);

        h_btag_lr_dl->Fill(t->btag_LR, w);
        h_btag_lr_dl2->Fill(t->btag_LR, w);

        return true;
    };
};