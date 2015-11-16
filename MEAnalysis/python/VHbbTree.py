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
class pileUpVertex_ptHat:
    """
    z position of hardest pile-up collisions
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "npileUpVertex_ptHat", 0)
        _pileUpVertex_ptHat = getattr(tree, "pileUpVertex_ptHat", [None]*n);
        return [pileUpVertex_ptHat(_pileUpVertex_ptHat[n]) for n in range(n)]
    def __init__(self, pileUpVertex_ptHat):
        self.pileUpVertex_ptHat = pileUpVertex_ptHat #z position of hardest pile-up collisions
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
class FatjetCA15pruned:
    """
    CA, R=1.5, pT > 200 GeV, pruned zcut=0.1, rcut=0.5, n=2
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nFatjetCA15pruned", 0)
        _pt = getattr(tree, "FatjetCA15pruned_pt", [None]*n)
        _eta = getattr(tree, "FatjetCA15pruned_eta", [None]*n)
        _phi = getattr(tree, "FatjetCA15pruned_phi", [None]*n)
        _mass = getattr(tree, "FatjetCA15pruned_mass", [None]*n)
        return [FatjetCA15pruned(_pt[n], _eta[n], _phi[n], _mass[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
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
class ajidxaddJetsdR08:
    """
    additional jet indices with Higgs formed adding cen jets if dR<0.8 from hJetsCSV
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "najidxaddJetsdR08", 0)
        _ajidxaddJetsdR08 = getattr(tree, "ajidxaddJetsdR08", [None]*n);
        return [ajidxaddJetsdR08(_ajidxaddJetsdR08[n]) for n in range(n)]
    def __init__(self, ajidxaddJetsdR08):
        self.ajidxaddJetsdR08 = ajidxaddJetsdR08 #additional jet indices with Higgs formed adding cen jets if dR<0.8 from hJetsCSV
class FatjetAK08pruned:
    """
    AK, R=0.8, pT > 200 GeV, pruned zcut=0.1, rcut=0.5, n=2
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nFatjetAK08pruned", 0)
        _pt = getattr(tree, "FatjetAK08pruned_pt", [None]*n)
        _eta = getattr(tree, "FatjetAK08pruned_eta", [None]*n)
        _phi = getattr(tree, "FatjetAK08pruned_phi", [None]*n)
        _mass = getattr(tree, "FatjetAK08pruned_mass", [None]*n)
        return [FatjetAK08pruned(_pt[n], _eta[n], _phi[n], _mass[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
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
        _wNuPt = getattr(tree, "GenJet_wNuPt", [None]*n)
        _wNuEta = getattr(tree, "GenJet_wNuEta", [None]*n)
        _wNuPhi = getattr(tree, "GenJet_wNuPhi", [None]*n)
        _wNuM = getattr(tree, "GenJet_wNuM", [None]*n)
        return [GenJet(_charge[n], _status[n], _pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _numBHadrons[n], _numCHadrons[n], _numBHadronsFromTop[n], _numCHadronsFromTop[n], _numBHadronsAfterTop[n], _numCHadronsAfterTop[n], _wNuPt[n], _wNuEta[n], _wNuPhi[n], _wNuM[n]) for n in range(n)]
    def __init__(self, charge,status,pdgId,pt,eta,phi,mass,numBHadrons,numCHadrons,numBHadronsFromTop,numCHadronsFromTop,numBHadronsAfterTop,numCHadronsAfterTop,wNuPt,wNuEta,wNuPhi,wNuM):
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
        self.wNuPt = wNuPt #pt of jet adding back the neutrinos
        self.wNuEta = wNuEta #eta of jet adding back the neutrinos
        self.wNuPhi = wNuPhi #phi of jet adding back the neutrinos
        self.wNuM = wNuM #mass of jet adding back the neutrinos
class SubjetCA15pruned:
    """
    Subjets of AK, R=1.5, pT > 200 GeV, pruned zcut=0.1, rcut=0.5, n=2
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nSubjetCA15pruned", 0)
        _pt = getattr(tree, "SubjetCA15pruned_pt", [None]*n)
        _eta = getattr(tree, "SubjetCA15pruned_eta", [None]*n)
        _phi = getattr(tree, "SubjetCA15pruned_phi", [None]*n)
        _mass = getattr(tree, "SubjetCA15pruned_mass", [None]*n)
        _btag = getattr(tree, "SubjetCA15pruned_btag", [None]*n)
        return [SubjetCA15pruned(_pt[n], _eta[n], _phi[n], _mass[n], _btag[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass,btag):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.btag = btag #CVS IVF V2 btag-score
class FatjetCA15ungroomed:
    """
    CA, R=1.5, pT > 200 GeV, no grooming
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nFatjetCA15ungroomed", 0)
        _pt = getattr(tree, "FatjetCA15ungroomed_pt", [None]*n)
        _eta = getattr(tree, "FatjetCA15ungroomed_eta", [None]*n)
        _phi = getattr(tree, "FatjetCA15ungroomed_phi", [None]*n)
        _mass = getattr(tree, "FatjetCA15ungroomed_mass", [None]*n)
        _tau1 = getattr(tree, "FatjetCA15ungroomed_tau1", [None]*n)
        _tau2 = getattr(tree, "FatjetCA15ungroomed_tau2", [None]*n)
        _tau3 = getattr(tree, "FatjetCA15ungroomed_tau3", [None]*n)
        _bbtag = getattr(tree, "FatjetCA15ungroomed_bbtag", [None]*n)
        _PFLepton_ptrel = getattr(tree, "FatjetCA15ungroomed_PFLepton_ptrel", [None]*n)
        _z_ratio = getattr(tree, "FatjetCA15ungroomed_z_ratio", [None]*n)
        _tau_dot = getattr(tree, "FatjetCA15ungroomed_tau_dot", [None]*n)
        _SV_mass_0 = getattr(tree, "FatjetCA15ungroomed_SV_mass_0", [None]*n)
        _SV_EnergyRatio_0 = getattr(tree, "FatjetCA15ungroomed_SV_EnergyRatio_0", [None]*n)
        _SV_EnergyRatio_1 = getattr(tree, "FatjetCA15ungroomed_SV_EnergyRatio_1", [None]*n)
        _PFLepton_IP2D = getattr(tree, "FatjetCA15ungroomed_PFLepton_IP2D", [None]*n)
        _tau_21 = getattr(tree, "FatjetCA15ungroomed_tau_21", [None]*n)
        _nSL = getattr(tree, "FatjetCA15ungroomed_nSL", [None]*n)
        _vertexNTracks = getattr(tree, "FatjetCA15ungroomed_vertexNTracks", [None]*n)
        return [FatjetCA15ungroomed(_pt[n], _eta[n], _phi[n], _mass[n], _tau1[n], _tau2[n], _tau3[n], _bbtag[n], _PFLepton_ptrel[n], _z_ratio[n], _tau_dot[n], _SV_mass_0[n], _SV_EnergyRatio_0[n], _SV_EnergyRatio_1[n], _PFLepton_IP2D[n], _tau_21[n], _nSL[n], _vertexNTracks[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass,tau1,tau2,tau3,bbtag,PFLepton_ptrel,z_ratio,tau_dot,SV_mass_0,SV_EnergyRatio_0,SV_EnergyRatio_1,PFLepton_IP2D,tau_21,nSL,vertexNTracks):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.tau1 = tau1 #Nsubjettiness (1 axis)
        self.tau2 = tau2 #Nsubjettiness (2 axes)
        self.tau3 = tau3 #Nsubjettiness (3 axes)
        self.bbtag = bbtag #Hbb b-tag score
        self.PFLepton_ptrel = PFLepton_ptrel #pt-rel of e/mu (for bb-tag)
        self.z_ratio = z_ratio #z-ratio (for bb-tag)
        self.tau_dot = tau_dot #tau_dot (for bb-tag)
        self.SV_mass_0 = SV_mass_0 #secondary vertex mass (for bb-tag)
        self.SV_EnergyRatio_0 = SV_EnergyRatio_0 #secondary vertex mass energy ratio 0 (for bb-tag)
        self.SV_EnergyRatio_1 = SV_EnergyRatio_1 #secondary vertex mass energy ratio 1 (for bb-tag)
        self.PFLepton_IP2D = PFLepton_IP2D #lepton IP2D (for bb-tag)
        self.tau_21 = tau_21 #nsubjettiness tau2/tau1 (for bb-tag)
        self.nSL = nSL #number of soft leptons (for bb-tag)
        self.vertexNTracks = vertexNTracks #number of tracks for vertex (for bb-tag)
class dRaddJetsdR08:
    """
    dR of add jet with Higgs formed adding cen jets if dR<0.8 from hJetsCSV
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "ndRaddJetsdR08", 0)
        _dRaddJetsdR08 = getattr(tree, "dRaddJetsdR08", [None]*n);
        return [dRaddJetsdR08(_dRaddJetsdR08[n]) for n in range(n)]
    def __init__(self, dRaddJetsdR08):
        self.dRaddJetsdR08 = dRaddJetsdR08 #dR of add jet with Higgs formed adding cen jets if dR<0.8 from hJetsCSV
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
class GenStatus2bHad:
    """
    Generated Status 2 b Hadrons
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenStatus2bHad", 0)
        _pdgId = getattr(tree, "GenStatus2bHad_pdgId", [None]*n)
        _pt = getattr(tree, "GenStatus2bHad_pt", [None]*n)
        _eta = getattr(tree, "GenStatus2bHad_eta", [None]*n)
        _phi = getattr(tree, "GenStatus2bHad_phi", [None]*n)
        _mass = getattr(tree, "GenStatus2bHad_mass", [None]*n)
        _charge = getattr(tree, "GenStatus2bHad_charge", [None]*n)
        _status = getattr(tree, "GenStatus2bHad_status", [None]*n)
        return [GenStatus2bHad(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
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
        _charge = getattr(tree, "GenTop_charge", [None]*n)
        _status = getattr(tree, "GenTop_status", [None]*n)
        _pdgId = getattr(tree, "GenTop_pdgId", [None]*n)
        _pt = getattr(tree, "GenTop_pt", [None]*n)
        _eta = getattr(tree, "GenTop_eta", [None]*n)
        _phi = getattr(tree, "GenTop_phi", [None]*n)
        _mass = getattr(tree, "GenTop_mass", [None]*n)
        _decayMode = getattr(tree, "GenTop_decayMode", [None]*n)
        return [GenTop(_charge[n], _status[n], _pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _decayMode[n]) for n in range(n)]
    def __init__(self, charge,status,pdgId,pt,eta,phi,mass,decayMode):
        self.charge = charge #
        self.status = status #
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.decayMode = decayMode #Generator level top decay mode: 0=leptonic, 1=hadronic, -1=not known
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
class FatjetCA15trimmed:
    """
    CA, R=1.5, pT > 200 GeV, trimmed r=0.2, f=0.06
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nFatjetCA15trimmed", 0)
        _pt = getattr(tree, "FatjetCA15trimmed_pt", [None]*n)
        _eta = getattr(tree, "FatjetCA15trimmed_eta", [None]*n)
        _phi = getattr(tree, "FatjetCA15trimmed_phi", [None]*n)
        _mass = getattr(tree, "FatjetCA15trimmed_mass", [None]*n)
        return [FatjetCA15trimmed(_pt[n], _eta[n], _phi[n], _mass[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
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
        _eleCutIdSpring15_25ns_v1 = getattr(tree, "aLeptons_eleCutIdSpring15_25ns_v1", [None]*n)
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
        _miniRelIso = getattr(tree, "aLeptons_miniRelIso", [None]*n)
        _tightCharge = getattr(tree, "aLeptons_tightCharge", [None]*n)
        _mcMatchId = getattr(tree, "aLeptons_mcMatchId", [None]*n)
        _mcMatchAny = getattr(tree, "aLeptons_mcMatchAny", [None]*n)
        _mcMatchTau = getattr(tree, "aLeptons_mcMatchTau", [None]*n)
        _mcPt = getattr(tree, "aLeptons_mcPt", [None]*n)
        _mediumMuonId = getattr(tree, "aLeptons_mediumMuonId", [None]*n)
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
        _mvaIdTrig = getattr(tree, "aLeptons_mvaIdTrig", [None]*n)
        _mvaIdTrigMediumResult = getattr(tree, "aLeptons_mvaIdTrigMediumResult", [None]*n)
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
        _dr03TkSumPt = getattr(tree, "aLeptons_dr03TkSumPt", [None]*n)
        _eleEcalClusterIso = getattr(tree, "aLeptons_eleEcalClusterIso", [None]*n)
        _eleHcalClusterIso = getattr(tree, "aLeptons_eleHcalClusterIso", [None]*n)
        return [aLeptons(_charge[n], _tightId[n], _eleCutIdCSA14_25ns_v1[n], _eleCutIdCSA14_50ns_v1[n], _eleCutIdSpring15_25ns_v1[n], _dxy[n], _dz[n], _edxy[n], _edz[n], _ip3d[n], _sip3d[n], _convVeto[n], _lostHits[n], _relIso03[n], _relIso04[n], _miniRelIso[n], _tightCharge[n], _mcMatchId[n], _mcMatchAny[n], _mcMatchTau[n], _mcPt[n], _mediumMuonId[n], _pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _looseIdSusy[n], _looseIdPOG[n], _chargedHadRelIso03[n], _chargedHadRelIso04[n], _eleSieie[n], _eleDEta[n], _eleDPhi[n], _eleHoE[n], _eleMissingHits[n], _eleChi2[n], _mvaIdTrig[n], _mvaIdTrigMediumResult[n], _nStations[n], _trkKink[n], _caloCompatibility[n], _globalTrackChi2[n], _nChamberHits[n], _isPFMuon[n], _isGlobalMuon[n], _isTrackerMuon[n], _pixelHits[n], _trackerLayers[n], _pixelLayers[n], _mvaTTH[n], _jetOverlapIdx[n], _jetPtRatio[n], _jetBTagCSV[n], _jetDR[n], _pfRelIso03[n], _pfRelIso04[n], _etaSc[n], _eleExpMissingInnerHits[n], _eleooEmooP[n], _dr03TkSumPt[n], _eleEcalClusterIso[n], _eleHcalClusterIso[n]) for n in range(n)]
    def __init__(self, charge,tightId,eleCutIdCSA14_25ns_v1,eleCutIdCSA14_50ns_v1,eleCutIdSpring15_25ns_v1,dxy,dz,edxy,edz,ip3d,sip3d,convVeto,lostHits,relIso03,relIso04,miniRelIso,tightCharge,mcMatchId,mcMatchAny,mcMatchTau,mcPt,mediumMuonId,pdgId,pt,eta,phi,mass,looseIdSusy,looseIdPOG,chargedHadRelIso03,chargedHadRelIso04,eleSieie,eleDEta,eleDPhi,eleHoE,eleMissingHits,eleChi2,mvaIdTrig,mvaIdTrigMediumResult,nStations,trkKink,caloCompatibility,globalTrackChi2,nChamberHits,isPFMuon,isGlobalMuon,isTrackerMuon,pixelHits,trackerLayers,pixelLayers,mvaTTH,jetOverlapIdx,jetPtRatio,jetBTagCSV,jetDR,pfRelIso03,pfRelIso04,etaSc,eleExpMissingInnerHits,eleooEmooP,dr03TkSumPt,eleEcalClusterIso,eleHcalClusterIso):
        self.charge = charge #
        self.tightId = tightId #POG Tight ID (for electrons it's configured in the analyzer)
        self.eleCutIdCSA14_25ns_v1 = eleCutIdCSA14_25ns_v1 #Electron cut-based id (POG CSA14_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.eleCutIdCSA14_50ns_v1 = eleCutIdCSA14_50ns_v1 #Electron cut-based id (POG CSA14_50ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.eleCutIdSpring15_25ns_v1 = eleCutIdSpring15_25ns_v1 #Electron cut-based id (POG Spring15_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
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
        self.miniRelIso = miniRelIso #PF Rel miniRel, pile-up corrected
        self.tightCharge = tightCharge #Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, 2 if ptError/pt < 0.20, 0 otherwise 
        self.mcMatchId = mcMatchId #Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake
        self.mcMatchAny = mcMatchAny #Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom
        self.mcMatchTau = mcMatchTau #True if the leptons comes from a tau
        self.mcPt = mcPt #p_{T} of associated gen lepton
        self.mediumMuonId = mediumMuonId #Muon POG Medium id
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
        self.mvaIdTrig = mvaIdTrig #EGamma POG MVA ID for triggering electrons; 1 for muons
        self.mvaIdTrigMediumResult = mvaIdTrigMediumResult #True if passes EGamma POG MVA ID for triggering electrons; True for muons
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
        self.jetOverlapIdx = jetOverlapIdx #index of jet with overlapping PF constituents. If idx>=1000, then idx = idx-1000 and refers to discarded jets.
        self.jetPtRatio = jetPtRatio #pt(lepton)/pt(nearest jet)
        self.jetBTagCSV = jetBTagCSV #btag of nearest jet
        self.jetDR = jetDR #deltaR(lepton, nearest jet)
        self.pfRelIso03 = pfRelIso03 #0.3 particle based iso
        self.pfRelIso04 = pfRelIso04 #0.4 particle based iso
        self.etaSc = etaSc #Electron supercluster pseudorapidity
        self.eleExpMissingInnerHits = eleExpMissingInnerHits #Electron expected missing inner hits
        self.eleooEmooP = eleooEmooP #Electron 1/E - 1/P
        self.dr03TkSumPt = dr03TkSumPt #Electron track sum pt
        self.eleEcalClusterIso = eleEcalClusterIso #Electron ecal cluster iso
        self.eleHcalClusterIso = eleHcalClusterIso #Electron hcal cluster iso
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
class FatjetAK08ungroomed:
    """
    AK, R=0.8, pT > 200 GeV, no grooming
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nFatjetAK08ungroomed", 0)
        _pt = getattr(tree, "FatjetAK08ungroomed_pt", [None]*n)
        _eta = getattr(tree, "FatjetAK08ungroomed_eta", [None]*n)
        _phi = getattr(tree, "FatjetAK08ungroomed_phi", [None]*n)
        _mass = getattr(tree, "FatjetAK08ungroomed_mass", [None]*n)
        _tau1 = getattr(tree, "FatjetAK08ungroomed_tau1", [None]*n)
        _tau2 = getattr(tree, "FatjetAK08ungroomed_tau2", [None]*n)
        _tau3 = getattr(tree, "FatjetAK08ungroomed_tau3", [None]*n)
        _msoftdrop = getattr(tree, "FatjetAK08ungroomed_msoftdrop", [None]*n)
        _mpruned = getattr(tree, "FatjetAK08ungroomed_mpruned", [None]*n)
        _mtrimmed = getattr(tree, "FatjetAK08ungroomed_mtrimmed", [None]*n)
        _mfiltered = getattr(tree, "FatjetAK08ungroomed_mfiltered", [None]*n)
        _bbtag = getattr(tree, "FatjetAK08ungroomed_bbtag", [None]*n)
        _PFLepton_ptrel = getattr(tree, "FatjetAK08ungroomed_PFLepton_ptrel", [None]*n)
        _z_ratio = getattr(tree, "FatjetAK08ungroomed_z_ratio", [None]*n)
        _tau_dot = getattr(tree, "FatjetAK08ungroomed_tau_dot", [None]*n)
        _SV_mass_0 = getattr(tree, "FatjetAK08ungroomed_SV_mass_0", [None]*n)
        _SV_EnergyRatio_0 = getattr(tree, "FatjetAK08ungroomed_SV_EnergyRatio_0", [None]*n)
        _SV_EnergyRatio_1 = getattr(tree, "FatjetAK08ungroomed_SV_EnergyRatio_1", [None]*n)
        _PFLepton_IP2D = getattr(tree, "FatjetAK08ungroomed_PFLepton_IP2D", [None]*n)
        _tau_21 = getattr(tree, "FatjetAK08ungroomed_tau_21", [None]*n)
        _nSL = getattr(tree, "FatjetAK08ungroomed_nSL", [None]*n)
        _vertexNTracks = getattr(tree, "FatjetAK08ungroomed_vertexNTracks", [None]*n)
        return [FatjetAK08ungroomed(_pt[n], _eta[n], _phi[n], _mass[n], _tau1[n], _tau2[n], _tau3[n], _msoftdrop[n], _mpruned[n], _mtrimmed[n], _mfiltered[n], _bbtag[n], _PFLepton_ptrel[n], _z_ratio[n], _tau_dot[n], _SV_mass_0[n], _SV_EnergyRatio_0[n], _SV_EnergyRatio_1[n], _PFLepton_IP2D[n], _tau_21[n], _nSL[n], _vertexNTracks[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass,tau1,tau2,tau3,msoftdrop,mpruned,mtrimmed,mfiltered,bbtag,PFLepton_ptrel,z_ratio,tau_dot,SV_mass_0,SV_EnergyRatio_0,SV_EnergyRatio_1,PFLepton_IP2D,tau_21,nSL,vertexNTracks):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.tau1 = tau1 #Nsubjettiness (1 axis)
        self.tau2 = tau2 #Nsubjettiness (2 axes)
        self.tau3 = tau3 #Nsubjettiness (3 axes)
        self.msoftdrop = msoftdrop #Softdrop Mass
        self.mpruned = mpruned #Pruned Mass
        self.mtrimmed = mtrimmed #Trimmed Mass
        self.mfiltered = mfiltered #Filtered Mass
        self.bbtag = bbtag #Hbb b-tag score
        self.PFLepton_ptrel = PFLepton_ptrel #pt-rel of e/mu (for bb-tag)
        self.z_ratio = z_ratio #z-ratio (for bb-tag)
        self.tau_dot = tau_dot #tau_dot (for bb-tag)
        self.SV_mass_0 = SV_mass_0 #secondary vertex mass (for bb-tag)
        self.SV_EnergyRatio_0 = SV_EnergyRatio_0 #secondary vertex mass energy ratio 0 (for bb-tag)
        self.SV_EnergyRatio_1 = SV_EnergyRatio_1 #secondary vertex mass energy ratio 1 (for bb-tag)
        self.PFLepton_IP2D = PFLepton_IP2D #lepton IP2D (for bb-tag)
        self.tau_21 = tau_21 #nsubjettiness tau2/tau1 (for bb-tag)
        self.nSL = nSL #number of soft leptons (for bb-tag)
        self.vertexNTracks = vertexNTracks #number of tracks for vertex (for bb-tag)
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
        _eleCutIdSpring15_25ns_v1 = getattr(tree, "selLeptons_eleCutIdSpring15_25ns_v1", [None]*n)
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
        _miniRelIso = getattr(tree, "selLeptons_miniRelIso", [None]*n)
        _tightCharge = getattr(tree, "selLeptons_tightCharge", [None]*n)
        _mcMatchId = getattr(tree, "selLeptons_mcMatchId", [None]*n)
        _mcMatchAny = getattr(tree, "selLeptons_mcMatchAny", [None]*n)
        _mcMatchTau = getattr(tree, "selLeptons_mcMatchTau", [None]*n)
        _mcPt = getattr(tree, "selLeptons_mcPt", [None]*n)
        _mediumMuonId = getattr(tree, "selLeptons_mediumMuonId", [None]*n)
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
        _mvaIdTrig = getattr(tree, "selLeptons_mvaIdTrig", [None]*n)
        _mvaIdTrigMediumResult = getattr(tree, "selLeptons_mvaIdTrigMediumResult", [None]*n)
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
        _dr03TkSumPt = getattr(tree, "selLeptons_dr03TkSumPt", [None]*n)
        _eleEcalClusterIso = getattr(tree, "selLeptons_eleEcalClusterIso", [None]*n)
        _eleHcalClusterIso = getattr(tree, "selLeptons_eleHcalClusterIso", [None]*n)
        return [selLeptons(_charge[n], _tightId[n], _eleCutIdCSA14_25ns_v1[n], _eleCutIdCSA14_50ns_v1[n], _eleCutIdSpring15_25ns_v1[n], _dxy[n], _dz[n], _edxy[n], _edz[n], _ip3d[n], _sip3d[n], _convVeto[n], _lostHits[n], _relIso03[n], _relIso04[n], _miniRelIso[n], _tightCharge[n], _mcMatchId[n], _mcMatchAny[n], _mcMatchTau[n], _mcPt[n], _mediumMuonId[n], _pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _looseIdSusy[n], _looseIdPOG[n], _chargedHadRelIso03[n], _chargedHadRelIso04[n], _eleSieie[n], _eleDEta[n], _eleDPhi[n], _eleHoE[n], _eleMissingHits[n], _eleChi2[n], _mvaIdTrig[n], _mvaIdTrigMediumResult[n], _nStations[n], _trkKink[n], _caloCompatibility[n], _globalTrackChi2[n], _nChamberHits[n], _isPFMuon[n], _isGlobalMuon[n], _isTrackerMuon[n], _pixelHits[n], _trackerLayers[n], _pixelLayers[n], _mvaTTH[n], _jetOverlapIdx[n], _jetPtRatio[n], _jetBTagCSV[n], _jetDR[n], _pfRelIso03[n], _pfRelIso04[n], _etaSc[n], _eleExpMissingInnerHits[n], _eleooEmooP[n], _dr03TkSumPt[n], _eleEcalClusterIso[n], _eleHcalClusterIso[n]) for n in range(n)]
    def __init__(self, charge,tightId,eleCutIdCSA14_25ns_v1,eleCutIdCSA14_50ns_v1,eleCutIdSpring15_25ns_v1,dxy,dz,edxy,edz,ip3d,sip3d,convVeto,lostHits,relIso03,relIso04,miniRelIso,tightCharge,mcMatchId,mcMatchAny,mcMatchTau,mcPt,mediumMuonId,pdgId,pt,eta,phi,mass,looseIdSusy,looseIdPOG,chargedHadRelIso03,chargedHadRelIso04,eleSieie,eleDEta,eleDPhi,eleHoE,eleMissingHits,eleChi2,mvaIdTrig,mvaIdTrigMediumResult,nStations,trkKink,caloCompatibility,globalTrackChi2,nChamberHits,isPFMuon,isGlobalMuon,isTrackerMuon,pixelHits,trackerLayers,pixelLayers,mvaTTH,jetOverlapIdx,jetPtRatio,jetBTagCSV,jetDR,pfRelIso03,pfRelIso04,etaSc,eleExpMissingInnerHits,eleooEmooP,dr03TkSumPt,eleEcalClusterIso,eleHcalClusterIso):
        self.charge = charge #
        self.tightId = tightId #POG Tight ID (for electrons it's configured in the analyzer)
        self.eleCutIdCSA14_25ns_v1 = eleCutIdCSA14_25ns_v1 #Electron cut-based id (POG CSA14_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.eleCutIdCSA14_50ns_v1 = eleCutIdCSA14_50ns_v1 #Electron cut-based id (POG CSA14_50ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.eleCutIdSpring15_25ns_v1 = eleCutIdSpring15_25ns_v1 #Electron cut-based id (POG Spring15_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
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
        self.miniRelIso = miniRelIso #PF Rel miniRel, pile-up corrected
        self.tightCharge = tightCharge #Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, 2 if ptError/pt < 0.20, 0 otherwise 
        self.mcMatchId = mcMatchId #Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake
        self.mcMatchAny = mcMatchAny #Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom
        self.mcMatchTau = mcMatchTau #True if the leptons comes from a tau
        self.mcPt = mcPt #p_{T} of associated gen lepton
        self.mediumMuonId = mediumMuonId #Muon POG Medium id
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
        self.mvaIdTrig = mvaIdTrig #EGamma POG MVA ID for triggering electrons; 1 for muons
        self.mvaIdTrigMediumResult = mvaIdTrigMediumResult #True if passes EGamma POG MVA ID for triggering electrons; True for muons
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
        self.jetOverlapIdx = jetOverlapIdx #index of jet with overlapping PF constituents. If idx>=1000, then idx = idx-1000 and refers to discarded jets.
        self.jetPtRatio = jetPtRatio #pt(lepton)/pt(nearest jet)
        self.jetBTagCSV = jetBTagCSV #btag of nearest jet
        self.jetDR = jetDR #deltaR(lepton, nearest jet)
        self.pfRelIso03 = pfRelIso03 #0.3 particle based iso
        self.pfRelIso04 = pfRelIso04 #0.4 particle based iso
        self.etaSc = etaSc #Electron supercluster pseudorapidity
        self.eleExpMissingInnerHits = eleExpMissingInnerHits #Electron expected missing inner hits
        self.eleooEmooP = eleooEmooP #Electron 1/E - 1/P
        self.dr03TkSumPt = dr03TkSumPt #Electron track sum pt
        self.eleEcalClusterIso = eleEcalClusterIso #Electron ecal cluster iso
        self.eleHcalClusterIso = eleHcalClusterIso #Electron hcal cluster iso
class GenHiggsSisters:
    """
    Sisters of the Higgs bosons
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenHiggsSisters", 0)
        _pdgId = getattr(tree, "GenHiggsSisters_pdgId", [None]*n)
        _pt = getattr(tree, "GenHiggsSisters_pt", [None]*n)
        _eta = getattr(tree, "GenHiggsSisters_eta", [None]*n)
        _phi = getattr(tree, "GenHiggsSisters_phi", [None]*n)
        _mass = getattr(tree, "GenHiggsSisters_mass", [None]*n)
        _charge = getattr(tree, "GenHiggsSisters_charge", [None]*n)
        _status = getattr(tree, "GenHiggsSisters_status", [None]*n)
        return [GenHiggsSisters(_pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _charge[n], _status[n]) for n in range(n)]
    def __init__(self, pdgId,pt,eta,phi,mass,charge,status):
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.charge = charge #
        self.status = status #
class hjidxaddJetsdR08:
    """
    Higgs jet indices with Higgs formed adding cen jets if dR<0.8 from hJetsCSV
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nhjidxaddJetsdR08", 0)
        _hjidxaddJetsdR08 = getattr(tree, "hjidxaddJetsdR08", [None]*n);
        return [hjidxaddJetsdR08(_hjidxaddJetsdR08[n]) for n in range(n)]
    def __init__(self, hjidxaddJetsdR08):
        self.hjidxaddJetsdR08 = hjidxaddJetsdR08 #Higgs jet indices with Higgs formed adding cen jets if dR<0.8 from hJetsCSV
class softActivityVHJets:
    """
    jets made for soft activity VH version
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nsoftActivityVHJets", 0)
        _pt = getattr(tree, "softActivityVHJets_pt", [None]*n)
        _eta = getattr(tree, "softActivityVHJets_eta", [None]*n)
        _phi = getattr(tree, "softActivityVHJets_phi", [None]*n)
        _mass = getattr(tree, "softActivityVHJets_mass", [None]*n)
        return [softActivityVHJets(_pt[n], _eta[n], _phi[n], _mass[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
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
        _corr_JERUp = getattr(tree, "DiscardedJet_corr_JERUp", [None]*n)
        _corr_JERDown = getattr(tree, "DiscardedJet_corr_JERDown", [None]*n)
        _corr_JER = getattr(tree, "DiscardedJet_corr_JER", [None]*n)
        _pt = getattr(tree, "DiscardedJet_pt", [None]*n)
        _eta = getattr(tree, "DiscardedJet_eta", [None]*n)
        _phi = getattr(tree, "DiscardedJet_phi", [None]*n)
        _mass = getattr(tree, "DiscardedJet_mass", [None]*n)
        _idxFirstTauMatch = getattr(tree, "DiscardedJet_idxFirstTauMatch", [None]*n)
        _heppyFlavour = getattr(tree, "DiscardedJet_heppyFlavour", [None]*n)
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
        _leptonDeltaPhi = getattr(tree, "DiscardedJet_leptonDeltaPhi", [None]*n)
        _leptonDeltaEta = getattr(tree, "DiscardedJet_leptonDeltaEta", [None]*n)
        _vtxMass = getattr(tree, "DiscardedJet_vtxMass", [None]*n)
        _vtxNtracks = getattr(tree, "DiscardedJet_vtxNtracks", [None]*n)
        _vtxPt = getattr(tree, "DiscardedJet_vtxPt", [None]*n)
        _vtx3DSig = getattr(tree, "DiscardedJet_vtx3DSig", [None]*n)
        _vtx3DVal = getattr(tree, "DiscardedJet_vtx3DVal", [None]*n)
        _vtxPosX = getattr(tree, "DiscardedJet_vtxPosX", [None]*n)
        _vtxPosY = getattr(tree, "DiscardedJet_vtxPosY", [None]*n)
        _vtxPosZ = getattr(tree, "DiscardedJet_vtxPosZ", [None]*n)
        _pullVectorPhi = getattr(tree, "DiscardedJet_pullVectorPhi", [None]*n)
        _pullVectorMag = getattr(tree, "DiscardedJet_pullVectorMag", [None]*n)
        _qgl = getattr(tree, "DiscardedJet_qgl", [None]*n)
        _ptd = getattr(tree, "DiscardedJet_ptd", [None]*n)
        _axis2 = getattr(tree, "DiscardedJet_axis2", [None]*n)
        _mult = getattr(tree, "DiscardedJet_mult", [None]*n)
        _numberOfDaughters = getattr(tree, "DiscardedJet_numberOfDaughters", [None]*n)
        _btagIdx = getattr(tree, "DiscardedJet_btagIdx", [None]*n)
        _mcIdx = getattr(tree, "DiscardedJet_mcIdx", [None]*n)
        _pt_reg = getattr(tree, "DiscardedJet_pt_reg", [None]*n)
        _pt_regVBF = getattr(tree, "DiscardedJet_pt_regVBF", [None]*n)
        _blike_VBF = getattr(tree, "DiscardedJet_blike_VBF", [None]*n)
        _bTagWeightJESUp = getattr(tree, "DiscardedJet_bTagWeightJESUp", [None]*n)
        _bTagWeightJESDown = getattr(tree, "DiscardedJet_bTagWeightJESDown", [None]*n)
        _bTagWeightLFUp = getattr(tree, "DiscardedJet_bTagWeightLFUp", [None]*n)
        _bTagWeightLFDown = getattr(tree, "DiscardedJet_bTagWeightLFDown", [None]*n)
        _bTagWeightHFUp = getattr(tree, "DiscardedJet_bTagWeightHFUp", [None]*n)
        _bTagWeightHFDown = getattr(tree, "DiscardedJet_bTagWeightHFDown", [None]*n)
        _bTagWeightStats1Up = getattr(tree, "DiscardedJet_bTagWeightStats1Up", [None]*n)
        _bTagWeightStats1Down = getattr(tree, "DiscardedJet_bTagWeightStats1Down", [None]*n)
        _bTagWeightStats2Up = getattr(tree, "DiscardedJet_bTagWeightStats2Up", [None]*n)
        _bTagWeightStats2Down = getattr(tree, "DiscardedJet_bTagWeightStats2Down", [None]*n)
        _bTagWeightcErr1Up = getattr(tree, "DiscardedJet_bTagWeightcErr1Up", [None]*n)
        _bTagWeightcErr1Down = getattr(tree, "DiscardedJet_bTagWeightcErr1Down", [None]*n)
        _bTagWeightcErr2Up = getattr(tree, "DiscardedJet_bTagWeightcErr2Up", [None]*n)
        _bTagWeightcErr2Down = getattr(tree, "DiscardedJet_bTagWeightcErr2Down", [None]*n)
        _bTagWeight = getattr(tree, "DiscardedJet_bTagWeight", [None]*n)
        return [DiscardedJet(_id[n], _puId[n], _btagCSV[n], _btagCMVA[n], _rawPt[n], _mcPt[n], _mcFlavour[n], _mcMatchId[n], _corr_JECUp[n], _corr_JECDown[n], _corr[n], _corr_JERUp[n], _corr_JERDown[n], _corr_JER[n], _pt[n], _eta[n], _phi[n], _mass[n], _idxFirstTauMatch[n], _heppyFlavour[n], _hadronFlavour[n], _btagBDT[n], _btagProb[n], _btagBProb[n], _btagSoftEl[n], _btagSoftMu[n], _btagnew[n], _btagCSVV0[n], _chHEF[n], _neHEF[n], _chEmEF[n], _neEmEF[n], _chMult[n], _leadTrackPt[n], _mcEta[n], _mcPhi[n], _mcM[n], _leptonPdgId[n], _leptonPt[n], _leptonPtRel[n], _leptonPtRelInv[n], _leptonDeltaR[n], _leptonDeltaPhi[n], _leptonDeltaEta[n], _vtxMass[n], _vtxNtracks[n], _vtxPt[n], _vtx3DSig[n], _vtx3DVal[n], _vtxPosX[n], _vtxPosY[n], _vtxPosZ[n], _pullVectorPhi[n], _pullVectorMag[n], _qgl[n], _ptd[n], _axis2[n], _mult[n], _numberOfDaughters[n], _btagIdx[n], _mcIdx[n], _pt_reg[n], _pt_regVBF[n], _blike_VBF[n], _bTagWeightJESUp[n], _bTagWeightJESDown[n], _bTagWeightLFUp[n], _bTagWeightLFDown[n], _bTagWeightHFUp[n], _bTagWeightHFDown[n], _bTagWeightStats1Up[n], _bTagWeightStats1Down[n], _bTagWeightStats2Up[n], _bTagWeightStats2Down[n], _bTagWeightcErr1Up[n], _bTagWeightcErr1Down[n], _bTagWeightcErr2Up[n], _bTagWeightcErr2Down[n], _bTagWeight[n]) for n in range(n)]
    def __init__(self, id,puId,btagCSV,btagCMVA,rawPt,mcPt,mcFlavour,mcMatchId,corr_JECUp,corr_JECDown,corr,corr_JERUp,corr_JERDown,corr_JER,pt,eta,phi,mass,idxFirstTauMatch,heppyFlavour,hadronFlavour,btagBDT,btagProb,btagBProb,btagSoftEl,btagSoftMu,btagnew,btagCSVV0,chHEF,neHEF,chEmEF,neEmEF,chMult,leadTrackPt,mcEta,mcPhi,mcM,leptonPdgId,leptonPt,leptonPtRel,leptonPtRelInv,leptonDeltaR,leptonDeltaPhi,leptonDeltaEta,vtxMass,vtxNtracks,vtxPt,vtx3DSig,vtx3DVal,vtxPosX,vtxPosY,vtxPosZ,pullVectorPhi,pullVectorMag,qgl,ptd,axis2,mult,numberOfDaughters,btagIdx,mcIdx,pt_reg,pt_regVBF,blike_VBF,bTagWeightJESUp,bTagWeightJESDown,bTagWeightLFUp,bTagWeightLFDown,bTagWeightHFUp,bTagWeightHFDown,bTagWeightStats1Up,bTagWeightStats1Down,bTagWeightStats2Up,bTagWeightStats2Down,bTagWeightcErr1Up,bTagWeightcErr1Down,bTagWeightcErr2Up,bTagWeightcErr2Down,bTagWeight):
        self.id = id #POG Loose jet ID
        self.puId = puId #puId (full MVA, loose WP, 5.3.X training on AK5PFchs: the only thing that is available now)
        self.btagCSV = btagCSV #CSV-IVF v2 discriminator
        self.btagCMVA = btagCMVA #CMVA discriminator
        self.rawPt = rawPt #p_{T} before JEC
        self.mcPt = mcPt #p_{T} of associated gen jet
        self.mcFlavour = mcFlavour #parton flavour (physics definition, i.e. including b's from shower)
        self.mcMatchId = mcMatchId #Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake
        self.corr_JECUp = corr_JECUp #pt correction from JEC up
        self.corr_JECDown = corr_JECDown #pt correction from JEC down
        self.corr = corr #pt correction from JEC
        self.corr_JERUp = corr_JERUp #pt correction from JER up
        self.corr_JERDown = corr_JERDown #pt correction from JER down 
        self.corr_JER = corr_JER #pt correction from JER
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.idxFirstTauMatch = idxFirstTauMatch #index of the first matching tau
        self.heppyFlavour = heppyFlavour #heppy-style match to gen quarks
        self.hadronFlavour = hadronFlavour #hadron flavour (ghost matching to B/C hadrons)
        self.btagBDT = btagBDT #combined super-btag
        self.btagProb = btagProb #jet probability b-tag
        self.btagBProb = btagBProb #jet b-probability b-tag
        self.btagSoftEl = btagSoftEl #soft electron b-tag
        self.btagSoftMu = btagSoftMu #soft muon b-tag
        self.btagnew = btagnew #newest btag discriminator
        self.btagCSVV0 = btagCSVV0 #should be the old CSV discriminator with AVR vertices
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
        self.leptonDeltaPhi = leptonDeltaPhi #deltaPhi of the first associated lepton
        self.leptonDeltaEta = leptonDeltaEta #deltaEta of the first associated lepton
        self.vtxMass = vtxMass #vtxMass from btag
        self.vtxNtracks = vtxNtracks #number of tracks at vertex from btag
        self.vtxPt = vtxPt #pt of vertex from btag
        self.vtx3DSig = vtx3DSig #decay len significance of vertex from btag
        self.vtx3DVal = vtx3DVal #decay len of vertex from btag
        self.vtxPosX = vtxPosX #X coord of vertex from btag
        self.vtxPosY = vtxPosY #Y coord of vertex from btag
        self.vtxPosZ = vtxPosZ #Z coord of vertex from btag
        self.pullVectorPhi = pullVectorPhi #pull angle phi in the phi eta plane
        self.pullVectorMag = pullVectorMag #pull angle magnitude
        self.qgl = qgl #QG Likelihood
        self.ptd = ptd #QG input variable: ptD
        self.axis2 = axis2 #QG input variable: axis2
        self.mult = mult #QG input variable: total multiplicity
        self.numberOfDaughters = numberOfDaughters #number of daughters
        self.btagIdx = btagIdx #ranking in btag
        self.mcIdx = mcIdx #index of the matching gen jet
        self.pt_reg = pt_reg #Regression
        self.pt_regVBF = pt_regVBF #Regression for VBF
        self.blike_VBF = blike_VBF #VBF blikelihood for SingleBtag dataset
        self.bTagWeightJESUp = bTagWeightJESUp #b-tag CSV weight, variating JES Up
        self.bTagWeightJESDown = bTagWeightJESDown #b-tag CSV weight, variating JES Down
        self.bTagWeightLFUp = bTagWeightLFUp #b-tag CSV weight, variating LF Up
        self.bTagWeightLFDown = bTagWeightLFDown #b-tag CSV weight, variating LF Down
        self.bTagWeightHFUp = bTagWeightHFUp #b-tag CSV weight, variating HF Up
        self.bTagWeightHFDown = bTagWeightHFDown #b-tag CSV weight, variating HF Down
        self.bTagWeightStats1Up = bTagWeightStats1Up #b-tag CSV weight, variating Stats1 Up
        self.bTagWeightStats1Down = bTagWeightStats1Down #b-tag CSV weight, variating Stats1 Down
        self.bTagWeightStats2Up = bTagWeightStats2Up #b-tag CSV weight, variating Stats2 Up
        self.bTagWeightStats2Down = bTagWeightStats2Down #b-tag CSV weight, variating Stats2 Down
        self.bTagWeightcErr1Up = bTagWeightcErr1Up #b-tag CSV weight, variating cErr1 Up
        self.bTagWeightcErr1Down = bTagWeightcErr1Down #b-tag CSV weight, variating cErr1 Down
        self.bTagWeightcErr2Up = bTagWeightcErr2Up #b-tag CSV weight, variating cErr2 Up
        self.bTagWeightcErr2Down = bTagWeightcErr2Down #b-tag CSV weight, variating cErr2 Down
        self.bTagWeight = bTagWeight #b-tag CSV weight, nominal
class SubjetAK08pruned:
    """
    Subjets of AK, R=0.8, pT > 200 GeV, pruned zcut=0.1, rcut=0.5, n=2
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nSubjetAK08pruned", 0)
        _pt = getattr(tree, "SubjetAK08pruned_pt", [None]*n)
        _eta = getattr(tree, "SubjetAK08pruned_eta", [None]*n)
        _phi = getattr(tree, "SubjetAK08pruned_phi", [None]*n)
        _mass = getattr(tree, "SubjetAK08pruned_mass", [None]*n)
        _btag = getattr(tree, "SubjetAK08pruned_btag", [None]*n)
        return [SubjetAK08pruned(_pt[n], _eta[n], _phi[n], _mass[n], _btag[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass,btag):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.btag = btag #CVS IVF V2 btag-score
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
class SubjetAK08softdrop:
    """
    Subjets of AK, R=0.8 softdrop
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nSubjetAK08softdrop", 0)
        _pt = getattr(tree, "SubjetAK08softdrop_pt", [None]*n)
        _eta = getattr(tree, "SubjetAK08softdrop_eta", [None]*n)
        _phi = getattr(tree, "SubjetAK08softdrop_phi", [None]*n)
        _mass = getattr(tree, "SubjetAK08softdrop_mass", [None]*n)
        _btag = getattr(tree, "SubjetAK08softdrop_btag", [None]*n)
        return [SubjetAK08softdrop(_pt[n], _eta[n], _phi[n], _mass[n], _btag[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass,btag):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.btag = btag #CVS IVF V2 btag-score
class GenHadTaus:
    """
    Generator level hadronic tau decays
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nGenHadTaus", 0)
        _charge = getattr(tree, "GenHadTaus_charge", [None]*n)
        _status = getattr(tree, "GenHadTaus_status", [None]*n)
        _pdgId = getattr(tree, "GenHadTaus_pdgId", [None]*n)
        _pt = getattr(tree, "GenHadTaus_pt", [None]*n)
        _eta = getattr(tree, "GenHadTaus_eta", [None]*n)
        _phi = getattr(tree, "GenHadTaus_phi", [None]*n)
        _mass = getattr(tree, "GenHadTaus_mass", [None]*n)
        _decayMode = getattr(tree, "GenHadTaus_decayMode", [None]*n)
        return [GenHadTaus(_charge[n], _status[n], _pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _decayMode[n]) for n in range(n)]
    def __init__(self, charge,status,pdgId,pt,eta,phi,mass,decayMode):
        self.charge = charge #
        self.status = status #
        self.pdgId = pdgId #
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.decayMode = decayMode #Generator level tau decay mode
class httCandidates:
    """
    OptimalR HEPTopTagger Candidates
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nhttCandidates", 0)
        _pt = getattr(tree, "httCandidates_pt", [None]*n)
        _eta = getattr(tree, "httCandidates_eta", [None]*n)
        _phi = getattr(tree, "httCandidates_phi", [None]*n)
        _mass = getattr(tree, "httCandidates_mass", [None]*n)
        _fRec = getattr(tree, "httCandidates_fRec", [None]*n)
        _Ropt = getattr(tree, "httCandidates_Ropt", [None]*n)
        _RoptCalc = getattr(tree, "httCandidates_RoptCalc", [None]*n)
        _ptForRoptCalc = getattr(tree, "httCandidates_ptForRoptCalc", [None]*n)
        _sjW1pt = getattr(tree, "httCandidates_sjW1pt", [None]*n)
        _sjW1eta = getattr(tree, "httCandidates_sjW1eta", [None]*n)
        _sjW1phi = getattr(tree, "httCandidates_sjW1phi", [None]*n)
        _sjW1mass = getattr(tree, "httCandidates_sjW1mass", [None]*n)
        _sjW1btag = getattr(tree, "httCandidates_sjW1btag", [None]*n)
        _sjW2pt = getattr(tree, "httCandidates_sjW2pt", [None]*n)
        _sjW2eta = getattr(tree, "httCandidates_sjW2eta", [None]*n)
        _sjW2phi = getattr(tree, "httCandidates_sjW2phi", [None]*n)
        _sjW2mass = getattr(tree, "httCandidates_sjW2mass", [None]*n)
        _sjW2btag = getattr(tree, "httCandidates_sjW2btag", [None]*n)
        _sjNonWpt = getattr(tree, "httCandidates_sjNonWpt", [None]*n)
        _sjNonWeta = getattr(tree, "httCandidates_sjNonWeta", [None]*n)
        _sjNonWphi = getattr(tree, "httCandidates_sjNonWphi", [None]*n)
        _sjNonWmass = getattr(tree, "httCandidates_sjNonWmass", [None]*n)
        _sjNonWbtag = getattr(tree, "httCandidates_sjNonWbtag", [None]*n)
        return [httCandidates(_pt[n], _eta[n], _phi[n], _mass[n], _fRec[n], _Ropt[n], _RoptCalc[n], _ptForRoptCalc[n], _sjW1pt[n], _sjW1eta[n], _sjW1phi[n], _sjW1mass[n], _sjW1btag[n], _sjW2pt[n], _sjW2eta[n], _sjW2phi[n], _sjW2mass[n], _sjW2btag[n], _sjNonWpt[n], _sjNonWeta[n], _sjNonWphi[n], _sjNonWmass[n], _sjNonWbtag[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass,fRec,Ropt,RoptCalc,ptForRoptCalc,sjW1pt,sjW1eta,sjW1phi,sjW1mass,sjW1btag,sjW2pt,sjW2eta,sjW2phi,sjW2mass,sjW2btag,sjNonWpt,sjNonWeta,sjNonWphi,sjNonWmass,sjNonWbtag):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.fRec = fRec #relative W width
        self.Ropt = Ropt #optimal value of R
        self.RoptCalc = RoptCalc #expected value of optimal R
        self.ptForRoptCalc = ptForRoptCalc #pT used for calculation of RoptCalc
        self.sjW1pt = sjW1pt #Leading W Subjet pT
        self.sjW1eta = sjW1eta #Leading W Subjet eta
        self.sjW1phi = sjW1phi #Leading W Subjet phi
        self.sjW1mass = sjW1mass #Leading W Subjet mass
        self.sjW1btag = sjW1btag #Leading W Subjet btag
        self.sjW2pt = sjW2pt #Second Subjet pT
        self.sjW2eta = sjW2eta #Second Subjet eta
        self.sjW2phi = sjW2phi #Second Subjet phi
        self.sjW2mass = sjW2mass #Second Subjet mass
        self.sjW2btag = sjW2btag #Second Subjet btag
        self.sjNonWpt = sjNonWpt #Non-W Subjet pT
        self.sjNonWeta = sjNonWeta #Non-W Subjet eta
        self.sjNonWphi = sjNonWphi #Non-W Subjet phi
        self.sjNonWmass = sjNonWmass #Non-W Subjet mass
        self.sjNonWbtag = sjNonWbtag #Non-W Subjet btag
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
        _corr_JERUp = getattr(tree, "Jet_corr_JERUp", [None]*n)
        _corr_JERDown = getattr(tree, "Jet_corr_JERDown", [None]*n)
        _corr_JER = getattr(tree, "Jet_corr_JER", [None]*n)
        _pt = getattr(tree, "Jet_pt", [None]*n)
        _eta = getattr(tree, "Jet_eta", [None]*n)
        _phi = getattr(tree, "Jet_phi", [None]*n)
        _mass = getattr(tree, "Jet_mass", [None]*n)
        _idxFirstTauMatch = getattr(tree, "Jet_idxFirstTauMatch", [None]*n)
        _heppyFlavour = getattr(tree, "Jet_heppyFlavour", [None]*n)
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
        _leptonDeltaPhi = getattr(tree, "Jet_leptonDeltaPhi", [None]*n)
        _leptonDeltaEta = getattr(tree, "Jet_leptonDeltaEta", [None]*n)
        _vtxMass = getattr(tree, "Jet_vtxMass", [None]*n)
        _vtxNtracks = getattr(tree, "Jet_vtxNtracks", [None]*n)
        _vtxPt = getattr(tree, "Jet_vtxPt", [None]*n)
        _vtx3DSig = getattr(tree, "Jet_vtx3DSig", [None]*n)
        _vtx3DVal = getattr(tree, "Jet_vtx3DVal", [None]*n)
        _vtxPosX = getattr(tree, "Jet_vtxPosX", [None]*n)
        _vtxPosY = getattr(tree, "Jet_vtxPosY", [None]*n)
        _vtxPosZ = getattr(tree, "Jet_vtxPosZ", [None]*n)
        _pullVectorPhi = getattr(tree, "Jet_pullVectorPhi", [None]*n)
        _pullVectorMag = getattr(tree, "Jet_pullVectorMag", [None]*n)
        _qgl = getattr(tree, "Jet_qgl", [None]*n)
        _ptd = getattr(tree, "Jet_ptd", [None]*n)
        _axis2 = getattr(tree, "Jet_axis2", [None]*n)
        _mult = getattr(tree, "Jet_mult", [None]*n)
        _numberOfDaughters = getattr(tree, "Jet_numberOfDaughters", [None]*n)
        _btagIdx = getattr(tree, "Jet_btagIdx", [None]*n)
        _mcIdx = getattr(tree, "Jet_mcIdx", [None]*n)
        _pt_reg = getattr(tree, "Jet_pt_reg", [None]*n)
        _pt_regVBF = getattr(tree, "Jet_pt_regVBF", [None]*n)
        _blike_VBF = getattr(tree, "Jet_blike_VBF", [None]*n)
        _bTagWeightJESUp = getattr(tree, "Jet_bTagWeightJESUp", [None]*n)
        _bTagWeightJESDown = getattr(tree, "Jet_bTagWeightJESDown", [None]*n)
        _bTagWeightLFUp = getattr(tree, "Jet_bTagWeightLFUp", [None]*n)
        _bTagWeightLFDown = getattr(tree, "Jet_bTagWeightLFDown", [None]*n)
        _bTagWeightHFUp = getattr(tree, "Jet_bTagWeightHFUp", [None]*n)
        _bTagWeightHFDown = getattr(tree, "Jet_bTagWeightHFDown", [None]*n)
        _bTagWeightStats1Up = getattr(tree, "Jet_bTagWeightStats1Up", [None]*n)
        _bTagWeightStats1Down = getattr(tree, "Jet_bTagWeightStats1Down", [None]*n)
        _bTagWeightStats2Up = getattr(tree, "Jet_bTagWeightStats2Up", [None]*n)
        _bTagWeightStats2Down = getattr(tree, "Jet_bTagWeightStats2Down", [None]*n)
        _bTagWeightcErr1Up = getattr(tree, "Jet_bTagWeightcErr1Up", [None]*n)
        _bTagWeightcErr1Down = getattr(tree, "Jet_bTagWeightcErr1Down", [None]*n)
        _bTagWeightcErr2Up = getattr(tree, "Jet_bTagWeightcErr2Up", [None]*n)
        _bTagWeightcErr2Down = getattr(tree, "Jet_bTagWeightcErr2Down", [None]*n)
        _bTagWeight = getattr(tree, "Jet_bTagWeight", [None]*n)
        return [Jet(_id[n], _puId[n], _btagCSV[n], _btagCMVA[n], _rawPt[n], _mcPt[n], _mcFlavour[n], _mcMatchId[n], _corr_JECUp[n], _corr_JECDown[n], _corr[n], _corr_JERUp[n], _corr_JERDown[n], _corr_JER[n], _pt[n], _eta[n], _phi[n], _mass[n], _idxFirstTauMatch[n], _heppyFlavour[n], _hadronFlavour[n], _btagBDT[n], _btagProb[n], _btagBProb[n], _btagSoftEl[n], _btagSoftMu[n], _btagnew[n], _btagCSVV0[n], _chHEF[n], _neHEF[n], _chEmEF[n], _neEmEF[n], _chMult[n], _leadTrackPt[n], _mcEta[n], _mcPhi[n], _mcM[n], _leptonPdgId[n], _leptonPt[n], _leptonPtRel[n], _leptonPtRelInv[n], _leptonDeltaR[n], _leptonDeltaPhi[n], _leptonDeltaEta[n], _vtxMass[n], _vtxNtracks[n], _vtxPt[n], _vtx3DSig[n], _vtx3DVal[n], _vtxPosX[n], _vtxPosY[n], _vtxPosZ[n], _pullVectorPhi[n], _pullVectorMag[n], _qgl[n], _ptd[n], _axis2[n], _mult[n], _numberOfDaughters[n], _btagIdx[n], _mcIdx[n], _pt_reg[n], _pt_regVBF[n], _blike_VBF[n], _bTagWeightJESUp[n], _bTagWeightJESDown[n], _bTagWeightLFUp[n], _bTagWeightLFDown[n], _bTagWeightHFUp[n], _bTagWeightHFDown[n], _bTagWeightStats1Up[n], _bTagWeightStats1Down[n], _bTagWeightStats2Up[n], _bTagWeightStats2Down[n], _bTagWeightcErr1Up[n], _bTagWeightcErr1Down[n], _bTagWeightcErr2Up[n], _bTagWeightcErr2Down[n], _bTagWeight[n]) for n in range(n)]
    def __init__(self, id,puId,btagCSV,btagCMVA,rawPt,mcPt,mcFlavour,mcMatchId,corr_JECUp,corr_JECDown,corr,corr_JERUp,corr_JERDown,corr_JER,pt,eta,phi,mass,idxFirstTauMatch,heppyFlavour,hadronFlavour,btagBDT,btagProb,btagBProb,btagSoftEl,btagSoftMu,btagnew,btagCSVV0,chHEF,neHEF,chEmEF,neEmEF,chMult,leadTrackPt,mcEta,mcPhi,mcM,leptonPdgId,leptonPt,leptonPtRel,leptonPtRelInv,leptonDeltaR,leptonDeltaPhi,leptonDeltaEta,vtxMass,vtxNtracks,vtxPt,vtx3DSig,vtx3DVal,vtxPosX,vtxPosY,vtxPosZ,pullVectorPhi,pullVectorMag,qgl,ptd,axis2,mult,numberOfDaughters,btagIdx,mcIdx,pt_reg,pt_regVBF,blike_VBF,bTagWeightJESUp,bTagWeightJESDown,bTagWeightLFUp,bTagWeightLFDown,bTagWeightHFUp,bTagWeightHFDown,bTagWeightStats1Up,bTagWeightStats1Down,bTagWeightStats2Up,bTagWeightStats2Down,bTagWeightcErr1Up,bTagWeightcErr1Down,bTagWeightcErr2Up,bTagWeightcErr2Down,bTagWeight):
        self.id = id #POG Loose jet ID
        self.puId = puId #puId (full MVA, loose WP, 5.3.X training on AK5PFchs: the only thing that is available now)
        self.btagCSV = btagCSV #CSV-IVF v2 discriminator
        self.btagCMVA = btagCMVA #CMVA discriminator
        self.rawPt = rawPt #p_{T} before JEC
        self.mcPt = mcPt #p_{T} of associated gen jet
        self.mcFlavour = mcFlavour #parton flavour (physics definition, i.e. including b's from shower)
        self.mcMatchId = mcMatchId #Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake
        self.corr_JECUp = corr_JECUp #pt correction from JEC up
        self.corr_JECDown = corr_JECDown #pt correction from JEC down
        self.corr = corr #pt correction from JEC
        self.corr_JERUp = corr_JERUp #pt correction from JER up
        self.corr_JERDown = corr_JERDown #pt correction from JER down 
        self.corr_JER = corr_JER #pt correction from JER
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.idxFirstTauMatch = idxFirstTauMatch #index of the first matching tau
        self.heppyFlavour = heppyFlavour #heppy-style match to gen quarks
        self.hadronFlavour = hadronFlavour #hadron flavour (ghost matching to B/C hadrons)
        self.btagBDT = btagBDT #combined super-btag
        self.btagProb = btagProb #jet probability b-tag
        self.btagBProb = btagBProb #jet b-probability b-tag
        self.btagSoftEl = btagSoftEl #soft electron b-tag
        self.btagSoftMu = btagSoftMu #soft muon b-tag
        self.btagnew = btagnew #newest btag discriminator
        self.btagCSVV0 = btagCSVV0 #should be the old CSV discriminator with AVR vertices
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
        self.leptonDeltaPhi = leptonDeltaPhi #deltaPhi of the first associated lepton
        self.leptonDeltaEta = leptonDeltaEta #deltaEta of the first associated lepton
        self.vtxMass = vtxMass #vtxMass from btag
        self.vtxNtracks = vtxNtracks #number of tracks at vertex from btag
        self.vtxPt = vtxPt #pt of vertex from btag
        self.vtx3DSig = vtx3DSig #decay len significance of vertex from btag
        self.vtx3DVal = vtx3DVal #decay len of vertex from btag
        self.vtxPosX = vtxPosX #X coord of vertex from btag
        self.vtxPosY = vtxPosY #Y coord of vertex from btag
        self.vtxPosZ = vtxPosZ #Z coord of vertex from btag
        self.pullVectorPhi = pullVectorPhi #pull angle phi in the phi eta plane
        self.pullVectorMag = pullVectorMag #pull angle magnitude
        self.qgl = qgl #QG Likelihood
        self.ptd = ptd #QG input variable: ptD
        self.axis2 = axis2 #QG input variable: axis2
        self.mult = mult #QG input variable: total multiplicity
        self.numberOfDaughters = numberOfDaughters #number of daughters
        self.btagIdx = btagIdx #ranking in btag
        self.mcIdx = mcIdx #index of the matching gen jet
        self.pt_reg = pt_reg #Regression
        self.pt_regVBF = pt_regVBF #Regression for VBF
        self.blike_VBF = blike_VBF #VBF blikelihood for SingleBtag dataset
        self.bTagWeightJESUp = bTagWeightJESUp #b-tag CSV weight, variating JES Up
        self.bTagWeightJESDown = bTagWeightJESDown #b-tag CSV weight, variating JES Down
        self.bTagWeightLFUp = bTagWeightLFUp #b-tag CSV weight, variating LF Up
        self.bTagWeightLFDown = bTagWeightLFDown #b-tag CSV weight, variating LF Down
        self.bTagWeightHFUp = bTagWeightHFUp #b-tag CSV weight, variating HF Up
        self.bTagWeightHFDown = bTagWeightHFDown #b-tag CSV weight, variating HF Down
        self.bTagWeightStats1Up = bTagWeightStats1Up #b-tag CSV weight, variating Stats1 Up
        self.bTagWeightStats1Down = bTagWeightStats1Down #b-tag CSV weight, variating Stats1 Down
        self.bTagWeightStats2Up = bTagWeightStats2Up #b-tag CSV weight, variating Stats2 Up
        self.bTagWeightStats2Down = bTagWeightStats2Down #b-tag CSV weight, variating Stats2 Down
        self.bTagWeightcErr1Up = bTagWeightcErr1Up #b-tag CSV weight, variating cErr1 Up
        self.bTagWeightcErr1Down = bTagWeightcErr1Down #b-tag CSV weight, variating cErr1 Down
        self.bTagWeightcErr2Up = bTagWeightcErr2Up #b-tag CSV weight, variating cErr2 Up
        self.bTagWeightcErr2Down = bTagWeightcErr2Down #b-tag CSV weight, variating cErr2 Down
        self.bTagWeight = bTagWeight #b-tag CSV weight, nominal
class FatjetCA15softdrop:
    """
    CA, R=1.5, pT > 200 GeV, softdrop zcut=0.1, beta=0
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nFatjetCA15softdrop", 0)
        _pt = getattr(tree, "FatjetCA15softdrop_pt", [None]*n)
        _eta = getattr(tree, "FatjetCA15softdrop_eta", [None]*n)
        _phi = getattr(tree, "FatjetCA15softdrop_phi", [None]*n)
        _mass = getattr(tree, "FatjetCA15softdrop_mass", [None]*n)
        return [FatjetCA15softdrop(_pt[n], _eta[n], _phi[n], _mass[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
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
        _eleCutIdSpring15_25ns_v1 = getattr(tree, "vLeptons_eleCutIdSpring15_25ns_v1", [None]*n)
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
        _miniRelIso = getattr(tree, "vLeptons_miniRelIso", [None]*n)
        _tightCharge = getattr(tree, "vLeptons_tightCharge", [None]*n)
        _mcMatchId = getattr(tree, "vLeptons_mcMatchId", [None]*n)
        _mcMatchAny = getattr(tree, "vLeptons_mcMatchAny", [None]*n)
        _mcMatchTau = getattr(tree, "vLeptons_mcMatchTau", [None]*n)
        _mcPt = getattr(tree, "vLeptons_mcPt", [None]*n)
        _mediumMuonId = getattr(tree, "vLeptons_mediumMuonId", [None]*n)
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
        _mvaIdTrig = getattr(tree, "vLeptons_mvaIdTrig", [None]*n)
        _mvaIdTrigMediumResult = getattr(tree, "vLeptons_mvaIdTrigMediumResult", [None]*n)
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
        _dr03TkSumPt = getattr(tree, "vLeptons_dr03TkSumPt", [None]*n)
        _eleEcalClusterIso = getattr(tree, "vLeptons_eleEcalClusterIso", [None]*n)
        _eleHcalClusterIso = getattr(tree, "vLeptons_eleHcalClusterIso", [None]*n)
        return [vLeptons(_charge[n], _tightId[n], _eleCutIdCSA14_25ns_v1[n], _eleCutIdCSA14_50ns_v1[n], _eleCutIdSpring15_25ns_v1[n], _dxy[n], _dz[n], _edxy[n], _edz[n], _ip3d[n], _sip3d[n], _convVeto[n], _lostHits[n], _relIso03[n], _relIso04[n], _miniRelIso[n], _tightCharge[n], _mcMatchId[n], _mcMatchAny[n], _mcMatchTau[n], _mcPt[n], _mediumMuonId[n], _pdgId[n], _pt[n], _eta[n], _phi[n], _mass[n], _looseIdSusy[n], _looseIdPOG[n], _chargedHadRelIso03[n], _chargedHadRelIso04[n], _eleSieie[n], _eleDEta[n], _eleDPhi[n], _eleHoE[n], _eleMissingHits[n], _eleChi2[n], _mvaIdTrig[n], _mvaIdTrigMediumResult[n], _nStations[n], _trkKink[n], _caloCompatibility[n], _globalTrackChi2[n], _nChamberHits[n], _isPFMuon[n], _isGlobalMuon[n], _isTrackerMuon[n], _pixelHits[n], _trackerLayers[n], _pixelLayers[n], _mvaTTH[n], _jetOverlapIdx[n], _jetPtRatio[n], _jetBTagCSV[n], _jetDR[n], _pfRelIso03[n], _pfRelIso04[n], _etaSc[n], _eleExpMissingInnerHits[n], _eleooEmooP[n], _dr03TkSumPt[n], _eleEcalClusterIso[n], _eleHcalClusterIso[n]) for n in range(n)]
    def __init__(self, charge,tightId,eleCutIdCSA14_25ns_v1,eleCutIdCSA14_50ns_v1,eleCutIdSpring15_25ns_v1,dxy,dz,edxy,edz,ip3d,sip3d,convVeto,lostHits,relIso03,relIso04,miniRelIso,tightCharge,mcMatchId,mcMatchAny,mcMatchTau,mcPt,mediumMuonId,pdgId,pt,eta,phi,mass,looseIdSusy,looseIdPOG,chargedHadRelIso03,chargedHadRelIso04,eleSieie,eleDEta,eleDPhi,eleHoE,eleMissingHits,eleChi2,mvaIdTrig,mvaIdTrigMediumResult,nStations,trkKink,caloCompatibility,globalTrackChi2,nChamberHits,isPFMuon,isGlobalMuon,isTrackerMuon,pixelHits,trackerLayers,pixelLayers,mvaTTH,jetOverlapIdx,jetPtRatio,jetBTagCSV,jetDR,pfRelIso03,pfRelIso04,etaSc,eleExpMissingInnerHits,eleooEmooP,dr03TkSumPt,eleEcalClusterIso,eleHcalClusterIso):
        self.charge = charge #
        self.tightId = tightId #POG Tight ID (for electrons it's configured in the analyzer)
        self.eleCutIdCSA14_25ns_v1 = eleCutIdCSA14_25ns_v1 #Electron cut-based id (POG CSA14_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.eleCutIdCSA14_50ns_v1 = eleCutIdCSA14_50ns_v1 #Electron cut-based id (POG CSA14_50ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
        self.eleCutIdSpring15_25ns_v1 = eleCutIdSpring15_25ns_v1 #Electron cut-based id (POG Spring15_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight
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
        self.miniRelIso = miniRelIso #PF Rel miniRel, pile-up corrected
        self.tightCharge = tightCharge #Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, 2 if ptError/pt < 0.20, 0 otherwise 
        self.mcMatchId = mcMatchId #Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake
        self.mcMatchAny = mcMatchAny #Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom
        self.mcMatchTau = mcMatchTau #True if the leptons comes from a tau
        self.mcPt = mcPt #p_{T} of associated gen lepton
        self.mediumMuonId = mediumMuonId #Muon POG Medium id
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
        self.mvaIdTrig = mvaIdTrig #EGamma POG MVA ID for triggering electrons; 1 for muons
        self.mvaIdTrigMediumResult = mvaIdTrigMediumResult #True if passes EGamma POG MVA ID for triggering electrons; True for muons
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
        self.jetOverlapIdx = jetOverlapIdx #index of jet with overlapping PF constituents. If idx>=1000, then idx = idx-1000 and refers to discarded jets.
        self.jetPtRatio = jetPtRatio #pt(lepton)/pt(nearest jet)
        self.jetBTagCSV = jetBTagCSV #btag of nearest jet
        self.jetDR = jetDR #deltaR(lepton, nearest jet)
        self.pfRelIso03 = pfRelIso03 #0.3 particle based iso
        self.pfRelIso04 = pfRelIso04 #0.4 particle based iso
        self.etaSc = etaSc #Electron supercluster pseudorapidity
        self.eleExpMissingInnerHits = eleExpMissingInnerHits #Electron expected missing inner hits
        self.eleooEmooP = eleooEmooP #Electron 1/E - 1/P
        self.dr03TkSumPt = dr03TkSumPt #Electron track sum pt
        self.eleEcalClusterIso = eleEcalClusterIso #Electron ecal cluster iso
        self.eleHcalClusterIso = eleHcalClusterIso #Electron hcal cluster iso
class pileUpVertex_z:
    """
    z position of hardest pile-up collisions
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "npileUpVertex_z", 0)
        _pileUpVertex_z = getattr(tree, "pileUpVertex_z", [None]*n);
        return [pileUpVertex_z(_pileUpVertex_z[n]) for n in range(n)]
    def __init__(self, pileUpVertex_z):
        self.pileUpVertex_z = pileUpVertex_z #z position of hardest pile-up collisions
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
class FatjetCA15softdropz2b1:
    """
    CA, R=1.5, pT > 200 GeV, softdrop zcut=0.2, beta=1
    """
    @staticmethod
    def make_array(tree):
        n = getattr(tree, "nFatjetCA15softdropz2b1", 0)
        _pt = getattr(tree, "FatjetCA15softdropz2b1_pt", [None]*n)
        _eta = getattr(tree, "FatjetCA15softdropz2b1_eta", [None]*n)
        _phi = getattr(tree, "FatjetCA15softdropz2b1_phi", [None]*n)
        _mass = getattr(tree, "FatjetCA15softdropz2b1_mass", [None]*n)
        _tau1 = getattr(tree, "FatjetCA15softdropz2b1_tau1", [None]*n)
        _tau2 = getattr(tree, "FatjetCA15softdropz2b1_tau2", [None]*n)
        _tau3 = getattr(tree, "FatjetCA15softdropz2b1_tau3", [None]*n)
        return [FatjetCA15softdropz2b1(_pt[n], _eta[n], _phi[n], _mass[n], _tau1[n], _tau2[n], _tau3[n]) for n in range(n)]
    def __init__(self, pt,eta,phi,mass,tau1,tau2,tau3):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.tau1 = tau1 #Nsubjettiness (1 axis)
        self.tau2 = tau2 #Nsubjettiness (2 axes)
        self.tau3 = tau3 #Nsubjettiness (3 axes)
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
class HaddJetsdR08:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HaddJetsdR08_pt", None)
        _eta = getattr(tree, "HaddJetsdR08_eta", None)
        _phi = getattr(tree, "HaddJetsdR08_phi", None)
        _mass = getattr(tree, "HaddJetsdR08_mass", None)
        return HaddJetsdR08(_pt, _eta, _phi, _mass)
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
class softActivityVH:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _njets2 = getattr(tree, "softActivityVH_njets2", None)
        _njets5 = getattr(tree, "softActivityVH_njets5", None)
        _njets10 = getattr(tree, "softActivityVH_njets10", None)
        _HT = getattr(tree, "softActivityVH_HT", None)
        return softActivityVH(_njets2, _njets5, _njets10, _HT)
    def __init__(self, njets2,njets5,njets10,HT):
        self.njets2 = njets2 #number of jets from soft activity with pt>2Gev
        self.njets5 = njets5 #number of jets from soft activity with pt>5Gev
        self.njets10 = njets10 #number of jets from soft activity with pt>10Gev
        self.HT = HT #sum pt of sa jets
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
class H_reg:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "H_reg_pt", None)
        _eta = getattr(tree, "H_reg_eta", None)
        _phi = getattr(tree, "H_reg_phi", None)
        _mass = getattr(tree, "H_reg_mass", None)
        return H_reg(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
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
class HCSV_reg:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCSV_reg_pt", None)
        _eta = getattr(tree, "HCSV_reg_eta", None)
        _phi = getattr(tree, "HCSV_reg_phi", None)
        _mass = getattr(tree, "HCSV_reg_mass", None)
        return HCSV_reg(_pt, _eta, _phi, _mass)
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
class softActivity:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _njets2 = getattr(tree, "softActivity_njets2", None)
        _njets5 = getattr(tree, "softActivity_njets5", None)
        _njets10 = getattr(tree, "softActivity_njets10", None)
        _HT = getattr(tree, "softActivity_HT", None)
        return softActivity(_njets2, _njets5, _njets10, _HT)
    def __init__(self, njets2,njets5,njets10,HT):
        self.njets2 = njets2 #number of jets from soft activity with pt>2Gev
        self.njets5 = njets5 #number of jets from soft activity with pt>5Gev
        self.njets10 = njets10 #number of jets from soft activity with pt>10Gev
        self.HT = HT #sum pt of sa jets
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
        event.pileUpVertex_ptHat = pileUpVertex_ptHat.make_array(event.input)
        event.GenHiggsBoson = GenHiggsBoson.make_array(event.input)
        event.hJidx_sortcsv = hJidx_sortcsv.make_array(event.input)
        event.aJCidx = aJCidx.make_array(event.input)
        event.FatjetCA15pruned = FatjetCA15pruned.make_array(event.input)
        event.GenLepFromTop = GenLepFromTop.make_array(event.input)
        event.GenVbosons = GenVbosons.make_array(event.input)
        event.ajidxaddJetsdR08 = ajidxaddJetsdR08.make_array(event.input)
        event.FatjetAK08pruned = FatjetAK08pruned.make_array(event.input)
        event.GenJet = GenJet.make_array(event.input)
        event.SubjetCA15pruned = SubjetCA15pruned.make_array(event.input)
        event.FatjetCA15ungroomed = FatjetCA15ungroomed.make_array(event.input)
        event.dRaddJetsdR08 = dRaddJetsdR08.make_array(event.input)
        event.GenBQuarkFromH = GenBQuarkFromH.make_array(event.input)
        event.GenStatus2bHad = GenStatus2bHad.make_array(event.input)
        event.hJCidx = hJCidx.make_array(event.input)
        event.GenTop = GenTop.make_array(event.input)
        event.aJidx = aJidx.make_array(event.input)
        event.FatjetCA15trimmed = FatjetCA15trimmed.make_array(event.input)
        event.GenLepFromTau = GenLepFromTau.make_array(event.input)
        event.aLeptons = aLeptons.make_array(event.input)
        event.GenNuFromTop = GenNuFromTop.make_array(event.input)
        event.FatjetAK08ungroomed = FatjetAK08ungroomed.make_array(event.input)
        event.selLeptons = selLeptons.make_array(event.input)
        event.GenHiggsSisters = GenHiggsSisters.make_array(event.input)
        event.hjidxaddJetsdR08 = hjidxaddJetsdR08.make_array(event.input)
        event.softActivityVHJets = softActivityVHJets.make_array(event.input)
        event.DiscardedJet = DiscardedJet.make_array(event.input)
        event.SubjetAK08pruned = SubjetAK08pruned.make_array(event.input)
        event.TauGood = TauGood.make_array(event.input)
        event.hJidx = hJidx.make_array(event.input)
        event.GenLep = GenLep.make_array(event.input)
        event.SubjetAK08softdrop = SubjetAK08softdrop.make_array(event.input)
        event.GenHadTaus = GenHadTaus.make_array(event.input)
        event.httCandidates = httCandidates.make_array(event.input)
        event.Jet = Jet.make_array(event.input)
        event.FatjetCA15softdrop = FatjetCA15softdrop.make_array(event.input)
        event.vLeptons = vLeptons.make_array(event.input)
        event.pileUpVertex_z = pileUpVertex_z.make_array(event.input)
        event.primaryVertices = primaryVertices.make_array(event.input)
        event.softActivityJets = softActivityJets.make_array(event.input)
        event.FatjetCA15softdropz2b1 = FatjetCA15softdropz2b1.make_array(event.input)
        event.GenWZQuark = GenWZQuark.make_array(event.input)
        event.GenBQuarkFromTop = GenBQuarkFromTop.make_array(event.input)
        event.V = V.make_obj(event.input)
        event.HaddJetsdR08 = HaddJetsdR08.make_obj(event.input)
        event.H = H.make_obj(event.input)
        event.softActivityVH = softActivityVH.make_obj(event.input)
        event.met_shifted_JetResUp = met_shifted_JetResUp.make_obj(event.input)
        event.met = met.make_obj(event.input)
        event.H_reg = H_reg.make_obj(event.input)
        event.met_shifted_JetEnDown = met_shifted_JetEnDown.make_obj(event.input)
        event.HCSV = HCSV.make_obj(event.input)
        event.met_shifted_MuonEnDown = met_shifted_MuonEnDown.make_obj(event.input)
        event.met_shifted_ElectronEnUp = met_shifted_ElectronEnUp.make_obj(event.input)
        event.met_shifted_ElectronEnDown = met_shifted_ElectronEnDown.make_obj(event.input)
        event.fakeMET = fakeMET.make_obj(event.input)
        event.met_shifted_TauEnDown = met_shifted_TauEnDown.make_obj(event.input)
        event.met_shifted_TauEnUp = met_shifted_TauEnUp.make_obj(event.input)
        event.HCSV_reg = HCSV_reg.make_obj(event.input)
        event.met_shifted_UnclusteredEnUp = met_shifted_UnclusteredEnUp.make_obj(event.input)
        event.met_shifted_UnclusteredEnDown = met_shifted_UnclusteredEnDown.make_obj(event.input)
        event.met_shifted_JetEnUp = met_shifted_JetEnUp.make_obj(event.input)
        event.met_shifted_JetResDown = met_shifted_JetResDown.make_obj(event.input)
        event.softActivity = softActivity.make_obj(event.input)
        event.met_shifted_MuonEnUp = met_shifted_MuonEnUp.make_obj(event.input)
        event.json = getattr(event.input, "json", None)
        event.nPU0 = getattr(event.input, "nPU0", None)
        event.nPVs = getattr(event.input, "nPVs", None)
        event.Vtype = getattr(event.input, "Vtype", None)
        event.VtypeSim = getattr(event.input, "VtypeSim", None)
        event.VMt = getattr(event.input, "VMt", None)
        event.HVdPhi = getattr(event.input, "HVdPhi", None)
        event.fakeMET_sumet = getattr(event.input, "fakeMET_sumet", None)
        event.rho = getattr(event.input, "rho", None)
        event.deltaR_jj = getattr(event.input, "deltaR_jj", None)
        event.lheNj = getattr(event.input, "lheNj", None)
        event.lheNb = getattr(event.input, "lheNb", None)
        event.lheNc = getattr(event.input, "lheNc", None)
        event.lheNg = getattr(event.input, "lheNg", None)
        event.lheNl = getattr(event.input, "lheNl", None)
        event.lheV_pt = getattr(event.input, "lheV_pt", None)
        event.lheHT = getattr(event.input, "lheHT", None)
        event.genTTHtoTauTauDecayMode = getattr(event.input, "genTTHtoTauTauDecayMode", None)
        event.ttCls = getattr(event.input, "ttCls", None)
        event.mhtJet30 = getattr(event.input, "mhtJet30", None)
        event.mhtPhiJet30 = getattr(event.input, "mhtPhiJet30", None)
        event.htJet30 = getattr(event.input, "htJet30", None)
        event.met_rawpt = getattr(event.input, "met_rawpt", None)
        event.metPuppi_pt = getattr(event.input, "metPuppi_pt", None)
        event.metPuppi_phi = getattr(event.input, "metPuppi_phi", None)
        event.metPuppi_rawpt = getattr(event.input, "metPuppi_rawpt", None)
        event.metNoHF_pt = getattr(event.input, "metNoHF_pt", None)
        event.metNoHF_phi = getattr(event.input, "metNoHF_phi", None)
        event.metNoHF_rawpt = getattr(event.input, "metNoHF_rawpt", None)
        event.metType1p2_pt = getattr(event.input, "metType1p2_pt", None)
        event.metNoPU_pt = getattr(event.input, "metNoPU_pt", None)
        event.metNoPU_phi = getattr(event.input, "metNoPU_phi", None)
        event.tkMet_pt = getattr(event.input, "tkMet_pt", None)
        event.tkMet_phi = getattr(event.input, "tkMet_phi", None)
        event.tkMetPVchs_pt = getattr(event.input, "tkMetPVchs_pt", None)
        event.tkMetPVchs_phi = getattr(event.input, "tkMetPVchs_phi", None)
        event.isrJetVH = getattr(event.input, "isrJetVH", None)
        event.Flag_hbheIsoFilter = getattr(event.input, "Flag_hbheIsoFilter", None)
        event.Flag_hbheFilterNew = getattr(event.input, "Flag_hbheFilterNew", None)
        event.simPrimaryVertex_z = getattr(event.input, "simPrimaryVertex_z", None)
        event.genHiggsDecayMode = getattr(event.input, "genHiggsDecayMode", None)
        event.bTagWeight_LFUp = getattr(event.input, "bTagWeight_LFUp", None)
        event.bTagWeight_Stats2Down = getattr(event.input, "bTagWeight_Stats2Down", None)
        event.bTagWeight_LFDown = getattr(event.input, "bTagWeight_LFDown", None)
        event.bTagWeight_HFUp = getattr(event.input, "bTagWeight_HFUp", None)
        event.bTagWeight_cErr1Down = getattr(event.input, "bTagWeight_cErr1Down", None)
        event.bTagWeight_JESDown = getattr(event.input, "bTagWeight_JESDown", None)
        event.bTagWeight_cErr1Up = getattr(event.input, "bTagWeight_cErr1Up", None)
        event.bTagWeight = getattr(event.input, "bTagWeight", None)
        event.bTagWeight_HFDown = getattr(event.input, "bTagWeight_HFDown", None)
        event.bTagWeight_Stats2Up = getattr(event.input, "bTagWeight_Stats2Up", None)
        event.bTagWeight_cErr2Up = getattr(event.input, "bTagWeight_cErr2Up", None)
        event.bTagWeight_JESUp = getattr(event.input, "bTagWeight_JESUp", None)
        event.bTagWeight_Stats1Up = getattr(event.input, "bTagWeight_Stats1Up", None)
        event.bTagWeight_Stats1Down = getattr(event.input, "bTagWeight_Stats1Down", None)
        event.bTagWeight_cErr2Down = getattr(event.input, "bTagWeight_cErr2Down", None)
