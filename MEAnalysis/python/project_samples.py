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


#list of filename -> selection that you want to project
inf = [
#    ("/scratch/joosep/ttHTobb_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root", sel),
#    ("/scratch/joosep/TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9.root", sel)
    #("/dev/shm/joosep/cfg_noME/TT_TuneCUETP8M1_13TeV-powheg-pythia8.root", ttjets_sel),
    #("/dev/shm/joosep/cfg_noME_jetPt20/TT_TuneCUETP8M1_13TeV-powheg-pythia8.root", ttjets_sel),
    ("/dev/shm/joosep/cfg_noME_btagBDT/TT_TuneCUETP8M1_13TeV-powheg-pythia8.root", ttjets_sel),
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
from TTH.TTHNtupleAnalyzer.ParHadd import hadd 
pool = multiprocessing.Pool(40)

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
        pool.map(SelectTree_par, arglist)
        print "Merging to", outfile
        hadd((outfile, filenames))
        for fn in filenames:
            os.remove(fn)
