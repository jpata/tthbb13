#!/usr/bin/env python
import ROOT, sys

f = ROOT.TFile(sys.argv[1])

tree = f.Get("tthNtupleAnalyzer/events")

if not tree or tree.IsZombie():
    raise Exception("could not open ttree tthNtupleAnalyzer/events")

of = ROOT.TFile(sys.argv[2], "RECREATE")
of.cd()

hleps = {}
hleps_tau = {}
hsleps = {}

for (a, b) in [(hleps, ""), (hsleps, "sig_")]:
	a["n"] = ROOT.TH1D("n__%slep"%b, "", 20, 0, 20)
	a["pt"] = ROOT.TH1D(b+"lep__pt", "", 100, 0, 400)
	a["eta"] = ROOT.TH1D(b+"lep__eta", "", 100, -5, 5)
	a["phi"] = ROOT.TH1D(b+"lep__phi", "", 100, -4, 4)
	a["mass"] = ROOT.TH1D(b+"lep__mass", "", 100, 0, 400)
	a["id"] = ROOT.TH1D(b+"lep__id", "", 41, -20, 20)

for (a, b) in [(hleps_tau, "")]:
	a["n"] = ROOT.TH1D("n__%stau"%b, "", 20, 0, 20)
	a["pt"] = ROOT.TH1D(b+"tau__pt", "", 100, 0, 400)
	a["eta"] = ROOT.TH1D(b+"tau__eta", "", 100, -5, 5)
	a["phi"] = ROOT.TH1D(b+"tau__phi", "", 100, -4, 4)
	a["mass"] = ROOT.TH1D(b+"tau__mass", "", 100, 0, 400)
	a["lead_ch_had__pt"] = ROOT.TH1D(b+"tau__lead_ch_had__pt", "", 100, 0, 400)
	a["pf_jet__pt"] = ROOT.TH1D(b+"tau__pf_jet__pt", "", 100, 0, 400)
	a["pf_cjet__pt"] = ROOT.TH1D(b+"tau__pf_cjet__pt", "", 100, 0, 400)
	a["id__ch_iso"] = ROOT.TH1D(b+"tau__id__ch_iso", "", 100, 0, 400)
	a["id"] = ROOT.TH1D(b+"tau__id", "", 41, -20, 20)

hjets = {}
hgjets = {}
for (a, b) in [(hjets, ""), (hgjets, "gen_")]:
	a["n"] = ROOT.TH1D("n__%sjet"%b, "", 20, 0, 20)
	a["pt"] = ROOT.TH1D(b+"jet__pt", "", 100, 0, 400)
	a["eta"] = ROOT.TH1D(b+"jet__eta", "", 100, -5, 5)
	a["phi"] = ROOT.TH1D(b+"jet__phi", "", 100, -4, 4)
	a["mass"] = ROOT.TH1D(b+"jet__mass", "", 100, 0, 400)
	a["id"] = ROOT.TH1D(b+"jet__id", "", 41, -20, 20)
	a["bd_csv"] = ROOT.TH1D(b+"jet__bd_csv", "", 41, 0, 1)
	a["bd_cisvv2"] = ROOT.TH1D(b+"jet__bd_cisvv2", "", 41, 0, 1)
	a["pileupJetId"] = ROOT.TH1D(b+"jet__pileupJetId", "", 41, 0, 1)
	#a["bd_tchp"] = ROOT.TH1D(b+"jet__bd_tchp", "", 41, 0, 1)

hgentop = {}

for t in ["t", "tbar", "t2", "tbar2"]:
	for (x, n1, n2) in [
			("pt", 0, 400),
			("eta", -5, 5),
			("phi", -4, 4),
			("mass", 0, 400),
			("b__pt", 0, 400),
			("b__eta", -5, 5),
			("b__phi", -4, 4),
			("b__mass", 0, 400),
			("w_d1__pt", 0, 400),
			("w_d1__eta", -5, 5),
			("w_d1__phi", -4, 4),
			("w_d1__mass", 0, 400),
			("w_d1__id", -400, 400),
			("w_d2__pt", 0, 400),
			("w_d2__eta", -5, 5),
			("w_d2__phi", -4, 4),
			("w_d2__mass", 0, 400),
			("w_d2__id", -400, 400),
		]:
		s = "gen_%s__%s" % (t, x)
		hgentop[s] = ROOT.TH1D(s, "", 100, n1, n2)

for ev in tree:
	hleps["n"].Fill(ev.n__lep)
	hleps_tau["n"].Fill(ev.n__tau)
	for i in range(ev.n__lep):
		for v in ["pt", "eta", "phi", "mass", "id"]:
			hleps[v].Fill(getattr(ev, "lep__"+v, 0)[i])
	for i in range(ev.n__tau):
		for v in ["pt", "eta", "phi", "mass", "id", "lead_ch_had__pt", "pf_jet__pt", "pf_cjet__pt", "id__ch_iso"]:
			hleps_tau[v].Fill(getattr(ev, "tau__"+v, 0)[i])

	hsleps["n"].Fill(ev.n__sig_lep)
	for i in range(ev.n__sig_lep):
		for v in ["pt", "eta", "phi", "mass", "id"]:
			hsleps[v].Fill(getattr(ev, "sig_lep__"+v, 0)[i])

	hjets["n"].Fill(ev.n__jet)
	for i in range(ev.n__jet):
		for v in ["pt", "eta", "phi", "mass", "id", "bd_csv", "bd_cisvv2", "pileupJetId"]:
			hjets[v].Fill(getattr(ev, "jet__"+v, 0)[i])

	hgjets["n"].Fill(ev.n__jet)
	for i in range(ev.n__jet):
		for v in ["pt", "eta", "phi", "mass", "id"]:
			hgjets[v].Fill(getattr(ev, "gen_jet__"+v, 0)[i])

	for k in hgentop.keys():
		hgentop[k].Fill(getattr(ev, k, 0))
of.Write()
of.Close()
