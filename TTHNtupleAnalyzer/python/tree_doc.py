import ROOT, sys, re
tf = ROOT.TFile(sys.argv[1])
tt = tf.Get("tthNtupleAnalyzer/events")
brs = sorted([b for b in tt.GetListOfBranches()])

#for br in brs:
#    bn = br.GetName()
#    ls = br.GetListOfLeaves()
#    print "| %s | %s | | |" % (bn, ls[0].GetTypeName())

print tt.GetEntries()

for ev in tt:
    print "---"
    print ev.event__id

    #print [ev.jet_toptagger__pt[i] for i in range(ev.n__jet_toptagger)]
    #print [ev.jet_toptagger__n_sj[i] for i in range(ev.n__jet_toptagger)]
    #print [ev.jet_toptagger__child_idx[i] for i in range(ev.n__jet_toptagger)]

    #njets = ev.n__jet
    #for i in range(njets):
    #    print ev.jet__pt[i], ev.gen_jet__pt[i]
    #    print ev.jet__id[i], ev.gen_jet__id[i]
    #print ev.gen_t__w_d1__id, ev.gen_t__w_d2__id, ev.gen_tbar__w_d1__id, ev.gen_tbar__w_d2__id, ev.hypo1
    #if ev.n__sig_lep == 0:
    #    print "HD", ev.n__jet
    #if ev.n__sig_lep == 1:
    #    print "SL", ev.sig_lep__pt[0], ev.lep__pt[ev.sig_lep__idx[0]]
    #if ev.n__sig_lep == 2:
    #    print "DL", ev.sig_lep__pt[0], ev.sig_lep__pt[1], ev.lep__pt[ev.sig_lep__idx[0]], ev.lep__pt[ev.sig_lep__idx[1]]
    #print "b", ev.gen_b__pt, ev.gen_bbar__pt
