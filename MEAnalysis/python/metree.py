import PhysicsTools.HeppyCore.framework.config as cfg
import os
from PhysicsTools.Heppy.physicsutils.BTagWeightCalculator import BTagWeightCalculator
from TTH.MEAnalysis.MEMAnalyzer import MEMPermutation

#Defines the output TTree branch structures
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer import *

#Override the default fillCoreVariables function, which
#by default looks for FWLite variables
#FIXME: this is a hack to run heppy on non-EDM formats. Better to propagate it to heppy
def fillCoreVariables(self, tr, event, isMC):
    if isMC:
        for x in ["run", "lumi", "evt", "xsec", "genWeight"]:
            tr.fill(x, getattr(event.input, x))
    else:
        for x in ["run", "lumi", "evt"]:
            tr.fill(x, getattr(event.input, x))

AutoFillTreeProducer.fillCoreVariables = fillCoreVariables
  
bweights = [
    "btagWeightCSV", "btagWeightCMVAV2"
]

for sdir in ["up", "down"]:
    for syst in ["cferr1", "cferr2", "hf", "hfstats1", "hfstats2", "jes", "lf", "lfstats1", "lfstats2"]:
        for tagger in ["CSV", "CMVAV2"]:
            bweights += ["btagWeight{0}_{1}_{2}".format(tagger, syst, sdir)]

#Specifies what to save for jets
jetType = NTupleObjectType("jetType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("id", lambda x : x.id, mcOnly=True),  
    NTupleVariable("qgl", lambda x : x.qgl),
    NTupleVariable("btagCSV", lambda x : x.btagCSV),
    NTupleVariable("btagCMVA", lambda x : x.btagCMVA),
    #NTupleVariable("btagCMVA_log", lambda x : getattr(x, "btagCMVA_log", -20), help="log-transformed btagCMVA"),
    NTupleVariable("btagFlag", lambda x : getattr(x, "btagFlag", -1), help="Jet was considered to be a b in MEM according to the algo"),
    NTupleVariable("mcFlavour", lambda x : x.mcFlavour, type=int, mcOnly=True),
    NTupleVariable("mcMatchId", lambda x : x.mcMatchId, type=int, mcOnly=True),
    NTupleVariable("hadronFlavour", lambda x : x.hadronFlavour, type=int, mcOnly=True),
    NTupleVariable("matchFlag",
        lambda x : getattr(x, "tth_match_label_numeric", -1),
        type=int,
        mcOnly=True,
        help="0 - matched to light quark from W, 1 - matched to b form top, 2 - matched to b from higgs"
    ),
    NTupleVariable("matchBfromHadT", lambda x : getattr(x, "tth_match_label_bfromhadt", -1), type=int, mcOnly=True),
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

lepton_sf_kind = [
    "SF_HLT_RunD4p2",
    "SF_HLT_RunD4p3",
    "SF_IdCutLoose",
    "SF_IdCutTight",
    "SF_IdMVALoose",
    "SF_IdMVATight",
    "SF_IsoLoose",
    "SF_IsoTight",
    "SF_trk_eta",
]

lepton_sf_kind_err = [x.replace("SF", "SFerr") for x in lepton_sf_kind]

#Specifies what to save for leptons
leptonType = NTupleObjectType("leptonType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("pdgId", lambda x : x.pdgId),
    NTupleVariable("relIso03", lambda x : x.pfRelIso03),
    NTupleVariable("relIso04", lambda x : x.pfRelIso04),
    NTupleVariable("ele_mva_id", lambda x : x.eleMVAIdSpring15Trig),
    NTupleVariable("mu_id", lambda x : 1*getattr(x, "looseIdPOG", 0) + 2*getattr(x, "tightId", 0)),
] + [NTupleVariable(sf, lambda x, sf=sf : getattr(x, sf, -1.0))
    for sf in lepton_sf_kind + lepton_sf_kind_err
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

genTopType = NTupleObjectType("genTopType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("decayMode", lambda x : x.decayMode),
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

perm_vars = [
    NTupleVariable("perm_{0}".format(i), lambda x : getattr(x, "perm_{0}".format(i)))
    for i in range(MEMPermutation.MAXOBJECTS)
]
memPermType = NTupleObjectType("memPermType", variables = [
    NTupleVariable("idx", lambda x : x.idx, type=int),
    NTupleVariable("p_mean", lambda x : x.p_mean),
    NTupleVariable("p_std", lambda x : x.p_std),
    NTupleVariable("p_tf_mean", lambda x : x.p_tf_mean),
    NTupleVariable("p_tf_std", lambda x : x.p_tf_std),
    NTupleVariable("p_me_mean", lambda x : x.p_me_mean),
    NTupleVariable("p_me_std", lambda x : x.p_me_std),
] + perm_vars)

commonMemType = NTupleObjectType("commonMemType", variables = [
    NTupleVariable("p", lambda x : x.p),
    NTupleVariable("p_sig", lambda x : x.p_sig),
    NTupleVariable("p_bkg", lambda x : x.p_bkg),
    NTupleVariable("blr_4b", lambda x : x.blr_4b),
    NTupleVariable("blr_2b", lambda x : x.blr_2b),
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

topCandidateType = NTupleObjectType("topCandidateType", variables = [
    NTupleVariable("fRec", lambda x: x.fRec ),
    NTupleVariable("Ropt", lambda x: x.Ropt ),
    NTupleVariable("RoptCalc", lambda x: x.RoptCalc ),
    NTupleVariable("ptForRoptCalc", lambda x: x.ptForRoptCalc ),
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("ptcal", lambda x: x.ptcal ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("etacal", lambda x: x.etacal ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("phical", lambda x: x.phical ),
    NTupleVariable("mass", lambda x: x.mass ),
    NTupleVariable("masscal", lambda x: x.masscal ),
    NTupleVariable("sjW1pt", lambda x: x.sjW1pt ),
    NTupleVariable("sjW1ptcal", lambda x: x.sjW1ptcal ),
    NTupleVariable("sjW1eta", lambda x: x.sjW1eta ),
    NTupleVariable("sjW1phi", lambda x: x.sjW1phi ),
    NTupleVariable("sjW1mass", lambda x: x.sjW1mass ),
    NTupleVariable("sjW1masscal", lambda x: x.sjW1masscal ),
    NTupleVariable("sjW1btag", lambda x: x.sjW1btag ),
    NTupleVariable("sjW2pt", lambda x: x.sjW2pt ),
    NTupleVariable("sjW2ptcal", lambda x: x.sjW2ptcal ),
    NTupleVariable("sjW2eta", lambda x: x.sjW2eta ),
    NTupleVariable("sjW2phi", lambda x: x.sjW2phi ),
    NTupleVariable("sjW2mass", lambda x: x.sjW2mass ),
    NTupleVariable("sjW2masscal", lambda x: x.sjW2masscal ),
    NTupleVariable("sjW2btag", lambda x: x.sjW2btag ),
    NTupleVariable("sjNonWpt", lambda x: x.sjNonWpt ),
    NTupleVariable("sjNonWptcal", lambda x: x.sjNonWptcal ),
    NTupleVariable("sjNonWeta", lambda x: x.sjNonWeta ),
    NTupleVariable("sjNonWphi", lambda x: x.sjNonWphi ),
    NTupleVariable("sjNonWmass", lambda x: x.sjNonWmass ),
    NTupleVariable("sjNonWmasscal", lambda x: x.sjNonWmasscal ),
    NTupleVariable("sjNonWbtag", lambda x: x.sjNonWbtag ),
    NTupleVariable("tau1", lambda x: x.tau1 ),   # Copied from matched fat jet
    NTupleVariable("tau2", lambda x: x.tau2 ),   # Copied from matched fat jet
    NTupleVariable("tau3", lambda x: x.tau3 ),   # Copied from matched fat jet
    NTupleVariable("bbtag", lambda x: x.bbtag ), # Copied from matched fat jet
    NTupleVariable("n_subjettiness", lambda x: x.n_subjettiness ), # Calculated
    NTupleVariable("n_subjettiness_groomed", lambda x: x.n_subjettiness_groomed ), # Calculated
    NTupleVariable("delRopt", lambda x: x.delRopt ),             # Calculated
    NTupleVariable("genTopHad_dr", lambda x: getattr(x, "genTopHad_dr", -1), help="DeltaR to the closest hadronic gen top" ),
    #NTupleVariable("genTopHad_index", lambda x: getattr(x, "genTopHad_index", -1), type=int, help="Index of the matched genTopHad" ),
])

higgsCandidateType = NTupleObjectType("higgsCandidateType", variables = [
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("mass", lambda x: x.mass ),
    NTupleVariable("tau1", lambda x: x.tau1 ),
    NTupleVariable("tau2", lambda x: x.tau2 ),
    NTupleVariable("tau3", lambda x: x.tau3 ),
    NTupleVariable("bbtag", lambda x: x.bbtag ),

    NTupleVariable("nallsubjets_softdrop", lambda x: x.nallsubjets_softdrop ),
    NTupleVariable("nallsubjets_softdropz2b1", lambda x: x.nallsubjets_softdropz2b1 ),
    NTupleVariable("nallsubjets_softdropfilt", lambda x: x.nallsubjets_softdropfilt ),
    NTupleVariable("nallsubjets_softdropz2b1filt", lambda x: x.nallsubjets_softdropz2b1filt ),
    NTupleVariable("nallsubjets_pruned", lambda x: x.nallsubjets_pruned ),
    NTupleVariable("nallsubjets_subjetfiltered", lambda x: x.nallsubjets_subjetfiltered ),

    NTupleVariable("sj1pt_softdrop",   lambda x: x.sj1pt_softdrop ),
    NTupleVariable("sj1eta_softdrop",  lambda x: x.sj1eta_softdrop ),
    NTupleVariable("sj1phi_softdrop",  lambda x: x.sj1phi_softdrop ),
    NTupleVariable("sj1mass_softdrop", lambda x: x.sj1mass_softdrop ),
    NTupleVariable("sj1btag_softdrop", lambda x: x.sj1btag_softdrop ),
    NTupleVariable("sj2pt_softdrop",   lambda x: x.sj2pt_softdrop ),
    NTupleVariable("sj2eta_softdrop",  lambda x: x.sj2eta_softdrop ),
    NTupleVariable("sj2phi_softdrop",  lambda x: x.sj2phi_softdrop ),
    NTupleVariable("sj2mass_softdrop", lambda x: x.sj2mass_softdrop ),
    NTupleVariable("sj2btag_softdrop", lambda x: x.sj2btag_softdrop ),

    NTupleVariable("sj1pt_softdropz2b1",   lambda x: x.sj1pt_softdropz2b1 ),
    NTupleVariable("sj1eta_softdropz2b1",  lambda x: x.sj1eta_softdropz2b1 ),
    NTupleVariable("sj1phi_softdropz2b1",  lambda x: x.sj1phi_softdropz2b1 ),
    NTupleVariable("sj1mass_softdropz2b1", lambda x: x.sj1mass_softdropz2b1 ),
    NTupleVariable("sj1btag_softdropz2b1", lambda x: x.sj1btag_softdropz2b1 ),
    NTupleVariable("sj2pt_softdropz2b1",   lambda x: x.sj2pt_softdropz2b1 ),
    NTupleVariable("sj2eta_softdropz2b1",  lambda x: x.sj2eta_softdropz2b1 ),
    NTupleVariable("sj2phi_softdropz2b1",  lambda x: x.sj2phi_softdropz2b1 ),
    NTupleVariable("sj2mass_softdropz2b1", lambda x: x.sj2mass_softdropz2b1 ),
    NTupleVariable("sj2btag_softdropz2b1", lambda x: x.sj2btag_softdropz2b1 ),

    NTupleVariable("sj1pt_softdropfilt",   lambda x: x.sj1pt_softdropfilt ),
    NTupleVariable("sj1eta_softdropfilt",  lambda x: x.sj1eta_softdropfilt ),
    NTupleVariable("sj1phi_softdropfilt",  lambda x: x.sj1phi_softdropfilt ),
    NTupleVariable("sj1mass_softdropfilt", lambda x: x.sj1mass_softdropfilt ),
    NTupleVariable("sj1btag_softdropfilt", lambda x: x.sj1btag_softdropfilt ),
    NTupleVariable("sj2pt_softdropfilt",   lambda x: x.sj2pt_softdropfilt ),
    NTupleVariable("sj2eta_softdropfilt",  lambda x: x.sj2eta_softdropfilt ),
    NTupleVariable("sj2phi_softdropfilt",  lambda x: x.sj2phi_softdropfilt ),
    NTupleVariable("sj2mass_softdropfilt", lambda x: x.sj2mass_softdropfilt ),
    NTupleVariable("sj2btag_softdropfilt", lambda x: x.sj2btag_softdropfilt ),

    NTupleVariable("sj1pt_softdropz2b1filt",   lambda x: x.sj1pt_softdropz2b1filt ),
    NTupleVariable("sj1eta_softdropz2b1filt",  lambda x: x.sj1eta_softdropz2b1filt ),
    NTupleVariable("sj1phi_softdropz2b1filt",  lambda x: x.sj1phi_softdropz2b1filt ),
    NTupleVariable("sj1mass_softdropz2b1filt", lambda x: x.sj1mass_softdropz2b1filt ),
    NTupleVariable("sj1btag_softdropz2b1filt", lambda x: x.sj1btag_softdropz2b1filt ),
    NTupleVariable("sj2pt_softdropz2b1filt",   lambda x: x.sj2pt_softdropz2b1filt ),
    NTupleVariable("sj2eta_softdropz2b1filt",  lambda x: x.sj2eta_softdropz2b1filt ),
    NTupleVariable("sj2phi_softdropz2b1filt",  lambda x: x.sj2phi_softdropz2b1filt ),
    NTupleVariable("sj2mass_softdropz2b1filt", lambda x: x.sj2mass_softdropz2b1filt ),
    NTupleVariable("sj2btag_softdropz2b1filt", lambda x: x.sj2btag_softdropz2b1filt ),

    NTupleVariable("sj1pt_pruned",   lambda x: x.sj1pt_pruned ),
    NTupleVariable("sj1eta_pruned",  lambda x: x.sj1eta_pruned ),
    NTupleVariable("sj1phi_pruned",  lambda x: x.sj1phi_pruned ),
    NTupleVariable("sj1mass_pruned", lambda x: x.sj1mass_pruned ),
    NTupleVariable("sj1btag_pruned", lambda x: x.sj1btag_pruned ),
    NTupleVariable("sj2pt_pruned",   lambda x: x.sj2pt_pruned ),
    NTupleVariable("sj2eta_pruned",  lambda x: x.sj2eta_pruned ),
    NTupleVariable("sj2phi_pruned",  lambda x: x.sj2phi_pruned ),
    NTupleVariable("sj2mass_pruned", lambda x: x.sj2mass_pruned ),
    NTupleVariable("sj2btag_pruned", lambda x: x.sj2btag_pruned ),

    NTupleVariable("sj1pt_subjetfiltered",   lambda x: x.sj1pt_subjetfiltered ),
    NTupleVariable("sj1eta_subjetfiltered",  lambda x: x.sj1eta_subjetfiltered ),
    NTupleVariable("sj1phi_subjetfiltered",  lambda x: x.sj1phi_subjetfiltered ),
    NTupleVariable("sj1mass_subjetfiltered", lambda x: x.sj1mass_subjetfiltered ),
    NTupleVariable("sj1btag_subjetfiltered", lambda x: x.sj1btag_subjetfiltered ),
    NTupleVariable("sj2pt_subjetfiltered",   lambda x: x.sj2pt_subjetfiltered ),
    NTupleVariable("sj2eta_subjetfiltered",  lambda x: x.sj2eta_subjetfiltered ),
    NTupleVariable("sj2phi_subjetfiltered",  lambda x: x.sj2phi_subjetfiltered ),
    NTupleVariable("sj2mass_subjetfiltered", lambda x: x.sj2mass_subjetfiltered ),
    NTupleVariable("sj2btag_subjetfiltered", lambda x: x.sj2btag_subjetfiltered ),
    NTupleVariable("sj12masspt_subjetfiltered", lambda x: x.sj12masspt_subjetfiltered ), # take leading two pt subjets for mass
    NTupleVariable("sj12massb_subjetfiltered", lambda x: x.sj12massb_subjetfiltered ), # take leading two bjet from leading three pt subjets
    NTupleVariable("sj123masspt_subjetfiltered", lambda x: x.sj123masspt_subjetfiltered ), # take leading three pt subjets for mass
    NTupleVariable("secondbtag_subjetfiltered", lambda x: x.secondbtag_subjetfiltered ), 

    NTupleVariable("sj3pt_subjetfiltered",   lambda x: x.sj3pt_subjetfiltered ),
    NTupleVariable("sj3eta_subjetfiltered",  lambda x: x.sj3eta_subjetfiltered ),
    NTupleVariable("sj3phi_subjetfiltered",  lambda x: x.sj3phi_subjetfiltered ),
    NTupleVariable("sj3mass_subjetfiltered", lambda x: x.sj3mass_subjetfiltered ),
    NTupleVariable("sj3btag_subjetfiltered", lambda x: x.sj3btag_subjetfiltered ),

    NTupleVariable("mass_softdrop", lambda x: x.mass_softdrop, help="mass of the matched softdrop jet" ),
    NTupleVariable("mass_softdropz2b1", lambda x: x.mass_softdropz2b1, help="mass of the matched softdropz2b1 jet" ),

    NTupleVariable("mass_softdropfilt", lambda x: x.mass_softdropfilt, help="mass of the matched softdropfilt jet" ),
    NTupleVariable("mass_softdropz2b1filt", lambda x: x.mass_softdropz2b1filt, help="mass of the matched softdropz2b1filt jet" ),
    NTupleVariable("mass_pruned", lambda x: x.mass_pruned, help="mass of the matched pruned jet" ),
    NTupleVariable("n_subjettiness", lambda x: x.n_subjettiness ),
    NTupleVariable("dr_top", lambda x: getattr(x, "dr_top", -1), help="deltaR to the best HTT candidate"),
    NTupleVariable("dr_genHiggs", lambda x: getattr(x, "dr_genHiggs", -1), help="deltaR to gen higgs"),
    NTupleVariable("dr_genTop", lambda x: getattr(x, "dr_genTop", -1), help="deltaR to closest gen top"),
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
            # "b_quarks_gen_nominal" : NTupleCollection("b_quarks_gen", quarkType, 5, help="generated b quarks", mcOnly=True),
            # "l_quarks_gen_nominal" : NTupleCollection("l_quarks_gen", quarkType, 3, help="generated light quarks", mcOnly=True),
            # "b_quarks_t_nominal" : NTupleCollection("GenBFromTop", quarkType, 3, help="generated b quarks from top", mcOnly=True),
            # "b_quarks_h_nominal" : NTupleCollection("GenBFromHiggs", quarkType, 3, help="generated b quarks from higgs", mcOnly=True),
            # "l_quarks_w_nominal" : NTupleCollection("GenQFromW", quarkType, 5, help="generated light quarks from W", mcOnly=True),
            "GenHiggsBoson" : NTupleCollection("genHiggs", quarkType, 2, help="Generated Higgs boson", mcOnly=True),
            "genTopLep" : NTupleCollection("genTopLep", genTopType, 2, help="Generated top quark (leptonic)", mcOnly=True),
            "genTopHad" : NTupleCollection("genTopHad", genTopType, 2, help="Generated top quark (hadronic)", mcOnly=True),

            "FatjetCA15ungroomed" : NTupleCollection("fatjets", FatjetCA15ungroomedType, 4, help="Ungroomed CA 1.5 fat jets"),
            "good_jets_nominal" : NTupleCollection("jets", jetType, 16, help="Selected resolved jets, pt ordered"),
            "good_leptons_nominal" : NTupleCollection("leps", leptonType, 2, help="Selected leptons"),
            
            "loose_jets_nominal" : NTupleCollection("loose_jets", jetType, 6, help="Additional jets with 20<pt<30"),
            
            "topCandidate_nominal": NTupleCollection("topCandidate" , topCandidateType, 1, help="Best top candidate in event. Currently chosen by max deltaR wrt. lepton"),
            "othertopCandidate_nominal": NTupleCollection("othertopCandidate", topCandidateType, 4, help="All other top candidates that pass HTTv2 cuts"),
            "topCandidatesSync_nominal": NTupleCollection("topCandidatesSync" , topCandidateType, 4, help=""),
            "higgsCandidate_nominal": NTupleCollection("higgsCandidate", higgsCandidateType, 4, help="Boosted Higgs candidates"),

        }
    )
    

    trignames = []
    for pathname, trigs in list(conf.trigger["trigTable"].items()) + list(conf.trigger["trigTableData"].items()):
        for pref in ["HLT", "HLT2"]:
            pathname = "_".join([pref, pathname])
            if not pathname in trignames:
                trignames += [pathname]
            for tn in trigs:
                #strip the star
                tn = pref + "_BIT_" + tn[:-1]
                if not tn in trignames:
                    trignames += [tn]
    print trignames 
    for trig in trignames:
        treeProducer.globalVariables += [NTupleVariable(
            trig, lambda ev, name=trig: getattr(ev.input, name, -1), type=int, mcOnly=False
        )]
        
    for systematic in ["nominal", "raw", "JESUp", "JESDown", "JERUp", "JERDown"]:
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

            #("btag_LR_4b_2b",        float,      ""),
            ("btag_LR_4b_2b_btagCMVA_log",        float,      ""),
            ("btag_LR_4b_2b_btagCMVA",        float,      ""),
            ("btag_LR_4b_2b_btagCSV",        float,      ""),
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
            ("nBCMVAM",             int,      "Number of good jets that pass cMVAv2 Medium WP"),
            ("nBCMVAT",             int,      "Number of good jets that pass cMVAv2 Tight WP"),
            ("nBCMVAL",             int,      "Number of good jets that pass cMVAv2 Loose WP"),
            ("numJets",             int,        "Total number of good jets that pass jet ID"),
            ("nMatchSimB",          int,        ""),
            ("nMatchSimC",          int,        ""),
            ("nSelected_wq",        int,        ""),
            ("nSelected_tb",        int,        ""),
            ("nSelected_hb",        int,        ""),
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
            ("common_bdt",          float,      "KIT BDT (SL/DL)"),
            ("common_bdt_withmem1", float,      "KIT BDT, MEM in 3t"),
            ("common_bdt_withmem2", float,      "KIT BDT, MEM in 3t, 4t"),
        ]:

            is_mc_only = False

            #Matching variables only defined for MC
            if "match" in vtype[0].lower() or "gen" in vtype[0].lower():
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
                "common_mem" + syst_suffix: NTupleCollection(
                    "common_mem" + syst_suffix2, commonMemType, 1,
                    help="Single common MEM result array", mcOnly=is_mc_only
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
            for hypo in conf.mem["methodsToRun"]:
                for proc in ["tth", "ttbb"]:
                    name = "mem_{0}_{1}".format(proc, hypo) 
                    treeProducer.globalObjects.update({
                        name + syst_suffix: NTupleObject(
                            name + syst_suffix2, memType,
                            help="MEM result for proc={0} hypo={1}".format(proc, hypo
                        )),
                    })
                    treeProducer.collections.update({
                        name + "_perm" + syst_suffix: NTupleCollection(
                            name + "_perm" + syst_suffix2, memPermType, 50,
                            help="MEM result permutations for proc={0} hypo={1}".format(
                                proc, hypo
                        )),
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


    for vtype in [
        ("ttCls",                   int,    "ttbar classification from GenHFHadronMatcher"),
        ("genHiggsDecayMode",       int,    ""),
        ("puWeight",                float,    ""),
        ("puWeightUp",              float,    ""),
        ("puWeightDown",            float,    ""),
        ("nPU0",                    float,  ""),
        ("nTrueInt",                int,  ""),
        ("triggerEmulationWeight",  float,  ""),
    ]:
        treeProducer.globalVariables += [makeGlobalVariable(vtype, "nominal", mcOnly=True)]
   
    for bweight in bweights:
        treeProducer.globalVariables += [
            makeGlobalVariable((bweight, float, ""), "nominal", mcOnly=True)
        ]

    for vtype in [
        ("rho",                     float,  ""),
        ("json",                    float,  ""),
        ("nPVs",                    float,  ""),
    ]:
        treeProducer.globalVariables += [makeGlobalVariable(vtype, "nominal", mcOnly=False)]
    return treeProducer
