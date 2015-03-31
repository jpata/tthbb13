import ROOT, multiprocessing, rootpy
ROOT.TH1.SetDefaultSumw2(True)
from copy import deepcopy, copy

samples = ["tth.root", "ttjets.root"]
sample_sizes = {"tth.root":10000, "ttjets.root":10000}

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
        
def project_hist(tree,
    selection,
    func, binning,
    histname,
    first_entry=None, n_entries=None
    ):

    tf = ROOT.TFile(tree[0])
    tt = tf.Get(tree[1])
    if n_entries is None:
        n_entries = tt.GetEntries()
    if first_entry is None:
        first_entry = 0

    nbins, low, high = binning
    
    ROOT.gROOT.cd()
    n = tt.Draw("{func} >> {hist}({nbins}, {low}, {high})".format(
        func=func, hist=histname, nbins=nbins, low=low, high=high
    ), selection, "goff", n_entries, first_entry
    )
    assert n >= 0, (histname, func, sel)
    h = ROOT.gROOT.Get(histname).Clone(histname)
    h.SetDirectory(ROOT.gROOT)
    assert(h != None)
    assert(h is not None)
    tf.Close()
    return h

def project_hist_kwargs(kwargs):
    tree = kwargs["tree"]
    selection = kwargs["selection"]
    func = kwargs["func"]
    binning = kwargs["binning"]
    histname = kwargs["histname"]
    first_entry = kwargs["first_entry"]
    n_entries = kwargs["n_entries"]
    return project_hist(
        tree,
        selection,
        func,
        binning,
        histname,
        first_entry,
        n_entries
    )
    
def project_hist_kwargs_multi(fn, chunksize, kwargs):
    
    
    args = deepcopy(kwargs)
    args["tree"] = (fn, "tree")

    arglist = []
    
    tf = ROOT.TFile(fn)
    tt = tf.Get("tree")
    
    chs = chunks(range(tt.GetEntries()), chunksize)
    tf.Close()
    
    for ch in chs:
        d = deepcopy(args)
        d["tree"] = (fn, "tree")
        d["first_entry"] = ch[0]
        d["n_entries"] = ch[-1] - ch[0] + 1
        arglist.append(d)

    pool = multiprocessing.Pool(4)
    hs = map(rootpy.asrootpy, pool.map(project_hist_kwargs, arglist))
    pool.close()
    pool.join()
    pool.terminate()
    ROOT.gROOT.cd()
    h = sum(hs).Clone(kwargs["histname"])
    #h.SetDirectory(ROOT.gROOT)
    return h

if __name__ == "__main__":
    outhists = {}
    
    for sample in samples:
        sample_name = sample.split(".")[0]    
    
        for selname, sel in [
            ("sl", "is_sl==1"), ("dl", "is_dl==1"),
            ("sl_6j_4t", "is_sl==1 && njets>=6 && nBCSVM>=4"),
            ("dl_5j_4t", "is_dl==1 && njets>=5 && nBCSVM>=4"),
            ("cat1", "cat==1"),
            ("cat2", "cat==2"),
            ("cat3", "cat==3"),
            ("cat6", "cat==6"),
        ]:
            print selname, sample
            if sample_name == "tth":
                sel += " && nGenBHiggs==2 "
            
            _id = selname + "_" + sample_name
            outhists["njets_"+_id ] = project_hist_kwargs_multi(
                sample,
                sample_sizes[sample],
                {
                    "selection": sel,
                    "func": "njets",
                    "binning": (10,4,14),
                    "histname": "njets_"+_id,
                }
            )
            
            outhists["ntags_csvm_"+_id] = project_hist_kwargs_multi(
                sample,
                sample_sizes[sample],
                {
                    "selection": sel,
                    "func": "nBCSVM",
                    "binning": (10, 0, 10),
                    "histname": "ntags_csvm_"+_id,
                }
            )
            
            for ilep in [0,1]:
                outhists["leps_pt{0}_".format(ilep)+_id] = project_hist_kwargs_multi(
                    sample,
                    sample_sizes[sample],
                    {
                        "selection": sel,
                        "func": "leps_pt[{0}]".format(ilep),
                        "binning": (60, 0, 400),
                        "histname": "leps_pt{0}_".format(ilep) + _id,
                    }
                )
                
                outhists["leps_eta{0}_".format(ilep)+_id] = project_hist_kwargs_multi(
                    sample,
                    sample_sizes[sample],
                    {
                        "selection": sel,
                        "func": "leps_eta[{0}]".format(ilep),
                        "binning": (60, 4.5, 4.5),
                        "histname": "leps_eta{0}_".format(ilep) + _id,
                    }
                )
            
            for ijet in [0,1,2]:
                outhists["jets_pt{0}_".format(ijet)+_id] = project_hist_kwargs_multi(
                    sample,
                    sample_sizes[sample],
                    {
                        "selection": sel,
                        "func": "jets_pt[{0}]".format(ijet),
                        "binning": (60, 0, 400),
                        "histname": "jets_pt{0}_".format(ijet)+_id,
                    }
                )
    
                
                outhists["jets_eta{0}_".format(ijet)+_id] = project_hist_kwargs_multi(
                    sample,
                    sample_sizes[sample],
                    {
                        "selection": sel,
                        "func": "jets_eta[{0}]".format(ijet),
                        "binning": (60,4.5, 4.5),
                        "histname": "jets_eta{0}_".format(ijet)+_id,
                    }
                )
            
            flcuts = [("", "(1)")]
            
            if sample_name == "ttjets":
                flcuts += [
                    ("bb", "nMatchSimB>=2"), ("bx", "nMatchSimB==1"),
                    ("cc", "nMatchSimB==0 && nMatchSimC>=2"),
                    ("ll", "nMatchSimB==0 && nMatchSimC<=1"),
                ]
            for (fl, flcut) in flcuts:
                _subid = _id + "_" + fl
                _sel = sel + " && " + flcut
                outhists["btag_lr_4b_2b_" + _subid] = project_hist_kwargs_multi(
                    sample,
                    sample_sizes[sample],
                    {
                        "selection": _sel,
                        "func": "btag_LR_4b_2b",
                        "binning": (60, 0, 1),
                        "histname": "btag_lr_4b_2b_" + _subid,
                    }
                )
            
            outhists["wmass_" + _id] = project_hist_kwargs_multi(
                sample,
                sample_sizes[sample],
                {
                    "selection": sel,
                    "func": "Wmass",
                    "binning": (60, 40, 200),
                    "histname": "wmass_" + _id,
                }
            )
            
    for sample in samples:
        sample_name = sample.split(".")[0]
        
        for selname, sel in [
            ("cat1H", "cat==1 && nmem_tth>0"),
            ("cat2H", "cat==2 && nmem_tth>0"),
            ("cat3H", "cat==3 && nmem_tth>0"),
            ("cat6H", "cat==6 && nmem_tth>0"),
            
            ("cat1H_matched", "cat==1 && nmem_tth>0"),
            ("cat2H_matched", "cat==2 && nmem_tth>0"),
            ("cat3H_matched", "cat==3 && nmem_tth>0"),
            ("cat6H_matched", "cat==6 && nmem_tth>0"),
        ]:
            print selname, sample
            
            if sample_name == "tth":
                sel += " && nGenBHiggs==2 "
                
            _id = selname + "_" + sample_name
            
            if "matched" in selname:
                if sample_name == "tth":
                    nh  = 2
                else:
                    nh = 0
                    
                if "cat1" in selname:
                    nw = 2
                if "cat2" in selname or "cat3" in selname:
                    nw = 1
                if "cat6" in selname:
                    nw = 0
                
                nt = 2
                sel += " && nMatch_wq_btag=={0} && nMatch_hb_btag=={1} && nMatch_tb_btag=={2}".format(
                    nw, nh, nt
                )
            
            flcuts = [("", "(1)")]
            
            if sample_name == "ttjets":
                flcuts += [
                    ("bb", "nMatchSimB>=2"), ("bx", "nMatchSimB==1"),
                    ("cc", "nMatchSimB==0 && nMatchSimC>=2"),
                    ("ll", "nMatchSimB==0 && nMatchSimC<=1"),
                ]
            for (fl, flcut) in flcuts:
                _subid = _id + "_" + fl
                _sel = sel + " && " + flcut
                outhists["mem_p_" + _subid] = project_hist_kwargs_multi(
                    sample,
                    sample_sizes[sample],
                    {
                        "selection": _sel,
                        "func": "mem_tth_p[0] / (mem_tth_p[0] + 0.12 * mem_ttbb_p[0])",
                        "binning": (40, 0, 1),
                        "histname": "mem_p_" + _subid,
                    }
                )
            
            outhists["mem_tth_time_" + _id] = project_hist_kwargs_multi(
                sample,
                sample_sizes[sample],
                {
                    "selection": sel,
                    "func": "mem_tth_time[0] / 1000",
                    "binning": (100, 0, 2000),
                    "histname": "mem_tth_time_" + _id,
                }
            )
            
            outhists["mem_ttbb_time_" + _id] = project_hist_kwargs_multi(
                sample,
                sample_sizes[sample],
                {
                    "selection": sel,
                    "func": "mem_ttbb_time[0] / 1000",
                    "binning": (100, 0, 2000),
                    "histname": "mem_ttbb_time_" + _id,
                }
            )
            
    of = ROOT.TFile("controlPlotsMEM.root", "RECREATE")
    for ohn, oh in sorted(outhists.items(), key=lambda x: x[0]):
        oh.SetDirectory(of)
    of.Write("", ROOT.TObject.kOverwrite)
    of.Close()
