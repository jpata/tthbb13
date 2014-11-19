#ifndef GEN_ASSOCIATION_H
#define GEN_ASSOCIATION_H

#include "TTH/TTHNtupleAnalyzer/interface/tth_tree.hh"
#include "TTH/TTHNtupleAnalyzer/interface/helpers.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include <iostream>

void gen_association(edm::Handle<edm::View<reco::GenParticle>> pruned, TTHTree* tthtree);

#endif
