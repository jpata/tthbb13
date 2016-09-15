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
    for proc in category.processes:
        d = {
            "input": "{0}/{1}".format(proc.input_name, basehist),
            "cuts": str(category.cuts + proc.cuts),
            "project": str([(category.discriminator, category.rebin)]),
            "output": "{0}/{1}/{2}".format(proc.output_name, category.name, category.discriminator),
            "xs_weight": proc.xs_weight
        }
        rules += [d]

        #make systematic variations
        systdict = category.shape_uncertainties[proc.output_name]
        for systname, systsize in systdict.items():
            for direction in ["Up", "Down"]:
                d2 = copy.deepcopy(d)
                d2["input"] += "_" + systname + direction
                d2["output"] += "_" + systname + direction
                rules += [d2]

    for proc in category.data_processes:
        d = {
            "input": "{0}/{1}".format(proc.input_name, basehist),
            "cuts": str(category.cuts + proc.cuts),
            "project": str([(category.discriminator, category.rebin)]),
            "output": "{0}/{1}/{2}".format(proc.output_name, category.name, category.discriminator),
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
            sparse_hist = input_map["ttHTobb_M125_13TeV_powheg_pythia8/sl/sparse"]
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
    inputs = []

    # preload THnSparse here, once per input, in order to prevent memory leak, see
    # https://github.com/jpata/tthbb13/issues/107
    unique_inputs = set([r["input"] for r in rules])
    logging.info("apply_rules_parallel: preloading {0} sparse histograms from {1}".format(
        len(unique_inputs), infile
    ))
    infile_tf = ROOT.TFile.Open(infile)
    if not infile_tf:
        raise FileError("Could not open file: {0}".format(infile))
    input_map = {
        k: infile_tf.Get(k) for k in unique_inputs
    }

    logging.info("apply_rules_parallel: creating chunks")
    #so that we can apply some N rules at the same time
    #sort so that we are creating histograms that end up in the same result
    for chunk in chunks(sorted(rules, key=lambda x: x["output"]), 100):
        inputs += [(input_map, chunk)]
    
    rets = {}
    if ncores > 1:
        rets = reduce(sparse.add_hdict, p.map(apply_rules, inputs), rets)
    else:
        for inp in inputs:
            ret = apply_rules(inp)
            logging.debug("reducing {0}".format(len(ret)))
            rets = sparse.add_hdict(rets, ret)
            logging.debug("len(rets) = {0}".format(len(rets)))
    
    if ncores > 1:
        p.close()
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

def main(analysis, categories, outdir=".", ncores=1):
    # Make all the rules
    rules = []
    for cat in categories:
        logging.debug("main: making rules for category={0} discr={1}".format(
            cat.name, cat.discriminator
        ))
        rules += make_rule_cut(cat.src_histogram, cat)
    
    of = open("rules.json", "w")
    logging.info("writing {0} rules".format(len(rules)))
    of.write(json.dumps(rules, indent=2))
    of.close()

    #project out all the histograms
    logging.info("main: applying {0} rules".format(len(rules)))
    hdict = apply_rules_parallel(analysis.sparse_input_file, rules, ncores)

    #split the big dictionary to category-based dictionaries
    hdict_cat = {}
    for k in hdict.keys():
        catname = k.split("/")[1]
        if not hdict_cat.has_key(catname):
            hdict_cat[catname] = {}
        hdict_cat[catname][k] = hdict[k]

    #produce the event counts per category
    logging.info("main: producing event counts")
    event_counts = {}
    for cat in categories:
        event_counts[cat.name] = {}
        for proc in cat.out_processes:
            event_counts[cat.name][proc] = hdict["{0}/{1}/{2}".format(
                proc, cat.name, cat.discriminator
            )].Integral()
    
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
            tf = ROOT.TFile(hfile, "UPDATE")
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
    
    logging.info("importing default analysis specification")
    from TTH.Plotting.Datacards.AnalysisSpecification import analyses as analyses

    import argparse
    parser = argparse.ArgumentParser(
        description='Creates datacards in categories based on a sparse histogram'
    )
    parser.add_argument(
        '--anspec',
        action="store",
        help="path to file containing analysis specification",
        default=os.path.join(
            os.environ["CMSSW_BASE"],
            "src/TTH/Plotting/python/Datacards/AnalysisSpecification.py"
        ),
    )
    parser.add_argument(
        '--ncores',
        action="store",
        help="number of parallel cores",
        default=1,
        type=int
    )
    parser.add_argument(
        '--analysis',
        action="store",
        help="name of analysis or glob pattern",
        default="*",
        type=str
    )
    parser.add_argument(
        '--category',
        action="store",
        help="name of category or glob pattern",
        default="*",
    )
    parser.add_argument(
        '--outdir',
        action="store",
        help="per-analsyis output directory (will be created)",
        default=r"{analysis}",
    )
    args = parser.parse_args()
    matched_analyses = [an for an in analyses.keys() if fnmatch.fnmatch(an, args.analysis)]
    if len(matched_analyses) == 0:
        raise Exception("No matched analyses")
        
    for analysis_name in matched_analyses:
        outdir = args.outdir.format(analysis=analysis_name)
        logging.info("__main__: analysis {0} to dir {1}".format(analysis_name, outdir))
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        analysis, categories = get_categories(args.anspec, analysis_name, args.category)
        main(analysis, categories, outdir=outdir, ncores=args.ncores)
    
