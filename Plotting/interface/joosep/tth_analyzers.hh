#include "TH2D.h"
#include "TH1D.h"

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

        MECategory cat = assign_me_category(t, s->type);

        bool is_sl = is_single_lepton(t, s->type);
        bool is_dl = is_double_lepton(t, s->type);

        addData(event, "sample", s);
        addData(event, "tree", t);
        addData(event, "weight", (double)t->weight_);
        addData(event, "syst", t->syst_);
        addData(event, "Vtype", static_cast<TTH::EventHypothesis>(t->Vtype_));
        addData(event, "is_sl", is_single_lepton(t, s->type));
        addData(event, "is_dl", is_double_lepton(t, s->type));
        addData(event, "cat", cat);
        addData(event, "rad", classify_radiation(t, s->process));
        addData(event, "btag_LR", t->btag_LR);
        addData(event, "numJets", t->numJets_);
        addData(event, "numBTagM", t->numBTagM_);
        addData(event, "btag_lr_high_low", is_btag_lr_high_low(t, cat));

        bool ret = true;
        ret = ret && (is_sl || is_dl) && !(is_sl && is_dl);
        ret = ret && (t->syst_ == 0);
        ret = ret && (t->btag_LR >= 0);
        return ret;
    };
};

class LeptonAnalyzer : public GenericAnalyzer
{

    TH1D* h_leptype = 0;
    TH1D* h_samptype = 0;
    TH1D *h_pt1 = 0;
    TH1D *h_pt2 = 0;

    TH1D *h_iso1 = 0;
    TH1D *h_iso2 = 0;
    TH1D *h_ntags = 0;
    TH1D *h_njets = 0;

    TH1D *h_btag_lr = 0;
    TH1D *h_btag_lr2 = 0;

    TH1D *h_vtype = 0;
    TH1D *h_type = 0;

    TH1D *h_cat = 0;
    TH2D *h_cat_btag_lr = 0;
    TH2D *h_cat_btag_lr2 = 0;

    TH1D* h_radmode = 0;
    TH2D* h_rad_lr_default = 0;
    TH2D* h_rad_lr_cc = 0;
    TH2D* h_rad_lr_cc_bj = 0;
    TH2D* h_rad_lr_cc_bj_w = 0;
    TH2D* h_rad_lr_wcq = 0;

    TH1D* h_w = 0;

    const double lambda_bb = 0.1;
    const double lambda_bj = 0.2;
    const double lambda_cc = 0.1;
    const double lambda_jj = 0.6;

public:
    LeptonAnalyzer(
        fwlite::TFileService *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    ) : GenericAnalyzer(fs, _sequence, pset)
    {
        LOG(DEBUG) << "LeptonAnalyzer: created LeptonAnalyzer";

        h_leptype = fsmake<TH1D>("lep_type", "Lepton selection type", 4, 0, 4);
        h_samptype = fsmake<TH1D>("sample_type", "Sample type", 6, 0, 6);


        h_pt1 = fsmake<TH1D>("lep1_pt", "Leading lepton p_t", 100, 0, 600);
        h_pt2 = fsmake<TH1D>("lep2_pt", "Subleading lepton p_t", 100, 0, 600);

        h_iso1 = fsmake<TH1D>("lep1_iso", "Leading lepton relative isolation", 100, 0, 0.2);
        h_iso2 = fsmake<TH1D>("lep2_iso", "Subleading lepton relative isolation", 100, 0, 0.2);

        h_njets = fsmake<TH1D>("njets", "Number of jets", 16, 0, 16);
        h_ntags = fsmake<TH1D>("ntags", "Number of CSVM b-tagged jets", 8, 0, 8);

        h_btag_lr = fsmake<TH1D>("btag_lr", "B-tagging likelihood ratio", 100, 0, 1);
        h_btag_lr2 = fsmake<TH1D>("btag_lr2", "B-tagging likelihood ratio", 100, 0.8, 1.0);

        h_vtype = fsmake<TH1D>("Vtype", "Vtype", 8, 0, 8);
        h_type = fsmake<TH1D>("type", "type", 8, 0, 8);

        h_cat = fsmake<TH1D>("cat", "ME category", 8, 0, 8);
        h_cat_btag_lr = fsmake<TH2D>("cat_btag_lr", "ME category vs. b-tagging likelihood ratio", 8, 0, 8, 100, 0, 1);
        h_cat_btag_lr2 = fsmake<TH2D>("cat_btag_lr2", "ME category vs. b-tagging likelihood ratio", 8, 0, 8, 100, 0.9, 1);

        h_radmode = fsmake<TH1D>("rad", "Radiation mode", 8, 0, 8);
        h_rad_lr_default = fsmake<TH2D>("rad_lr", "Radiation mode vs bLR", 8, 0, 8, 100, 0, 1);
        h_rad_lr_cc = fsmake<TH2D>("rad_lr_cc", "Radiation mode vs bLR", 8, 0, 8, 100, 0, 1);
        h_rad_lr_cc_bj = fsmake<TH2D>("rad_lr_cc_bj", "Radiation mode vs bLR", 8, 0, 8, 100, 0, 1);
        h_rad_lr_cc_bj_w = fsmake<TH2D>("rad_lr_cc_bj_w", "Radiation mode vs bLR", 8, 0, 8, 100, 0, 1);
        h_rad_lr_wcq = fsmake<TH2D>("rad_lr_wcq", "Radiation mode vs bLR", 8, 0, 8, 100, 0, 1);

        h_w = fsmake<TH1D>("w", "Event weight", 100, -2, 2);
    };

    virtual bool process(EventContainer &event)
    {
        GenericAnalyzer::process(event);
        LOG(DEBUG) << "processing " << name << " " << event.i;
        METree *t = event.getData<METree *>("tth_metree__tree");

        double w = event.getData<double>("tth_metree__weight");
        MECategory cat = event.getData<MECategory>("tth_metree__cat");
        RadiationMode rad = event.getData<RadiationMode>("tth_metree__rad");
        //SampleType samp = event.getData<SampleType>("sample");


        bool is_sl = event.getData<bool>("tth_metree__is_sl");
        bool is_dl = event.getData<bool>("tth_metree__is_dl");

        if (is_sl && is_dl) {
            h_leptype->Fill(3.0, w);
        }
        else if (is_sl) {
            h_leptype->Fill(1.0, w);
        }
        else if (is_dl) {
            h_leptype->Fill(2.0, w);
        } else {
            h_leptype->Fill(0.0, w);
        }

        //h_samptype->Fill(samp, w);

        const double lr_default = t->btag_lr_l_bbbb / (t->btag_lr_l_bbbb + t->btag_lr_l_bbjj);
        const double lr_cc = lambda_bb * t->btag_lr_l_bbbb / (lambda_bb * t->btag_lr_l_bbbb + (1.0 - lambda_bb - lambda_cc) * t->btag_lr_l_bbjj + lambda_cc * t->btag_lr_l_bbcc);
        const double lr_cc_bj = t->btag_lr_l_bbbb / (t->btag_lr_l_bbbb + t->btag_lr_l_bbbj + t->btag_lr_l_bbjj + t->btag_lr_l_bbcc);
        const double lr_cc_bj_w = lambda_bb * t->btag_lr_l_bbbb / (lambda_bb * t->btag_lr_l_bbbb + lambda_bj * t->btag_lr_l_bbbj + lambda_jj * t->btag_lr_l_bbjj + lambda_cc * t->btag_lr_l_bbcc);
        const double lr_wcq = (t->btag_lr_l_bbbb + t->btag_lr_l_bbbbcq) / (t->btag_lr_l_bbbb + t->btag_lr_l_bbbbcq + t->btag_lr_l_bbjj + t->btag_lr_l_bbjjcq);
        
        if (t->numJets_ >= 6) {
            h_radmode->Fill(rad, w);
            h_rad_lr_default  -> Fill(rad, lr_default, w);
            h_rad_lr_cc       -> Fill(rad, lr_cc, w);
            h_rad_lr_cc_bj    -> Fill(rad, lr_cc_bj, w);
            h_rad_lr_cc_bj_w  -> Fill(rad, lr_cc_bj_w, w);
            h_rad_lr_wcq      -> Fill(rad, lr_wcq, w);
        }

        h_w->Fill(w);

        h_pt1->Fill(t->lepton_pt_[0], w);
        h_pt2->Fill(t->lepton_pt_[1], w);

        h_iso1->Fill(t->lepton_rIso_[0], w);
        h_iso2->Fill(t->lepton_rIso_[1], w);

        h_njets->Fill(t->numJets_, w);
        h_ntags->Fill(t->numBTagM_, w);

        h_btag_lr->Fill(t->btag_LR, w);
        h_btag_lr2->Fill(t->btag_LR, w);

        h_vtype->Fill(t->Vtype_, w);
        h_type->Fill(t->type_, w);

        h_cat->Fill(cat, w);
        h_cat_btag_lr->Fill(cat, t->btag_LR, w);
        h_cat_btag_lr2->Fill(cat, t->btag_LR, w);

        return true;
    };
};


class MEDiscriminatorAnalyzer : public GenericAnalyzer
{


TH2D *h_cat_discr = 0;

TH2D *h_cat_n_wqq_matched = 0;
TH2D *h_cat_n_bt_matched = 0;
TH2D *h_cat_n_bh_matched = 0;

public:
    MEDiscriminatorAnalyzer(
        fwlite::TFileService *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    ) : GenericAnalyzer(fs, _sequence, pset)
    {
        LOG(DEBUG) << "MEDiscriminatorAnalyzer: created MEDiscriminatorAnalyzer";

        h_cat_discr = fsmake<TH2D>("cat_discr", "ME Category vs. discriminator", 8, 0, 8, 6, 0, 1);

        h_cat_n_wqq_matched = fsmake<TH2D>("cat_n_wqq_matched", "ME Category vs. discriminator", 8, 0, 8, 3, 0, 3);
        h_cat_n_bt_matched  = fsmake<TH2D>("cat_n_bt_matched", "ME Category vs. discriminator", 8, 0, 8, 3, 0, 3);
        h_cat_n_bh_matched  = fsmake<TH2D>("cat_n_bh_matched", "ME Category vs. discriminator", 8, 0, 8, 3, 0, 3);

    };

    virtual bool process(EventContainer &event)
    {
        GenericAnalyzer::process(event);
        LOG(DEBUG) << "processing " << name << " " << event.i;
        METree *t = event.getData<METree *>("tth_metree__tree");

        double w = event.getData<double>("tth_metree__weight");
        MECategory cat = event.getData<MECategory>("tth_metree__cat");

        double me_discr = t->probAtSgn_ / (t->probAtSgn_ + 0.02 * t->probAtSgn_alt_);
        if (me_discr > 1.0)
            me_discr = 1.0;
        if (me_discr < 0.0)
            me_discr = 0.0;
        if (me_discr != me_discr)
            me_discr = 0.0;
        
        h_cat_discr->Fill(cat, me_discr, w);


        int n_best_perm = -1;
        int best_perm = 0;
        for (int np=0; np < t->nPermut_; np++) {
            const int perm = t->perm_to_gen_[np];

            //number of particles matched out of 6
            int _n = perm_maps::count_matched(perm);
            if (_n > n_best_perm) {
                n_best_perm = _n;
                best_perm = perm;
                //idx_best_perm = np;
            }
        }

        bool bt1_match = perm_maps::get_n(best_perm, 6);
        bool bt2_match = perm_maps::get_n(best_perm, 3);

        bool bh1_match = perm_maps::get_n(best_perm, 1);
        bool bh2_match = perm_maps::get_n(best_perm, 2);

        bool q1_match = perm_maps::get_n(best_perm, 4);
        bool q2_match = perm_maps::get_n(best_perm, 5);


        int n_q_matched = q1_match + q2_match;
        int n_bt_matched = bt1_match + bt2_match;
        int n_bh_matched = bh1_match + bh2_match;

        h_cat_n_wqq_matched->Fill(cat, n_q_matched, w);
        h_cat_n_bt_matched->Fill(cat, n_bt_matched, w);
        h_cat_n_bh_matched->Fill(cat, n_bh_matched, w);

        return true;
    };
};

class TTHEventPrinterAnalyzer : public GenericAnalyzer
{

public:
    TTHEventPrinterAnalyzer(
        fwlite::TFileService *fs,
        Sequence *_sequence,
        const edm::ParameterSet &pset
    ) : GenericAnalyzer(fs, _sequence, pset)
    {
        LOG(DEBUG) << "TTHEventPrinterAnalyzer: created TTHEventPrinterAnalyzer";
    };

    virtual bool process(EventContainer &event)
    {
        GenericAnalyzer::process(event);
        LOG(DEBUG) << "processing " << name << " " << event.i;

        bool proc_MEAnalysisSeq = event.wasRun("MEAnalysisSeq");
        bool proc_slSeq = event.wasRun("slSeq");
        bool proc_slCatLSeq = event.wasRun("slCatLSeq");
        bool proc_slCatHSeq = event.wasRun("slCatHSeq");
        bool proc_dlSeq = event.wasRun("dlSeq");
        bool proc_dlCatLSeq = event.wasRun("dlCatLSeq");
        bool proc_dlCatHSeq = event.wasRun("dlCatHSeq");

        bool succ_MEAnalysisSeq = event.wasSuccess("MEAnalysisSeq");
        bool succ_slSeq = event.wasSuccess("slSeq");
        bool succ_slCatLSeq = event.wasSuccess("slCatLSeq");
        bool succ_slCatHSeq = event.wasSuccess("slCatHSeq");
        bool succ_dlSeq = event.wasSuccess("dlSeq");
        bool succ_dlCatLSeq = event.wasSuccess("dlCatLSeq");
        bool succ_dlCatHSeq = event.wasSuccess("dlCatHSeq");

        METree *t = static_cast<METree *>(event.getData<void *>("metree"));
        MECategory cat = event.getData<MECategory>("tth_metree__cat");

        std::cout
            << "vt=" << t->Vtype_ <<  " "
            << "cat=" << cat <<  " "
            << "blr=" << t->btag_LR <<  " "
            << "HL=" << is_btag_lr_high_low(t, cat) <<  " "
            << "sl=" << event.getData<bool>("tth_metree__is_sl") <<  " "
            << "dl=" << event.getData<bool>("tth_metree__is_dl") << " "
            << proc_MEAnalysisSeq << " "
            << proc_slSeq << " " 
            << proc_slCatLSeq << " " 
            << proc_slCatHSeq << " " 
            << proc_dlSeq << " " 
            << proc_dlCatLSeq << " " 
            << proc_dlCatHSeq << " " 

            << succ_MEAnalysisSeq << " "
            << succ_slSeq << " " 
            << succ_slCatLSeq << " " 
            << succ_slCatHSeq << " " 
            << succ_dlSeq << " " 
            << succ_dlCatLSeq << " " 
            << succ_dlCatHSeq << std::endl;
        return true;
    };
};