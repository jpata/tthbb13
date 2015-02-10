
//
//  event_interpretation.cpp
//  MEStudiesJP
//
//  Created by Joosep Pata on 13/12/14.
//  Copyright (c) 2014 Joosep Pata. All rights reserved.
//

#include <stdio.h>
#include <TTH/TTHNtupleAnalyzer/interface/event_interpretation.hh>
#include <TTH/TTHNtupleAnalyzer/interface/tth_tree.hh>

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

Event::Event(plist _particles, plist _jets, plist _gen_jets, plist _leptons, plist _gen_leptons, plist _top_decays, plist _w_decays, plist _higgs_decays) :
particles(_particles),
jets(_jets),
gen_jets(_gen_jets),
leptons(_leptons),
gen_leptons(_gen_leptons),
top_decays(_top_decays),
w_decays(_w_decays),
higgs_decays(_higgs_decays)
{
}

Event::~Event() {
	for (auto* v : particles) {
		delete v;
	}
}

std::ostream& operator<<(std::ostream& os, const Particle& obj)
{
  	using namespace std;
  	os << obj.p4.Pt() << " " << obj.p4.Eta() << " " << obj.p4.Phi() << " " << obj.p4.M() << " " << obj.id;
  	os << " parents ";
  	for (auto* x : obj.parents) {
  		os << x << ",";
  	}
  	os << " children ";
  	for (auto* x : obj.children) {
  		os << x << ",";
  	}
  	os << endl;
  	return os;
}

Event* TTHTree::as_event() {
	std::vector<Particle*> particles;
	std::vector<Particle*> jets;
	std::vector<Particle*> gen_jets;
	std::vector<Particle*> w_decay;
	std::vector<Particle*> top_decay;
	std::vector<Particle*> higgs_decay;
	std::vector<Particle*> leptons;
	std::vector<Particle*> gen_leptons;
	
	for (int i=0;i < n__jet; i++) {
		Particle* jet = new Particle(jet__pt[i], jet__eta[i], jet__phi[i], jet__mass[i], jet__id[i], i);
		particles.push_back(jet);
		jets.push_back(jet);
	}
	
	for (int i=0;i < n__jet; i++) {
		Particle* jet = new Particle(gen_jet__pt[i], gen_jet__eta[i], gen_jet__phi[i], gen_jet__mass[i], gen_jet__id[i], i);
		particles.push_back(jet);
		gen_jets.push_back(jet);
	}
	
	for (int i=0;i < n__lep; i++) {
		Particle* lep = new Particle(lep__pt[i], lep__eta[i], lep__phi[i], lep__mass[i], lep__id[i], i);
		particles.push_back(lep);
		leptons.push_back(lep);
	}
	
	for (int i=0;i < n__lep; i++) {
		Particle* lep = new Particle(gen_lep__pt[i], gen_lep__eta[i], gen_lep__phi[i], gen_lep__mass[i], gen_lep__id[i], i);
		particles.push_back(lep);
		gen_leptons.push_back(lep);
	}
	
	Particle* d1 = new Particle(gen_t__w_d1__pt, gen_t__w_d1__eta, gen_t__w_d1__phi, gen_t__w_d1__mass, gen_t__w_d1__id);
	w_decay.push_back(d1);
	particles.push_back(d1);
	
	Particle* d2 = new Particle(gen_t__w_d2__pt, gen_t__w_d2__eta, gen_t__w_d2__phi, gen_t__w_d2__mass, gen_t__w_d2__id);
	w_decay.push_back(d2);
	particles.push_back(d2);
	
	Particle* d3 = new Particle(gen_tbar__w_d1__pt, gen_tbar__w_d1__eta, gen_tbar__w_d1__phi, gen_tbar__w_d1__mass, gen_tbar__w_d1__id);
	w_decay.push_back(d3);
	particles.push_back(d3);
	
	Particle* d4 = new Particle(gen_tbar__w_d2__pt, gen_tbar__w_d2__eta, gen_tbar__w_d2__phi, gen_tbar__w_d2__mass, gen_tbar__w_d2__id);
	w_decay.push_back(d4);
	particles.push_back(d4);
	
	Particle* d5 = new Particle(gen_t__b__pt, gen_t__b__eta, gen_t__b__phi, gen_t__b__mass, 5);
	top_decay.push_back(d5);
	particles.push_back(d5);
	
	Particle* d6 = new Particle(gen_tbar__b__pt, gen_tbar__b__eta, gen_tbar__b__phi, gen_tbar__b__mass, -5);
	top_decay.push_back(d6);
	particles.push_back(d6);
	
	Particle* d7 = new Particle(gen_b__pt, gen_b__eta, gen_b__phi, gen_b__mass, 5);
	higgs_decay.push_back(d7);
	particles.push_back(d7);
	
	Particle* d8 = new Particle(gen_bbar__pt, gen_bbar__eta, gen_bbar__phi, gen_bbar__mass, -5);
	higgs_decay.push_back(d8);
	particles.push_back(d8);
	
	return new Event(particles, jets, gen_jets, leptons, gen_leptons, top_decay, w_decay, higgs_decay);
}
