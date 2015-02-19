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
import numpy as np

#samples = ["tthbb_13TeV", "ttjets_13TeV"]
samples = [
	"tthbb_8TeV_noME__slSeq__cplots",
	"tthbb_8TeV_noME__slCatLSeq__cplots",
	"tthbb_8TeV_noME__slCatHSeq__cplots",

	"tthbb_8TeV_noME__dlSeq__cplots",
	"tthbb_8TeV_noME__dlCatLSeq__cplots",
	"tthbb_8TeV_noME__dlCatHSeq__cplots",

	"tthbb_13TeV_phys14__slSeq__cplots",
	"tthbb_13TeV_phys14__slCatLSeq__cplots",
	"tthbb_13TeV_phys14__slCatHSeq__cplots",

	"tthbb_13TeV_phys14__dlSeq__cplots",
	"tthbb_13TeV_phys14__dlCatLSeq__cplots",
	"tthbb_13TeV_phys14__dlCatHSeq__cplots",

	"ttjets_8TeV_noME__slSeq__cplots",
	"ttjets_8TeV_noME__slCatLSeq__cplots",
	"ttjets_8TeV_noME__slCatHSeq__cplots",
	"ttjets_8TeV_noME__dlSeq__cplots",
	"ttjets_8TeV_noME__dlCatLSeq__cplots",
	"ttjets_8TeV_noME__dlCatHSeq__cplots",
	"ttjets_13TeV_phys14__slSeq__cplots",
	"ttjets_13TeV_phys14__slCatLSeq__cplots",
	"ttjets_13TeV_phys14__slCatHSeq__cplots",
	"ttjets_13TeV_phys14__dlSeq__cplots",
	"ttjets_13TeV_phys14__dlCatLSeq__cplots",
	"ttjets_13TeV_phys14__dlCatHSeq__cplots",

]

sample_pairs = [
	("tthbb_8TeV_noME__slSeq__cplots", "tthbb_13TeV_phys14__slSeq__cplots"),
	("tthbb_8TeV_noME__dlSeq__cplots", "tthbb_13TeV_phys14__dlSeq__cplots"),
	("tthbb_8TeV_noME__slCatLSeq__cplots", "tthbb_13TeV_phys14__slCatLSeq__cplots"),
	("tthbb_8TeV_noME__slCatHSeq__cplots", "tthbb_13TeV_phys14__slCatHSeq__cplots"),
	("tthbb_8TeV_noME__dlCatLSeq__cplots", "tthbb_13TeV_phys14__dlCatLSeq__cplots"),
	("tthbb_8TeV_noME__dlCatHSeq__cplots", "tthbb_13TeV_phys14__dlCatHSeq__cplots"),

	("ttjets_8TeV_noME__slSeq__cplots", "ttjets_13TeV_phys14__slSeq__cplots"),
	("ttjets_8TeV_noME__dlSeq__cplots", "ttjets_13TeV_phys14__dlSeq__cplots"),
	("ttjets_8TeV_noME__slCatLSeq__cplots", "ttjets_13TeV_phys14__slCatLSeq__cplots"),
	("ttjets_8TeV_noME__slCatHSeq__cplots", "ttjets_13TeV_phys14__slCatHSeq__cplots"),
	("ttjets_8TeV_noME__dlCatLSeq__cplots", "ttjets_13TeV_phys14__dlCatLSeq__cplots"),
	("ttjets_8TeV_noME__dlCatHSeq__cplots", "ttjets_13TeV_phys14__dlCatHSeq__cplots"),
]

def sample_name(s):
	ret = "$"
	if "tthbb" in s:
		ret += "t\\bar{t} + H"
	if "ttjets" in s:
		ret += "t\\bar{t} + \\mathrm{jets}"
	ret += "$"

	if "8TeV" in s:
		ret += " 8 TeV"
	if "13TeV" in s:
		ret += " 13 TeV"

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

def sample_weight(sample):
	if "tthbb" in sample:
		if "8TeV" in sample:
			return (0.5085 / 0.1293) * 20.0/12.0
		else:
			if "13TeV_phys14" in sample:
				return 20000 * (0.5085) * 0.569 / 199700.0
	elif "ttjets" in sample:
		if "8TeV" in sample:
			return (831.76  /  252.89) * 20.0/12.0
		else:
			if "13TeV_phys14" in sample:
				return 20000 * (831.76) / 25405611

def axis_label(var):
	if "lep1_pt" in var:
		return "leading lepton $p_{t}$ [GeV]"
	if "lep2_pt" in var:
		return "subleading lepton $p_{t}$ [GeV]"
	if "njets" in var:
		return "$N_{j}$"
	if "ntags" in var:
		return "$N_{b,CSVM}$"
	if "btag_lr" in var:
		return "$b_{LR}$"
	if "wqq_pt" in var:
		return "$p_{t,q,gen}$ [GeV] of quarks from W"
	if "wqq_eta" in var:
		return "$\\eta_{q,gen}$ of quarks from W"

def get_by_categories(h2):
	assert(h2 != None)
	hs = []
	for i in range(2,8):
		h = h2.ProjectionY(h2.GetName() + "_cat{0}".format(i), i,i)
		h = asrootpy(h).Clone()
		hs += [h]
	return hs

def rebin(h, var):
	if "btag_lr" in var:
		h.Rebin(5)

def yield_plot(tf, s1, s2, w1, w2):

    catyields = {}
    for lep in ["sl", "dl"]:
        for cat in ["H", "L"]:
            _s1 = s1 + "__" + lep + "Cat" + cat + "Seq__cplots" 
            _s2 = s2 + "__" + lep + "Cat" + cat + "Seq__cplots" 
            h1 = tf.Get(_s1 + "__cat")
            h2 = tf.Get(_s2 + "__cat")

            assert(h1!=None)
            assert(h2!=None)
            h1 = asrootpy(h1).Clone()
            h2 = asrootpy(h2).Clone()

            for i in range(2,8):
                catyields[(lep, cat, i-2)] = (h1.GetBinContent(i)*w1, h2.GetBinContent(i)*w2, h1.GetBinError(i)*w1, h2.GetBinError(i)*w2)
    return catyields

def get_discriminator_hists(tf, postf):
    hs = {}
    for sample in ["tthbb_8TeV_ME", "tthbb_13TeV_phys14", "ttjets_8TeV_ME", "ttjets_13TeV_phys14"]:
        h = tf.Get(sample + "__" + postf)
        for i in range(2,8):
            hn = "{0}/{1}/cat{2}".format(sample, postf, i-2)
            hs[hn] = asrootpy(h.ProjectionY(hn, i, i))
            hs[hn].Scale(sample_weight(sample))
    return hs

def get_cat_fails(tf, hn):
    hs = {}
    for i in range(2,8):
        h1 = asrootpy(tf.Get(hn).ProjectionY(str(i), i,i))
        bs = [h1.GetBinContent(j) for j in range(1,4)]
        hs[hn + "/" + str(i-2)] = bs
    return hs

def draw_mismatches(tf, sample, pref):
    d = get_cat_fails(tf, "{0}__slCatHSeq__meplots__{1}".format(sample, pref))
    d.update(get_cat_fails(tf, "{0}__dlCatHSeq__meplots__{1}".format(sample, pref)))
    d.update(get_cat_fails(tf, "{0}__slCatLSeq__meplots__{1}".format(sample, pref)))
    d.update(get_cat_fails(tf, "{0}__dlCatLSeq__meplots__{1}".format(sample, pref)))

    #fig = plt.figure(figsize=(16,16))
    btags = ["H", "L"]
    m_ax = plt.axes([0.0, 0.0, 0.6, 0.2])
    for i in range(2):
        for j in range(6):
            ax = plt.axes([j*0.1, i*0.1, 0.1, 0.1])
            if j<3:
                lep = "sl"
            else:
                lep = "dl"
            btag = btags[i]
            cat = j
            effs = d["{3}__{0}Cat{1}Seq__meplots__{4}/{2}".format(lep, btag, cat, sample, pref)]
            if sum(effs)>0:
                effs = [e/sum(effs) for e in effs]
            ax.pie(effs, colors=["red", "yellow", "green"])
            #ax.set_title(btag + str(cat), y=0.6)
    m_ax.set_xticks([(x + 0.5)/6 for x in range(6)])
    m_ax.set_xticklabels(["cat 1", "cat 2", "cat 3", "DL $\\mu\\mu$", "DL $e\\mu$", "DL $ee$"])
    m_ax.set_yticks([0.25, 0.75])
    m_ax.set_yticklabels(["H", "L"])
    return d


if __name__ == "__main__":

	tf = ROOT.TFile(sys.argv[1])

	for k in tf.GetListOfKeys():
		print "*", k.GetName()

	variables_1d = [
		"lep1_pt", "lep2_pt",
		"lep1_iso", "lep2_iso",
		"njets", "ntags",
		"btag_lr", "btag_lr2",
		#"Vtype", "type",
		#"cat",
		#"rad",
		# "lepton_pt_sl", "lepton1_pt_dl", "lepton2_pt_dl",
		# "numJets_sl", "numJets_dl",
		# "numBTagM_dl", "numBTagM_sl",
		# "btag_lr_dl", "btag_lr_dl2",
		# "btag_lr_sl", "btag_lr_sl2",
		# "category", "categoryH", "categoryL"
	]

	for sample in samples:
		for var in variables_1d:
			print sample + "__" + var
			h = tf.Get(sample + "__" + var)

			assert(h != None)
			h = asrootpy(h.Clone())

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

	for sample in [
		"tthbb_8TeV_ME__slCatHSeq__meplots",
		"tthbb_8TeV_ME__dlCatHSeq__meplots",
		"tthbb_13TeV_phys14__slCatHSeq__meplots",
		"tthbb_13TeV_phys14__dlCatHSeq__meplots"
		]:
		hs = get_by_categories(tf.Get(sample + "__" + "cat_discr"))
		for (i, h) in enumerate(hs):
			h.Scale(sample_weight(sample))
			fig = plt.figure(figsize=(8,8))
			ax = plt.axes()
			b1 = he.barhist(h, color="red", lw=2)
			plt.title(parse_title(h.GetTitle()))
			plt.savefig(sample + "_cat{0}_discr.png".format(i))
			plt.close()

	for (s1, s2) in sample_pairs:
		for var in variables_1d:
			print s1, s2, var
			h1 = tf.Get(s1 + "__" + var)
			h2 = tf.Get(s2 + "__" + var)
			assert(h1 != None)
			assert(h2 != None)
			h1 = asrootpy(h1).Clone()
			h2 = asrootpy(h2).Clone()

			rebin(h1, var)
			rebin(h2, var)

			for instr in ["", "normalized"]:
				fig = plt.figure(figsize=(8,8))
				ax = plt.axes()
				#ax.grid()

				if "normalized" in instr:
					if h1.Integral()>0:
						h1.Scale(1.0 / h1.Integral())
					if h2.Integral()>0:
						h2.Scale(1.0 / h2.Integral())
				else:
					h1.Scale(sample_weight(s1))
					h2.Scale(sample_weight(s2))

				b1 = he.barhist(h1, color="red", lw=2, label=sample_name(s1))
				b2 = he.barhist(h2, color="blue", lw=2, label=sample_name(s2))

				configure_ticks(ax, var)

				if "normalized" in instr:
					plt.ylabel("normalized events / bin")
				else:
					plt.ylabel("events / 20 $fb^{-1}$/ bin")
				plt.xlabel(axis_label(var))

				#ax.xaxis.grid(True, which='minor')
				plt.legend()
				plt.title(parse_title(h1.GetTitle()))

				plt.savefig(s1 + "_" + s2 + "_" + var + "_" + instr + ".png")
				plt.close()

	for (s1, s2) in [("tthbb_8TeV_noME", "tthbb_13TeV_phys14"), ("ttjets_8TeV_noME", "ttjets_13TeV_phys14")]:
		yt = yield_plot(tf, s1, s2, sample_weight(s1), sample_weight(s2))

		fig = plt.figure(figsize=(8,8))
		xs = np.linspace(1, 12, 12)
		ys1 = ([yt["sl", "H", i][0] for i in range(3)] + [yt["dl", "H", i][0] for i in range(3,6)] +
		    [yt["sl", "L", i][0] for i in range(3)] + [yt["dl", "L", i][0] for i in range(3,6)])
		ys1e = ([yt["sl", "H", i][2] for i in range(3)] + [yt["dl", "H", i][2] for i in range(3,6)] +
		    [yt["sl", "L", i][2] for i in range(3)] + [yt["dl", "L", i][2] for i in range(3,6)])

		ys2 = ([yt["sl", "H", i][1] for i in range(3)] + [yt["dl", "H", i][1] for i in range(3,6)] + 
		    [yt["sl", "L", i][1] for i in range(3)] + [yt["dl", "L", i][1] for i in range(3,6)])
		ys2e = ([yt["sl", "H", i][3] for i in range(3)] + [yt["dl", "H", i][3] for i in range(3,6)] + 
		    [yt["sl", "L", i][3] for i in range(3)] + [yt["dl", "L", i][3] for i in range(3,6)])

		plt.bar(xs+0.1, ys1, 0.3, yerr=ys1e, color="red", ecolor="black", label="8 TeV scaled to 13 TeV")
		plt.bar(xs+0.1+0.3+0.1, ys2, 0.3, yerr=ys2e, color="green", ecolor="black", label="13 TeV")
		plt.legend()
		plt.xticks(xs+0.5, ["cat 1 H", "cat 2 H", "cat 3 H", "DL $\\mu\\mu$ H", "DL $e\\mu$ H", "DL $ee$ H",
		                    "cat 1 L", "cat 2 L", "cat 3 L", "DL $\\mu\\mu$ L", "DL $e\\mu$ L", "DL $ee$ L"
		], rotation=90)
		plt.grid()
		plt.xlim(1, 13)
		plt.axvline(7-0.05)
		plt.ylabel("expected yield / 20 $fb^{-1}$ at $\\sqrt{s} = 13 TeV$")
		plt.savefig(s1 + "_" + s2 + "_yields.png")
		plt.close()
		#plt.bar([2], [b], 1, color="green")

	hs = get_discriminator_hists(tf, "slCatLSeq__meplots__cat_discr")
	hs.update(get_discriminator_hists(tf, "dlCatLSeq__meplots__cat_discr"))

	hs.update(get_discriminator_hists(tf, "slCatHSeq__meplots__cat_discr"))
	hs.update(get_discriminator_hists(tf, "dlCatHSeq__meplots__cat_discr"))

	for (s1, s2) in [("tthbb_8TeV_ME", "tthbb_13TeV_phys14"), ("ttjets_8TeV_ME", "ttjets_13TeV_phys14")]:
		for lep in ["sl", "dl"]:
			for cat in range(6):
				if lep == "sl" and cat>2:
					continue
				if lep == "dl" and cat<3:
					continue
				fig = plt.figure(figsize=(8,8))
				h1 = hs["{0}/{1}CatHSeq__meplots__cat_discr/cat{2}".format(s1, lep, cat)]
				h2 = hs["{0}/{1}CatHSeq__meplots__cat_discr/cat{2}".format(s2, lep, cat)]
				h1.Scale(1.0 / h1.Integral())
				h2.Scale(1.0 / h2.Integral())

				he.barhist(h1, color="blue", lw=2, label=sample_name(s1))
				he.barhist(h2, color="red", lw=2, label=sample_name(s2))
				plt.xlabel("$p_s / (p_s + 0.02 p_b)$", fontsize=16)
				#plt.ylabel("Expected events / 20 $\\mathrm{fb}^{-1}$ / bin")
				plt.ylabel("Normalized events / bin")
				plt.grid()
				plt.legend()
				plt.xticks(np.linspace(0.0, 1.0, 7))
				plt.savefig(s1 + "_" + s2 + "_" + lep + "cat{0}H_discr.png".format(cat))
				plt.close()
		for mismatch in ["cat_n_wqq_matched", "cat_n_bt_matched", "cat_n_bh_matched"]:
			for s in [s1, s2]:
				fig = plt.figure(figsize=(16,16))
				draw_mismatches(tf, s, mismatch)
				plt.savefig(s + "_" + mismatch + ".png", bbox_inches='tight', pad_inches=0)
				plt.close()

	# for tostack in [("tthbb_13TeV", "ttjets_13TeV")]:
	# 	for var in variables:
	# 		s1, s2 = tostack
	# 		h1 = asrootpy(tf.Get(s1 + "_" + var).Clone())
	# 		h2 = asrootpy(tf.Get(s2 + "_" + var).Clone())

	# 		h1.SetFillColor(ROOT.kRed)
	# 		h2.SetFillColor(ROOT.kBlue)

	# 		c = ROOT.TCanvas("c", "c", 800, 800)
	# 		st = ROOT.THStack()
	# 		st.Add(h1)
	# 		st.Add(h2)

	# 		st.Draw()

	# 		h1.SetStats(False)
	# 		#st.GetXaxis().SetTitle(axis_label(var))
	# 		h1.SetTitle(parse_title(h1.GetTitle()))

	# 		st.Draw("SAME H2")
	# 		c.SaveAs("fullstack_" + var + ".png")
