#!/usr/bin/env python
import ROOT, sys

f = ROOT.TFile(sys.argv[1])

tree = f.Get("tree")

if not tree or tree.IsZombie():
    raise Exception("could not open TTree 'tree'")

of = ROOT.TFile(sys.argv[2], "RECREATE")
of.cd()

hjets = {
	"n": ROOT.TH1D("nJets", "nJets", 10, 0, 10),
	"pt": ROOT.TH1D("jet_pt", "jet_pt", 100, 0, 300),
	"eta": ROOT.TH1D("jet_eta", "jet_eta", 100, -5, 5),
	"phi": ROOT.TH1D("jet_phi", "jet_phi", 100, -4, 4)
}

hlep = {
	"n": ROOT.TH1D("nLep", "nLep", 10, 0, 10),
	"pt": ROOT.TH1D("lepton_pt", "lepton_pt", 100, 0, 300),
	"eta": ROOT.TH1D("lepton_eta", "lepton_eta", 100, -5, 5),
	"phi": ROOT.TH1D("lepton_phi", "lepton_phi", 100, -4, 4)
}

hbtag = {
	"lr": ROOT.TH1D("btag_LR", "btag_LR", 100, 0, 1),
}

hall = {
	"Mtln": ROOT.TH1D("Mtln", "Mtln", 100, 0, 300),
	"Mtll": ROOT.TH1D("Mtll", "Mtll", 100, 0, 300),
}

for ev in tree:
	hjets["n"].Fill(ev.nJet)
	for i in range(ev.nJet):
		hjets["pt"].Fill(ev.jet_pt[i])
		hjets["eta"].Fill(ev.jet_eta[i])
		hjets["phi"].Fill(ev.jet_phi[i])

	hlep["n"].Fill(ev.nLep)
	for i in range(ev.nLep):
		hlep["pt"].Fill(ev.lepton_pt[i])
		hlep["eta"].Fill(ev.lepton_eta[i])
		hlep["phi"].Fill(ev.lepton_phi[i])
	hbtag["lr"].Fill(ev.btag_LR)
	hall["Mtln"].Fill(ev.Mtln)
	hall["Mtll"].Fill(ev.Mtll)

of.Write()
of.Close()
