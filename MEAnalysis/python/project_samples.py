import ROOT

inf = [
    ("/scratch/joosep/ttjets_13tev_madgraph_pu20bx25_phys14.root",
    [
        ("ttbb", "nMatchSimB>=2"),
        ("ttb", "nMatchSimB==1"),
        ("ttcc", "nMatchSimB==0 && nMatchSimC>=2"),
        ("ttll", "nMatchSimB==0 && nMatchSimC<=1")
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
        t2.Write()
        ni = t2.GetEntries()
        print cn, ni
        Nt += ni
        otf.Close()
    print Nt

