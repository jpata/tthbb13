#ifndef GEN_ASSOCIATION_H
#define GEN_ASSOCIATION_H

#include "TTH/TTHNtupleAnalyzer/interface/tth_tree.hh"
#include "TTH/TTHNtupleAnalyzer/interface/helpers.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include <iostream>
#include <vector>

void gen_association(edm::Handle<edm::View<reco::GenParticle>> pruned, 
		     TTHTree* tthtree,
		     // These vectors will be filled by gen_association - pass empty
		     std::vector<const reco::GenParticle*> & tops_last,
		     std::vector<const reco::GenParticle*> & antitops_last,		     
		     //first top quarks of chain
		     std::vector<const reco::Candidate*> & tops_first,
		     std::vector<const reco::Candidate*> & antitops_first,		     
		     std::vector<const reco::GenParticle*> & bquarks,
		     std::vector<const reco::GenParticle*> & antibquarks);

int is_hadronic_top(const reco::Candidate* p);

void get_hard_partons(edm::Handle<edm::View<reco::GenParticle>> pruned, 
		      double min_parton_pt,
		      std::vector<const reco::GenParticle*> & hard_partons);

#endif
