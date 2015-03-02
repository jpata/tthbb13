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
from draw_control_plots import *

if __name__ == "__main__":

	tf = ROOT.TFile(sys.argv[1])

	for (s1, s2) in [
		#("tthbb_8TeV_noME", "tthbb_8TeV_noME"),
		("tthbb_8TeV_noME", "tthbb_13TeV_spring14__s1_3a4602f__s2_b7e13a1"),
		("tthbb_8TeV_noME", "tthbb_13TeV_spring14__s1_eb733a1__s2_3f71e05"),
		("tthbb_8TeV_noME", "tthbb_13TeV_phys14"),
		("tthbb_13TeV_spring14__s1_eb733a1__s2_3f71e05", "tthbb_13TeV_spring14__s1_3a4602f__s2_b7e13a1"),
		("ttjets_8TeV_noME", "ttjets_13TeV_spring14__s1_3a4602f__s2_b7e13a1"),
		("ttjets_8TeV_noME", "ttjets_13TeV_spring14__s1_eb733a1__s2_3f71e05"),
		("ttjets_8TeV_noME", "ttjets_13TeV_phys14"),
		("ttjets_13TeV_spring14__s1_eb733a1__s2_3f71e05", "ttjets_13TeV_spring14__s1_3a4602f__s2_b7e13a1"),
		]:
		yt = yield_plot(tf, s1, s2, sample_weight(s1), sample_weight(s2))

		fig = plt.figure(figsize=(8,8))
		ax = plt.axes()

		xs = np.linspace(1, 12, 12)
		ys1 = ([yt["sl", "H", i][0] for i in range(3)] + [yt["dl", "H", i][0] for i in range(3,6)] +
		    [yt["sl", "L", i][0] for i in range(3)] + [yt["dl", "L", i][0] for i in range(3,6)])
		ys1e = ([yt["sl", "H", i][2] for i in range(3)] + [yt["dl", "H", i][2] for i in range(3,6)] +
		    [yt["sl", "L", i][2] for i in range(3)] + [yt["dl", "L", i][2] for i in range(3,6)])

		ys2 = ([yt["sl", "H", i][1] for i in range(3)] + [yt["dl", "H", i][1] for i in range(3,6)] +
		    [yt["sl", "L", i][1] for i in range(3)] + [yt["dl", "L", i][1] for i in range(3,6)])
		ys2e = ([yt["sl", "H", i][3] for i in range(3)] + [yt["dl", "H", i][3] for i in range(3,6)] +
		    [yt["sl", "L", i][3] for i in range(3)] + [yt["dl", "L", i][3] for i in range(3,6)])

		plt.bar(xs+0.1, ys1, 0.3, yerr=ys1e, color="red", ecolor="black", label=sample_name(s1))
		plt.bar(xs+0.1+0.3+0.1, ys2, 0.3, yerr=ys2e, color="green", ecolor="black", label=sample_name(s2))

		leg = plt.legend(loc=0, frameon=True, fancybox=True, framealpha=0.9)
		#statsbox(ax, [h1, h2, h3, h4])

		xlabs = [
			"cat 1 H", "cat 2 H", "cat 3 H", "DL $\\mu\\mu$ H", "DL $e\\mu$ H", "DL $ee$ H",
			"cat 1 L", "cat 2 L", "cat 3 L", "DL $\\mu\\mu$ L", "DL $e\\mu$ L", "DL $ee$ L"
		]
		plt.xticks(xs + 0.5 - 0.05, xlabs, rotation=90)
		plt.grid()
		plt.xlim(1, 13)
		plt.axvline(7-0.05)
		#ax.set_xticks(xs)

		plt.ylabel("expected yield / 20 $fb^{-1}$ at $\\sqrt{s} = 13 TeV$")
		plt.savefig(s1 + "_" + s2 + "_yields.png", bbox_inches="tight", pad_inches=2.0)
		plt.close()

		print s1, s2
		for (x, y1, e1, y2, e2) in zip(xlabs, ys1, ys1e, ys2, ys2e):
			print "| {4} | {0} | {1} | {2} | {3} |".format(
				round(y1,2), round(e1,2), round(y2,2), round(e2, 2), x
			)
		#plt.bar([2], [b], 1, color="green")
