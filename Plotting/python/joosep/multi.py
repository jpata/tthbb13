import ROOT, multiprocessing
ROOT.gROOT.SetBatch(True)
from rootpy import asrootpy

def process_one(args):    
    import ROOT, multiprocessing
    ROOT.gROOT.SetBatch(True)
    from rootpy import asrootpy

    fn, tree, hist, formula, cut, skipev, n = args
    print "processing ", skipev, n
    tf = ROOT.TFile(fn)
    tt = tf.Get(tree)
    ROOT.gROOT.cd()
    nproc = tt.Draw(
        formula + " >> " + hist,
        cut,
        "GOFF",
        n,
        skipev
    )
    hname = hist.split("(")[0]
    
    
    h = asrootpy(ROOT.gROOT.Get(hname).Clone(hname))
    tf.Close()
    return h

def make_arglist(fn, tree, hist, formula, cut, N=1000000):
    tf = ROOT.TFile(fn)
    assert(tf != None)
    tt = tf.Get(tree)
    assert(tt != None)
    Nentries = tt.GetEntries()
    args = []
    for skip in range(0, Nentries, N):
        args += [(fn, tree, hist, formula, cut, skip, N)]
    return args

def add_hists(hl):
	first = hl[0].Clone("tot")
	for r in hl[1:]:
		first.Add(r)
	return first

def multi_draw(fn, tree, hist, formula, cut, Ncores=10):
	p = multiprocessing.Pool(Ncores)
	res = p.map(process_one, make_arglist(fn, tree, hist, formula, cut))
	return add_hists(res)

if __name__ == "__main__":
	A = "/Users/joosep/Documents/tth/data/ttjets.root", "tree", "h(100, 0, 1)", "btag_lr_l_bbbb", "btag_lr_l_bbbb > 0"
	args = make_arglist(*A)

	tot = add_hists(map(process_one, args))
	print tot.Integral(), tot.GetMean(), tot.GetRMS()
	tot2 = multi_draw(*A)
	print tot2.Integral(), tot2.GetMean(), tot2.GetRMS()
