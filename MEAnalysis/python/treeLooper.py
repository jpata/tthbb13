import ROOT, sys, re, os
import numpy

evids = {}
for fn in sys.argv[1:]:
    tf = ROOT.TFile.Open(fn)

    tt = tf.Get("tree")

    event = numpy.zeros(4, dtype=numpy.int32)
    tt.SetBranchAddress("EVENT", event)

    tt.SetBranchStatus("*", False)
    tt.SetBranchStatus("EVENT*", True)


    for ev in range(tt.GetEntries()):
        tt.GetEntry(ev)
        r, l, e = event[0], event[1], event[2]
        print "EV", r, l, e
        if not evids.has_key((r,l,e)):
            evids[(r,l,e)] = 0
        evids[(r,l,e)] += 1
    tf.Close()

for (k, v) in evids.items():
    if v != 1:
        print k, v
