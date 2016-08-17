from rq import Queue
from redis import Redis
from rq import push_connection, get_failed_queue, Queue
from job import myjob
import time

# Tell RQ what Redis connection to use
redis_conn = Redis(host="t3ui17.psi.ch")
q = Queue(connection=redis_conn)  # no args implies the default queue
qfail = Queue("failed", connection=redis_conn)  # no args implies the default queue

inputs = ["/store/user/jpata/tth/Aug11_leptonic_nome_v1/ttHTobb_M125_13TeV_powheg_pythia8/Aug11_leptonic_nome_v1/160811_213359/0000/tree_{0}.root".format(i) for i in range(10)]
jobs = [
    q.enqueue_call(func=myjob, args=(inp, ), timeout=120)
    for inp in inputs
]

def get_job_status(job):
    """
    Returns a number giving the status of the job.
    job (rq job): the job to check
    returns (int): 0  if successful, 1 if failed, -1 if running
    """
    stat = -1
    res = job.result
    if not res is None and not job.is_failed:
        stat = 0
    elif job.is_failed:
        stat = 1 
    return stat

done = False
istep = 0
while not done:
    status = []
    for job in jobs:
        stat = get_job_status(job)
        status += [stat]
    n_good = status.count(0)
    n_failed = status.count(1)
    n_running = status.count(-1)

    print istep, n_good, n_failed, status
    if n_running == 0:
        done = True

    time.sleep(5)
    istep += 1

results = [j.result for j in jobs]
print results
print "all done, len(q)={0} len(qfail)={1}".format(
    len(q), len(qfail)
)
