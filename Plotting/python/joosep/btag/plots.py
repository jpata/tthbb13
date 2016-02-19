import sys
import os

if "CMSSW" in os.environ["PYTHONPATH"]:
    from TTH.Plotting.joosep.plotlib import *
else:
    sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_15/src/TTH/Plotting/python/joosep/")
    from plotlib import *

import rootpy, glob
import matplotlib.pyplot as plt
import rootpy.plotting.root2matplotlib as rplt

f = rootpy.io.File(sys.argv[1])

for bin in ["Bin0", "Bin1"]:
    hl1 = f.Get("btagCSV_l_{0}__rec".format(bin))
    hc1 = f.Get("btagCSV_c_{0}__rec".format(bin))
    hb1 = f.Get("btagCSV_b_{0}__rec".format(bin))

    hl2 = f.Get("btagBDT_l_{0}__rec".format(bin))
    hc2 = f.Get("btagBDT_c_{0}__rec".format(bin))
    hb2 = f.Get("btagBDT_b_{0}__rec".format(bin))

    for h in [hl1, hc1, hb1, hl2, hc2, hb2]:
        h.Rebin(10)
        h.Scale(1.0 / h.Integral())
    plt.figure(figsize=(6,6))
    hl1.color = "green"
    hc1.color = "blue"
    hb1.color = "red"
    rplt.errorbar(hl1, label="udsg")
    rplt.errorbar(hc1, label="c")
    rplt.errorbar(hb1, label="b")
    plt.yscale("log")
    plt.legend(loc="best", numpoints=1, frameon=False)
    plt.grid()
    plt.ylim(0.001,1.0)
    plt.xlabel("CSV b-discriminator")
    plt.ylabel("fraction of jets")
    svfg("plots/btagCSV_{0}.pdf".format(bin))

    plt.figure(figsize=(6,6))
    hl2.color = "green"
    hc2.color = "blue"
    hb2.color = "red"
    rplt.errorbar(hl2, color="green")
    rplt.errorbar(hc2, color="blue")
    rplt.errorbar(hb2, color="red")
    plt.yscale("log")
    plt.legend(loc="best", numpoints=1, frameon=False)
    plt.grid()
    plt.ylim(0.001,1.0)
    plt.xlabel("cMVAv2 b-discriminator")
    plt.ylabel("fraction of jets")
    svfg("plots/btagBDT_{0}.pdf".format(bin))

    r1, re1 = calc_roc(hb1, hl1)
    r2, re2 = calc_roc(hb2, hl2)

    rc1, rce1 = calc_roc(hb1, hc1)
    rc2, rce2 = calc_roc(hb2, hc2)

    plt.figure(figsize=(6,6))
    plt.plot(r1[:, 0], r1[:, 1], label="CSV udsg", color="black", lw=2)
    plt.plot(r2[:, 0], r2[:, 1], label="cMVAv2 udsg", color="red", lw=2)

    plt.plot(rc1[:, 0], rc1[:, 1], label="CSV c", color="black", ls="--", lw=2)
    plt.plot(rc2[:, 0], rc2[:, 1], label="cMVAv2 c", color="red", ls="--", lw=2)

    plt.legend(loc="best")
    plt.yscale("log")
    plt.grid()
    plt.xlabel("b efficiency")
    plt.ylabel("udgsg (c) efficiency")
    plt.text(0.42, 0.011, "c", fontsize=24)
    plt.text(0.42, 0.0004, "udsg", fontsize=24)
    plt.xlim(0.3,1.0)
    plt.ylim(0.0001,1.0)
    plt.axhline(0.1)
    plt.axhline(0.01)
    svfg("plots/btag_{0}.pdf".format(bin))
