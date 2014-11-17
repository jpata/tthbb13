#!/usr/bin/env python
#simple gen-particle loop
#extracts top quarks from MINIAODSIM
import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *
import numpy as np

#provide input files from cmdline
events = Events (sys.argv[1:])

#handles for gen particles
handlePruned = Handle ("std::vector<reco::GenParticle>")
handlePacked = Handle ("std::vector<pat::PackedGenParticle>")
labelPruned = ("prunedGenParticles")
labelPacked = ("packedGenParticles")

#output file
outfile = ROOT.TFile("out.root", "RECREATE")
outtree = ROOT.TTree("tree", "tree")
outtree.SetDirectory(outfile)

#branches for top quark properties in output file
top_pt = np.zeros(1, dtype=np.float32)
top_eta = np.zeros(1, dtype=np.float32)
top_phi = np.zeros(1, dtype=np.float32)
top_mass = np.zeros(1, dtype=np.float32)
top_id = np.zeros(1, dtype=np.float32)
top_status = np.zeros(1, dtype=np.int32)
top_event = np.zeros(1, dtype=np.int32)
top_mothers = np.zeros(100, dtype=np.int32)
top_daughters = np.zeros(100, dtype=np.int32)
top_nmothers = np.zeros(1, dtype=np.int32)
top_ndaughters = np.zeros(1, dtype=np.int32)

outtree.Branch("top_event", top_event, "top_event/I")
outtree.Branch("top_pt", top_pt, "top_pt/F")
outtree.Branch("top_eta", top_eta, "top_eta/F")
outtree.Branch("top_phi", top_phi, "top_phi/F")
outtree.Branch("top_mass", top_mass, "top_mass/F")
outtree.Branch("top_id", top_id, "top_id/I")
outtree.Branch("top_status", top_status, "top_status/I")
outtree.Branch("top_nmothers", top_nmothers, "top_nmothers/I")
outtree.Branch("top_ndaughters", top_ndaughters, "top_ndaughters/I")
outtree.Branch("top_mothers", top_mothers, "top_mothers[top_nmothers]/I")
outtree.Branch("top_daughters", top_daughters, "top_daughters[top_ndaughters]/I")

DEF = -99

# loop over events
count= 0
for event in events:
		count += 1
		event.getByLabel (labelPacked, handlePacked)
		event.getByLabel (labelPruned, handlePruned)

		#get the genparticles
		packed = handlePacked.product()
		pruned = handlePruned.product()

		#loop over gen particles in event
		for p in pruned:

			#initialize branch variables
			top_pt[:] = DEF
			top_eta[:] = DEF
			top_phi[:] = DEF
			top_mass[:] = DEF
			top_id[:] = DEF
			top_status[:] = DEF
			top_event[:] = DEF
			top_mothers[:] = DEF
			top_daughters[:] = DEF
			top_nmothers[:] = 0
			top_ndaughters[:] = 0

			#is a top quark, fill
			if abs(p.pdgId())==6:
				top_event[0] = count
				top_status[0] = p.status()
				top_id[0] = p.pdgId()
				top_pt[0] = p.pt()
				top_eta[0] = p.eta()
				top_phi[0] = p.phi()
				top_mass[0] = p.mass()
				top_nmothers[0] = p.numberOfMothers()
				top_ndaughters[0] = p.numberOfDaughters()

				for i in range(min(p.numberOfMothers(), 10)):
					top_mothers[i] = p.mother(i).pdgId()
				for i in range(min(p.numberOfDaughters(), 10)):
					top_daughters[i] = p.daughter(i).pdgId()
		#			print ",".join(map(str, (count, p.pdgId(), p.pt(), p.eta(), p.phi(), p.mass(), p.status(),
		#				[p.mother(i).pdgId() for i in xrange(0, p.numberOfMothers())],
		#				[p.daughter(i).pdgId() for i in xrange(0, p.numberOfDaughters())]))
		#			)
				outtree.Fill()

outtree.SetDirectory(outfile)
#outtree.Write()
outfile.Write("", ROOT.TObject.kOverwrite)
outfile.Close()
