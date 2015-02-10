import ROOT
ROOT.gROOT.SetBatch(True)
import sys, os
sys.path += ["./heplot/"]
import heplot.heplot as he
from rootpy.plotting import Hist, Hist2D
import matplotlib.pyplot as plt
import random
import matplotlib
from rootpy import asrootpy
from matplotlib.ticker import NullLocator, LinearLocator, MultipleLocator, FormatStrFormatter, AutoMinorLocator

tf = ROOT.TFile("outfile.root")

samples = ["tthbb_13TeV", "ttjets_13TeV"]

def sample_name(s):
	ret = "$"
	if "tthbb" in s:
		ret += "t\\bar{t} + H"
	if "ttjets" in s:
		ret += "t\\bar{t} + \\mathrm{jets}"
	ret += "$"
	return ret

def configure_ticks(ax, var):
	#majorLocatorX = LinearLocator(10)
	minorLocatorX = AutoMinorLocator()

	#ax.xaxis.set_major_locator(majorLocatorX)
	ax.xaxis.set_minor_locator(minorLocatorX)

	#majorLocatorY = MultipleLocator()
	minorLocatorY = AutoMinorLocator()

	#ax.yaxis.set_major_locator(majorLocatorY)
	ax.yaxis.set_minor_locator(minorLocatorY)

	ax.tick_params(which="major", length=10)
	ax.tick_params(which="minor", length=5)

	if "category" in var:
		ax.set_xlim(1,7)
		ax.set_xticks([x + 0.5 for x in range(1,7)])
		ax.set_xticklabels([
			"cat 1", "cat 2", "cat 3",
			"cat 6 ee", "cat 6 emu", "cat 6 mumu"],
			rotation=90
		)
		ax.xaxis.set_minor_locator(NullLocator())

def parse_title(t):
	t = t.replace("_", " ")
	return t

def axis_label(var):
	if "lepton_pt" in var:
		return "$p_{t,l}$ [GeV]"
	if "numJets" in var:
		return "$N_{j}$"
	if "numBTagM" in var:
		return "$N_{b,CSVM}$"
	if "btag_lr" in var:
		return "$b_{LR}$"
	if "wqq_pt" in var:
		return "$p_{t,q,gen}$ [GeV] of quarks from W"
	if "wqq_eta" in var:
		return "$\\eta_{q,gen}$ of quarks from W"
if __name__ == "__main__":

	tf = ROOT.TFile(sys.argv[1])
	variables = [
		"lepton_pt_sl", "lepton1_pt_dl", "lepton2_pt_dl",
		"numJets_sl", "numJets_dl",
		"numBTagM_dl", "numBTagM_sl",
		"btag_lr_dl", "btag_lr_dl2",
		"btag_lr_sl", "btag_lr_sl2",
		"category", "categoryH", "categoryL"
	]

	for sample in samples:
		for var in variables:
			print sample + "_" + var
			h = asrootpy(tf.Get(sample + "_" + var).Clone())
			assert(h != None)
			fig = plt.figure(figsize=(8,8))
			ax = plt.axes()
			#ax.grid()
			b1 = he.barhist(h, color="red", lw=2)
			plt.title(parse_title(h.GetTitle()))

			configure_ticks(ax, var)
			plt.ylabel("events / bin / L")
			plt.xlabel(axis_label(var))

			plt.savefig(sample + "_" + var + ".png")
			plt.close()

	for (s1, s2) in [("tthbb_13TeV", "ttjets_13TeV")]:
		for var in variables:
			print s1 + "_" + s2 + "_" + var
			h1 = asrootpy(tf.Get(s1 + "_" + var).Clone())
			h2 = asrootpy(tf.Get(s2 + "_" + var).Clone())
			assert(h != None)
			fig = plt.figure(figsize=(8,8))
			ax = plt.axes()
			#ax.grid()
			h1.Scale(1.0 / h1.Integral())
			h2.Scale(1.0 / h2.Integral())
			b1 = he.barhist(h1, color="red", lw=2, label=sample_name(s1))
			b2 = he.barhist(h2, color="blue", lw=2, label=sample_name(s2))

			configure_ticks(ax, var)

			plt.ylabel("normalized events")
			plt.xlabel(axis_label(var))

			#ax.xaxis.grid(True, which='minor')
			plt.legend()
			plt.title(parse_title(h1.GetTitle()))

			plt.savefig(s1 + "_" + s2 + "_" + var + ".png")
			plt.close()


	for tostack in [("tthbb_13TeV", "ttjets_13TeV")]:
		for var in variables:
			s1, s2 = tostack
			h1 = asrootpy(tf.Get(s1 + "_" + var).Clone())
			h2 = asrootpy(tf.Get(s2 + "_" + var).Clone())

			h1.SetFillColor(ROOT.kRed)
			h2.SetFillColor(ROOT.kBlue)

			c = ROOT.TCanvas("c", "c", 800, 800)
			st = ROOT.THStack()
			st.Add(h1)
			st.Add(h2)

			st.Draw()

			h1.SetStats(False)
			#st.GetXaxis().SetTitle(axis_label(var))
			h1.SetTitle(parse_title(h1.GetTitle()))

			st.Draw("SAME H2")
			c.SaveAs("fullstack_" + var + ".png")
