#ifndef TTH_HELPERS
#define TTH_HELPERS

#define CANDPRINT(x) " pt=" << x.pt() << " eta=" << x.eta() << " phi=" << x.phi() << " id=" << x.pdgId() << " st=" << x.status()
#define PCANDPRINT(x) " pt=" << x->pt() << " eta=" << x->eta() << " phi=" << x->phi() << " id=" << x->pdgId() << " st=" << x->status()
#define GENJET_DR 0.5
#define GENJET_REL_DP 0.5

#define GENLEPTON_DR 0.5
#define GENLEPTON_REL_DP 0.5

//minimum dR between jet and leptonn
#define JET_LEPTON_DR 0.4

//how many good leptons to store in the good_lep array at most?
#define N_MAX_GOOD_LEPTONS 2

#endif
