import json, copy, os, imp, multiprocessing, sys
import sparse, ROOT
import logging
from utils import fakeData

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
            "cuts": str(category.cuts + samp.cuts),
            "project": str([(category.discriminator, category.rebin)]),
            "output": "{0}/{1}/{2}".format(samp.output_name, category.name, category.discriminator),
            "xs_weight": samp.xs_weight
        }
        rules += [d]

        #make systematic variations
        systdict = category.shape_uncertainties[samp.output_name]
        for systname, systsize in systdict.items():
            for direction in ["Up", "Down"]:
                d2 = copy.deepcopy(d)
                d2["input"] += "_" + systname + direction
                d2["output"] += "_" + systname + direction
                rules += [d2]

    for samp in category.data_samples:
        d = {
            "input": "{0}/{1}".format(samp.input_name, basehist),
            "cuts": str(category.cuts + samp.cuts),
            "project": str([(category.discriminator, category.rebin)]),
            "output": "{0}/{1}/{2}".format(samp.output_name, category.name, category.discriminator),
            "xs_weight": 1.0
        }
    
        rules += [d]
    return rules

def apply_rules(args):
    """
    The worker function for the histogram projection rules.
    args (tuple): (input filename, list of rules) to apply

    Returns: a dictionary with the output histograms
    """

    infile, rules = args
    infile_tf = ROOT.TFile.Open(infile)
    if not infile_tf:
        raise FileError("Could not open file: {0}".format(infile))
    hdict = {}

    for rule in rules:
        
        #convert the string of the cut list into the actual list
        cuts = eval(rule["cuts"])
        hk = rule["output"]
        inp = str(rule["input"])
        logging.debug("apply_rules: histogram {0} => {1} with cut {2}".format(inp, hk, cuts))
        h = infile_tf.Get(inp)

        #in case no histogram could be found, use a dummy histogram so that we
        #have at least the correct binning
        dummy = False
        if not h:
            dummy = True
            logging.warning("Could not get histogram {0}, using fallback".format(inp))
            h = infile_tf.Get(str("ttHTobb_M125_13TeV_powheg_pythia8/sl/sparse"))
            if not h:
                raise Exception("Could not get fallback histogram {0}".format("ttHTobb_M125_13TeV_powheg_pythia8/sl/sparse"))
            cuts = []

        variables = eval(rule["project"])
        vnames = [v[0] for v in variables]
        ret = sparse.apply_cuts_project(h, cuts, vnames)

        logging.debug("{2} = {0} {1}".format(ret.GetEntries(), ret.Integral(), hk))

        #dummy histogram needs to be made empty
        if dummy:
            logging.debug("{2} = {0} {1}".format(ret.GetEntries(), ret.Integral(), hk))
            ret.Scale(0)
            ret.SetEntries(0)

        ret.SetName(rule["output"].split("/")[-1])

        #1D rebin
        if len(variables) == 1:
            ret.Rebin(variables[0][1])

        #2D rebin
        elif len(variables) == 2:
            ret.Rebin2D(variables[0][1], variables[0][2])
        ret.Scale(rule["xs_weight"])

        if hdict.has_key(hk):
            hdict[hk] += ret
        else:
            hdict[hk] = ret
    infile_tf.Close()
    return hdict

def apply_rules_parallel(infile, rules, ncores=1):
    """
    Project out all the histograms according to the projection rules.
    infile (string) - path to input root file with sparse histograms
    rules (list of dicts) - all the rules
    
    Optional:
    ncores (int) - number of parallel cores for projection
    """ 
    if ncores > 1:
        p = multiprocessing.Pool(ncores)
    inputs = [
        (infile, [r]) for r in rules
    ]
    if ncores > 1:
        rets = p.map(apply_rules, inputs)
    else:
        rets = map(apply_rules, inputs)

    #add all the histogram dictionaries together
    print "reducing..."
    ret = reduce(sparse.add_hdict, rets)
    
    if ncores > 1:
        p.close()
    return ret


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Process one analysis/category name and write output to current working directory
    if not len(sys.argv)==5:
        print "Invalid number of arguments. Usage:"
        print "{0} sparse.root AnalysisSpecification.py SL_7cat sl_j4_t3".format(sys.argv[0])
        sys.exit()
        
    infile = sys.argv[1] # path to sparse.root from MELooper
    anspec = imp.load_source("anspec", sys.argv[2])
    analysis_to_process = sys.argv[3]
    cat_to_process = sys.argv[4]
        
    # Limit to one analysis/category
    analysis = anspec.analyses[analysis_to_process]
    categories = [c for c in analysis.categories if c.name==cat_to_process]


    # Make all the rules
    rules = []
    for cat in categories:
        print "making rules for analysis={0} category={1} discr={2}".format(
            analysis_to_process, cat.name, cat.discriminator
        )
        rules += make_rule_cut(cat.src_histogram, cat)
    
    of = open("rules.json", "w")
    print "writing {0} rules".format(len(rules))
    of.write(json.dumps(rules, indent=2))
    of.close()

    #project out all the histograms
    print "applying {0} rules".format(len(rules))
    hdict = apply_rules_parallel(infile, rules)

    #split the big dictionary to category-based dictionaries
    hdict_cat = {}
    for k in hdict.keys():
        catname = k.split("/")[1]
        if not hdict_cat.has_key(catname):
            hdict_cat[catname] = {}
        hdict_cat[catname][k] = hdict[k]

    #produce the event counts per category
    print "producing event counts"
    event_counts = {}
    for cat in categories:
        event_counts[cat.name] = {}
        for proc in cat.processes:
            event_counts[cat.name][proc] = hdict["{0}/{1}/{2}".format(
                proc, cat.name, cat.discriminator
            )].Integral()
    
    #catname -> file name
    category_files = {}

    #save the histograms into per-category files
    print "saving categories"
    for catname in hdict_cat.keys():
        hfile = "{0}.root".format(catname)
        print "saving {0} histograms to {1}".format(len(hdict_cat[catname]), hfile)
        category_files[catname] = hfile
        sparse.save_hdict(hfile, hdict_cat[catname])
    
    #add the fake data
    if analysis.do_fake_data:
        print "adding fake data"
        for cat in categories:
            hfile = category_files[cat.name]
            tf = ROOT.TFile(hfile, "UPDATE")
            fakeData(tf, tf, [cat])
            tf.Close()

    #add the stat variations
    if analysis.do_stat_variations:
        print "adding stat variations"
        from utils import makeStatVariations
        for cat in categories:
            hfile = category_files[cat.name]
            tf = ROOT.TFile(hfile, "UPDATE")
            stathist_names = makeStatVariations(tf, tf, [cat])
            tf.Close()
            
            #add the statistical uncertainties to the datacard specification
            for proc in cat.processes:
                for syst in stathist_names[cat.name][proc]:
                    cat.shape_uncertainties[proc][syst] = 1.0
                
    from utils import PrintDatacard
    #make datacards for individual categories 
    for cat in categories:
        if not cat.do_limit:
            continue
        fn = "shapes_{0}.txt".format(cat.full_name)
        print "writing shape file {0}".format(fn)
        dcof = open(fn, "w")
        PrintDatacard([cat], event_counts, category_files, dcof)
        dcof.write("# execute with\n")
        dcof.write("# combine -n {0} -M Asymptotic -t -1 {1}\n".format(cat.name, os.path.basename(fn)))
        dcof.close()

    
