from TTH.TTHNtupleAnalyzer.CrabHelpers import hadd_from_file, replicate
import argparse, subprocess, glob, os

version = "X"

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--action',
    choices=['status', 'submit', 'report', 'hadd', 'replicate'], type=str,
    required=True,
    help="the action to perform"
)

args = parser.parse_args()

jobs = ["confs/sig.conf", "confs/bkg.conf"]
#gc = "/shome/jpata/grid-control/GC"
gc = "./grid-control/go.py"

if args.action == "status":
    for job in jobs:
        print job
        subprocess.call([gc, job, "-qs"])
        subprocess.call([gc, job, "-r"])
if args.action == "submit":
    for job in jobs:
        subprocess.call([gc, job, "-q"])
if args.action == "report":
    for job in jobs:
        subprocess.call([gc, job, "-r"])
if args.action == "hadd":
    completed_files = []
    input_filenames = []
    for job in jobs:
        wd = "work." +job.split("/")[-1].split(".")[0]
        donefiles = glob.glob(wd + "/output/*/output.txt")
        for df in donefiles:
            input_filenames += map(lambda x: x.strip(), open(df).readlines())
    datasets = {}

    for inf in input_filenames:
        spl = inf.split("/")
        spl = filter(lambda x: len(x)>0, spl)
        dataset = spl[-2]
        fn = inf
        if not datasets.has_key(dataset):
            datasets[dataset] = []
        datasets[dataset] += [inf]

    for (dataset, input_filenames) in datasets.items():
        output_filename = "/scratch/" + os.environ["USER"] + "/" + dataset + ".root"
        print "merging {0} files for dataset {1} -> {2}".format(len(input_filenames), dataset, output_filename)
        for inf in input_filenames:
            print inf
        subprocess.call(["python", os.environ["CMSSW_BASE"] + "/src/TTH/TTHNtupleAnalyzer/python/ParHadd.py", output_filename] + input_filenames)
        completed_files += [output_filename]

    repl_files = open("to-replica.txt", "w")
    for cf in completed_files:
        repl_files.write(cf + "\n")
    repl_files.close()
#end hadd
if args.action == "replicate":
    if not os.path.isfile("to-replica.txt"):
        raise FileError("file to-replica.txt does not exist, create it using --action=hadd")
    replicate("to-replica.txt", "T3_CH_PSI", "/store/user/jpata/tth/" + version)
    replicate("to-replica.txt", "T2_EE_Estonia", "/store/user/jpata/tth/" + version)
