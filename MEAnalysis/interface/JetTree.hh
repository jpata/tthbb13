#ifndef JET_TREE_H
#define JET_TREE_H

#include "TTree.h"
#include "TTH/TTHNtupleAnalyzer/interface/tth_tree.hh"

class JetTree {
public:
	JetTree(TTree* _genTree, TTree* _genJetLightTree, TTree* _genJetGluonTree, TTree* _genJetHeavyTree, TTree* _genEventTree) {
    	genTree = _genTree;
    	genJetLightTree = _genJetLightTree;
    	genJetGluonTree = _genJetGluonTree;
    	genJetHeavyTree = _genJetHeavyTree;
    	genEventTree = _genEventTree;
    };

    TTree* genTree;
    TTree* genJetLightTree;
    TTree* genJetGluonTree;
    TTree* genJetHeavyTree;
    TTree* genEventTree;

    float BetaW;
    float GammaW;
    float BetaWLep;
    float GammaWLep;

    float sumEt;
    float et;
    float etReco;
    float phi;
    float phiReco;
    float px, pxReco, py, pyReco;
    float puWeight;

    float regVarsFHeavy[14];
    int   regVarsIHeavy[2];

    float eRecoHeavy;
    float ptRecoHeavy;
    float phiRecoHeavy;
    float etaRecoHeavy;
    float massRecoHeavy;
    float csvRecoHeavy;
    float csvRecoStdHeavy;
    float csvRecoMVAHeavy;
    float eRecoRegHeavy;
    float ptRecoRegHeavy;
    float ePartHeavy;
    float ptPartHeavy;
    float etaPartHeavy;
    float phiPartHeavy;
    float eGenHeavy;
    float ptGenHeavy;
    float etaGenHeavy;
    float phiGenHeavy;
    int   flavorHeavy;

    float eRecoLight;
    float ptRecoLight;
    float phiRecoLight;
    float etaRecoLight;
    float massRecoLight;
    float csvRecoLight;
    float csvRecoStdLight;
    float csvRecoMVALight;
    float eRecoRegLight;
    float ptRecoRegLight;
    float ePartLight;
    float ptPartLight;
    float etaPartLight;
    float phiPartLight;
    float eGenLight;
    float ptGenLight;
    float etaGenLight;
    float phiGenLight;
    int   flavorLight;

    float eRecoGluon;
    float ptRecoGluon;
    float phiRecoGluon;
    float etaRecoGluon;
    float massRecoGluon;
    float csvRecoGluon;
    float csvRecoStdGluon;
    float csvRecoMVAGluon;
    float eRecoRegGluon;
    float ptRecoRegGluon;
    float ePartGluon;
    float ptPartGluon;
    float etaPartGluon;
    float phiPartGluon;
    float eGenGluon;
    float ptGenGluon;
    float etaGenGluon;
    float phiGenGluon;
    int   flavorGluon;
	
	void make_branches() {
        genTree->Branch("BetaW",               &BetaW,       "BetaW/F");
        genTree->Branch("GammaW",              &GammaW,      "GammaW/F");
        genTree->Branch("BetaWLep",            &BetaWLep,    "BetaWLep/F");
        genTree->Branch("GammaWLep",           &GammaWLep,   "GammaWLep/F");

        genEventTree->Branch("sumEt",          &sumEt,       "sumEt/F");
        genEventTree->Branch("et",             &et,          "et/F");
        genEventTree->Branch("etReco",         &etReco,      "etReco/F");
        genEventTree->Branch("phi",            &phi,         "phi/F");
        genEventTree->Branch("phiReco",        &phiReco,     "phiReco/F");
        genEventTree->Branch("px",             &px,          "px/F");
        genEventTree->Branch("pxReco",         &pxReco,      "pxReco/F");
        genEventTree->Branch("py",             &py,          "py/F");
        genEventTree->Branch("pyReco",         &pyReco,      "pyReco/F");
        genEventTree->Branch("puWeight",       &puWeight,    "puWeight/F");

        addRegressionBranchesPerJet(genJetHeavyTree, regVarsFHeavy, regVarsIHeavy);
        genJetHeavyTree->Branch("e_rec",       &eRecoHeavy,    "e_rec/F");
        genJetHeavyTree->Branch("pt_rec",      &ptRecoHeavy,   "pt_rec/F");
        genJetHeavyTree->Branch("eta_rec",     &etaRecoHeavy,  "eta_rec/F");
        genJetHeavyTree->Branch("phi_rec",     &phiRecoHeavy,  "phi_rec/F");
        genJetHeavyTree->Branch("csv_rec",     &csvRecoHeavy,  "csv_rec/F");
        genJetHeavyTree->Branch("csv_std_rec", &csvRecoStdHeavy,"csv_std_rec/F");
        genJetHeavyTree->Branch("csv_mva_rec", &csvRecoMVAHeavy,"csv_mva_rec/F");
        genJetHeavyTree->Branch("mass_rec",    &massRecoHeavy, "mass_rec/F");
        genJetHeavyTree->Branch("e_rec_reg",   &eRecoRegHeavy, "e_rec_reg/F");
        genJetHeavyTree->Branch("pt_rec_reg",  &ptRecoRegHeavy,"pt_rec_reg/F");
        genJetHeavyTree->Branch("e_part",      &ePartHeavy,    "e_part/F");
        genJetHeavyTree->Branch("pt_part",     &ptPartHeavy,   "pt_part/F");
        genJetHeavyTree->Branch("eta_part",    &etaPartHeavy,  "eta_part/F");
        genJetHeavyTree->Branch("phi_part",    &phiPartHeavy,  "phi_part/F");
        genJetHeavyTree->Branch("e_gen",       &eGenHeavy,     "e_gen/F");
        genJetHeavyTree->Branch("pt_gen",      &ptGenHeavy,    "pt_gen/F");
        genJetHeavyTree->Branch("eta_gen",     &etaGenHeavy,   "eta_gen/F");
        genJetHeavyTree->Branch("phi_gen",     &phiGenHeavy,   "phi_gen/F");
        genJetHeavyTree->Branch("flavor",      &flavorHeavy,   "flavor/I");

        genJetLightTree->Branch("e_rec",       &eRecoLight,    "e_rec/F");
        genJetLightTree->Branch("pt_rec",      &ptRecoLight,   "pt_rec/F");
        genJetLightTree->Branch("eta_rec",     &etaRecoLight,  "eta_rec/F");
        genJetLightTree->Branch("phi_rec",     &phiRecoLight,  "phi_rec/F");
        genJetLightTree->Branch("csv_rec",     &csvRecoLight,  "csv_rec/F");
        genJetLightTree->Branch("csv_std_rec", &csvRecoStdLight,"csv_std_rec/F");
        genJetLightTree->Branch("csv_mva_rec", &csvRecoMVALight,"csv_mva_rec/F");
        genJetLightTree->Branch("mass_rec",    &massRecoLight, "mass_rec/F");
        genJetLightTree->Branch("e_rec_reg",   &eRecoRegLight, "e_rec_reg/F");
        genJetLightTree->Branch("pt_rec_reg",  &ptRecoRegLight,"pt_rec_reg/F");
        genJetLightTree->Branch("e_part",      &ePartLight,    "e_part/F");
        genJetLightTree->Branch("pt_part",     &ptPartLight,   "pt_part/F");
        genJetLightTree->Branch("eta_part",    &etaPartLight,  "eta_part/F");
        genJetLightTree->Branch("phi_part",    &phiPartLight,  "phi_part/F");
        genJetLightTree->Branch("e_gen",       &eGenLight,     "e_gen/F");
        genJetLightTree->Branch("pt_gen",      &ptGenLight,    "pt_gen/F");
        genJetLightTree->Branch("eta_gen",     &etaGenLight,   "eta_gen/F");
        genJetLightTree->Branch("phi_gen",     &phiGenLight,   "phi_gen/F");
        genJetLightTree->Branch("flavor",      &flavorLight,   "flavor/I");

        genJetGluonTree->Branch("e_rec",       &eRecoGluon,    "e_rec/F");
        genJetGluonTree->Branch("pt_rec",      &ptRecoGluon,   "pt_rec/F");
        genJetGluonTree->Branch("eta_rec",     &etaRecoGluon,  "eta_rec/F");
        genJetGluonTree->Branch("phi_rec",     &phiRecoGluon,  "phi_rec/F");
        genJetGluonTree->Branch("csv_rec",     &csvRecoGluon,  "csv_rec/F");
        genJetGluonTree->Branch("csv_std_rec", &csvRecoStdGluon,"csv_std_rec/F");
        genJetGluonTree->Branch("csv_mva_rec", &csvRecoMVAGluon,"csv_mva_rec/F");
        genJetGluonTree->Branch("mass_rec",    &massRecoGluon, "mass_rec/F");
        genJetGluonTree->Branch("e_rec_reg",   &eRecoRegGluon, "e_rec_reg/F");
        genJetGluonTree->Branch("pt_rec_reg",  &ptRecoRegGluon,"pt_rec_reg/F");
        genJetGluonTree->Branch("e_part",      &ePartGluon,    "e_part/F");
        genJetGluonTree->Branch("pt_part",     &ptPartGluon,   "pt_part/F");
        genJetGluonTree->Branch("eta_part",    &etaPartGluon,  "eta_part/F");
        genJetGluonTree->Branch("phi_part",    &phiPartGluon,  "phi_part/F");
        genJetGluonTree->Branch("e_gen",       &eGenGluon,     "e_gen/F");
        genJetGluonTree->Branch("pt_gen",      &ptGenGluon,    "pt_gen/F");
        genJetGluonTree->Branch("eta_gen",     &etaGenGluon,   "eta_gen/F");
        genJetGluonTree->Branch("phi_gen",     &phiGenGluon,   "phi_gen/F");
        genJetGluonTree->Branch("flavor",      &flavorGluon,   "flavor/I");
	}

	void loop_initialize() {
    	BetaW = DEF_VAL_FLOAT;
    	GammaW = DEF_VAL_FLOAT;
    	BetaWLep = DEF_VAL_FLOAT;
    	GammaWLep = DEF_VAL_FLOAT;

    	sumEt = DEF_VAL_FLOAT;
    	et = DEF_VAL_FLOAT;
    	etReco = DEF_VAL_FLOAT;
    	phi = DEF_VAL_FLOAT;
    	phiReco = DEF_VAL_FLOAT;
    	px = DEF_VAL_FLOAT, pxReco = DEF_VAL_FLOAT, py = DEF_VAL_FLOAT, pyReco = DEF_VAL_FLOAT;
    	puWeight = DEF_VAL_FLOAT;

    	SET_ZERO(regVarsFHeavy, 14, DEF_VAL_FLOAT);
    	SET_ZERO(regVarsIHeavy, 2, DEF_VAL_INT);

    	eRecoHeavy = DEF_VAL_FLOAT;
    	ptRecoHeavy = DEF_VAL_FLOAT;
    	phiRecoHeavy = DEF_VAL_FLOAT;
    	etaRecoHeavy = DEF_VAL_FLOAT;
    	massRecoHeavy = DEF_VAL_FLOAT;
    	csvRecoHeavy = DEF_VAL_FLOAT;
    	csvRecoStdHeavy = DEF_VAL_FLOAT;
    	csvRecoMVAHeavy = DEF_VAL_FLOAT;
    	eRecoRegHeavy = DEF_VAL_FLOAT;
    	ptRecoRegHeavy = DEF_VAL_FLOAT;
    	ePartHeavy = DEF_VAL_FLOAT;
    	ptPartHeavy = DEF_VAL_FLOAT;
    	etaPartHeavy = DEF_VAL_FLOAT;
    	phiPartHeavy = DEF_VAL_FLOAT;
    	eGenHeavy = DEF_VAL_FLOAT;
    	ptGenHeavy = DEF_VAL_FLOAT;
    	etaGenHeavy = DEF_VAL_FLOAT;
    	phiGenHeavy = DEF_VAL_FLOAT;
    	flavorHeavy = DEF_VAL_INT;

    	eRecoLight = DEF_VAL_FLOAT;
    	ptRecoLight = DEF_VAL_FLOAT;
    	phiRecoLight = DEF_VAL_FLOAT;
    	etaRecoLight = DEF_VAL_FLOAT;
    	massRecoLight = DEF_VAL_FLOAT;
    	csvRecoLight = DEF_VAL_FLOAT;
    	csvRecoStdLight = DEF_VAL_FLOAT;
    	csvRecoMVALight = DEF_VAL_FLOAT;
    	eRecoRegLight = DEF_VAL_FLOAT;
    	ptRecoRegLight = DEF_VAL_FLOAT;
    	ePartLight = DEF_VAL_FLOAT;
    	ptPartLight = DEF_VAL_FLOAT;
    	etaPartLight = DEF_VAL_FLOAT;
    	phiPartLight = DEF_VAL_FLOAT;
    	eGenLight = DEF_VAL_FLOAT;
    	ptGenLight = DEF_VAL_FLOAT;
    	etaGenLight = DEF_VAL_FLOAT;
    	phiGenLight = DEF_VAL_FLOAT;
    	flavorLight = DEF_VAL_INT;

    	eRecoGluon = DEF_VAL_FLOAT;
    	ptRecoGluon = DEF_VAL_FLOAT;
    	phiRecoGluon = DEF_VAL_FLOAT;
    	etaRecoGluon = DEF_VAL_FLOAT;
    	massRecoGluon = DEF_VAL_FLOAT;
    	csvRecoGluon = DEF_VAL_FLOAT;
    	csvRecoStdGluon = DEF_VAL_FLOAT;
    	csvRecoMVAGluon = DEF_VAL_FLOAT;
    	eRecoRegGluon = DEF_VAL_FLOAT;
    	ptRecoRegGluon = DEF_VAL_FLOAT;
    	ePartGluon = DEF_VAL_FLOAT;
    	ptPartGluon = DEF_VAL_FLOAT;
    	etaPartGluon = DEF_VAL_FLOAT;
    	phiPartGluon = DEF_VAL_FLOAT;
    	eGenGluon = DEF_VAL_FLOAT;
    	ptGenGluon = DEF_VAL_FLOAT;
    	etaGenGluon = DEF_VAL_FLOAT;
    	phiGenGluon = DEF_VAL_FLOAT;
    	flavorGluon = DEF_VAL_INT;
	}
};

#endif
