from rq import Queue
from redis import Redis
from rq import push_connection, get_failed_queue, Queue
from job import count, sparse

import time, os
from collections import Counter
import uuid
import logging

import ROOT
from TTH.MEAnalysis.samples_base import getSitePrefix
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.Plotting.Datacards import MakeCategory

def getFileNames(sample_file):
    data = open(sample_file)
    files = []
    for line in data.readlines():
        fn = line.split()[0]
        if "/store" in fn:
            files += [fn]
    return files

class Dataset:
    def __init__(self, **kwargs):
        self.input_files = kwargs.get("input_files")
        self.sample = kwargs.get("sample")
        self.step_size = kwargs.get("step_size")

    @staticmethod
    def from_dataset_file(dsfile, nmax=-1, step_size={"sparse": 1}):
        sample = dsfile.split("/")[-1].split(".")[0]
        inputs = getFileNames(dsfile)
        inputs = map(getSitePrefix, inputs)
        if nmax > 0:
            inputs = inputs[:nmax]
        return Dataset(input_files=inputs, sample=sample, step_size=step_size)


def waitJobs(jobs, num_retries=3):
    done = False
    istep = 0
    perm_failed = []
    workflow_failed = False
    while not done:
        logger.debug("queues: main({0}) failed({1})".format(len(qmain), len(qfail)))
        logger.debug("--- all")
        for job in jobs:
            logger.debug("id={0} status={1} meta={2}".format(job.id, job.status, job.meta))
            if job.status == "failed":
                if job.meta["retries"] < num_retries:
                    job.meta["retries"] += 1
                    qfail.requeue(job.id)
                else:
                    perm_failed += [job]
            if job.status is None:
                import pdb
                pdb.set_trace()
        status = [j.status for j in jobs]
        status_counts = Counter(status)
        print status_counts 
        if len(qfail)>0:
            logger.info("--- failed")
        for job in qfail.jobs:
            workflow_failed = True
            logger.info("job {0} failed with message:\n{1}".format(job.id, job.exc_info))
            qfail.remove(job.id)
        
        if status_counts.get("started", 0) == 0 and status_counts.get("queued", 0) == 0:
            done = True
            break
        time.sleep(1)
        istep += 1
    if workflow_failed:
        raise Exception("workflow failed, see errors above")
    results = [j.result for j in jobs]
    return results

def getGeneratedEvents(sample_file):
    inputs = getFileNames(sample_file)

    jobs = []
    logger.info("launching jobs")
    for ijob, inp in enumerate(inputs):
        jobs += [
            qmain.enqueue_call(
                func=count,
                args=([inp, ], ),
                timeout=60*10,
                result_ttl=86400,
            )
        ]
    logger.info("{0} jobs launched".format(len(jobs)))
    waitJobs(jobs, 0) 
    total = 0
    for res in results:
        total += res["Count"]
    return total

def mergeFiles(outfile, infiles, remove_inputs=True):
    if len(infiles) == 1:
        logger.info("copying output to {0}".format(outfile))
        shutil.copy(infiles[0], outfile)
    else:
        logger.info("merging output to {0}".format(outfile))
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

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def runSparsinator_async(dataset):
    jobs = []
    for ijob, inputs in enumerate(chunks(dataset.input_files, dataset.step_size["sparse"])):
        ofname = "/mnt/t3nfs01/data01/shome/jpata/tth/sw/CMSSW/src/TTH/MEAnalysis/rq/results/{0}/sparse/{1}/sparse_{2}.root".format(workflow_id, dataset.sample, ijob)
        jobs += [
            qmain.enqueue_call(
                func=sparse,
                args=(inputs, dataset.sample, ofname),
                timeout=60*60,
                result_ttl=86400,
                meta={"retries": 0}
            )
        ]
    logger.info("{0} async jobs launched for dataset {1}".format(len(jobs), dataset.sample))
    return jobs

if __name__ == "__main__":
    workflow_id = uuid.uuid4()
    
    # Tell RQ what Redis connection to use
    redis_conn = Redis(host="t3ui17.psi.ch")
    qmain = Queue("default", connection=redis_conn)  # no args implies the default queue
    qfail = get_failed_queue(redis_conn)
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("main")
    
    datasets = [
        Dataset.from_dataset_file("../gc/datasets/Sep13_testing_v1/ttHTobb_M125_13TeV_powheg_pythia8.txt", nmax=-1, step_size={"sparse": 1}),
        Dataset.from_dataset_file("../gc/datasets/Sep13_testing_v1/TT_TuneCUETP8M1_13TeV-powheg-pythia8.txt", nmax=-1, step_size={"sparse": 1}),
    ]
   
    jobs = {}
    jobs["sparse"] = {}
    results = {}
    results["sparse"] = []

    all_jobs = []
    for ds in datasets:
        jobs["sparse"][ds] = runSparsinator_async(ds)
        all_jobs += jobs["sparse"][ds]
    
    waitJobs(all_jobs)
    time.sleep(10)

    for ds in datasets:
        ds_results = ["file://" + job.result for job in jobs["sparse"][ds]]
        results["sparse"] += [
            mergeFiles(
                "file://" + os.path.abspath("results/{0}/sparse/sparse_{1}.root".format(workflow_id, ds.sample)),
                ds_results,
                remove_inputs = True
            )
        ]
    results["sparse-merge"] = mergeFiles(
        "file://" + os.path.abspath("results/{0}/sparse/merged.root".format(workflow_id)),
        results["sparse"],
        remove_inputs = True
    )
    
    name, analysis = analysisFromConfig(
        os.path.join(os.environ["CMSSW_BASE"],
            "src/TTH/Plotting/python/Datacards",
            "config_sl.cfg"
        )
    )
    analysis.sparse_input_file = results["sparse-merge"]
    all_jobs = []
    cats_by_name = {}
    for cat in analysis.categories:
        if not cats_by_name.has_key(cat.name):
            cats_by_name[cat.name] = []
        cats_by_name[cat.name] += [cat]
    os.makedirs("results/{0}/categories".format(workflow_id))
    for catname, cats in cats_by_name.items(): 
        all_jobs += [
            qmain.enqueue_call(
                func=MakeCategory.main,
                args=(analysis, cats, "results/{0}/categories".format(workflow_id), 1),
                timeout=20*60,
                result_ttl=86400,
                meta={"retries": 0}
            )
        ]
    waitJobs(all_jobs)
    
    logger.info("all done, len(qmain)={0} len(qfail)={1}".format(
        len(qmain), len(qfail)
    ))
