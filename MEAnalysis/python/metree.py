import PhysicsTools.HeppyCore.framework.config as cfg


#Defines the output TTree branch structures
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer import *

#Override the default fillCoreVariables function, which
#by default looks for FWLite variables
#FIXME: this is a hack to run heppy on non-EDM formats. Better to propagate it to heppy
def fillCoreVariables(self, tr, event, isMC):
    for x in ["run", "lumi", "evt", "xsec", "nTrueInt", "puWeight", "genWeight"]:
        tr.fill(x, getattr(event.input, x))
AutoFillTreeProducer.fillCoreVariables = fillCoreVariables

#Specifies what to save for jets
jetType = NTupleObjectType("jetType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("id", lambda x : x.id),
    NTupleVariable("btagCSV", lambda x : x.btagCSV),
    NTupleVariable("btagCSVV0", lambda x : x.btagCSVV0),
    NTupleVariable("btagProb", lambda x : x.btagProb),
    NTupleVariable("btagSoftEl", lambda x : x.btagSoftEl),
    NTupleVariable("btagSoftMu", lambda x : x.btagSoftMu),
    NTupleVariable("mcFlavour", lambda x : x.mcFlavour, type=int),
    NTupleVariable("mcMatchId", lambda x : x.mcMatchId, type=int),
    NTupleVariable("hadronFlavour", lambda x : x.hadronFlavour, type=int),
    NTupleVariable("matchFlag", lambda x : getattr(x, "tth_match_label_numeric", -1), type=int),
    NTupleVariable("mcPt", lambda x : x.mcPt),
    NTupleVariable("mcEta", lambda x : x.mcEta),
    NTupleVariable("mcPhi", lambda x : x.mcPhi),
    NTupleVariable("mcM", lambda x : x.mcM),
    NTupleVariable("corr", lambda x : x.corr),
    NTupleVariable("corr_JESUp", lambda x : x.corr_JECUp),
    NTupleVariable("corr_JESDown", lambda x : x.corr_JECDown),

])
#Specifies what to save for leptons
leptonType = NTupleObjectType("leptonType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("pdgId", lambda x : x.pdgId),
    NTupleVariable("relIso03", lambda x : x.relIso03),
    NTupleVariable("relIso04", lambda x : x.relIso04),
    #NTupleVariable("mcPt", lambda x : x.mcPt),
    #NTupleVariable("mcEta", lambda x : x.mcEta),
    #NTupleVariable("mcPhi", lambda x : x.mcPhi),
    #NTupleVariable("mcMass", lambda x : x.mcMass),
])

#Specifies what to save for leptons
pvType = NTupleObjectType("pvType", variables = [
    NTupleVariable("z", lambda x : x.z),
    NTupleVariable("rho", lambda x : x.Rho),
    NTupleVariable("ndof", lambda x : x.ndof),
    NTupleVariable("isFake", lambda x : x.isFake),
])

quarkType = NTupleObjectType("quarkType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("pdgId", lambda x : x.pdgId),
])

metType = NTupleObjectType("metType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("px", lambda x : x.px),
    NTupleVariable("py", lambda x : x.py),
    NTupleVariable("sumEt", lambda x : x.sumEt),
    NTupleVariable("genPt", lambda x : x.genPt),
    NTupleVariable("genPhi", lambda x : x.genPhi),
])

memType = NTupleObjectType("memType", variables = [
    NTupleVariable("p", lambda x : x.p),
    NTupleVariable("p_err", lambda x : x.p_err),
    NTupleVariable("chi2", lambda x : x.chi2),
    NTupleVariable("time", lambda x : x.time),
    NTupleVariable("error_code", lambda x : x.error_code, type=int),
    NTupleVariable("efficiency", lambda x : x.efficiency),
    NTupleVariable("nperm", lambda x : x.num_perm, type=int),
    NTupleVariable("prefit_code", lambda x : x.prefit_code),
    NTupleVariable("btag_weight_bb", lambda x : x.btag_weights[0]),
    NTupleVariable("btag_weight_cc", lambda x : x.btag_weights[1]),
    NTupleVariable("btag_weight_jj", lambda x : x.btag_weights[2]),
])

FoxWolframType = NTupleObjectType("FoxWolframType", variables = [
    NTupleVariable("v", lambda x : x),
])

quarkType = NTupleObjectType("quarkType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("id", lambda x : x.pdgId),
])


def makeGlobalVariable(vtype, systematic="nominal"):
    name = vtype[0]
    typ = vtype[1]
    hlp = vtype[2]

    if len(vtype) == 3:
        func = lambda ev, systematic=systematic, name=name: \
            getattr(ev.systResults[systematic], name, -9999)
    elif len(vtype) == 4:
        if isinstance(vtype[3], str):
            func = lambda ev, systematic=systematic, name=vtype[3]: \
                getattr(ev.systResults[systematic], name, -9999)
        else:
            func = vtype[4]
    syst_suffix = "_" + systematic
    if systematic == "nominal":
        syst_suffix = ""
    return NTupleVariable(
        name + syst_suffix, func, type=typ, help=hlp
    )

def getTreeProducer(conf):
    #Create the output TTree writer
    #Here we define all the variables that we want to save in the output TTree
    treeProducer = cfg.Analyzer(
        class_object = AutoFillTreeProducer,
        verbose = False,
        vectorTree = True,
        globalVariables = [
            NTupleVariable(
               "nGenBHiggs", lambda ev: len(getattr(ev, "b_quarks_h_nominal", [])),
               type=int,
               help="Number of generated b from higgs"
            ),

            NTupleVariable(
               "nGenBTop", lambda ev: len(getattr(ev, "b_quarks_t_nominal", [])),
               type=int,
               help="Number of generated b from top"
            ),

            NTupleVariable(
               "nGenQW", lambda ev: len(getattr(ev, "l_quarks_w_nominal", [])),
               type=int,
               help="Number of generated quarks from W"
            ),
            
            NTupleVariable(
               "passPV", lambda ev: getattr(ev, "passPV", False),
               type=int,
               help="First PV passes selection"
            ),

            #NTupleVariable(
            #    "nGenNuTop", lambda ev: getattr(ev, "nu_top", -1),
            #    type=int,
            #    help="Number of generated nu from top"
            #),

            #NTupleVariable(
            #    "nGenLepTop", lambda ev: getattr(ev, "lep_top"),
            #    type=int,
            #    help="Number of generated charged leptons from top"
            #),

            ####
            #NTupleVariable(
            #    "btag_p_2b_2c", lambda ev: getattr(ev, "btag_lr_2b_2c", -1),
            #    help="B-tagging likelihood for the 2b, 2c hypo (13TeV CSV curves)"
            #),

            #NTupleVariable(
            #    "btag_p_2b_1c", lambda ev: getattr(ev, "btag_lr_2b_1c", -1),
            #    help="B-tagging likelihood for the 2b, 1c hypo (13TeV CSV curves)"
            #),

            #NTupleVariable(
            #    "btag_p_4b_1c", lambda ev: getattr(ev, "btag_lr_4b_1c", -1),
            #    help="B-tagging likelihood for the 4b, 1c hypo (13TeV CSV curves)"
            #),

            #NTupleVariable(
            #    "btag_p_4b", lambda ev: getattr(ev, "btag_lr_4b", -1),
            #    help="B-tagging likelihood for the 4b hypo (13TeV CSV curves)"
            #),

            #NTupleVariable(
            #    "btag_p_2b", lambda ev: getattr(ev, "btag_lr_2b", -1),
            #    help="B-tagging likelihood for the 2b hypo (13TeV CSV curves)"
            #),
            ####

            #NTupleVariable(
            #    "btag_LR_4b_2b_old", lambda ev: getattr(ev, "btag_LR_4b_2b_old", -1),
            #    help="B-tagging likelihood ratio: 4b vs 2b (8TeV CSV curves)"
            #),
            #NTupleVariable(
            #    "btag_LR_4b_2b", lambda ev: getattr(ev, "btag_LR_4b_2b", -1),
            #    help="B-tagging likelihood ratio: 4b vs 2b (8TeV algo, 13 TeV curves)"
            #),
            #NTupleVariable(
            #    "btag_LR_4b_2b_alt", lambda ev: getattr(ev, "btag_LR_4b_2b_alt", -1),
            #    help="B-tagging likelihood ratio: 4b vs 2b with 3-dimensional pt/eta binning for CSV"
            #),
            #NTupleVariable(
            #    "nMatchSimB", lambda ev: getattr(ev, "nMatchSimB", 0),
            #    type=int,
            #    help="number of gen B not matched to top decay (after ISR)"
            #),
            #NTupleVariable(
            #    "nMatchSimC", lambda ev: getattr(ev, "nMatchSimC", 0),
            #    type=int,
            #    help="number of gen C not matched to W decay (after ISR)"
            #),
            
            #NTupleVariable(
            #    "lheNj", lambda ev: ev.input.lheNj if hasattr(ev.input, "lheNj") else 0,
            #    type=int,
            #    help=""
            #),
            #NTupleVariable(
            #    "lheNb", lambda ev: ev.input.lheNb if hasattr(ev.input, "lheNb") else 0,
            #    type=int,
            #    help=""
            #),
            #NTupleVariable(
            #    "lheNc", lambda ev: ev.input.lheNc if hasattr(ev.input, "lheNc") else 0,
            #    type=int,
            #    help=""
            #),
            #NTupleVariable(
            #    "lheNg", lambda ev: ev.input.lheNg if hasattr(ev.input, "lheNg") else 0,
            #    type=int,
            #    help=""
            #),

            #NTupleVariable(
            #    "n_mu_tight", lambda ev: ev.n_mu_tight if hasattr(ev, "n_mu_tight") else 0,
            #    type=int,
            #    help="Number of tight selected muons"
            #),

            #NTupleVariable(
            #    "n_el_tight", lambda ev: ev.n_el_tight if hasattr(ev, "n_el_tight") else 0,
            #    type=int,
            #    help="Number of tight selected electrons"
            #),

            #NTupleVariable(
            #    "n_mu_loose", lambda ev: ev.n_mu_loose if hasattr(ev, "n_mu_loose") else 0,
            #    type=int,
            #    help="Number of loose (DL) selected muons"
            #),

            #NTupleVariable(
            #    "n_el_loose", lambda ev: ev.n_el_loose if hasattr(ev, "n_el_loose") else 0,
            #    type=int,
            #    help="Number of loose (DL) selected electrons"
            #),

            #NTupleVariable(
            #    "tth_px_gen", lambda ev: ev.tth_px_gen if hasattr(ev, "tth_px_gen") else 0,
            #    help="generator-level ttH system px"
            #),
            #NTupleVariable(
            #    "tth_py_gen", lambda ev: ev.tth_py_gen if hasattr(ev, "tth_py_gen") else 0,
            #    help="generator-level ttH system py"
            #),
            #NTupleVariable(
            #    "tth_px_reco", lambda ev: ev.tth_px_reco if hasattr(ev, "tth_px_reco") else 0,
            #    help="reco-level ttH system px from matched jets and leptons"
            #),
            #NTupleVariable(
            #    "tth_py_reco", lambda ev: ev.tth_py_reco if hasattr(ev, "tth_py_reco") else 0,
            #    help="reco-level ttH system py from matched jets and leptons"
            #),

            #NTupleVariable(
            #    "tth_rho_px_reco", lambda ev: ev.tth_rho_px_reco if hasattr(ev, "tth_rho_px_reco") else 0,
            #    help="reco-level ttH system recoil px"
            #),
            #NTupleVariable(
            #    "tth_rho_py_reco", lambda ev: ev.tth_rho_py_reco if hasattr(ev, "tth_rho_py_reco") else 0,
            #    help="reco-level ttH system recoil py"
            #),

            #NTupleVariable(
            #    "tth_rho_px_gen", lambda ev: ev.tth_rho_px_gen if hasattr(ev, "tth_rho_px_gen") else 0,
            #    help="gen-level ttH system recoil px"
            #),
            #NTupleVariable(
            #    "tth_rho_py_gen", lambda ev: ev.tth_rho_py_gen if hasattr(ev, "tth_rho_py_gen") else 0,
            #    help="gen-level ttH system recoil py"
            #),
        ],
        globalObjects = {
           "MET_nominal" : NTupleObject("met", metType, help="Reconstructed MET"),
           "MET_gen_nominal" : NTupleObject("met_gen", metType, help="Generated MET"),
           "MET_jetcorr_nominal" : NTupleObject("met_jetcorr", metType, help="Reconstructed MET, corrected to gen-level jets"),
           "MET_tt_nominal" : NTupleObject("met_ttbar_gen", metType, help="Generated MET from nu(top)"),
           "primaryVertex" : NTupleObject("pv", pvType, help="First PV"),
        },
        collections = {
        #standard dumping of objects
        #    "b_quarks_gen" : NTupleCollection("b_quarks_gen", quarkType, 5, help=""),
        #    "l_quarks_gen" : NTupleCollection("l_quarks_gen", quarkType, 3, help=""),
        #    "b_quarks_t" : NTupleCollection("GenBFromTop", quarkType, 3, help=""),
        #    "b_quarks_h" : NTupleCollection("GenBFromHiggs", quarkType, 3, help=""),
        #    "l_quarks_w" : NTupleCollection("GenQFromW", quarkType, 5, help=""),
            "good_jets_nominal" : NTupleCollection("jets", jetType, 9, help="Selected jets"),
            "good_leptons_nominal" : NTupleCollection("leps", leptonType, 2, help="Selected leptons"),
            # "mem_results_tth_JES": NTupleCollection(
            #     "mem_tth_JES", memType, len(conf.mem["methodsToRun"]),
            #     help="MEM tth results array, element per config.methodsToRun"
            # ),
        }
    )

    for systematic in ["nominal", "JES", "JESUp", "JESDown"]:
        if not (systematic in conf.general["systematics"]):
            continue

        for vtype in [
            ("is_sl",               int,        "Passes single lepton cuts"),
            ("is_dl",               int,        "Passes dilepton cuts"),
            ("Wmass",               float,      "Best reconstructed W candidate mass"),
            ("cat",                 int,        "ME category", "catn"),
            ("cat_btag",            int,        "ME category (b-tag)", "cat_btag_n"),
            ("cat_gen",             int,        "top decay category (-1 unknown, 0 single-leptonic, 1 di-leptonic, 2 fully hadronic)", "cat_gen_n"),
            ("btag_lr_4b",          float,      "4b, N-4 light, probability"),
            ("btag_lr_2b",          float,      "2b, N-2 Nlight probability"),
            ("btag_lr_4b_alt",      float,      "4b, N-4 light, probability, 3D binning"),
            ("btag_lr_2b_alt",      float,      "2b, N-2 Nlight probability, 3D binning"),
            ("btag_LR_4b_2b_old",   float,      ""),
            ("btag_LR_4b_2b",       float,      ""),
            ("btag_LR_4b_2b_alt",   float,      ""),
            ("btag_LR_4b_2b_max4",  float,      ""),
            ("nBCSVM",              float,      ""),
            ("numJets",             int,        ""),
            ("nMatchSimB",          int,        ""),
            ("nMatchSimC",          int,        ""),
            ("nMatch_wq",           int,        ""),
            ("nMatch_wq_btag",      int,        ""),
            ("nMatch_tb",           int,        ""),
            ("nMatch_tb_btag",      int,        ""),
            ("nMatch_hb",           int,        ""),
            ("nMatch_hb_btag",      int,        ""),
            ("isotropy",            float,      ""),
            ("sphericity",          float,      ""),
            ("C",                   float,      ""),
            ("D",                   float,      ""),
            ("aplanarity",          float,      ""),
            ("mean_bdisc",          float,      ""),
            ("mean_bdisc_btag",     float,      ""),
            ("std_bdisc",           float,      ""),
            ("std_bdisc_btag",      float,      ""),
            ("mean_dr_btag",        float,      ""),
            ("std_dr_btag",         float,      ""),
            ("min_dr_btag",         float,      ""),
            ("ht",                  float,      ""),
            ("momentum_eig0",       float,      ""),
            ("momentum_eig1",       float,      ""),
            ("momentum_eig2",       float,      ""),
            ("mass_drpair_btag",    float,      ""),
            ("eta_drpair_btag",     float,      ""),
            ("pt_drpair_btag",      float,      ""),
            ("passes_jet",          int,        ""),
            ("passes_btag",         int,        ""),
        ]:
            treeProducer.globalVariables += [makeGlobalVariable(vtype, systematic)]

            syst_suffix = "_" + systematic
            syst_suffix2 = syst_suffix
            if systematic == "nominal":
                syst_suffix2 = ""
            treeProducer.collections.update({
                "mem_results_tth" + syst_suffix: NTupleCollection(
                    "mem_tth" + syst_suffix2, memType, len(conf.mem["methodOrder"]),
                    help="MEM tth results array, element per config.methodOrder"
                ),
                "mem_results_ttbb" + syst_suffix: NTupleCollection(
                    "mem_ttbb" + syst_suffix2, memType, len(conf.mem["methodOrder"]),
                    help="MEM ttbb results array, element per config.methodOrder"
                ),

                "fw_h_alljets" + syst_suffix: NTupleCollection(
                    "fw_aj" + syst_suffix2, FoxWolframType, 8,
                    help="Fox-Wolfram momenta calculated with all jets"
                ),
                "fw_h_btagjets" + syst_suffix: NTupleCollection(
                    "fw_bj" + syst_suffix2, FoxWolframType, 8,
                    help="Fox-Wolfram momenta calculated with b-tagged jets"
                ),
                "fw_h_untagjets" + syst_suffix: NTupleCollection(
                    "fw_uj" + syst_suffix2, FoxWolframType, 8,
                    help="Fox-Wolfram momenta calculated with untagged jets"
                ),
            })

    for systematic in ["nominal"]:
        for vtype in [
            ("weight_xs",               float,  ""),
            ("ttCls",                   int,    ""),
            ("bTagWeight_LFUp",         float,  ""),
            ("bTagWeight_Stats2Down",   float,  ""),
            ("bTagWeight_LFDown",       float,  ""),
            ("bTagWeight_HFUp",         float,  ""),
            ("bTagWeight_JESDown",      float,  ""),
            ("bTagWeight",              float,  ""),
            ("bTagWeight_HFDown",       float,  ""),
            ("bTagWeight_Stats2Up",     float,  ""),
            ("bTagWeight_JESUp",        float,  ""),
            ("bTagWeight_Stats1Up",     float,  ""),
            ("bTagWeight_Stats1Down",   float,  ""),
        ]:
            treeProducer.globalVariables += [makeGlobalVariable(vtype, systematic)]
    return treeProducer
