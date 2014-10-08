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
    bb,
    UNKNOWN_HYPO
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
        if(
            mu.isLooseMuon() &&
            mu.isTightMuon(vtx)
        ) {
            out.push_back(&mu);
        }
    }
    return out;
}

//select electrons which pass quality criteria
vector<const pat::Electron*> find_good_electrons(const vector<pat::Electron>& electrons, const DecayMode mode) {
    vector<const pat::Electron*> out;

    for (auto& ele : electrons) {
        out.push_back(&ele);
    }
    return out;
}

//select taus which pass quality criteria
vector<const pat::Tau*> find_good_taus(const vector<pat::Tau>& taus, const DecayMode mode) {
    vector<const pat::Tau*> out;

    for (auto& tau : taus) {
        out.push_back(&tau);
    }
    return out;
}

//select taus which pass quality criteria
vector<const pat::Jet*> find_good_jets(const vector<pat::Jet>& jets, const DecayMode mode) {
    vector<const pat::Jet*> out;

    for (auto& jet : jets) {
        out.push_back(&jet);
    }
    return out;
}

//contains the kinematic data of an event with quality cuts, reduction and disambiguation applied on the particles
class EventDescription {
    public:
    const vector<const pat::Muon*>& muons;
    const vector<const pat::Electron*>& electrons;
    const vector<const pat::Tau*>& taus;
    const vector<const pat::Jet*>& jets;

    EventDescription(
        const vector<const pat::Muon*>& _muons,
        const vector<const pat::Electron*>& _electrons,
        const vector<const pat::Tau*>& _taus,
        const vector<const pat::Jet*>& _jets) :
        muons(_muons),
        electrons(_electrons),
        taus(_taus),
        jets(_jets) { 
    }
};

//FIXME: these can be put into a different namespace, e.g. Htobb, if other competing definitions arise
//Assigns a unique event hypothesis based on the particle contents of the event
EventHypothesis assign_event_hypothesis(const EventDescription& ev) {
    
    //default 
    return EventHypothesis::UNKNOWN_HYPO;
}

//FIXME: implement these checks 

bool is_mu_mu(const EventDescription& ev) { 
    return false;
}

bool is_e_e(const EventDescription& ev) { 
    return false;
}

bool is_mu_n(const EventDescription& ev) { 
    return false;
}

bool is_e_n(const EventDescription& ev) { 
    return false;
}

bool is_n_n(const EventDescription& ev) { 
    return false;
}

bool is_e_mu(const EventDescription& ev) { 
    return false;
}

bool is_tau_mu(const EventDescription& ev) { 
    return false;
}

bool is_tau_e(const EventDescription& ev) { 
    return false;
}

bool is_tau_n(const EventDescription& ev) { 
    return false;
}

}

