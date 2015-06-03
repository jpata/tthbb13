#!/usr/bin/env python
from collections import OrderedDict
import ROOT
ROOT.gROOT.SetBatch(True)
from tabulate import tabulate
import sys, os

tf = ROOT.TFile(sys.argv[1])

from weighting import get_weight

def get_sample_yields(sn, cuts):
    ret = OrderedDict()
    errd = OrderedDict()
    for c in cuts:
        h = tf.Get(sn + "/" + c)
        if not h:
            errd[c] = 0
            ret[c] = 0
        else:
            err = ROOT.Double(0)
            ret[c] = h.IntegralAndError(0, h.GetNbinsX()+1, err)
            errd[c] = err
    return ret, errd

samples = [
    ("tth", "tth_13TeV_phys14"),
    ("ttbb", "ttjets_13TeV_phys14_bb"),
    ("ttb", "ttjets_13TeV_phys14_b"),
    ("ttcc", "ttjets_13TeV_phys14_cc"),
    ("ttll", "ttjets_13TeV_phys14_ll"),
]

#tab = []
#for sn, s in samples:
#    r, e = get_sample_yields(s, [
#        "sl/cat1L/jet0_pt",
#        "sl/cat2L/jet0_pt",
#        "sl/cat3L/jet0_pt",
#        "dl/cat6Lee/jet0_pt",
#        "dl/cat6Lem/jet0_pt",
#        "dl/cat6Lmm/jet0_pt",
#        ]
#    )
#    w = get_weight(s)
#    row = [sn] + ["{0:.2f} +- {1:.2f}".format(w*_r, w*_e)
#        for _r, _e in zip(r.values(), e.values())
#    ]
#    tab += [row]
#print tabulate(tab, ["sample", "cat1L", "cat2L", "cat3L", "cat6Lee", "cat6Lem", "cat6Lmm"], tablefmt="grid")

tab = []
for sn, s in samples:
    r, e = get_sample_yields(s, [
        "sl/cat1H/jet0_pt",
        "sl/cat2H/jet0_pt",
        "sl/cat3H/jet0_pt",
        "dl/cat6Hee/jet0_pt",
        "dl/cat6Hem/jet0_pt",
        "dl/cat6Hmm/jet0_pt",
        ]
    )
    w = get_weight(s)
    row = [sn] + ["{0:.1f} +- {1:.1f}".format(w*_r, w*_e)
        for _r, _e in zip(r.values(), e.values())
    ]
    tab += [row]
print tabulate(tab, ["sample", "cat1H", "cat2H", "cat3H", "cat6Hee", "cat6Hem", "cat6Hmm"], tablefmt="grid")

tab = []
for sn, s in samples:
    r, e = get_sample_yields(s, [
        "sl/lep0_pt",
        "sl/5j3t/jet0_pt", "sl/5j4t/jet0_pt",
        "sl/6j3t/jet0_pt", "sl/6j4t/jet0_pt", "sl/6jH/jet0_pt",
        "sl/7j3t/jet0_pt", "sl/7j4t/jet0_pt", "sl/7jH/jet0_pt"
        ]
    )
    w = get_weight(s)
    row = [sn] + ["{0:.1f} +- {1:.1f}".format(w*_r, w*_e)
        for _r, _e in zip(r.values(), e.values())
    ]
    tab += [row]
print tabulate(tab, ["sample", "sl", "5j3t", "5j4t", "6j3t", "6j4t", "6jH", "7j3t", "7j4t", "7jH"], tablefmt="grid")

tab = []
for sn, s in samples:
    r, e = get_sample_yields(s, [
        "dl/lep0_pt",
        "dl/5j3t/jet0_pt", "dl/5j4t/jet0_pt",
        "dl/6j3t/jet0_pt", "dl/6j4t/jet0_pt", "dl/6jH/jet0_pt",
        "dl/7j3t/jet0_pt", "dl/7j4t/jet0_pt", "dl/7jH/jet0_pt"
        ]
    )
    w = get_weight(s)
    row = [sn] + ["{0:.1f} +- {1:.1f}".format(w*_r, w*_e)
        for _r, _e in zip(r.values(), e.values())
    ]
    tab += [row]
print tabulate(tab, ["sample", "dl", "5j3t", "5j4t", "6j3t", "6j4t", "6jH", "7j3t", "7j4t", "7jH"], tablefmt="grid")
#
#tab = []
#for sn, s in samples:
#    r, e = get_sample_yields(s, [
#        "sl/lep0_pt",
#        "sl/5j/jet0_pt", "sl/6j/jet0_pt", "sl/7j/jet0_pt", "sl/8plusj/jet0_pt"
#        ]
#    )
#    w = get_weight(s)
#    row = [sn] + ["{0:.2f} +- {1:.2f}".format(w*_r, w*_e)
#        for _r, _e in zip(r.values(), e.values())
#    ]
#    tab += [row]
#print tabulate(tab, ["sample", "sl", "5j", "6j", "7j", ">7j"], tablefmt="grid")
#
#
#tab = []
#for sn, s in samples:
#    r, e = get_sample_yields(s, [
#        "sl/5j/jet0_pt", "sl/5jL/jet0_pt", "sl/5j3t/jet0_pt", "sl/5j4t/jet0_pt", "sl/5jH/jet0_pt",
#        ]
#    )
#    w = get_weight(s)
#    row = [sn] + ["{0:.2f} +- {1:.2f}".format(w*_r, w*_e)
#        for _r, _e in zip(r.values(), e.values())
#    ]
#    tab += [row]
#print tabulate(tab, ["sample", "5j", "5j <3t", "5j 3t", "5j 4t", "5j >4t"], tablefmt="grid")
#
#
#tab = []
#for sn, s in samples:
#    r, e = get_sample_yields(s, [
#        "sl/6j/jet0_pt", "sl/6jL/jet0_pt", "sl/6j3t/jet0_pt", "sl/6j4t/jet0_pt", "sl/6jH/jet0_pt",
#        ]
#    )
#    w = get_weight(s)
#    row = [sn] + ["{0:.2f} +- {1:.2f}".format(w*_r, w*_e)
#        for _r, _e in zip(r.values(), e.values())
#    ]
#    tab += [row]
#print tabulate(tab, ["sample", "6j", "6j <3t", "6j 3t", "6j 4t", "6j >4t"], tablefmt="grid")
#
#tab = []
#for sn, s in samples:
#    r, e = get_sample_yields(s, [
#        "sl/7j/jet0_pt", "sl/7jL/jet0_pt", "sl/7j3t/jet0_pt", "sl/7j4t/jet0_pt", "sl/7jH/jet0_pt",
#        ]
#    )
#    w = get_weight(s)
#    row = [sn] + ["{0:.2f} +- {1:.2f}".format(w*_r, w*_e)
#        for _r, _e in zip(r.values(), e.values())
#    ]
#    tab += [row]
#print tabulate(tab, ["sample", "7j", "7j <3t", "7j 3t", "7j 4t", "7j >4t"], tablefmt="grid")
#
#tab = []
#for sn, s in samples:
#    r, e = get_sample_yields(s, [
#        "sl/8plusj/jet0_pt", "sl/8plusjL/jet0_pt", "sl/8plusj3t/jet0_pt", "sl/8plusj4t/jet0_pt", "sl/8plusjH/jet0_pt",
#        ]
#    )
#    w = get_weight(s)
#    row = [sn] + ["{0:.2f} +- {1:.2f}".format(w*_r, w*_e)
#        for _r, _e in zip(r.values(), e.values())
#    ]
#    tab += [row]
#print tabulate(tab, ["sample", ">7j", ">7j <3t", ">7j 3t", ">7j 4t", ">7j >4t"], tablefmt="grid")
#
#
#
#
#tab = []
#for sn, s in samples:
#    r, e = get_sample_yields(s, [
#        "dl/lep0_pt",
#        "dl/5j/jet0_pt", "dl/6j/jet0_pt", "dl/7j/jet0_pt", "dl/8plusj/jet0_pt",
#        ]
#    )
#    w = get_weight(s)
#    row = [sn] + ["{0:.2f} +- {1:.2f}".format(w*_r, w*_e)
#        for _r, _e in zip(r.values(), e.values())
#    ]
#    tab += [row]
#print tabulate(tab, ["sample", "dl", "5j", "6j", "7j", ">7j"], tablefmt="grid")
