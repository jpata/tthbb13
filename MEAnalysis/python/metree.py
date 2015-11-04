import PhysicsTools.HeppyCore.framework.config as cfg


#Defines the output TTree branch structures
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer import *

#Override the default fillCoreVariables function, which
#by default looks for FWLite variables
#FIXME: this is a hack to run heppy on non-EDM formats. Better to propagate it to heppy
def fillCoreVariables(self, tr, event, isMC):
    if isMC:
        for x in ["run", "lumi", "evt", "xsec", "nTrueInt", "puWeight", "genWeight"]:
            tr.fill(x, getattr(event.input, x))
    else:
        for x in ["run", "lumi", "evt"]:
            tr.fill(x, getattr(event.input, x))
    #attrs = dir(event.input)
    #print attrs 
    #for attr in attrs:
    #    if attr.startswith("HLT"):
    #        tr.fill(attr, getattr(event.input, attr))
AutoFillTreeProducer.fillCoreVariables = fillCoreVariables

#Specifies what to save for jets
jetType = NTupleObjectType("jetType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("id", lambda x : x.id, mcOnly=True),  
    NTupleVariable("qgl", lambda x : x.qgl),
    NTupleVariable("btagCSV", lambda x : x.btagCSV),
    NTupleVariable("btagBDT", lambda x : x.btagBDT),
    NTupleVariable("bTagWeight", lambda x : x.bTagWeight, mcOnly=True),
    NTupleVariable("bTagWeightHFUp", lambda x : x.bTagWeightHFUp, mcOnly=True),
    NTupleVariable("bTagWeightHFDown", lambda x : x.bTagWeightHFDown, mcOnly=True),
    NTupleVariable("bTagWeightLFUp", lambda x : x.bTagWeightLFUp, mcOnly=True),
    NTupleVariable("bTagWeightLFDown", lambda x : x.bTagWeightLFDown, mcOnly=True),
    NTupleVariable("bTagWeightStats1Up", lambda x : x.bTagWeightStats1Up, mcOnly=True),
    NTupleVariable("bTagWeightStats1Down", lambda x : x.bTagWeightStats1Down, mcOnly=True),
    NTupleVariable("bTagWeightStats2Up", lambda x : x.bTagWeightStats2Up, mcOnly=True),
    NTupleVariable("bTagWeightStats2Down", lambda x : x.bTagWeightStats2Down, mcOnly=True),
    NTupleVariable("bTagWeightJESUp", lambda x : x.bTagWeightJESUp, mcOnly=True),
    NTupleVariable("bTagWeightJESDown", lambda x : x.bTagWeightJESDown, mcOnly=True),
    NTupleVariable("mcFlavour", lambda x : x.mcFlavour, type=int, mcOnly=True),
    NTupleVariable("mcMatchId", lambda x : x.mcMatchId, type=int, mcOnly=True),
    NTupleVariable("hadronFlavour", lambda x : x.hadronFlavour, type=int, mcOnly=True),
    NTupleVariable("matchFlag", lambda x : getattr(x, "tth_match_label_numeric", -1), type=int, mcOnly=True),
    NTupleVariable("mcPt", lambda x : x.mcPt, mcOnly=True),
    NTupleVariable("mcEta", lambda x : x.mcEta, mcOnly=True),
    NTupleVariable("mcPhi", lambda x : x.mcPhi, mcOnly=True),
    NTupleVariable("mcM", lambda x : x.mcM, mcOnly=True),
    NTupleVariable("mcNumBHadrons", lambda x : x.genjet.numBHadrons if hasattr(x, "genjet") else -1, mcOnly=True),
    NTupleVariable("mcNumCHadrons", lambda x : x.genjet.numCHadrons if hasattr(x, "genjet") else -1, mcOnly=True),
    NTupleVariable("corr", lambda x : x.corr, mcOnly=True),
    NTupleVariable("corr_JER", lambda x : x.corr_JER, mcOnly=True),
    NTupleVariable("corr_JESUp", lambda x : x.corr_JECUp, mcOnly=True),
    NTupleVariable("corr_JESDown", lambda x : x.corr_JECDown, mcOnly=True),
    NTupleVariable("corr_JERUp", lambda x : x.corr_JERUp, mcOnly=True),
    NTupleVariable("corr_JERDown", lambda x : x.corr_JERDown, mcOnly=True),
])

#Specifies what to save for leptons
leptonType = NTupleObjectType("leptonType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("pdgId", lambda x : x.pdgId),
    NTupleVariable("relIso03", lambda x : x.pfRelIso03),
    NTupleVariable("relIso04", lambda x : x.pfRelIso04),
])

p4type = NTupleObjectType("p4Type", variables = [
    NTupleVariable("pt", lambda x : x.Pt()),
    NTupleVariable("eta", lambda x : x.Eta()),
    NTupleVariable("phi", lambda x : x.Phi()),
    NTupleVariable("mass", lambda x : x.M()),
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
    NTupleVariable("genPt", lambda x : x.genPt, mcOnly=True),
    NTupleVariable("genPhi", lambda x : x.genPhi, mcOnly=True),
])

memType = NTupleObjectType("memType", variables = [
    NTupleVariable("p", lambda x : x.p),
    NTupleVariable("p_err", lambda x : x.p_err),
    NTupleVariable("chi2", lambda x : x.chi2),
    NTupleVariable("time", lambda x : x.time),
    NTupleVariable("error_code", lambda x : x.error_code, type=int),
    NTupleVariable("efficiency", lambda x : x.efficiency),
    NTupleVariable("nperm", lambda x : x.num_perm, type=int),
])

branType = NTupleObjectType("branType", variables = [
    NTupleVariable("p",        lambda x : x[0] ),
    NTupleVariable("ntoys",    lambda x : x[1], type=int),
    NTupleVariable("pass",     lambda x : x[2], type=int),
    NTupleVariable("tag_id",   lambda x : x[3], type=int),
])

#branvalType = NTupleObjectType("branvalType", variables = [
#    NTupleVariable("btagCSVRnd",        lambda x : x ),
#])

#binpvalType = NTupleObjectType("branvalType", variables = [
#    NTupleVariable("btagCSVInp",        lambda x : x ),
#])

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


def makeGlobalVariable(vtype, systematic="nominal", mcOnly=False):
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
        name + syst_suffix, func, type=typ, help=hlp, mcOnly=mcOnly
    )
# V11 & V12
# ==============================

topType = NTupleObjectType("topType", variables = [
    NTupleVariable("fRec", lambda x: x.fRec ),
    NTupleVariable("Ropt", lambda x: x.Ropt ),
    NTupleVariable("RoptCalc", lambda x: x.RoptCalc ),
    NTupleVariable("ptForRoptCalc", lambda x: x.ptForRoptCalc ),
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("mass", lambda x: x.mass ),
    NTupleVariable("sjW1pt", lambda x: x.sjW1pt ),
    NTupleVariable("sjW1eta", lambda x: x.sjW1eta ),
    NTupleVariable("sjW1phi", lambda x: x.sjW1phi ),
    NTupleVariable("sjW1mass", lambda x: x.sjW1mass ),
    NTupleVariable("sjW1btag", lambda x: x.sjW1btag ),
    NTupleVariable("sjW2pt", lambda x: x.sjW2pt ),
    NTupleVariable("sjW2eta", lambda x: x.sjW2eta ),
    NTupleVariable("sjW2phi", lambda x: x.sjW2phi ),
    NTupleVariable("sjW2mass", lambda x: x.sjW2mass ),
    NTupleVariable("sjW2btag", lambda x: x.sjW2btag ),
    NTupleVariable("sjNonWpt", lambda x: x.sjNonWpt ),
    NTupleVariable("sjNonWeta", lambda x: x.sjNonWeta ),
    NTupleVariable("sjNonWphi", lambda x: x.sjNonWphi ),
    NTupleVariable("sjNonWmass", lambda x: x.sjNonWmass ),
    NTupleVariable("sjNonWbtag", lambda x: x.sjNonWbtag ),
    NTupleVariable("tau1", lambda x: x.tau1 ),   # Copied from matched fat jet
    NTupleVariable("tau2", lambda x: x.tau2 ),   # Copied from matched fat jet
    NTupleVariable("tau3", lambda x: x.tau3 ),   # Copied from matched fat jet
    NTupleVariable("bbtag", lambda x: x.bbtag ), # Copied from matched fat jet
    NTupleVariable("n_subjettiness", lambda x: x.n_subjettiness ), # Calculated
    NTupleVariable("n_subjettiness_groomed", lambda x: x.n_subjettiness_groomed ), # Calculated
    NTupleVariable("delRopt", lambda x: x.delRopt ),             # Calculated
])

higgsType = NTupleObjectType("higgsType", variables = [
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("mass", lambda x: x.mass ),
    NTupleVariable("tau1", lambda x: x.tau1 ),
    NTupleVariable("tau2", lambda x: x.tau2 ),
    NTupleVariable("tau3", lambda x: x.tau3 ),
    NTupleVariable("bbtag", lambda x: x.bbtag ),
    NTupleVariable("mass_softdrop", lambda x: x.mass_softdrop, help="mass of the matched softdrop jet" ),
    NTupleVariable("mass_softdropz2b1", lambda x: x.mass_softdropz2b1, help="mass of the matched softdropz2b1 jet" ),
    NTupleVariable("mass_pruned", lambda x: x.mass_pruned, help="mass of the matched pruned jet" ),
    NTupleVariable("n_subjettiness", lambda x: x.n_subjettiness ),
    NTupleVariable("dr_top", lambda x: getattr(x, "dr_top", -1), help="deltaR to the best HTT candidate"),
    NTupleVariable("dr_genHiggs", lambda x: getattr(x, "dr_genHiggs", -1), help="deltaR to gen higgs"),
])

FatjetCA15ungroomedType = NTupleObjectType("FatjetCA15ungroomedType", variables = [
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("mass", lambda x: x.mass ),
    NTupleVariable("tau1", lambda x: x.tau1 ),
    NTupleVariable("tau2", lambda x: x.tau2 ),
    NTupleVariable("tau3", lambda x: x.tau3 ),
    NTupleVariable("bbtag", lambda x: x.bbtag ),
])

FatjetCA15prunedType = NTupleObjectType("FatjetCA15prunedType", variables = [
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("mass", lambda x: x.mass ),
])

SubjetCA15prunedType = NTupleObjectType("SubjetCA15prunedType", variables = [
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("mass", lambda x: x.mass ),
    NTupleVariable("btag", lambda x: x.btag ),
])

def getTreeProducer(conf):
    #Create the output TTree writer
    #Here we define all the variables that we want to save in the output TTree
    treeProducer = cfg.Analyzer(
        class_object = AutoFillTreeProducer,
        verbose = False,
        vectorTree = True,
        globalVariables = [

            # Used by Subjet Analyzer
            NTupleVariable(
                "n_bjets",
                lambda ev: getattr(ev, "n_bjets_nominal", -1),
                help="Number of selected bjets in event"
            ),

            NTupleVariable(
                "n_ljets",
                lambda ev: getattr(ev, "n_ljets_nominal", -1),
                help="Number of selected ljets in event"
            ),

            NTupleVariable(
                "n_boosted_bjets",
                lambda ev: getattr(ev, "n_boosted_bjets_nominal", -1),
                help="Number of selected bjets in subjet-modified bjet list"
            ),

            NTupleVariable(
                "n_boosted_ljets",
                lambda ev: getattr(ev, "n_boosted_ljets_nominal", -1),
                help="Number of selected ljets in subjet-modified ljet list"
            ),

            NTupleVariable(
                "n_excluded_bjets",
                lambda ev: getattr(ev, "n_excluded_bjets_nominal", -1),
                help="Number of excluded bjets: reco resolved b-jets that match a subjet in the HTT-candidate"
            ),

            NTupleVariable(
                "n_excluded_ljets",
                lambda ev: getattr(ev, "n_excluded_ljets_nominal", -1),
                help="Number of excluded ljets: "
            ),
            #--END OF USED BY SUBJETANALYZER--#

            NTupleVariable(
               "nGenBHiggs", lambda ev: len(getattr(ev, "b_quarks_h_nominal", [])),
               type=int,
               help="Number of generated b from higgs", mcOnly=True
            ),

            NTupleVariable(
               "nGenBTop", lambda ev: len(getattr(ev, "b_quarks_t_nominal", [])),
               type=int,
               help="Number of generated b from top", mcOnly=True
            ),

            NTupleVariable(
               "nGenQW", lambda ev: len(getattr(ev, "l_quarks_w_nominal", [])),
               type=int,
               help="Number of generated quarks from W", mcOnly=True
            ),
            
            NTupleVariable(
               "passPV", lambda ev: getattr(ev, "passPV", -1),
               type=int,
               help="First PV passes selection"
            ),

            NTupleVariable(
               "triggerDecision", lambda ev: getattr(ev, "triggerDecision", -1),
               type=int,
               help="Trigger selection"
            ),
            NTupleVariable(
               "triggerBitmask", lambda ev: getattr(ev, "triggerBitmask", -1),
               type=int,
               help="Bitmask of trigger decisions"
            ),

        ],
        globalObjects = {
           "MET_nominal" : NTupleObject("met", metType, help="Reconstructed MET"),
           "MET_gen_nominal" : NTupleObject("met_gen", metType, help="Generated MET", mcOnly=True),
           "MET_jetcorr_nominal" : NTupleObject("met_jetcorr", metType, help="Reconstructed MET, corrected to gen-level jets"),
           "MET_tt_nominal" : NTupleObject("met_ttbar_gen", metType, help="Generated MET from nu(top)"),
           "primaryVertex" : NTupleObject("pv", pvType, help="First PV"),
           "dilepton_p4" : NTupleObject("ll", p4type, help="Dilepton system"),
        },
        collections = {
        #standard dumping of objects
        #These are collections which are not variated
        #    "b_quarks_gen" : NTupleCollection("b_quarks_gen", quarkType, 5, help=""),
        #    "l_quarks_gen" : NTupleCollection("l_quarks_gen", quarkType, 3, help=""),
        #    "b_quarks_t" : NTupleCollection("GenBFromTop", quarkType, 3, help=""),
        #    "b_quarks_h" : NTupleCollection("GenBFromHiggs", quarkType, 3, help=""),
        #    "l_quarks_w" : NTupleCollection("GenQFromW", quarkType, 5, help=""),
            "GenHiggsBoson" : NTupleCollection("genHiggs", quarkType, 2, help="Generated Higgs boson"),
            "GenTop" : NTupleCollection("genTop", quarkType, 4, help="Generated top quark"),
            "FatjetCA15ungroomed" : NTupleCollection("fatjets", FatjetCA15ungroomedType, 4, help="Ungroomed CA 1.5 fat jets"),
            "good_jets_nominal" : NTupleCollection("jets", jetType, 9, help="Selected jets, pt ordered"),
            "good_leptons_nominal" : NTupleCollection("leps", leptonType, 2, help="Selected leptons"),
            
            "topCandidate_nominal": NTupleCollection("topCandidate" , topType, 4, help="Best top candidate in event"),
            "othertopCandidate_nominal": NTupleCollection("othertopCandidate", topType, 4, help=""),
            "higgsCandidate_nominal": NTupleCollection("higgsCandidate", higgsType, 4, help=""),

            #"topCandidate" : NTupleCollection("topCandidate", topType, 28, help=""),
            #"othertopCandidate" : NTupleCollection("othertopCandidate", topType, 28, help=""),
            #"higgsCandidate" : NTupleCollection("higgsCandidate", higgsType, 9, help=""),
        }
    )
    

    trignames = []
    for pathname, trigs in list(conf.trigger["trigTable"].items()) + list(conf.trigger["trigTableData"].items()):
        pathname = "HLT_" + pathname 
        if not pathname in trignames:
            trignames += [pathname]
        for tn in trigs:
            #strip the star
            tn = "HLT_BIT_" + tn[:-1]
            if not tn in trignames:
                trignames += [tn]
    
    print trignames
    for trig in trignames:
        treeProducer.globalVariables += [NTupleVariable(
            trig, lambda ev, name=trig: getattr(ev.input, name, -1), type=int, mcOnly=False
        )]
        
    for systematic in ["nominal", "raw", "JESUp", "JESDown"]:
        if not (systematic in conf.general["systematics"]):
            continue

        #scalar variables that have systematic variations
        for vtype in [
            ("is_sl",               int,        "Passes single lepton cuts"),
            ("is_dl",               int,        "Passes dilepton cuts"),
            ("is_fh",               int,        "Passes all-hadronic cuts"),
            ("Wmass",               float,      "Best reconstructed W candidate mass"),
            ("cat",                 int,        "ME category", "catn"),
            ("cat_btag",            int,        "ME category (b-tag)", "cat_btag_n"),
            ("cat_gen",             int,        "top decay category (-1 unknown, 0 single-leptonic, 1 di-leptonic, 2 fully hadronic)", "cat_gen_n"),
            ("btag_lr_4b",          float,      "4b, N-4 light, probability, 3D binning"),
            ("btag_lr_2b",          float,      "2b, N-2 Nlight probability, 3D binning"),
            #("btag_lr_4b_Rndge4t",  float,      "4b, N-4 light, probability, 3D binning, ge4t random"),
            #("btag_lr_2b_Rndge4t",  float,      "2b, N-2 Nlight probability, 3D binning, ge4t random"),
            #("btag_lr_4b_Inpge4t",  float,      "4b, N-4 light, probability, 3D binning, ge4t input"),
            #("btag_lr_2b_Inpge4t",  float,      "2b, N-2 Nlight probability, 3D binning, ge4t input"),
            #("btag_lr_4b_Rnd3t",    float,      "4b, N-4 light, probability, 3D binning, 3t   random"),
            #("btag_lr_2b_Rnd3t",    float,      "2b, N-2 Nlight probability, 3D binning, 3t   random"),
            #("btag_lr_4b_Inp3t",    float,      "4b, N-4 light, probability, 3D binning, 3t   input"),
            #("btag_lr_2b_Inp3t",    float,      "2b, N-2 Nlight probability, 3D binning, 3t   input"),

            ("btag_LR_4b_2b",        float,      ""),
            #("btag_LR_4b_2b_ded",        float,      ""),
            #("btag_LR_4b_2b_Rndge4t",float,      ""),
            #("btag_LR_4b_2b_Inpge4t",float,      ""),
            #("btag_LR_4b_2b_Rnd3t",  float,      ""),
            #("btag_LR_4b_2b_Inp3t",  float,      ""),
            ("qg_LR_flavour_4q_0q", float,      ""),
            ("qg_LR_flavour_4q_1q", float,      ""), 
            ("qg_LR_flavour_4q_2q", float,      ""),
            ("qg_LR_flavour_4q_3q", float,      ""),
            ("qg_LR_flavour_4q_0q_1q", float,      ""), 
            ("qg_LR_flavour_4q_1q_2q", float,      ""),
            ("qg_LR_flavour_4q_2q_3q", float,      ""),
            ("qg_LR_flavour_4q_0q_1q_2q", float,      ""), 
            ("qg_LR_flavour_4q_1q_2q_3q", float,      ""),
            ("qg_LR_flavour_4q_0q_1q_2q_3q", float,      ""),
            ("nBCSVM",              int,      ""),
            ("nBCSVT",              int,      ""),
            ("nBCSVL",              int,      ""),
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
            ("passes_mem",          int,        "MEM was evaluated"),
            ("tth_mva",             float,      "ttH vs tt+jets bdt"),
        ]:

            is_mc_only = False

            #Matching variables only defined for MC
            if "match" in vtype[0].lower():
                is_mc_only = True
            #only define the nominal values for data
            if systematic != "nominal":
                is_mc_only = True

            treeProducer.globalVariables += [makeGlobalVariable(vtype, systematic, mcOnly=is_mc_only)]

            syst_suffix = "_" + systematic
            syst_suffix2 = syst_suffix
            if systematic == "nominal":
                syst_suffix2 = ""
            #These are collections which are variated in a systematic loop and saved to the event in TreeVarAnalyzer
            treeProducer.collections.update({
                "mem_results_tth" + syst_suffix: NTupleCollection(
                    "mem_tth" + syst_suffix2, memType, len(conf.mem["methodOrder"]),
                    help="MEM tth results array, element per config.methodOrder", mcOnly=is_mc_only
                ),
                "mem_results_ttbb" + syst_suffix: NTupleCollection(
                    "mem_ttbb" + syst_suffix2, memType, len(conf.mem["methodOrder"]),
                    help="MEM ttbb results array, element per config.methodOrder", mcOnly=is_mc_only
                ),
                "fw_h_alljets" + syst_suffix: NTupleCollection(
                    "fw_aj" + syst_suffix2, FoxWolframType, 8,
                    help="Fox-Wolfram momenta calculated with all jets", mcOnly=is_mc_only
                ),
                "fw_h_btagjets" + syst_suffix: NTupleCollection(
                    "fw_bj" + syst_suffix2, FoxWolframType, 8,
                    help="Fox-Wolfram momenta calculated with b-tagged jets", mcOnly=is_mc_only
                ),
                "fw_h_untagjets" + syst_suffix: NTupleCollection(
                    "fw_uj" + syst_suffix2, FoxWolframType, 8,
                    help="Fox-Wolfram momenta calculated with untagged jets", mcOnly=is_mc_only
                ),
            })

            if conf.bran["enabled"]:
                for cat in conf.bran["jetCategories"].items():
                    treeProducer.globalObjects.update({ 
                            "b_rnd_results_" + cat[0] + syst_suffix: NTupleObject(
                                "bRnd_rnd_"+ cat[0] + syst_suffix2, branType,
                                help="BTagrRandomizer results (p,ntoys,pass,tag_id)", mcOnly=True
                                ),
                            "b_inp_results_" + cat[0] + syst_suffix: NTupleObject(
                                "bRnd_inp_"+ cat[0] + syst_suffix2, branType,
                                help="BTagrRandomizer input results (p,ntoys,pass,tag_id)", mcOnly=True
                                )                                                
                            })


    for systematic in ["nominal"]:
        for vtype in [
            ("weight_xs",               float,  ""),
            ("ttCls",                   int,    ""),
            ("bTagWeight",              float,  ""),
            ("bTagWeight_HFDown",       float,  ""),
            ("bTagWeight_HFUp",         float,  ""),
            ("bTagWeight_JESDown",      float,  ""),
            ("bTagWeight_JESUp",        float,  ""),
            ("bTagWeight_LFDown",       float,  ""),
            ("bTagWeight_LFUp",         float,  ""),
            ("bTagWeight_Stats1Down",   float,  ""),
            ("bTagWeight_Stats1Up",     float,  ""),
            ("bTagWeight_Stats2Down",   float,  ""),
            ("bTagWeight_Stats2Up",     float,  ""),
            ("nPU0",                    float,  ""),
            ("nPVs",                    float,  ""),
        ]:
            treeProducer.globalVariables += [makeGlobalVariable(vtype, systematic, mcOnly=True)]
    for vtype in [
        ("rho",                     float,  ""),
        ("json",                    float,  ""),
    ]:
        treeProducer.globalVariables += [makeGlobalVariable(vtype, "nominal", mcOnly=False)]
    return treeProducer
