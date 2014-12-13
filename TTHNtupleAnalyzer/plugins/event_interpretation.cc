
//
//  event_interpretation.cpp
//  MEStudiesJP
//
//  Created by Joosep Pata on 13/12/14.
//  Copyright (c) 2014 Joosep Pata. All rights reserved.
//

#include <stdio.h>
#include <TTH/TTHNtupleAnalyzer/interface/event_interpretation.hh>

//these are simple 'sentinel values' for uninitialized variables
//for clarity, it would be best to use these instead of manually writing -99 etc.
//this way, undefined variables are always unique and one can write functions to recognize them
#define DEF_VAL_FLOAT -9999.0f
#define DEF_VAL_DOUBLE -9999.0d
#define DEF_VAL_INT -9999
#define FLOAT_EPS 0.0000001f
#define DOUBLE_EPS 0.0000001d

//checks if a branch variable is undefined
inline bool is_undef(int x) { return x==DEF_VAL_INT; };
inline bool is_undef(float x) { return fabs(x-DEF_VAL_FLOAT) < FLOAT_EPS; };
inline bool is_undef(double x) { return fabs(x-DEF_VAL_DOUBLE) < DOUBLE_EPS; };

const TLorentzVector vec_from_ptetaphim(double pt, double eta, double phi, double m) {
	TLorentzVector _p4;
	if (!is_undef(pt) && !is_undef(eta) && !is_undef(phi) && !is_undef(m))
		_p4.SetPtEtaPhiM(pt, eta, phi, m);
	return _p4;
}


Particle::Particle(double pt, double eta, double phi, double m, int _id, int _idx, const std::vector<Particle*> _parents, const std::vector<Particle*> _children) :
p4(vec_from_ptetaphim(pt, eta, phi, m)),
id(_id),
idx(_idx),
parents(_parents),
children(_children)
{
}

Particle::Particle(double pt, double eta, double phi, double m, int _id, int _idx) :
p4(vec_from_ptetaphim(pt, eta, phi, m)),
id(_id),
idx(_idx)
{
}

Particle::Particle(double pt, double eta, double phi, double m, int _id) :
p4(vec_from_ptetaphim(pt, eta, phi, m)),
id(_id),
idx(-1)
{
}

Event::Event(plist _particles, plist _jets, plist _gen_jets, plist _leptons, plist _gen_leptons, plist _top_decays, plist _higgs_decays) :
particles(_particles),
jets(_jets),
gen_jets(_gen_jets),
leptons(_leptons),
gen_leptons(_gen_leptons),
top_decays(_top_decays),
higgs_decays(_higgs_decays)
{
}

Event::~Event() {
	for (auto* v : particles) {
		delete v;
	}
}
