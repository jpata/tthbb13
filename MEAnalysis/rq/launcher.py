import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

from rq import Queue
from redis import Redis
from rq import push_connection, get_failed_queue, Queue, Worker
from job import count, sparse, plot, makecategory, makelimits
import socket

import time, os, sys
import shutil
from collections import Counter
import uuid

import subprocess

import ROOT
from TTH.MEAnalysis.samples_base import getSitePrefix, chunks
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Analysis

import pdb

import TTH.Plotting.joosep.plotlib as plotlib #heplot, 

import matplotlib
from matplotlib import rc
#temporarily disable true latex for fast testing
rc('text', usetex=False)
matplotlib.use('PS') #needed on T3
import matplotlib.pyplot as plt


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

procs_names = [
    ("ttH_hbb", "tt+H(bb)"),
    ("ttH_nonhbb", "tt+H(non-bb)"),
    ("ttbarOther", "tt+light"),
    ("ttbarPlusBBbar", "tt+bb"),
    ("ttbarPlus2B", "tt+2b"),
    ("ttbarPlusB", "tt+b"),
    ("ttbarPlusCCbar", "tt+cc"),
]
procs = [x[0] for x in procs_names]

syst_pairs = []


####
# Configuation
####

def kill_jobs():

    proc = subprocess.Popen("qstat -u $USER | grep 'rq_worker'",
                     shell=True,
                     stdout=subprocess.PIPE)
    out = proc.communicate()[0]

    jobs = []
    for line in out.split("\n"):
        if not line:
            continue
        jobs.append(line.split(" ")[0])
        
    for job in jobs:
        subprocess.Popen("qdel {0}".format(job),
                         shell=True,
                         stdout=subprocess.PIPE).communicate()       
    

def start_jobs(queue, njobs, extra_requirements = []):
    
    pwd = os.getcwd()

    qsub_command = ["qsub", 
                    "-q", queue,
                    "-N", "rq_worker", 
                    "-wd", pwd, 
                    "-o", pwd+"/logs/", 
                    "-e", pwd+"/logs/"]
                    
    if extra_requirements:
        qsub_command += extra_requirements

    qsub_command.append("worker.sh")

    for _ in range(njobs):    
        subprocess.Popen(qsub_command,                         
                         stdout=subprocess.PIPE).communicate()[0] 
    print "waiting 30s for jobs to be run..."
    time.sleep(30)


def get_base_plot(basepath, outpath, analysis, category, variable):
    

    s = "{0}/{1}/{2}".format(basepath, analysis, category)
    return {
        "infile": s + ".root",
        "histname": "/".join([category, variable]),
        "outname": "/".join([outpath, category, variable]),
        "procs": procs_names,
        "signal_procs": ["ttH_hbb"],
        "dataname": "data", #data_obs for fake data
        "rebin": 1,
        "xlabel": plotlib.varnames[variable] if variable in plotlib.varnames.keys() else "PLZ add me to Varnames",
        "xunit": plotlib.varunits[variable] if variable in plotlib.varunits.keys() else "",
        "legend_fontsize": 12,
        "legend_loc": "best",
        "colors": [plotlib.colors.get(p) for p in procs],
        "do_legend": True,
        "show_overflow": True,
        "title_extended": r"$,\ \mathcal{L}=17\ \mathrm{fb}^{-1}$, ",
        "systematics": syst_pairs,
        "do_syst": False, #currently crashes with True due to some dvipng/DISPLAY issue
        "blindFunc": "blind_mem" if "common" in variable else "no_blind",
    }



def waitJobs(jobs, redis_conn, num_retries=0):
    done = False
    istep = 0
    perm_failed = []
    workflow_failed = False

    workers = Worker.all(connection=redis_conn)
    n_workers = len(workers) 
    logger.info("waitJobs: {0} active workers".format(n_workers))

    while not done:
        logger.debug("queues: main({0}) failed({1})".format(len(qmain), len(qfail)))
        logger.debug("--- all")
        
        workers = Worker.all(connection=redis_conn)
        if n_workers != len(workers):
            raise Exception("some workers died, aborting workflow")

        for job in jobs:
            #logger.debug("id={0} status={1} meta={2}".format(job.id, job.status, job.meta))
            if job.status == "failed":
                if job.meta["retries"] < num_retries:
                    job.meta["retries"] += 1
                    logger.debug("requeueing job {0}".format(job.id))
                    qfail.requeue(job.id)
                else:
                    perm_failed += [job]
            if job.status is None:
                raise Exception("Job status is None")

        status = [j.status for j in jobs]
        status_counts = dict(Counter(status))

        sys.stdout.write("\033[K") # Clear this line
        sys.stdout.write("\033[92mstatus\033[0m {4:.2f}%\tq={0}\ts={1}\tf={2}\tE={3}\n".format(
            status_counts.get("queued", 0),
            status_counts.get("started", 0),
            status_counts.get("finished", 0),
            status_counts.get("failed", 0),
            100.0 * status_counts.get("finished", 0) / sum(status_counts.values()),
        ))

        if len(qfail)>0 or len(perm_failed)>0:
            logger.error("--- fail queue has {0} items".format(len(qfail)))
            for job in qfail.jobs:
                workflow_failed = True
                logger.error("job {0}, call={1} failed with message:\n{2}".format(job.id, job.get_call_string(), job.exc_info))
                qfail.remove(job.id)
        
        if status_counts.get("started", 0) == 0 and status_counts.get("queued", 0) == 0:
            done = True
            break

        time.sleep(1)
        
        sys.stdout.write("\033[F") # Cursor up one line

        istep += 1

    if workflow_failed:
        raise Exception("workflow failed, see errors above")
    results = [j.result for j in jobs]
    return results

def getGeneratedEvents(sample):
    jobs = []
    for ijob, inputs in enumerate(chunks(sample.file_names, sample.step_size_sparsinator)):
        jobs += [
            qmain.enqueue_call(
                func=count,
                args=(inputs, ),
                timeout=60*10,
                result_ttl=60*60,
                meta={"retries": 0}
            )
        ]
    logger.info("getGeneratedEvents: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
    return jobs

def mergeFiles(outfile, infiles, remove_inputs=True):
    if len(infiles) == 1:
        logger.debug("copying output to {0}".format(outfile))
        shutil.copy(infiles[0], outfile)
    else:
        logger.debug("merging output to {0}".format(outfile))
        merger = ROOT.TFileMerger(False)
        merger.OutputFile(outfile)
        for res in infiles:
            logger.debug("adding file {0}".format(res))
            merger.AddFile(res, False)
        merger.Merge()
    if remove_inputs:
        for res in infiles:
            if os.path.isfile(res):
                os.remove(res)
    return outfile

def runSparsinator_async(config_path, sample, workdir):
    jobs = []
    for ijob, inputs in enumerate(chunks(sample.file_names, sample.step_size_sparsinator)):
        ofname = "{0}/sparse/{1}/sparse_{2}.root".format(
            workdir, sample.name, ijob
        )
        jobs += [
            qmain.enqueue_call(
                func=sparse,
                args=(config_path, inputs, sample.name, ofname),
                timeout=60*60,
                result_ttl=60*60,
                meta={"retries": 0}
            )
        ]
    logger.info("runSparsinator: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
    return jobs

if __name__ == "__main__":
    workflow_id = uuid.uuid4()
    workdir = "results/{0}".format(workflow_id)
    os.makedirs(workdir)

    logger.info("starting workflow {0}".format(workflow_id))

    starting_points = ["ngen", "sparse", "categories", "plots", "limits"]
    
    import argparse
    parser = argparse.ArgumentParser(
        description='Runs the workflow'
    )
    parser.add_argument(
        '--config',
        action = "store",
        help = "Analysis configuration",
        type = str,
        required = True
    )
    parser.add_argument(
        '--hostname',
        action = "store",
        help = "Redis hostname",
        type = str,
        default = socket.gethostname()
    )
    parser.add_argument(
        '--queue',
        action = "store",
        help = "Job queue",
        type = str,
        default = "short.q"
    )
    parser.add_argument(
        '--start',
        action = "store",
        help = "Starting point",
        type = str,
        choices = starting_points,
        default = "ngen"
    )
    parser.add_argument(
        '--njobs',
        action = "store",
        help = "Job queue",
        type = int,
        default = 100
    )
    args = parser.parse_args()

    # Tell RQ what Redis connection to use
    redis_conn = Redis(host=args.hostname)
    qmain = Queue("default", connection=redis_conn)  # no args implies the default queue
    qfail = get_failed_queue(redis_conn)
    
    #clean queues in case they are full
    if len(qmain) > 0:
        logging.warning("main queue has jobs, emptying")
        qmain.empty()

    if len(qfail) > 0:
        logging.warning("fail queue has jobs, emptying")
        qfail.empty()

    tmp_conf_name = "{0}/analysis.cfg".format(workdir)
    analysis_name, analysis = analysisFromConfig(args.config)

    logger.info("starting point is:".format(args.start))
    
    jobs = {}
    results = {}

    ###
    ### NGEN
    ###
    if starting_points.index(args.start) <= starting_points.index("ngen"):

        if args.queue != "EXISTING":
            kill_jobs()
            start_jobs(args.queue, args.njobs)

        logger.info("starting step NGEN")
        t0 = time.time()
        jobs["ngen"] = {}
        all_jobs = []
        for sample in analysis.samples:
            _jobs = getGeneratedEvents(sample)
            jobs["ngen"][sample.name] = _jobs
            all_jobs += _jobs

        #synchronize
        waitJobs(all_jobs, redis_conn, 0)

        for sample in analysis.samples:
            ngen = sum(
                [j.result["Count"] for j in jobs["ngen"][sample.name]]
            )
            sample.ngen = int(ngen)
            #propagate this change to the config parser
            sample.updateConfig(analysis.config)

        #save configuration, re-initialize parser
        with open(tmp_conf_name, "wb") as configfile:
            analysis.config.write(configfile)
        analysis.config = Analysis.getConfigParser(tmp_conf_name)

        #reload the analysis from the updated configuration
        analysis_name, analysis = analysisFromConfig(tmp_conf_name)
        t1 = time.time()
        dt = t1 - t0
        logging.info("step NGEN done in {0:.2f} seconds".format(dt))
 
        if args.queue != "EXISTING":
            kill_jobs()        
    else:

        logger.info("skipping step NGEN")
        
        logger.info("Verifying ngen is set")
        for sample in analysis.samples:
            logger.info("{0}: {1}".format(sample.name, sample.ngen))

        # Copy the cfg also to the new output (for reference)
        with open(tmp_conf_name, "wb") as configfile:
            analysis.config.write(configfile)                        

    ###
    ### SPARSINATOR
    ###
                        
    if starting_points.index(args.start) <= starting_points.index("sparse"):

        if args.queue != "EXISTING":
            kill_jobs()
            start_jobs(args.queue, args.njobs)

        logger.info("starting step SPARSINATOR")
        t0 = time.time()
        jobs["sparse"] = {}
        results["sparse"] = []

        all_jobs = []
        for ds in analysis.samples:
            jobs["sparse"][ds] = runSparsinator_async(tmp_conf_name, ds, workdir)
            all_jobs += jobs["sparse"][ds]
        logger.info("waiting on sparsinator jobs")
        waitJobs(all_jobs, redis_conn)
        #just in case to make sure NFS is synced
        t1 = time.time()
        time.sleep(5)
        dt = t1 - t0
        logging.info("step SPARSINATOR done in {0:.2f} seconds".format(dt))

        if args.queue != "EXISTING":
            kill_jobs()

        ###
        ### SPARSE MERGE
        ###
        logger.info("starting step SPARSEMERGE")
        for ds in analysis.samples:
            ds_results = [os.path.abspath(job.result) for job in jobs["sparse"][ds]]
            logger.info("sparsemerge: merging {0} files for sample {1}".format(len(ds_results), ds.name))
            results["sparse"] += [
                mergeFiles(
                    os.path.abspath("{0}/sparse/sparse_{1}.root".format(workdir, ds.name)),
                    ds_results,
                    remove_inputs = True
                )
            ]
        results["sparse-merge"] = mergeFiles(
            os.path.abspath("{0}/sparse/merged.root".format(workdir)),
            results["sparse"],
            remove_inputs = True
        )
        analysis.config.set("sparse_data", "infile", results["sparse-merge"])
        with open(tmp_conf_name, "wb") as configfile:
            analysis.config.write(configfile)

        logger.info("step SPARSEMERGE done")

    else:
        logger.info("skipping steps SPARSINATOR & SPARSEMERGE" )

        # If we skipped sparse, we would assume that the output is in
        # the same directory as the cfg file
        results["sparse-merge"] = analysis.config.get("sparse_data", "infile")

    
    ###
    ### CATEGORIES
    ###

    if starting_points.index(args.start) <= starting_points.index("categories"):

        if args.queue != "EXISTING":
            kill_jobs()
            start_jobs(args.queue, 50, ["-l", "h_vmem=5G"])

        logger.info("starting step CATEGORIES")
        t0 = time.time()

        logger.info("running categories on file {0}".format(results["sparse-merge"]))
        analysis.sparse_input_file = results["sparse-merge"]

        os.makedirs("{0}/categories".format(workdir))

        all_jobs = []
        for cat in analysis.categories:

            os.makedirs("{0}/categories/{1}/{2}".format(workdir, cat.name, cat.discriminator))

            all_jobs += [
                qmain.enqueue_call(
                    func=makecategory,
                    args=(tmp_conf_name, [cat], "{0}/categories/{1}/{2}".format(workdir, cat.name, cat.discriminator)),
                    timeout=20*60,
                    result_ttl=60*60,
                    meta={"retries": 0}
                )
            ]
        waitJobs(all_jobs, redis_conn)
        t1 = time.time()
        time.sleep(5)
        dt = t1 - t0
        logger.info("step CATEGORIES done in {0:.2f} seconds".format(dt))

        logger.info("all done, len(qmain)={0} len(qfail)={1}".format(
            len(qmain), len(qfail)
        ))

        # hadd Results        
        cat_names = list(set([cat.name for cat in analysis.categories]))        

        for cat_name in cat_names:                                                        
            logger.info("hadd-ing: {0}".format(cat_name))
            
            process = subprocess.Popen( "hadd {0}/categories/{1}.root {0}/categories/{1}/*/*.root".format(workdir, cat_name),
                                        shell=True,
                                        stdout=subprocess.PIPE)
            process.communicate()

        # move the shape text files into the right place
        process = subprocess.Popen( "mv {0}/categories/*/*/*.txt {0}/categories/".format(workdir),
                                    shell=True,
                                    stdout=subprocess.PIPE)        

        # and tidy up
        for cat_name in cat_names:                                                                
            shutil.rmtree("{0}/categories/{1}".format(workdir, cat_name))

        results["categories-path"] = "{0}/categories".format(workdir)

        logger.info("done with post processing CATEGORIES")
        
        if args.queue != "EXISTING":
            kill_jobs()

    else:        
        logger.info("skipping step CATEGORIES")

        # If we skipped categories, we would assume that the output is in
        # the same directory as the cfg file
        results["categories-path"] = os.path.join(os.path.dirname(args.config), "categories")


    ###
    ### PLOTTING
    ###
        
    if starting_points.index(args.start) <= starting_points.index("plots"):

        if args.queue != "EXISTING":
            kill_jobs()
            start_jobs(args.queue, args.njobs)

        logger.info("starting step PLOTS")
        t0 = time.time()

        logger.info("running plotting on directory {0}".format(results["categories-path"]))

        all_jobs = []

        for cat in analysis.categories:

            all_jobs += [
                qmain.enqueue_call(
                    func=plot,
                    args=[get_base_plot(results["categories-path"], 
                                        os.path.join(workdir, "plots"),
                                        "", cat.name, cat.discriminator)],
                    timeout=20*60,
                    result_ttl=60*60,
                    meta={"retries": 0}
                )
            ]

        t0 = time.time()
        waitJobs(all_jobs, redis_conn)
        t1 = time.time()
        time.sleep(5)
        dt = t1 - t0
        logger.info("step PLOTS done in {0:.2f} seconds".format(dt))

        if args.queue != "EXISTING":
            kill_jobs()

    else:        
        logger.info("skipping step PLOTS")


    ###
    ### LIMITS
    ###
        
    if starting_points.index(args.start) <= starting_points.index("limits"):

        if args.queue != "EXISTING":
            kill_jobs()
            start_jobs(args.queue, args.njobs)

        logger.info("starting step LIMITS")

        # Limits are based on categories
        # copy categories to the right place
        shutil.copytree(results["categories-path"], "{0}/limits".format(workdir))

        # Add individual limits for all categories
        for cat in analysis.categories:
            if cat.do_limit:
                analysis.groups[cat.name] = [cat]
        
        # Prepare jobs
        all_jobs = []
        for group in analysis.groups.keys():
            all_jobs += [
                qmain.enqueue_call(
                    func=makelimits,
                    args=["{0}/limits".format(workdir),
                          tmp_conf_name,
                          group],
                    timeout=40*60,
                    result_ttl=60*60,
                    meta={"retries": 0})]
            
        t0 = time.time()
        waitJobs(all_jobs, redis_conn)
        t1 = time.time()
        time.sleep(5)
        dt = t1 - t0
        logger.info("step LIMITS done in {0:.2f} seconds".format(dt))
        
        if args.queue != "EXISTING":
            kill_jobs()
