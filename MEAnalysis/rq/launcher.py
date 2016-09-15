from rq import Queue
from redis import Redis
from rq import push_connection, get_failed_queue, Queue
from job import count, sparse

import time, os, sys
import shutil
from collections import Counter
import uuid
import logging

import ROOT
from TTH.MEAnalysis.samples_base import getSitePrefix, chunks
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Analysis
from TTH.Plotting.Datacards import MakeCategory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

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
        status_counts = dict(Counter(status))

        sys.stdout.write("\033[K") # Clear this line
        sys.stdout.write("\033[92mstatus\033[0m {3:.2f}%\tq={0}\ts={1}\tf={2}\n".format(
            status_counts.get("queued", 0),
            status_counts.get("started", 0),
            status_counts.get("finished", 0),
            100.0 * status_counts.get("finished", 0) / sum(status_counts.values()),
        ))

        if len(qfail)>0:
            logger.error("--- failed")
        for job in qfail.jobs:
            workflow_failed = True
            logger.error("job {0} failed with message:\n{1}".format(job.id, job.exc_info))
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
                result_ttl=86400,
            )
        ]
    logger.debug("getGeneratedEvents: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
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

def runSparsinator_async(sample, workdir):
    jobs = []
    for ijob, inputs in enumerate(chunks(sample.file_names, sample.step_size_sparsinator)):
        ofname = "{0}/sparse/{1}/sparse_{2}.root".format(
            workdir, sample.name, ijob
        )
        jobs += [
            qmain.enqueue_call(
                func=sparse,
                args=(inputs, sample.name, ofname),
                timeout=60*60,
                result_ttl=86400,
                meta={"retries": 0}
            )
        ]
    logger.debug("runSparsinator: {0} jobs launched for sample {1}".format(len(jobs), sample.name))
    return jobs

if __name__ == "__main__":
    workflow_id = uuid.uuid4()
    workdir = "results/{0}".format(workflow_id)
    os.makedirs(workdir)

    logger.info("starting workflow {0}".format(workflow_id))

    # Tell RQ what Redis connection to use
    redis_conn = Redis(host="t3ui17.psi.ch")
    qmain = Queue("default", connection=redis_conn)  # no args implies the default queue
    qfail = get_failed_queue(redis_conn)
    
    #clean queues in case they are full
    if len(qmain) > 0:
        logging.warning("main queue has jobs, emptying")
        qmain.empty()

    if len(qfail) > 0:
        logging.warning("fail queue has jobs, emptying")
        qfail.empty()

    conf_file_name = sys.argv[1]
    tmp_conf_name = "{0}/analysis.cfg".format(workdir)
    analysis_name, analysis_cfg = analysisFromConfig(conf_file_name)
    
    config_parser = Analysis.getConfigParser(conf_file_name)
    
    jobs = {}
    results = {}

    ###
    ### NGEN
    ###
    logger.info("starting step NGEN")
    t0 = time.time()
    jobs["ngen"] = {}
    all_jobs = []
    for sample in analysis_cfg.samples:
        _jobs = getGeneratedEvents(sample)
        jobs["ngen"][sample.name] = _jobs
        all_jobs += _jobs

    #synchronize
    waitJobs(all_jobs, 0)

    for sample in analysis_cfg.samples:
        ngen = sum(
            [j.result["Count"] for j in jobs["ngen"][sample.name]]
        )
        sample.ngen = int(ngen)
        #propagate this change to the config parser
        sample.updateConfig(config_parser)

    #save configuration, re-initialize parser
    with open(tmp_conf_name, "wb") as configfile:
        config_parser.write(configfile)
    config_parser = Analysis.getConfigParser(tmp_conf_name)

    #reload the analysis from the updated configuration
    analysis_name, analysis_cfg = analysisFromConfig(tmp_conf_name)
    t1 = time.time()
    dt = t1 - t0
    logging.info("step NGEN done in {0:.2f} seconds".format(dt))

    ###
    ### SPARSINATOR
    ###
    
    logger.info("starting step SPARSINATOR")
    t0 = time.time()
    jobs["sparse"] = {}
    results["sparse"] = []

    all_jobs = []
    for ds in analysis_cfg.samples:
        jobs["sparse"][ds] = runSparsinator_async(ds, workdir)
        all_jobs += jobs["sparse"][ds]
    logger.info("waiting on sparsinator jobs")
    waitJobs(all_jobs)
    #just in case to make sure NFS is synced
    t1 = time.time()
    time.sleep(5)
    dt = t1 - t0
    logging.info("step SPARSINATOR done in {0:.2f} seconds".format(dt))

    ###
    ### SPARSE MERGE
    ###
    logger.info("starting step SPARSEMERGE")
    for ds in analysis_cfg.samples:
        ds_results = ["file://" + job.result for job in jobs["sparse"][ds]]
        results["sparse"] += [
            mergeFiles(
                "file://" + os.path.abspath("{0}/sparse/sparse_{1}.root".format(workdir, ds.name)),
                ds_results,
                remove_inputs = True
            )
        ]
    results["sparse-merge"] = mergeFiles(
        "file://" + os.path.abspath("{0}/sparse/merged.root".format(workdir)),
        results["sparse"],
        remove_inputs = True
    )
   
    logger.info("step SPARSEMERGE done")

    ###
    ### CATEGORIES
    ###
    logger.info("starting step CATEGORIES")
    t0 = time.time()

    logger.info("running categories on file {0}".format(results["sparse-merge"]))
    analysis_cfg.sparse_input_file = results["sparse-merge"]

    all_jobs = []
    cats_by_name = {}
    for cat in analysis_cfg.categories:
        if not cats_by_name.has_key(cat.name):
            cats_by_name[cat.name] = []
        cats_by_name[cat.name] += [cat]
    os.makedirs("{0}/categories".format(workdir))
    for catname, cats in cats_by_name.items(): 
        all_jobs += [
            qmain.enqueue_call(
                func=MakeCategory.main,
                args=(analysis_cfg, cats, "{0}/categories".format(workdir), 1),
                timeout=20*60,
                result_ttl=86400,
                meta={"retries": 0}
            )
        ]
    waitJobs(all_jobs)
    t1 = time.time()
    time.sleep(5)
    dt = t1 - t0
    logger.info("step CATEGORIES done in {0:.2f} seconds".format(dt))
    
    logger.info("all done, len(qmain)={0} len(qfail)={1}".format(
        len(qmain), len(qfail)
    ))
