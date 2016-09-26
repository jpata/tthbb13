import ROOT

#select only high jet-multiplicity events
#sel = [
#    ("sl_highjet", "is_sl== 1 && (((numJets==4 || numJets==5) && nBCSVM >= 3) || (numJets>=6 && nBCSVM>=2))"),
#    ("dl_highjet", "is_dl== 1 && (numJets>=3 && nBCSVM>=2)")
#]

#ttH classification by decay channel
tth_sel = [
    ("hbb", "nGenBHiggs>=2"),
    ("hX", "nGenBHiggs<2"),
]

#ttbar heavy-light classification
presel = "is_sl && numJets>=6"
ttjets_sel = [
    ("ttb", "ttCls == 51 && " + presel),
    ("tt2b", "ttCls == 52 && " + presel),
    ("ttbb", "(ttCls == 53 || ttCls == 54 || ttCls == 55 || ttCls==56) && " + presel),

    ("ttcc", "(ttCls == 41 || ttCls == 42 || ttCls == 43 || ttCls == 44 || ttCls == 45) && " + presel),
    ("ttll", "(ttCls == 0 || ttCls<0) && " + presel)
]


#list of filename -> selection that you want to project
inf = [
    ("/Volumes/Samsung_T3/tth_data/Jul6_leptonic_nome_v1/Jul6_leptonic_nome_v1__TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root", ttjets_sel),
]

def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def SelectTree(infile, outfile, treename, cut, firstEntry=0, numEntries=-1):
    tf = ROOT.TFile(infile)
    otf = ROOT.TFile(outfile, "RECREATE")
    otf.cd()
    if numEntries < 0:
        numEntries = tf.Get(treename).GetEntries()
    print cut, numEntries, firstEntry
    t2 = tf.Get(treename).CopyTree(cut, "", numEntries, firstEntry)
    if not t2:
        raise Exception("could not project tree with cut {0}".format(cut))
    t2.Write()
    ni = t2.GetEntries()
    otf.Close()
    tf.Close()

def SelectTree_par(args):
    return SelectTree(*args)

import multiprocessing, os
#from TTH.TTHNtupleAnalyzer.ParHadd import hadd 
def hadd(args):
    os.system("hadd {0} {1}".format(args[0], " ".join(args[1:])))
#pool = multiprocessing.Pool(1)

for infile, cuts in inf:
    tf = ROOT.TFile(infile)
    Ntree = tf.Get("tree").GetEntries()
    chunksize = 500000 
    for cn, cut in cuts:
        outfile = infile.replace(".root", "_{0}.root".format(cn))
        
        arglist = []
        ichunk = 0
        filenames = []
        for ch in chunks(range(Ntree), chunksize):
            _ofn = outfile + "." + str(ichunk)
            filenames += [_ofn] 
            arglist += [(infile, _ofn, "tree", cut, ch[0], len(ch))] 
            ichunk += 1 
        print "mapping", infile, cn
        map(SelectTree_par, arglist)
        print "Merging to", outfile
        hadd((outfile, filenames))
        for fn in filenames:
            os.remove(fn)
