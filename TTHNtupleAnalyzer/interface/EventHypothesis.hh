#include <algorithm>

template <typename T> bool is_in(const std::vector<T>& v, T o) {
    return std::find(v.begin(), v.end(), o)!=v.end();
}

//delta-beta corrected relative isolations
double dbc_rel_iso(const pat::Electron& lepton) {
    return (
               (lepton.chargedHadronIso() +
                std::max(0.0, lepton.neutralHadronIso() + lepton.photonIso() - 0.5*lepton.puChargedHadronIso()))/lepton.pt()
           );
}

double dbc_rel_iso(const pat::Muon& lepton) {
    return (
               (lepton.chargedHadronIso() +
                std::max(0.0, lepton.neutralHadronIso() + lepton.photonIso() - 0.5*lepton.puChargedHadronIso()))/lepton.pt()
           );
}

//jet ID
//https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopJME#Jets
bool jetID(const pat::Jet& j) {
    if(j.neutralHadronEnergyFraction() > 0.99) return false;
    if(j.neutralEmEnergyFraction() > 0.99)     return false;
    if(fabs(j.p4().Eta())<2.4 && j.chargedEmEnergyFraction() > 0.99)   return false;
    if(fabs(j.p4().Eta())<2.4 && j.chargedHadronEnergyFraction() == 0) return false;
    //if(fabs(j.p4().Eta())<2.4 && j.associatedTracks().size() == 0) return false;
    if(j.numberOfDaughters() <= 1) return false;
    return true;
}

bool is_tight_electron(const pat::Electron& ele, const reco::Vertex& vtx) {
    const float ae = TMath::Abs(ele.eta());
    return (
        ele.gsfTrack().isNonnull() &&
        ele.pt() > 30 && ae < 2.5 && !(ae>1.4442 && ae<1.5660) &&
        TMath::Abs(ele.gsfTrack()->dxy(vtx.position())) < 0.02 &&
        ele.passConversionVeto() &&
        
        //throws error:
        //pat::Electron: the ID mvaTrigV0 can't be found in this pat::Electron.
        //The available IDs are: 'eidLoose' 'eidRobustHighEnergy' 'eidRobustLoose' 'eidRobustTight' 'eidTight'
        //ele.electronID("mvaTrigV0") > 0.5 &&
        ele.electronID("eidLoose") > 0.5 &&
        //ele.gsfTrack()->trackerExpectedHitsInner().numberOfHits() <= 0 &&
        dbc_rel_iso(ele) < 0.1
    );
}

bool is_loose_electron(const pat::Electron& ele, const reco::Vertex& vtx) {
    const float ae = TMath::Abs(ele.eta());
    return (
        ele.gsfTrack().isNonnull() &&
        ele.pt() > 20 && ae < 2.5 &&
        TMath::Abs(ele.gsfTrack()->dxy(vtx.position())) < 0.04 &&
        ele.passConversionVeto() &&
        
        //throws error:
        //pat::Electron: the ID mvaTrigV0 can't be found in this pat::Electron.
        //The available IDs are: 'eidLoose' 'eidRobustHighEnergy' 'eidRobustLoose' 'eidRobustTight' 'eidTight'
        //ele.electronID("mvaTrigV0") > 0.5 &&
        ele.electronID("eidLoose") > 0.5 &&
        //ele.gsfTrack()->trackerExpectedHitsInner().numberOfHits() <= 0 &&
        dbc_rel_iso(ele) < 0.15
    ); 
}

//https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopMUO
//lepton + jets / single-top
bool is_tight_muon(const pat::Muon& mu, const reco::Vertex& vtx) {
    return (
        mu.pt()>26 &&
        TMath::Abs(mu.eta()) < 2.1 &&
        mu.isPFMuon() &&
        mu.isGlobalMuon() &&
        mu.normChi2() < 10 &&
        mu.track()->hitPattern().trackerLayersWithMeasurement() > 5 &&
        mu.globalTrack()->hitPattern().numberOfValidMuonHits() > 0 &&
        mu.muonBestTrack()->dxy(vtx.position()) < 0.2 &&
        mu.muonBestTrack()->dz(vtx.position())< 0.5 &&
        mu.innerTrack()->hitPattern().numberOfValidPixelHits() > 0 &&
        mu.numberOfMatchedStations() > 1 &&
        dbc_rel_iso(mu) < 0.12
    );
}

//https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopMUO
//dilepton
bool is_loose_muon(const pat::Muon& mu) {
    return (
        mu.pt()>20 &&
        mu.isPFMuon() &&
        TMath::Abs(mu.eta()) < 2.4 &&
        (mu.isGlobalMuon() || mu.isTrackerMuon()) &&
        dbc_rel_iso(mu) < 0.2
    );
}

bool is_good_tau(const pat::Tau& tau) {
    return (tau.pt() > 20 &&
        tau.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits") &&
        tau.tauID("againstMuonTight2") &&
        //MVA3 is not in CMSSW7
        //pat::Tau: the ID againstElectronMediumMVA3 can't be found in this pat::Tau.
        tau.tauID("againstElectronMediumMVA5")
    );
}

//https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopMUO
//Muon POG does not provide recommendations for muon veto ID. Feedback from analyses are encouraged. Our suggestion is to use the same muon requirements defined in the dilepton channel to veto muons in the lepton+jets channel. This leads to a natural decoupling of the two final states.
bool is_veto_muon(const pat::Muon& mu) {
    return is_loose_muon(mu);
}

bool is_veto_tau(const pat::Tau& tau) {
    return is_good_tau(tau);
}


bool is_veto_electron_loose(const pat::Electron& ele) {
    return (
        //ele.isPF() &&
        ele.gsfTrack().isNonnull() &&
        ele.pt() > 10 &&
        TMath::Abs(ele.eta()) < 2.5 &&
        dbc_rel_iso(ele) < 0.15
    );
}

bool is_veto_electron_tight(const pat::Electron& ele) {
    return (
        ele.gsfTrack().isNonnull() &&
        //ele.isPF() &&
        ele.pt() > 20 &&
        TMath::Abs(ele.eta()) < 2.5 &&
        dbc_rel_iso(ele) < 0.15
    );
}


namespace TTH {

//Initial classification based on the decay mode of the two top quarks
enum EventHypothesis {
    mumu,
    ee,
    mun,
    en,
    nn,
    emu,
    taumu,
    taue,
    taun,
    tautau,
    //bb,
    //could not assign a hyothesis
    UNKNOWN_HYPO,

    //assigned multiple hypotheses
    BAD_HYPO
};

//top quark pair decay mode
enum DecayMode {
    dileptonic,
    semileptonic,
    hadronic,
    UNKNOWN_MODE
};

//select muons which pass quality criteria
vector<const pat::Muon*> find_good_muons(const vector<pat::Muon>& muons, const reco::Vertex& vtx, const DecayMode mode) {
    vector<const pat::Muon*> out;

    for (auto& mu : muons) {

        //if need to do track checking and no tracks associated, skip muon
        if(mode == DecayMode::dileptonic) {
            if (mu.track().isNull() || mu.globalTrack().isNull() || mu.muonBestTrack().isNull() || mu.innerTrack().isNull()) {
                continue;
            }
            if (mode==DecayMode::dileptonic && is_loose_muon(mu)) {
                out.push_back(&mu);
            }
            else if (mode==DecayMode::semileptonic && is_tight_muon(mu, vtx)) {
                out.push_back(&mu);
            }
        }
    }
    return out;
}

//select electrons which pass quality criteria
//https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopEGM
vector<const pat::Electron*> find_good_electrons(const vector<pat::Electron>& electrons, const reco::Vertex& vtx, const DecayMode mode) {
    vector<const pat::Electron*> out;

    for (auto& ele : electrons) {

        //electrons with no track will not pass in any case 
        if(mode == DecayMode::dileptonic) {
            if (ele.gsfTrack().isNull()) {
                continue;
            }
        }

        if (mode==DecayMode::dileptonic && is_loose_electron(ele, vtx)) {
            out.push_back(&ele); 
        }
        else if (mode==DecayMode::semileptonic && is_tight_electron(ele, vtx)) {
            out.push_back(&ele); 
        }
    }
    return out;
}

vector<const pat::Electron*> find_veto_electrons(const vector<pat::Electron>& electrons, const vector<const pat::Electron*> signal_electrons,  const DecayMode mode) {
    vector<const pat::Electron*> out;

    for (auto& ele : electrons) {
        //skip already identified signal electrons
        if (is_in<const pat::Electron*>(signal_electrons, &ele)) {
            LogDebug("veto ele") << "skipping ele" << CANDPRINT(ele);
            continue;
        }
        if (mode==DecayMode::dileptonic && is_veto_electron_loose(ele)) {
            out.push_back(&ele); 
        }
        else if (mode==DecayMode::semileptonic && is_veto_electron_tight(ele)) {
            out.push_back(&ele); 
        } else {
            LogDebug("veto ele") << "ele" << CANDPRINT(ele) << " " << ele.isPF() << " " << dbc_rel_iso(ele) << " did not pass cuts for mode " << mode;
        }
    }
    return out;
}

//select muons which pass quality criteria
vector<const pat::Muon*> find_veto_muons(const vector<pat::Muon>& muons, const vector<const pat::Muon*>& signal_muons, const DecayMode mode) {
    vector<const pat::Muon*> out;

    for (auto& mu : muons) {
        //skip already identified signal muons
        if (is_in<const pat::Muon*>(signal_muons, &mu)) {
            continue;
        }

        if (is_veto_muon(mu)) {
            out.push_back(&mu);
        }
    }
    return out;
}

//select taus which pass quality criteria
//https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendation
//https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopTAU
vector<const pat::Tau*> find_good_taus(const vector<pat::Tau>& taus, const DecayMode mode) {
    vector<const pat::Tau*> out;

    for (auto& tau : taus) {
        if (is_good_tau(tau)) {
            out.push_back(&tau);
        }
    }
    return out;
}

vector<const pat::Tau*> find_veto_taus(const vector<pat::Tau>& taus, const vector<const pat::Tau*>& signal_taus, const DecayMode mode) {
    vector<const pat::Tau*> out;

    for (auto& tau : taus) {
        if (is_in<const pat::Tau*>(signal_taus, &tau)) {
            continue;
        }

        if (is_good_tau(tau)) {
            out.push_back(&tau);
        }
    }
    return out;
}

//select jets which pass quality criteria
vector<const pat::Jet*> find_good_jets(const vector<pat::Jet>& jets, const DecayMode mode) {
    vector<const pat::Jet*> out;

    for (auto& jet : jets) {
        if(
            jet.pt() > 30 &&
            TMath::Abs(jet.eta()) < 2.5 &&
            jetID(jet)
	    // LB: add jet pileup id
        ) {
            out.push_back(&jet);
        }
    }
    return out;
}

//contains the kinematic data of an event with quality cuts, reduction and disambiguation applied on the particles
class EventDescription {
    public:
    const vector<const pat::Muon*>& muons;
    const vector<const pat::Electron*>& electrons;
    const vector<const pat::Tau*>& taus;
    
    const vector<const pat::Muon*>& veto_muons;
    const vector<const pat::Electron*>& veto_electrons;
    const vector<const pat::Tau*>& veto_taus;
    
    const vector<const pat::Jet*>& jets;

    EventDescription(
        const vector<const pat::Muon*>& _muons,
        const vector<const pat::Electron*>& _electrons,
        const vector<const pat::Tau*>& _taus,
        
        const vector<const pat::Muon*>& _veto_muons,
        const vector<const pat::Electron*>& _veto_electrons,
        const vector<const pat::Tau*>& _veto_taus,
        const vector<const pat::Jet*>& _jets) :
        muons(_muons),
        electrons(_electrons),
        taus(_taus),
        veto_muons(_veto_muons),
        veto_electrons(_veto_electrons),
        veto_taus(_veto_taus),
        jets(_jets) { 
    }

    bool veto() const {
        return (veto_muons.size()==0 && veto_electrons.size()==0 && veto_taus.size()==0);  
    }

    void print() const {
        cout << muons.size() << " " << electrons.size() << " " << taus.size() << " "
             << veto_muons.size() << " " << veto_electrons.size() << " " << veto_taus.size() << " "
             << jets.size() << endl;
    }
};

bool is_mu_mu(const EventDescription& ev) { 
    if (ev.muons.size() == 2 && ev.electrons.size() == 0 && ev.taus.size() == 0 && ev.veto()) {
        return true; 
    }
    return false;
}

bool is_e_e(const EventDescription& ev) { 
    if (ev.muons.size() == 0 && ev.electrons.size() == 2 && ev.taus.size() == 0 && ev.veto()) {
        return true; 
    }
    return false;
}

bool is_mu_n(const EventDescription& ev) { 
    if (ev.muons.size() == 1 && ev.electrons.size() == 0 && ev.taus.size() == 0 && ev.veto()) {
        if (ev.jets.size() >= 2) { 
            return true; 
        }
    }
    return false;
}

bool is_e_n(const EventDescription& ev) { 
    if (ev.muons.size() == 0 && ev.electrons.size() == 1 && ev.taus.size() == 0 && ev.veto()) {
        if (ev.jets.size() >= 2) { 
            return true; 
        }
    }
    return false;
}

//this does not check leptons, relies on lepton checks being run earlier
bool is_n_n(const EventDescription& ev) {
    if (ev.jets.size()>=4) {
        return true; 
    }
    return false;
}

bool is_e_mu(const EventDescription& ev) { 
    if (ev.muons.size() == 1 && ev.electrons.size() == 1 && ev.taus.size() == 0 && ev.veto()) {
        return true; 
    }
    return false;
}

bool is_tau_mu(const EventDescription& ev) { 
    if (ev.muons.size() == 1 && ev.electrons.size() == 0 && ev.taus.size() == 1 && ev.veto()) {
        return true; 
    }
    return false;
}

bool is_tau_e(const EventDescription& ev) { 
    if (ev.muons.size() == 0 && ev.electrons.size() == 1 && ev.taus.size() == 1 && ev.veto()) {
        return true; 
    }
    return false;
}

bool is_tau_n(const EventDescription& ev) { 
    if (ev.muons.size() == 0 && ev.electrons.size() == 0 && ev.taus.size() == 1 && ev.veto()) {
        if (ev.jets.size() >= 2) { 
            return true; 
        }
    }
    return false;
}

bool is_tau_tau(const EventDescription& ev) { 
    if (ev.muons.size() == 0 && ev.electrons.size() == 0 && ev.taus.size() == 2 && ev.veto()) {
        return true; 
    }
    return false;
}

//FIXME: these can be put into a different namespace, e.g. Htobb, if other competing definitions arise
//Assigns a unique event hypothesis based on the particle contents of the event
EventHypothesis assign_event_hypothesis(const EventDescription& ev_sl, const EventDescription& ev_dl) {
    
   
    //check single lepton hypotheses
    if (is_e_n(ev_sl)) {
        return EventHypothesis::en; 
    }
    
    if (is_mu_n(ev_sl)) {
        return EventHypothesis::mun; 
    }
    
    if (is_tau_n(ev_sl)) {
        return EventHypothesis::taun; 
    }
   
    //check dilepton hypotheses
    if (is_e_e(ev_dl)) {
        return EventHypothesis::ee; 
    }
    
    if (is_mu_mu(ev_dl)) {
        return EventHypothesis::mumu;
    }
    
    if (is_tau_tau(ev_dl)) {
        return EventHypothesis::tautau;
    }

    if (is_e_mu(ev_dl)) {
        return EventHypothesis::emu;
    }
    
    if (is_tau_e(ev_dl)) {
        return EventHypothesis::taue;
    }
    
    if (is_tau_mu(ev_dl)) {
        return EventHypothesis::taumu;
    }
    //check other hypotheses
    
    if (is_n_n(ev_sl)) {
        return EventHypothesis::nn; 
    }
    
    //default 
    return EventHypothesis::UNKNOWN_HYPO;
}

bool is_unique_hypothesis(const EventDescription& ev_sl, const EventDescription& ev_dl) {
    
    const EventHypothesis hypo = assign_event_hypothesis(ev_sl, ev_dl); 
    const bool h1 = is_e_n(ev_sl); 
    const bool h2 = is_mu_n(ev_sl); 
    const bool h3 = is_tau_n(ev_sl); 
    
    const bool h4 = is_e_e(ev_dl); 
    const bool h5 = is_mu_mu(ev_dl); 
    const bool h6 = is_tau_tau(ev_dl); 
    const bool h7 = is_e_mu(ev_dl); 
    const bool h8 = is_tau_e(ev_dl); 
    const bool h9 = is_tau_mu(ev_dl);

    //this is a bit clunky because is_n_n does not do lepton checking
    const bool h10 = ((hypo==EventHypothesis::nn) && is_n_n(ev_sl));
    
    LogDebug("hypo") << h1 << " "
        << h2 << " "
        << h3 << " "
        << h4 << " "
        << h5 << " "
        << h6 << " "
        << h7 << " "
        << h8 << " "
        << h9 << " "
        << h10;

    if ((
        (int)h1 + 
        (int)h2 + 
        (int)h3 + 
        (int)h4 + 
        (int)h5 + 
        (int)h6 + 
        (int)h7 + 
        (int)h8 + 
        (int)h9 + 
        (int)h10
    ) > 1) {
        edm::LogWarning("badhypo") << h1 << " "
            << h2 << " "
            << h3 << " "
            << h4 << " "
            << h5 << " "
            << h6 << " "
            << h7 << " "
            << h8 << " "
            << h9 << " "
            << h10;
        return false;
    }
    return true;
}

}

