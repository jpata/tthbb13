import ROOT, math
from TTH.MEAnalysis.VHbbTree import *
class httCandidate:
    def __init__(self, tree, n):
        self.pt = tree.httCandidates_pt[n];
        self.eta = tree.httCandidates_eta[n];
        self.phi = tree.httCandidates_phi[n];
        self.mass = tree.httCandidates_mass[n];
        self.fW = tree.httCandidates_fW[n];
        self.Rmin = tree.httCandidates_Rmin[n];
        self.RminExpected = tree.httCandidates_RminExpected[n];
        self.sjW1pt = tree.httCandidates_sjW1pt[n];
        self.sjW1eta = tree.httCandidates_sjW1eta[n];
        self.sjW1phi = tree.httCandidates_sjW1phi[n];
        self.sjW1mass = tree.httCandidates_sjW1mass[n];
        self.sjW2pt = tree.httCandidates_sjW2pt[n];
        self.sjW2eta = tree.httCandidates_sjW2eta[n];
        self.sjW2phi = tree.httCandidates_sjW2phi[n];
        self.sjW2mass = tree.httCandidates_sjW2mass[n];
        self.sjNonWpt = tree.httCandidates_sjNonWpt[n];
        self.sjNonWeta = tree.httCandidates_sjNonWeta[n];
        self.sjNonWphi = tree.httCandidates_sjNonWphi[n];
        self.sjNonWmass = tree.httCandidates_sjNonWmass[n];
    @staticmethod
    def make_array(event):
        return [httCandidate(event.input, i) for i in range(event.input.nhttCandidates)]
class GenBQuarkFromHafterISR:
    def __init__(self, tree, n):
        self.pdgId = tree.GenBQuarkFromHafterISR_pdgId[n];
        self.pt = tree.GenBQuarkFromHafterISR_pt[n];
        self.eta = tree.GenBQuarkFromHafterISR_eta[n];
        self.phi = tree.GenBQuarkFromHafterISR_phi[n];
        self.mass = tree.GenBQuarkFromHafterISR_mass[n];
        self.charge = tree.GenBQuarkFromHafterISR_charge[n];
        self.status = tree.GenBQuarkFromHafterISR_status[n];
    @staticmethod
    def make_array(event):
        return [GenBQuarkFromHafterISR(event.input, i) for i in range(event.input.nGenBQuarkFromHafterISR)]
class hJidx_sortcsv:
    def __init__(self, tree, n):
        self.hJidx_sortcsv = tree.hJidx_sortcsv[n];
    @staticmethod
    def make_array(event):
        return [hJidx_sortcsv(event.input, i) for i in range(event.input.nhJidx_sortcsv)]
class aJCidx:
    def __init__(self, tree, n):
        self.aJCidx = tree.aJCidx[n];
    @staticmethod
    def make_array(event):
        return [aJCidx(event.input, i) for i in range(event.input.naJCidx)]
class GenLepFromTop:
    def __init__(self, tree, n):
        self.pdgId = tree.GenLepFromTop_pdgId[n];
        self.pt = tree.GenLepFromTop_pt[n];
        self.eta = tree.GenLepFromTop_eta[n];
        self.phi = tree.GenLepFromTop_phi[n];
        self.mass = tree.GenLepFromTop_mass[n];
        self.charge = tree.GenLepFromTop_charge[n];
        self.status = tree.GenLepFromTop_status[n];
    @staticmethod
    def make_array(event):
        return [GenLepFromTop(event.input, i) for i in range(event.input.nGenLepFromTop)]
class GenVbosons:
    def __init__(self, tree, n):
        self.pdgId = tree.GenVbosons_pdgId[n];
        self.pt = tree.GenVbosons_pt[n];
        self.eta = tree.GenVbosons_eta[n];
        self.phi = tree.GenVbosons_phi[n];
        self.mass = tree.GenVbosons_mass[n];
        self.charge = tree.GenVbosons_charge[n];
        self.status = tree.GenVbosons_status[n];
    @staticmethod
    def make_array(event):
        return [GenVbosons(event.input, i) for i in range(event.input.nGenVbosons)]
class GenJet:
    def __init__(self, tree, n):
        self.pdgId = tree.GenJet_pdgId[n];
        self.pt = tree.GenJet_pt[n];
        self.eta = tree.GenJet_eta[n];
        self.phi = tree.GenJet_phi[n];
        self.mass = tree.GenJet_mass[n];
        self.charge = tree.GenJet_charge[n];
        self.status = tree.GenJet_status[n];
    @staticmethod
    def make_array(event):
        return [GenJet(event.input, i) for i in range(event.input.nGenJet)]
class GenHiggsBoson:
    def __init__(self, tree, n):
        self.pdgId = tree.GenHiggsBoson_pdgId[n];
        self.pt = tree.GenHiggsBoson_pt[n];
        self.eta = tree.GenHiggsBoson_eta[n];
        self.phi = tree.GenHiggsBoson_phi[n];
        self.mass = tree.GenHiggsBoson_mass[n];
        self.charge = tree.GenHiggsBoson_charge[n];
        self.status = tree.GenHiggsBoson_status[n];
    @staticmethod
    def make_array(event):
        return [GenHiggsBoson(event.input, i) for i in range(event.input.nGenHiggsBoson)]
class GenBQuarkFromH:
    def __init__(self, tree, n):
        self.pdgId = tree.GenBQuarkFromH_pdgId[n];
        self.pt = tree.GenBQuarkFromH_pt[n];
        self.eta = tree.GenBQuarkFromH_eta[n];
        self.phi = tree.GenBQuarkFromH_phi[n];
        self.mass = tree.GenBQuarkFromH_mass[n];
        self.charge = tree.GenBQuarkFromH_charge[n];
        self.status = tree.GenBQuarkFromH_status[n];
    @staticmethod
    def make_array(event):
        return [GenBQuarkFromH(event.input, i) for i in range(event.input.nGenBQuarkFromH)]
class hJCidx:
    def __init__(self, tree, n):
        self.hJCidx = tree.hJCidx[n];
    @staticmethod
    def make_array(event):
        return [hJCidx(event.input, i) for i in range(event.input.nhJCidx)]
class GenTop:
    def __init__(self, tree, n):
        self.pdgId = tree.GenTop_pdgId[n];
        self.pt = tree.GenTop_pt[n];
        self.eta = tree.GenTop_eta[n];
        self.phi = tree.GenTop_phi[n];
        self.mass = tree.GenTop_mass[n];
        self.charge = tree.GenTop_charge[n];
        self.status = tree.GenTop_status[n];
    @staticmethod
    def make_array(event):
        return [GenTop(event.input, i) for i in range(event.input.nGenTop)]
class aJidx:
    def __init__(self, tree, n):
        self.aJidx = tree.aJidx[n];
    @staticmethod
    def make_array(event):
        return [aJidx(event.input, i) for i in range(event.input.naJidx)]
class hJets:
    def __init__(self, tree, n):
        self.id = tree.hJets_id[n];
        self.puId = tree.hJets_puId[n];
        self.btagCSV = tree.hJets_btagCSV[n];
        self.btagCMVA = tree.hJets_btagCMVA[n];
        self.rawPt = tree.hJets_rawPt[n];
        self.mcPt = tree.hJets_mcPt[n];
        self.mcFlavour = tree.hJets_mcFlavour[n];
        self.mcMatchId = tree.hJets_mcMatchId[n];
        self.pt = tree.hJets_pt[n];
        self.eta = tree.hJets_eta[n];
        self.phi = tree.hJets_phi[n];
        self.mass = tree.hJets_mass[n];
        self.hadronFlavour = tree.hJets_hadronFlavour[n];
        self.btagProb = tree.hJets_btagProb[n];
        self.btagBProb = tree.hJets_btagBProb[n];
        self.btagnew = tree.hJets_btagnew[n];
        self.btagCSVV0 = tree.hJets_btagCSVV0[n];
        self.chHEF = tree.hJets_chHEF[n];
        self.neHEF = tree.hJets_neHEF[n];
        self.chEmEF = tree.hJets_chEmEF[n];
        self.neEmEF = tree.hJets_neEmEF[n];
        self.chMult = tree.hJets_chMult[n];
        self.leadTrackPt = tree.hJets_leadTrackPt[n];
        self.mcEta = tree.hJets_mcEta[n];
        self.mcPhi = tree.hJets_mcPhi[n];
        self.mcM = tree.hJets_mcM[n];
        self.leptonPdgId = tree.hJets_leptonPdgId[n];
        self.leptonPt = tree.hJets_leptonPt[n];
        self.leptonPtRel = tree.hJets_leptonPtRel[n];
        self.leptonPtRelInv = tree.hJets_leptonPtRelInv[n];
        self.leptonDeltaR = tree.hJets_leptonDeltaR[n];
        self.vtxMass = tree.hJets_vtxMass[n];
        self.vtxNtracks = tree.hJets_vtxNtracks[n];
        self.vtxPt = tree.hJets_vtxPt[n];
        self.vtx3DSig = tree.hJets_vtx3DSig[n];
        self.vtx3DVal = tree.hJets_vtx3DVal[n];
        self.vtxPosX = tree.hJets_vtxPosX[n];
        self.vtxPosY = tree.hJets_vtxPosY[n];
        self.vtxPosZ = tree.hJets_vtxPosZ[n];
    @staticmethod
    def make_array(event):
        return [hJets(event.input, i) for i in range(event.input.nhJets)]
class GenLepFromTau:
    def __init__(self, tree, n):
        self.pdgId = tree.GenLepFromTau_pdgId[n];
        self.pt = tree.GenLepFromTau_pt[n];
        self.eta = tree.GenLepFromTau_eta[n];
        self.phi = tree.GenLepFromTau_phi[n];
        self.mass = tree.GenLepFromTau_mass[n];
        self.charge = tree.GenLepFromTau_charge[n];
        self.status = tree.GenLepFromTau_status[n];
    @staticmethod
    def make_array(event):
        return [GenLepFromTau(event.input, i) for i in range(event.input.nGenLepFromTau)]
class aLeptons:
    def __init__(self, tree, n):
        self.charge = tree.aLeptons_charge[n];
        self.tightId = tree.aLeptons_tightId[n];
        self.eleCutIdCSA14_25ns_v1 = tree.aLeptons_eleCutIdCSA14_25ns_v1[n];
        self.eleCutIdCSA14_50ns_v1 = tree.aLeptons_eleCutIdCSA14_50ns_v1[n];
        self.dxy = tree.aLeptons_dxy[n];
        self.dz = tree.aLeptons_dz[n];
        self.edxy = tree.aLeptons_edxy[n];
        self.edz = tree.aLeptons_edz[n];
        self.ip3d = tree.aLeptons_ip3d[n];
        self.sip3d = tree.aLeptons_sip3d[n];
        self.convVeto = tree.aLeptons_convVeto[n];
        self.lostHits = tree.aLeptons_lostHits[n];
        self.relIso03 = tree.aLeptons_relIso03[n];
        self.relIso04 = tree.aLeptons_relIso04[n];
        self.tightCharge = tree.aLeptons_tightCharge[n];
        self.mcMatchId = tree.aLeptons_mcMatchId[n];
        self.mcMatchAny = tree.aLeptons_mcMatchAny[n];
        self.mcMatchTau = tree.aLeptons_mcMatchTau[n];
        self.pdgId = tree.aLeptons_pdgId[n];
        self.pt = tree.aLeptons_pt[n];
        self.eta = tree.aLeptons_eta[n];
        self.phi = tree.aLeptons_phi[n];
        self.mass = tree.aLeptons_mass[n];
        self.looseIdSusy = tree.aLeptons_looseIdSusy[n];
        self.looseIdPOG = tree.aLeptons_looseIdPOG[n];
        self.chargedHadRelIso03 = tree.aLeptons_chargedHadRelIso03[n];
        self.chargedHadRelIso04 = tree.aLeptons_chargedHadRelIso04[n];
        self.nStations = tree.aLeptons_nStations[n];
        self.trkKink = tree.aLeptons_trkKink[n];
        self.caloCompatibility = tree.aLeptons_caloCompatibility[n];
        self.globalTrackChi2 = tree.aLeptons_globalTrackChi2[n];
        self.trackerLayers = tree.aLeptons_trackerLayers[n];
        self.pixelLayers = tree.aLeptons_pixelLayers[n];
        self.mvaTTH = tree.aLeptons_mvaTTH[n];
        self.jetPtRatio = tree.aLeptons_jetPtRatio[n];
        self.jetBTagCSV = tree.aLeptons_jetBTagCSV[n];
        self.jetDR = tree.aLeptons_jetDR[n];
    @staticmethod
    def make_array(event):
        return [aLeptons(event.input, i) for i in range(event.input.naLeptons)]
class aJets:
    def __init__(self, tree, n):
        self.id = tree.aJets_id[n];
        self.puId = tree.aJets_puId[n];
        self.btagCSV = tree.aJets_btagCSV[n];
        self.btagCMVA = tree.aJets_btagCMVA[n];
        self.rawPt = tree.aJets_rawPt[n];
        self.mcPt = tree.aJets_mcPt[n];
        self.mcFlavour = tree.aJets_mcFlavour[n];
        self.mcMatchId = tree.aJets_mcMatchId[n];
        self.pt = tree.aJets_pt[n];
        self.eta = tree.aJets_eta[n];
        self.phi = tree.aJets_phi[n];
        self.mass = tree.aJets_mass[n];
        self.hadronFlavour = tree.aJets_hadronFlavour[n];
        self.btagProb = tree.aJets_btagProb[n];
        self.btagBProb = tree.aJets_btagBProb[n];
        self.btagnew = tree.aJets_btagnew[n];
        self.btagCSVV0 = tree.aJets_btagCSVV0[n];
        self.chHEF = tree.aJets_chHEF[n];
        self.neHEF = tree.aJets_neHEF[n];
        self.chEmEF = tree.aJets_chEmEF[n];
        self.neEmEF = tree.aJets_neEmEF[n];
        self.chMult = tree.aJets_chMult[n];
        self.leadTrackPt = tree.aJets_leadTrackPt[n];
        self.mcEta = tree.aJets_mcEta[n];
        self.mcPhi = tree.aJets_mcPhi[n];
        self.mcM = tree.aJets_mcM[n];
        self.leptonPdgId = tree.aJets_leptonPdgId[n];
        self.leptonPt = tree.aJets_leptonPt[n];
        self.leptonPtRel = tree.aJets_leptonPtRel[n];
        self.leptonPtRelInv = tree.aJets_leptonPtRelInv[n];
        self.leptonDeltaR = tree.aJets_leptonDeltaR[n];
        self.vtxMass = tree.aJets_vtxMass[n];
        self.vtxNtracks = tree.aJets_vtxNtracks[n];
        self.vtxPt = tree.aJets_vtxPt[n];
        self.vtx3DSig = tree.aJets_vtx3DSig[n];
        self.vtx3DVal = tree.aJets_vtx3DVal[n];
        self.vtxPosX = tree.aJets_vtxPosX[n];
        self.vtxPosY = tree.aJets_vtxPosY[n];
        self.vtxPosZ = tree.aJets_vtxPosZ[n];
    @staticmethod
    def make_array(event):
        return [aJets(event.input, i) for i in range(event.input.naJets)]
class selLeptons:
    def __init__(self, tree, n):
        self.charge = tree.selLeptons_charge[n];
        self.tightId = tree.selLeptons_tightId[n];
        self.eleCutIdCSA14_25ns_v1 = tree.selLeptons_eleCutIdCSA14_25ns_v1[n];
        self.eleCutIdCSA14_50ns_v1 = tree.selLeptons_eleCutIdCSA14_50ns_v1[n];
        self.dxy = tree.selLeptons_dxy[n];
        self.dz = tree.selLeptons_dz[n];
        self.edxy = tree.selLeptons_edxy[n];
        self.edz = tree.selLeptons_edz[n];
        self.ip3d = tree.selLeptons_ip3d[n];
        self.sip3d = tree.selLeptons_sip3d[n];
        self.convVeto = tree.selLeptons_convVeto[n];
        self.lostHits = tree.selLeptons_lostHits[n];
        self.relIso03 = tree.selLeptons_relIso03[n];
        self.relIso04 = tree.selLeptons_relIso04[n];
        self.tightCharge = tree.selLeptons_tightCharge[n];
        self.mcMatchId = tree.selLeptons_mcMatchId[n];
        self.mcMatchAny = tree.selLeptons_mcMatchAny[n];
        self.mcMatchTau = tree.selLeptons_mcMatchTau[n];
        self.pdgId = tree.selLeptons_pdgId[n];
        self.pt = tree.selLeptons_pt[n];
        self.eta = tree.selLeptons_eta[n];
        self.phi = tree.selLeptons_phi[n];
        self.mass = tree.selLeptons_mass[n];
        self.looseIdSusy = tree.selLeptons_looseIdSusy[n];
        self.looseIdPOG = tree.selLeptons_looseIdPOG[n];
        self.chargedHadRelIso03 = tree.selLeptons_chargedHadRelIso03[n];
        self.chargedHadRelIso04 = tree.selLeptons_chargedHadRelIso04[n];
        self.nStations = tree.selLeptons_nStations[n];
        self.trkKink = tree.selLeptons_trkKink[n];
        self.caloCompatibility = tree.selLeptons_caloCompatibility[n];
        self.globalTrackChi2 = tree.selLeptons_globalTrackChi2[n];
        self.trackerLayers = tree.selLeptons_trackerLayers[n];
        self.pixelLayers = tree.selLeptons_pixelLayers[n];
        self.mvaTTH = tree.selLeptons_mvaTTH[n];
        self.jetPtRatio = tree.selLeptons_jetPtRatio[n];
        self.jetBTagCSV = tree.selLeptons_jetBTagCSV[n];
        self.jetDR = tree.selLeptons_jetDR[n];
    @staticmethod
    def make_array(event):
        return [selLeptons(event.input, i) for i in range(event.input.nselLeptons)]
class hJ3Cidx:
    def __init__(self, tree, n):
        self.hJ3Cidx = tree.hJ3Cidx[n];
    @staticmethod
    def make_array(event):
        return [hJ3Cidx(event.input, i) for i in range(event.input.nhJ3Cidx)]
class hJidx:
    def __init__(self, tree, n):
        self.hJidx = tree.hJidx[n];
    @staticmethod
    def make_array(event):
        return [hJidx(event.input, i) for i in range(event.input.nhJidx)]
class TauGood:
    def __init__(self, tree, n):
        self.pdgId = tree.TauGood_pdgId[n];
        self.pt = tree.TauGood_pt[n];
        self.eta = tree.TauGood_eta[n];
        self.phi = tree.TauGood_phi[n];
        self.mass = tree.TauGood_mass[n];
        self.charge = tree.TauGood_charge[n];
        self.decayMode = tree.TauGood_decayMode[n];
        self.idDecayMode = tree.TauGood_idDecayMode[n];
        self.idDecayModeNewDMs = tree.TauGood_idDecayModeNewDMs[n];
        self.dxy = tree.TauGood_dxy[n];
        self.dz = tree.TauGood_dz[n];
        self.idMVA = tree.TauGood_idMVA[n];
        self.idMVANewDM = tree.TauGood_idMVANewDM[n];
        self.idCI3hit = tree.TauGood_idCI3hit[n];
        self.idAntiMu = tree.TauGood_idAntiMu[n];
        self.idAntiE = tree.TauGood_idAntiE[n];
        self.isoCI3hit = tree.TauGood_isoCI3hit[n];
        self.mcMatchId = tree.TauGood_mcMatchId[n];
    @staticmethod
    def make_array(event):
        return [TauGood(event.input, i) for i in range(event.input.nTauGood)]
class GenLep:
    def __init__(self, tree, n):
        self.pdgId = tree.GenLep_pdgId[n];
        self.pt = tree.GenLep_pt[n];
        self.eta = tree.GenLep_eta[n];
        self.phi = tree.GenLep_phi[n];
        self.mass = tree.GenLep_mass[n];
        self.charge = tree.GenLep_charge[n];
        self.status = tree.GenLep_status[n];
    @staticmethod
    def make_array(event):
        return [GenLep(event.input, i) for i in range(event.input.nGenLep)]
class Jet:
    def __init__(self, tree, n):
        self.id = tree.Jet_id[n];
        self.puId = tree.Jet_puId[n];
        self.btagCSV = tree.Jet_btagCSV[n];
        self.btagCMVA = tree.Jet_btagCMVA[n];
        self.rawPt = tree.Jet_rawPt[n];
        self.mcPt = tree.Jet_mcPt[n];
        self.mcFlavour = tree.Jet_mcFlavour[n];
        self.mcMatchId = tree.Jet_mcMatchId[n];
        self.pt = tree.Jet_pt[n];
        self.eta = tree.Jet_eta[n];
        self.phi = tree.Jet_phi[n];
        self.mass = tree.Jet_mass[n];
        self.hadronFlavour = tree.Jet_hadronFlavour[n];
        self.btagProb = tree.Jet_btagProb[n];
        self.btagBProb = tree.Jet_btagBProb[n];
        self.btagnew = tree.Jet_btagnew[n];
        self.btagCSVV0 = tree.Jet_btagCSVV0[n];
        self.chHEF = tree.Jet_chHEF[n];
        self.neHEF = tree.Jet_neHEF[n];
        self.chEmEF = tree.Jet_chEmEF[n];
        self.neEmEF = tree.Jet_neEmEF[n];
        self.chMult = tree.Jet_chMult[n];
        self.leadTrackPt = tree.Jet_leadTrackPt[n];
        self.mcEta = tree.Jet_mcEta[n];
        self.mcPhi = tree.Jet_mcPhi[n];
        self.mcM = tree.Jet_mcM[n];
        self.leptonPdgId = tree.Jet_leptonPdgId[n];
        self.leptonPt = tree.Jet_leptonPt[n];
        self.leptonPtRel = tree.Jet_leptonPtRel[n];
        self.leptonPtRelInv = tree.Jet_leptonPtRelInv[n];
        self.leptonDeltaR = tree.Jet_leptonDeltaR[n];
        self.vtxMass = tree.Jet_vtxMass[n];
        self.vtxNtracks = tree.Jet_vtxNtracks[n];
        self.vtxPt = tree.Jet_vtxPt[n];
        self.vtx3DSig = tree.Jet_vtx3DSig[n];
        self.vtx3DVal = tree.Jet_vtx3DVal[n];
        self.vtxPosX = tree.Jet_vtxPosX[n];
        self.vtxPosY = tree.Jet_vtxPosY[n];
        self.vtxPosZ = tree.Jet_vtxPosZ[n];
    @staticmethod
    def make_array(event):
        return [Jet(event.input, i) for i in range(event.input.nJet)]
class vLeptons:
    def __init__(self, tree, n):
        self.charge = tree.vLeptons_charge[n];
        self.tightId = tree.vLeptons_tightId[n];
        self.eleCutIdCSA14_25ns_v1 = tree.vLeptons_eleCutIdCSA14_25ns_v1[n];
        self.eleCutIdCSA14_50ns_v1 = tree.vLeptons_eleCutIdCSA14_50ns_v1[n];
        self.dxy = tree.vLeptons_dxy[n];
        self.dz = tree.vLeptons_dz[n];
        self.edxy = tree.vLeptons_edxy[n];
        self.edz = tree.vLeptons_edz[n];
        self.ip3d = tree.vLeptons_ip3d[n];
        self.sip3d = tree.vLeptons_sip3d[n];
        self.convVeto = tree.vLeptons_convVeto[n];
        self.lostHits = tree.vLeptons_lostHits[n];
        self.relIso03 = tree.vLeptons_relIso03[n];
        self.relIso04 = tree.vLeptons_relIso04[n];
        self.tightCharge = tree.vLeptons_tightCharge[n];
        self.mcMatchId = tree.vLeptons_mcMatchId[n];
        self.mcMatchAny = tree.vLeptons_mcMatchAny[n];
        self.mcMatchTau = tree.vLeptons_mcMatchTau[n];
        self.pdgId = tree.vLeptons_pdgId[n];
        self.pt = tree.vLeptons_pt[n];
        self.eta = tree.vLeptons_eta[n];
        self.phi = tree.vLeptons_phi[n];
        self.mass = tree.vLeptons_mass[n];
        self.looseIdSusy = tree.vLeptons_looseIdSusy[n];
        self.looseIdPOG = tree.vLeptons_looseIdPOG[n];
        self.chargedHadRelIso03 = tree.vLeptons_chargedHadRelIso03[n];
        self.chargedHadRelIso04 = tree.vLeptons_chargedHadRelIso04[n];
        self.nStations = tree.vLeptons_nStations[n];
        self.trkKink = tree.vLeptons_trkKink[n];
        self.caloCompatibility = tree.vLeptons_caloCompatibility[n];
        self.globalTrackChi2 = tree.vLeptons_globalTrackChi2[n];
        self.trackerLayers = tree.vLeptons_trackerLayers[n];
        self.pixelLayers = tree.vLeptons_pixelLayers[n];
        self.mvaTTH = tree.vLeptons_mvaTTH[n];
        self.jetPtRatio = tree.vLeptons_jetPtRatio[n];
        self.jetBTagCSV = tree.vLeptons_jetBTagCSV[n];
        self.jetDR = tree.vLeptons_jetDR[n];
    @staticmethod
    def make_array(event):
        return [vLeptons(event.input, i) for i in range(event.input.nvLeptons)]
class aJ3Cidx:
    def __init__(self, tree, n):
        self.aJ3Cidx = tree.aJ3Cidx[n];
    @staticmethod
    def make_array(event):
        return [aJ3Cidx(event.input, i) for i in range(event.input.naJ3Cidx)]
class GenWZQuark:
    def __init__(self, tree, n):
        self.pdgId = tree.GenWZQuark_pdgId[n];
        self.pt = tree.GenWZQuark_pt[n];
        self.eta = tree.GenWZQuark_eta[n];
        self.phi = tree.GenWZQuark_phi[n];
        self.mass = tree.GenWZQuark_mass[n];
        self.charge = tree.GenWZQuark_charge[n];
        self.status = tree.GenWZQuark_status[n];
    @staticmethod
    def make_array(event):
        return [GenWZQuark(event.input, i) for i in range(event.input.nGenWZQuark)]
class GenBQuarkFromTop:
    def __init__(self, tree, n):
        self.pdgId = tree.GenBQuarkFromTop_pdgId[n];
        self.pt = tree.GenBQuarkFromTop_pt[n];
        self.eta = tree.GenBQuarkFromTop_eta[n];
        self.phi = tree.GenBQuarkFromTop_phi[n];
        self.mass = tree.GenBQuarkFromTop_mass[n];
        self.charge = tree.GenBQuarkFromTop_charge[n];
        self.status = tree.GenBQuarkFromTop_status[n];
    @staticmethod
    def make_array(event):
        return [GenBQuarkFromTop(event.input, i) for i in range(event.input.nGenBQuarkFromTop)]

class GenNuFromTop:
    def __init__(self, tree, n):
        self.pdgId = tree.GenNuFromTop_pdgId[n];
        self.pt = tree.GenNuFromTop_pt[n];
        self.eta = tree.GenNuFromTop_eta[n];
        self.phi = tree.GenNuFromTop_phi[n];
        self.mass = tree.GenNuFromTop_mass[n];
        self.charge = tree.GenNuFromTop_charge[n];
        self.status = tree.GenNuFromTop_status[n];
    @staticmethod
    def make_array(event):
        return [GenNuFromTop(event.input, i) for i in range(event.input.nGenNuFromTop)]

class MET:
    def __init__(self, **kwargs):
        self.p4 = ROOT.TLorentzVector()

        _px, _py = kwargs.get("px", None), kwargs.get("py", None)
        _pt, _phi = kwargs.get("pt", None), kwargs.get("phi", None)
        tree = kwargs.get("tree", None)

        self.sumEt = 0
        self.genPt = 0
        self.genPhi = 0

        if not (_px is None or _py is None):
            self.p4.SetPxPyPzE(_px, _py, 0, math.sqrt(_px*_px + _py*_py))
        elif not (_pt is None or _phi is None):
            self.p4.SetPtEtaPhiM(_pt, 0, _phi, 0)

        elif tree != None:
            self.pt = tree.met_pt;
            self.phi = tree.met_phi;
            self.sumEt = tree.met_sumEt;
            self.genPt = tree.met_genPt;
            self.genPhi = tree.met_genPhi;
            self.p4.SetPtEtaPhiM(self.pt, 0, self.phi, 0)

        self.pt = self.p4.Pt()
        self.phi = self.p4.Phi()
        self.px = self.p4.Px()
        self.py = self.p4.Py()

    @staticmethod
    def make_array(event):
        return [MET(tree=event.input)]

from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
class EventAnalyzer(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
    def process(self, event):
        #event.GenBQuarkFromHafterISR = GenBQuarkFromHafterISR.make_array(event)
        #event.hJidx_sortcsv = hJidx_sortcsv.make_array(event)
        #event.aJCidx = aJCidx.make_array(event)
        event.GenLepFromTop = GenLepFromTop.make_array(event)
        #event.GenVbosons = GenVbosons.make_array(event)
        #event.GenJet = GenJet.make_array(event)
        #event.GenHiggsBoson = GenHiggsBoson.make_array(event)
        event.GenBQuarkFromH = GenBQuarkFromH.make_array(event)
        #event.hJCidx = hJCidx.make_array(event)
        #event.GenTop = GenTop.make_array(event)
        #event.aJidx = aJidx.make_array(event)
        #event.hJets = hJets.make_array(event)
        #event.GenLepFromTau = GenLepFromTau.make_array(event)
        #event.aLeptons = aLeptons.make_array(event)
        #event.aJets = aJets.make_array(event)
        event.selLeptons = selLeptons.make_array(event)
        #event.hJ3Cidx = hJ3Cidx.make_array(event)
        #event.hJidx = hJidx.make_array(event)
        #event.TauGood = TauGood.make_array(event)
        #event.GenLep = GenLep.make_array(event)
        event.Jet = Jet.make_array(event)
        #event.vLeptons = vLeptons.make_array(event)
        #event.aJ3Cidx = aJ3Cidx.make_array(event)
        event.GenWZQuark = GenWZQuark.make_array(event)
        event.GenBQuarkFromTop = GenBQuarkFromTop.make_array(event)
        event.GenNuFromTop = GenNuFromTop.make_array(event)
        event.httCandidate = httCandidate.make_array(event)

        event.met = MET.make_array(event)

def lvec(self):
    """
    Converts an object with pt, eta, phi, mass to a TLorentzVector
    """
    lv = ROOT.TLorentzVector()
    lv.SetPtEtaPhiM(self.pt, self.eta, self.phi, self.mass)
    return lv
