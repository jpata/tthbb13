import json, copy, os, multiprocessing, sys
import sparse, ROOT

#Nota bene: this is very important!
#need to store histograms in memory, not on disk
ROOT.TH1.AddDirectory(False)

def make_rule_cut(basehist, category):
    """
    Given a THnSparse base histogram and a list of cuts, makes the rules to
    project out the given variables into a TH1D histogram. The rules are a list
    of dictionary objects with
    {
        'input': 'ttH_hbb/sl/sparse' #the source sparse histogram
        'cuts': [('numJets', 6, 8), ('nBCSVM', 4, 6)] #the list of cuts to apply
        'project': [('mem_SL_0w2h2t', 4)] #the variables to project out
        'output': 'ttH_hbb/sl_jge6_tge4/mem_SL_0w2h2t' #the output histogram
    }
    which can be used to produce a set of histograms. Each rule should be
    independent of the other rules.

    basehist (string): name of the sparse histogram in the input file, e.g.
        "sl/sparse". Systematic variations are added automatically to this base name.
    category (Category): the category for which to make the cuts

    Returns: a list of rules to apply using apply_rule.
    """
    rules = []
    for samp in category.samples:
        d = {
            "input": "{0}/{1}".format(samp.input_name, basehist),
            "cuts": str(category.cuts),
            "project": str([(category.discriminator, category.rebin)]),
            "output": "{0}/{1}/{2}".format(samp.output_name, category.name, category.discriminator),
        }
        rules += [d]

        #make systematic variations
        for syst in category.shape_uncertainties.keys():
            for direction in ["Up", "Down"]:
                d2 = copy.deepcopy(d)
                d2["input"] += "_" + syst + direction
                d2["output"] += "_" + syst + direction
                rules += [d2]

    # #Now we need to apply additional cuts on data samples based on the lepton
    # #flavour
    # for samp in data_samples:
    #     if "sl/" in basehist:
    #         if samp == "SingleMuon":
    #             cuts = [("leptonFlavour", 1, 2)] + cuts
    #         elif samp == "SingleElectron":
    #             cuts = [("leptonFlavour", 2, 3)] + cuts
    #         else:
    #             continue
    #     elif "dl/" in basehist:
    #         if samp == "DoubleMuon":
    #             cuts = [("leptonFlavour", 3, 4)] + cuts
    #         elif samp == "MuonEG":
    #             cuts = [("leptonFlavour", 4, 5)] + cuts
    #         elif samp == "DoubleEG":
    #             cuts = [("leptonFlavour", 5, 6)] + cuts
    #         else:
    #             continue
    #     d = {
    #         "input": "{0}/{1}".format(samp, basehist),
    #         "cuts": str(cuts),
    #         "project": str(variables),
    #         "output": "data/{1}/{2}".format(samp, catname, histname),
    #     }
    # 
    #     rules += [d]
    return rules

def apply_rules(args):
    """
    The worker function for the histogram projection rules.
    args (tuple): (input filename, list of rules) to apply

    Returns: a dictionary with the output histograms
    """

    infile, rules = args
    infile_tf = ROOT.TFile.Open(infile)
    hdict = {}
    for rule in rules:
        cuts = eval(rule["cuts"])
        hk = rule["output"]
        h = infile_tf.Get(str(rule["input"]))
        dummy = False

        #in case no histogram could be found, use a dummy histogram so that we
        #have at least the correct binning
        if h == None:
            h = infile_tf.Get(str("ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb/sl/sparse"))
            if not h:
                raise Exception("Could not get histogram")
            dummy = True
            cuts = []
        variables = eval(rule["project"])
        vnames = [v[0] for v in variables]
        ret = sparse.apply_cuts_project(h, cuts, vnames)

        #dummy histogram needs to be made empty
        if dummy:
            ret.Scale(0)
            ret.SetEntries(0)
        ret.SetName(rule["output"].split("/")[-1])
        if len(variables) == 1:
            ret.Rebin(variables[0][1])
        elif len(variables) == 2:
            ret.Rebin2D(variables[0][1], variables[0][2])
        if hdict.has_key(hk):
            hdict[hk] += ret
        else:
            hdict[hk] = ret
    infile_tf.Close()
    return hdict

def apply_rules_parallel(infile, rules, ncores=4):
    p = multiprocessing.Pool(ncores)
    inputs = [
        (infile, [r]) for r in rules
    ]
    rets = p.map(apply_rules, inputs)
    ret = reduce(sparse.add_hdict, rets)
    p.close()
    return ret


if __name__ == "__main__":
    
    #path to sparse.root from MELooper
    infile = sys.argv[1]

    #use the pre-defined analysis specification
    if len(sys.argv)==2:
        import AnalysisSpecification as anspec
    #load from file
    elif len(sys.argv)==3:
        import imp
        anspec = imp.load_source("anspec", sys.argv[2])
    analysis = anspec.analysis

    rules = []
    for cat in analysis.categories:
        rules += make_rule_cut(cat.src_histogram, cat)
    
    #project out all the histograms
    hdict = apply_rules_parallel(infile, rules)

    #split the big dictionary to category-based dictionaries
    hdict_cat = {}
    for k in hdict.keys():
        catname = k.split("/")[1]
        if not hdict_cat.has_key(catname):
            hdict_cat[catname] = {}
        hdict_cat[catname][k] = hdict[k]
    
    #catname -> file name
    category_files = {}

    #save the histograms into per-category files
    for catname in hdict_cat.keys():
        hfile = os.path.join(analysis.output_directory, "{0}.root".format(catname))
        category_files[catname] = hfile
        sparse.save_hdict(hfile, hdict_cat[catname])
    
    #add the fake data
    if analysis.do_fake_data:
        from datacardCombiner import fakeData
        for cat in analysis.categories:
            hfile = category_files[cat.name]
            tf = ROOT.TFile(hfile, "UPDATE")
            fakeData(tf, tf, [cat])
            tf.Close()

    #add the stat variations
    if analysis.do_stat_variations:
        from datacardCombiner import makeStatVariations
        for cat in analysis.categories:
            hfile = category_files[cat.name]
            tf = ROOT.TFile(hfile, "UPDATE")
            makeStatVariations(tf, tf, [cat])
            tf.Close()
