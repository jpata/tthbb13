from draw_control_plots import tf, samples, sample_name, configure_ticks, parse_title, axis_label

import heplot.heplot as he
from rootpy.plotting import Hist, Hist2D
import matplotlib.pyplot as plt
import random
import matplotlib
from rootpy import asrootpy
from matplotlib.ticker import NullLocator, LinearLocator, MultipleLocator, FormatStrFormatter, AutoMinorLocator
from math import factorial as fac
import math
import numpy

def calc_eff(s1, var):
	h1 = asrootpy(tf.Get(s1 + "_unmatched_" + var).Clone())
	h2 = asrootpy(tf.Get(s1 + "_matched_" + var).Clone())
	htot = h2.Clone("tot")
	htot.Add(h1)
	heff = h2.Clone(s1 + "_eff")
	print "eff", h2.Integral() / htot.Integral()
	heff.Divide(htot)
	return heff

for (s1, s2) in [("tthbb_13TeV", "ttjets_13TeV")]:
	for var in ["wqq_pt", "wqq_eta"]:
		eff1 = calc_eff(s1, var)
		#eff2 = calc_eff(s2, var)
		fig = plt.figure(figsize=(8,8))
		ax = plt.axes()
		b1 = he.barhist(eff1, color="red", lw=2, label=sample_name(s1))
		#b2 = he.barhist(eff2, color="blue", lw=2, label=sample_name(s2))
		configure_ticks(ax, var)
		plt.ylabel("efficiency to reconstruct $W \\rightarrow qq' $")
		plt.xlabel(axis_label(var))
		plt.ylim(bottom=0)
		#ax.xaxis.grid(True, which='minor')
		plt.legend()
		plt.title(parse_title(eff1.GetTitle()))
		plt.savefig("eff_" + s1 + "_" + s2 + "_" + var + ".png")
		plt.close()


def binomial(x, y):
    try:
        binom = fac(x) // fac(y) // fac(x - y)
    except ValueError:
        binom = 0
    return binom

def prob_theor(n, k, p):
	return binomial(n,k) * math.pow(p, k) * math.pow(1.0 - p, n-k)


h1 = asrootpy(tf.Get("tthbb_13TeV_nmatched_wqq").Clone())
#h2 = asrootpy(tf.Get("ttjets_13TeV_nmatched_wqq").Clone())
h1.Scale(1.0 / h1.Integral())
#h2.Scale(1.0 / h2.Integral())
fig = plt.figure(figsize=(8,8))
ax = plt.axes()

# for i in range(0,3):
# 	w = prob_theor(2, i, 0.8)
# 	h1.SetBinContent(i + 1, h1.GetBinContent(i + 1) / w)
# 	h1.SetBinError(i + 1, h1.GetBinError(i + 1) / w)

b1 = he.barhist(h1, color="red", lw=2, label=sample_name("tthbb_13TeV"))
##b2 = he.barhist(h2, color="blue", lw=2, label=sample_name("ttjets_13TeV"))

configure_ticks(ax, "nmatched_wqq")
plt.ylabel("efficiency to match N $W \\rightarrow qq' $ quarks as 'untagged'")
plt.xlabel("Number of matched quarks")
plt.xticks([0.5, 1.5, 2.5], [0,1,2])
plt.ylim(bottom=0, top=1.0)
plt.legend()
plt.title("cat1 H")
plt.savefig("eff_nmatched_tthbb.png")
plt.close()


h1 = asrootpy(tf.Get("tthbb_13TeV_nmatched_tagging_wqq").Clone())

print [h1.GetBinContent(1, i) for i in range(1,4)]
print [h1.GetBinContent(2, i) for i in range(1,4)]
print [h1.GetBinContent(3, i) for i in range(1,4)]

def get_lr_sig_bg(hn):
	h1 = asrootpy(tf.Get(hn).Clone())

	h_bb = asrootpy(h1.ProjectionX("bb", 1, 1))
	h_bj = asrootpy(h1.ProjectionX("bj", 2, 2))
	h_cc = asrootpy(h1.ProjectionX("cc", 3, 3))
	h_jj = asrootpy(h1.ProjectionX("jj", 4, 4))
	h_u = asrootpy(h1.ProjectionX("u", 5, 5))

	h_sig = h_jj.Clone("sig")
	h_bg = h_bb.Clone("bg")
	h_bg.Add(h_bj)
	h_bg.Add(h_cc)
	
	he.normalize(h_bg)
	he.normalize(h_sig)

	return h_bg, h_sig

def get_cumulative(h_sig, h_bg):
	h_sig_cum = asrootpy(h_sig.GetCumulative())
	h_bg_cum = asrootpy(h_bg.GetCumulative())

	h_sig_cum.Scale(1.0 / h_sig.Integral())
	h_bg_cum.Scale(1.0 / h_bg.Integral())

	return (h_bg_cum, h_sig_cum)


def roc(bg, sig):
	assert(bg.size == sig.size)

	bg = bg / bg[-1]
	sig = sig / sig[-1]

	assert(bg[-1] == 1)
	assert(sig[-1] == 1)

	out = numpy.zeros((bg.size, 2))
	for i in range(bg.size):
		out[i, 0] = sig[i]
		out[i, 1] = 1.0 - bg[i]
	return out

hlr1 = get_lr_sig_bg("ttjets_13TeV_btag_lr_rad")
hlr2 = get_lr_sig_bg("ttjets_13TeV_btag_lr2_rad")
hlr3 = get_lr_sig_bg("ttjets_13TeV_btag_lr3_rad")
hlr4 = get_lr_sig_bg("ttjets_13TeV_btag_lr4_rad")

# tf.Get("tree_s2").Draw("(btag_lr_l_bbbb / (btag_lr_l_bbjj + btag_lr_l_bbcc) >> sig(200, 0, 1)", "nMatchSimBs > 2 || nMatchSimCs > 1")
# tf.Get("tree_s2").Draw("(btag_lr_l_bbbb / (btag_lr_l_bbjj + btag_lr_l_bbcc) >> bg(200, 0, 1)", "nMatchSimBs==0 && nMatchSimCs <= 1")
# hlr5 = asrootpy(tf.Get("bg")), asrootpy(tf.Get("sig"))

fig = plt.figure(figsize=(8,8))
ax = plt.axes()
he.barhist(hlr1[0], color="blue", label="bb, bj, cc")
he.barhist(hlr1[1], color="red", label="jj")
plt.savefig("lr1.png")
plt.close()

fig = plt.figure(figsize=(8,8))
ax = plt.axes()
he.barhist(hlr2[0], color="blue", label="bb, bj, cc")
he.barhist(hlr2[1], color="red", label="jj")
plt.savefig("lr2.png")
plt.close()

fig = plt.figure(figsize=(8,8))
ax = plt.axes()
he.barhist(hlr3[0], color="blue", label="bb, bj, cc")
he.barhist(hlr3[1], color="red", label="jj")
plt.savefig("lr3.png")
plt.close()

fig = plt.figure(figsize=(8,8))
ax = plt.axes()
he.barhist(hlr4[0], color="blue", label="bb, bj, cc")
he.barhist(hlr4[1], color="red", label="jj")
plt.savefig("lr4.png")
plt.close()

# fig = plt.figure(figsize=(8,8))
# ax = plt.axes()
# he.barhist(hlr5[0], color="blue", label="bb, bj, cc")
# he.barhist(hlr5[1], color="red", label="jj")
# plt.savefig("lr5.png")
# plt.close()



lr1 = get_cumulative(*hlr1)
lr2 = get_cumulative(*hlr2)
lr3 = get_cumulative(*hlr3)
lr4 = get_cumulative(*hlr4)


roc_lr1 = roc(he.as_array(lr1[0]), he.as_array(lr1[1]))
roc_lr2 = roc(he.as_array(lr2[0]), he.as_array(lr2[1]))
roc_lr3 = roc(he.as_array(lr3[0]), he.as_array(lr3[1]))
roc_lr4 = roc(he.as_array(lr4[0]), he.as_array(lr4[1]))

fig = plt.figure(figsize=(8,8))
ax = plt.axes()
plt.plot(roc_lr1[:, 0], roc_lr1[:, 1], label="default")
plt.plot(roc_lr2[:, 0], roc_lr2[:, 1], label="default (2)")
plt.plot(roc_lr3[:, 0], roc_lr3[:, 1], label="W cq")
plt.plot(roc_lr4[:, 0], roc_lr4[:, 1], label="cc radiation")
plt.legend()
# he.barhist(h_sig_cum, color="red", lw=2)
# he.barhist(h_bg_cum, color="blue", lw=2)

print roc_lr1
print roc_lr2
print roc_lr3
plt.savefig("proj.png")
