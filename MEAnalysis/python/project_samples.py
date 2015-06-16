import ROOT

inf = [
#    ("/scratch/joosep/ttjets_13tev_madgraph_pu20bx25_phys14.root",
#    [
#        ("ttbb", "nMatchSimB>=2"),
#        ("ttb", "nMatchSimB==1"),
#        ("ttcc", "nMatchSimB==0 && nMatchSimC>=2"),
#        ("ttll", "nMatchSimB==0 && nMatchSimC<=1")
#    ])
    ("/home/joosep/tth/gc/GC309d86211ddf/ttjets_13tev_madgraph_pu20bx25_phys14.root",
    [
        ("ttb", "ttCls == 51"),
        ("tt2b", "ttCls == 52"),
        ("ttbb", "ttCls == 53 || ttCls == 54 || ttCls == 55 || ttCls==56"),
        #("ttbb", "ttCls == 53"),
        #("ttb2b", "ttCls == 54"),
        #("tt2b2b", "ttCls == 55"),

        ("ttcc", "(ttCls == 41 || ttCls == 42 || ttCls == 43 || ttCls == 44 || ttCls == 45)"),
        #("ttc", "ttCls == 41"),
        #("tt2c", "ttCls == 42"),
        #("ttcc", "ttCls == 43"),
        #("ttc2c", "ttCls == 44"),
        #("tt2c2c", "ttCls == 45"),
        ("ttll", "ttCls == 0")
    ])
]

for f, cuts in inf:
    tf = ROOT.TFile(f)
    N0 = tf.Get("tree").GetEntries()
    Nt = 0
    print N0
    for cn, cut in cuts:
        of = f.replace(".root", "_{0}.root".format(cn))
        otf = ROOT.TFile(of, "RECREATE")
        otf.cd()
        t2 = tf.Get("tree").CopyTree(cut)
        if not t2:
            raise Exception("could not project tree with cut {0}".format(cut))
        t2.Write()
        ni = t2.GetEntries()
        print cn, ni
        Nt += ni
        otf.Close()
    print Nt

