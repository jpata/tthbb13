import ROOT

tth_sel = [
    ("hbb", "nGenBHiggs>=2"),
    ("hX", "nGenBHiggs<2"),
]

ttjets_sel = [
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
    ("ttll", "ttCls == 0 || ttCls<0")
]

inf = [
#    ("/home/joosep/tth/gc/GC3c2c5704ee07/MEAnalysis_cfg_heppy/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8.root", tth_sel),
#    ("/home/joosep/tth/gc/GC3c2c5704ee07/MEAnalysis_cfg_heppy/ttHTobb_M125_13TeV_powheg_pythia8.root", tth_sel),
#    ("/home/joosep/tth/gc/GCaeca6a813136/MEAnalysis_cfg_heppy/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root", ttjets_sel),
    ("/home/joosep/tth/gc/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9.root", ttjets_sel)
]

for f, cuts in inf:
    tf = ROOT.TFile(f)
    N0 = tf.Get("tree").GetEntries()
    Nt = 0
    print N0
    for cn, cut in cuts:
        of = f.replace(".root", "_{0}.root".format(cn))
        print "writing to",of
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
