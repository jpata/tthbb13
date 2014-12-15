//
//  event_interpretation.hh
//  TTHNtupleAnalyzer
//
//  Created by Joosep Pata on 13/12/14.
//  Copyright (c) 2014 Joosep Pata. All rights reserved.
//

#ifndef TTHNtupleAnalyzer_event_interpretation_hh
#define TTHNtupleAnalyzer_event_interpretation_hh

#include "TLorentzVector.h"

class Particle {
public:
	const TLorentzVector p4;
	const int id;
	const int idx;
	std::vector<Particle*> parents;
	std::vector<Particle*> children;
	
	Particle(double pt, double eta, double phi, double m, int _id, int _idx, const std::vector<Particle*> _parents, const std::vector<Particle*> _children);
	
	Particle(double pt, double eta, double phi, double m, int _id, int _idx);
	Particle(double pt, double eta, double phi, double m, int _id);
	~Particle() {};
};

class Event {
public:
	typedef std::vector<Particle*> plist;
	std::vector<Particle*> particles;
	
	std::vector<Particle*> jets;
	std::vector<Particle*> gen_jets;
	std::vector<Particle*> leptons;
	std::vector<Particle*> gen_leptons;
	
	std::vector<Particle*> top_decays;
	std::vector<Particle*> higgs_decays;
	
	Event(plist _particles, plist _jets, plist _gen_jets, plist _leptons, plist _gen_leptons, plist _top_decays, plist _higgs_decays);
	~Event();
	
};

#endif
