//
//  event_interpretation.hh
//  TTHNtupleAnalyzer
//
//  Created by Joosep Pata on 13/12/14.
//  Copyright (c) 2014 Joosep Pata. All rights reserved.
//

#ifndef TTHNtupleAnalyzer_event_interpretation_hh
#define TTHNtupleAnalyzer_event_interpretation_hh

//these are simple 'sentinel values' for uninitialized variables
//for clarity, it would be best to use these instead of manually writing -99 etc.
//this way, undefined variables are always unique and one can write functions to recognize them
#include <cmath>
#define DEF_VAL_FLOAT -9999.0f
#define DEF_VAL_DOUBLE -9999.0d
#define DEF_VAL_INT -9999
#define FLOAT_EPS 0.0000001f
#define DOUBLE_EPS 0.0000001d

//checks if a branch variable is undefined
inline bool is_undef(int x) { return x==DEF_VAL_INT; };
inline bool is_undef(float x) { return fabs(x-DEF_VAL_FLOAT) < FLOAT_EPS; };
inline bool is_undef(double x) { return fabs(x-DEF_VAL_DOUBLE) < DOUBLE_EPS; };

#include "TLorentzVector.h"
#include <iostream>

class Particle {
public:
	const TLorentzVector p4;
	const int id;
	const int idx;
	std::vector<Particle*> parents;
	std::vector<Particle*> children;
	
	Particle(double pt, double eta, double phi, double m, int _id, int _idx,
		const std::vector<Particle*> _parents,
		const std::vector<Particle*> _children
	);
	
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
	std::vector<Particle*> w_decays;
	std::vector<Particle*> higgs_decays;
	
	Event(plist _particles,
		plist _jets,
		plist _gen_jets,
		plist _leptons,
		plist _gen_leptons,
		plist _top_decays,
		plist _w_decays,
		plist _higgs_decays
		);
	~Event();
	
};

#endif
