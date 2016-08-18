from rq import Queue
from redis import Redis
from rq import push_connection, get_failed_queue, Queue
from job import count, sparse

import time, os
from collections import Counter
import ROOT
from TTH.MEAnalysis.samples_base import getSitePrefix

import uuid
workflow_id = uuid.uuid4()

# Tell RQ what Redis connection to use
redis_conn = Redis(host="t3ui17.psi.ch")
qmain = Queue(connection=redis_conn)  # no args implies the default queue
qfail = Queue("failed", connection=redis_conn)  # no args implies the default queue

def getFileNames(sample_file):
    data = open(sample_file)
    files = []
    for line in data.readlines():
        fn = line.split()[0]
        if "/store" in fn:
            files += [fn]
    return files

def waitJobs(jobs):
    done = False
    istep = 0
    while not done:
        status = [j.status for j in jobs]
        status_counts = Counter(status)
        print status_counts
        if status_counts.get("failed", 0) == len(jobs):
            raise Exception("all jobs failed")
        if status_counts.get("started", 0) == 0 and status_counts.get("queued", 0) == 0:
            done = True
            break
        time.sleep(1)
        istep += 1
    results = [j.result for j in jobs]
    return results

def getGeneratedEvents(sample_file):
    inputs = getFileNames(sample_file)

    jobs = []
    print "launching jobs"
    for ijob, inp in enumerate(inputs):
        jobs += [
            qmain.enqueue_call(
                func=count,
                args=([inp, ], ),
                timeout=60*10
            )
        ]
    print "{0} jobs launched".format(len(jobs))
    waitJobs(jobs) 
    total = 0
    for res in results:
        total += res["Count"]
    return total

def runSparsinator(sample_file):
    sample = sample_file.split("/")[-1].split(".")[0]
    inputs = getFileNames(sample_file)
    inputs = map(getSitePrefix, inputs)
    jobs = []
    for ijob, inp in enumerate(inputs):
        ofname = "/mnt/t3nfs01/data01/shome/jpata/tth/sw/CMSSW/src/TTH/MEAnalysis/rq/results/{0}/{1}/sparse_{2}.root".format(workflow_id, sample, ijob)
        jobs += [
            qmain.enqueue_call(
                func=sparse,
                args=([inp, ], sample, ofname),
                timeout=20*60
            )
        ]
    print "{0} jobs launched".format(len(jobs))
    results = waitJobs(jobs)

    merger = ROOT.TFileMerger()
    outfile = "results/{0}/sparse_{1}.root".format(workflow_id, sample)
    merger.OutputFile(outfile)
    for res in results:
        merger.AddFile(res)
    merger.Merge()
    for res in results:
        os.remove(res)
    return outfile

datasets = [
    "../gc/datasets/Aug11_leptonic_nome_v1/ttHTobb_M125_13TeV_powheg_pythia8.txt",
    "../gc/datasets/Aug11_leptonic_nome_v1/ttHToNonbb_M125_13TeV_powheg_pythia8.txt",
    "../gc/datasets/Aug11_leptonic_nome_v1/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",
    "../gc/datasets/Aug11_leptonic_nome_v1/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.txt",
    "../gc/datasets/Aug11_leptonic_nome_v1/TT_TuneCUETP8M1_13TeV-powheg-pythia8.txt",
]

results = {}
for ds in datasets:
    ds_name = ds.split("/")[-1].split(".")[0]
    runSparsinator(ds)
    #ret = getGeneratedEvents(ds)
    #results[ds_name] = ret 
print results

print "all done, len(qmain)={0} len(qfail)={1}".format(
    len(qmain), len(qfail)
)
