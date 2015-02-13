#ifndef HELPERS_STEP2_H
#define HELPERS_STEP2_H

#include "TTH/TTHNtupleAnalyzer/interface/HypoEnums.hh"
#include "TTH/TTHNtupleAnalyzer/interface/event_interpretation.hh"
#include "TTH/MEAnalysis/interface/METree.hh"
#include "TTH/TTHNtupleAnalyzer/interface/tth_tree.hh"

enum SampleType {
    NOME_8TEV,
    ME_8TEV,
    NOME_13TEV,
    ME_13TEV
};

enum Process {
    TTHBB,
    TTJETS
};

enum MECategory {
    UNKNOWN_CAT,
    CAT1,
    CAT2,
    CAT3,
//    CAT6,
    CAT6ee,
    CAT6emu,
    CAT6mumu,
};

enum CutReasons {
    SYST,
    LEPTON,
    BTAG_LR,
};

enum RadiationMode {
    BB,
    BJ,
    CC,
    JJ,
    UNKNOWN_RADIATION
};

double clip_value(double x, double l, double h);

MECategory assign_me_category(METree* t, SampleType st);
bool is_single_lepton(METree* t, SampleType sample_type);
bool is_double_lepton(METree* t, SampleType sample_type);
int is_btag_lr_high_low(METree* t, MECategory cat);
bool is_correct_perm(int perm, MECategory cat, Process prc);
TTH::EventHypothesis assing_gen_vtype(TTHTree* t);
RadiationMode classify_radiation(METree* t, Process p);

#endif