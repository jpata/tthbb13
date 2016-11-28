import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

from rq import Queue
from redis import Redis
from rq import push_connection, get_failed_queue, Queue, Worker
from job import count, sparse, plot, makecategory, makelimits, mergeFiles
import socket

import time, os, sys
import shutil
from collections import Counter
import uuid
import cPickle as pickle

import subprocess

import ROOT
from TTH.MEAnalysis.samples_base import getSitePrefix, chunks
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Analysis
from TTH.Plotting.Datacards.MakeCategory import make_datacard
from TTH.Plotting.Datacards.sparse import add_hdict

import TTH.Plotting.joosep.plotlib as plotlib #heplot, 

import matplotlib
from matplotlib import rc
#temporarily disable true latex for fast testing
rc('text', usetex=False)
matplotlib.use('PS') #needed on T3
import matplotlib.pyplot as plt

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
    

def start_jobs(queue, njobs, extra_requirements = [], redis_host=None, redis_port=None):

    if redis_host is None:
        redis_host = socket.gethostname()
    if redis_port is None:
        redis_port = 6379

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
    qsub_command.append("redis://{0}:{1}".format(redis_host, redis_port))

    for _ in range(njobs):
        subprocess.Popen(qsub_command, 
                         stdout=subprocess.PIPE).communicate()[0] 
    print "waiting 30s for jobs to be run..."
    time.sleep(30)

def basic_job_status(jobs):
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
    sys.stdout.write("\033[F") # Cursor up one line

def waitJobs(jobs, redis_conn, qmain, qfail, num_retries=0, callback=basic_job_status):
    done = False
    istep = 0
    perm_failed = []
    workflow_failed = False

    while not done:
        logger.debug("queues: main({0}) failed({1})".format(len(qmain), len(qfail)))
        logger.debug("--- all")
        
        for job in jobs:
            #logger.debug("id={0} status={1} meta={2}".format(job.id, job.status, job.meta))
            if job.status == "failed":
                if job.meta["retries"] < num_retries:
                    job.meta["retries"] += 1
                    logger.info("requeueing job {0}".format(job.id))
                    logger.error("job error: {0}".format(job.exc_info))
                    qfail.requeue(job.id)
                else:
                    perm_failed += [job]
                    raise Exception("job failed: {0}".format(job.exc_info))
            if job.status is None:
                raise Exception("Job status is None")
            if job.status == "finished":
                key = (job.func.func_name, job.meta["args"])
                if job.meta["args"] != "": 
                    hkey = hash(str(key))
                    if not redis_conn.exists(hkey):
                        logger.debug("setting key {0} in db".format(hkey))
                        redis_conn.set(hkey, pickle.dumps(job.result))
        
        status = [j.status for j in jobs]
        status_counts = dict(Counter(status))

        if len(perm_failed) > 0:
            logger.error("--- fail queue has {0} items".format(len(qfail)))
            for job in qfail.jobs:
                workflow_failed = True
                logger.error("job {0} failed with message:\n{1}".format(job.id, job.exc_info))
                qfail.remove(job.id)
        
        if status_counts.get("started", 0) == 0 and status_counts.get("queued", 0) == 0:
            done = True
            break

        time.sleep(1)
        
        if not callback is None:
            callback(jobs)
        istep += 1

    if workflow_failed:
        raise Exception("workflow failed, see errors above")
    results = [j.result for j in jobs]
    return results

class JobMemoize:
    """
    Fake job instance with manually configured properties
    """
    def __init__(self, result, func, args, meta):
        self.result = result
        self.status = "finished"
        self.func = func
        self.args = args
        self.meta = meta

def enqueue_nomemoize(queue, **kwargs):
    return queue.enqueue_call(**kwargs)

def enqueue_memoize(queue, **kwargs):
    """
    Check if result already exists in redis DB and return it or compute it.
    """
    key = (kwargs.get("func").func_name, kwargs.get("meta")["args"])
    hkey = hash(str(key))
    logger.debug("checking for key {0} -> {1}".format(hkey, str(key)))
    if redis_conn.exists(hkey):
        res = pickle.loads(redis_conn.get(hkey))
        logger.debug("found key {0}, res={1}".format(hkey, res))
        return JobMemoize(res, kwargs.get("func"), kwargs.get("args"), kwargs.get("meta"))
    else:
        logger.debug("didn't find key, enqueueing")
        return queue.enqueue_call(**kwargs)

class Task(object):
    def __init__(self, workdir, name, analysis):
        self.workdir = workdir
        self.name = name
        self.analysis = analysis

    def run(self, inputs, redis_conn, qmain, qfail):
        jobs = {}
        return jobs

    def get_analysis_config(self, workdir = None):
        if not workdir:
            workdir = self.workdir
        return os.path.join(workdir, "analysis.pickle")

    def save_state(self):
        self.analysis.serialize(self.get_analysis_config())

    def load_state(self, workdir):
        self.analysis = self.analysis.deserialize(
            self.get_analysis_config(workdir)
        )

class TaskNumGen(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskNumGen, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        all_jobs = []
        jobs = {}
        for sample in self.analysis.samples:
            _jobs = TaskNumGen.getGeneratedEvents(sample, qmain)
            jobs[sample.name] = _jobs
            all_jobs += _jobs

        #synchronize
        waitJobs(all_jobs, redis_conn, qmain, qfail, 0)

        for sample in analysis.samples:
            ngen = sum(
                [j.result["Count"] for j in jobs[sample.name]]
            )
            sample.ngen = int(ngen)
        self.save_state()
        return jobs

    @staticmethod
    def getGeneratedEvents(sample, queue):
        jobs = []
        for ijob, inputs in enumerate(chunks(sample.file_names, sample.step_size_sparsinator)):
            jobs += [
                enqueue_memoize(
                    queue,
                    func = count,
                    args = (inputs, ),
                    timeout = 2*60*60,
                    ttl = 2*60*60,
                    result_ttl = 2*60*60,
                    meta = {"retries": 0, "args": str((inputs, ))}
                )
            ]
        logger.info("getGeneratedEvents: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
        return jobs

class TaskSparsinator(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskSparsinator, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        all_jobs = []
        jobs = {}
        for sample in self.analysis.samples:
            if not sample.name in [p.input_name for p in self.analysis.processes]:
                logging.info("Skipping sample {0} because matched to no process".format(
                    sample.name
                ))
                continue
            jobs[sample.name] = TaskSparsinator.runSparsinator_async(
                self.get_analysis_config(workdir),
                sample,
                self.workdir
            )
            all_jobs += jobs[sample.name]
        logger.info("waiting on sparsinator jobs")
        waitJobs(all_jobs, redis_conn, qmain, qfail, callback=self.status_callback)
        self.save_state()
        return jobs

    @staticmethod
    def status_callback(jobs):

        basic_job_status(jobs)

        res = []
        samples = set()
        for job in jobs:
            sample_name = job.args[2]
            k = (sample_name, job.status)
            samples.add(sample_name)
            res += [k]

        res = dict(Counter(res))
        res_by_sample = {sample: {"queued": 0, "started": 0, "finished": 0} for sample in samples}
        for k in res.keys():
            res_by_sample[k[0]][k[1]] = res[k]
        
        stat = open("status.md", "w")
        for sample in sorted(samples):
            s = "| " + sample + " | "
            s += " | ".join([str(res_by_sample[sample][k]) for k in ["queued", "started", "finished"]])
            stat.write(s + "\n")
        stat.close()

    @staticmethod
    def runSparsinator_async(config_path, sample, workdir):
        jobs = []
        for ijob, inputs in enumerate(chunks(sample.file_names, sample.step_size_sparsinator)):
            ofname = "{0}/sparse/{1}/sparse_{2}.root".format(
                workdir, sample.name, ijob
            )
            jobs += [
                enqueue_memoize(
                    qmain,
                    func = sparse,
                    args = (config_path, inputs, sample.name, ofname),
                    timeout = 2*60*60,
                    ttl = 2*60*60,
                    result_ttl = 2*60*60,
                    meta = {"retries": 2, "args": str((inputs, sample.name))}
                )
            ]
        logger.info("runSparsinator: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
        return jobs

class TaskSparseMerge(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskSparseMerge, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        all_jobs = []
        jobs_by_sample = {}

        for sample in analysis.samples:
            
            if not sample.name in inputs.keys():
                continue

            sample_results = [os.path.abspath(job.result) for job in inputs[sample.name]]
            logger.info("sparsemerge: submitting merge of {0} files for sample {1}".format(len(sample_results), sample.name))
            outfile = os.path.abspath("{0}/sparse/sparse_{1}.root".format(workdir, sample.name))
            job = enqueue_memoize(
                qmain,
                func = mergeFiles,
                args = (outfile, sample_results),
                timeout = 20*60,
                result_ttl = 60*60,
                meta = {"retries": 0, "args": sample.name}
            )
            jobs_by_sample[sample.name] = job
            all_jobs += [job]
        waitJobs(all_jobs, redis_conn, qmain, qfail, callback=TaskSparseMerge.status_callback)
        results = [j.result for j in all_jobs]
        logger.info("sparsemerge: merging final sparse out of {0} files".format(len(results)))
        final_merge = os.path.abspath("{0}/merged.root".format(workdir))
        job = enqueue_memoize(
            qmain,
            func = mergeFiles,
            args = (final_merge, results),
            timeout = 20*60,
            result_ttl = 60*60,
            meta = {"retries": 0, "args": ("final", final_merge, results)}
        )
        waitJobs([job], redis_conn, qmain, qfail, callback=TaskSparseMerge.status_callback)
        self.save_state()
        return final_merge

    @staticmethod
    def status_callback(jobs):

        basic_job_status(jobs)

        res = []
        samples = set()
        for job in jobs:
            sample_name = job.args[0]
            k = (sample_name, job.status)
            samples.add(sample_name)
            res += [k]

        res = dict(Counter(res))
        res_by_sample = {sample: {"queued": 0, "started": 0, "finished": 0} for sample in samples}
        for k in res.keys():
            res_by_sample[k[0]][k[1]] = res[k]
        
        stat = open("status.md", "w")
        for sample in sorted(samples):
            s = "| " + sample + " | "
            s += " | ".join([str(res_by_sample[sample][k]) for k in ["queued", "started", "finished"]])
            stat.write(s + "\n")
        stat.close()
class TaskCategories(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskCategories, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        hdict = {}

        logging.info("Opening {0}".format(inputs))
        tf = ROOT.TFile(inputs)
        ROOT.gROOT.cd()
        for k in tf.GetListOfKeys():

            #check if this is a valid histogram according to its name
            if len(k.GetName().split("__")) >= 3:
                hdict[k.GetName()] = k.ReadObj().Clone()

        #make all the datacards for all the categories
        for cat in self.analysis.categories:
            category_dir = "{0}/categories/{1}/{2}".format(
                workdir, cat.name, cat.discriminator.name
            )
            logging.info("creating category to {0}".format(category_dir))
            os.makedirs(category_dir)
            make_datacard(self.analysis, [cat], category_dir, hdict)

        # hadd Results        
        cat_names = list(set([cat.name for cat in self.analysis.categories]))        

        for cat_name in cat_names:                                                        
            logger.info("hadd-ing: {0}".format(cat_name))
            
            process = subprocess.Popen(
                "hadd {0}/categories/{1}.root {0}/categories/{1}/*/*.root".format(workdir, cat_name),
                shell=True,
                stdout=subprocess.PIPE
            )
            process.communicate()

        # move the shape text files into the right place
        process = subprocess.Popen(
            "mv {0}/categories/*/*/*.txt {0}/categories/".format(workdir),
            shell=True,
            stdout=subprocess.PIPE
        )

        time.sleep(1) #NFS

        result = "{0}/categories".format(workdir)
        self.save_state()
        return result

class TaskPlotting(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskPlotting, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):
        from plots import run_plots
       
        run_plots(
            workdir,
            analysis,
            inputs,
            redis_conn,
            qmain,
            qfail
        )

class TaskLimits(Task):
    def __init__(self, workdir, name, analysis):
        super(TaskLimits, self).__init__(workdir, name, analysis)

    def run(self, inputs, redis_conn, qmain, qfail):

        # Prepare jobs
        all_jobs = []
        for group in self.analysis.groups.keys():
            all_jobs += [
                qmain.enqueue_call(
                    func = makelimits,
                    args = [
                        "{0}/limits".format(workdir),
                        self.analysis,
                        group
                    ],
                    timeout = 40*60,
                    result_ttl = 60*60,
                    meta = {"retries": 0, "args": ""})]
            
        waitJobs(all_jobs, redis_conn)
        self.save_state()

def make_workdir():
    workflow_id = uuid.uuid4()
    workdir = "results/{0}".format(workflow_id)
    os.makedirs(workdir)
    return workdir

if __name__ == "__main__":
    workdir = make_workdir()

    logger.info("starting workflow {0}".format(workdir))

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
        '--port',
        action = "store",
        help = "Redis port",
        type = int,
        default = 6379
    )
    parser.add_argument(
        '--queue',
        action = "store",
        help = "Job queue",
        type = str,
        default = "EXISTING"
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
        default = 200
    )
    args = parser.parse_args()

    queue_kwargs = {}
    if args.queue == "SYNC":
        queue_kwargs["async"] = False
    # Tell RQ what Redis connection to use
    redis_conn = Redis(host=args.hostname, port=args.port)
    qmain = Queue("default", connection=redis_conn, **queue_kwargs)  # no args implies the default queue
    qfail = get_failed_queue(redis_conn)
    
    #clean queues in case they are full
    if len(qmain) > 0:
        logging.warning("main queue has jobs, emptying")
        qmain.empty()

    if len(qfail) > 0:
        logging.warning("fail queue has jobs, emptying")
        qfail.empty()

    analysis = analysisFromConfig(args.config)

    tasks = []
    tasks += [
        TaskNumGen(workdir, "NGEN", analysis),
        TaskSparsinator(workdir, "SPARSE", analysis),
        TaskSparseMerge(workdir, "MERGE", analysis),
        TaskCategories(workdir, "CAT", analysis),
        TaskPlotting(workdir, "PLOT", analysis),
    ]

    inputs = []
    for task in tasks:
        res = task.run(inputs, redis_conn, qmain, qfail)
        inputs = res