class GenBQuarkFromHafterISR:
    """
    Generated bottom quarks from Higgs decays
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenBQuarkFromHafterISR", 0)
        _pdgId = getattr(tree, "GenBQuarkFromHafterISR_pdgId", [None]*n)
        _pt = getattr(tree, "GenBQuarkFromHafterISR_pt", [None]*n)
        _eta = getattr(tree, "GenBQuarkFromHafterISR_eta", [None]*n)
        _phi = getattr(tree, "GenBQuarkFromHafterISR_phi", [None]*n)
        _mass = getattr(tree, "GenBQuarkFromHafterISR_mass", [None]*n)
        _charge = getattr(tree, "GenBQuarkFromHafterISR_charge", [None]*n)
        _status = getattr(tree, "GenBQuarkFromHafterISR_status", [None]*n)
        return [GenBQuarkFromHafterISR(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class GenHiggsBoson:
    """
    Generated Higgs boson 
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenHiggsBoson", 0)
        _pdgId = getattr(tree, "GenHiggsBoson_pdgId", [None]*n)
        _pt = getattr(tree, "GenHiggsBoson_pt", [None]*n)
        _eta = getattr(tree, "GenHiggsBoson_eta", [None]*n)
        _phi = getattr(tree, "GenHiggsBoson_phi", [None]*n)
        _mass = getattr(tree, "GenHiggsBoson_mass", [None]*n)
        _charge = getattr(tree, "GenHiggsBoson_charge", [None]*n)
        _status = getattr(tree, "GenHiggsBoson_status", [None]*n)
        return [GenHiggsBoson(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class hJidx_sortcsv:
    """
    Higgs jet indices within hJets with CSV sorting 
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nhJidx_sortcsv", 0)
        _hJidx_sortcsv = getattr(tree, "hJidx_sortcsv", [None]*n);
        return [hJidx_sortcsv(_hJidx_sortcsv[n]) for n in range(n)]
    def __init__(self, hJidx_sortcsv):
        self.hJidx_sortcsv = hJidx_sortcsv #Higgs jet indices within hJets with CSV sorting 
class aJCidx:
    """
    additional jet indices CSV
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "naJCidx", 0)
        _aJCidx = getattr(tree, "aJCidx", [None]*n);
        return [aJCidx(_aJCidx[n]) for n in range(n)]
    def __init__(self, aJCidx):
        self.aJCidx = aJCidx #additional jet indices CSV
class GenLepFromTop:
    """
    Generated leptons from t->W decays
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenLepFromTop", 0)
        _pdgId = getattr(tree, "GenLepFromTop_pdgId", [None]*n)
        _pt = getattr(tree, "GenLepFromTop_pt", [None]*n)
        _eta = getattr(tree, "GenLepFromTop_eta", [None]*n)
        _phi = getattr(tree, "GenLepFromTop_phi", [None]*n)
        _mass = getattr(tree, "GenLepFromTop_mass", [None]*n)
        _charge = getattr(tree, "GenLepFromTop_charge", [None]*n)
        _status = getattr(tree, "GenLepFromTop_status", [None]*n)
        return [GenLepFromTop(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class GenVbosons:
    """
    Generated W or Z bosons, mass > 30
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenVbosons", 0)
        _pdgId = getattr(tree, "GenVbosons_pdgId", [None]*n)
        _pt = getattr(tree, "GenVbosons_pt", [None]*n)
        _eta = getattr(tree, "GenVbosons_eta", [None]*n)
        _phi = getattr(tree, "GenVbosons_phi", [None]*n)
        _mass = getattr(tree, "GenVbosons_mass", [None]*n)
        _charge = getattr(tree, "GenVbosons_charge", [None]*n)
        _status = getattr(tree, "GenVbosons_status", [None]*n)
        return [GenVbosons(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class GenBQuarkFromH:
    """
    Generated bottom quarks from Higgs decays
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenBQuarkFromH", 0)
        _pdgId = getattr(tree, "GenBQuarkFromH_pdgId", [None]*n)
        _pt = getattr(tree, "GenBQuarkFromH_pt", [None]*n)
        _eta = getattr(tree, "GenBQuarkFromH_eta", [None]*n)
        _phi = getattr(tree, "GenBQuarkFromH_phi", [None]*n)
        _mass = getattr(tree, "GenBQuarkFromH_mass", [None]*n)
        _charge = getattr(tree, "GenBQuarkFromH_charge", [None]*n)
        _status = getattr(tree, "GenBQuarkFromH_status", [None]*n)
        return [GenBQuarkFromH(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class hJCidx:
    """
    Higgs jet indices CSV
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nhJCidx", 0)
        _hJCidx = getattr(tree, "hJCidx", [None]*n);
        return [hJCidx(_hJCidx[n]) for n in range(n)]
    def __init__(self, hJCidx):
        self.hJCidx = hJCidx #Higgs jet indices CSV
class GenTop:
    """
    Generated top quarks from hard scattering
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenTop", 0)
        _pdgId = getattr(tree, "GenTop_pdgId", [None]*n)
        _pt = getattr(tree, "GenTop_pt", [None]*n)
        _eta = getattr(tree, "GenTop_eta", [None]*n)
        _phi = getattr(tree, "GenTop_phi", [None]*n)
        _mass = getattr(tree, "GenTop_mass", [None]*n)
        _charge = getattr(tree, "GenTop_charge", [None]*n)
        _status = getattr(tree, "GenTop_status", [None]*n)
        return [GenTop(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class aJidx:
    """
    additional jet indices
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "naJidx", 0)
        _aJidx = getattr(tree, "aJidx", [None]*n);
        return [aJidx(_aJidx[n]) for n in range(n)]
    def __init__(self, aJidx):
        self.aJidx = aJidx #additional jet indices
class GenLepFromTau:
    """
    Generated leptons from decays of taus from W/Z decays
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenLepFromTau", 0)
        _pdgId = getattr(tree, "GenLepFromTau_pdgId", [None]*n)
        _pt = getattr(tree, "GenLepFromTau_pt", [None]*n)
        _eta = getattr(tree, "GenLepFromTau_eta", [None]*n)
        _phi = getattr(tree, "GenLepFromTau_phi", [None]*n)
        _mass = getattr(tree, "GenLepFromTau_mass", [None]*n)
        _charge = getattr(tree, "GenLepFromTau_charge", [None]*n)
        _status = getattr(tree, "GenLepFromTau_status", [None]*n)
        return [GenLepFromTau(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class aLeptons:
    """
    Additional leptons, not passing the preselection
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "naLeptons", 0)
        _charge = getattr(tree, "aLeptons_charge", [None]*n)
        _tightId = getattr(tree, "aLeptons_tightId", [None]*n)
        _eleCutIdCSA14_25ns_v1 = getattr(tree, "aLeptons_eleCutIdCSA14_25ns_v1", [None]*n)
        _eleCutIdCSA14_50ns_v1 = getattr(tree, "aLeptons_eleCutIdCSA14_50ns_v1", [None]*n)
        _dxy = getattr(tree, "aLeptons_dxy", [None]*n)
        _dz = getattr(tree, "aLeptons_dz", [None]*n)
        _edxy = getattr(tree, "aLeptons_edxy", [None]*n)
        _edz = getattr(tree, "aLeptons_edz", [None]*n)
        _ip3d = getattr(tree, "aLeptons_ip3d", [None]*n)
        _sip3d = getattr(tree, "aLeptons_sip3d", [None]*n)
        _convVeto = getattr(tree, "aLeptons_convVeto", [None]*n)
        _lostHits = getattr(tree, "aLeptons_lostHits", [None]*n)
        _relIso03 = getattr(tree, "aLeptons_relIso03", [None]*n)
        _relIso04 = getattr(tree, "aLeptons_relIso04", [None]*n)
        _tightCharge = getattr(tree, "aLeptons_tightCharge", [None]*n)
        _mcMatchId = getattr(tree, "aLeptons_mcMatchId", [None]*n)
        _mcMatchAny = getattr(tree, "aLeptons_mcMatchAny", [None]*n)
        _mcMatchTau = getattr(tree, "aLeptons_mcMatchTau", [None]*n)
        _mcPt = getattr(tree, "aLeptons_mcPt", [None]*n)
        _pdgId = getattr(tree, "aLeptons_pdgId", [None]*n)
        _pt = getattr(tree, "aLeptons_pt", [None]*n)
        _eta = getattr(tree, "aLeptons_eta", [None]*n)
        _phi = getattr(tree, "aLeptons_phi", [None]*n)
        _mass = getattr(tree, "aLeptons_mass", [None]*n)
        _looseIdSusy = getattr(tree, "aLeptons_looseIdSusy", [None]*n)
        _looseIdPOG = getattr(tree, "aLeptons_looseIdPOG", [None]*n)
        _chargedHadRelIso03 = getattr(tree, "aLeptons_chargedHadRelIso03", [None]*n)
        _chargedHadRelIso04 = getattr(tree, "aLeptons_chargedHadRelIso04", [None]*n)
        _eleSieie = getattr(tree, "aLeptons_eleSieie", [None]*n)
        _eleDEta = getattr(tree, "aLeptons_eleDEta", [None]*n)
        _eleDPhi = getattr(tree, "aLeptons_eleDPhi", [None]*n)
        _eleHoE = getattr(tree, "aLeptons_eleHoE", [None]*n)
        _eleMissingHits = getattr(tree, "aLeptons_eleMissingHits", [None]*n)
        _eleChi2 = getattr(tree, "aLeptons_eleChi2", [None]*n)
        _nMuonHits = getattr(tree, "aLeptons_nMuonHits", [None]*n)
        _nStations = getattr(tree, "aLeptons_nStations", [None]*n)
        _trkKink = getattr(tree, "aLeptons_trkKink", [None]*n)
        _caloCompatibility = getattr(tree, "aLeptons_caloCompatibility", [None]*n)
        _globalTrackChi2 = getattr(tree, "aLeptons_globalTrackChi2", [None]*n)
        _nChamberHits = getattr(tree, "aLeptons_nChamberHits", [None]*n)
        _isPFMuon = getattr(tree, "aLeptons_isPFMuon", [None]*n)
        _isGlobalMuon = getattr(tree, "aLeptons_isGlobalMuon", [None]*n)
        _isTrackerMuon = getattr(tree, "aLeptons_isTrackerMuon", [None]*n)
        _pixelHits = getattr(tree, "aLeptons_pixelHits", [None]*n)
        _trackerLayers = getattr(tree, "aLeptons_trackerLayers", [None]*n)
        _pixelLayers = getattr(tree, "aLeptons_pixelLayers", [None]*n)
        _mvaTTH = getattr(tree, "aLeptons_mvaTTH", [None]*n)
        _jetOverlapIdx = getattr(tree, "aLeptons_jetOverlapIdx", [None]*n)
        _jetPtRatio = getattr(tree, "aLeptons_jetPtRatio", [None]*n)
        _jetBTagCSV = getattr(tree, "aLeptons_jetBTagCSV", [None]*n)
        _jetDR = getattr(tree, "aLeptons_jetDR", [None]*n)
        _pfRelIso03 = getattr(tree, "aLeptons_pfRelIso03", [None]*n)
        _pfRelIso04 = getattr(tree, "aLeptons_pfRelIso04", [None]*n)
        _etaSc = getattr(tree, "aLeptons_etaSc", [None]*n)
        _eleExpMissingInnerHits = getattr(tree, "aLeptons_eleExpMissingInnerHits", [None]*n)
        _eleooEmooP = getattr(tree, "aLeptons_eleooEmooP", [None]*n)
        return [aLeptons(_charge[n], _tightId[n], _eleCutIdCSA14_25ns_v1[n], _eleCutIdCSA14_50ns_v1[n], _dxy[n], _dz[n], _edxy[n], _edz[n], _ip3d[n], _sip3d[n], _convVeto[n], _lostHits[n], _relIso03[n], _relIso04[n], _tightCharge[n], _mcMatchId[n], _mcMatchAny[n], _mcMatchTau[n], _mcPt[n], _pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _looseIdSusy[n], _looseIdPOG[n], _chargedHadRelIso03[n], _chargedHadRelIso04[n], _eleSieie[n], _eleDEta[n], _eleDPhi[n], _eleHoE[n], _eleMissingHits[n], _eleChi2[n], _nMuonHits[n], _nStations[n], _trkKink[n], _caloCompatibility[n], _globalTrackChi2[n], _nChamberHits[n], _isPFMuon[n], _isGlobalMuon[n], _isTrackerMuon[n], _pixelHits[n], _trackerLayers[n], _pixelLayers[n], _mvaTTH[n], _jetOverlapIdx[n], _jetPtRatio[n], _jetBTagCSV[n], _jetDR[n], _pfRelIso03[n], _pfRelIso04[n], _etaSc[n], _eleExpMissingInnerHits[n], _eleooEmooP[n]) for n in range(n)]
    def __init__(self, charge,tightId,eleCutIdCSA14_25ns_v1,eleCutIdCSA14_50ns_v1,dxy,dz,edxy,edz,ip3d,sip3d,convVeto,lostHits,relIso03,relIso04,tightCharge,mcMatchId,mcMatchAny,mcMatchTau,mcPt,pdgId,pt,eta,phi,mass,looseIdSusy,looseIdPOG,chargedHadRelIso03,chargedHadRelIso04,eleSieie,eleDEta,eleDPhi,eleHoE,eleMissingHits,eleChi2,nMuonHits,nStations,trkKink,caloCompatibility,globalTrackChi2,nChamberHits,isPFMuon,isGlobalMuon,isTrackerMuon,pixelHits,trackerLayers,pixelLayers,mvaTTH,jetOverlapIdx,jetPtRatio,jetBTagCSV,jetDR,pfRelIso03,pfRelIso04,etaSc,eleExpMissingInnerHits,eleooEmooP):
        self.charge = charge #
        self.tightId = tightId #POG Tight ID (for electrons it's configured in the analyzer)
        self.eleCutIdCSA14_25ns_v1 = eleCutIdCSA14_25ns_v1 #Electron cut-based id (POG CSA14_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.eleCutIdCSA14_50ns_v1 = eleCutIdCSA14_50ns_v1 #Electron cut-based id (POG CSA14_50ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.dxy = dxy #d_{xy} with respect to PV, in cm (with sign)
        self.dz = dz #d_{z} with respect to PV, in cm (with sign)
        self.edxy = edxy ##sigma(d_{xy}) with respect to PV, in cm
        self.edz = edz ##sigma(d_{z}) with respect to PV, in cm
        self.ip3d = ip3d #d_{3d} with respect to PV, in cm (absolute value)
        self.sip3d = sip3d #S_{ip3d} with respect to PV (significance)
        self.convVeto = convVeto #Conversion veto (always true for muons)
        self.lostHits = lostHits #Number of lost hits on inner track
        self.relIso03 = relIso03 #PF Rel Iso, R=0.3, pile-up corrected
        self.relIso04 = relIso04 #PF Rel Iso, R=0.4, pile-up corrected
        self.tightCharge = tightCharge #Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, 2 if ptError/pt < 0.20, 0 otherwise 
        self.mcMatchId = mcMatchId #Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake
        self.mcMatchAny = mcMatchAny #Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom
        self.mcMatchTau = mcMatchTau #True if the leptons comes from a tau
        self.mcPt = mcPt #p_{T} of associated gen lepton
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.looseIdSusy = looseIdSusy #Loose ID for Susy ntuples (always true on selected leptons)
        self.looseIdPOG = looseIdPOG #Loose ID for Susy ntuples (always true on selected leptons)
        self.chargedHadRelIso03 = chargedHadRelIso03 #PF Rel Iso, R=0.3, charged hadrons only
        self.chargedHadRelIso04 = chargedHadRelIso04 #PF Rel Iso, R=0.4, charged hadrons only
        self.eleSieie = eleSieie #sigma IEtaIEta for electrons
        self.eleDEta = eleDEta #delta eta for electrons
        self.eleDPhi = eleDPhi #delta phi for electrons
        self.eleHoE = eleHoE #H/E for electrons
        self.eleMissingHits = eleMissingHits #Missing hits for electrons
        self.eleChi2 = eleChi2 #Track chi squared for electrons' gsf tracks
        self.nMuonHits = nMuonHits #Number of matched muons stations (4 for electrons)
        self.nStations = nStations #Number of matched muons stations (4 for electrons)
        self.trkKink = trkKink #Tracker kink-finder
        self.caloCompatibility = caloCompatibility #Calorimetric compatibility
        self.globalTrackChi2 = globalTrackChi2 #Global track normalized chi2
        self.nChamberHits = nChamberHits #Number of muon chamber hits (-1 for electrons)
        self.isPFMuon = isPFMuon #1 if muon passes particle flow ID
        self.isGlobalMuon = isGlobalMuon #1 if muon is global muon
        self.isTrackerMuon = isTrackerMuon #1 if muon is tracker muon
        self.pixelHits = pixelHits #Number of pixel hits (-1 for electrons)
        self.trackerLayers = trackerLayers #Tracker Layers
        self.pixelLayers = pixelLayers #Pixel Layers
        self.mvaTTH = mvaTTH #Lepton MVA (ttH version)
        self.jetOverlapIdx = jetOverlapIdx #index of jet with overlapping PF constituents
        self.jetPtRatio = jetPtRatio #pt(lepton)/pt(nearest jet)
        self.jetBTagCSV = jetBTagCSV #btag of nearest jet
        self.jetDR = jetDR #deltaR(lepton, nearest jet)
        self.pfRelIso03 = pfRelIso03 #0.3 particle based iso
        self.pfRelIso04 = pfRelIso04 #0.4 particle based iso
        self.etaSc = etaSc #Electron supercluster pseudorapidity
        self.eleExpMissingInnerHits = eleExpMissingInnerHits #Electron expected missing inner hits
        self.eleooEmooP = eleooEmooP #Electron 1/E - 1/P
class GenNuFromTop:
    """
    Generated neutrino from t->W decay
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenNuFromTop", 0)
        _pdgId = getattr(tree, "GenNuFromTop_pdgId", [None]*n)
        _pt = getattr(tree, "GenNuFromTop_pt", [None]*n)
        _eta = getattr(tree, "GenNuFromTop_eta", [None]*n)
        _phi = getattr(tree, "GenNuFromTop_phi", [None]*n)
        _mass = getattr(tree, "GenNuFromTop_mass", [None]*n)
        _charge = getattr(tree, "GenNuFromTop_charge", [None]*n)
        _status = getattr(tree, "GenNuFromTop_status", [None]*n)
        return [GenNuFromTop(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class DiscardedJet:
    """
    jets that were discarded
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nDiscardedJet", 0)
        _id = getattr(tree, "DiscardedJet_id", [None]*n)
        _puId = getattr(tree, "DiscardedJet_puId", [None]*n)
        _btagCSV = getattr(tree, "DiscardedJet_btagCSV", [None]*n)
        _btagCMVA = getattr(tree, "DiscardedJet_btagCMVA", [None]*n)
        _rawPt = getattr(tree, "DiscardedJet_rawPt", [None]*n)
        _mcPt = getattr(tree, "DiscardedJet_mcPt", [None]*n)
        _mcFlavour = getattr(tree, "DiscardedJet_mcFlavour", [None]*n)
        _mcMatchId = getattr(tree, "DiscardedJet_mcMatchId", [None]*n)
        _corr_JECUp = getattr(tree, "DiscardedJet_corr_JECUp", [None]*n)
        _corr_JECDown = getattr(tree, "DiscardedJet_corr_JECDown", [None]*n)
        _corr = getattr(tree, "DiscardedJet_corr", [None]*n)
        _pt = getattr(tree, "DiscardedJet_pt", [None]*n)
        _eta = getattr(tree, "DiscardedJet_eta", [None]*n)
        _phi = getattr(tree, "DiscardedJet_phi", [None]*n)
        _mass = getattr(tree, "DiscardedJet_mass", [None]*n)
        _idxFirstTauMatch = getattr(tree, "DiscardedJet_idxFirstTauMatch", [None]*n)
        _hadronFlavour = getattr(tree, "DiscardedJet_hadronFlavour", [None]*n)
        _btagBDT = getattr(tree, "DiscardedJet_btagBDT", [None]*n)
        _btagProb = getattr(tree, "DiscardedJet_btagProb", [None]*n)
        _btagBProb = getattr(tree, "DiscardedJet_btagBProb", [None]*n)
        _btagSoftEl = getattr(tree, "DiscardedJet_btagSoftEl", [None]*n)
        _btagSoftMu = getattr(tree, "DiscardedJet_btagSoftMu", [None]*n)
        _btagnew = getattr(tree, "DiscardedJet_btagnew", [None]*n)
        _btagCSVV0 = getattr(tree, "DiscardedJet_btagCSVV0", [None]*n)
        _chHEF = getattr(tree, "DiscardedJet_chHEF", [None]*n)
        _neHEF = getattr(tree, "DiscardedJet_neHEF", [None]*n)
        _chEmEF = getattr(tree, "DiscardedJet_chEmEF", [None]*n)
        _neEmEF = getattr(tree, "DiscardedJet_neEmEF", [None]*n)
        _chMult = getattr(tree, "DiscardedJet_chMult", [None]*n)
        _leadTrackPt = getattr(tree, "DiscardedJet_leadTrackPt", [None]*n)
        _mcEta = getattr(tree, "DiscardedJet_mcEta", [None]*n)
        _mcPhi = getattr(tree, "DiscardedJet_mcPhi", [None]*n)
        _mcM = getattr(tree, "DiscardedJet_mcM", [None]*n)
        _leptonPdgId = getattr(tree, "DiscardedJet_leptonPdgId", [None]*n)
        _leptonPt = getattr(tree, "DiscardedJet_leptonPt", [None]*n)
        _leptonPtRel = getattr(tree, "DiscardedJet_leptonPtRel", [None]*n)
        _leptonPtRelInv = getattr(tree, "DiscardedJet_leptonPtRelInv", [None]*n)
        _leptonDeltaR = getattr(tree, "DiscardedJet_leptonDeltaR", [None]*n)
        _vtxMass = getattr(tree, "DiscardedJet_vtxMass", [None]*n)
        _vtxNtracks = getattr(tree, "DiscardedJet_vtxNtracks", [None]*n)
        _vtxPt = getattr(tree, "DiscardedJet_vtxPt", [None]*n)
        _vtx3DSig = getattr(tree, "DiscardedJet_vtx3DSig", [None]*n)
        _vtx3DVal = getattr(tree, "DiscardedJet_vtx3DVal", [None]*n)
        _vtxPosX = getattr(tree, "DiscardedJet_vtxPosX", [None]*n)
        _vtxPosY = getattr(tree, "DiscardedJet_vtxPosY", [None]*n)
        _vtxPosZ = getattr(tree, "DiscardedJet_vtxPosZ", [None]*n)
        _qgl = getattr(tree, "DiscardedJet_qgl", [None]*n)
        _ptd = getattr(tree, "DiscardedJet_ptd", [None]*n)
        _axis2 = getattr(tree, "DiscardedJet_axis2", [None]*n)
        _mult = getattr(tree, "DiscardedJet_mult", [None]*n)
        _numberOfDaughters = getattr(tree, "DiscardedJet_numberOfDaughters", [None]*n)
        return [DiscardedJet(_id[n], _puId[n], _btagCSV[n], _btagCMVA[n], _rawPt[n], _mcPt[n], _mcFlavour[n], _mcMatchId[n], _corr_JECUp[n], _corr_JECDown[n], _corr[n], _pt[n], _eta[n], _phi[n], _mass[n], _idxFirstTauMatch[n], _hadronFlavour[n], _btagBDT[n], _btagProb[n], _btagBProb[n], _btagSoftEl[n], _btagSoftMu[n], _btagnew[n], _btagCSVV0[n], _chHEF[n], _neHEF[n], _chEmEF[n], _neEmEF[n], _chMult[n], _leadTrackPt[n], _mcEta[n], _mcPhi[n], _mcM[n], _leptonPdgId[n], _leptonPt[n], _leptonPtRel[n], _leptonPtRelInv[n], _leptonDeltaR[n], _vtxMass[n], _vtxNtracks[n], _vtxPt[n], _vtx3DSig[n], _vtx3DVal[n], _vtxPosX[n], _vtxPosY[n], _vtxPosZ[n], _qgl[n], _ptd[n], _axis2[n], _mult[n], _numberOfDaughters[n]) for n in range(n)]
    def __init__(self, id,puId,btagCSV,btagCMVA,rawPt,mcPt,mcFlavour,mcMatchId,corr_JECUp,corr_JECDown,corr,pt,eta,phi,mass,idxFirstTauMatch,hadronFlavour,btagBDT,btagProb,btagBProb,btagSoftEl,btagSoftMu,btagnew,btagCSVV0,chHEF,neHEF,chEmEF,neEmEF,chMult,leadTrackPt,mcEta,mcPhi,mcM,leptonPdgId,leptonPt,leptonPtRel,leptonPtRelInv,leptonDeltaR,vtxMass,vtxNtracks,vtxPt,vtx3DSig,vtx3DVal,vtxPosX,vtxPosY,vtxPosZ,qgl,ptd,axis2,mult,numberOfDaughters):
        self.id = id #POG Loose jet ID
        self.puId = puId #puId (full MVA, loose WP, 5.3.X training on AK5PFchs: the only thing that is available now)
        self.btagCSV = btagCSV #CSV-IVF v2 discriminator
        self.btagCMVA = btagCMVA #CMVA discriminator
        self.rawPt = rawPt #p_{T} before JEC
        self.mcPt = mcPt #p_{T} of associated gen jet
        self.mcFlavour = mcFlavour #parton flavour (physics definition, i.e. including b's from shower)
        self.mcMatchId = mcMatchId #Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake
        self.corr_JECUp = corr_JECUp #
        self.corr_JECDown = corr_JECDown #
        self.corr = corr #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.idxFirstTauMatch = idxFirstTauMatch #index of the first matching tau
        self.hadronFlavour = hadronFlavour #match to heavy hadrons
        self.btagBDT = btagBDT #btag
        self.btagProb = btagProb #btag
        self.btagBProb = btagBProb #btag
        self.btagSoftEl = btagSoftEl #soft electron b-tag
        self.btagSoftMu = btagSoftMu #soft muon b-tag
        self.btagnew = btagnew #newest btag discriminator
        self.btagCSVV0 = btagCSVV0 #should be the old CSV discriminator
        self.chHEF = chHEF #chargedHadronEnergyFraction (relative to uncorrected jet energy)
        self.neHEF = neHEF #neutralHadronEnergyFraction (relative to uncorrected jet energy)
        self.chEmEF = chEmEF #chargedEmEnergyFraction (relative to uncorrected jet energy)
        self.neEmEF = neEmEF #neutralEmEnergyFraction (relative to uncorrected jet energy)
        self.chMult = chMult #chargedMultiplicity from PFJet.h
        self.leadTrackPt = leadTrackPt #pt of the leading track in the jet
        self.mcEta = mcEta #eta of associated gen jet
        self.mcPhi = mcPhi #phi of associated gen jet
        self.mcM = mcM #mass of associated gen jet
        self.leptonPdgId = leptonPdgId #pdg id of the first associated lepton
        self.leptonPt = leptonPt #pt of the first associated lepton
        self.leptonPtRel = leptonPtRel #ptrel of the first associated lepton
        self.leptonPtRelInv = leptonPtRelInv #ptrel Run1 definition of the first associated lepton
        self.leptonDeltaR = leptonDeltaR #deltaR of the first associated lepton
        self.vtxMass = vtxMass #vtxMass from btag
        self.vtxNtracks = vtxNtracks #number of tracks at vertex from btag
        self.vtxPt = vtxPt #pt of vertex from btag
        self.vtx3DSig = vtx3DSig #decay len significance of vertex from btag
        self.vtx3DVal = vtx3DVal #decay len of vertex from btag
        self.vtxPosX = vtxPosX #X coord of vertex from btag
        self.vtxPosY = vtxPosY #Y coord of vertex from btag
        self.vtxPosZ = vtxPosZ #Z coord of vertex from btag
        self.qgl = qgl #QG Likelihood
        self.ptd = ptd #QG input variable: ptD
        self.axis2 = axis2 #QG input variable: axis2
        self.mult = mult #QG input variable: total multiplicity
        self.numberOfDaughters = numberOfDaughters #number of daughters
class selLeptons:
    """
    Leptons after the preselection
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nselLeptons", 0)
        _charge = getattr(tree, "selLeptons_charge", [None]*n)
        _tightId = getattr(tree, "selLeptons_tightId", [None]*n)
        _eleCutIdCSA14_25ns_v1 = getattr(tree, "selLeptons_eleCutIdCSA14_25ns_v1", [None]*n)
        _eleCutIdCSA14_50ns_v1 = getattr(tree, "selLeptons_eleCutIdCSA14_50ns_v1", [None]*n)
        _dxy = getattr(tree, "selLeptons_dxy", [None]*n)
        _dz = getattr(tree, "selLeptons_dz", [None]*n)
        _edxy = getattr(tree, "selLeptons_edxy", [None]*n)
        _edz = getattr(tree, "selLeptons_edz", [None]*n)
        _ip3d = getattr(tree, "selLeptons_ip3d", [None]*n)
        _sip3d = getattr(tree, "selLeptons_sip3d", [None]*n)
        _convVeto = getattr(tree, "selLeptons_convVeto", [None]*n)
        _lostHits = getattr(tree, "selLeptons_lostHits", [None]*n)
        _relIso03 = getattr(tree, "selLeptons_relIso03", [None]*n)
        _relIso04 = getattr(tree, "selLeptons_relIso04", [None]*n)
        _tightCharge = getattr(tree, "selLeptons_tightCharge", [None]*n)
        _mcMatchId = getattr(tree, "selLeptons_mcMatchId", [None]*n)
        _mcMatchAny = getattr(tree, "selLeptons_mcMatchAny", [None]*n)
        _mcMatchTau = getattr(tree, "selLeptons_mcMatchTau", [None]*n)
        _mcPt = getattr(tree, "selLeptons_mcPt", [None]*n)
        _pdgId = getattr(tree, "selLeptons_pdgId", [None]*n)
        _pt = getattr(tree, "selLeptons_pt", [None]*n)
        _eta = getattr(tree, "selLeptons_eta", [None]*n)
        _phi = getattr(tree, "selLeptons_phi", [None]*n)
        _mass = getattr(tree, "selLeptons_mass", [None]*n)
        _looseIdSusy = getattr(tree, "selLeptons_looseIdSusy", [None]*n)
        _looseIdPOG = getattr(tree, "selLeptons_looseIdPOG", [None]*n)
        _chargedHadRelIso03 = getattr(tree, "selLeptons_chargedHadRelIso03", [None]*n)
        _chargedHadRelIso04 = getattr(tree, "selLeptons_chargedHadRelIso04", [None]*n)
        _eleSieie = getattr(tree, "selLeptons_eleSieie", [None]*n)
        _eleDEta = getattr(tree, "selLeptons_eleDEta", [None]*n)
        _eleDPhi = getattr(tree, "selLeptons_eleDPhi", [None]*n)
        _eleHoE = getattr(tree, "selLeptons_eleHoE", [None]*n)
        _eleMissingHits = getattr(tree, "selLeptons_eleMissingHits", [None]*n)
        _eleChi2 = getattr(tree, "selLeptons_eleChi2", [None]*n)
        _nMuonHits = getattr(tree, "selLeptons_nMuonHits", [None]*n)
        _nStations = getattr(tree, "selLeptons_nStations", [None]*n)
        _trkKink = getattr(tree, "selLeptons_trkKink", [None]*n)
        _caloCompatibility = getattr(tree, "selLeptons_caloCompatibility", [None]*n)
        _globalTrackChi2 = getattr(tree, "selLeptons_globalTrackChi2", [None]*n)
        _nChamberHits = getattr(tree, "selLeptons_nChamberHits", [None]*n)
        _isPFMuon = getattr(tree, "selLeptons_isPFMuon", [None]*n)
        _isGlobalMuon = getattr(tree, "selLeptons_isGlobalMuon", [None]*n)
        _isTrackerMuon = getattr(tree, "selLeptons_isTrackerMuon", [None]*n)
        _pixelHits = getattr(tree, "selLeptons_pixelHits", [None]*n)
        _trackerLayers = getattr(tree, "selLeptons_trackerLayers", [None]*n)
        _pixelLayers = getattr(tree, "selLeptons_pixelLayers", [None]*n)
        _mvaTTH = getattr(tree, "selLeptons_mvaTTH", [None]*n)
        _jetOverlapIdx = getattr(tree, "selLeptons_jetOverlapIdx", [None]*n)
        _jetPtRatio = getattr(tree, "selLeptons_jetPtRatio", [None]*n)
        _jetBTagCSV = getattr(tree, "selLeptons_jetBTagCSV", [None]*n)
        _jetDR = getattr(tree, "selLeptons_jetDR", [None]*n)
        _pfRelIso03 = getattr(tree, "selLeptons_pfRelIso03", [None]*n)
        _pfRelIso04 = getattr(tree, "selLeptons_pfRelIso04", [None]*n)
        _etaSc = getattr(tree, "selLeptons_etaSc", [None]*n)
        _eleExpMissingInnerHits = getattr(tree, "selLeptons_eleExpMissingInnerHits", [None]*n)
        _eleooEmooP = getattr(tree, "selLeptons_eleooEmooP", [None]*n)
        return [selLeptons(_charge[n], _tightId[n], _eleCutIdCSA14_25ns_v1[n], _eleCutIdCSA14_50ns_v1[n], _dxy[n], _dz[n], _edxy[n], _edz[n], _ip3d[n], _sip3d[n], _convVeto[n], _lostHits[n], _relIso03[n], _relIso04[n], _tightCharge[n], _mcMatchId[n], _mcMatchAny[n], _mcMatchTau[n], _mcPt[n], _pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _looseIdSusy[n], _looseIdPOG[n], _chargedHadRelIso03[n], _chargedHadRelIso04[n], _eleSieie[n], _eleDEta[n], _eleDPhi[n], _eleHoE[n], _eleMissingHits[n], _eleChi2[n], _nMuonHits[n], _nStations[n], _trkKink[n], _caloCompatibility[n], _globalTrackChi2[n], _nChamberHits[n], _isPFMuon[n], _isGlobalMuon[n], _isTrackerMuon[n], _pixelHits[n], _trackerLayers[n], _pixelLayers[n], _mvaTTH[n], _jetOverlapIdx[n], _jetPtRatio[n], _jetBTagCSV[n], _jetDR[n], _pfRelIso03[n], _pfRelIso04[n], _etaSc[n], _eleExpMissingInnerHits[n], _eleooEmooP[n]) for n in range(n)]
    def __init__(self, charge,tightId,eleCutIdCSA14_25ns_v1,eleCutIdCSA14_50ns_v1,dxy,dz,edxy,edz,ip3d,sip3d,convVeto,lostHits,relIso03,relIso04,tightCharge,mcMatchId,mcMatchAny,mcMatchTau,mcPt,pdgId,pt,eta,phi,mass,looseIdSusy,looseIdPOG,chargedHadRelIso03,chargedHadRelIso04,eleSieie,eleDEta,eleDPhi,eleHoE,eleMissingHits,eleChi2,nMuonHits,nStations,trkKink,caloCompatibility,globalTrackChi2,nChamberHits,isPFMuon,isGlobalMuon,isTrackerMuon,pixelHits,trackerLayers,pixelLayers,mvaTTH,jetOverlapIdx,jetPtRatio,jetBTagCSV,jetDR,pfRelIso03,pfRelIso04,etaSc,eleExpMissingInnerHits,eleooEmooP):
        self.charge = charge #
        self.tightId = tightId #POG Tight ID (for electrons it's configured in the analyzer)
        self.eleCutIdCSA14_25ns_v1 = eleCutIdCSA14_25ns_v1 #Electron cut-based id (POG CSA14_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.eleCutIdCSA14_50ns_v1 = eleCutIdCSA14_50ns_v1 #Electron cut-based id (POG CSA14_50ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.dxy = dxy #d_{xy} with respect to PV, in cm (with sign)
        self.dz = dz #d_{z} with respect to PV, in cm (with sign)
        self.edxy = edxy ##sigma(d_{xy}) with respect to PV, in cm
        self.edz = edz ##sigma(d_{z}) with respect to PV, in cm
        self.ip3d = ip3d #d_{3d} with respect to PV, in cm (absolute value)
        self.sip3d = sip3d #S_{ip3d} with respect to PV (significance)
        self.convVeto = convVeto #Conversion veto (always true for muons)
        self.lostHits = lostHits #Number of lost hits on inner track
        self.relIso03 = relIso03 #PF Rel Iso, R=0.3, pile-up corrected
        self.relIso04 = relIso04 #PF Rel Iso, R=0.4, pile-up corrected
        self.tightCharge = tightCharge #Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, 2 if ptError/pt < 0.20, 0 otherwise 
        self.mcMatchId = mcMatchId #Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake
        self.mcMatchAny = mcMatchAny #Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom
        self.mcMatchTau = mcMatchTau #True if the leptons comes from a tau
        self.mcPt = mcPt #p_{T} of associated gen lepton
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.looseIdSusy = looseIdSusy #Loose ID for Susy ntuples (always true on selected leptons)
        self.looseIdPOG = looseIdPOG #Loose ID for Susy ntuples (always true on selected leptons)
        self.chargedHadRelIso03 = chargedHadRelIso03 #PF Rel Iso, R=0.3, charged hadrons only
        self.chargedHadRelIso04 = chargedHadRelIso04 #PF Rel Iso, R=0.4, charged hadrons only
        self.eleSieie = eleSieie #sigma IEtaIEta for electrons
        self.eleDEta = eleDEta #delta eta for electrons
        self.eleDPhi = eleDPhi #delta phi for electrons
        self.eleHoE = eleHoE #H/E for electrons
        self.eleMissingHits = eleMissingHits #Missing hits for electrons
        self.eleChi2 = eleChi2 #Track chi squared for electrons' gsf tracks
        self.nMuonHits = nMuonHits #Number of matched muons stations (4 for electrons)
        self.nStations = nStations #Number of matched muons stations (4 for electrons)
        self.trkKink = trkKink #Tracker kink-finder
        self.caloCompatibility = caloCompatibility #Calorimetric compatibility
        self.globalTrackChi2 = globalTrackChi2 #Global track normalized chi2
        self.nChamberHits = nChamberHits #Number of muon chamber hits (-1 for electrons)
        self.isPFMuon = isPFMuon #1 if muon passes particle flow ID
        self.isGlobalMuon = isGlobalMuon #1 if muon is global muon
        self.isTrackerMuon = isTrackerMuon #1 if muon is tracker muon
        self.pixelHits = pixelHits #Number of pixel hits (-1 for electrons)
        self.trackerLayers = trackerLayers #Tracker Layers
        self.pixelLayers = pixelLayers #Pixel Layers
        self.mvaTTH = mvaTTH #Lepton MVA (ttH version)
        self.jetOverlapIdx = jetOverlapIdx #index of jet with overlapping PF constituents
        self.jetPtRatio = jetPtRatio #pt(lepton)/pt(nearest jet)
        self.jetBTagCSV = jetBTagCSV #btag of nearest jet
        self.jetDR = jetDR #deltaR(lepton, nearest jet)
        self.pfRelIso03 = pfRelIso03 #0.3 particle based iso
        self.pfRelIso04 = pfRelIso04 #0.4 particle based iso
        self.etaSc = etaSc #Electron supercluster pseudorapidity
        self.eleExpMissingInnerHits = eleExpMissingInnerHits #Electron expected missing inner hits
        self.eleooEmooP = eleooEmooP #Electron 1/E - 1/P
class TauGood:
    """
    Taus after the preselection
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nTauGood", 0)
        _charge = getattr(tree, "TauGood_charge", [None]*n)
        _decayMode = getattr(tree, "TauGood_decayMode", [None]*n)
        _idDecayMode = getattr(tree, "TauGood_idDecayMode", [None]*n)
        _idDecayModeNewDMs = getattr(tree, "TauGood_idDecayModeNewDMs", [None]*n)
        _dxy = getattr(tree, "TauGood_dxy", [None]*n)
        _dz = getattr(tree, "TauGood_dz", [None]*n)
        _idMVA = getattr(tree, "TauGood_idMVA", [None]*n)
        _idMVANewDM = getattr(tree, "TauGood_idMVANewDM", [None]*n)
        _idCI3hit = getattr(tree, "TauGood_idCI3hit", [None]*n)
        _idAntiMu = getattr(tree, "TauGood_idAntiMu", [None]*n)
        _idAntiE = getattr(tree, "TauGood_idAntiE", [None]*n)
        _isoCI3hit = getattr(tree, "TauGood_isoCI3hit", [None]*n)
        _mcMatchId = getattr(tree, "TauGood_mcMatchId", [None]*n)
        _pdgId = getattr(tree, "TauGood_pdgId", [None]*n)
        _pt = getattr(tree, "TauGood_pt", [None]*n)
        _eta = getattr(tree, "TauGood_eta", [None]*n)
        _phi = getattr(tree, "TauGood_phi", [None]*n)
        _mass = getattr(tree, "TauGood_mass", [None]*n)
        _idxJetMatch = getattr(tree, "TauGood_idxJetMatch", [None]*n)
        _genMatchType = getattr(tree, "TauGood_genMatchType", [None]*n)
        return [TauGood(_charge[n], _decayMode[n], _idDecayMode[n], _idDecayModeNewDMs[n], _dxy[n], _dz[n], _idMVA[n], _idMVANewDM[n], _idCI3hit[n], _idAntiMu[n], _idAntiE[n], _isoCI3hit[n], _mcMatchId[n], _pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _idxJetMatch[n], _genMatchType[n]) for n in range(n)]
    def __init__(self, charge,decayMode,idDecayMode,idDecayModeNewDMs,dxy,dz,idMVA,idMVANewDM,idCI3hit,idAntiMu,idAntiE,isoCI3hit,mcMatchId,pdgId,pt,eta,phi,mass,idxJetMatch,genMatchType):
        self.charge = charge #
        self.decayMode = decayMode #
        self.idDecayMode = idDecayMode #
        self.idDecayModeNewDMs = idDecayModeNewDMs #
        self.dxy = dxy #d_{xy} of lead track with respect to PV, in cm (with sign)
        self.dz = dz #d_{z} of lead track with respect to PV, in cm (with sign)
        self.idMVA = idMVA #1,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the MVA3oldDMwLT discriminator
        self.idMVANewDM = idMVANewDM #1,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the MVA3newDMwLT discriminator
        self.idCI3hit = idCI3hit #1,2,3 if the tau passes the loose, medium, tight WP of the By<X>CombinedIsolationDBSumPtCorr3Hits discriminator
        self.idAntiMu = idAntiMu #1,2 if the tau passes the loose/tight WP of the againstMuon<X>3 discriminator
        self.idAntiE = idAntiE #1,2,3,4,5 if the tau passes the v loose, loose, medium, tight, v tight WP of the againstElectron<X>MVA5 discriminator
        self.isoCI3hit = isoCI3hit #byCombinedIsolationDeltaBetaCorrRaw3Hits raw output discriminator
        self.mcMatchId = mcMatchId #Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.idxJetMatch = idxJetMatch #index of the matching jet
        self.genMatchType = genMatchType #..FILLME PLEASE..
class hJ3Cidx:
    """
    Higgs jet indices 3 cen jets
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nhJ3Cidx", 0)
        _hJ3Cidx = getattr(tree, "hJ3Cidx", [None]*n);
        return [hJ3Cidx(_hJ3Cidx[n]) for n in range(n)]
    def __init__(self, hJ3Cidx):
        self.hJ3Cidx = hJ3Cidx #Higgs jet indices 3 cen jets
class hJidx:
    """
    Higgs jet indices
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nhJidx", 0)
        _hJidx = getattr(tree, "hJidx", [None]*n);
        return [hJidx(_hJidx[n]) for n in range(n)]
    def __init__(self, hJidx):
        self.hJidx = hJidx #Higgs jet indices
class GenLep:
    """
    Generated leptons from W/Z decays
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenLep", 0)
        _pdgId = getattr(tree, "GenLep_pdgId", [None]*n)
        _pt = getattr(tree, "GenLep_pt", [None]*n)
        _eta = getattr(tree, "GenLep_eta", [None]*n)
        _phi = getattr(tree, "GenLep_phi", [None]*n)
        _mass = getattr(tree, "GenLep_mass", [None]*n)
        _charge = getattr(tree, "GenLep_charge", [None]*n)
        _status = getattr(tree, "GenLep_status", [None]*n)
        return [GenLep(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class GenJet:
    """
    Generated jets with hadron matching, sorted by pt descending
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenJet", 0)
        _charge = getattr(tree, "GenJet_charge", [None]*n)
        _status = getattr(tree, "GenJet_status", [None]*n)
        _pdgId = getattr(tree, "GenJet_pdgId", [None]*n)
        _pt = getattr(tree, "GenJet_pt", [None]*n)
        _eta = getattr(tree, "GenJet_eta", [None]*n)
        _phi = getattr(tree, "GenJet_phi", [None]*n)
        _mass = getattr(tree, "GenJet_mass", [None]*n)
        _numBHadrons = getattr(tree, "GenJet_numBHadrons", [None]*n)
        _numCHadrons = getattr(tree, "GenJet_numCHadrons", [None]*n)
        _numBHadronsFromTop = getattr(tree, "GenJet_numBHadronsFromTop", [None]*n)
        _numCHadronsFromTop = getattr(tree, "GenJet_numCHadronsFromTop", [None]*n)
        _numBHadronsAfterTop = getattr(tree, "GenJet_numBHadronsAfterTop", [None]*n)
        _numCHadronsAfterTop = getattr(tree, "GenJet_numCHadronsAfterTop", [None]*n)
        return [GenJet(_charge[n], _status[n], _pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _numBHadrons[n], _numCHadrons[n], _numBHadronsFromTop[n], _numCHadronsFromTop[n], _numBHadronsAfterTop[n], _numCHadronsAfterTop[n]) for n in range(n)]
    def __init__(self, charge,status,pdgId,pt,eta,phi,mass,numBHadrons,numCHadrons,numBHadronsFromTop,numCHadronsFromTop,numBHadronsAfterTop,numCHadronsAfterTop):
        self.charge = charge #
        self.status = status #
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.numBHadrons = numBHadrons #number of matched b hadrons before top quark decay
        self.numCHadrons = numCHadrons #number of matched c hadrons before top quark decay
        self.numBHadronsFromTop = numBHadronsFromTop #number of matched b hadrons from top quark decay
        self.numCHadronsFromTop = numCHadronsFromTop #number of matched c hadrons from top quark decay
        self.numBHadronsAfterTop = numBHadronsAfterTop #number of matched b hadrons after top quark decay
        self.numCHadronsAfterTop = numCHadronsAfterTop #number of matched c hadrons after top quark decay
class Jet:
    """
    Cental+fwd jets after full selection and cleaning, sorted by b-tag
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nJet", 0)
        _id = getattr(tree, "Jet_id", [None]*n)
        _puId = getattr(tree, "Jet_puId", [None]*n)
        _btagCSV = getattr(tree, "Jet_btagCSV", [None]*n)
        _btagCMVA = getattr(tree, "Jet_btagCMVA", [None]*n)
        _rawPt = getattr(tree, "Jet_rawPt", [None]*n)
        _mcPt = getattr(tree, "Jet_mcPt", [None]*n)
        _mcFlavour = getattr(tree, "Jet_mcFlavour", [None]*n)
        _mcMatchId = getattr(tree, "Jet_mcMatchId", [None]*n)
        _corr_JECUp = getattr(tree, "Jet_corr_JECUp", [None]*n)
        _corr_JECDown = getattr(tree, "Jet_corr_JECDown", [None]*n)
        _corr = getattr(tree, "Jet_corr", [None]*n)
        _pt = getattr(tree, "Jet_pt", [None]*n)
        _eta = getattr(tree, "Jet_eta", [None]*n)
        _phi = getattr(tree, "Jet_phi", [None]*n)
        _mass = getattr(tree, "Jet_mass", [None]*n)
        _idxFirstTauMatch = getattr(tree, "Jet_idxFirstTauMatch", [None]*n)
        _hadronFlavour = getattr(tree, "Jet_hadronFlavour", [None]*n)
        _btagBDT = getattr(tree, "Jet_btagBDT", [None]*n)
        _btagProb = getattr(tree, "Jet_btagProb", [None]*n)
        _btagBProb = getattr(tree, "Jet_btagBProb", [None]*n)
        _btagSoftEl = getattr(tree, "Jet_btagSoftEl", [None]*n)
        _btagSoftMu = getattr(tree, "Jet_btagSoftMu", [None]*n)
        _btagnew = getattr(tree, "Jet_btagnew", [None]*n)
        _btagCSVV0 = getattr(tree, "Jet_btagCSVV0", [None]*n)
        _chHEF = getattr(tree, "Jet_chHEF", [None]*n)
        _neHEF = getattr(tree, "Jet_neHEF", [None]*n)
        _chEmEF = getattr(tree, "Jet_chEmEF", [None]*n)
        _neEmEF = getattr(tree, "Jet_neEmEF", [None]*n)
        _chMult = getattr(tree, "Jet_chMult", [None]*n)
        _leadTrackPt = getattr(tree, "Jet_leadTrackPt", [None]*n)
        _mcEta = getattr(tree, "Jet_mcEta", [None]*n)
        _mcPhi = getattr(tree, "Jet_mcPhi", [None]*n)
        _mcM = getattr(tree, "Jet_mcM", [None]*n)
        _leptonPdgId = getattr(tree, "Jet_leptonPdgId", [None]*n)
        _leptonPt = getattr(tree, "Jet_leptonPt", [None]*n)
        _leptonPtRel = getattr(tree, "Jet_leptonPtRel", [None]*n)
        _leptonPtRelInv = getattr(tree, "Jet_leptonPtRelInv", [None]*n)
        _leptonDeltaR = getattr(tree, "Jet_leptonDeltaR", [None]*n)
        _vtxMass = getattr(tree, "Jet_vtxMass", [None]*n)
        _vtxNtracks = getattr(tree, "Jet_vtxNtracks", [None]*n)
        _vtxPt = getattr(tree, "Jet_vtxPt", [None]*n)
        _vtx3DSig = getattr(tree, "Jet_vtx3DSig", [None]*n)
        _vtx3DVal = getattr(tree, "Jet_vtx3DVal", [None]*n)
        _vtxPosX = getattr(tree, "Jet_vtxPosX", [None]*n)
        _vtxPosY = getattr(tree, "Jet_vtxPosY", [None]*n)
        _vtxPosZ = getattr(tree, "Jet_vtxPosZ", [None]*n)
        _qgl = getattr(tree, "Jet_qgl", [None]*n)
        _ptd = getattr(tree, "Jet_ptd", [None]*n)
        _axis2 = getattr(tree, "Jet_axis2", [None]*n)
        _mult = getattr(tree, "Jet_mult", [None]*n)
        _numberOfDaughters = getattr(tree, "Jet_numberOfDaughters", [None]*n)
        return [Jet(_id[n], _puId[n], _btagCSV[n], _btagCMVA[n], _rawPt[n], _mcPt[n], _mcFlavour[n], _mcMatchId[n], _corr_JECUp[n], _corr_JECDown[n], _corr[n], _pt[n], _eta[n], _phi[n], _mass[n], _idxFirstTauMatch[n], _hadronFlavour[n], _btagBDT[n], _btagProb[n], _btagBProb[n], _btagSoftEl[n], _btagSoftMu[n], _btagnew[n], _btagCSVV0[n], _chHEF[n], _neHEF[n], _chEmEF[n], _neEmEF[n], _chMult[n], _leadTrackPt[n], _mcEta[n], _mcPhi[n], _mcM[n], _leptonPdgId[n], _leptonPt[n], _leptonPtRel[n], _leptonPtRelInv[n], _leptonDeltaR[n], _vtxMass[n], _vtxNtracks[n], _vtxPt[n], _vtx3DSig[n], _vtx3DVal[n], _vtxPosX[n], _vtxPosY[n], _vtxPosZ[n], _qgl[n], _ptd[n], _axis2[n], _mult[n], _numberOfDaughters[n]) for n in range(n)]
    def __init__(self, id,puId,btagCSV,btagCMVA,rawPt,mcPt,mcFlavour,mcMatchId,corr_JECUp,corr_JECDown,corr,pt,eta,phi,mass,idxFirstTauMatch,hadronFlavour,btagBDT,btagProb,btagBProb,btagSoftEl,btagSoftMu,btagnew,btagCSVV0,chHEF,neHEF,chEmEF,neEmEF,chMult,leadTrackPt,mcEta,mcPhi,mcM,leptonPdgId,leptonPt,leptonPtRel,leptonPtRelInv,leptonDeltaR,vtxMass,vtxNtracks,vtxPt,vtx3DSig,vtx3DVal,vtxPosX,vtxPosY,vtxPosZ,qgl,ptd,axis2,mult,numberOfDaughters):
        self.id = id #POG Loose jet ID
        self.puId = puId #puId (full MVA, loose WP, 5.3.X training on AK5PFchs: the only thing that is available now)
        self.btagCSV = btagCSV #CSV-IVF v2 discriminator
        self.btagCMVA = btagCMVA #CMVA discriminator
        self.rawPt = rawPt #p_{T} before JEC
        self.mcPt = mcPt #p_{T} of associated gen jet
        self.mcFlavour = mcFlavour #parton flavour (physics definition, i.e. including b's from shower)
        self.mcMatchId = mcMatchId #Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake
        self.corr_JECUp = corr_JECUp #
        self.corr_JECDown = corr_JECDown #
        self.corr = corr #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.idxFirstTauMatch = idxFirstTauMatch #index of the first matching tau
        self.hadronFlavour = hadronFlavour #match to heavy hadrons
        self.btagBDT = btagBDT #btag
        self.btagProb = btagProb #btag
        self.btagBProb = btagBProb #btag
        self.btagSoftEl = btagSoftEl #soft electron b-tag
        self.btagSoftMu = btagSoftMu #soft muon b-tag
        self.btagnew = btagnew #newest btag discriminator
        self.btagCSVV0 = btagCSVV0 #should be the old CSV discriminator
        self.chHEF = chHEF #chargedHadronEnergyFraction (relative to uncorrected jet energy)
        self.neHEF = neHEF #neutralHadronEnergyFraction (relative to uncorrected jet energy)
        self.chEmEF = chEmEF #chargedEmEnergyFraction (relative to uncorrected jet energy)
        self.neEmEF = neEmEF #neutralEmEnergyFraction (relative to uncorrected jet energy)
        self.chMult = chMult #chargedMultiplicity from PFJet.h
        self.leadTrackPt = leadTrackPt #pt of the leading track in the jet
        self.mcEta = mcEta #eta of associated gen jet
        self.mcPhi = mcPhi #phi of associated gen jet
        self.mcM = mcM #mass of associated gen jet
        self.leptonPdgId = leptonPdgId #pdg id of the first associated lepton
        self.leptonPt = leptonPt #pt of the first associated lepton
        self.leptonPtRel = leptonPtRel #ptrel of the first associated lepton
        self.leptonPtRelInv = leptonPtRelInv #ptrel Run1 definition of the first associated lepton
        self.leptonDeltaR = leptonDeltaR #deltaR of the first associated lepton
        self.vtxMass = vtxMass #vtxMass from btag
        self.vtxNtracks = vtxNtracks #number of tracks at vertex from btag
        self.vtxPt = vtxPt #pt of vertex from btag
        self.vtx3DSig = vtx3DSig #decay len significance of vertex from btag
        self.vtx3DVal = vtx3DVal #decay len of vertex from btag
        self.vtxPosX = vtxPosX #X coord of vertex from btag
        self.vtxPosY = vtxPosY #Y coord of vertex from btag
        self.vtxPosZ = vtxPosZ #Z coord of vertex from btag
        self.qgl = qgl #QG Likelihood
        self.ptd = ptd #QG input variable: ptD
        self.axis2 = axis2 #QG input variable: axis2
        self.mult = mult #QG input variable: total multiplicity
        self.numberOfDaughters = numberOfDaughters #number of daughters
class vLeptons:
    """
    Leptons after the preselection
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nvLeptons", 0)
        _charge = getattr(tree, "vLeptons_charge", [None]*n)
        _tightId = getattr(tree, "vLeptons_tightId", [None]*n)
        _eleCutIdCSA14_25ns_v1 = getattr(tree, "vLeptons_eleCutIdCSA14_25ns_v1", [None]*n)
        _eleCutIdCSA14_50ns_v1 = getattr(tree, "vLeptons_eleCutIdCSA14_50ns_v1", [None]*n)
        _dxy = getattr(tree, "vLeptons_dxy", [None]*n)
        _dz = getattr(tree, "vLeptons_dz", [None]*n)
        _edxy = getattr(tree, "vLeptons_edxy", [None]*n)
        _edz = getattr(tree, "vLeptons_edz", [None]*n)
        _ip3d = getattr(tree, "vLeptons_ip3d", [None]*n)
        _sip3d = getattr(tree, "vLeptons_sip3d", [None]*n)
        _convVeto = getattr(tree, "vLeptons_convVeto", [None]*n)
        _lostHits = getattr(tree, "vLeptons_lostHits", [None]*n)
        _relIso03 = getattr(tree, "vLeptons_relIso03", [None]*n)
        _relIso04 = getattr(tree, "vLeptons_relIso04", [None]*n)
        _tightCharge = getattr(tree, "vLeptons_tightCharge", [None]*n)
        _mcMatchId = getattr(tree, "vLeptons_mcMatchId", [None]*n)
        _mcMatchAny = getattr(tree, "vLeptons_mcMatchAny", [None]*n)
        _mcMatchTau = getattr(tree, "vLeptons_mcMatchTau", [None]*n)
        _mcPt = getattr(tree, "vLeptons_mcPt", [None]*n)
        _pdgId = getattr(tree, "vLeptons_pdgId", [None]*n)
        _pt = getattr(tree, "vLeptons_pt", [None]*n)
        _eta = getattr(tree, "vLeptons_eta", [None]*n)
        _phi = getattr(tree, "vLeptons_phi", [None]*n)
        _mass = getattr(tree, "vLeptons_mass", [None]*n)
        _looseIdSusy = getattr(tree, "vLeptons_looseIdSusy", [None]*n)
        _looseIdPOG = getattr(tree, "vLeptons_looseIdPOG", [None]*n)
        _chargedHadRelIso03 = getattr(tree, "vLeptons_chargedHadRelIso03", [None]*n)
        _chargedHadRelIso04 = getattr(tree, "vLeptons_chargedHadRelIso04", [None]*n)
        _eleSieie = getattr(tree, "vLeptons_eleSieie", [None]*n)
        _eleDEta = getattr(tree, "vLeptons_eleDEta", [None]*n)
        _eleDPhi = getattr(tree, "vLeptons_eleDPhi", [None]*n)
        _eleHoE = getattr(tree, "vLeptons_eleHoE", [None]*n)
        _eleMissingHits = getattr(tree, "vLeptons_eleMissingHits", [None]*n)
        _eleChi2 = getattr(tree, "vLeptons_eleChi2", [None]*n)
        _nMuonHits = getattr(tree, "vLeptons_nMuonHits", [None]*n)
        _nStations = getattr(tree, "vLeptons_nStations", [None]*n)
        _trkKink = getattr(tree, "vLeptons_trkKink", [None]*n)
        _caloCompatibility = getattr(tree, "vLeptons_caloCompatibility", [None]*n)
        _globalTrackChi2 = getattr(tree, "vLeptons_globalTrackChi2", [None]*n)
        _nChamberHits = getattr(tree, "vLeptons_nChamberHits", [None]*n)
        _isPFMuon = getattr(tree, "vLeptons_isPFMuon", [None]*n)
        _isGlobalMuon = getattr(tree, "vLeptons_isGlobalMuon", [None]*n)
        _isTrackerMuon = getattr(tree, "vLeptons_isTrackerMuon", [None]*n)
        _pixelHits = getattr(tree, "vLeptons_pixelHits", [None]*n)
        _trackerLayers = getattr(tree, "vLeptons_trackerLayers", [None]*n)
        _pixelLayers = getattr(tree, "vLeptons_pixelLayers", [None]*n)
        _mvaTTH = getattr(tree, "vLeptons_mvaTTH", [None]*n)
        _jetOverlapIdx = getattr(tree, "vLeptons_jetOverlapIdx", [None]*n)
        _jetPtRatio = getattr(tree, "vLeptons_jetPtRatio", [None]*n)
        _jetBTagCSV = getattr(tree, "vLeptons_jetBTagCSV", [None]*n)
        _jetDR = getattr(tree, "vLeptons_jetDR", [None]*n)
        _pfRelIso03 = getattr(tree, "vLeptons_pfRelIso03", [None]*n)
        _pfRelIso04 = getattr(tree, "vLeptons_pfRelIso04", [None]*n)
        _etaSc = getattr(tree, "vLeptons_etaSc", [None]*n)
        _eleExpMissingInnerHits = getattr(tree, "vLeptons_eleExpMissingInnerHits", [None]*n)
        _eleooEmooP = getattr(tree, "vLeptons_eleooEmooP", [None]*n)
        return [vLeptons(_charge[n], _tightId[n], _eleCutIdCSA14_25ns_v1[n], _eleCutIdCSA14_50ns_v1[n], _dxy[n], _dz[n], _edxy[n], _edz[n], _ip3d[n], _sip3d[n], _convVeto[n], _lostHits[n], _relIso03[n], _relIso04[n], _tightCharge[n], _mcMatchId[n], _mcMatchAny[n], _mcMatchTau[n], _mcPt[n], _pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _looseIdSusy[n], _looseIdPOG[n], _chargedHadRelIso03[n], _chargedHadRelIso04[n], _eleSieie[n], _eleDEta[n], _eleDPhi[n], _eleHoE[n], _eleMissingHits[n], _eleChi2[n], _nMuonHits[n], _nStations[n], _trkKink[n], _caloCompatibility[n], _globalTrackChi2[n], _nChamberHits[n], _isPFMuon[n], _isGlobalMuon[n], _isTrackerMuon[n], _pixelHits[n], _trackerLayers[n], _pixelLayers[n], _mvaTTH[n], _jetOverlapIdx[n], _jetPtRatio[n], _jetBTagCSV[n], _jetDR[n], _pfRelIso03[n], _pfRelIso04[n], _etaSc[n], _eleExpMissingInnerHits[n], _eleooEmooP[n]) for n in range(n)]
    def __init__(self, charge,tightId,eleCutIdCSA14_25ns_v1,eleCutIdCSA14_50ns_v1,dxy,dz,edxy,edz,ip3d,sip3d,convVeto,lostHits,relIso03,relIso04,tightCharge,mcMatchId,mcMatchAny,mcMatchTau,mcPt,pdgId,pt,eta,phi,mass,looseIdSusy,looseIdPOG,chargedHadRelIso03,chargedHadRelIso04,eleSieie,eleDEta,eleDPhi,eleHoE,eleMissingHits,eleChi2,nMuonHits,nStations,trkKink,caloCompatibility,globalTrackChi2,nChamberHits,isPFMuon,isGlobalMuon,isTrackerMuon,pixelHits,trackerLayers,pixelLayers,mvaTTH,jetOverlapIdx,jetPtRatio,jetBTagCSV,jetDR,pfRelIso03,pfRelIso04,etaSc,eleExpMissingInnerHits,eleooEmooP):
        self.charge = charge #
        self.tightId = tightId #POG Tight ID (for electrons it's configured in the analyzer)
        self.eleCutIdCSA14_25ns_v1 = eleCutIdCSA14_25ns_v1 #Electron cut-based id (POG CSA14_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.eleCutIdCSA14_50ns_v1 = eleCutIdCSA14_50ns_v1 #Electron cut-based id (POG CSA14_50ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.dxy = dxy #d_{xy} with respect to PV, in cm (with sign)
        self.dz = dz #d_{z} with respect to PV, in cm (with sign)
        self.edxy = edxy ##sigma(d_{xy}) with respect to PV, in cm
        self.edz = edz ##sigma(d_{z}) with respect to PV, in cm
        self.ip3d = ip3d #d_{3d} with respect to PV, in cm (absolute value)
        self.sip3d = sip3d #S_{ip3d} with respect to PV (significance)
        self.convVeto = convVeto #Conversion veto (always true for muons)
        self.lostHits = lostHits #Number of lost hits on inner track
        self.relIso03 = relIso03 #PF Rel Iso, R=0.3, pile-up corrected
        self.relIso04 = relIso04 #PF Rel Iso, R=0.4, pile-up corrected
        self.tightCharge = tightCharge #Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, 2 if ptError/pt < 0.20, 0 otherwise 
        self.mcMatchId = mcMatchId #Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake
        self.mcMatchAny = mcMatchAny #Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom
        self.mcMatchTau = mcMatchTau #True if the leptons comes from a tau
        self.mcPt = mcPt #p_{T} of associated gen lepton
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.looseIdSusy = looseIdSusy #Loose ID for Susy ntuples (always true on selected leptons)
        self.looseIdPOG = looseIdPOG #Loose ID for Susy ntuples (always true on selected leptons)
        self.chargedHadRelIso03 = chargedHadRelIso03 #PF Rel Iso, R=0.3, charged hadrons only
        self.chargedHadRelIso04 = chargedHadRelIso04 #PF Rel Iso, R=0.4, charged hadrons only
        self.eleSieie = eleSieie #sigma IEtaIEta for electrons
        self.eleDEta = eleDEta #delta eta for electrons
        self.eleDPhi = eleDPhi #delta phi for electrons
        self.eleHoE = eleHoE #H/E for electrons
        self.eleMissingHits = eleMissingHits #Missing hits for electrons
        self.eleChi2 = eleChi2 #Track chi squared for electrons' gsf tracks
        self.nMuonHits = nMuonHits #Number of matched muons stations (4 for electrons)
        self.nStations = nStations #Number of matched muons stations (4 for electrons)
        self.trkKink = trkKink #Tracker kink-finder
        self.caloCompatibility = caloCompatibility #Calorimetric compatibility
        self.globalTrackChi2 = globalTrackChi2 #Global track normalized chi2
        self.nChamberHits = nChamberHits #Number of muon chamber hits (-1 for electrons)
        self.isPFMuon = isPFMuon #1 if muon passes particle flow ID
        self.isGlobalMuon = isGlobalMuon #1 if muon is global muon
        self.isTrackerMuon = isTrackerMuon #1 if muon is tracker muon
        self.pixelHits = pixelHits #Number of pixel hits (-1 for electrons)
        self.trackerLayers = trackerLayers #Tracker Layers
        self.pixelLayers = pixelLayers #Pixel Layers
        self.mvaTTH = mvaTTH #Lepton MVA (ttH version)
        self.jetOverlapIdx = jetOverlapIdx #index of jet with overlapping PF constituents
        self.jetPtRatio = jetPtRatio #pt(lepton)/pt(nearest jet)
        self.jetBTagCSV = jetBTagCSV #btag of nearest jet
        self.jetDR = jetDR #deltaR(lepton, nearest jet)
        self.pfRelIso03 = pfRelIso03 #0.3 particle based iso
        self.pfRelIso04 = pfRelIso04 #0.4 particle based iso
        self.etaSc = etaSc #Electron supercluster pseudorapidity
        self.eleExpMissingInnerHits = eleExpMissingInnerHits #Electron expected missing inner hits
        self.eleooEmooP = eleooEmooP #Electron 1/E - 1/P
class primaryVertices:
    """
    first four PVs
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nprimaryVertices", 0)
        _x = getattr(tree, "primaryVertices_x", [None]*n)
        _y = getattr(tree, "primaryVertices_y", [None]*n)
        _z = getattr(tree, "primaryVertices_z", [None]*n)
        _isFake = getattr(tree, "primaryVertices_isFake", [None]*n)
        _ndof = getattr(tree, "primaryVertices_ndof", [None]*n)
        _Rho = getattr(tree, "primaryVertices_Rho", [None]*n)
        return [primaryVertices(_x[n], _y[n], _z[n], _isFake[n], _ndof[n], _Rho[n]) for n in range(n)]
    def __init__(self, x,y,z,isFake,ndof,Rho):
        self.x = x #
        self.y = y #
        self.z = z #
        self.isFake = isFake #
        self.ndof = ndof #
        self.Rho = Rho #
class softActivityJets:
    """
    jets made for soft activity
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nsoftActivityJets", 0)
        _pt = getattr(tree, "softActivityJets_pt", [None]*n)
        _eta = getattr(tree, "softActivityJets_eta", [None]*n)
        _phi = getattr(tree, "softActivityJets_phi", [None]*n)
        _mass = getattr(tree, "softActivityJets_mass", [None]*n)
        return [softActivityJets(_pt[n], _eta[n], _phi[n], _mass[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
class aJ3Cidx:
    """
    additional jet indices 3 cen  jets
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "naJ3Cidx", 0)
        _aJ3Cidx = getattr(tree, "aJ3Cidx", [None]*n);
        return [aJ3Cidx(_aJ3Cidx[n]) for n in range(n)]
    def __init__(self, aJ3Cidx):
        self.aJ3Cidx = aJ3Cidx #additional jet indices 3 cen  jets
class GenWZQuark:
    """
    Generated quarks from W/Z decays
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenWZQuark", 0)
        _pdgId = getattr(tree, "GenWZQuark_pdgId", [None]*n)
        _pt = getattr(tree, "GenWZQuark_pt", [None]*n)
        _eta = getattr(tree, "GenWZQuark_eta", [None]*n)
        _phi = getattr(tree, "GenWZQuark_phi", [None]*n)
        _mass = getattr(tree, "GenWZQuark_mass", [None]*n)
        _charge = getattr(tree, "GenWZQuark_charge", [None]*n)
        _status = getattr(tree, "GenWZQuark_status", [None]*n)
        return [GenWZQuark(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class GenBQuarkFromTop:
    """
    Generated bottom quarks from top decays
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenBQuarkFromTop", 0)
        _pdgId = getattr(tree, "GenBQuarkFromTop_pdgId", [None]*n)
        _pt = getattr(tree, "GenBQuarkFromTop_pt", [None]*n)
        _eta = getattr(tree, "GenBQuarkFromTop_eta", [None]*n)
        _phi = getattr(tree, "GenBQuarkFromTop_phi", [None]*n)
        _mass = getattr(tree, "GenBQuarkFromTop_mass", [None]*n)
        _charge = getattr(tree, "GenBQuarkFromTop_charge", [None]*n)
        _status = getattr(tree, "GenBQuarkFromTop_status", [None]*n)
        return [GenBQuarkFromTop(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class met_shifted_TauEnDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_TauEnDown_pt", None)
        _phi = getattr(tree, "met_shifted_TauEnDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_TauEnDown_sumEt", None)
        return met_shifted_TauEnDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
class met_shifted_TauEnUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_TauEnUp_pt", None)
        _phi = getattr(tree, "met_shifted_TauEnUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_TauEnUp_sumEt", None)
        return met_shifted_TauEnUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
class met_shifted_ElectronEnDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_ElectronEnDown_pt", None)
        _phi = getattr(tree, "met_shifted_ElectronEnDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_ElectronEnDown_sumEt", None)
        return met_shifted_ElectronEnDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
class met_shifted_JetEnDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_JetEnDown_pt", None)
        _phi = getattr(tree, "met_shifted_JetEnDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_JetEnDown_sumEt", None)
        return met_shifted_JetEnDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
class H3cj:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "H3cj_pt", None)
        _eta = getattr(tree, "H3cj_eta", None)
        _phi = getattr(tree, "H3cj_phi", None)
        _mass = getattr(tree, "H3cj_mass", None)
        return H3cj(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
class H:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "H_pt", None)
        _eta = getattr(tree, "H_eta", None)
        _phi = getattr(tree, "H_phi", None)
        _mass = getattr(tree, "H_mass", None)
        return H(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
class met_shifted_UnclusteredEnUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_UnclusteredEnUp_pt", None)
        _phi = getattr(tree, "met_shifted_UnclusteredEnUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_UnclusteredEnUp_sumEt", None)
        return met_shifted_UnclusteredEnUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
class met_shifted_UnclusteredEnDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_UnclusteredEnDown_pt", None)
        _phi = getattr(tree, "met_shifted_UnclusteredEnDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_UnclusteredEnDown_sumEt", None)
        return met_shifted_UnclusteredEnDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
class met_shifted_JetEnUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_JetEnUp_pt", None)
        _phi = getattr(tree, "met_shifted_JetEnUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_JetEnUp_sumEt", None)
        return met_shifted_JetEnUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
class met:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_pt", None)
        _eta = getattr(tree, "met_eta", None)
        _phi = getattr(tree, "met_phi", None)
        _mass = getattr(tree, "met_mass", None)
        _sumEt = getattr(tree, "met_sumEt", None)
        _genPt = getattr(tree, "met_genPt", None)
        _genPhi = getattr(tree, "met_genPhi", None)
        _genEta = getattr(tree, "met_genEta", None)
        return met(_pt, _eta, _phi, _mass, _sumEt, _genPt, _genPhi, _genEta)
    def __init__(self, pt,eta,phi,mass,sumEt,genPt,genPhi,genEta):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.sumEt = sumEt #
        self.genPt = genPt #
        self.genPhi = genPhi #
        self.genEta = genEta #
class met_shifted_JetResUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_JetResUp_pt", None)
        _phi = getattr(tree, "met_shifted_JetResUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_JetResUp_sumEt", None)
        return met_shifted_JetResUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
class met_shifted_JetResDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_JetResDown_pt", None)
        _phi = getattr(tree, "met_shifted_JetResDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_JetResDown_sumEt", None)
        return met_shifted_JetResDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
class HCSV:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCSV_pt", None)
        _eta = getattr(tree, "HCSV_eta", None)
        _phi = getattr(tree, "HCSV_phi", None)
        _mass = getattr(tree, "HCSV_mass", None)
        return HCSV(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
class met_shifted_MuonEnDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_MuonEnDown_pt", None)
        _phi = getattr(tree, "met_shifted_MuonEnDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_MuonEnDown_sumEt", None)
        return met_shifted_MuonEnDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
class met_shifted_ElectronEnUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_ElectronEnUp_pt", None)
        _phi = getattr(tree, "met_shifted_ElectronEnUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_ElectronEnUp_sumEt", None)
        return met_shifted_ElectronEnUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
class V:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "V_pt", None)
        _eta = getattr(tree, "V_eta", None)
        _phi = getattr(tree, "V_phi", None)
        _mass = getattr(tree, "V_mass", None)
        return V(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
class fakeMET:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "fakeMET_pt", None)
        _eta = getattr(tree, "fakeMET_eta", None)
        _phi = getattr(tree, "fakeMET_phi", None)
        _mass = getattr(tree, "fakeMET_mass", None)
        return fakeMET(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
class met_shifted_MuonEnUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_MuonEnUp_pt", None)
        _phi = getattr(tree, "met_shifted_MuonEnUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_MuonEnUp_sumEt", None)
        return met_shifted_MuonEnUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #

from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
class EventAnalyzer(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
    def process(self, event):
        event.GenBQuarkFromHafterISR = GenBQuarkFromHafterISR.make_array(event.input)
        event.GenHiggsBoson = GenHiggsBoson.make_array(event.input)
        event.hJidx_sortcsv = hJidx_sortcsv.make_array(event.input)
        event.aJCidx = aJCidx.make_array(event.input)
        event.GenLepFromTop = GenLepFromTop.make_array(event.input)
        event.GenVbosons = GenVbosons.make_array(event.input)
        event.GenBQuarkFromH = GenBQuarkFromH.make_array(event.input)
        event.hJCidx = hJCidx.make_array(event.input)
        event.GenTop = GenTop.make_array(event.input)
        event.aJidx = aJidx.make_array(event.input)
        event.GenLepFromTau = GenLepFromTau.make_array(event.input)
        event.aLeptons = aLeptons.make_array(event.input)
        event.GenNuFromTop = GenNuFromTop.make_array(event.input)
        event.DiscardedJet = DiscardedJet.make_array(event.input)
        event.selLeptons = selLeptons.make_array(event.input)
        event.TauGood = TauGood.make_array(event.input)
        event.hJ3Cidx = hJ3Cidx.make_array(event.input)
        event.hJidx = hJidx.make_array(event.input)
        event.GenLep = GenLep.make_array(event.input)
        event.GenJet = GenJet.make_array(event.input)
        event.Jet = Jet.make_array(event.input)
        event.vLeptons = vLeptons.make_array(event.input)
        event.primaryVertices = primaryVertices.make_array(event.input)
        event.softActivityJets = softActivityJets.make_array(event.input)
        event.aJ3Cidx = aJ3Cidx.make_array(event.input)
        event.GenWZQuark = GenWZQuark.make_array(event.input)
        event.GenBQuarkFromTop = GenBQuarkFromTop.make_array(event.input)
        event.met_shifted_TauEnDown = met_shifted_TauEnDown.make_obj(event.input)
        event.met_shifted_TauEnUp = met_shifted_TauEnUp.make_obj(event.input)
        event.met_shifted_ElectronEnDown = met_shifted_ElectronEnDown.make_obj(event.input)
        event.met_shifted_JetEnDown = met_shifted_JetEnDown.make_obj(event.input)
        event.H3cj = H3cj.make_obj(event.input)
        event.H = H.make_obj(event.input)
        event.met_shifted_UnclusteredEnUp = met_shifted_UnclusteredEnUp.make_obj(event.input)
        event.met_shifted_UnclusteredEnDown = met_shifted_UnclusteredEnDown.make_obj(event.input)
        event.met_shifted_JetEnUp = met_shifted_JetEnUp.make_obj(event.input)
        event.met = met.make_obj(event.input)
        event.met_shifted_JetResUp = met_shifted_JetResUp.make_obj(event.input)
        event.met_shifted_JetResDown = met_shifted_JetResDown.make_obj(event.input)
        event.HCSV = HCSV.make_obj(event.input)
        event.met_shifted_MuonEnDown = met_shifted_MuonEnDown.make_obj(event.input)
        event.met_shifted_ElectronEnUp = met_shifted_ElectronEnUp.make_obj(event.input)
        event.V = V.make_obj(event.input)
        event.fakeMET = fakeMET.make_obj(event.input)
        event.met_shifted_MuonEnUp = met_shifted_MuonEnUp.make_obj(event.input)
        event.Vtype = getattr(event.input, "Vtype", None)
        event.VtypeSim = getattr(event.input, "VtypeSim", None)
        event.VMt = getattr(event.input, "VMt", None)
        event.HVdPhi = getattr(event.input, "HVdPhi", None)
        event.fakeMET_sumet = getattr(event.input, "fakeMET_sumet", None)
        event.rho = getattr(event.input, "rho", None)
        event.deltaR_jj = getattr(event.input, "deltaR_jj", None)
        event.minDr3 = getattr(event.input, "minDr3", None)
        event.lheNj = getattr(event.input, "lheNj", None)
        event.lheNb = getattr(event.input, "lheNb", None)
        event.lheNc = getattr(event.input, "lheNc", None)
        event.lheNg = getattr(event.input, "lheNg", None)
        event.lheNl = getattr(event.input, "lheNl", None)
        event.lheV_pt = getattr(event.input, "lheV_pt", None)
        event.lheHT = getattr(event.input, "lheHT", None)
        event.genTTHtoTauTauDecayMode = getattr(event.input, "genTTHtoTauTauDecayMode", None)
        event.totSoftActivityJets = getattr(event.input, "totSoftActivityJets", None)
        event.ttCls = getattr(event.input, "ttCls", None)
        event.genHiggsDecayMode = getattr(event.input, "genHiggsDecayMode", None)
        event.bTagWeight_LFUp = getattr(event.input, "bTagWeight_LFUp", None)
        event.bTagWeight_Stats2Down = getattr(event.input, "bTagWeight_Stats2Down", None)
        event.bTagWeight_LFDown = getattr(event.input, "bTagWeight_LFDown", None)
        event.bTagWeight_HFUp = getattr(event.input, "bTagWeight_HFUp", None)
        event.bTagWeight_JESDown = getattr(event.input, "bTagWeight_JESDown", None)
        event.bTagWeight = getattr(event.input, "bTagWeight", None)
        event.bTagWeight_HFDown = getattr(event.input, "bTagWeight_HFDown", None)
        event.bTagWeight_Stats2Up = getattr(event.input, "bTagWeight_Stats2Up", None)
        event.bTagWeight_JESUp = getattr(event.input, "bTagWeight_JESUp", None)
        event.bTagWeight_Stats1Up = getattr(event.input, "bTagWeight_Stats1Up", None)
        event.bTagWeight_Stats1Down = getattr(event.input, "bTagWeight_Stats1Down", None)
