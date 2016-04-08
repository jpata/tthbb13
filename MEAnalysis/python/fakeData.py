import ROOT, sys

inf = sys.argv[1]
tf = ROOT.TFile(inf)
processes = [
    "ttbarPlus2B",
    "ttbarPlusB",
    "ttbarPlusBBbar",
    "ttbarPlusCCbar",
    "ttbarOther",
]

channels = [
    "sl_j4_t3_blrH",
    "sl_j4_t3_blrL",
    "sl_j5_t3_blrH",
    "sl_j5_t3_blrL",
    "sl_jge6_t3_blrH",
    "sl_jge6_t3_blrL",
    "sl_jge6_tge4_blrH",
    "sl_jge6_tge4_blrL"
]
hist = "mem_SL_0w2h2t"


of = ROOT.TFile("fakeData.root", "RECREATE")

for ch in channels:
    h = None
    for proc in processes:
        h2 = tf.Get("{0}/{1}/{2}".format(proc, ch, hist))
        if not h:
            h = h2.Clone()
        else:
            h.Add(h2)
    outdir = "data_obs/{0}".format(ch)
    of.mkdir(outdir)
    outdir = of.Get(outdir)
    h.SetDirectory(outdir)
    outdir.Write()
#of.Write()
of.Close()
