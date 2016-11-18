import json, copy, os, imp, multiprocessing, sys
import sparse, ROOT
import logging
from utils import fakeData
import os
import os.path
import fnmatch
import time
import itertools
import gc

#Nota bene: this is very important!
#need to store histograms in memory, not on disk
ROOT.TH1.AddDirectory(False)
ROOT.gROOT.SetBatch(True)

def make_rule_cut(infile, basehist, category, processes):
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
    for proc in processes:
        cuts = []
        cuts += category.cuts
        for c in proc.cuts:
            cuts += c.sparsinator

        d = {
            "infile": infile,
            "input": "{0}/{1}".format(proc.input_name, basehist),
            "cuts": str(cuts),
            "project": str([(category.discriminator, category.rebin)]),
            "output": "{0}/{1}/{2}".format(proc.output_name, category.name, category.discriminator),
            "xs_weight": proc.xs_weight
        }
        rules += [d]
    
        if proc not in category.data_processes:
            #make systematic variations
            systdict = category.shape_uncertainties[proc.output_name]
            for systname, systsize in systdict.items():
                for direction in ["Up", "Down"]:
                    d2 = copy.deepcopy(d)
                    d2["input"] += "_" + systname + direction
                    d2["output"] += "_" + systname + direction
                    rules += [d2]
    
        rules += [d]
    return rules

def apply_rules(args):
    """
    The worker function for the histogram projection rules.
    args (tuple): (input filename, list of rules) to apply

    Returns: a dictionary with the output histograms
    """

    input_map, rules = args
    hdict = {}

    t0 = time.time()
    logging.info("apply_rules: len(rules)={0}".format(len(rules)))
    for rule in rules:
        #convert the string of the cut list into the actual list
        cuts = eval(rule["cuts"])
        hk = rule["output"]
        inp = str(rule["input"])
        logging.debug("apply_rules: histogram {0} => {1} with rule {2}".format(inp, hk, rule))
        sparse_hist = input_map[inp]

        #in case no histogram could be found, use a dummy histogram so that we
        #have at least the correct binning
        dummy = False
        if not sparse_hist:
            dummy = True
            logging.warning("Could not get histogram {0}, using fallback".format(inp))
            sparse_hist = input_map["dummy"]
            if not sparse_hist:
                raise Exception("Could not get fallback histogram {0}".format("ttHTobb_M125_13TeV_powheg_pythia8/sl/sparse"))
            cuts = []

        variables = eval(rule["project"])
        vnames = [v[0] for v in variables]
        ret = sparse.apply_cuts_project(sparse_hist, cuts, vnames)

        #dummy histogram needs to be made empty
        if dummy:
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

        logging.debug("apply_rules: {2}: N={0} I={1}".format(ret.GetEntries(), ret.Integral(), hk))

        if hdict.has_key(hk):
            hdict[hk] += ret
        else:
            hdict[hk] = ret
    t1 = time.time()
    logging.info("apply_rules: projected {0} rules in {1} seconds: {2} r/s".format(len(rules), t1-t0, len(rules)/float(t1-t0)))
    return hdict

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def apply_rules_parallel(rules):
    """
    Project out all the histograms according to the projection rules.
    infile (string) - path to input root file with sparse histograms
    rules (list of dicts) - all the rules
    
    Optional:
    """ 
    
    rets = {}
    if len(rules) == 0:
        logging.error("no rules!")
        return rets

    #split rules into unique batches by input histogram
    rules_per_input = {}
    for rule in rules:
        infile = rule["infile"]
        inp = rule["input"]
        if not rules_per_input.has_key((infile, inp)):
            rules_per_input[(infile, inp)] = []
        rules_per_input[(infile, inp)].append(rule)
   
    infile_dummy = ROOT.TFile.Open(rules[0]["infile"])
    dummy_h = infile_dummy.Get(rules[0]["input"]).Clone()
    dummy_h.Reset()

    #process batches
    for (infile, inp), rules_batch in rules_per_input.items():
    
        infile_tf = ROOT.TFile.Open(infile)
        
        if not infile_tf:
            raise FileError("Could not open file: {0}".format(infile))
       
        print infile, rules_batch[0]["input"]
        
        # preload THnSparse here, once per input, in order to prevent memory leak, see
        # https://github.com/jpata/tthbb13/issues/107
        input_map = {
            "dummy": dummy_h,
            inp: infile_tf.Get(inp)
        }
        logging.info("apply_rules_parallel: applying {0} rules for input {1}".format(
            len(rules_batch),
            inp
        ))

        #process in chunks of 100
        for chunk in chunks(sorted(rules_batch, key=lambda x: x["output"]), 100):
            ret = apply_rules((input_map, chunk))
            rets = sparse.add_hdict(rets, ret)
    
        input_map[inp].Delete()

        infile_tf.Close()

    return rets

def get_categories(analysis_spec, analysis_name, category_name):
    #load the python analysis specification
    logging.info("main: importing {0}".format(analysis_spec))
    anspec = imp.load_source("anspec", analysis_spec)
        
    # Limit to one analysis/category
    logging.info("main: loading analysis {0}".format(analysis_name))
    analysis = anspec.analyses[analysis_name]
    categories = [c for c in analysis.categories if fnmatch.fnmatch(c.name, category_name)]

    logging.info("main: matched categories: {0}".format(str([s.full_name for s in categories])))

    if len(categories) == 0:
        raise Exception("Could not match any categories")
    return analysis, categories

def make_rules(analysis, infile, categories, processes=None):
    rules = []
    for cat in categories:
        logging.debug("main: making rules for category={0} discr={1}".format(
            cat.name, cat.discriminator
        ))
        _processes = processes
        if processes is None:
            _processes = cat.processes + cat.data_processes
        rules += make_rule_cut(infile, cat.src_histogram, cat, _processes)

    return rules

def main(analysis, categories, outdir="."):
    
    rules = make_rules(analysis, analysis.sparse_input_file, categories)

    #project out all the histograms
    logging.info("main: applying {0} rules".format(len(rules)))
    hdict = apply_rules_parallel(rules)
    return make_datacard(analysis, categories, outdir, hdict)

def make_datacard(analysis, categories, outdir, hdict):
    #split the big dictionary to category-based dictionaries
    #produce the event counts per category
    logging.info("main: producing event counts")
    event_counts = {}
    hdict_cat = {}
    for cat in categories:
        event_counts[cat.name] = {}
        hdict_cat[cat.name] = {}
        for proc in cat.out_processes:
            k = "{0}__{1}__{2}".format(
                proc, cat.name, cat.discriminator.name
            )
            logging.debug("getting {0}".format(k))
            v = 0.0
            if hdict.has_key(k):
                v = hdict[k].Integral()
                hdict_cat[cat.name][k] = hdict[k].Clone()
            event_counts[cat.name][proc] = v
    import pdb
    pdb.set_trace()
    #catname -> file name
    category_files = {}

    #save the histograms into per-category files
    logging.info("main: saving categories")
    for catname in hdict_cat.keys():
        hfile = os.path.join(outdir, "{0}.root".format(catname))
        logging.debug("saving {0} histograms to {1}".format(
            len(hdict_cat[catname]), hfile)
        )
        category_files[catname] = hfile
        sparse.save_hdict(hfile, hdict_cat[catname])
    
    #add the fake data
    if analysis.do_fake_data:
        logging.info("main: adding fake data")
        for cat in categories:
            hfile = category_files[cat.name]
            tf = ROOT.TFile(hfile, "UPDATE")
            fakeData(tf, tf, [cat])
            tf.Close()

    #add the stat variations
    if analysis.do_stat_variations:
        logging.info("main: adding stat variations")
        from utils import makeStatVariations
        for cat in categories:
            hfile = category_files[cat.name]
            c = ROOT.TFile(hfile, "UPDATE")
            stathist_names = makeStatVariations(tf, tf, [cat])
            tf.Close()
            
            #add the statistical uncertainties to the datacard specification
            for proc in cat.out_processes:
                for syst in stathist_names[cat.name][proc]:
                    cat.shape_uncertainties[proc][syst] = 1.0
                
    from utils import PrintDatacard
    #make combine datacards (.txt) for individual categories 
    for cat in categories:
        if not cat.do_limit:
            continue
        fn = os.path.join(outdir, "shapes_{0}.txt".format(cat.full_name))
        logging.debug("main: writing shape file {0}".format(fn))
        dcof = open(fn, "w")
        PrintDatacard([cat], event_counts, category_files, dcof)
        dcof.write("# execute with\n")
        dcof.write("# combine -n {0} -M Asymptotic -t -1 {1}\n".format(cat.name, os.path.basename(fn)))
        dcof.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    import argparse
    parser = argparse.ArgumentParser(
        description='Creates datacards in categories based on a sparse histogram'
    )
    parser.add_argument(
        '--config',
        action = "store",
        help = "Analysis configuration",
        type = str,
        required = True
    )
    parser.add_argument(
        '--category',
        action = "store",
        help = "name of category or glob pattern",
        default = "*",
    )
    parser.add_argument(
        '--outdir',
        action = "store",
        help = "per-analsyis output directory (will be created)",
        default = "."
    )

    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
    args = parser.parse_args()
    an_name, analysis = analysisFromConfig(args.config)
    
    categories = [
        c for c in analysis.categories if fnmatch.fnmatch(c.full_name, args.category)
    ]
    if len(categories) == 0:
        print "no categories matched out of:"
        print "\n".join([c.full_name for c in analysis.categories])
    main(analysis, categories, outdir=".")
